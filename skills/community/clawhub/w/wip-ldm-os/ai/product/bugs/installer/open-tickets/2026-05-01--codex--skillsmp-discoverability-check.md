# Universal Installer: SkillsMP discoverability check for public skills

**Date:** 2026-05-01
**Owner:** unassigned
**Status:** open
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## What

SkillsMP (`https://skillsmp.com/`) is a third-party discovery surface for public `SKILL.md` ecosystem skills. It presents itself as an open skills marketplace, discovers skills from public GitHub repositories, and documents a REST API for keyword and semantic search.

This ticket tracks whether WIP public skills should have a release-time discoverability check against third-party skills indexes such as SkillsMP.

## Decision frame

SkillsMP should be treated as a **discovery and audit surface**, not as a required deploy target or trust authority.

The WIP source of truth remains:

- the private source repo and public mirror
- npm packages and dist-tags
- `wip.computer/install/<slug>.txt`
- LDM OS catalog metadata
- GitHub releases and release notes

SkillsMP may help users and agents find public WIP skills, but it must not become the source of provenance, install authorization, version truth, or release success.

## Proposed shape

Add a non-blocking post-public-sync check for public skills:

1. After stable release and public mirror sync, identify public products with `SKILL.md`.
2. Verify the public GitHub URL is reachable and the `SKILL.md` frontmatter is valid.
3. Optionally query SkillsMP's keyword search API for the skill name or package slug.
4. Report one of:
   - indexed
   - not indexed yet
   - third-party unavailable
   - skipped because product is private or prerelease-only
5. Never block a release solely because SkillsMP is down, delayed, stale, or rate-limited.

## Out of scope

- Auto-installing from SkillsMP.
- Treating SkillsMP as trusted provenance.
- Blocking stable releases on SkillsMP availability or indexing lag.
- Publishing to SkillsMP as if it were an official WIP deploy target.
- Replacing LDM OS catalog, install-spec URLs, npm, or GitHub releases.

## Acceptance

- A release or audit command can report whether each public WIP `SKILL.md` is likely discoverable through third-party skills indexes.
- Failures are warnings, not release blockers.
- The output clearly labels SkillsMP and similar services as third-party discovery surfaces.
- Documentation says the primary flow remains: user asks for an outcome, agent resolves services through WIP-controlled catalog/install specs/provenance, then composes the bespoke artifact.

## References

- SkillsMP home: `https://skillsmp.com/`
- SkillsMP API docs: `https://skillsmp.com/docs/api`
- Universal Installer master plan: [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)
