# Query pack: devtools / CLI / SDK / infra

For products sold to engineers: CLI tools, SDKs, observability, infra,
dev-productivity tools. Buyer and user are usually the same person (or a
small team), which makes Individual and Segment prospects more common than
Company here.

## Query buckets

**Explicit demand**
- `"looking for a [category] tool" site:reddit.com`
- `"alternative to [competitor]" site:news.ycombinator.com`
- `"does anything exist for [job]"` on Hacker News, r/devops, r/programming
- GitHub issue search: `is:issue "would be nice if" [feature]` in relevant repos

**Pain**
- `"[workflow] is so painful"`, `"[task] takes forever"` on HN/Reddit
- `"why does [competitor] not support"` in GitHub issues and forums
- StackOverflow questions tagged with the product's category that have no
  accepted answer (signals an unsolved, repeated problem)

**Workaround**
- Custom scripts or Makefile/CI hacks described in blog posts as "how we
  solved X ourselves" — often precedes buying a tool for the same job
- Internal tooling posts on engineering blogs describing a hand-rolled
  version of what the product does

**Switching**
- `"migrating from [competitor]"`, `"[competitor] pricing change"`,
  `"[competitor] sunset"` / `"[competitor] deprecated"`
- GitHub issues in the competitor's own repo tagged with churn language
  ("switching to", "moving away from")

**Timing**
- Company engineering blog posts announcing a new stack, a rewrite, or an
  infra migration (new adopters of the underlying tech are prime targets)
- Job posts for roles this product serves (e.g. "Platform Engineer",
  "Developer Experience") — signals budget and a champion about to exist
- Recently created GitHub repos in the product's category (proxy for teams
  actively building in this space right now)

## Source mix specific to this vertical

- Hacker News (front page and comments — comments often have the real pain)
- r/devops, r/programming, r/ExperiencedDevs, category-specific subreddits
- GitHub issues/discussions in both the product's own repo and adjacent/
  competitor repos
- Engineering blogs (many companies publish "why we chose X" or "why we
  built our own Y" posts — both are qualification signals)
- Dev.to, Hashnode for indie/solo-maintainer signals

## Classification notes

- A solo maintainer of a popular open-source project is almost always an
  **Individual**, even if they're "at" a company — they're personally
  addressable via GitHub/Twitter.
- Treat a company's engineering blog post as a **Company** signal only when
  the ask is a partnership/integration; if it just describes one engineer's
  pain, look for that engineer's name/handle and classify as Individual.
