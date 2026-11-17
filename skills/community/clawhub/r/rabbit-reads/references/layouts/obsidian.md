# Layout: obsidian

**Index file:** index.md
**Link syntax:** wikilink
**Frontmatter keys:** source, kind, tags, aliases
**Note kinds:** concept
**Spine notes:** chapter:8-20, topic:8-25, summary:20-40
**Folders:** concepts/, chapters/, topics/

An Obsidian-style vault instead of a flat folder. The doc set is still cut by
concept at the book type's grain; only the shape around the docs changes.

- `concepts/<slug>.md`, one per concept: the book-type template as usual, plus
  a frontmatter block carrying every declared key with a non-empty value.
  Wikilinks (`[[concepts/other-slug]]` or `[[other-slug]]`) replace markdown
  links in See also.
- `chapters/<nn>-<slug>.md`, one per source chapter: an orienting sentence and
  wikilinks out to the concepts that chapter develops. A spine note is a map,
  not a summary: link lines must strictly outnumber prose lines.
- `topics/<term>.md`, an alphabetical topic entry pointing back into the
  concepts that use the term.
- `summary.md`, a whole-source note in the same spine style.
- `index.md`, a Map of Content: every concept appears as a wikilink target in
  it exactly once, and no wikilink in it is unresolved.

Spine-note kind-to-location convention: a spine note's kind is its containing
folder with the trailing `s` stripped (`chapters/x.md` is kind `chapter`,
`topics/x.md` is kind `topic`), and a root-level file named `<kind>.md` matches
that kind (`summary.md` is kind `summary`). The declared `Spine notes` bands
are line ranges per kind, and each band's kind names its folder this way.

Free-form files a book type declares stay root-level. Concept docs are tracked
and indexed relative to the vault root, so index rows and See also targets are
paths like `concepts/<slug>.md`.
