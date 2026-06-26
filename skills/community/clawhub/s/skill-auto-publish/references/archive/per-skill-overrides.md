# Per-Skill Overrides

When these slugs appear in a request, use the registered canonical source path. Do not guess.

## Override Table

| slug | canonical source path | required first major section | notes |
|------|---------------------|------------------------------|-------|
| `waste-audit` | `/root/.openclaw/skills/waste-audit/` | `## Features` | User explicitly rejected routing-first structure. `## Features` must be the first section, not `## Trigger / Routing Contract`. |
| `buffett-do` | `/root/.openclaw/skills/buffett-do/` | default | Canonical source is NOT under Hermes workflow-kits. Published from local OpenClaw workspace for v1.1.3 through v1.1.7. |
| `skill-release-lifecycle` | `/root/.hermes/skills/workflow-kits/skill-release-lifecycle/` | default | Release quality lifecycle skill. Used for pre-publish review gate. |
| `clawhub-auto-publish` | `/root/.hermes/skills/workflow-kits/clawhub-auto-publish/` | default | This skill. Publishing execution workflow. |

---

## Detailed Notes

### waste-audit

**Path:** `/root/.openclaw/skills/waste-audit/SKILL.md`

**Structure requirement:** `## Features` must be the FIRST major section. User explicitly rejected the routing-first pattern where `## Trigger / Routing Contract` appears at the top.

**Why:** User found the routing contract wording too technical for the public page activation section. The `## Features` section now serves as both the human-facing overview and the routing signal.

**Top install block limitation:** Even with `--name "OpenClaw Token Waste Audit"` and body `## Install` section with `waste-audit --global`, the top auto-generated install block still shows `openclaw skills install waste-audit` (no `--global`). This is a ClawHub platform limitation, not a source file issue.

---

### buffett-do

**Path:** `/root/.openclaw/skills/buffett-do/SKILL.md`

**Note:** This is NOT under Hermes workflow-kits. It is under the OpenClaw local workspace (`/root/.openclaw/skills/`).

**Published versions:** v1.1.3 through v1.1.7 were published from this path.

**HTML comment pitfall:** The v1.1.3 publish used `<!-- internal activation coverage: ... -->` to hide internal trigger phrases. ClawHub does NOT strip HTML comments — they appear as raw visible text on the public page. This was a user-corrected mistake.

---

### skill-release-lifecycle

**Path:** `/root/.hermes/skills/workflow-kits/skill-release-lifecycle/SKILL.md`

**Purpose:** The release gate skill. Used by BG/Hermes to evaluate whether a skill is ready for publish before invoking `clawhub-auto-publish`.

**Note:** When `GUARDIAN REVIEW: required` is set, the review must be completed using `skill-release-lifecycle` before `clawhub-auto-publish` proceeds.

---

## Rule

For any slug NOT in this table: use the path provided in the request packet. If no path is provided → return `NEEDS_INFO`.

Do not mix up `waste-audit` (OpenClaw workspace path) with skill-release-lifecycle (Hermes workflow-kits path). They are separate registries.