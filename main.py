import os
from dotenv import load_dotenv
from deepagent.agent import create_compliance_agent
from langsmith import traceable

load_dotenv()

os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "Compliance Agent"

@traceable(name="policy_creation_workflow")
def run_policy_workflow(agent, user_input):
    """Traced workflow for policy creation"""
    return agent.invoke(user_input)

if __name__ == "__main__":
    try:
        print("=" * 80)
        print("🚀 STARTING AUTONOMOUS COMPLIANCE OFFICER")
        print("=" * 80)
        
        # Create agent
        print("\n📋 Initializing agent...")
        agent = create_compliance_agent()
        print("✓ Agent created successfully\n")
        
        # Run with tracing
        print("🔍 Processing request (with LangSmith tracing)...")
        result = run_policy_workflow(agent, {
            "messages": [{
                "role": "user",
                "content": """
Create a comprehensive Data Protection Policy that covers:
1. GDPR compliance requirements
2. HIPAA compliance requirements  
3. SOC2 Type II requirements for data security
4. Internal data handling procedures

Deliver:
- Research findings on all applicable regulations
- Comprehensive policy document
- Legal compliance review
- Security audit findings
- Employee-friendly summary
- Version history log
"""
            }]
        })
        
        print("\n" + "=" * 80)
        print("✅ POLICY CREATION WORKFLOW COMPLETE")
        print("=" * 80)
        
        # Extract result
        if isinstance(result, dict) and "messages" in result:
            last_msg = result["messages"][-1]
            content = last_msg.get("content") if isinstance(last_msg, dict) else last_msg.content
        else:
            content = str(result)
        
        print("\n" + content)
        
        # Output summary
        print("\n" + "=" * 80)
        print("📁 OUTPUT FILES")
        print("=" * 80)
        print("""
CORE DELIVERABLES:
  ✓ workspace/policies/                    - Final Policy Documents
  ✓ workspace/summaries/                   - Employee-Friendly Guides
  ✓ workspace/POLICY_VERSIONS.md           - Master Version Log

RESEARCH & ANALYSIS:
  ✓ workspace/research/                    - Regulatory Requirements
  ✓ workspace/reviews/                     - Legal Compliance Reviews
  ✓ workspace/audits/                      - Security Audit Findings

VERSION CONTROL:
  ✓ workspace/archive/                     - Previous Versions
""")
        print("=" * 80)
        print("✅ Workflow completed!")
        print("📊 View traces: https://smith.langchain.com/")
        print("=" * 80)
        
    except Exception as e:
        import traceback
        print(f"\n❌ ERROR: {e}")
        traceback.print_exc()
        exit(1)