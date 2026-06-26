"""
SEEM Skill - Unified Configuration

Central configuration for all API endpoints and default settings.
Import this file to get consistent configuration across the entire skill.

Usage:
    from SEEM.config import SEEM_DEFAULT_CONFIG
    
    config = SEEMConfig(**SEEM_DEFAULT_CONFIG)
"""

# ============================================================
# API Configuration
# ============================================================

# LLM API Configuration (Xiaomi Mimo / OpenAI compatible)
LLM_CONFIG = {
    "api_key": "",  # Set via environment: LLM_API_KEY
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-chat",
}

# Embedding API Configuration (SiliconFlow / OpenAI compatible)
EMBEDDING_CONFIG = {
    "api_key": "",  # Set via environment: MM_ENCODER_API_KEY
    "base_url": "https://api.siliconflow.cn/v1",
    "model": "Qwen/Qwen3-Embedding-8B",
}

# ============================================================
# Default SEEMConfig Parameters
# ============================================================

SEEM_DEFAULT_CONFIG = {
    # LLM Configuration
    "llm_api_key": LLM_CONFIG["api_key"],  # Loaded from config.py
    "llm_model": LLM_CONFIG["model"],
    "llm_base_url": LLM_CONFIG["base_url"],
    
    # Embedding Configuration
    "mm_encoder_api_key": EMBEDDING_CONFIG["api_key"],  # Loaded from config.py
    "mm_encoder_model": EMBEDDING_CONFIG["model"],
    "mm_encoder_base_url": EMBEDDING_CONFIG["base_url"],
    
    # Retrieval Configuration
    "retrieve_strategy": "ppr",  # Options: "dpr", "hybrid_rrf", "ppr"
    "top_k_candidates": 3,      # For integration judgment
    "top_k_chunks": 3,          # For recall
    "top_k_facts": 5,           # Top-K fact triples via vector similarity
    "backfill_chunks": 5,       # Additional chunks for recall
    "rrf_rank_constant": 30,    # RRF smoothing constant
    "ppr_damping": 0.5,         # PPR damping factor (teleport probability)
    
    # Fact Graph Configuration
    "enable_fact_graph": True,
    "entity_similarity_threshold": 0.9,
    
    # Cache Configuration
    "enable_cache": True,
    "cache_max_size": 1000,
    "cache_ttl_seconds": 300,
    
    # Integration Configuration
    "enable_integration": True,
    "integration_window": 5,        # Batch size: accumulate w observations before running integration (1 = immediate, no batching)
}

# ============================================================
# Environment Variable Names
# ============================================================

ENV_VARS = {
    "LLM_API_KEY": "LLM_API_KEY",
    "LLM_BASE_URL": "LLM_BASE_URL",
    "LLM_MODEL": "LLM_MODEL",
    "MM_ENCODER_API_KEY": "MM_ENCODER_API_KEY",
    "MM_ENCODER_BASE_URL": "MM_ENCODER_BASE_URL",
    "MM_ENCODER_MODEL": "MM_ENCODER_MODEL",
}

# ============================================================
# Helper Functions
# ============================================================

def load_api_key_from_env(env_var: str) -> str:
    """Load API key from environment variable"""
    import os
    return os.getenv(env_var, "")


def get_config_from_env() -> dict:
    """Build configuration dictionary from environment variables"""
    import os
    
    config = SEEM_DEFAULT_CONFIG.copy()
    
    # Override with environment variables if set
    if os.getenv(ENV_VARS["LLM_API_KEY"]):
        config["llm_api_key"] = os.getenv(ENV_VARS["LLM_API_KEY"])
    if os.getenv(ENV_VARS["LLM_BASE_URL"]):
        config["llm_base_url"] = os.getenv(ENV_VARS["LLM_BASE_URL"])
    if os.getenv(ENV_VARS["LLM_MODEL"]):
        config["llm_model"] = os.getenv(ENV_VARS["LLM_MODEL"])
    
    if os.getenv(ENV_VARS["MM_ENCODER_API_KEY"]):
        config["mm_encoder_api_key"] = os.getenv(ENV_VARS["MM_ENCODER_API_KEY"])
    if os.getenv(ENV_VARS["MM_ENCODER_BASE_URL"]):
        config["mm_encoder_base_url"] = os.getenv(ENV_VARS["MM_ENCODER_BASE_URL"])
    if os.getenv(ENV_VARS["MM_ENCODER_MODEL"]):
        config["mm_encoder_model"] = os.getenv(ENV_VARS["MM_ENCODER_MODEL"])
    
    return config


# ============================================================
# Quick Start Example
# ============================================================

if __name__ == "__main__":
    import os
    
    print("SEEM Skill Configuration")
    print("=" * 60)
    print()
    
    # Show current configuration
    config = get_config_from_env()
    
    print("LLM Configuration:")
    print(f"  API Key: {config['llm_api_key'][:10]}..." if config['llm_api_key'] else "  API Key: (not set)")
    print(f"  Base URL: {config['llm_base_url']}")
    print(f"  Model: {config['llm_model']}")
    print()
    
    print("Embedding Configuration:")
    print(f"  API Key: {config['mm_encoder_api_key'][:10]}..." if config['mm_encoder_api_key'] else "  API Key: (not set)")
    print(f"  Base URL: {config['mm_encoder_base_url']}")
    print(f"  Model: {config['mm_encoder_model']}")
    print()
    
    print("Environment Variables:")
    for env_name in ENV_VARS.values():
        value = os.getenv(env_name, "(not set)")
        if value and len(value) > 10:
            value = value[:10] + "..."
        print(f"  {env_name}: {value}")
