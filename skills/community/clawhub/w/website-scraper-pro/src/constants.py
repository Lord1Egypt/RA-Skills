DEFAULT_FORMAT = "markdown"
SUPPORTED_FORMATS = ("markdown", "json")

DEFAULT_WORD_COUNT_THRESHOLD = 5
DEFAULT_WAIT_FOR = "body"
DEFAULT_WAIT_UNTIL = "domcontentloaded"
DEFAULT_PAGE_TIMEOUT_MS = 30000
DEFAULT_DELAY_BEFORE_RETURN_HTML = 0.25

JS_WAIT_FOR = "body"
JS_WAIT_UNTIL = "networkidle"
JS_PAGE_TIMEOUT_MS = 45000
JS_DELAY_BEFORE_RETURN_HTML = 0.75
JS_SCROLL_DELAY_SECONDS = 0.4

PRUNING_THRESHOLD = 0.48
PRUNING_THRESHOLD_TYPE = "dynamic"
PRUNING_MIN_WORD_THRESHOLD = 5

BM25_THRESHOLD = 0.8
QUERY_FALLBACK_MIN_LENGTH = 120
QUERY_MAX_SECTIONS = 8

EXCLUDED_TAGS = ["nav", "footer", "form", "svg"]

QUERY_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
}

SETUP_COMMANDS = (
    "uv run --with crawl4ai crawl4ai-setup",
    "uv run --with crawl4ai python -m playwright install chromium",
)
