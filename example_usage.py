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
