"""Topic domain classification and source routing for SCRY skill."""

from typing import Dict, List, Tuple

DOMAIN_KEYWORDS: Dict[str, Dict[str, list]] = {
    "tech": {
        "exact": ["AI", "ML", "LLM", "GPU", "API", "SDK", "CLI", "IDE", "SaaS", "CSS", "HTML",
                  "SQL", "DNS", "CDN", "CI", "CD", "NPM", "AWS", "GCP", "K8S"],
        "contains": [
            "programming", "software", "developer", "code", "framework", "database",
            "cloud", "kubernetes", "docker", "react", "python", "javascript", "typescript",
            "rust", "golang", "devops", "frontend", "backend", "claude", "openai",
            "anthropic", "chatgpt", "llama", "gemini", "copilot", "vscode", "neovim",
            "linux", "macos", "android", "ios", "swift", "kotlin", "flutter", "nextjs",
            "svelte", "tailwind", "webpack", "vite", "bun", "deno", "node",
            "microservice", "serverless", "terraform", "ansible", "nginx",
            "postgresql", "mongodb", "redis", "graphql", "rest api",
            "machine learning", "deep learning", "neural network", "transformer",
            "fine-tun", "rag", "embedding", "vector database", "langchain",
            "agent", "mcp", "tool use",
        ],
    },
    "science": {
        "exact": ["CRISPR", "mRNA", "DNA", "RNA", "NASA", "ESA", "CERN", "NIH", "WHO"],
        "contains": [
            "research", "study", "peer-review", "experiment", "hypothesis",
            "quantum", "physics", "chemistry", "biology", "neuroscience",
            "astronomy", "climate", "genome", "protein", "vaccine",
            "particle", "telescope", "mars", "exoplanet", "fusion",
            "arxiv", "paper", "journal", "preprint",
        ],
    },
    "finance": {
        "exact": ["SEC", "IPO", "ETF", "SPAC", "NYSE", "NASDAQ", "DOW", "GDP", "CPI", "FOMC"],
        "contains": [
            "stock", "market", "trading", "investment", "earnings", "revenue",
            "valuation", "hedge fund", "fed", "inflation", "interest rate",
            "bond", "dividend", "portfolio", "mutual fund", "401k",
            "wall street", "fiscal", "monetary", "recession",
        ],
    },
    "crypto": {
        "exact": ["BTC", "ETH", "SOL", "NFT", "DeFi", "DAO", "USDT", "USDC", "XRP"],
        "contains": [
            "bitcoin", "ethereum", "blockchain", "cryptocurrency", "token",
            "mining", "staking", "wallet", "defi", "smart contract", "web3",
            "solana", "cardano", "polkadot", "cosmos", "layer 2",
            "decentralized", "dex", "yield",
        ],
    },
    "news": {
        "contains": [
            "election", "president", "congress", "senate", "war", "conflict",
            "sanctions", "treaty", "geopolitics", "breaking", "crisis",
            "disaster", "protest", "legislation", "supreme court",
            "nato", "united nations", "diplomacy", "immigration",
            "tariff", "trade war",
        ],
    },
    "entertainment": {
        "contains": [
            "movie", "film", "album", "song", "artist", "concert",
            "tv show", "series", "streaming", "netflix", "spotify",
            "gaming", "game", "esports", "celebrity", "rapper",
            "singer", "actor", "director", "anime", "manga",
            "marvel", "disney", "hbo", "playstation", "xbox", "nintendo",
            "tiktok trend", "viral", "meme",
        ],
    },
}

