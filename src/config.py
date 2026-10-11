import os
from pathlib import Path
from dotenv import load_dotenv

# Locate the root directory (up one level from 'src')
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

# Load variables
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    """Centralizes application configuration for multi-provider support."""
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "openai")
    ENV: str = os.getenv("ENV", "development")

    @classmethod
    def validate_keys(cls):
        """Ensures that crucial API keys are present before starting runtime engines."""
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        
        if missing:
            raise ValueError(f"Missing crucial environment settings configuration profiles: {', '.join(missing)}")

settings = Settings()
