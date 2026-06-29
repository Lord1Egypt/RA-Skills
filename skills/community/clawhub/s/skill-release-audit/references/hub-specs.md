# Skill Registry / Hub Specifications

Reference for the publishing targets that `skill-release-audit --target <hub>` can
validate against. This documents *what each registry expects* so the auditor can
tune its checks per target. The auditor itself does **not** publish — publishing
is done by each ecosystem's own tooling (e.g. `npx clawhub publish`).

> Sources: ClawHub `docs/skill-format.md`, the Anthropic/cross-platform SKILL.md
> standard, and the iFLYTEK SkillHub ClawHub-compatibility doc (researched
> 2026-06-14). Treat version-specific numbers as point-in-time; re-verify against
> the live spec before relying on exact limits.

---

## Target matrix (summary)

| Target           | Required frontmatter | `version` | README/LICENSE | Slug rule                | Bundle limit | License model |
|------------------|----------------------|-----------|----------------|--------------------------|--------------|---------------|
| `generic`        | name, description    | optional  | not required   | lowercase + hyphen       | —            | —             |
| `anthropic`      | name, description    | optional  | LICENSE opt.   | `^[a-z0-9-]+`, ≤64 chars | <5k tok body | per-skill     |
| `clawhub`        | name, description    | optional  | not required   | `^[a-z0-9][a-z0-9-]*$`   | 50 MB        | MIT-0 (rec.)  |
| `github`         | name, description    | optional  | **README req** | repo-name style          | —            | repo LICENSE  |
| `skillhub`       | name, description    | optional* | not required   | `^[a-z0-9][a-z0-9-]*$`   | 50 MB        | org policy    |

`*` Some private SkillHub deployments require `version`; make it WARN under that profile.

---

## 1. Cross-platform SKILL.md base spec (Anthropic standard)

The portable core adopted by Claude Code, OpenAI Codex, GitHub Copilot, Cursor,
and OpenClaw.

**Frontmatter fields (base):**

| Field           | Required | Notes |
|-----------------|----------|-------|
| `name`          | yes      | Max 64 chars. Lowercase, numbers, hyphens. |
| `description`   | yes      | Max ~1024 chars. Third person. Describes *what* + *when*. |
| `license`       | no       | e.g. `MIT`. |
| `compatibility` | no       | Max 500 chars, free text. |
| `metadata`      | no       | String→string map. Holds `author`, `version`, `allowed-tools`, etc. |
| `allowed-tools` | no       | Experimental. Space-delimited tool whitelist. |

**Directory structure:**
```
skill-name/
  SKILL.md        # required
  scripts/        # optional executable code
  references/     # optional docs loaded on demand
  assets/         # optional templates/icons
  LICENSE.txt     # optional
```

**Guidance:**
- Body recommended < 5,000 tokens (progressive disclosure: only ~100-token
  frontmatter loads at startup).
- No XML in description.

---

## 2. ClawHub spec

**Required:** `SKILL.md` (or `skill.md`).
**Honored ignore files:** `.clawhubignore`, `.gitignore`.
**Install metadata written by CLI:** `<skill>/.clawhub/origin.json`,
`<workdir>/.clawhub/lock.json`.

**Frontmatter — basic:**
```yaml
---
name: my-skill
description: Short summary of what this skill does.
version: 1.0.0        # optional
---
```

**Runtime metadata under `metadata.openclaw`** (aliases: `metadata.clawdbot`,
`metadata.clawdis`):

