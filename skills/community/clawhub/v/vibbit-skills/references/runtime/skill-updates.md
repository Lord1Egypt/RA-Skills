# Skill updates

For an installed Vibbit Skill, attempt one update before the first actual Vibbit operation in each conversation. Mark the attempt before starting, including failures, so rereading the entry after an update does not recurse. Skip discussion, dry runs, local-only work, user-disabled updates (`VIBBIT_AUTO_UPDATE=0`), and any production already in progress. Follow host execution permissions.

Only a copy installed through `skills add vibbit-ai/skills` with recorded upstream tracking can use this path. Do not update a maintenance source tree or a manually copied/ZIP Skill. For an untracked copy, explain once that migration requires the normal installation command; continue with the local version and do not reinstall automatically.

Use the installation record and actual loaded Skill path to select the scope. Update the loaded project installation with `-p`, or the loaded user installation with `-g`; do not update other Skills or both scopes indiscriminately. The command is:

```bash
npx --yes skills@latest update vibbit-skills -y -g
```

Use `-p` instead of `-g` for a project installation. Apply a total deadline of 20 seconds through the command runner. If it remains running at the deadline, stop that update process before continuing; do not leave it modifying files during production.

Success: reread the installed SKILL.md and only the references needed for the current task, then continue quietly. A file update does not replace instructions already read into the conversation. Report success only when the command confirms an update or that the installation is current. Failure, missing tracking, offline access, or a timeout: briefly say the current local version will be used, and continue if it is usable. Do not loop, update unrelated software, or reject the creative task solely because upgrading failed.

Updates replace distributed instructions, references, and bundled scripts. Account selection and private credentials live outside the Skill and must not be overwritten or included in a release. Updates follow the recorded upstream source/ref, not necessarily the newest GitHub Release. A user-pinned source stays pinned.

[Installer update documentation](https://github.com/vercel-labs/skills#skills-update)
