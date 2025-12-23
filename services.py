'''# services.py
import os
from duckduckgo_search import DDGS
from google import genai




GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY environment variable not set")


client = genai.Client(api_key=GEMINI_API_KEY)




def get_market_data(sector: str) -> str:
   
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




def analyze_with_gemini(sector: str, context: str) -> str:


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




def get_market_data(sector: str) -> str:
 
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

