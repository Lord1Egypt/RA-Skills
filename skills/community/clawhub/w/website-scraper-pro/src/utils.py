import re
from urllib.parse import urlparse

from constants import (
    DEFAULT_FORMAT,
    QUERY_MAX_SECTIONS,
    QUERY_STOPWORDS,
    SETUP_COMMANDS,
    SUPPORTED_FORMATS,
)


def parse_cli_args(args: list[str]) -> dict:
    """Parse CLI args for the website scraper skill."""
    if not args:
        raise ValueError(usage_text())

    url = None
    use_js = False
    query = None
    output_format = DEFAULT_FORMAT

    index = 0
    while index < len(args):
        arg = args[index]

        if arg == "--js":
            use_js = True
            index += 1
            continue

        if arg == "--query":
            if index + 1 >= len(args):
                raise ValueError("Missing value for --query.")
            query = args[index + 1].strip()
            if not query:
                raise ValueError("Query must not be empty.")
            index += 2
            continue

        if arg == "--format":
            if index + 1 >= len(args):
                raise ValueError("Missing value for --format.")
            output_format = args[index + 1].strip().lower()
            if output_format not in SUPPORTED_FORMATS:
                raise ValueError(
                    "Unsupported format "
                    f"'{args[index + 1]}'. Supported formats: {', '.join(SUPPORTED_FORMATS)}."
                )
            index += 2
            continue

        if arg.startswith("--"):
            raise ValueError(f"Unknown flag '{arg}'.")

        if url is not None:
            raise ValueError(f"Unexpected argument '{arg}'.")

        url = validate_url(arg)
        index += 1

    if url is None:
        raise ValueError("A URL is required.\n" + usage_text())

    return {
        "url": url,
        "use_js": use_js,
        "query": query,
        "output_format": output_format,
    }


def usage_text() -> str:
    """Return the CLI usage text."""
    return (
        "Usage: website-scraper-pro <URL> [--js] [--query <TEXT>] [--format markdown|json]\n"
        "Examples:\n"
        "  website-scraper-pro https://example.com\n"
        "  website-scraper-pro https://example.com --js\n"
        '  website-scraper-pro https://example.com --query "example domain"\n'
        "  website-scraper-pro https://example.com --format json"
    )


def validate_url(value: str) -> str:
    """Validate that a full HTTP or HTTPS URL was provided."""
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Invalid URL '{value}'. Use a full http:// or https:// URL.")
    return value


def clean_markdown(value: str | None) -> str:
    """Normalize markdown output into a stable plain-text form."""
    if not value:
        return ""

    lines = [line.rstrip() for line in value.replace("\r\n", "\n").split("\n")]
    cleaned = "\n".join(lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def tokenize_query(query: str) -> list[str]:
    """Tokenize a user query into simple lowercase keywords."""
    tokens = []
    for token in re.findall(r"[a-z0-9]+", query.lower()):
        if len(token) < 2 or token in QUERY_STOPWORDS:
            continue
        tokens.append(token)
    return tokens


def split_markdown_sections(markdown: str) -> list[str]:
    """Split markdown into heading-aware sections."""
    sections = []
    current = []

    for line in markdown.split("\n"):
        if line.startswith("#") and current:
            sections.append("\n".join(current).strip())
            current = [line]
            continue
        current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    normalized = [section for section in sections if section.strip()]
    if normalized:
        return normalized

    return [block.strip() for block in re.split(r"\n\s*\n", markdown) if block.strip()]


def select_relevant_markdown(markdown: str, query: str) -> str:
    """Select the most relevant markdown sections with a deterministic scorer."""
    cleaned = clean_markdown(markdown)
    if not cleaned:
        return ""

    tokens = tokenize_query(query)
    if not tokens:
        return cleaned

    sections = split_markdown_sections(cleaned)
    scored_sections = []

    for index, section in enumerate(sections):
        lowered = section.lower()
        unique_matches = sum(1 for token in tokens if token in lowered)
        total_matches = sum(lowered.count(token) for token in tokens)
        if total_matches <= 0:
            continue
        score = (unique_matches * 5) + total_matches
        scored_sections.append((score, index, section))

    if not scored_sections:
        return cleaned

    scored_sections.sort(key=lambda item: (-item[0], item[1]))
    selected_indexes = {index for _, index, _ in scored_sections[:QUERY_MAX_SECTIONS]}
    selected_sections = [
        section for index, section in enumerate(sections) if index in selected_indexes
    ]
    return clean_markdown("\n\n".join(selected_sections))


def to_json_safe(value):
    """Convert nested values into JSON-safe primitives."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): to_json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_json_safe(item) for item in value]
    return str(value)


def normalize_links(links) -> dict:
    """Normalize Crawl4AI link output into a stable JSON shape."""
    normalized = {"internal": [], "external": []}
    if not isinstance(links, dict):
        return normalized

    for bucket in ("internal", "external"):
        entries = links.get(bucket)
        if not isinstance(entries, list):
            continue

        normalized_entries = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            normalized_entry = {
                key: to_json_safe(entry.get(key))
                for key in (
                    "href",
                    "text",
                    "title",
                    "context",
                    "domain",
                    "base_domain",
                )
                if entry.get(key) not in (None, "")
            }
            if normalized_entry:
                normalized_entries.append(normalized_entry)

        normalized_entries.sort(
            key=lambda item: (
                item.get("href", ""),
                item.get("text", ""),
                item.get("title", ""),
            )
        )
        normalized[bucket] = normalized_entries

    return normalized


def build_setup_error(detail: str) -> str:
    """Build a setup-focused error message for missing Crawl4AI dependencies."""
    commands = "\n".join(f"- {command}" for command in SETUP_COMMANDS)
    return f"{detail}\nRun one-time setup commands:\n{commands}"


def looks_like_browser_setup_error(message: str) -> bool:
    """Detect common Playwright or browser-installation failures."""
    lowered = message.lower()
    return any(
        token in lowered
        for token in (
            "playwright",
            "browsertype.launch",
            "executable doesn't exist",
            "failed to launch browser",
            "please run the following command",
            "install chromium",
        )
    )
