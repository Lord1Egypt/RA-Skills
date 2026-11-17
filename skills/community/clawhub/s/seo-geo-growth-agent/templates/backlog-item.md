# Backlog item template

Use this as a proposed, reviewable output. Filling it out does **not** create or
publish a backlog item.

```yaml
status: proposed
requestType: audit | GEO | competitor-gaps | opportunities | content-brief
title: "<specific opportunity>"
problem: "<evidence-backed problem or gap>"
observation: "<what the supplied/allowlisted source shows>"
inference: "<hypothesis, clearly labeled>"
recommendation: "<proposed read-only next action>"
audience: "<ICP or audience>"
conversionGoal: "<goal>"
priority: P0 | P1 | P2 | P3
confidence: low | medium | high
effort: low | medium | high
evidence:
  - url: "https://<allowlisted-source>"
    title: "<source title>"
    observedAt: "YYYY-MM-DD"
limitations: []
nextSafeStep: "Have an authorized owner review and explicitly create this item."
```

The agent must never submit this template to a backlog, CMS, social channel, or
publishing system. If the requester asks for that, follow the refusal in
`../SKILL.md` and return this proposed artifact instead.
