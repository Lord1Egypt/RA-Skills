# Publish Procedures Reference

Complete procedures for publishing to GitHub and ClawHub, including API details, fallback methods, and troubleshooting.

**When to read**: When entering Phase 3 (push and publish). Read this file in full before executing any publish commands.

---

## GitHub Publishing

### Push Fallback Chain

```
git push（优先，最快）
  → 失败 → gh CLI（次优，自动认证）
  → 失败 → REST API 逐文件上传（最后手段，最慢）
```

### Method A: git push (preferred)

```bash
# Initialize (first time)
cd <skill-dir>
git init
git config user.name "<author>"
git config user.email "<author>@users.noreply.github.com"
git add .
git commit -m "feat: initial release vX.Y.Z"
git remote add origin https://github.com/<owner>/<repo>.git
git branch -M main
git push -u origin main
```

**Git config notes**:
- Use repo-level config (`git config` without `--global`) to avoid polluting global settings
- Use `@users.noreply.github.com` email to protect privacy
- Author name from user confirmation

### Method B: gh CLI (fallback when git push fails)

When `git push` times out (443 connection failure), try `gh` CLI first:

```bash
# Check if gh CLI is available
gh --version

# Create repository (first time)
gh repo create <owner>/<repo> --public --description "<description>"

# Push files via git (gh handles auth)
git push -u origin main

# If git push still fails, use gh api for file operations
gh api repos/<owner>/<repo>/contents/<path> \
  --method PUT \
  -f message="Upload <path>" \
  -f content="<base64>" \
  -f branch="main"

# Create Release
gh release create vX.Y.Z \
  --repo <owner>/<repo> \
  --title "<Skill Name> vX.Y.Z · <English phrase>" \
  --notes "<Release Notes>"
```

**gh CLI advantages over REST API**:
- Automatic authentication (no token extraction needed)
- Handles rate limiting transparently
- Supports `gh repo create` one-command repo setup
- Supports `gh release create` one-command release
- Better error messages

**gh CLI availability check**:
```bash
# Check if gh is installed
gh --version 2>/dev/null || echo "gh CLI not available"

# Check if gh is authenticated
gh auth status 2>/dev/null || echo "gh CLI not authenticated"
```

If gh CLI is not available or not authenticated, fall through to Method C.

### Method C: GitHub REST API (last resort when both git push and gh CLI fail)

When `git push` times out (443 connection failure), use REST API:

#### Step 1: Create repository

```
POST https://api.github.com/user/repos
Headers: Authorization: token <GH_TOKEN>
         Content-Type: application/json
Body: {"name": "<repo>", "private": false, "auto_init": false}
```

#### Step 2: Upload files

```
PUT https://api.github.com/repos/<owner>/<repo>/contents/<path>
Headers: Authorization: token <GH_TOKEN>
Body: {"message": "Upload <path>", "content": "<base64>", "branch": "main"}
```

**For updating existing files**, must first GET to obtain sha:

```
GET https://api.github.com/repos/<owner>/<repo>/contents/<path>
→ response.sha

PUT https://api.github.com/repos/<owner>/<repo>/contents/<path>
Body: {"message": "Update <path>", "content": "<base64>", "sha": "<existing-sha>", "branch": "main"}
```

**Important**: REST API does NOT check .gitignore. Must implement own exclusion logic (same as security audit).

#### Step 3: Create Release

```
POST https://api.github.com/repos/<owner>/<repo>/releases
Headers: Authorization: token <GH_TOKEN>
Body: {
  "tag_name": "vX.Y.Z",
  "target_commitish": "main",
  "name": "<Skill Name> vX.Y.Z · <English phrase>",
  "body": "<Release Notes in Markdown>"
}
```

### Token Extraction

Token can be extracted from existing project git remotes:

```bash
git remote -v
# Look for: https://<user>:ghp_xxx@github.com/...
```

### Windows PowerShell Compatibility

**Forbidden in PowerShell 5**:
- `$(cat <<'EOF' ... EOF)` — heredoc not supported, `<<` parsed as redirect
- `Invoke-RestMethod` with Chinese JSON body — causes `_x000A_` corruption
- Double-quoted string interpolation with `?` — `"?name="` gets eaten by PS variable parsing

**Workarounds**:
- Single-line commit messages; detailed notes in GitHub Release
- Use Python `urllib.request` for Chinese JSON bodies
- Use `+` string concatenation for URLs with `?` and `&`

---

## GitHub Release Notes Template

### Title Format

```
<Skill Name> vX.Y.Z · <English phrase describing this release>
```

**Examples**:
- `Guizang PPT Skill v1.1.0 · Swiss style and community-ready release`
- `WX Peitu v7.0.0 · Design system overhaul with 24 recipes`
- `Skill Publisher v2.0.0 · Product-landing-page README and community templates`

### Body Format (Highlights + Validation)

```markdown
## Highlights

- Added <feature 1>.
- Added <feature 2>.
- Changed <change description>.
- Fixed <fix description>.

## Validation

- <How to verify the changes, e.g., run a script, check a file>
- <Another verification step>
```

### Release Notes Writing Rules

1. **Highlights**：用 `- ` 列表，每条一个完整句子，描述"添加/变更/修复了什么"
2. **Validation**：说明如何验证这个版本的变更
3. **语言**：纯英文（Release 面向国际用户）
4. **不分类**：不需要 Breaking/Feature/Fix 分区，5-8 条要点即可
5. **简洁**：Release Notes 不是 CHANGELOG，不追求穷举

### Release Assets

