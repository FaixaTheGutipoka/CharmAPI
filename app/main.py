from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.routes import router, limiter

app = FastAPI(
    title="Flirt-as-a-Service",
    description="Context-aware flirt line generator",
    version="1.0"
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too much rizz. Slow down."}
    )

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "ai": False}
