---
name: clawhub-publish
description: |
  Publishes a skill to ClawhHub — the Claude skills marketplace. Use this skill whenever
  the user wants to publish, release, or push a new version of a skill to clawhub.

  Trigger on any of these:
  - "发布skill", "发布到clawhub", "发布新版本", "上传skill", "推送skill"
  - "publish skill", "clawhub publish", "release skill", "push skill to clawhub"
  - "skill 发布", "把这个skill发布出去"
  - User mentions bumping a version and publishing

  Even if the user just says "发布" or "publish" in the context of a skill or a
  ~/.claude/skills/ folder, this skill should trigger.
---

# ClawhHub Skill Publisher

You help users publish (or update) a skill on ClawhHub using the `clawhub publish` CLI.

## Workflow (follow in order)

### Step 1 — Identify the skill folder

Check if the user already specified a path or skill name. If not, list available skills:

```bash
ls ~/.claude/skills/
```

If there's only one skill, use it directly. If there are multiple, ask the user which one to publish.

The skill folder path is typically `~/.claude/skills/<slug>/`.

### Step 2 — Read the skill's metadata

Read `SKILL.md` from the skill folder to extract:
- `name` field from frontmatter → use as `--name`
- The slug is the folder name (unless the user says otherwise)

Also check if there's a `version` field in the frontmatter (some skills track it there).

### Step 3 — Check current published version

Run:
```bash
clawhub inspect <slug> 2>&1
```

Look for the `Latest:` line (e.g. `Latest: 1.0.2`). If the skill has never been published, start at `1.0.0`.

If `clawhub inspect` returns an error like "not found", treat current version as `0.0.0` and suggest `1.0.0` as the first release.

### Step 4 — Suggest a version bump

Show the user the current version and suggest the next **patch** version by default (most releases are patches). Also offer minor and major:

```
当前版本：1.0.2
建议版本：
  1. 1.0.3（patch — 修复bug、优化提示词）← 推荐
  2. 1.1.0（minor — 新增功能或较大改动）
  3. 2.0.0（major — 破坏性变更或完全重写）

请选择版本号，或直接输入自定义版本：
```

Wait for the user to confirm or specify a version.

### Step 5 — Get changelog

Ask what changed in this version:
```
这次版本更新了什么？（将作为 changelog 写入发布记录）
```

Keep it brief — one sentence is fine. If the user says "skip" or similar, use a generic message like "Minor updates".

### Step 6 — Confirm and publish

Show a summary before running:
```
📦 即将发布：
  Skill：<folder-path>
  Slug：<slug>
  名称：<name>
  版本：<version>
  Changelog：<changelog>
  Tags：latest

确认发布吗？
```

After confirmation, run:
```bash
clawhub publish <folder-path> \
  --slug <slug> \
  --name "<name>" \
  --version <version> \
  --changelog "<changelog>" \
  --tags latest
```

### Step 7 — Report result

On success, the output contains: `✔ OK. Published <slug>@<version> (<id>)`

Report back clearly:
```
✅ 发布成功！
  <slug>@<version>
  ID：<id>
```

If it fails, show the error message and suggest common fixes:
- Version already exists → bump the version
- Not logged in → run `clawhub login`
- Slug mismatch → verify the slug matches what was previously published

## Optional: Update version in SKILL.md

After a successful publish, offer to update the `version` field in SKILL.md frontmatter (so future publishes can auto-detect it):

```
是否将版本号 <version> 写入 SKILL.md frontmatter？（方便下次自动识别当前版本）
```

If the user agrees, add or update `version: <version>` in the YAML frontmatter of SKILL.md.

## Key CLI reference

```
clawhub publish <path>
  --slug <slug>        # Unique skill identifier (required)
  --name <name>        # Display name shown on clawhub.com
  --version <version>  # Semver (required, must be higher than current)
  --changelog <text>   # Release notes for this version
  --tags <tags>        # Comma-separated, default "latest"

clawhub whoami         # Show logged-in user
clawhub inspect <slug> # Show published skill info including latest version
clawhub sync           # Auto-scan and publish all local skills with changes
```
