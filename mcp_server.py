"""MCP Server for Multimodal PDF Contract Clause Risk Auditor."""
import sys
import json
import time
from client import MultimodalPDFContractClauseRiskAuditor

auditor = MultimodalPDFContractClauseRiskAuditor()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "audit_contract_clause_risks":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "audit_contract_risks")
    text = args.get("contract_text", "")
    title = args.get("contract_type", "Standard Agreement")

    if action == "audit_contract_risks":
        return auditor.audit_contract_risks(text, contract_title=title)
    elif action == "generate_redlines":
        res = auditor.audit_contract_risks(text, contract_title=title)
        redline_doc = auditor.generate_redlines(res)
        return {"health_score": res["overall_health_score"], "redlines_markdown": redline_doc}
    elif action == "calculate_risk_score":
        res = auditor.audit_contract_risks(text, contract_title=title)
        return {"health_score": res["overall_health_score"], "status": res["composite_status"]}
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        sample_contract = (
            "Section 8. Vendor shall indemnify, hold harmless and defend Customer against all claims with sole liability.\n\n"
            "Section 12. This Agreement will automatically renew for successive one-year periods unless written notice is given."
        )
        res = auditor.audit_contract_risks(sample_contract, "Vendor MSA")
        assert res["total_risk_findings"] == 2
        assert res["overall_health_score"] < 80
        redline = auditor.generate_redlines(res)
        assert "原条款片段" in redline
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "MultimodalPDFContractClauseRiskAuditor", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "audit_contract_clause_risks",
                            "description": "Segment contract clauses, evaluate legal risk heuristics (indemnity, IP, termination, auto-renewal), compute compliance risk score, and generate redline revisions.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["audit_contract_risks", "generate_redlines", "calculate_risk_score"]},
                                    "contract_text": {"type": "string"},
                                    "contract_type": {"type": "string"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
