# Public work collection contract

## Browser and author checks

Honor the user's browser selection. Otherwise identify the connected browser and confirm the visible account without changing it. Use separate research tabs and fresh page state after navigation. Obtain rendered public content through documented browser operations, not authenticated shell requests or cookie extraction.

Discover work links through the profile, Articles tab and visible dated searches. Where available, span recent and older windows, multiple subjects, ordinary and popular works. Record unavailable strata and selection bias. A timeline's first screen is not a representative corpus.

For X, locate the primary author's block and permalink before extracting. Names, dates and cover images inside a quote belong to the quoted work. Open expanded/detail views and read through the ending. Native Articles need a complete title and body; an article cover in a quote does not change the primary post's genre. A long post stays a post, a grouped thread is one thread, and external articles occupy a separate source class.

An external archive needs a visible cross-link or a verified exact-body correspondence with a primary X work. Pending attribution stays pending. Do not label an archive-only profile as a confirmed X-author profile.

Use only supported export mechanisms. If the browser returns text, save that public text through file tools. Parsing a run's own public-content tool output is permissible only for narrowly identified blocks; never export the surrounding chat or unrelated records. Inspect images separately; text completion does not prove visual evidence was understood.

## Record shape

One JSON object per work in a JSONL file. A thread records ordered parts and one joined body. Required audit observations use this structure:

```json
{
  "author": "example",
  "medium": "post",
  "format": "short_post",
  "source_kind": "x_native",
  "url": "https://x.com/example/status/123",
  "title": "",
  "date": null,
  "date_source": "unknown",
  "captured_at": "2026-01-01T12:00:00Z",
  "body": "Complete primary authored text",
  "author_verified": true,
  "identity_status": "confirmed",
  "identity_evidence": "Visible primary account and permalink were inspected",
  "complete": true,
  "completeness_evidence": "Detail opened and ending inspected",
  "group_id": "123",
  "coauthors": [],
  "exclude_reason": "",
  "campaign": "",
  "images": [],
  "metrics": null
}
```

`medium` accepts `post`, `article`, `thread`. Formats are `short_post`, `long_post`, `x_article`, `external_article`, `thread`. Sources are `x_native`, `author_archive`, `mirror`. Retain mirrors as a separate stratum even after corroboration. Missing dates and metrics are null. Coauthors are actual additional authors, not interview subjects.

## Checkpoint and recovery

Preserve raw capture batches. Put normalization and exclusions in new files. Start `run-status.md` with stage, result and next action, followed by author/genre counts, source classes, remaining links and observed failures. Recover by canonical URL and body hash rather than remembered scroll position.
