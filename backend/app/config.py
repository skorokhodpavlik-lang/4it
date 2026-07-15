from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    app_name: str = "BABЛО - Crypto Trading Bot"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database
    database_url: str = "postgresql://crypto_user:crypto_password@db:5432/crypto_db"
    
    # Redis
    redis_url: str = "redis://redis:6379"
    
    # API Keys - Exchanges
    bybit_api_key: str = ""
    bybit_api_secret: str = ""
    binance_api_key: str = ""
    binance_api_secret: str = ""
    
    # API Keys - Social & Data
    twitter_api_key: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    coingecko_api_key: str = ""
    whale_alert_api_key: str = ""
    
    # AI Models
    openai_api_key: str = ""
    use_openai: bool = True
    use_local_models: bool = True
    ollama_base_url: str = "http://ollama:11434"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Trading Settings
    default_leverage: float = 50.0
    default_risk_percentage: float = 2.0
    confidence_threshold: float = 0.90
    
    # Notifications
    telegram_bot_token: str = ""
    sendgrid_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
