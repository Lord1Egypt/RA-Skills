#!/usr/bin/env python3
"""Generate, validate, and test robots.txt files."""

import argparse
import sys
import re
import urllib.request
import urllib.error
from pathlib import Path
from fnmatch import fnmatch

# ── Platform presets ────────────────────────────────────────────────────────

PRESETS = {
    "wordpress": {
        "agents": {
            "*": {
                "allow": ["/wp-admin/admin-ajax.php"],
                "disallow": ["/wp-admin/", "/wp-includes/", "/*?s=", "/*?p=", "/trackback/", "/feed/", "/comments/"],
            }
        },
    },
    "nextjs": {
        "agents": {
            "*": {
                "allow": ["/"],
                "disallow": ["/_next/static/", "/api/", "/.next/"],
            }
        },
    },
    "django": {
        "agents": {
            "*": {
                "allow": ["/"],
                "disallow": ["/admin/", "/static/admin/", "/media/private/", "/__debug__/"],
            }
        },
    },
    "rails": {
        "agents": {
            "*": {
                "allow": ["/"],
                "disallow": ["/admin/", "/assets/", "/tmp/", "/rails/"],
            }
        },
    },
    "laravel": {
        "agents": {
            "*": {
                "allow": ["/"],
                "disallow": ["/admin/", "/storage/", "/vendor/", "/telescope/"],
            }
        },
    },
    "static": {
        "agents": {
            "*": {
                "allow": ["/"],
                "disallow": [],
            }
        },
    },
    "spa": {
        "agents": {
            "*": {
                "allow": ["/"],
                "disallow": ["/api/", "/assets/", "/_internal/"],
            }
        },
    },
    "ecommerce": {
        "agents": {
            "*": {
                "allow": ["/"],
                "disallow": ["/cart/", "/checkout/", "/account/", "/wishlist/", "/search?", "/compare/"],
            }
        },
    },
}

AI_CRAWLERS = [
    "GPTBot",
    "ChatGPT-User",
    "Google-Extended",
    "CCBot",
    "anthropic-ai",
    "ClaudeBot",
    "Bytespider",
    "FacebookBot",
    "Applebot-Extended",
    "PerplexityBot",
    "YouBot",
]

# ── Generator ───────────────────────────────────────────────────────────────

def generate_robots_txt(args):
    lines = []
    agents_config = {}

    if args.preset:
        preset = PRESETS.get(args.preset)
        if not preset:
            print(f"Error: Unknown preset '{args.preset}'. Available: {', '.join(PRESETS.keys())}", file=sys.stderr)
            sys.exit(1)
        agents_config = dict(preset["agents"])

    # Apply custom rules
    agent_name = args.agent or "*"
    if args.allow or args.disallow:
        if agent_name not in agents_config:
            agents_config[agent_name] = {"allow": [], "disallow": []}
        if args.allow:
            agents_config[agent_name]["allow"].extend(args.allow)
        if args.disallow:
            agents_config[agent_name]["disallow"].extend(args.disallow)

    # If no config at all, default allow-all
    if not agents_config:
        agents_config["*"] = {"allow": ["/"], "disallow": []}

    # Render agent blocks
    for agent, rules in agents_config.items():
        lines.append(f"User-agent: {agent}")
        for path in rules.get("disallow", []):
            lines.append(f"Disallow: {path}")
        for path in rules.get("allow", []):
            lines.append(f"Allow: {path}")
        if args.crawl_delay:
            lines.append(f"Crawl-delay: {args.crawl_delay}")
        lines.append("")

    # AI blocker
    if args.block_ai:
        lines.append("# Block AI training crawlers")
        for bot in AI_CRAWLERS:
            lines.append(f"User-agent: {bot}")
            lines.append("Disallow: /")
            lines.append("")

    # Sitemaps
    if args.sitemap:
        for sm in args.sitemap:
            lines.append(f"Sitemap: {sm}")

    output = "\n".join(lines).strip() + "\n"

    if args.output:
        Path(args.output).write_text(output)
        print(f"Written to {args.output}")
    else:
        print(output)


# ── Validator ───────────────────────────────────────────────────────────────

VALID_DIRECTIVES = {
    "user-agent", "disallow", "allow", "sitemap", "crawl-delay", "host",
    "clean-param", "request-rate", "visit-time", "noindex",
}

