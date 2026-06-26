Fix the deploy bug. Every release since the Mar 24 migration silently failed to deploy the install skill to wip.computer because .publish-skill.json still pointed to the old iCloud path. wip-release copied the file to a path that didn't exist, said "deploy skipped," and moved on. The VPS stayed stale. We manually deployed three times today before finding the root cause.

One-line fix: updated websiteRepo in .publish-skill.json from the old iCloud location to ~/wipcomputerinc/repos/wip-web/wip-websites-private. Now wip-release will find deploy.sh and auto-deploy the skill to wip.computer on every release.

This is a symptom of the larger problem: hardcoded paths that break when the workspace moves. The real fix is reading websiteRepo from settings/config.json so there's one place to update. Filed #208 for that.

Closes #208.
