# Global Skill Discovery

Skill2Team is intended to be installed as a global, user-invocable, discoverable skill.

Keep these signals aligned:

- folder name: `skill2team`;
- frontmatter `name: skill2team`;
- frontmatter `display_name: Skill2Team`;
- frontmatter `version: 1.9.2`;
- frontmatter `user-invocable: true`;
- frontmatter `visibility: global`;
- frontmatter `global-skill: true`;
- frontmatter `discoverable: true`;
- `metadata.openclaw.scope: global`;
- `metadata.openclaw.discoverable: true`;
- `metadata.openclaw.global_skill: true`;
- `metadata.openclaw.registry_name: skill2team`;
- `data/global_skill_manifest.json` with matching id, aliases, keywords, routes, deliveries, and entry file.
