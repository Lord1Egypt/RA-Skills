# Checker Pitfalls

Edge cases that trip up `check-tag-coverage.py` and tag-balance logic.
All cases are verified against `benchmark/resources/html_tags.json` (113 tags).

## HTML comments do not count toward coverage

`check_coverage` strips HTML comments (`<!-- ... -->`) before running
`TAG_RE` against the document. A commented-out `<base>` literal does NOT
count as base coverage. **Always use a real element** for tags required by
`benchmark/resources/html_tags.json` — a `<base target="_self">` satisfies the tag requirement
without rewriting relative URLs.

## Optional-end-tag tracking is context-sensitive, not global

A stray end tag for an optional-end-tag element (e.g. `</li>`, `</p>`,
`</rp>`) is **always a parse error** unless that exact element was
implicitly closed earlier by an `AUTO_CLOSE_ON_OPEN` rule. Tracking by
tag name alone causes false negatives: `<p>one<div>two</div><p>three</p></p>`
passes because the second `</p>` sees `p` was "previously" implied-closed,
even though no `<p>` is open at that point.

Correct approach: handle all implied closes in `handle_starttag` (pop from
stack via AUTO_CLOSE_ON_OPEN). A tag not present in the stack at the time
of `handle_endtag` has no valid open context and is always an error.

## Void elements close open optional-end-tag elements

Per HTML5 parsing, a void element (e.g. `<hr>`) implicitly closes a
preceding open `<p>` (or other optional-end-tag element). The checker
must apply `AUTO_CLOSE_ON_OPEN` rules *before* the void-element early
return in `handle_starttag`, or `<p>text<hr>` leaves an unclosed `<p>`.

## Ruby optional end tags

`<rt>` and `</rp>` have optional end tags in HTML5:
- `</rt>` before another `<rt>` is legally omitted (self-closes the previous)
- `</rp>` at end of ruby or before `<rt>` is legally omitted

Add `rt`/`rp` to `OPTIONAL_END_TAGS` and their close rules to
`AUTO_CLOSE_ON_OPEN`.

## Table header scope in tfoot

`<tfoot>` row labels use `scope="row"` (the label describes the row).
`scope="col"` associates the cell with a column instead. For a footer
summary row like "Average", `scope="row"` is semantically correct.

## Template <base> vs harness <base>

The AI-WCAG-Gauntlet harness injects `<base href="/AI-WCAG-Gauntlet/">`
into benchmark pages. A benchmark template should NOT include its own
`<base href=...>` (duplicate base elements cause the first to control
relative URLs). Use a bare `<base>` (no href) solely for tag-coverage
compliance, or rely on the harness-injected base for URL resolution.
