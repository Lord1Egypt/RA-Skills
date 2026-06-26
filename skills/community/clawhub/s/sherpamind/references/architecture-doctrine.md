# Architecture Doctrine

## The SherpaMind split

SherpaMind has two clean halves:

### 1. Backend/service half
Responsible for:
- data ingestion
- syncing
- enrichment
- cleanup/normalization
- metadata extraction
- structuring
- chunking
- replaceable derived artifact generation
- background maintenance/runtime behavior

### 2. OpenClaw skill-front half
Responsible for:
- teaching OpenClaw when SherpaMind should activate
- teaching OpenClaw which retrieval/summary commands to use
- teaching OpenClaw how to answer SherpaDesk questions efficiently from prepared data
- keeping the retrieval/query strategy aligned with the backend’s actual capabilities

## The mantra

- **Backend prepares the data.**
- **Skill-front teaches access.**
- **OpenClaw reasons at query time.**

If a change blurs those boundaries, it should be treated as architectural drift.

## Anti-drift rules

### Backend should own
- richer source capture
- stronger cleanup
- stronger metadata
- better chunking
- better retrieval artifacts
- stronger vector readiness
- safe/background runtime behavior

### Skill-front should own
- activation guidance
- retrieval command strategy
- factual workflow guidance
- examples of how to query the prepared data
- public-safe anonymized examples and reference material

### OpenClaw should own
- interpretation
- open-ended reasoning
- contextual synthesis
- comparative analysis across tickets/accounts/technicians
- user/technician/client voice analysis over retrieved ticket history
- final user-facing analytical conclusions

## Change checklist

When backend capabilities change, ask:
1. Did the canonical/private data model change?
2. Did the public artifact shape change?
3. Did retrieval commands change?
4. Did new retrieval surfaces become available?
5. Did old commands become misleading or obsolete?
6. Does `SKILL.md` still teach the best activation/query strategy?
7. Do `README.md` / query-model docs still describe reality?

If any answer is yes, update the skill-front/references in the same wave.

## Preferred bias

When choosing between:
- hardcoding interpretation into SherpaMind
- improving data prep/retrieval so OpenClaw can interpret later

prefer the second option unless there is a strong reason not to.
