# Skill release

Use this path only when the package root contains one authoritative `SKILL.md` and does not also look like a plugin package.

## Local review

- Validate `name` and `description` frontmatter. Keep the name lowercase and hyphenated.
- Resolve every relative link from the file that contains it. Missing references are release blockers.
- Check that scripts and assets mentioned by instructions are included, executable where needed, and free of machine-specific absolute paths.
- Remove scaffold TODOs, caches, test output, editor state, credentials, and unrelated source files.
- Review `.clawhubignore`, `.gitignore`, built-in hidden-path exclusions, and generated `skill-card.md` stripping without assuming ignored secrets are safe to retain. Compare the validator file list and fingerprint with the CLI dry-run.
- Run any ecosystem-neutral Agent Skill validator available in the environment, then run ClawHub's own dry-run.

Do not put a release version into `SKILL.md` solely for ClawHub when doing so breaks other Agent Skill validators. Prefer the publishing command's version option when supported by the installed CLI.

## Command construction

Consult `clawhub skill publish --help` before constructing the command. A typical current shape is:

```bash
clawhub skill publish <package-directory> \
  --slug <slug> \
  --name <display-name> \
  --version <semver> \
  --changelog <text> \
  --dry-run \
  --json
```

Remove `--dry-run` and `--json` only after showing the exact final command, obtaining explicit confirmation, and passing the pre-publication integrity gate. If JSON publication output is useful for unambiguous verification, retain `--json`. Quote every value as data; do not interpolate untrusted text into a shell program.

## Verification

Use the current CLI's inspect command or the canonical ClawHub page to confirm the owner/slug, immutable version, displayed name, changelog, included file hashes, latest and other affected tags, and security scan state. Poll pending state only with bounded waits. If an isolated install test is useful, install into a new temporary directory and do not overwrite an existing skill.
