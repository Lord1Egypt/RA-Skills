"""Platform definitions for multi-site price comparison.

Each platform specifies its bb-browser site adapter name, default region
params, and how to normalize results into a unified format.

For platforms with per-country domains (eBay, Amazon), each country has
its own Platform instance so bb-browser can resolve the correct tab.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Platform:
    name: str
    display_name: str
    adapter: str        # bb-browser site adapter name, e.g. "ebay/search-uk"
    domain: str
    default_args: dict = field(default_factory=dict)
    enabled: bool = True
    country: str = ""   # country code when platform is region-specific
    family: str = ""    # logical group, e.g. "ebay" — used for routing

    def build_cmd(self, keyword: str, **overrides) -> list[str]:
        """Build bb-browser CLI args for this platform."""
        args = {**self.default_args, **overrides}
        cmd = ["bb-browser", "site", self.adapter, keyword, "--json"]
        for k, v in args.items():
            if v:
                cmd.extend([f"--{k}", str(v)])
        return cmd


PLATFORMS: dict[str, Platform] = {
    # --- Single-domain platforms (city via URL params) ---
    "ok": Platform(
        name="ok",
        display_name="OK.com",
        adapter="ok/search",
        domain="ok.com",
        default_args={"country": "us", "city": "los-angeles"},
    ),
    # --- Gumtree (UK-only) ---
    "gumtree": Platform(
        name="gumtree",
        display_name="Gumtree",
        adapter="gumtree/search",
        domain="www.gumtree.com",
        default_args={"location": "London"},
        country="uk",
    ),

    # --- eBay: per-country adapter instances ---
    "ebay-us": Platform(
        name="ebay-us",
        display_name="eBay US",
        adapter="ebay/search-us",
        domain="www.ebay.com",
        default_args={"condition": "used"},
        country="us",
        family="ebay",
    ),
    "ebay-uk": Platform(
        name="ebay-uk",
        display_name="eBay UK",
        adapter="ebay/search-uk",
        domain="www.ebay.co.uk",
        default_args={"condition": "used"},
        country="uk",
        family="ebay",
    ),
    "ebay-au": Platform(
        name="ebay-au",
        display_name="eBay AU",
        adapter="ebay/search-au",
        domain="www.ebay.com.au",
        default_args={"condition": "used"},
        country="au",
        family="ebay",
    ),
    "ebay-ca": Platform(
        name="ebay-ca",
        display_name="eBay CA",
        adapter="ebay/search-ca",
        domain="www.ebay.ca",
        default_args={"condition": "used"},
        country="ca",
        family="ebay",
    ),

    # --- Amazon: per-country adapter instances ---
    "amazon-us": Platform(
        name="amazon-us",
        display_name="Amazon US",
        adapter="amazon/search",
        domain="www.amazon.com",
        default_args={"condition": "renewed"},
        country="us",
        family="amazon",
    ),
    "amazon-uk": Platform(
        name="amazon-uk",
        display_name="Amazon UK",
        adapter="amazon/search-uk",
        domain="www.amazon.co.uk",
        default_args={"condition": "renewed"},
        country="uk",
        family="amazon",
    ),
}


# ---------------------------------------------------------------------------
# City → Country routing
# ---------------------------------------------------------------------------

# User-facing aliases (e.g. Chinese queries) → canonical slug in CITY_COUNTRY_MAP / CITY_MAP
CITY_ALIASES: dict[str, str] = {
    "伦敦": "london",
    "英国伦敦": "london",
}


def normalize_city(city: str) -> str:
    """Normalize user city input to a canonical slug (hyphenated, lower-case ASCII)."""
    c = (city or "").strip()
    if not c:
        return "los-angeles"
    if c in CITY_ALIASES:
        return CITY_ALIASES[c]
    lowered = c.lower()
    if lowered in CITY_ALIASES:
        return CITY_ALIASES[lowered]
    return lowered.replace(" ", "-")


CITY_COUNTRY_MAP: dict[str, str] = {
    # US West
    "los-angeles": "us",
    "san-francisco": "us",
    "seattle": "us",
    # US Central
    "chicago": "us",
    "houston": "us",
    "dallas": "us",
    # US East
    "new-york": "us",
    "boston": "us",
    "miami": "us",
    "washington-dc": "us",
    "philadelphia": "us",
    "atlanta": "us",
    # UK cities
    "london": "uk",
    "greater-london": "uk",
    "manchester": "uk",
    "birmingham": "uk",
    "leeds": "uk",
    "liverpool": "uk",
    "glasgow": "uk",
    "edinburgh": "uk",
    "bristol": "uk",
    "cardiff": "uk",
    "sheffield": "uk",
    "nottingham": "uk",
    "newcastle": "uk",
    # AU cities
    "sydney": "au",
    "melbourne": "au",
    "brisbane": "au",
    # CA cities
    "toronto": "ca",
    "vancouver": "ca",
    "montreal": "ca",
    # UAE
    "abu-dhabi": "ae",
    "dubai": "ae",
}


def get_country_for_city(city: str) -> str:
    """Resolve country code from city name, defaulting to 'us'."""
    normalized = normalize_city(city)
    return CITY_COUNTRY_MAP.get(normalized, "us")


# Per-platform city slug mapping (only for platforms that need it).
CITY_MAP: dict[str, dict[str, str]] = {
    "los-angeles": {
        "ok": "los-angeles",
    },
    "new-york": {
        "ok": "new-york",
    },
    "san-francisco": {
        "ok": "san-francisco",
    },
    "chicago": {
        "ok": "chicago",
    },
    "houston": {
        "ok": "houston",
    },
    "seattle": {
        "ok": "seattle",
    },
    "dallas": {
        "ok": "dallas",
    },
    "boston": {
        "ok": "boston",
    },
    "miami": {
        "ok": "miami",
    },
    "washington-dc": {
        "ok": "washington-dc",
    },
    "philadelphia": {
        "ok": "philadelphia",
    },
    "atlanta": {
        "ok": "atlanta",
    },
    "london": {
        "ok": "greater-london",
        "gumtree": "London",
    },
    "greater-london": {
        "ok": "greater-london",
        "gumtree": "London",
    },
    "manchester": {
        "ok": "manchester",
        "gumtree": "Manchester",
    },
    "birmingham": {
        "ok": "birmingham",
        "gumtree": "Birmingham",
    },
    "leeds": {
        "ok": "leeds",
        "gumtree": "Leeds",
    },
    "liverpool": {
        "ok": "liverpool",
        "gumtree": "Liverpool",
    },
    "glasgow": {
        "ok": "glasgow",
        "gumtree": "Glasgow",
    },
    "edinburgh": {
        "ok": "edinburgh",
        "gumtree": "Edinburgh",
    },
    "bristol": {
        "ok": "bristol",
        "gumtree": "Bristol",
    },
    "cardiff": {
        "ok": "cardiff",
        "gumtree": "Cardiff",
    },
    "sheffield": {
        "ok": "sheffield",
        "gumtree": "Sheffield",
    },
    "nottingham": {
        "ok": "nottingham",
        "gumtree": "Nottingham",
    },
    "newcastle": {
        "ok": "newcastle",
        "gumtree": "Newcastle upon Tyne",
    },
    "abu-dhabi": {
        "ok": "abu-dhabi",
    },
    "dubai": {
        "ok": "dubai",
    },
}


def get_city_slug(city: str, platform_name: str) -> str:
    """Resolve city slug for a given platform, falling back to the canonical slug."""
    normalized = normalize_city(city)
    mapping = CITY_MAP.get(normalized)
    if mapping:
        return mapping.get(platform_name, normalized)
    return normalized


# ---------------------------------------------------------------------------
# Platform resolution: pick the right adapter instances for a given context
# ---------------------------------------------------------------------------

def resolve_platforms(
    city: str = "los-angeles",
    country: str | None = None,
    platform_filter: list[str] | None = None,
) -> list[Platform]:
    """Select which platform instances to query for a given city/country.

    Logic:
    - For family-based platforms (ebay-us/uk/au/ca), pick the one matching
      the resolved country. If user explicitly names "ebay-uk", use that.
      If user just says "ebay", resolve via city→country.
    - For single-domain platforms, include as-is (subject to filter).
    - Platforms are only included if enabled.

    Args:
        city: Normalized city name.
        country: Explicit country override (if given by user).
        platform_filter: User-specified platform names to include.
                         Accepts both "ebay" (family) and "ebay-uk" (instance).
    """
    resolved_country = country or get_country_for_city(city)

    result: list[Platform] = []
    seen_families: set[str] = set()

    for name, plat in PLATFORMS.items():
        if not plat.enabled:
            continue

        # Apply user filter
        if platform_filter:
            # Match by exact name ("ebay-uk") or by family ("ebay")
            family_match = plat.family and plat.family in platform_filter
            exact_match = name in platform_filter
            if not family_match and not exact_match:
                continue

        if plat.family:
            # For family platforms, pick the right country variant
            if platform_filter and name in platform_filter:
                result.append(plat)
                seen_families.add(plat.family)
            elif plat.family not in seen_families:
                if plat.country == resolved_country:
                    result.append(plat)
                    seen_families.add(plat.family)
        elif plat.country:
            # Country-specific non-family platform (e.g. gumtree=uk)
            if platform_filter and name in platform_filter:
                result.append(plat)
            elif plat.country == resolved_country:
                result.append(plat)
        else:
            result.append(plat)

    # If a family was requested but no variant matched (e.g. country="ae"
    # has no eBay), fall back to US variant
    if platform_filter:
        for fam_name in platform_filter:
            fam_platforms = [p for p in PLATFORMS.values() if p.family == fam_name]
            if fam_platforms and fam_name not in seen_families:
                us_fallback = next(
                    (p for p in fam_platforms if p.country == "us"), fam_platforms[0]
                )
                result.append(us_fallback)
                seen_families.add(fam_name)

    return result
