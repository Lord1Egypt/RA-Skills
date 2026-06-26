# Dev Guide ... Best Practices for AI-Assisted Development

**WIP team members: also read the private Dev Guide at `~/wipcomputerinc/settings/templates/dev-guide-private.md`.** It covers WIP-specific conventions (branch prefixes, agent IDs, deploy paths, incidents) that supplement everything below. Neither guide is complete without the other.

## Repo Structure Convention

Every project follows this split:

### Public Repo
Clean. Code only.
- `README.md` ... what it is, how to use it
- `LICENSE` ... MIT (verified, always)
- `SKILL.md` ... agent skill definition (if applicable)
- `src/` or `core/` ... source code
- `cli/` ... CLI wrapper
- `package.json` / `pyproject.toml` ... package config
- `CHANGELOG.md` ... release notes

**No dev noise.** No todos, no conversations, no internal notes.

### Plans and Dev Notes (per-repo `ai/` folder)

Plans, todos, dev updates, and conversations live in the repo's own `ai/` folder. See the `ai/` folder section under Git Conventions for the full structure.

### Architecture (4-piece pattern)

Every tool follows the dual-interface architecture:
1. **core.ts** ... pure logic, zero framework deps
2. **cli.ts** ... thin wrapper (argv -> core -> stdout)
3. **mcp-server.ts** ... MCP wrapper for agents
4. *(optional)* **plugin wrapper** ... platform-specific integration

CLI is the universal fallback. MCP and plugin wrappers are optimizations.

## Release Process

### Branch, PR, Merge, Publish

```
1. Create feature branch:  git checkout -b <prefix>/<feature>
2. Make changes, commit
3. Write release notes:    RELEASE-NOTES-v{next-version}.md (see below)
4. Push branch:            git push -u origin <prefix>/<feature>
5. Create PR:              gh pr create --title "..." --body "..."
6. Merge PR:               gh pr merge <number> --merge --delete-branch
7. Rename merged branch:   (see Post-Merge Branch Rename below)
8. Pull merged main:       git checkout main && git pull origin main
9. Release:                wip-release patch     (stable: full pipeline)
                           wip-release alpha     (prerelease: npm @alpha, silent)
                           wip-release beta      (prerelease: npm @beta, public notes)
                           wip-release hotfix    (urgent: npm @latest, no deploy-public)
                           # flags: --dry-run (preview), --no-publish (bump + tag only)
```

### Release Tracks

Four release tracks. Choose the right one for the situation:

| Track | Command | npm tag | Public code sync | When to use |
|-------|---------|---------|-----------------|-------------|
| Alpha | `wip-release alpha` | @alpha | No | Internal testing, not ready for users |
| Beta | `wip-release beta` | @beta | No | External testing, release candidate |
| Hotfix | `wip-release hotfix` | @latest | No | Urgent fix, skip deploy-public |
| Stable | `wip-release patch/minor/major` | @latest | Yes | Normal release, full pipeline |

**Alpha** is silent by default. No public release notes, no code sync. Add `--release-notes` to create a prerelease on the public GitHub repo.

**Beta** publishes prerelease notes to the public GitHub repo by default. Add `--no-release-notes` to skip.

**Hotfix** publishes to npm @latest and creates a release on the public GitHub repo, but does NOT run deploy-public (no code sync). Use this when you need a fix in npm immediately but the public repo code can wait for the next stable release.

**Stable** is the existing behavior. Full pipeline: npm @latest, deploy-public (code sync), full release notes.

Version numbering:
- Alpha: `1.9.68-alpha.1`, `1.9.68-alpha.2` (increments on repeat)
- Beta: `1.9.68-beta.1`, `1.9.68-beta.2` (increments on repeat)
- Hotfix: normal patch bump (`1.9.67` -> `1.9.68`)
- Stable: normal bump (patch/minor/major)

Install integration:
```bash
ldm install              # checks @latest (stable + hotfix)
ldm install --beta       # checks @beta
ldm install --alpha      # checks @alpha
```

**Important:**
- **Every change goes through a PR.** No direct pushes to main. Not even "just a README fix." Branch, PR, merge. Every time.
- **Never squash merge.** Every commit has co-authors and tells the story of how something was built. Squashing destroys attribution and history. Always use `--merge` or fast-forward. This applies to `gh pr merge`, manual merges, deploy-public.sh, and any other merge path. No exceptions. Always include `--delete-branch` so the PR branch is cleaned up automatically.
- **Never delete branches.** Branches are history. They tell the story of what was built and when. After merging, rename them (see below). Never `git branch -D` or `git push --delete` without renaming first.
- **Never use `--no-publish` before deploying to public.** `deploy-public.sh` pulls release notes from the private repo's GitHub release. If you skip the release with `--no-publish`, the public repo gets empty notes. Run the full pipeline first.
- After merging, switch back to your dev branch. Don't sit on main.

### Release Notes on the Branch

