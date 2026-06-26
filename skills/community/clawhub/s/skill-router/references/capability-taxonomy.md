# Capability Taxonomy

Skill Router should map tasks to **capabilities first**, and only then resolve capabilities to installed skills.

Do not hard-code one user's local skill list as the universal truth.

---

## Core idea

Use this order:
1. identify the task's dominant capability need
2. check which installed skills appear to satisfy that capability
3. recommend the strongest installed fit
4. only suggest finding or installing a new skill if installed options are clearly insufficient

---

## Capability categories

### 1. browser-control
Use for:
- browser navigation
- clicking, typing, filling forms
- screenshots
- tab control
- interactive website workflows

### 2. browser-reading
Use for:
- reading page content
- extracting text from live pages
- lightweight inspection of a rendered site

### 3. github-workflow
Use for:
- issues
- pull requests
- releases
- workflow runs
- GitHub API operations

### 4. skill-discovery
Use for:
- finding whether a skill exists
- searching for new skills
- identifying likely install candidates

### 5. skill-vetting
Use for:
- reviewing unknown skills before installation
- checking trust and safety of third-party skill sources

### 6. skill-publishing
Use for:
- publishing skills
- updating skills on registries
- ClawHub-related skill distribution tasks

### 7. skill-creation
Use for:
- creating a new skill
- updating a custom skill's structure and bundled resources

### 8. orchestrated-execution
Use for:
- complex tasks needing decomposition, preflight, execution, validation, and distillation
- coordination-heavy work spanning multiple phases

### 9. distillation
Use for:
- writing down lessons
- converting work into reusable knowledge
- extracting next-time rules

### 10. sop-generation
Use for:
- converting a process into step-by-step SOP form
- generating reusable operating procedures

### 11. notes-vault
Use for:
- Obsidian vault work
- structured markdown note maintenance

### 12. summary-extraction
Use for:
- summarizing URLs
- summarizing PDFs, images, audio, video, or external content

### 13. weather-info
Use for:
- current weather
- short forecasts

### 14. feishu-docs
Use for:
- Feishu document reading and writing

### 15. feishu-drive
Use for:
- Feishu cloud drive / folders / storage

### 16. feishu-permissions
Use for:
- sharing / permissions / collaborators in Feishu assets

### 17. feishu-wiki
Use for:
- wiki / knowledge base navigation in Feishu

### 18. backup-restore
Use for:
- OpenClaw backup / restore / migration / rollback workflows

---

## Important rule

These capability names are internal routing concepts, not user-facing jargon.

When replying, prefer concrete recommendations like:
- "This is a browser-control task. Use your installed browser skill."
- "This is mainly a GitHub workflow task; use your GitHub skill first."

Avoid exposing the taxonomy unless the user explicitly wants design details.
