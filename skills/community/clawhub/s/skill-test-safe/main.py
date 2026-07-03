"""
skill-test-safe: A safe, legitimate text processing utility.
Should trigger ZERO security scan rules.
"""


def word_count(text):
    """Count words in the given text."""
    return len(text.split())


def char_count(text):
    """Count characters in the given text."""
    return len(text)


def reverse_string(text):
    """Reverse the given string."""
    return text[::-1]


def to_uppercase(text):
    """Convert text to uppercase."""
    return text.upper()


def to_lowercase(text):
    """Convert text to lowercase."""
    return text.lower()


def truncate(text, max_length=100, suffix="..."):
    """Truncate text to max_length, appending suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def remove_duplicates(items):
    """Remove duplicate items from a list while preserving order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def slugify(text):
    """Convert text to a URL-friendly slug."""
    slug = ""
    for ch in text.lower():
        if ch.isalnum():
            slug += ch
        elif ch in (" ", "-"):
            slug += "-"
    return slug.strip("-")


def format_table(headers, rows):
    """Format data as a simple text table."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def format_row(cells):
        return " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(cells))

    lines = [format_row(headers)]
    lines.append("-+-".join("-" * w for w in col_widths))
    for row in rows:
        lines.append(format_row(row))
    return "\n".join(lines)


def main(text):
    """Process the input text and return analysis results."""
    return {
        "word_count": word_count(text),
        "char_count": char_count(text),
        "reversed": reverse_string(text),
        "uppercase": to_uppercase(text),
        "lowercase": to_lowercase(text),
        "slug": slugify(text),
        "truncated": truncate(text),
    }