**Every PR must include a `RELEASE-NOTES-v{next-version}.md` file.** This is how release notes get reviewed before publishing. Same pattern as code review: the notes are on the branch, visible in the PR, reviewed alongside the changes.

**How it works:**

1. Figure out the next version. Current is v0.7.2, this is a patch, so next is v0.7.3.
2. Create `RELEASE-NOTES-v0-7-3.md` in the repo root. **Dashes, not dots** in the filename.
3. Write the summary: what changed, why it matters, what it fixes. Narrative, not a changelog.
4. Commit it with the rest of your changes. It ships with the branch.
5. The PR now shows code changes AND release notes. Both get reviewed.
6. After merge, `wip-release patch` auto-detects the file and uses it as the release summary.
7. After release, `wip-release` moves the file to `ai/_trash/` automatically.

**The file is the summary paragraph.** `wip-release` builds the full structured release (Changes, Fixes, Docs, Files changed, Install, Attribution, Changelog) from git history. Your file provides the human-written context at the top.

**Three-source priority** (first match wins):
1. `--notes-file=path` ... explicit file path via CLI flag
2. `RELEASE-NOTES-v{ver}.md` ... auto-detected from repo root (this is the standard)
3. `ai/dev-updates/` ... today's dev update files (fallback only)

**If no release notes file exists,** `wip-release` falls back to `--notes="..."` or dev updates. But the standard is: write the file, commit it, review it in the PR. Don't skip this.

### Post-Merge Branch Rename

**Never delete branches after merging.** Instead, rename them with `--merged-YYYY-MM-DD` appended. This preserves history and makes it instantly clear which branches are done and when they were merged.

**Format:**
```
<original-branch-name>--merged-YYYY-MM-DD
```

**Examples:**
```
dev/fix-search                  -> dev/fix-search--merged-2026-03-08
agent-a/weekly-tuning           -> agent-a/weekly-tuning--merged-2026-03-08
team-b/add-relay                -> team-b/add-relay--merged-2026-03-08
```

**After merging a PR:**
```bash
# 1. Rename locally
git branch -m <prefix>/<feature> <prefix>/<feature>--merged-$(date +%Y-%m-%d)

# 2. Push renamed branch to remote
git push origin <prefix>/<feature>--merged-$(date +%Y-%m-%d)

# 3. Remove old remote branch name
git push origin --delete <prefix>/<feature>

# 4. Scan for any other merged branches that missed renaming
git branch --merged main | grep -v main | grep -v "\-\-merged\-" | while read branch; do
  echo "WARNING: $branch is merged but not renamed"
done
```

