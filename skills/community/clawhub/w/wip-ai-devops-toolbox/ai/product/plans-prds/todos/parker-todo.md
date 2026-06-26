# Parker ... To Do

*Created 2026-02-28, updated 2026-03-11*

---

## To Do

### 1. Renew npm token (BLOCKED)

The npm publish token in 1Password (`op://dev/npm-publish-token/credential`) is expired or revoked. Need to:
1. Log in to npmjs.com
2. Generate a new publish token
3. Update the 1Password item
4. Then publish: `cd tools/wip-license-hook && npm run build && npm publish --access public`

Package name: `@wipcomputer/wip-license-hook` v1.0.0. Already built and ready. Blocks all npm publishing.

### 2. Record a 2-minute demo video

Show the full wip-release flow in action:
- AI calls `wip-release patch --notes="..."` in terminal
- Version bumps in package.json
- CHANGELOG.md generates automatically
- Git commit + tag created
- npm publishes
- GitHub release appears

Use asciinema or screen recording. Post to README and share on X.

### 3. Create an example template repo

A minimal repo people can clone and immediately use wip-release on:
- Simple package.json with a version
- CHANGELOG.md (started)
- README: "clone this, run `wip-release patch --notes="first release"`, see what happens"

Could be `wipcomputer/wip-release-example`.

---

## Done

_(nothing moved here yet)_

---

## Deprecated

_(nothing yet)_
