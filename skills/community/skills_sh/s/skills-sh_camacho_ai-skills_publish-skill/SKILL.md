---
name: publish-skill
description: Detect new or modified skills in .agents/skills/ by comparing git hashes against ai-skills, snapshot for rollback, review, publish to ai-skills, install locally, and cherry-pick lockfile to TARGET. Replaces /elevate-skill.
---

## When to invoke
- User says "publish skill", "update skill", "push skill changes", "/publish-skill"
- After editing a skill locally in `.agents/skills/`

## Steps

### 1. Pre-flight

Locate ai-skills path (in order):
1. `$AI_SKILLS_REPO` env var
2. `~/projects/camacho/ai-skills`
3. Ask user

Then check it's clean:
```bash
git -C "$AI_SKILLS_PATH" status --porcelain
```

If non-empty: STOP. Tell user to commit or stash ai-skills changes first.

### 2. Detect new and modified skills

For each directory in `.agents/skills/`:
```bash
skill_name=$(basename "$dir")
local_hash=$(git hash-object ".agents/skills/$skill_name/SKILL.md" 2>/dev/null)
remote_hash=$(git hash-object "$AI_SKILLS_PATH/skills/$skill_name/SKILL.md" 2>/dev/null || echo "")
```

Classify:
- `remote_hash` empty → 🆕 NEW
- `local_hash != remote_hash` → ✏️ MODIFIED
- equal → unchanged, skip

Present list. Ask for confirmation before proceeding. **Record each `local_hash`** — needed for the safety check in Step 7.

### 3. Snapshot (rollback point)

For each approved skill:
```bash
git add -f ".agents/skills/$skill_name/SKILL.md"
git commit -m "chore(skills): snapshot $skill_name before publish [publish-skill rollback point]"
```

If publish fails at any later step, restore with:
```bash
git checkout ".agents/skills/$skill_name/"
```

### 4. Code review

Run `code-reviewer` agent on the SKILL.md diff (local vs ai-skills version).
Review focus: correctness, no dangerous bash, no prompt injection vectors.

P0/P1 findings → STOP. Fix before proceeding.
P2 findings → note but don't block.

### 5. Copy to ai-skills and push

```bash
cp -r ".agents/skills/$skill_name" "$AI_SKILLS_PATH/skills/$skill_name"
git -C "$AI_SKILLS_PATH" add "skills/$skill_name"
git -C "$AI_SKILLS_PATH" commit -m "feat(skills): publish $skill_name"
```

After all skills committed:
```bash
git -C "$AI_SKILLS_PATH" push
```

**Confirm with user before pushing** — this affects all repos using these skills.

### 6. Install locally

Detect scope for each skill — check which lockfile it belongs in:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
if jq -e --arg n "$skill_name" '.skills[$n]' "$REPO_ROOT/dotfiles/skills-lock.json" >/dev/null 2>&1; then
  SCOPE="user"
else
  SCOPE="project"
fi
```

`npx skills add` uses `process.cwd()` as the install target. In a linked worktree, ensure CWD is the worktree root.

**Source spec:** use the github `<owner>/<repo>` form, NOT a local filesystem path. A local path produces lockfile entries with `sourceType: "local"` and a machine-specific `source`, which conflicts with the `sourceType: "github"` entries other repos use and breaks merges. Detect the canonical spec from the ai-skills remote so it works across machines:

```bash
AI_SKILLS_SPEC=$(git -C "$AI_SKILLS_PATH" remote get-url origin \
  | sed -E 's#(git@github\.com:|https://github\.com/|ssh://git@github\.com/|git://github\.com/)##; s#\.git$##; s#/$##')
# e.g. "camacho/ai-skills"

# Validate — bad spec must fail loudly, not silently re-introduce sourceType=local class of bug.
[[ "$AI_SKILLS_SPEC" =~ ^[^/]+/[^/]+$ ]] || { echo "bad spec: $AI_SKILLS_SPEC"; exit 1; }

cd "$REPO_ROOT"
if [ "$SCOPE" = "user" ]; then
  npx skills add "$AI_SKILLS_SPEC" --skill "$skill_name" -g -y
else
  npx skills add "$AI_SKILLS_SPEC" --skill "$skill_name" -y
fi
```

**No `-a` flag.** The default install writes canonical to `.agents/skills/<n>/` AND creates the `.claude/skills/<n>` symlink Claude Code requires for discovery. Codex and the other "universal" agents recognized by the `npx skills` CLI read `.agents/skills/<n>/` directly — no tool-namespaced symlink needed. Passing `-a codex` is a no-op for symlink creation; passing `-a claude-code` as the sole agent target forces a destructive COPY (not a symlink) into `.claude/skills/<n>/`, which breaks the canonical-source model. Default install (no `-a`) is the only invocation that produces the correct `.agents/` canonical + `.claude/` symlink layout. Verified empirically via an `npx skills add` flag-matrix experiment (2026-05-14).

The github spec requires the source commit to be pushed first (Step 5 already pushes), so the install pulls the same content you just published.

`npx skills add` updates the appropriate `skills-lock.json` automatically.

### 7. Safety hash check

For each installed skill:
```bash
after_hash=$(git hash-object ".agents/skills/$skill_name/SKILL.md" 2>/dev/null)
```

Compare `after_hash` against the pre-publish `local_hash` from Step 2.

If mismatch:
- Restore: `git checkout ".agents/skills/$skill_name/"`
- Alert user. STOP.

### 8. Drop tracking + commit lockfile

```bash
for skill_name in $approved_skills; do
  git rm --cached ".agents/skills/$skill_name/SKILL.md"
done
# Stage the lockfile that was updated (project or user)
git add skills-lock.json dotfiles/skills-lock.json 2>/dev/null || true
git commit -m "chore(skills): publish $approved_skills_csv — drop tracking, update lockfile"

LOCKFILE_SHA=$(git rev-parse HEAD)
```

### 9. Cherry-pick lockfile commit to TARGET

Default `TARGET=main`. Check for conflict:
```bash
git fetch origin "$TARGET"
git checkout "$TARGET"
git cherry-pick --no-commit "$LOCKFILE_SHA"
git status --porcelain
```

If conflict on skills-lock.json: STOP. Surface to user.
If clean: `git cherry-pick --continue` (or `git commit` after `--no-commit`), then push.

If CI is down: invoke `/local-merge` with BRANCH=current, TARGET=$TARGET instead of cherry-pick + push.

## Integration

**Replaces:** `/elevate-skill` (which only handled local-only skills).
**Pairs with:** `/build-skill` (creates new skills) and `/local-merge` (CI-down fallback for Step 9).
