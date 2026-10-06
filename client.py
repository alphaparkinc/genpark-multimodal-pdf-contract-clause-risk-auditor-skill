"""
Multimodal PDF Contract Clause Risk Auditor (Zero External Dependencies)
Parses legal clauses, identifies one-sided indemnification traps, and drafts redline recommendations.
"""
import time
import math
import hashlib
import json
import re
from typing import Dict, Any, List, Optional

RISK_HEURISTICS = [
    {
        "category": "INDEMNIFICATION",
        "pattern": r"(?:indemnify(?:ing)?|hold harmless|defend)[\w\s\-,]{0,100}(?:unlimited|all claims|sole liability)",
        "risk_level": "CRITICAL",
        "score_penalty": 35,
        "recommendation": "Cap indemnification liability to aggregate fees paid in past 12 months."
    },
    {
        "category": "INTELLECTUAL_PROPERTY",
        "pattern": r"(?:exclusive property|all rights, title and interest|work made for hire)[\w\s\-,]{0,80}(?:shall vest exclusively|sole property of customer)",
        "risk_level": "HIGH",
        "score_penalty": 25,
        "recommendation": "Carve out pre-existing background IP and grant non-exclusive license instead of full assignment."
    },
    {
        "category": "AUTO_RENEWAL_EVERGREEN",
        "pattern": r"(?:automatically renew|perpetual|renew(?:s)? for successive)[\w\s\-,]{0,80}(?:unless written notice|30 days prior)",
        "risk_level": "MEDIUM",
        "score_penalty": 15,
        "recommendation": "Require express affirmative mutual consent for contract renewals."
    },
    {
        "category": "UNILATERAL_TERMINATION",
        "pattern": r"(?:terminate(?:s)? for convenience|terminate at any time)[\w\s\-,]{0,80}(?:without penalty|immediately upon written notice)",
        "risk_level": "MEDIUM",
        "score_penalty": 15,
        "recommendation": "Ensure reciprocal 30-day notice and reimbursement for unrecoverable incurred expenses."
    }
]

class MultimodalPDFContractClauseRiskAuditor:
    def __init__(self):
        self.compiled_rules = [
            {
                "category": r["category"],
                "regex": re.compile(r["pattern"], re.IGNORECASE),
                "risk_level": r["risk_level"],
                "penalty": r["score_penalty"],
                "recommendation": r["recommendation"]
            }
            for r in RISK_HEURISTICS
        ]

    def audit_contract_risks(
        self,
        contract_text: str,
        contract_title: str = "Enterprise Master Services Agreement"
    ) -> Dict[str, Any]:
        """Performs clause-by-clause automated risk audit and redline synthesis."""
        findings = []
        total_penalty = 0

        # Split text into paragraphs / clauses
        paragraphs = [p.strip() for p in contract_text.split("\n\n") if len(p.strip()) > 20]
        if not paragraphs:
            paragraphs = [contract_text]

        for p_idx, para in enumerate(paragraphs):
            for rule in self.compiled_rules:
                if rule["regex"].search(para):
                    findings.append({
                        "finding_id": f"RISK-{rule['category'][:4]}-{p_idx+1}",
                        "category": rule["category"],
                        "risk_level": rule["risk_level"],
                        "score_penalty": rule["penalty"],
                        "problematic_clause_excerpt": para[:180] + ("..." if len(para) > 180 else ""),
                        "suggested_redline": rule["recommendation"]
                    })
                    total_penalty += rule["penalty"]

        # Health score: 100 - total penalties, bounded [0, 100]
        health_score = max(0, 100 - total_penalty)
        composite_status = "SAFE" if health_score >= 80 else ("CAUTION" if health_score >= 50 else "CRITICAL_ACTION_REQUIRED")

        return {
            "contract_title": contract_title,
            "overall_health_score": health_score,
            "composite_status": composite_status,
            "total_risk_findings": len(findings),
            "findings": findings
        }

    def generate_redlines(self, audit_result: Dict[str, Any]) -> str:
        """Generates executive legal redline memo in Markdown format."""
        lines = [
            f"# 📜 合同合规审查与红线批注报告: {audit_result['contract_title']}",
            f"**综合合规评分**: `{audit_result['overall_health_score']}/100` ({audit_result['composite_status']})",
            f"**高风险条款总计**: {audit_result['total_risk_findings']} 项",
            "---"
        ]

        for f in audit_result.get("findings", []):
            lines.append(f"### [{f['risk_level']}] {f['category']}")
            lines.append(f"> **原条款片段**: {f['problematic_clause_excerpt']}")
            lines.append(f"**修改建议 / Redline**: {f['suggested_redline']}\n")

        return "\n".join(lines)
