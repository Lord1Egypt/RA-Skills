# Storage Specification

> This file defines how different source-research artifacts should be stored in a portable way.

## 1. Default portable layout

If the workspace does not already have a source-research structure, create a dedicated workspace directory:

```text
.source-research/
  README.md
  source-pools/
    index.md
    <pool-name>.md
  acquisition/
    <pool-name>.md
  filtering/
    <pool-name>.md
  high-quality-sources/
    index.md
    <pool-name>.md
  high-quality-information/
    index.md
    <pool-name>.md
  rejections/
    index.md
    <pool-name>.md
  programs/
    README.md
```

This follows the same pattern used by strong skills that keep their persistent data in a dedicated top-level directory such as `.learnings/` or `.autonomous/`.

## 2. Source pool information

Store pool definitions in a canonical pool file.

What belongs there:
- pool name;
- pool type;
- what information it is good for;
- current pool status;
- whether it seems worth further investment.

## 3. Acquisition and filtering methods

Store stable method docs in a methods area.

Examples:
- how to acquire from X
- how to acquire from Weibo
- how to filter high-quality accounts
- how to filter arXiv leads

These files should describe:
- manual method;
- semi-automated method;
- engineering direction;
- input/output structure;
- when the method is worth reusing.

## 4. High-quality source lists

Store filtered results in a canonical high-quality source file, or later split by pool when size grows.

What belongs there:
- long-term tracked sources;
- observation list;
- why each source is valuable;
- source direction/topic;
- current confidence/status.

## 5. Rejection conclusions

If a pool or source is judged not worth continued investment, store a reusable rejection conclusion.

Preferred locations:
- inline in the pool entry; or
- a dedicated rejections file; or
- a dedicated note when the reasoning is substantial.

Minimum contents:
- what was evaluated;
- why it is not worth continued investment now;
- whether there is any reopen condition.

## 6. Information results / notes / outputs

When source information is used to produce content, the produced artifact should live in the destination system, not inside the skill.

Examples:
- blog output -> the blog content system
- notes -> the workspace's notes/docs area
- framework updates -> framework or methodology docs

## 7. Programs and automation

If acquisition/filtering is worth engineering, store code outside the skill’s markdown docs.

Preferred pattern:
- keep stable guidance in docs;
- keep scripts/programs in a real code or automation directory.

## 8. Rule of thumb

- Framework rules -> framework directory
- Pool metadata/status -> pool file
- Acquisition/filtering rules -> methods area
- Filtered source results -> high-quality source file
- Rejection decisions -> recorded conclusion
- Programs/automation -> code assets outside skill prose
