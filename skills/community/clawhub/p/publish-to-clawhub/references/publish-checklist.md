# Publish Checklist

Use this file when you need concrete checks or command patterns for GitHub and ClawHub publishing.

## Recommended Order

For the clean local workflow:

1. improve or validate the skill itself
2. publish the local skill folder to ClawHub
3. add a temporary `README.md` for GitHub
4. push the GitHub-facing copy
5. delete the local `README.md`

This keeps the local publish directory minimal while still giving the GitHub repo a human-readable landing page.

## Pre-Publish Checklist

- `SKILL.md` exists and is valid
- public-facing content is in English if the release is intended for a broad audience
- no proprietary project names remain unless the user explicitly wants them public
- no tokens, emails, secret keys, or private paths remain
- the target GitHub repo is correct
- the user understands whether the repo will be public
- version bump and changelog are ready for the ClawHub release

## Sensitive Content Sweep

Look for:

- API keys
- personal email addresses
- private local paths
- unpublished project names
- comments written only for the original author

Search common file types such as:

- `*.md`
- `*.py`
- `*.ipynb`
- config files

## GitHub Workflow

If the user wants GitHub as backup and showcase, prefer a clean GitHub working copy rather than pushing directly from the local publish folder.

Typical steps:

```bash
git clone <repo-url>
# copy updated skill files plus temporary README into the clone
git add -A
git status
git commit -m "Update skill and README"
git push origin main
```

Prefer:

- SSH auth when already configured
- credential manager or browser login over pasting tokens

Use force-push only with explicit user confirmation.

## ClawHub Workflow

Typical checks:

```bash
clawhub whoami
```

Typical publish pattern:

```bash
clawhub publish <skill-dir> \
  --slug <skill-name> \
  --name "<display name>" \
  --version <version> \
  --changelog "<summary>"
```

Publish from the local skill folder before adding a README if the user wants the local folder to remain skill-only.

## README Handling

If the user wants both strict local cleanliness and a better GitHub presentation:

- add `README.md` only after the ClawHub publish succeeds
- push that README to GitHub
- remove the local README after the GitHub push

This is intentional, not redundant.

## Common Problems

### `SKILL.md required`

- confirm you are publishing the correct folder
- confirm the file name is exactly `SKILL.md`

### Push Rejected Because Remote Is Not Empty

- inspect the remote first
- pull and merge only if the remote files are intended to stay
- avoid overwriting remote history blindly

### ClawHub CLI Missing Or Not Logged In

- install the CLI first
- authenticate before retrying publish

### Browser Login Looks Complete But CLI Still Says Not Logged In

- rerun `clawhub login`
- finish the fresh browser flow started by that exact command
- verify with `clawhub whoami`

### GitHub Push Auth Feels Repetitive

- configure SSH once and reuse it
- set a global git `user.name` and `user.email`
- prefer a GitHub `noreply` email if privacy matters

## Safe Wording To Use With Users

Prefer:

- "This will publish the skill to ClawHub first."
- "After that, I can add a temporary README and sync GitHub."
- "I need your confirmation before any force-push."
- "Please complete login in the browser if prompted."

Avoid:

- asking the user to paste secrets into chat by default
- describing history rewrite as harmless
