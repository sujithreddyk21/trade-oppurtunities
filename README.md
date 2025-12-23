# Trade-oppurtunities

A secure FastAPI service that analyzes Indian market sectors and returns structured Markdown trade opportunity reports.
The system supports both cloud-based LLMs (Google Gemini) and local LLMs (Ollama), ensuring reliability even when cloud quotas are exhausted

📌 Features

✅ Sector-based market analysis 
✅ Structured Markdown reports 
✅ Live market data retrieval (DuckDuckGo / DDGS)
🌐 Google Gemini API (cloud)
🖥️ Ollama (local, offline)
✅ JWT-based authentication
✅ Rate limiting to prevent abuse
✅ Graceful error handling
✅ Clean, modular codebase

🛠️ Tech Stack
Layer   >>Technology
Backend >>FastAPI
Auth	  >>JWT (python-jose)
Rate Limiting	>> SlowAPI
LLMs	>> Google Gemini, Ollama
Search>>	DuckDuckGo (ddgs)
Language>>	Python 3.10+
Docs>>	Swagger UI
