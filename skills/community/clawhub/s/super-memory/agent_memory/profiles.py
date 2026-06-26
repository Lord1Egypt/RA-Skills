"""Memory Profiles — Preset configurations for different use cases.

Usage:
    from agent_memory import Memory

    # Preset profiles
    mem = Memory(profile="chatbot")    # High recall, fast response
    mem = Memory(profile="knowledge")  # High precision, deep retrieval
    mem = Memory(profile="personal")   # Balanced (default)

    # Custom overrides
    mem = Memory(profile="chatbot", recall_config={"max_results": 20})
"""

# Profile presets
PROFILES = {
    "personal": {
        # Balanced mode — good for personal assistants
        "description": "Balanced mode for personal AI assistants",
        "recall": {
            "max_results": 10,
            "bm25_k1": 1.5,
            "bm25_b": 0.75,
            "rrf_k": 60,
            "parallel_retrieval": True,
        },
        "ingest": {
            "quality_gate": "auto",
            "max_writes_per_topic": 3,
        },
        "store": {
            "cache_size_kb": 16000,
            "wal_checkpoint_interval": 1000,
        },
    },
    "chatbot": {
        # High recall, fast response — good for conversational AI
        "description": "High recall, fast response for chatbots",
        "recall": {
            "max_results": 20,
            "bm25_k1": 2.0,       # Higher k1 = more term frequency emphasis
            "bm25_b": 0.5,        # Lower b = less document length penalty
            "rrf_k": 40,          # Lower k = more weight to top ranks
            "parallel_retrieval": True,
            "feedback_boost": 1.5, # Stronger feedback learning
        },
        "ingest": {
            "quality_gate": "off",  # Accept everything in chat
            "max_writes_per_topic": 10,
        },
        "store": {
            "cache_size_kb": 32000,
            "wal_checkpoint_interval": 2000,
        },
    },
    "knowledge": {
        # High precision, deep retrieval — good for knowledge bases
        "description": "High precision for knowledge management",
        "recall": {
            "max_results": 5,
            "bm25_k1": 1.2,       # Lower k1 = less term frequency saturation
            "bm25_b": 0.9,        # Higher b = stronger length normalization
            "rrf_k": 80,          # Higher k = more uniform rank fusion
            "parallel_retrieval": True,
            "feedback_penalty": 0.3, # Stronger negative feedback
        },
        "ingest": {
            "quality_gate": "strict",  # Only high-quality memories
            "max_writes_per_topic": 5,
        },
        "store": {
            "cache_size_kb": 16000,
            "wal_checkpoint_interval": 500,
        },
    },
    "enterprise": {
        # Enterprise mode — compliance, audit, multi-tenant
        "description": "Enterprise mode with compliance and audit focus",
        "recall": {
            "max_results": 10,
            "bm25_k1": 1.5,
            "bm25_b": 0.75,
            "rrf_k": 60,
            "parallel_retrieval": True,
        },
        "ingest": {
            "quality_gate": "auto",
            "max_writes_per_topic": 5,
        },
        "store": {
            "cache_size_kb": 32000,
            "wal_checkpoint_interval": 500,
        },
    },
}


def get_profile(name: str) -> dict:
    """Get a profile preset by name.

    Args:
        name: Profile name ("personal", "chatbot", "knowledge", "enterprise")

    Returns:
        Profile configuration dict

    Raises:
        ValueError: If profile name is not recognized
    """
    if name not in PROFILES:
        available = ", ".join(PROFILES.keys())
        raise ValueError(f"未知配置 '{name}'。可选: {available}")
    return PROFILES[name]


def merge_profile(profile_name: str, overrides: dict = None) -> dict:
    """Merge a profile preset with user overrides.

    Args:
        profile_name: Profile name
        overrides: User-provided overrides (deep merged)

    Returns:
        Merged configuration dict
    """
    config = get_profile(profile_name)

    if not overrides:
        return config

    # Deep merge
    result = dict(config)
    for key, value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = {**result[key], **value}
        else:
            result[key] = value

    return result
