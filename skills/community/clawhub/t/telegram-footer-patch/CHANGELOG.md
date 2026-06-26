# Changelog

## 1.0.11
- Live-validate OpenClaw `2026.4.12` with a real Telegram private-chat acceptance after a true process restart.
- Document that runner-only patching is insufficient on `2026.4.12`; the real delivery/send path also has to be patched.
- Update patch/revert tooling to include `delivery-*.js` candidates and verify the live-path patch more conservatively.
- Clarify in docs that hot refresh / SIGUSR1 is not enough evidence by itself; acceptance requires a new PID plus a real Telegram private-chat reply showing the footer.

## 1.0.10
- Add a second live validation boundary: OpenClaw `2026.4.5` is now real-world verified via Telegram private-chat acceptance.
- Document the current live-validated bundle path on `2026.4.5`: `agent-runner.runtime-UIIO4kss.js`.
- Update README/SKILL wording so published support claims distinguish between live-validated versions (`2026.3.22`, `2026.4.5`) and merely compatibility-targeted versions.

## 1.0.9
- Clarify version-support wording: live-validated on OpenClaw `2026.3.22` only; untested versions must not be described as “supported”.
- Document the exact live-validated bundle path: `agent-runner.runtime-BWpOtdxK.js`.
- Tighten acceptance wording so smoke test / static patch verification is no longer treated as final proof; real Telegram private-chat reply validation is required.

## 1.0.8
- Remove stray Python bytecode/cache artifacts from the package again.
- Tighten README/SKILL wording to reduce false-positive suspicious scanning while keeping behavior unchanged.

## 1.0.7
- Fix: footer now appends correctly for Telegram streaming replies that use HTML payloads (not just text payloads).
- Fix: patch reapply uses a function replacement to avoid accidental backslash/escape expansion when updating marker blocks.

## 1.0.6
- Add install/run safety notice to docs.
- Add preflight checks and disable Python bytecode cache writes in scripts.

## 1.0.5
- Remove Python bytecode/cache artifacts from the published package (avoid false-positive malware/suspicious flags).

## 1.0.4
- Compatibility update for latest OpenClaw dist bundles.
- Verified current patch flow against local OpenClaw `2026.3.7`.
- Refreshed skill docs to reflect the current footer format and upgrade-aware reapply workflow.

## 1.0.2
- Updated homepage/skill copy to reflect the current footer format: `🧠 Model + 💭 Think + 📊 Context`.
- Added footer preview image to the top of the README.

## 1.0.1
- Added license and maintenance documentation.
- Clarified apply, rollback, and verification steps.
- Added lightweight README for project hygiene.

## 1.0.0
- Initial release: private-chat footer injection, dry-run check, backup, rollback script.