# Source priority multipliers per domain
DOMAIN_SOURCE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "tech": {
        "hackernews": 1.3, "lobsters": 1.2, "devto": 1.1, "github": 1.3,
        "gitlab": 1.1, "stackoverflow": 1.2, "product_hunt": 1.2,
        "huggingface": 1.1, "reddit": 1.1, "x_twitter": 1.0,
        "bluesky": 1.0, "arxiv": 0.9, "youtube": 0.9,
        "techmeme": 1.2, "mastodon": 0.9,
        "sec_edgar": 0.4, "coingecko": 0.5, "gdelt": 0.5,
        "tiktok": 0.5, "instagram": 0.5, "polymarket": 0.6,
    },
    "science": {
        "arxiv": 1.5, "semantic_scholar": 1.4, "openalex": 1.3,
        "hackernews": 1.0, "wikipedia": 1.2, "reddit": 0.9,
        "devto": 0.5, "github": 0.8, "x_twitter": 0.7,
        "polymarket": 0.4, "tiktok": 0.3, "instagram": 0.3,
        "sec_edgar": 0.3, "coingecko": 0.3,
    },
    "finance": {
        "sec_edgar": 1.5, "polymarket": 1.3, "reddit": 1.1,
        "x_twitter": 1.1, "hackernews": 0.9, "gdelt": 1.1,
        "coingecko": 0.8, "wikipedia": 0.8,
        "arxiv": 0.4, "devto": 0.3, "github": 0.4,
        "lobsters": 0.3, "tiktok": 0.4, "instagram": 0.4,
    },
    "crypto": {
        "coingecko": 1.5, "polymarket": 1.3, "reddit": 1.2,
        "x_twitter": 1.2, "hackernews": 1.0, "github": 0.8,
        "bluesky": 0.7, "youtube": 0.9,
        "sec_edgar": 0.7, "arxiv": 0.5, "devto": 0.5,
        "lobsters": 0.3, "gdelt": 0.6,
    },
    "news": {
        "gdelt": 1.4, "techmeme": 1.2, "reddit": 1.2,
        "x_twitter": 1.3, "bluesky": 1.1, "mastodon": 1.0,
        "polymarket": 1.2, "wikipedia": 1.0, "substack": 1.0,
        "hackernews": 0.8, "youtube": 0.9,
        "arxiv": 0.4, "github": 0.3, "devto": 0.3,
    },
    "entertainment": {
        "x_twitter": 1.4, "tiktok": 1.3, "instagram": 1.3,
        "youtube": 1.3, "reddit": 1.2, "threads": 1.1,
        "substack": 0.9, "bluesky": 0.8, "google_news": 1.1,
        "hackernews": 0.4, "arxiv": 0.2, "sec_edgar": 0.3,
        "github": 0.2, "lobsters": 0.2, "devto": 0.2,
    },
}


def classify_topic(topic: str) -> List[Tuple[str, float]]:
    """Classify topic into domains with confidence scores.

    Returns list of (domain, confidence) sorted by confidence desc.
    Always includes ("general", 0.3) as fallback.
    """
    topic_lower = topic.lower()
    topic_upper = topic.upper()
    words_upper = topic_upper.split()

    scores: Dict[str, float] = {}

    for domain, rules in DOMAIN_KEYWORDS.items():
        score = 0.0
        exact_matches = rules.get("exact", [])
        for term in exact_matches:
            if term in words_upper:
                score += 0.4

        contains_matches = rules.get("contains", [])
        for term in contains_matches:
            if term in topic_lower:
                score += 0.25

        if score > 0:
            scores[domain] = min(1.0, score)

    result = [(d, s) for d, s in scores.items() if s >= 0.1]
    result.sort(key=lambda x: x[1], reverse=True)

    # Always include general as fallback
    if not result or result[0][1] < 0.8:
        result.append(("general", 0.3))

    return result


def get_primary_domain(topic: str) -> str:
    """Get the primary (highest confidence) domain for a topic."""
    domains = classify_topic(topic)
    return domains[0][0] if domains else "general"


def get_source_weight(source_id: str, domain: str) -> float:
    """Get the scoring weight multiplier for a source in a domain."""
    weights = DOMAIN_SOURCE_WEIGHTS.get(domain, {})
    return weights.get(source_id, 1.0)
