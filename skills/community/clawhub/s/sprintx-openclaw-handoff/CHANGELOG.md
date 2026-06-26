# Changelog

## 0.1.3 - 2026-04-13

- Add Korean and Chinese README variants
- Rewrite access-token guidance so the skill only declares the real required runtime dependency (`sx`)
- Republish the bundle with narrower metadata to reduce registry packaging ambiguity

## 0.1.2 - 2026-04-13

- Rewrite the README for humans instead of maintainers
- Add a clearer quick start, trust boundary, audience, and repo structure explanation
- Republish the registry bundle so ClawHub and GitHub show the same onboarding story

## 0.1.1 - 2026-04-13

- Declare `SX_API_URL` in frontmatter because the troubleshooting path references it
- Add `LICENSE.md` so the published file list carries a visible license artifact
- Keep the published release instructions aligned with the locally verified `clawhub publish` command

## 0.1.0 - 2026-04-13

- Scaffold standalone public repo for the first SprintX ClawHub skill
- Lock the v1 handoff flow to `sx auth -> sx project use -> sx event -> sx artifact add -> sx status -> sx brief`
- Add repo-local validation for frontmatter and instruction contract