| Field                | Type       | Meaning |
|----------------------|------------|---------|
| `requires.env`       | string[]   | Env vars that MUST be present (skill can't run without them). |
| `requires.bins`      | string[]   | CLI binaries that must ALL be installed. |
| `requires.anyBins`   | string[]   | CLI binaries where AT LEAST ONE must exist. |
| `requires.config`    | string[]   | Config file paths the skill reads. |
| `primaryEnv`         | string     | Main credential env var. |
| `envVars`            | array      | Per-var declarations: `name`, `required` (bool), `description`. Use `required: false` for optional vars (do NOT put optional vars in `requires.env`). |
| `always`             | boolean    | If true, skill is always active. |
| `skillKey`           | string     | Override invocation key. |
| `emoji`              | string     | Display emoji. |
| `homepage`           | string     | Homepage/docs URL. |
| `os`                 | string[]   | OS restrictions, e.g. `["macos"]`, `["linux"]`. |
| `install`            | array      | Dependency install specs (kinds: `brew`, `node`, `go`, `uv`). |
| `nix` / `config`     | object     | Nix plugin spec / clawdbot config spec. |

**Security analysis (CRITICAL for the auditor):** ClawHub checks that *declarations
match code*. If code references `TODOIST_API_KEY` but frontmatter doesn't declare
it under `requires.env` / `primaryEnv` / `envVars`, it's flagged as a **metadata
mismatch**. → This is the basis for the auditor's "declaration-vs-code" check.

**Constraints:**
- Allowed files: text-based only (allowlist in schema `TEXT_FILE_EXTENSIONS`;
  JSON/YAML/TOML/JS/TS/Markdown/SVG + `text/*` content types; `.ps1/.psm1/.psd1`
  accepted as text).
- Bundle size: **50 MB total**. Embedding includes SKILL.md + up to ~40 non-`.md`
  files.
- Slug: derived from folder name; must match `^[a-z0-9][a-z0-9-]*$`.
- Versioning: each publish = new semver version; tags point to versions (`latest`).
- License: ClawHub **recommends MIT-0** (permissive, no-attribution). Other
  permissive licenses (MIT, Apache-2.0) are generally accepted; avoid restrictive
  or conflicting terms. No paid skills / pricing metadata.

**OpenClaw parser quirk:** OpenClaw requires the `metadata` field as **single-line
JSON**, not multi-line YAML. Deviates from the base spec; trips up hand-authoring.

**Publish (not done by this auditor):** `npx clawhub publish ./my-skill --slug ... --version ...`

---

## 3. SkillHub (ClawHub-compatible private registries)

iFLYTEK SkillHub — and, per ecosystem reports, private SkillHub deployments from
Tencent / Volcano Engine / Aliyun — expose a **ClawHub-compatible API layer**, so
the same `clawhub` CLI works by pointing at a different registry:

```bash
export CLAWHUB_REGISTRY=https://skillhub.your-company.com
clawhub login --token <API_TOKEN>      # needed for private / write ops
npx clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0
```

**Compatibility API endpoints** (subset):

| Endpoint                          | Method | Auth |
|-----------------------------------|--------|------|
| `/api/v1/whoami`                  | GET    | required |
| `/api/v1/search`                  | GET    | optional |
| `/api/v1/resolve`                 | GET    | optional |
| `/api/v1/download/{slug}`         | GET    | optional* |
| `/api/v1/skills/{slug}`           | GET    | optional |
| `/api/v1/publish`                 | POST   | required |

**Namespacing:** internal `@{namespace}/{skill}` maps to canonical slug
`namespace--skill` (global namespace → bare slug). Recommend keeping SKILL.md
`name` aligned with the canonical slug tail.

**Visibility:** PUBLIC / NAMESPACE_ONLY / PRIVATE — affects download auth.

> ⚠️ The Tencent / Volcano / Aliyun publish APIs are reported as ClawHub-compatible
> but were NOT independently verified here. Any future *publisher* (Phase 5) must
> validate each provider's publish endpoint + auth before relying on it. The
> auditor's `--target skillhub` profile only validates *format*, so it does not
> depend on these endpoints.

---

## 4. GitHub (open-source distribution)

Not a skill registry per se, but a common open-source target. Differs from
registries:

- **README.md is expected** (registries like ClawHub treat README as optional /
  sometimes discourage extra top-level docs; GitHub needs it).
- **LICENSE file expected** (this skill ships MIT).
- Slug ≈ repo name (lowercase + hyphen recommended).
- No bundle-size or text-only constraints.
- `metadata.openclaw.*` extensions are harmless (ignored by non-OpenClaw tools).

---

## How the auditor uses this (Phase 3)

`--target <profile>` selects a profile in `profiles/` that declares, per target:
required vs optional frontmatter fields, whether README/LICENSE are required,
bundle-size limit, slug regex, and `version` strictness. Each check module reads
the active profile and adjusts severity instead of hardcoding one registry's rules.
Default profile is `generic` (loosest; the minimal common denominator).
