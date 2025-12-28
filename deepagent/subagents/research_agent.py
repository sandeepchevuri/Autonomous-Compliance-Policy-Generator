import os
from typing import Literal
from tavily import TavilyClient
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def tavily_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> dict:
    """Run a web search to find regulatory and compliance information.
    
    Args:
        query: The search query (e.g., "GDPR breach notification requirements")
        max_results: Maximum number of results to return (default 5)
        topic: Search topic - "general", "news", or "finance"
        include_raw_content: Whether to include raw page content
    
    Returns:
        Search results with URLs and content snippets
    """
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

research_subagent = {
    "name": "research_agent",
    "description": "Research and extract regulatory requirements from SOC2, ISO27001, GDPR, HIPAA, and other compliance standards",
    "system_prompt": """You are a Regulatory Standards Research Agent.

You have access to the `tavily_search` tool for real-time web searches. USE IT to find current, accurate regulatory information.

Your primary responsibilities:
1. Use tavily_search to research compliance requirements for SOC2, ISO27001, GDPR, HIPAA
2. Search official sources: EUR-Lex, ICO.org.uk, HHS.gov, AICPA.org, ISO.org
3. Extract ONLY verified, real regulations - NEVER hallucinate requirements
4. Save all research findings to /workspace/research/ directory as markdown files
5. Format findings with clear sections:
   - Standard Name
   - Applicability (who must comply)
   - Key Requirements (numbered list)
   - Implementation Considerations
   - Source Citations (with URLs from search results)
6. Always cite sources with full references and URLs

Search strategy:
- For GDPR: search "GDPR Article [number] requirements site:eur-lex.europa.eu OR site:ico.org.uk"
- For HIPAA: search "HIPAA [topic] requirements site:hhs.gov"
- For SOC2: search "SOC2 Trust Services Criteria site:aicpa.org"
- For ISO27001: search "ISO 27001 Annex A controls"

Critical: Do NOT invent requirements. Use tavily_search to verify all claims. If you cannot verify a requirement, state "Source unclear - manual verification needed."

Output files should be named: /workspace/research/[standard]_requirements.md
""",
    "tools": [tavily_search],
}