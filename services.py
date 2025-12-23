'''# services.py
import os
from duckduckgo_search import DDGS
from google import genai


# ============================================================
# 1. CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY environment variable not set")

# Initialize Gemini Client (NEW SDK)
client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# 2. MARKET DATA COLLECTION
# ============================================================

def get_market_data(sector: str) -> str:
    """
    Fetches recent market news and context for a given sector
    using DuckDuckGo search.
    """
    try:
        query = f"{sector} sector trade opportunities India market analysis 2024"

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=2)

        context = "\n".join(
            f"- {item.get('title')}: {item.get('body')}"
            for item in results
        )

        return context if context else "Market data unavailable."

    except Exception as e:
        print(f"❌ Search Error: {e}")
        return "Market data unavailable."


# ============================================================
# 3. GEMINI ANALYSIS
# ============================================================

def analyze_with_gemini(sector: str, context: str) -> str:
    """
    Generates a structured Trade Opportunity report
    using Gemini LLM in Markdown format.
    """

    prompt = f"""
You are a Senior Market Analyst.

Analyze the **{sector} sector in India**.

Context Data:
{context}

Generate a detailed Trade Opportunity Report in VALID MARKDOWN.

Include:
1. Market Overview
2. Key Trends
3. Trade Opportunities
4. Risks

Return ONLY raw markdown text.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        raise RuntimeError("AI Analysis failed")

'''
# services.py
from ddgs import DDGS
import ollama


# ============================================================
# 1. LIVE MARKET DATA (RETRIEVAL)
# ============================================================

def get_market_data(sector: str) -> str:
    """
    Fetch latest market-related information using DuckDuckGo.
    Acts as the Retrieval step in RAG.
    """
    try:
        query = f"{sector} sector trade opportunities India market analysis 2024"

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)

        context = "\n".join(
            f"- {item.get('title')}: {item.get('body')}"
            for item in results
        )

        return context if context else "No recent market data found."

    except Exception as e:
        print("❌ Search Error:", e)
        return "No recent market data found."


# ============================================================
# 2. LOCAL LLM ANALYSIS (OLLAMA)
# ============================================================

def analyze_with_ollama(sector: str, context: str) -> str:
    """
    Generates a grounded trade opportunity report using
    a lightweight local LLM with hallucination control.
    """

    prompt = f"""
ROLE:
You are a professional market analyst.

TASK:
Analyze the **{sector} sector in India** using ONLY the information
provided in the context below.

CONTEXT (REAL-TIME DATA):
{context}

STRICT RULES:
- Do NOT add facts outside the given context
- Do NOT guess or assume missing information
- If data is insufficient, clearly state "Data not available"
- Be factual, concise, and professional

OUTPUT FORMAT (VALID MARKDOWN ONLY):
## Market Overview
## Key Trends
## Trade Opportunities
## Risks & Challenges

STYLE:
- Bullet points where possible
- No marketing language
- No exaggeration
- No speculative predictions
"""

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.1,   # 🔥 VERY LOW → minimal hallucination
                "top_p": 0.9,
                "num_ctx": 2048,      # RAM-safe context window
                "repeat_penalty": 1.1
            }
        )

        return response["message"]["content"]

    except Exception as e:
        print("❌ Ollama Error:", e)
        raise RuntimeError("Local AI analysis failed")
