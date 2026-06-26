import os
from dotenv import load_dotenv

# Load environment variables from a local .env file if one exists
load_dotenv()

DEFAULT_CONFIG = {
    # --- LLM Provider Settings ---
    # Supported values: "gemini" | "openai" | "anthropic"
    # When using "anthropic", you MUST also set PRIMARY_MODEL and REASONING_MODEL
    # to valid Anthropic model strings (e.g. "claude-3-5-haiku-latest").
    "LLM_PROVIDER":       os.getenv("LLM_PROVIDER",       "gemini"),
    "EMBEDDING_PROVIDER": os.getenv("EMBEDDING_PROVIDER", "gemini"),
    "PRIMARY_MODEL":      os.getenv("PRIMARY_MODEL",      "gemini-2.5-flash"),
    "REASONING_MODEL":    os.getenv("REASONING_MODEL",    "gemini-2.5-pro"),

    # --- API Keys ---
    "GEMINI_API_KEY":      os.getenv("GEMINI_API_KEY",      ""),
    "OPENAI_API_KEY":      os.getenv("OPENAI_API_KEY",      ""),
    "ANTHROPIC_API_KEY":   os.getenv("ANTHROPIC_API_KEY",   ""),
    "GSC_SERVICE_ACCOUNT": os.getenv("GSC_SERVICE_ACCOUNT", ""),
    "SCRAPER_TIER2_KEY":   os.getenv("SCRAPER_TIER2_KEY",   ""),  # Firecrawl
    "SCRAPER_TIER3_KEY":   os.getenv("SCRAPER_TIER3_KEY",   ""),  # Crawl4AI
    "JINA_API_KEY":        os.getenv("JINA_API_KEY",        ""),  # Optional — free tier works without key
    "INDEXNOW_KEY":        os.getenv("INDEXNOW_KEY",        ""),

    # --- Residential Proxy (optional — only used when SCRAPE_MODE = "playwright") ---
    "PROXY_PROVIDER":      os.getenv("PROXY_PROVIDER",      ""),   # Leave empty for api_only mode
    "PROXY_GATE":          os.getenv("PROXY_GATE",          ""),   # e.g. brd.superproxy.io:22225
    "PROXY_USER":          os.getenv("PROXY_USER",          ""),
    "PROXY_PASS":          os.getenv("PROXY_PASS",          ""),
    "PROXY_COUNTRY":       os.getenv("PROXY_COUNTRY",       "US"),
    "PROXY_ROTATE_ON_BAN": os.getenv("PROXY_ROTATE_ON_BAN", "True").lower() == "true",

    # --- Scraping Mode ---
    # "api_only"   → Skip Playwright (Tier 1).  Default for all installs.
    # "playwright" → Full 6-tier waterfall.  Requires PROXY_* fields.
    "SCRAPE_MODE": os.getenv("SCRAPE_MODE", "api_only"),

    # --- Identity ---
    "TARGET_NICHE":          os.getenv("TARGET_NICHE",          ""),
    "INITIAL_KEYWORDS":      [
        k.strip()
        for k in os.getenv("INITIAL_KEYWORDS", "").split(",")
        if k.strip()
    ],
    "IDEAL_CUSTOMER_AVATAR": os.getenv("IDEAL_CUSTOMER_AVATAR", ""),
    "BRAND_ENTITY_NAME":     os.getenv("BRAND_ENTITY_NAME",     ""),
    "BRAND_ENTITY_URL":      os.getenv("BRAND_ENTITY_URL",      ""),

    # --- WordPress ---
    "WP_URL":               os.getenv("WP_URL",               ""),
    "WP_USERNAME":          os.getenv("WP_USERNAME",          ""),
    "WP_APP_PASSWORD":      os.getenv("WP_APP_PASSWORD",      ""),
    "STAGING_WP_URL":       os.getenv("STAGING_WP_URL",       ""),
    "WP_SEO_META_DESC_KEY": os.getenv("WP_SEO_META_DESC_KEY", "_yoast_wpseo_metadesc"),

    # --- CTA ---
    "CTA_LINK":  "https://oneclickvids.com",
    "CTA_TEXT":  "GENERATE AI VIDEO",
    "CTA_ANCHOR_VARIATIONS": [
        "this guide", "learn more", "see how it works",
        "full breakdown here", "read next", "explore this tool"
    ],

    # --- Semantic Dedup ---
    "SIMILARITY_THRESHOLD": 0.85,
    "MAX_QUERY_RETRIES":    5,

    # --- Quality Gates ---
    "MIN_WORD_COUNT":        1200,
    "MAX_WORD_COUNT":        3500,
    "MIN_READABILITY_SCORE": 45.0,
    "REQUIRE_HUMAN_APPROVAL": False,

    # --- Publishing ---
    "PUBLISH_FREQUENCY": 1,
    "PUBLISH_MODE":      "auto",

    # --- Analytics ---
    "ANALYTICS_FREQUENCY_DAYS":   30,
    "STRIKING_DISTANCE_MIN":      11,
    "STRIKING_DISTANCE_MAX":      40,
    "CONTENT_AGE_GATE_BASE_DAYS": 90,
    "ADDITIVE_UPDATES_ONLY":      True,

    # --- Internal Linking ---
    "MAX_INBOUND_LINKS_PER_POST": 5,
    "ANCHOR_VARIATION_REQUIRED":  True,

    # --- Cost Controls ---
    "DAILY_COST_CAP_USD": 2.00,

    # --- Schema ---
    "SCHEMA_AUTHOR_TWITTER":  os.getenv("SCHEMA_AUTHOR_TWITTER",  ""),
    "SCHEMA_AUTHOR_LINKEDIN": os.getenv("SCHEMA_AUTHOR_LINKEDIN", ""),
    "SCHEMA_LOGO_URL":        os.getenv("SCHEMA_LOGO_URL",        ""),
    "SCHEMA_SITE_NAME":       os.getenv("SCHEMA_SITE_NAME",       ""),

    # --- Storage Paths ---
    "CHROMA_DB_PATH": "./chroma_db",
    "SQLITE_DB_PATH": "./openclaw.db",
    "LOG_DIR":        "./logs",
}