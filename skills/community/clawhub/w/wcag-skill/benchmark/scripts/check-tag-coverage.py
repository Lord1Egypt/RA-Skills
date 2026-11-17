#!/usr/bin/env python3
"""Check HTML5 tag coverage (against html_tags.json) and tag balance for WCAG pages.

Usage (from the repository root):
  python3 benchmark/scripts/check-tag-coverage.py <index.html> [html_tags.json]

Reports obsolete start tags. In benchmark mode, also prints coverage and balance.
Implements HTML5 optional-end-tag implied-closing rules (option, li, dt/dd,
tr/td/th, thead/tbody/tfoot, colgroup, p, rt/rp) so legally omitted end tags do
not cascade into false UNMATCHED/UNCLOSED reports for structural elements.
HTML comments are stripped before counting, so commented-out tag literals do not
count toward coverage. Exits nonzero for obsolete tags, missing required tags,
or a structural mismatch.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Elements whose end tag may be legally omitted (HTML5 §13.1.2).
OPTIONAL_END_TAGS = {
    "option", "optgroup", "li", "dt", "dd", "tr", "td", "th",
    "thead", "tbody", "tfoot", "colgroup", "p", "rt", "rp",
}

# Tags that, when opened, implicitly close a given tag left open at the top
# of the stack (the HTML5 parser's implied end-tag behaviour).
# Includes void elements: e.g. an open <p> is implicitly closed by a
# following <hr>, <address>, <div>, etc. hgroup is added because an open
# <p> is implicitly closed by a following <h1>–<h6>/<hgroup>.
# rt/rp close a preceding rt so that <ruby><rt>one<rt>two</ruby> parses cleanly.
_P_CLOSERS = {
    "address", "article", "aside", "blockquote", "details", "div", "dl",
    "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3",
    "h4", "h5", "h6", "header", "hr", "main", "menu", "nav", "ol", "p",
    "pre", "section", "table", "ul", "hgroup", "search",
}

AUTO_CLOSE_ON_OPEN = {
    "li": {"li"},
    "option": {"option"},
    "optgroup": {"option", "optgroup"},
    "dt": {"dt", "dd"},
    "dd": {"dt", "dd"},
    "tr": {"tr", "td", "th"},
    "td": {"td", "th"},
    "th": {"td", "th"},
    "thead": {"thead", "tbody", "tfoot"},
    "tbody": {"thead", "tbody", "tfoot"},
    "tfoot": {"thead", "tbody", "tfoot"},
    "colgroup": {"colgroup"},
    "rt": {"rt", "rp"},
    "rp": {"rt", "rp"},
}
for _closer in _P_CLOSERS:
    AUTO_CLOSE_ON_OPEN.setdefault(_closer, set()).add("p")

TAG_RE = r"<\s*([a-zA-Z][a-zA-Z0-9\-]*)\b"


def strip_comments(html):
    """Strip HTML comments while respecting quoted attribute values.

    A raw regex r'<!--.*?-->' treats <!-- inside quoted attribute
    values (e.g. data-value=\\\"<!--\\\") as a comment start, which can
    destroy legitimate content. This scanner tracks quote state so
    <!-- only starts a comment outside attribute values.

    Quote tracking is scoped to tag attributes only, and disabled
    inside HTML comments. This avoids false negatives from apostrophes
    in text content like "It's <!-- <base> -->" leaving the comment
    unstripped and falsely counting <base> toward coverage.
    """
    result = []
    i = 0
    in_single_quote = False
    in_double_quote = False
    in_comment = False
    in_tag = False
    while i < len(html):
        ch = html[i]
        if in_comment:
            if i + 2 < len(html) and html[i:i+3] == '-->':
                in_comment = False
                i += 3
                continue
            i += 1
            continue
        if ch == '<':
            if not in_single_quote and not in_double_quote:
                if i + 3 < len(html) and html[i:i+4] == '<!--':
                    in_comment = True
                    i += 4
                    continue
                in_tag = True
                in_single_quote = False
                in_double_quote = False
                result.append(ch)
                i += 1
                continue
            # Inside quotes, '<' has no special meaning - just append it
            result.append(ch)
            i += 1
            continue
        if ch == '>' and in_tag:
            in_tag = False
            result.append(ch)
            i += 1
            continue
        if in_tag:
            if ch == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
                result.append(ch)
                i += 1
                continue
            elif ch == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
                result.append(ch)
                i += 1
                continue
        result.append(ch)
        i += 1
    return ''.join(result)


def check_coverage(html, tags_path):
    with open(tags_path) as f:
        expected = set(json.load(f)["tags"])
    used = set(t.lower() for t in re.findall(TAG_RE, strip_comments(html)))
    missing = sorted(expected - used)
    print(f"Expected: {len(expected)}  Used: {len(used)}  Missing: {len(missing)}")
    if missing:
        print("MISSING:", ", ".join(missing))
    return missing


def check_deprecated(html):
    rules_path = Path(__file__).resolve().parents[2] / "resources" / "legacy_tags.json"
    with rules_path.open(encoding="utf-8") as f:
        deprecated = set(json.load(f)["tags"])

    class DeprecatedParser(HTMLParser):
        CDATA_CONTENT_ELEMENTS = (
            "script", "style", "title", "textarea", "xmp", "iframe", "noembed", "noframes",
        )

        def __init__(self):
            super().__init__()
            self.found = set()

        def handle_starttag(self, tag, attrs):
            if tag in deprecated:
                self.found.add(tag)
            if tag == "plaintext":
                self.set_cdata_mode(tag)

        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)

    parser = DeprecatedParser()
    parser.feed(html)
    found = sorted(parser.found)
    print("Deprecated tags present:", ", ".join(found) if found else "none")
    return found


def check_balance(html):
    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.implied_closes = []
            self.mismatches = []
            self.stray_end_tags = []

        def handle_starttag(self, tag, attrs):
            # Apply implied-close rules BEFORE the void check, so a void
            # element that closes an open optional-end-tag element (e.g. <hr>
            # closing an open <p>) is still recorded.
            closers = AUTO_CLOSE_ON_OPEN.get(tag)
            if closers:
                while self.stack and self.stack[-1] in closers:
                    self.implied_closes.append((self.stack.pop(), tag, self.getpos()))
            if tag in VOID:
                return
            self.stack.append(tag)

        def handle_startendtag(self, tag, attrs):
            # For non-void start-end tags (e.g. <div/>), HTML5 does NOT treat them as self-closing.
            # Previously we called handle_starttag then synthesized an end tag, which could mask structural errors.
            # Instead, we treat such occurrences as a stray end tag error (or could ignore). Here we record a stray end tag.
            self.handle_starttag(tag, attrs)
            if tag not in VOID:
                # Record as stray end tag to surface the issue.
                self.stray_end_tags.append((tag, self.getpos()))
                return

        def handle_endtag(self, tag):
            if tag in VOID:
                self.stray_end_tags.append((tag, self.getpos()))
                return
            if tag not in self.stack:
                # No matching open tag. A stray end tag is always a parse
                # error: an element implicitly closed (popped by
                # AUTO_CLOSE_ON_OPEN) cannot be "closed again" by a later
                # explicit end tag. Only the implied closes recorded in
                # handle_starttag are legal.
                self.stray_end_tags.append((tag, self.getpos()))
                return
            idx = len(self.stack) - 1 - self.stack[::-1].index(tag)
            while len(self.stack) - 1 > idx:
                popped = self.stack.pop()
                if popped not in OPTIONAL_END_TAGS:
                    self.mismatches.append(
                        f"UNMATCHED </{tag}> at {self.getpos()} force-closed unclosed <{popped}>"
                    )
            self.stack.pop()

    p = P()
    p.feed(html)

    if p.implied_closes:
        print(f"INFO: {len(p.implied_closes)} optional end tag(s) legally omitted (implied close)")
    for tag, pos in p.stray_end_tags:
        print(f"ERROR: stray </{tag}> at {pos} (no matching open tag)")

    has_error = bool(p.mismatches) or bool(p.stray_end_tags)
    for m in p.mismatches:
        print(m)

    structural_unclosed = [t for t in p.stack if t not in OPTIONAL_END_TAGS]
    optional_unclosed = [t for t in p.stack if t in OPTIONAL_END_TAGS]
    if structural_unclosed:
        print("UNCLOSED (structural mismatch):", structural_unclosed)
        has_error = True
    if optional_unclosed:
        print("UNCLOSED (optional end tag, not an error):", optional_unclosed)
    if not has_error:
        print("Balance: OK")
    return has_error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html")
    parser.add_argument("tags", nargs="?", help="benchmark required-tag JSON")
    args = parser.parse_args()
    default_tags = Path(__file__).resolve().parent.parent / "resources" / "html_tags.json"
    tags_path = args.tags or default_tags
    with open(args.html, encoding="utf-8") as f:
        html = f.read()
    deprecated = check_deprecated(html)
    missing = check_coverage(html, tags_path)
    balance_error = check_balance(html)
    sys.exit(1 if (deprecated or missing or balance_error) else 0)


if __name__ == "__main__":
    main()