def validate_robots_txt(args):
    content = _load_content(args)
    errors = []
    warnings = []
    line_num = 0
    has_user_agent = False
    in_group = False
    seen_sitemaps = []

    for raw_line in content.splitlines():
        line_num += 1
        line = raw_line.strip()

        # Skip blanks and comments
        if not line or line.startswith("#"):
            if not line:
                in_group = False
            continue

        # Check for colon-separated directive
        if ":" not in line:
            errors.append(f"Line {line_num}: Invalid syntax (no colon found): {line}")
            continue

        directive, _, value = line.partition(":")
        directive = directive.strip().lower()
        value = value.strip()

        if directive not in VALID_DIRECTIVES:
            warnings.append(f"Line {line_num}: Unknown directive '{directive}' (may not be supported by all crawlers)")

        if directive == "user-agent":
            has_user_agent = True
            in_group = True
            if not value:
                errors.append(f"Line {line_num}: User-agent has no value")

        elif directive in ("disallow", "allow"):
            if not in_group and not has_user_agent:
                errors.append(f"Line {line_num}: '{directive}' before any User-agent directive")
            if value and not value.startswith("/") and not value.startswith("*"):
                warnings.append(f"Line {line_num}: Path '{value}' should start with /")

        elif directive == "sitemap":
            if not value.startswith("http"):
                warnings.append(f"Line {line_num}: Sitemap should be an absolute URL: {value}")
            seen_sitemaps.append(value)

        elif directive == "crawl-delay":
            try:
                float(value)
            except ValueError:
                errors.append(f"Line {line_num}: Crawl-delay must be a number, got '{value}'")

    if not has_user_agent:
        errors.append("No User-agent directive found")

    # Report
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")
    if not errors and not warnings:
        print("✓ robots.txt is valid — no issues found.")
    elif not errors:
        print(f"\n✓ Valid with {len(warnings)} warning(s).")
    else:
        print(f"\n✗ Found {len(errors)} error(s) and {len(warnings)} warning(s).")
        sys.exit(1)


# ── Tester ──────────────────────────────────────────────────────────────────

def test_robots_txt(args):
    content = _load_content_file(args.file)
    test_url = args.url
    test_agent = args.agent or "Googlebot"

    rules = _parse_rules(content)
    result = _check_url(rules, test_agent, test_url)

    if result:
        print(f"✓ ALLOWED: {test_url} for {test_agent}")
    else:
        print(f"✗ BLOCKED: {test_url} for {test_agent}")

def _parse_rules(content):
    """Parse robots.txt into {agent: [(allow/disallow, path), ...]}"""
    rules = {}
    current_agents = []

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            continue

        directive, _, value = line.partition(":")
        directive = directive.strip().lower()
        value = value.strip()

        if directive == "user-agent":
            current_agents = [value.lower()]
            for a in current_agents:
                if a not in rules:
                    rules[a] = []
        elif directive in ("allow", "disallow"):
            for a in current_agents:
                rules.setdefault(a, []).append((directive, value))

    return rules

def _check_url(rules, agent, url):
    """Check if url is allowed for agent. Returns True if allowed."""
    agent_lower = agent.lower()

    # Find matching rules: specific agent first, then wildcard
    matching_rules = rules.get(agent_lower, rules.get("*", []))

    # Find the most specific matching rule
    best_match = None
    best_length = -1

    for directive, path in matching_rules:
        if not path:  # Empty disallow = allow all
            if directive == "disallow":
                if best_length < 0:
                    best_match = "allow"
                    best_length = 0
            continue

        # Convert robots.txt pattern to check
        if _path_matches(path, url):
            if len(path) > best_length:
                best_length = len(path)
                best_match = directive

    if best_match is None:
        return True  # Default: allowed
    return best_match == "allow"

def _path_matches(pattern, url):
    """Check if a robots.txt path pattern matches a URL."""
    # Handle $ anchor
    if pattern.endswith("$"):
        pattern = pattern[:-1]
        if "*" in pattern:
            return fnmatch(url, pattern)
        return url == pattern

    # Handle * wildcards
    if "*" in pattern:
        return fnmatch(url, pattern + "*") or fnmatch(url, pattern)

    # Simple prefix match
    return url.startswith(pattern)


# ── Helpers ─────────────────────────────────────────────────────────────────

def _load_content(args):
    if hasattr(args, "file") and args.file:
        return _load_content_file(args.file)
    elif hasattr(args, "url") and args.url:
        return _load_content_url(args.url)
    else:
        print("Error: Provide --file or --url", file=sys.stderr)
        sys.exit(1)

def _load_content_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

def _load_content_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "robots-txt-gen/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate, validate, and test robots.txt files.")
    sub = parser.add_subparsers(dest="command", help="Command")

    # generate
    gen = sub.add_parser("generate", help="Generate a robots.txt file")
    gen.add_argument("--preset", choices=list(PRESETS.keys()), help="Platform preset")
    gen.add_argument("--agent", default=None, help="User-agent name (default: *)")
    gen.add_argument("--allow", action="append", help="Allow path (repeatable)")
    gen.add_argument("--disallow", action="append", help="Disallow path (repeatable)")
    gen.add_argument("--sitemap", action="append", help="Sitemap URL (repeatable)")
    gen.add_argument("--crawl-delay", type=float, help="Crawl delay in seconds")
    gen.add_argument("--block-ai", action="store_true", help="Block known AI crawlers")
    gen.add_argument("--output", "-o", help="Output file path")

    # validate
    val = sub.add_parser("validate", help="Validate a robots.txt file")
    val.add_argument("--file", help="Local file path")
    val.add_argument("--url", help="Remote URL to fetch")

    # test
    tst = sub.add_parser("test", help="Test URL against robots.txt rules")
    tst.add_argument("--file", required=True, help="robots.txt file")
    tst.add_argument("--url", required=True, help="URL path to test")
    tst.add_argument("--agent", default="Googlebot", help="User-agent (default: Googlebot)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "generate":
        generate_robots_txt(args)
    elif args.command == "validate":
        validate_robots_txt(args)
    elif args.command == "test":
        test_robots_txt(args)

if __name__ == "__main__":
    main()
