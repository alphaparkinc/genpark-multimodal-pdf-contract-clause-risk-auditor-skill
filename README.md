# genpark-multimodal-pdf-contract-clause-risk-auditor-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Skill-blue.svg)](https://genpark.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Enterprise Multi-Modal Contract Clause Risk Auditor & Redline Synthesizer. Scans enterprise MSAs, NDAs, and Vendor SOWs in Tencent Docs, detects high-risk clauses (unlimited indemnity, one-sided IP assignment, perpetual non-compete, evergreen auto-renewal traps), calculates composite risk scores, and generates precise legal redlines.

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
"""Example usage for MultimodalPDFContractClauseRiskAuditor."""
import sys
import json
from client import MultimodalPDFContractClauseRiskAuditor

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Enterprise Legal WorkBuddy Contract Clause Risk Auditor Demo ===")
    auditor = MultimodalPDFContractClauseRiskAuditor()

    draft_contract = """
Section 4: Intellectual Property.
All work product, inventions, and discoveries created under this SOW shall vest exclusively as the sole property of customer.

Section 9: Indemnification.
Vendor shall indemnify, defend and hold harmless the customer from all claims, damages, liabilities and legal costs with unlimited liability.

Section 14: Term and Renewal.
This agreement shall automatically renew for successive twelve-month periods unless written notice is given 90 days prior.
"""

    print("\n--- 1. Auditing Contract Clauses for Structural Legal Risks ---")
    audit = auditor.audit_contract_risks(draft_contract, "Vendor Cloud AI SOW")
    print(f"Contract Health Score: {audit['overall_health_score']}/100 ({audit['composite_status']})")
    print(f"Detected {audit['total_risk_findings']} high-risk clauses.")

    print("\n--- 2. Generating Redlines and Executive Legal Memo ---")
    redlines = auditor.generate_redlines(audit)
    print(redlines)

if __name__ == "__main__":
    main()

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License

Licensed under the [MIT License](LICENSE). Copyright © 2026 GenPark AI.
