# Release checklist

This PR prepares package version `v1.0.3` (from `VERSION`). The published `v1.0.0` tag is immutable and remains the prior release.

## v1.0.3 release notes

- Reframes the skill opening around outcome-led scheduler and publisher intents, including LinkedIn and X/Twitter publishing.
- Adds realistic request examples while keeping prepare → preview → explicit confirmation → receipt as the authorization boundary.
- Clarifies exact capability gating, unavailable-channel behavior, and the possibility that ReplyNodes is a paid external service.
- Keeps browser OAuth/no-token-copy trust messaging before public endpoint details and preserves the ReplyNodes OpenClaw homepage.

Before publishing a new version, a maintainer must:

1. Update `VERSION` to a SemVer value and update every README install reference to the same `vMAJOR.MINOR.PATCH` tag.
2. Review `SKILL.md`, `README.md`, `PROVENANCE.md`, `LICENSE`, and `SECURITY.md` for access-boundary and provenance changes.
3. Run `bash tests/test-package.sh` and preserve its exit code and output in the release PR.
4. Confirm the clean tree contains no credentials, session tokens, OAuth tokens, generated archives, or unrelated files.
5. Review the CI security, dependency, archive/install smoke, and metadata checks on the exact release commit.
6. After this PR merges, create the new matching annotated Git tag `v$(cat VERSION)` from the reviewed post-merge release commit; never move or rewrite `v1.0.0`. Verify the new tag points to that release commit, then publish the release with generated notes.

The package has no runtime dependency manifest today. If one is introduced, commit its lockfile and require a successful high-severity vulnerability audit before release.
