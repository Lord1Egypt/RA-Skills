---
name: rfc-lookup
description: >
  Look up IETF RFCs and read what a specification actually says. Use whenever an RFC
  number comes up ("RFC 9110", "RFC 2616", "rfc7231"), when checking what a protocol
  spec requires, when quoting normative MUST/SHOULD/MAY language, when asked "what does
  the spec say about X", or when verifying whether an RFC is still current or has been
  obsoleted. Covers HTTP, TCP/IP, DNS, TLS, QUIC, SMTP, OAuth, JSON/JOSE and every other
  IETF standard. Finds the right RFC, reads one section instead of the whole document,
  and flags superseded specifications before they get cited.
---

# RFC lookup

`scripts/rfc.py` reads the IETF RFC corpus. It needs nothing but a Python
interpreter — no install step, no packages.

```bash
python3 scripts/rfc.py <command> [options]
```

It works immediately, fetching documents over HTTPS as needed. If the section
index has been downloaded or a local mirror synced, it reads from disk instead and
can search the full text of every RFC. Same commands either way.

## The loop

Four steps, and skipping the middle two is how a wrong or oversized answer
happens:

```bash
python3 scripts/rfc.py search "http caching"     # find it            → RFC 9111
python3 scripts/rfc.py meta 9111                 # is it still current?
python3 scripts/rfc.py sections 9111             # where does it say that?
python3 scripts/rfc.py get 9111 --section 5.2    # read only that
```

Then quote the text verbatim and cite the section — `RFC 9111 §5.2` — so the
claim can be checked. Normative words carry weight (MUST is not SHOULD, and
neither is "recommended"), so quote them rather than paraphrasing; section
numbers come straight from `sections`, so a citation is always verifiable.

## Check obsolescence before citing anything

This is the rule, not a suggestion. RFCs are superseded constantly and the
best-known number is very often the dead one — RFC 2616 has been obsolete since
2014, and it is still what most people reach for on HTTP.

Every command prints a banner, and a superseded document says so:

```
RFC 2616 — Hypertext Transfer Protocol -- HTTP/1.1  [DRAFT STANDARD]
!! OBSOLETED BY: RFC 7230, 7231, 7232, 7233, 7234, 7235
```

When you see `!! OBSOLETED BY`, go read the replacement and cite that instead.
Mention the supersession to the user rather than quietly substituting. `meta`
shows this without fetching the document:

```bash
python3 scripts/rfc.py meta 2616
```

## Find the right RFC

```bash
python3 scripts/rfc.py search "http semantics"        # all terms must appear in the title
python3 scripts/rfc.py search 'HTTP/\d\.\d' --regex
```

Title search is available always. Searching document bodies needs the section
index or a synced mirror:

```bash
python3 scripts/rfc.py search "how long can a cache serve a stale response" --fulltext
```

With the section index, each result is one section, ranked by BM25 with heading
words counting more, and names the section to read next:

```
RFC 9111 — HTTP Caching  [INTERNET STANDARD]
   §4.2.4 Serving Stale Responses  (line 784, 17 lines)
   790: A cache MUST NOT generate a stale response if it is prohibited by an
```

Pass that number straight to `get --section`. The query is words, not a phrase:
write the question or its key terms, and expect sections that use some of them,
best first. A section with no number is the RFC's front matter.

Without the index, `--fulltext` searches the mirror with `rg` or `grep`: the
query is a literal string, results are whole RFCs ranked by how many lines
match, and each quoted line names its section. `--regex` opts into pattern
matching, in titles or over the mirror; the index cannot take a pattern.
`--json` names the backend in `tool`.

If neither is present, `--fulltext` fails with a message rather than falling
back to titles — a title search silently standing in for a full-text search
answers a different question than the one asked.

Both scopes return at most `--limit` results (default 20, at most 200), and an
empty query is refused. Title results put current RFCs before superseded ones, so
a page cut short at the limit keeps the document you want rather than the one it
replaced. When more matched, the output ends with
`(showing 20 of 795 — raise --limit for more)`, and `--json` carries `total` and
`truncated`. **Report the total, never the number of rows you were
handed** — a truncated page counted as the answer is off by whatever was cut.

