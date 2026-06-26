# ClawHub Skill Audit Standards (2026 Reference)

Based on current registry behavior and security reports, the following standards must be met for a GREEN PASS:

## 1. Governance & Metadata
- **Manifest Alignment**: `_meta.json` must exactly match the capabilities declared in `SKILL.md`.
- **Identity (Provenance)**: `ownerId` must match the current authenticated user's hash ID.
- **Dependency Transparency**: Every binary (`requires.bins`) and Python package (`requires.python`) must be explicitly declared in the manifest.
- **Autonomous Gating**: High-risk skills must set `disable-model-invocation: true` if they can perform sensitive local actions without human intent.

## 2. Security (Code Level)
- **Zero Persistence**: No 'ghost processes' or permanent listeners. Services must have auto-cleanup/lifespan logic.
- **No Hardcoding**: Absolutely no personal paths (e.g., `/home/username`). Use dynamic resolution.
- **Loopback Lockdown**: Relays and CDP endpoints must bind strictly to `127.0.0.1`.
- **Explicit Gating**: High-privilege scripts must verify human presence through interactive challenges or secure lockfiles.

## 3. Transparency (Documentation)
- **Asset Disclosure**: 100% of bundled scripts must be listed in an 'Asset Inventory' section.
- **Legal Disclaimer**: Mandatory disclaimer regarding ethical use and isolated environments.
- **Environment Policy**: Clear recommendation to run only in Docker/VMs for high-risk tools.

## 4. Install Integrity
- **Predictable Install**: No remote binary downloads. All logic must be contained or available via standard package managers (apt, pip).
- **Requirements**: A standard `requirements.txt` must exist in the root if Python is used.
