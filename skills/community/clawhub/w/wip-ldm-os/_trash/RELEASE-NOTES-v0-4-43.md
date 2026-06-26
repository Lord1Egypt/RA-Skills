Every change flows through the repo and the installer. Never touch the running system directly.

The release pipeline rule now leads with the principle that was missing: deployed files at ~/.ldm/, ~/.claude/, ~/.openclaw/ are never edited directly. Every change goes through the repo, gets released, and ldm install deploys it. The guard was already enforcing this. Now the rule says why. Every feature plan must answer 5 questions: what source files change, what does ldm install deploy, what needs to update for fresh vs existing install, what docs need updating, what files does the installer touch.

The install prompt got the fix Parker asked for. Existing users no longer get a generic "What is LDM OS" explainer. The prompt checks first (which ldm), shows what's new if installed, and only explains if you're new. The prompt lives in shared/templates/install-prompt.md and gets deployed by ldm install to settings/templates/. The README references the same text. One source, no drift.

The installer now deploys shared templates to the workspace settings/templates/ folder, reading the workspace path from ~/.ldm/config.json.

Closes #202.
