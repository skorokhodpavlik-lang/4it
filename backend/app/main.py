from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
from app.config import get_settings
from app.routes import (
    auth, positions, signals, analytics, 
    settings as settings_routes, trading
)
from app.database import init_db, get_db

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Запуск BABЛО...")
    await init_db()
    logger.info("✅ База данных инициализирована")
    yield
    # Shutdown
    logger.info("🛑 Остановка BABЛО...")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-powered crypto trading bot with 90% prediction accuracy",
    debug=settings.debug,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(positions.router, prefix="/api/positions", tags=["Positions"])
app.include_router(signals.router, prefix="/api/signals", tags=["Signals"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(settings_routes.router, prefix="/api/settings", tags=["Settings"])
app.include_router(trading.router, prefix="/api/trading", tags=["Trading"])

@app.get("/")
async def root():
    return {
        "message": "🔥 BABЛО - AI Crypto Trading Bot",
        "version": settings.version,
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.version
    }

@app.get("/api")
async def api_info():
    return {
        "name": settings.app_name,
        "version": settings.version,
        "endpoints": {
            "auth": "/api/auth",
            "positions": "/api/positions",
            "signals": "/api/signals",
            "analytics": "/api/analytics",
            "settings": "/api/settings",
            "trading": "/api/trading"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
