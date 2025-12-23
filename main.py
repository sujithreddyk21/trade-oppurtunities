'''# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from datetime import datetime


# modules
#from services import get_market_data, analyze_with_gemini
from security import verify_token, create_access_token, users_db, pwd_context


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Trade Opportunities API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class LoginRequest(BaseModel):
    username: str
    password: str

class ReportResponse(BaseModel):
    sector: str
    report_markdown: str



@app.post("/login")
def login(creds: LoginRequest):
    """Simple auth to get a token."""
    if creds.username in users_db:
        # Verify password (in a real app)
        if pwd_context.verify(creds.password, users_db[creds.username]):
            token = create_access_token({"sub": creds.username})
            return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/analyze/{sector}")
@limiter.limit("5/minute")  # Rate limit: 5 requests per minute per IP
async def analyze_sector(
    request: Request, 
    sector: str, 
    username: str = Depends(verify_token)
):

    
   
    if not sector.isalpha():
         raise HTTPException(status_code=400, detail="Sector must contain only letters.")

    print(f"Gathering data for {sector}...")
    market_context = get_market_data(sector)
    
    if not market_context:
        raise HTTPException(status_code=500, detail="Failed to fetch market data")

    
    print(f"Analyzing {sector} with Gemini...")
    try:
        markdown_report = analyze_with_gemini(sector, market_context)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI Analysis failed: {str(e)}")

    
    return {
        "sector": sector,
        "generated_at": str(datetime.now()),
        "report": markdown_report
    }

'''# uvicorn main:app --reload

# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from datetime import datetime, timezone

from services import get_market_data, analyze_with_ollama
from security import verify_token, create_access_token, users_db, pwd_context




limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Trade Opportunities API",
    description="Returns structured Markdown trade reports",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)




class LoginRequest(BaseModel):
    username: str
    password: str




@app.post("/login")
def login(creds: LoginRequest):
    """
    Authenticate user and return JWT token
    """
    if creds.username in users_db:
        if pwd_context.verify(
            creds.password,
            users_db[creds.username]
        ):
            token = create_access_token(
                {"sub": creds.username}
            )
            return {
                "access_token": token,
                "token_type": "bearer"
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )




@app.get(
    "/analyze/{sector}",
    response_class=PlainTextResponse
)
@limiter.limit("5/minute")
async def analyze_sector(
    request: Request,
    sector: str,
    username: str = Depends(verify_token)
):

   
    if not sector.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Sector must contain only letters."
        )

   
    print(f"Gathering data for {sector}...")
    market_context = get_market_data(sector)

    if not market_context:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch market data"
        )

    
    print(f"Analyzing {sector} with Ollama...")
    try:
        markdown_report = analyze_with_ollama(
            sector,
            market_context
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI Analysis failed: {str(e)}"
        )

    
    header = f"""# Trade Opportunity Report: {sector.title()}

{datetime.now(timezone.utc).isoformat()}



    return header + markdown_report