**默认不上传 Assets**（zip/tar 包）。用户通过以下方式安装：
- `git clone https://github.com/<owner>/<repo>.git`
- `npx skills add <owner>/<repo>`
- `clawhub install <slug>`

**仅在用户明确要求时**才打包上传。打包命令：

```bash
# PowerShell
Compress-Archive -Path SKILL.md, README.md, README.en.md, CHANGELOG.md, LICENSE, .claude-plugin/, references/, .github/ -DestinationPath <skill-name>-vX.Y.Z.zip
```

---

## GitHub Release Update (Workflow B)

### When to Update vs Create New

| Scenario | Action |
|----------|--------|
| MAJOR or MINOR bump | Create new Release |
| PATCH bump, same day as last Release | Update existing Release Notes |
| PATCH bump, different day | Create new Release |

### Update Existing Release

```bash
# Get the latest release ID
gh api repos/<owner>/<repo>/releases/latest --jq '.id'

# Update Release Notes
gh api repos/<owner>/<repo>/releases/<release-id> \
  --method PATCH \
  -f body="<Updated Release Notes>"

# Or via REST API
PATCH https://api.github.com/repos/<owner>/<repo>/releases/<release-id>
Headers: Authorization: token <GH_TOKEN>
Body: {"body": "<Updated Release Notes>"}
```

### Update Release Notes Format

When appending to an existing Release, add new items to the Highlights section:

```markdown
## Highlights

- Added provenance block for skill source identification. (v7.0.1)
- Fixed palette hex values in README.en.md. (v7.0.1)
- Rewrote README as product landing page. (v7.0.0)

## Validation

- Version sync verified across SKILL.md, plugin.json, and CHANGELOG.md.
- Security audit passed.
```

Each appended item includes the version tag in parentheses for traceability.

---

## ClawHub Publishing

### CLI Commands

```bash
# Verify login
clawhub whoami

# Publish
clawhub publish <path> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <version> \
  --tags "<tag1>,<tag2>" \
  --changelog "<changelog text>"
```

### Available Options

| Option | Required | Description |
|--------|----------|-------------|
| `path` | Yes | Skill folder path |
| `--slug` | No | Skill slug (must be globally unique) |
| `--name` | No | Display name |
| `--version` | **Yes** | Version (semver, REQUIRED) |
| `--fork-of` | No | Mark as fork of existing skill |
| `--changelog` | No | Changelog text |
| `--tags` | No | Comma-separated tags (default: "latest") |

### Important Notes

1. **No `--token` option** — login via `clawhub login --token <token> --no-browser` first
2. **No `--license` option** — read from plugin.json
3. **`--version` is REQUIRED** — CLI will fail without it
4. **Slug cannot be changed after publish** — can only publish new versions
5. **Protected namespaces**: `clawhub-` prefix and `-clawhub` suffix are protected
6. **Also avoid**: `openclaw` keyword in slug

### Slug Collision Prevention

Before publishing, always check:

```bash
clawhub inspect <slug>
```

If slug is taken:
1. Choose alternative slug (e.g., `skill-forge` → `skill-forge-ai`)
2. Update ALL references:
   - README.md Badge URL
   - README.en.md Badge URL
   - `clawhub install` command in both READMEs
3. Update plugin.json if needed

### Cross-Platform Naming Strategy

1. Choose GitHub repo name first (no restrictions)
2. Check ClawHub slug availability (avoid protected namespaces)
3. If names differ, add 1-line explanation in README:
   `本项目在 GitHub 仓库为 <repo-name>；在 ClawHub 市场注册名为 <slug>`
4. `plugin.json` name = GitHub repo name; `--slug` overrides for ClawHub

---

## Troubleshooting

### git push timeout (443)

**Symptom**: `Failed to connect to github.com port 443 after 21xxx ms`

**Fix**: Switch to GitHub REST API (Method B above)

### ClawHub "Slug is already taken"

**Symptom**: `Uncaught ConvexError: Slug is already taken`

**Fix**: Choose alternative slug, update all references, re-publish

### PowerShell heredoc error

**Symptom**: `Missing file specification after redirection operator`

**Fix**: Use single-line commit message, put details in GitHub Release

### PowerShell `?` in URL string

**Symptom**: URL gets truncated when using `"$baseUrl?name=$name"`

**Fix**: Use `+` concatenation: `$baseUrl + "?name=" + $name`

### Invoke-RestMethod Chinese corruption

**Symptom**: `_x000A_` appearing in Release notes

**Fix**: Use Python `urllib.request` with `json.dumps(ensure_ascii=False).encode("utf-8")`

### ClawHub SSL certificate error

**Symptom**: `api.clawhub.io` returns SSL error

**Fix**: Do NOT use HTTP API. Use `clawhub` CLI only.

### GitHub API upload bypasses .gitignore

**Symptom**: Files in .gitignore still appear in GitHub repo

**Fix**: Implement own exclusion logic when using REST API. Filter files using the same criteria as security audit before uploading.

---

## Update Workflow (for existing repos)

### Updating files on GitHub

```bash
# Method 1: git push (preferred)
git add <changed-files>
git commit -m "fix: description of change"
git push

# Method 2: REST API (when git push fails)
# GET current sha → PUT with new content + sha
```

### Publishing new version on ClawHub

```bash
# Update version in SKILL.md, plugin.json, CHANGELOG.md
# Then re-publish
clawhub publish <path> --slug <slug> --version <new-version> --changelog "<changes>"
```

**Note**: Old versions on ClawHub cannot be deleted. New version automatically becomes `latest`.
