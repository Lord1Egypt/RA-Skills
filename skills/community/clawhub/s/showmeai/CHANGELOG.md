# Changelog

## [2.1.0] - 2026-07-18

- Added runtime-enforced progressive onboarding with `needs_key`, `needs_defaults`, and category-complete states.
- Added `onboarding status`, `onboarding models`, and validated `onboarding apply` commands for Agent-guided first-use setup.
- Changed Agent-assisted Key setup so it cannot silently skip model and parameter confirmation.
- Added blocking `ONBOARDING_REQUIRED` errors before creative intake or new generation.
- Added model-specific strict parameter rejection and configurable image quantity defaults for Gemini image models.
- Added `doctor --category` and `paths --json` for deterministic readiness checks and host-neutral path discovery.
- Invalidated category onboarding when low-level defaults change or the selected model is unavailable to the current token group.
- Strengthened the Agent contract to prohibit writing ShowMeAI settings into OpenClaw, WorkBuddy, Hermes, Codex, or other host configuration files.

## [2.0.0] - 2026-07-17

- Added platform-neutral, OS-native configuration and task-state paths.
- Added secure one-time Key setup, validation, and Agent-assisted standard-input flow.
- Added token-group-aware creative model discovery and model-specific parameter guidance.
- Changed the initial image preference to `gemini-3.1-flash-image`, while allowing setup overrides.
- Added unified image, video, 3D, TTS, music, and image-tool commands.
- Added durable terminal-state polling, heartbeats, task journals, recovery, and automatic result downloads.
- Added structured errors, HTTP retry behavior, filename collision protection, and compatibility wrappers.
- Rewrote English and Chinese documentation.
- Completed strict SCK structure, semantic, error-path, and custom runtime verification.
- Added conservative discovery for newly released creative model IDs before their parameter schemas are cataloged.
- Documented `verified_uncataloged` handling in both user guides and the Agent contract.
- Added an offline Agent-assisted setup contract test covering stdin Key validation and persistence.
- Hardened unexpected-error output and redacted reflected credentials from HTTP error bodies.
- Standardized the Agent contract on English execution instructions while preserving author `ian`.
- Kept the concise English file-tree delegation to `README.md`.
- Updated the output-convention contract test for the English section heading.
- Guaranteed requested counts across image models by using native batching when available and bounded parallel single-image completion requests otherwise.
- Added aggregate usage and physical request-count reporting for multi-request image generation.
- Corrected the token-group notice to reference the actual `models` command.
- Detects the real PNG, JPEG, GIF, or WebP signature for base64 image outputs instead of trusting a fallback extension.
- Rejects output filenames containing absolute paths or directory traversal.

## 1.x

- Initial image, Seedance video, and image-to-3D scripts.
