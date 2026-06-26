# Issues in release notes + auto-close on release

**Date:** 2026-03-15
**Closes:** #80

## What changed

Three connected changes to make releases track issues properly:

1. **Release notes gate requires issue references.** If the release notes file doesn't contain at least one `#XX` issue reference, wip-release blocks. Every release should close or reference an issue.

2. **Scaffolded template auto-detects issues.** When wip-release scaffolds a RELEASE-NOTES template, it scans commits since the last tag for `#XX` references and pre-populates the "Issues closed" section. The agent just verifies and adds any missing ones.

3. **Auto-close on release.** After creating the GitHub release, wip-release parses the release notes for `#XX` references and runs `gh issue close` on each one (on the public repo). No more manually closing issues after deploy.

## Why

Issues were not being closed when releases shipped. Parker had to check the release notes, cross-reference with the issue list, and close them manually. The release notes didn't say which issues they addressed. This makes it automatic: write the issue number in the notes, the pipeline closes it.