**The scan step is mandatory.** Every time you merge, check for stale branches that missed renaming. If you find any, rename them with the date they were merged (check `git log main` for the merge date, not today's date).

**Automation:** `wip-release` runs this scan automatically as step 10 of the release pipeline. It finds all local branches merged into main that haven't been renamed yet, renames them with the correct merge date, and pushes to remote. You don't have to do anything extra on release.

For repos where you merge but don't release immediately, use the standalone script:
```bash
bash scripts/post-merge-rename.sh            # scan + rename all
bash scripts/post-merge-rename.sh --dry-run   # preview only
bash scripts/post-merge-rename.sh <branch>    # rename specific branch
```
- Use scoped npm tokens for publishing, not personal credentials.

### Release Quality Standards

**Every release must have exhaustive, categorized notes.** People use our software. Sloppy notes are embarrassing. Look at [OpenClaw releases](https://github.com/openclaw/openclaw/releases) as the benchmark.

`wip-release` generates structured notes automatically:

1. **Changes** ... new features, refactors, additions. One bullet per commit with hash.
2. **Fixes** ... bug fixes, hotfixes. One bullet per commit with hash.
3. **Docs** ... README, TECHNICAL, RELAY, any documentation changes.
4. **Files changed** ... diffstat (excludes `ai/` folder).
5. **Install** ... npm install command + git pull.
6. **Attribution** ... Built-by line.
7. **Full changelog** ... GitHub compare URL.

The `--notes` flag provides the summary paragraph at the top. The tool builds everything else from git history.

**For major releases (minor/major bumps):** the auto-generated notes are a starting point. Always review and expand them. Add context, describe architectural changes, explain why things changed. A commit subject like "Add cc-poller.ts" should become a paragraph explaining what the poller does, why it replaces the old hook, and what problem it solves.

**For patch releases:** auto-generated notes are usually sufficient. Review before publishing.

**Never publish a release with just a one-liner.** If two days of work went into it, the release notes should reflect that.

#### Release Checklist

Every release must also have:

1. **All contributors represented.** Every team member (human and AI) must have authored at least one commit in the repo. GitHub tracks contributors by commit author, not co-author trailers. If a contributor is missing, make a real commit with `--author`.
2. **Release on both repos.** The private repo gets the release from wip-release. The public repo gets a matching release from deploy-public.sh. Both must show the release in their GitHub Releases tab.
3. **npm package published.** Available via `npm install <package-name>@<version>`. Verify after publishing.
4. **CHANGELOG.md updated.** wip-release handles this, but verify it's accurate and complete.

**After every release, verify all of these.** Check the public repo's GitHub page. Does it show the release? Does it show all three contributors? Are the release notes complete? Is the npm package available? If any of these are missing, fix it before moving on.

### Release Order (Critical)

The release flow must happen in this exact order:

1. **Merge PR to main** on the private repo
2. **`wip-release`** on the private repo (bumps version, creates tag, creates GitHub release with full notes, publishes npm)
3. **`deploy-public`** to sync to the public repo (pulls release notes from private repo's GitHub release)

If you skip step 2 or do it manually (e.g. `git tag` + `git push` without creating a GitHub release), `deploy-public` will create the public release with empty notes. The script pulls notes from the private repo's GitHub release. No release on private = no notes on public.

### Merge, Deploy, Install ... Three Separate Steps

These are three distinct actions. Never combine them.

| Step | What it means | What happens |
|------|--------------|-------------|
| **Merge** | Development done | PR merged to private repo's main. Code lands. Nothing else changes. |
| **Deploy** | Ship to public | `wip-release` + `deploy-public.sh`. Package published. Available to the world. **Not on your machine yet.** |
| **Install** | Put it on your system | Run the install prompt (`crystal init`, `ldm install`, etc.). Only when the user says "install." |

After Deploy, stop. Do not copy files to extension directories. Do not run `npm install -g`. Do not run `npm link`. The user tests the install flow by running the install prompt. That's how you dogfood.

**If you must release manually** (no root package.json, toolbox repos, etc.):
1. Update CHANGELOG.md and SKILL.md version
2. Commit, PR, merge
3. `git tag vX.Y.Z && git push origin vX.Y.Z`
4. `gh release create vX.Y.Z --title "vX.Y.Z" --notes "..."` on the PRIVATE repo first
5. THEN run `deploy-public`

The GitHub release on the private repo must exist before deploy-public runs. This is not optional.

### Universal Installer Checklist

Every tool must be verified with the Universal Installer before release. This is not optional.

**Before every release:**
```bash
wip-install /path/to/tool --dry-run
```

This shows which interfaces are detected and which are missing.

**Minimum for agent-callable tools:**
- Module (`main` or `exports` in package.json)
- Skill (SKILL.md with YAML frontmatter)
- MCP Server (`mcp-server.mjs` wrapping the core module)

**Full interface coverage (the goal):**
- CLI (`bin` in package.json)
- Module (`main`/`exports`)
- MCP Server (`mcp-server.mjs`)
- OpenClaw Plugin (`openclaw.plugin.json`, only for tools with lifecycle hooks)
- Skill (`SKILL.md`)
- Claude Code Hook (`guard.mjs` or `claudeCode.hook`, only for tools that guard operations)

**For toolbox repos** (repos with multiple tools in `tools/` subfolders): apply this checklist to each sub-tool, not just the root. Every sub-tool gets its own package.json, SKILL.md, and interface files.

**Dogfood rule:** After releasing, run `wip-install` on the toolbox itself to reinstall. Eat your own cooking.

### Pre-Publish Checklist

Before any repo goes public:

1. [ ] Code complete (all punchlist items done)
2. [ ] Code review (architecture, edge cases, quality)
3. [ ] Human review (spec, UX, direction)
4. [ ] LICENSE file present (MIT, verified)
5. [ ] README covers usage, installation, examples
6. [ ] CHANGELOG started
7. [ ] npm package published (scoped)
8. [ ] GitHub release created with tag
9. [ ] License compliance ledger initialized for all dependencies

## Cloudflare Workers Deploy

Some repos deploy to Cloudflare Workers via `wrangler deploy`. Same rules as git: **never deploy uncommitted code.**

### The Rule

**Commit first. Deploy second. Always.** The source that produced the deployed worker must exist in git before it goes to Cloudflare. If something breaks, we need to know exactly what's running.

### Deploy Workflow

```
1. Write code on feature branch
2. Build:                npm run build:demo (or whatever the build script is)
3. Test locally:         npm run dev:demo (wrangler dev)
4. Commit source:        git add src/worker-*.ts wrangler-*.toml && git commit
5. Push + PR + merge:    normal PR flow
6. Deploy:               npm run deploy:demo (wrangler deploy)
```

**Steps 4-5 happen BEFORE step 6.** Not after. Not "I'll commit later." The deploy command should never run on uncommitted code.

### Deploy Guard

Every repo with a `wrangler*.toml` should use guarded deploy scripts in package.json:

```json
"deploy:demo": "bash -c 'git diff --quiet HEAD -- src/ wrangler-demo.toml || (echo \"ERROR: uncommitted changes. commit before deploying.\" && exit 1)' && wrangler deploy --config wrangler-demo.toml"
```

This checks that all source files are committed before `wrangler deploy` runs. If anything is dirty, it refuses.

### What Gets Tracked

The deployed worker is the compiled output of committed source. The chain is:

```
source (git) -> build (tsup) -> dist/*.js -> wrangler deploy -> Cloudflare edge
```

We track the source. The build is reproducible from source. The deploy is reproducible from the build. If we have the git commit, we can reconstruct exactly what's running.

## License Compliance

Use `wip-license-hook` for license rug-pull detection:
- Pre-pull hook: blocks upstream merges if license changed
- Pre-push hook: alerts if upstream has drifted
- LICENSE snapshots archived at adoption
- Daily cron scan of all dependencies
- Dashboard published for public verification

**Rule: never merge upstream if license changed. Hard stop.**

## Git Conventions

### Never Work on Main

**Main is for merged, released code only.** Never make changes directly on main. Every repo should have a dev branch checked out as the working branch at all times.

When you clone a repo or finish a PR, immediately create or switch to a dev branch:

```bash
git checkout -b <prefix>/dev           # new repo, first time
git checkout <prefix>/<feature>        # existing feature work
```

If you find yourself on main with uncommitted changes, stash, branch, and apply:

```bash
git stash
git checkout -b <prefix>/fix-name
git stash pop
```

### Branch Prefixes

Branch names use the **harness name** (agent + machine) as the prefix. Every harness is a distinct entity. Claude Code on the Mini is not the same as Claude Code on the Air.

```
<harness>/<feature>
```

Examples: `dev/fix-search`, `agent-a/add-relay`, `team-b/weekly-tuning`

### Multi-Agent Clone Workflow

**Every harness gets their own clone of every repo.** This prevents checkout collisions when multiple agents work on the same repo at the same time.

```
staff/
  Agent-A/
    repos/
      my-project-private/         <- agent-a works here, agent-a/ branches
  Agent-B/
    repos/
      my-project-private/         <- agent-b works here, agent-b/ branches
  Human/
    repos/
      my-project-private/         <- human works here, dev/ branches
```

**Rules:**
- Never work in another agent's folder. If Agent-A originated a repo, Agent-B still clones it to their own folder.
- Each harness uses their own branch prefix.
- PRs merge to `main` on GitHub. That's the shared integration point.
- If something needs to change in another agent's working tree, open a PR or ask them.

**When a new repo is created:**
1. Whoever creates it pushes to GitHub
2. Every other agent clones it to their own repos folder
3. Each agent creates their dev branch with their prefix

This is how we avoid the "two agents have different branches checked out in the same folder" problem. It doesn't work. Separate folders, separate clones, shared remote.

### Commit Messages

- Imperative mood, concise (`add: license scanner`, `fix: offline detection`)
- Co-author trailers for all contributors on every commit
- PRs for cross-agent edits: don't edit another agent's working tree directly
- Never push directly to main. Always branch, PR, merge. No exceptions.

### File Naming Convention

All files authored by an agent use this format:

```
YYYY-MM-DD--HH-MM-SS--{agent}--{description}.md
```

Single dashes within date and time. Double dashes between segments. 24-hour clock.

This applies to dev updates, plans, todos, notes, session exports, daily logs ... everything with an author and a timestamp.

### Daily Logs

Each entry is its own file, not appended to a shared file.

```
agents/{agent-id}/memory/daily/
  2026-02-27--17-45-30--agent-a--feature-deploy.md
  2026-02-27--19-12-00--agent-a--config-migration.md
```

One file per entry. Full timestamp. Agent ID in the name. Nothing gets overwritten or collided.

### The `ai/` Folder (per-repo standard)

Every repo gets an `ai/` folder. It holds all the thinking between humans and agents ... plans, dev updates, todos, conversations, notes. Scoped to the repo it belongs to.

```
ai/
  plan/              ... architecture plans, roadmaps, convention notes
  dev-updates/       ... what was built, session logs
  todos/
    Human-todo.md    ... human lead's action items
    Agent-A-todo.md  ... Agent A's action items
    Agent-B-todo.md  ... Agent B's action items
  notes/             ... research, raw conversation logs, references
```

### Todo Files

One file per person/agent. Named `{Name}-todo.md`. Lives in `ai/todos/`.

**Three sections, always in this order:**

```markdown
# {Name} ... {Project} To-Do

**Updated:** YYYY-MM-DD

---

## To Do
- [ ] Thing that needs doing
- [ ] Another thing

---

## Done
- [x] Thing that was completed ... YYYY-MM-DD

---

## Deprecated
- ~~Thing that's no longer needed~~ ... reason. (YYYY-MM-DD)
```

**Rules:**
- **Never delete anything.** Items move between sections, never off the page.
- **To Do** ... work that needs to happen.
- **Done** ... work that was completed. Check the box, add the date.
- **Deprecated** ... work that was planned but is no longer needed (code changed, approach changed, requirement dropped). Strikethrough the text, add the reason and date. This is NOT the same as Done. Deprecated means "we decided not to do this."
- **Update the date** at the top of the file every time you edit it.
- Each person/agent has exactly one file. Don't create per-date or per-feature todo files.

**Example todo files:**

| File | Who |
|------|-----|
| `Human-todo.md` | Human lead (setup, deploy, review) |
| `Agent-A-todo.md` | Agent A (code, docs, builds) |
| `Agent-B-todo.md` | Agent B (testing, integration) |

Add more as agents or team members are added.

### GitHub Issues

**Use GitHub Issues for actionable bugs, feature requests, and tasks.** The `ai/todos/` files are for rough planning and brainstorming. Once something becomes a concrete action item, it goes on GitHub.

**Why both?** Todos are quick, local, and low-friction. Issues are trackable, cross-referenceable, and visible to all agents and humans. Todos are where you think. Issues are where you commit to doing.

#### Filing Convention

Every issue filed by an agent must include:

1. **Attribution line** at the top of the body:
   ```
   > Filed by: <agent-name> (<agent-id>) on <YYYY-MM-DD>
   ```

2. **`filed-by` label** identifying the author:
   ```
   filed-by:<agent-id>
   ```
   This makes issues filterable by who created them. Create these labels per-agent on every repo in the org.

3. **Clear problem/solution structure.** State what's wrong, then what should change.

#### When to use issues vs todos

| Use | When |
|-----|------|
| GitHub Issue | Bug, feature request, task with a clear definition of done |
| `ai/todos/` | Brainstorming, rough planning, "we should think about..." |
| Both | Start in todos, promote to issue when it's concrete |

#### Public vs Private Issues

For repos following the public/private pattern:

- **Public repo issues** are for users. Someone installs your tool, finds a bug, files an issue on the public repo. Triage and respond there.
- **Private repo issues** are for the team. Internal work, architecture decisions, agent coordination.

**When a public issue needs internal work:**
1. Respond on the public issue ("Looking into this")
2. Open a private issue with the full context, link back (`Public: org/repo#42`)
3. Fix in private, release, deploy to public
4. Close the public issue with the version (`Fixed in v0.5.0`)

**When you find a bug internally:**
1. File on the private repo
2. Fix, release, deploy
3. No public issue needed unless it's worth announcing

The release is what connects public and private. No issue syncing, no mirroring. Public issues are the front door. Private issues are the workshop.

#### Agent ID Convention

Agents are identified by a structured ID that encodes platform, name, and machine:

```
[platform]-[agent]-[machine]
```

Examples: `oc-lesa-mini` (OpenClaw, Lesa, on mini), `cc-mini` (Claude Code, on mini), `cc-air` (Claude Code, on air).

This ID is used in:
- GitHub issue labels (`filed-by:*`)
- Memory systems (agent_id field)
- LDM agent config (`~/.ldm/agents/<id>/config.json`)
- Git branch prefixes

## Branch Protection

All repos should have branch protection on `main` with `enforce_admins=true`. This means:
- No direct pushes to main (even for admins)
- All changes go through PRs

**To add protection:**
```bash
gh api "repos/<org>/<repo>/branches/main/protection" -X PUT \
  -F "required_pull_request_reviews[required_approving_review_count]=0" \
  -F "enforce_admins=true" \
  -F "restrictions=null" \
  -F "required_status_checks=null"
```

## Worktree Workflow

**Every session starts in a worktree. No one works directly in the main working tree.**

The main working tree stays on `main` and is read-only in practice. All development happens in git worktrees. This keeps the primary clone clean, prevents accidental commits to main, and enables parallel work within a single agent.

### Worktree Location Convention

**All worktrees go in `.worktrees/` as a sibling to the repos directory.** Never create worktrees as siblings to repos directly. They look like real repos, confuse iCloud sync, and are hard to find/clean.

**Convention:** `.worktrees/<repo-name>--<branch-suffix>/`

```
repos/
  ldm-os/
    components/
      memory-crystal-private/     <- real repo
    devops/
      wip-ai-devops-toolbox-private/  <- real repo
  .worktrees/
    memory-crystal-private--cc-mini--fix-search/   <- worktree
    wip-ai-devops-toolbox-private--cc-mini--guard/  <- worktree
```

### Starting a Worktree

**Preferred:** Use the `ldm worktree` command:
```bash
ldm worktree add cc-mini/fix-bug    # auto-detects repo, creates in .worktrees/
```

**From Claude Code:**
```bash
claude --worktree <name>
```

**Manual:**
```bash
git worktree add ../.worktrees/<repo>--<branch> -b <branch>
```

The branch guard warns if you create worktrees outside `.worktrees/` or `.claude/worktrees/`.

### Branch Naming

Worktree branches follow the same prefix convention as regular branches:

```
<harness>/<feature>
```

Examples: `cc-mini/fix-search`, `lesa-mini/add-relay`, `cc-air/weekly-tuning`

The worktree name and the branch name don't have to match, but the branch must use your harness prefix.

### Subagents and Parallel Work

Subagents use `isolation: "worktree"` for parallel tasks. Each subagent gets its own worktree, its own branch, and can commit independently without interfering with the parent session or other subagents.

This is the safe way to do parallel work within a single agent. Repos-per-agent solves cross-agent isolation. Worktrees solve within-agent parallelism.

### Commit Before Session Ends

**Always commit and push before a session ends.** Worktree cleanup deletes the entire worktree directory, including any uncommitted work. If it's not committed and pushed, it's gone.

```bash
git add <files>
git commit -m "description"
git push -u origin <prefix>/<feature>
```

### Release from the Main Working Tree

**`wip-release` must run from the main working tree, not a worktree.** The release pipeline expects to be on `main` in the primary clone. After merging your PR, switch to the main working tree to run the release:

```bash
cd /path/to/repo          # the main working tree, not .claude/worktrees/...
git checkout main && git pull
wip-release patch --notes="description"
```

### Gitignore

**`.claude/worktrees/` must be in `.gitignore`.** Worktrees are local, ephemeral, and per-machine. They should never be committed.

```
# .gitignore
.claude/worktrees/
```

Add this to every repo that uses worktrees.

## Review Flow

```
Agent builds -> pushes to dev branch
  -> Code review (another agent or human)
  -> Human reviews (direction, spec)
  -> merge to main
  -> publish (npm, GitHub, skill registry)
```

## PR Checklist (Private Repos)

Every PR to a private repo must include product doc updates. This is not optional. Do it before merging, not after.

### Required on every PR:

1. **Dev update.** Write a dev update in `ai/dev-updates/` documenting what changed, key decisions, and what's next. Format: `YYYY-MM-DD--HH-MM--agent--description.md`.

2. **Roadmap update.** Review `ai/product/plans-prds/roadmap.md`:
   - Move completed items from **Upcoming** to **Done** (with `[x]` checkboxes)
   - Add new items to **Upcoming** if the work revealed them
   - Move abandoned items to **Deprecated** (never delete)

3. **readme-first update.** Review `ai/product/readme-first.md`:
   - Update **What's Built** and **What's Missing** sections
   - Update any stats, counts, or version references
   - Update the **Databases** or architecture sections if they changed

4. **Plan archival.** If a plan in `plans-prds/current/` is complete, move it to `plans-prds/archive-complete/`.

### Why this matters:

Product docs drift fast. If roadmap updates only happen "when someone remembers," the roadmap becomes fiction. Tying updates to PRs means the docs stay current by default, not by heroics.

### Release notes:

Release notes are the public face of the project. They must be comprehensive. One-liners like "Release v0.6.0" are unacceptable. Every feature, every change, documented section by section. This applies to both private and public GitHub releases.

## Feature Planning: 5 Mandatory Questions

Before implementing any feature that changes how the system works (installer, config, deploy, architecture), answer these 5 questions in your plan or PR description. Not optional. Not "consider this." Answer all five or the plan is incomplete.

1. **What source files change?** (in the repo)
2. **What does `ldm install` deploy?** (templates, rules, docs, boot config, CLAUDE.md, skills)
3. **What needs to update for fresh install vs existing install?**
4. **What docs need updating?** (repo docs, settings/docs, website)
5. **What are ALL the files the installer touches on deploy?**

If you can't answer #5, you don't understand the change well enough to ship it.

## Doc Update Dependencies

When you change a file on the left, you MUST also update the files on the right. This is not optional.

| If you change | You must also update |
|--------------|---------------------|
| `SKILL.md` | `references/`, `settings/docs/how-install-works.md`, wip.computer/install/ (auto via wip-release) |
| `lib/deploy.mjs` | `settings/docs/how-install-works.md`, `docs/universal-installer/SPEC.md`, `docs/universal-installer/TECHNICAL.md` |
| `catalog.json` | `settings/docs/what-is-ldm-os.md`, `README.md`, `docs/skills/README.md` |
| `bin/ldm.js` (init) | `settings/docs/how-install-works.md`, `settings/docs/system-directories.md` |
| `shared/rules/*` | `settings/docs/how-rules-and-commands-work.md` |
| `shared/boot/*` | `settings/docs/how-agents-work.md` |
| `lib/detect.mjs` | `docs/universal-installer/SPEC.md`, `settings/docs/how-install-works.md` |
| Backup scripts | `settings/docs/how-backup-works.md` |
| Agent identity files | `settings/docs/how-agents-work.md` |
| Any repo `README.md` | Public repo README (via deploy-public.sh) |

Machine-readable version: `~/wipcomputerinc/settings/docs/change-dependencies.json`

### Three doc layers

Every change flows through three layers:

1. **Repo docs** (generic, source of truth): README.md, TECHNICAL.md, SPEC.md per repo. Written for anyone.
2. **Settings docs** (personalized, deployed by ldm install): `~/wipcomputerinc/settings/docs/`. Written for YOUR system. Personalized from config.json.
3. **Website docs** (public): wip.computer. SKILL.md auto-deployed by wip-release. Other docs via Mintlify or deploy script.

If repo docs change but settings docs don't update, the user's local docs drift. If settings docs change but the website doesn't, the public docs drift. All three layers must stay in sync.

## Repo Directory Structure

### The Standard Layout

All repos are organized into this directory structure. Every agent on every machine must follow this layout. The folders are organizational categories, not monorepos. Each repo inside is its own independent git repo.

```
repos/
├── <project>/                   ← NOT a repo. Organizes project repos by category.
│   ├── apis/                    ← API integrations
│   ├── apps/                    ← user-facing apps
│   ├── components/              ← core components
│   ├── operations/              ← dev tools, release pipeline
│   └── utilities/               ← support tools
├── <company>/                   ← Repo. Company docs (always private).
├── third-party-repos/           ← NOT a repo. Forks and external repos.
├── _sort/                       ← NOT a repo. Repos not yet categorized.
├── _sunsetted/                  ← NOT a repo. Deprecated repos.
└── _trash/                      ← NOT a repo. Deleted repos.
```

### Staging Folder Conventions

- **`_to-privatize/`** ... repos staged for privatization
- **`_sort/`** ... repos that need to be categorized or figured out
- **`_trash/`** ... deleted items (never truly delete, move here)
- **Underscore prefix** (`_`) keeps staging folders sorted to the top, visually separated from real repos

These conventions apply at every level: top-level `repos/`, inside project categories, and nested within staging folders.

### Creating a New Repo

**Always create repos as `-private` from day one.** Do not create a repo and privatize it later. Start with the right name and structure.

```bash
# 1. Pick the category
#    apis, apps, components, operations, utilities

# 2. Create on GitHub as private with -private suffix
gh repo create <org>/<name>-private --private

# 3. Clone into the correct category folder
cd repos/<project>/<category>/
git clone git@github.com:<org>/<name>-private.git

# 4. Create the ai/ folder structure
cd <name>-private
mkdir -p ai/product/plans-prds/{upcoming,current,archive-complete}
mkdir -p ai/product/plans-prds/todos
mkdir -p ai/product/product-ideas
mkdir -p ai/product/notes/research
mkdir -p ai/dev-updates

# 5. Create your dev branch
git checkout -b <prefix>/dev
```

**Never create a repo without picking its category first.** If you don't know where it goes, put it in `_sort/` and figure it out before starting work.

### The Manifest

`repos/repos-manifest.json` is the source of truth for where every repo lives. It maps local paths to GitHub remotes. When a repo is created, moved, or renamed, update the manifest.

Every agent can use the manifest to sync their local directory structure. The goal: every agent on every machine has the same layout.

### Privatize Before You Work

**Do not start any work on a non-privatized repo.** If a repo is in `_to-privatize` and you need to work on it, run it through the privatization process first:

1. Rename the GitHub repo to `<name>-private`
2. Update the local remote URL (`git remote set-url origin ...`)
3. Rename the local folder to match
4. Then start your work

Working on a non-privatized repo means your `ai/` content (plans, todos, dev updates) gets committed to a repo that could accidentally go public. No exceptions.

---

## Public/Private Repo Pattern

### The Rule

**Never make a repo public unless it has a `-private` counterpart with all `ai/` content separated out.** If a repo doesn't have a `-private` counterpart yet, it stays private until one is created. No exceptions. Violating this exposes internal plans, todos, and development context.

**The private repo is the working repo. The public repo is everything except `ai/`.**

**You only need the private repo locally.** Clone `<name>-private`, work in it, release from it, deploy to public from it. Never clone the public repo for development. The public repo is a deployment target, not a working tree. The deploy script handles syncing.

Every repo has an `ai/` folder where agents and humans collaborate ... plans, todos, dev updates, notes, conversations. This is the development process. It doesn't ship publicly.

The private repo tracks everything, including `ai/`. The public repo is the same codebase without `ai/`. Two repos, same code, clean boundary.

```
<name>-private/      <- working repo (clone this one, work here)
  src/, README.md, LICENSE, package.json, SKILL.md ...
  ai/                <- plans, todos, notes, dev updates
    plan/
    todos/
    dev-updates/
    notes/

<name>/              <- public repo (deploy target only, never clone for dev)
  src/, README.md, LICENSE, package.json, SKILL.md ...
  (no ai/ folder)
```

### Why

The `ai/` folder contains personal notes, half-formed ideas, internal debates, agent inboxes. Useful for the team. Irrelevant to users. Can be taken out of context. Should not be public.

The public repo has everything an LLM or human needs to understand and use the project: README, code, docs, SKILL.md, LICENSE. The `ai/` folder is operational context, not conceptual context.

### Workflow

1. All work happens in the private repo
2. Merge PR to main on the private repo
3. Run `wip-release` on the private repo (version bump, changelog, npm publish, GitHub release)
4. Deploy to public repo (everything except `ai/`)

**The order matters.** Release first, then deploy. The public repo should always reflect a released version with correct version numbers, changelog, and SKILL.md.

```bash
# Step 1-2: normal PR flow on private repo
cd /path/to/private-repo
git checkout main && git pull origin main

# Step 3: release (MUST create GitHub release for deploy-public.sh to pull notes)
wip-release patch --notes="description of changes"

# Step 4: deploy to public (code sync + release)
bash deploy-public.sh /path/to/private-repo <org>/<public-repo>
```

**Never use `--no-publish` before deploying to public.** The `deploy-public.sh` script pulls release notes from the private repo's GitHub release. If the GitHub release doesn't exist (because `--no-publish` skipped it), the public release gets empty notes. Always run the full `wip-release` pipeline before `deploy-public.sh`.

The deploy script:
1. Clones the public repo
2. Rsyncs everything except `ai/` and `.git/`
3. Creates a branch, commits, opens a PR, merges it
4. Creates a matching GitHub release on the public repo (pulls notes from the private repo's release)

**After deploy, the public repo should show:**
- Updated code (matching private minus `ai/`)
- A GitHub release with the version tag and release notes
- npm package available via `npm install <package-name>`

**What goes where:**

| Artifact | Where it lives |
|----------|---------------|
| npm package | Public npm registry (anyone can install) |
| GitHub release (private) | `<name>-private` repo (internal reference) |
| GitHub release (public) | `<name>` repo (what users see) |
| GitHub Packages | Not used (npm registry is the source of truth) |

### Config-specific splits

Some repos also have deployment config that shouldn't be public (real paths, contacts, secrets references). Same pattern applies ... the private repo has `config.json`, the public repo has `config.example.json`.

**Key rule:** never put real paths, contacts, personal notes, or deployment values in the public repo.

## Scheduled Automation (.app Pattern)

macOS restricts cron and shell scripts from accessing protected files (Full Disk Access). The workaround: wrap automation in a native `.app` bundle and grant FDA to the app.

### How it works

A minimal macOS `.app` bundle that:
1. Contains a compiled Mach-O binary (so macOS recognizes it as a real app)
2. The binary calls a shell script that dispatches to individual job scripts
3. Jobs live in `YourApp.app/Contents/Resources/jobs/*.sh`
4. Adding a new job = dropping a new `.sh` file in that folder

### Structure

```
~/Applications/YourDevTools.app/
  Contents/
    Info.plist                    ... app metadata (bundle ID, version)
    MacOS/
      your-dev-tools              ... compiled binary (Mach-O, calls dispatcher)
      your-dev-tools-run          ... shell dispatcher (routes to jobs)
    Resources/
      jobs/
        backup.sh                 ... daily backup of databases + state
        branch-protect.sh         ... audit + enforce branch protection across org
        visibility-audit.sh       ... audit public repos for missing -private counterparts
```

### Setup

1. Build the app (or copy from dev-tools repo)
2. Drag the `.app` into **System Settings > Privacy & Security > Full Disk Access**
3. Schedule via cron:

```bash
0 0 * * * open -W ~/Applications/YourDevTools.app --args backup >> /tmp/dev-tools/cron.log 2>&1
0 1 * * * open -W ~/Applications/YourDevTools.app --args branch-protect >> /tmp/dev-tools/cron.log 2>&1
```

### Why not LaunchAgents?

LaunchAgents have been unreliable across macOS updates. FDA grants to `/bin/bash` and `cron` don't persist. The `.app` bundle is the one thing macOS consistently respects for FDA permissions.

### Adding a new job

Create a file in `Contents/Resources/jobs/`:

```bash
# ~/Applications/YourDevTools.app/Contents/Resources/jobs/my-job.sh
#!/bin/bash
echo "=== My job: $(date) ==="
# ... your automation here
echo "=== Done ==="
```

Then: `open -W ~/Applications/YourDevTools.app --args my-job`

### Logs

All job output goes to `/tmp/dev-tools/`:
- `dev-tools.log` ... dispatcher log (which jobs ran, exit codes)
- `<job-name>.log` ... individual job output
- `<job-name>-last-exit` ... last exit code (for monitoring)
- `<job-name>-last-run` ... last run timestamp

## The _trash Convention

**Never delete files. Move them to `_trash/`.** Every directory that might have discarded files should have a `_trash/` subfolder.

### Why:

- Space is cheap. Recovery from `_trash/` is instant. Recovery from git history requires knowing the commit, the path, and the exact filename.
- Files in `_trash/` are visible. You can browse them, grep them, copy them back. Deleted files are invisible unless you know they existed.
- It prevents the "wait, who deleted that?" conversation.

### Where it applies:

- **Repos:** `ai/product/plans-prds/_trash/`, `ai/product/product-ideas/_trash/`, etc.
- **Agent data:** workspace files, config backups, old extension versions
- **Extension installs:** old plugin versions before upgrade

### How:

```bash
# Instead of this:
rm old-file.md

# Do this:
mkdir -p _trash
mv old-file.md _trash/
```

Use `git mv` if the file is tracked. The underscore prefix sorts `_trash/` to the top of directory listings so it stays visible but out of the way.

### When to clean up:

Rarely. Maybe annually. If `_trash/` gets huge, archive it. But the default is: leave it. The cost of keeping files around is near zero. The cost of needing a file you deleted is real.