`status` says which mode you are in:

```bash
python3 scripts/rfc.py status
```

### When search finds nothing

Without a mirror, the only search is over titles, and it requires *every* term
to appear there. `search "cache control header"` returns nothing, because no RFC
is titled that. Empty output means the query was too specific, not that the RFC
does not exist.

Cut back to the one word that would plausibly be in a title — `search "caching"`,
`search "transport layer security"` — and widen from there. Or go the other way:
if you already believe the number, skip search entirely and confirm it with
`meta`, which is the honest use of what you know.

```bash
python3 scripts/rfc.py meta 9111        # "HTTP Caching" — right, and current
```

Never cite a number you have not put through `meta`. Recalling a plausible RFC
number and being wrong is the failure this tool exists to prevent.

## Read one section, not the whole document

Fetching an entire RFC is usually the wrong move. The average is 53 KB but the
tail runs past 1.6 MB, and a whole specification in context buys nothing over the
two or three paragraphs that answer the question.

List the headings first, then read the one you need:

```bash
python3 scripts/rfc.py sections 9110
python3 scripts/rfc.py get 9110 --section 9.3.1
python3 scripts/rfc.py get 9110 --section "Idempotent Methods"
```

A section includes its subsections and stops at the next heading of the same
depth. Page headers, footers and form feeds are stripped; pass `--raw` to keep
them.

`sections` reports how long each section runs, so the cost of a read is visible
before you pay it. Most are a few hundred lines; a few — RFC 2616's section 13
among them — run past a thousand, and `--max-lines N` caps any read when the
first part of one is enough.

`get` refuses a read of more than 1500 lines that is not a named section — a
whole document, or a `--lines` range that long — and tells you how long it is;
run `sections` and pick one. A section you named is never refused for its
length, however long it is. `--full` lifts the limit when the entire text really
is the goal, which is rarer than it sounds.

Some older RFCs — RFC 768 and RFC 1060 among them — have no numbered headings at
all. `sections` says so instead of inventing any, and a line range is the
fallback:

```bash
python3 scripts/rfc.py get 1060 --lines 200:320
```

Line numbers are the file's real line numbers, so they agree with `sections`,
with `--fulltext` results, and with `rg` or `sed` over the same file.

`--json` works on every read command — `status`, `search`, `meta`, `sections`,
`get` — when you want to parse the output rather than read it.

## Escape hatch

With a synced mirror, the documents are plain text files in `$RFC_MIRROR`, or
under the platform's data directory when that is unset —
`$XDG_DATA_HOME/rfc-ai-tooling`, falling back to `~/.local/share/rfc-ai-tooling`.
`status` prints the path in use. For anything the CLI does not cover, use
ripgrep directly on that path. `$RFC_MIRROR` is usually unset, so ask `status`
for the path instead of using the variable:

```bash
mirror=$(python3 scripts/rfc.py status --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["mirror"])')
rg -l 'Retry-After' "$mirror"
```

## Full-text mode is opt-in — never sync unprompted

Two downloads enable it, and neither is small:

- `python3 scripts/rfc.py sync --index` fetches the prebuilt section index,
  about 270 MB, from this project's GitHub releases. It gives ranked search by
  section and serves every read from disk.
- `python3 scripts/rfc.py sync` copies the corpus as 512 MB of text files from
  the RFC Editor's volunteer-run rsync mirror and takes a few minutes. It is
  what `rg` and `--regex` search.

**Only run either when the user explicitly asks for it.** Do not run one because
`--fulltext` failed, do not run one to "set things up", and do not run one as a
first step. Suggest them, explain the cost, and let the user decide:

```bash
python3 scripts/rfc.py sync --index    # prompts for confirmation
python3 scripts/rfc.py sync            # prompts for confirmation
```

Everything else works without it.
