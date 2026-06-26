# Discussion: Skill Naming Conflict Resolution (USM)

To prevent users from unintentionally creating skills with names that collide with existing or future official skills (e.g., `docker`, `git`, `search`), we propose the following multi-layered approach.

## 🎯 The Problem
In the USM 2-layer architecture (`~/.skills/`), all skills reside in the same flat directory. If a user creates a skill named `git` to manage their local commits, and then uses `skill-installer` to download an "official" `git` skill from SkillHub, one will overwrite the other, or the symlinks will collide.

## 💡 Proposed Solutions

### 1. `skill-creator`: Front-end Prevention
- **Decision**: Keep local name as `skill-creator` but use registry slug `skill-creator-usm`.
- **Prompt**: During the "Interview" phase, the AI checks if the chosen name is a common keyword (e.g., `git`, `docker`, `search`, `openai`).
- **Logic**: If a collision is detected locally or globally (by checking `~/.skills/`), proactive advice is offered:
  - "The name `docker` is common. I suggest `user-docker` or `docker-management` to avoid conflict."
- **Enforcement**: In `SKILL.md` frontmatter, the `name` should be unique.

### 2. `skill-manager`: Middle-ware Governance
- **Provisioning Agent**: In `agents/provision_agent.md`, the provisioning process MUST check for duplicate folders.
- **`meta.yaml` Namespace**: Add an optional `namespace` or `owner` field to `meta.yaml` to allow logical grouping (e.g., `Ziwei/docker`).

### 3. `skill-installer`: Back-end Compatibility
- **Collision Flag**: The installer should detect if the downloaded `<slug>` matches an existing folder in `~/.skills/` and prompt the user to:
  - **Overwrite**: Standard update.
  - **Fork/Rename**: Keep both by appending a suffix.

---

## 🙋 User Choice Required
Should we:
1.  **Enforce a `namespace` field in `meta.yaml`** for all user-created skills?
2.  **Add a "Naming Conflict Check" step** to `skill-creator` instructions only?
3.  **Both** (Stricter engineering + AI advisory)?
