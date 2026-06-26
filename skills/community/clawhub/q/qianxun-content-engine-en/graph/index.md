# Graph Index

> The agent reads this file first when entering this skill, then follows `[[wikilinks]]` to load related nodes.

## What is this?

The "memory / soul / context" of Content Engine. Brand, audience, platform, hooks, and styles live in separate `.md` files connected by `[[]]` wikilinks. The agent loads on demand.

## Brands served

> Single-brand or multi-brand both fine. One row per brand, link to its brand-story node.

- **{{Your-Brand-1}}** → [[brand/brand-story]] · founder / values / positioning
- _(duplicate this row for additional brands)_

# TODO: Replace placeholders with your real brand name(s), or delete and write your own line.

## Node map

Grouped by purpose. Parenthesis = one-line use case for that node.

### Brand
- [[brand/brand-voice]] — cross-platform brand voice DNA (tone, vocabulary, banned phrases)
- [[brand/brand-story]] — brand story / founder / store background

### Platform
- [[platforms/xiaohongshu]] — XHS playbook (deconstruction lens + platform rules + observation log)
- _v2 to add: Douyin, WeChat Channels_

### Audience
- [[audience/segments]] — target audience segmentation (persona, concerns, decision path)

### Engine
- [[engine/hooks]] — hook library (categorized by emotion type; auto-fed by deconstructions)
- [[engine/style-tags]] — style tag dictionary (avoid coining new words every time)
- [[engine/taboo]] — banned words / compliance requirements

---

## Conventions

1. **New node** → pick a stable short name (kebab-case), add to "Node map"
2. **Modifying existing nodes** → append a "Change log" entry at the end of the file with date + source (which deconstruction triggered it)
3. **Cross-references** → always use `[[path/filename]]` (no `.md` suffix), e.g., `[[brand/brand-voice]]`
4. **Graph is append-only**: don't remove old observations; conflicts get ⚠️ for human review

---

## Status

- [ ] brand-voice filled
- [ ] brand-story filled
- [ ] xiaohongshu playbook basics filled
- [ ] segments has at least 1 audience layer
- [x] hooks template ready (will be auto-extended by deconstructions)
- [x] style-tags template ready
- [ ] taboo filled

# TODO: Flip [ ] → [x] as you complete each. Once the first 4 are done, the next deconstruction will run in brand-aware mode.
