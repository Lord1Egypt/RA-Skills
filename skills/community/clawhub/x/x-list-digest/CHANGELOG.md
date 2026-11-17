# Changelog

## 2.0.1 - 2026-10-12

- Activate native browser targets before list/detail interactions to avoid background-page wheel timeouts.
- Track explicitly created tabs and close only matching owned targets; preserve budget resumes and user pages.
- Clean terminal-run leftovers on startup and preserve original errors if cleanup persistence fails.
- Document model-iteration budgets separately from collection ceilings and publication-only recovery after local report generation.
- Add lifecycle and resume regression coverage. Keep public configuration generic and scheduling opt-in.

## 2.0.0 - 2026-10-11

- Replace the old HTTP publishing, process wrappers and standalone installer with host-native browsing and Feishu CLI instructions.
- Add incremental archive exclusion, fixed-window boundary evidence, separate list/detail traversal and cumulative protected resume.
- Merge daily reruns and lists, require grounded top-five editorial directions, and include weekly statistics automatically on Sundays.
- Verify complete Feishu readback and persist source associations; reject Sunday archives missing weekly statistics.
- Add a macOS Hermes dedicated-browser preflight using process and IPv4-listener ownership.
- Remove machine-specific paths, private lists and application/destination bindings from public configuration.
- Package English instructions and report labels under MIT-0; retain localized browser-label recognition.
