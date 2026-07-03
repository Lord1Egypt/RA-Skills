# SL Trafiklab API Skill

An [OpenClaw](https://github.com/openclaw) skill that retrieves real-time Stockholm public transport (SL) departures and deviation data. This repository is packaged specifically to be published to and installed from the [ClawHub Registry](https://clawhub.ai).

---

## Repository Structure

This repository is designed for the ClawHub registry distribution format:

- **`_meta.json`**: Registry metadata containing the owner ID, slug, and current version of the skill.
- **`SKILL.md`**: The instruction file loaded by the OpenClaw agent, defining capabilities, monitoring directives, and preferences storage.
- **`references/api.md`**: Technical references and sample payloads for SL sites, departures, and deviation APIs.
- **`.clawignore`**: Instructs `clawhub publish` to ignore files that are not needed at runtime (such as CI workflows and git metadata).

---

## Installation

To add this skill to your OpenClaw workspace:

```bash
clawhub install sl-trafiklab-api
```

This will automatically download the skill assets into your workspace's `skills/sl-trafiklab-api/` directory.

---

## Automated Publishing

This repository is configured with a automated GitHub Action workflow (`.github/workflows/clawhub-publish.yml`) to publish releases to the ClawHub registry.

To publish a new version:
1. Ensure your local changes are committed and pushed to `master`.
2. Create and push a new semantic tag prefixed with `v` (e.g., `v1.0.1`):
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
3. The CI runner will automatically extract the version number, update `_meta.json`, and publish the package to ClawHub.

> **Note:** To enable publishing, you must add your registry token as a repository secret named `CLAWHUB_TOKEN` under **Settings > Secrets and variables > Actions** in GitHub.

---

## Disclaimer

This is an independent, open-source project and is not affiliated with, sponsored by, or endorsed by Samtrafiken or Trafiklab. All public transport data is retrieved from their public API endpoints in accordance with their developer terms of service.

