# Changelog

## [0.2.1](https://github.com/es6kr/skills/compare/web-browser-v0.2.0...web-browser-v0.2.1) (2026-06-19)


### Bug Fixes

* bundle skill patches across 7 scopes ([f18f47c](https://github.com/es6kr/skills/commit/f18f47c2d05f13b8e3f3ad42675a2dabbb31c824))
* **credential:** add PAT scope matrix + Settings UI procedure + Service × Store persist matrix ([c61525b](https://github.com/es6kr/skills/commit/c61525b1a2d886b677c85d2638d39a1e2311c142))
* **web-browser:** compress SKILL.md description + replace credential-issue placeholder ([4fb1148](https://github.com/es6kr/skills/commit/4fb114800991d757c07eb63d1a3d3b8fc19bde4a))

## [0.2.0](https://github.com/es6kr/skills/compare/web-browser-v0.1.0...web-browser-v0.2.0) (2026-06-12)


### Features

* decompose workflow/git rules + rename web-ui-test→web-browser ([#50](https://github.com/es6kr/skills/issues/50)) ([e10d48f](https://github.com/es6kr/skills/commit/e10d48fea4e507b95888de44812b53484d32128d))

## [0.1.0] (2026-06-09)

Initial release. `web-browser` is the environment-aware browser-operations skill, succeeding the
legacy `web-ui-test` skill (which is retained, local-only, for `sso-verify`).

### Features

* **ui-test**: snapshot analysis, click/fill/verify UI, page-state diagnosis (migrated from web-ui-test).
* **cdp-trace**: CDP-based closed shadow DOM cascade diagnosis (migrated from web-ui-test).
* **credential-issue**: new topic — take a service + command as parameters, open the service login
  screen via the detected backend, wait for the user to sign in, then issue the requested access
  key / token / secret and hand the result to follow-up automation (aws-cli upload, gh secret set,
  etc.). chrome-devtools backend preferred for real-session reuse.
* Shared **Step 0** environment detection (wmux/cmux/Playwright) + user-visibility HARD STOP.
