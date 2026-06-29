# Uandai Agent Packaging Guide (OpenClaw → Upload Zip)

**Docs-Version:** 2026.06.19  
**Related:** [Programmatic API guide](./programmatic-api.md) — upload after packaging (minimal ZIP: `bundle` + name + description).

---

## Section 0 — Uandai upload contract

`POST /v1/agents/upload` (legacy: `/agents/upload`) accepts **one** mode per request.

### ZIP mode (`bundle`)

Use this guide to build the archive. **Minimal trainer POST:** `bundle`, `agent_name`, `description` only (price/model via app or proposals). **Full POST** also requires `subscription_price`, `default_model_identifier`, provider `config_data_type_json` / `test_values_json` (provider URL when required; **never** `{PROVIDER}_KEY` in `test_values_json`).

| Rule | Detail |
|------|--------|
| Format | `.zip` only, max **50MB** |
| Zip root | Personality files (e.g. `SOUL.md`, `IDENTITY.md`) at **archive root**, not only under `workspace/` |
| No nested wrapper | Do not zip a single parent folder that contains everything (e.g. `MyAgent/SOUL.md`) |
| `SKILL.md` placement | Only at `skills/<id>/SKILL.md`, `workspace/skills/<id>/SKILL.md`, or zip root |
| Exclusions | No `node_modules/`, `.env`, `logs/`, `memory/`, `.openclaw/`, `output/`, **`uandai-ai/`** (platform skill) in final zip |
| Artifact path | `output/<agent-name>-workspace.zip` under workspace root |
| After packaging | Upload with [programmatic API](./programmatic-api.md) (`bundle` field) |

### OpenClaw import (`openclaw_root` / multipart `files`)

Server/advanced path — **not** the trainer minimal flow. Requires price, model, and provider URL / custom test rows at POST (not `{PROVIDER}_KEY`). Trainers should package a ZIP per this guide instead. See [programmatic API — OpenClaw import](./programmatic-api.md#prerequisites--openclaw-import-openclaw_root--files).

Common validation errors:

- `openclaw_bundle_legacy_workspace` — move personality markdown to zip root
- `openclaw_bundle_nested_wrapper` — remove extra parent folder
- `openclaw_bundle_missing_personality` — add required personality files at root
- `openclaw_bundle_platform_skill` — remove `uandai-ai/` (and deprecated platform skill dirs) from zip

---

## OpenClaw packaging instructions

Role: You are an Automated DevOps Packaging Agent.

Objective:
Analyze the current workspace, identify its unique structure and dependencies
(including nested skill components), sanitize the workspace, and create a
portable ZIP archive suitable for redistribution.

CRITICAL RULE (read first):
• NEVER zip the live workspace root directly.
• Compress-Archive and zip do NOT support exclusion filters.
• You MUST copy into a staging folder with exclusions, validate staging,
  then zip ONLY the staging folder.

==================================================
PHASE 1: DEEP STRUCTURAL AUDIT (Discovery)
==================================================

1. Recursive Workspace Scan
   • For discovery only (full tree), execute:
     - Windows: tree /f
     - Linux/macOS: find .
   • For “what will be packaged” preview, use the filtered tree command in
     Phase 2 step 5 (mandatory before zipping).

2. Identify "The Core"
   Locate and document:
   • Entry-point scripts
   • Identity/configuration files
   • Runtime launchers
   • Main application files

   Examples include:
   • SOUL.md
   • IDENTITY.md
   • *.js
   • *.mjs
   • *.cjs
   • *.ts
   • *.py
   • main.*
   • index.*
   • app.*

3. Dependency Mapping
   Scan BOTH the root workspace AND all nested directories,
   especially:
   • skills/
   • modules/
   • packages/
   • services/
   • tools/

   Detect dependency systems:

   Node.js:
   • package.json
   • package-lock.json
   • pnpm-lock.yaml
   • yarn.lock

   Python:
   • requirements.txt
   • pyproject.toml
   • poetry.lock
   • Pipfile

   Go:
   • go.mod

   Rust:
   • Cargo.toml

   Java:
   • pom.xml
   • build.gradle

   Document discovered dependencies as:
   • Root Dependencies
   • Component Dependencies
   • Skill-Specific Dependencies

4. Asset Categorization
   Categorize discovered directories/files:

   • references/
   • docs/
   • knowledge/
     → "Domain Knowledge"

   • scripts/
   • bin/
   • cli/
     → "CLI Tooling"

   • skills/
   • modules/
   • agents/
     → "Composable Components"

==================================================
PHASE 2: PRECISION SANITIZATION & PACKAGING
==================================================

1. Create Output Directory
   Ensure output/ exists under the workspace root (not inside skills/).

2. Strict Recursive Exclusion Rules
   The following MUST NEVER be included in the archive,
   regardless of nesting depth.

   --------------------------------------------------
   Secrets & Sensitive Files
   --------------------------------------------------

   Exclude recursively:
   • .env (exact name only — NOT .env.example / .env.template)
   • secrets.json
   • credentials.json
   • id_rsa
   • id_dsa
   • *.pem
   • *.key
   • *.p12
   • *.crt

   IMPORTANT:
   • Preserve `.env.example`
   • Preserve `.env.template`
   • Preserve sample/example configuration files

   --------------------------------------------------
   Dependency / Build Artifacts
   --------------------------------------------------

   Exclude recursively:
   • node_modules/
   • venv/
   • .venv/
   • __pycache__/
   • dist/
   • build/
   • target/
   • coverage/
   • .next/
   • .nuxt/
   • .cache/
   • tmp/

   --------------------------------------------------
   Version Control / IDE / Tooling
   --------------------------------------------------

   Exclude recursively:
   • .git/
   • .svn/
   • .hg/
   • .idea/
   • .vscode/
   • .openclaw/

   --------------------------------------------------
   Runtime / Generated Data
   --------------------------------------------------

   Exclude recursively:
   • memory/
   • logs/
   • output/
   • *.log
   • *.tmp
   • *.sqlite
   • *.sqlite3
   • *.db

   --------------------------------------------------
   Platform Integration Skills (trainer-only)
   --------------------------------------------------

   Exclude recursively (directory name match at any depth):
   • uandai-ai/

   Rationale: Uandai platform skill for configure, package, exchange, and upload.
   Install from `GET /docs/openclaw-skills/uandai-ai/SKILL.md` or `~/.openclaw/skills/`;
   never ship inside the agent product zip.


   --------------------------------------------------
   REQUIRED SAFETY RULES
   --------------------------------------------------

   • Apply exclusions recursively at ALL directory depths.
   • Exclude both directories AND all contents within them.
   • Never follow symlinks into excluded paths.
   • Never include hidden secrets accidentally discovered.
   • If exclusion conflicts occur, EXCLUSION ALWAYS WINS.
   • Sanitize BEFORE archive creation.

3. MANDATORY STAGING WORKFLOW (execute exactly)

   Replace [AGENT_NAME] with the workspace agent slug (e.g. jove, Agent).
   Run all commands from the OpenClaw workspace ROOT (parent of output/).

   ---------- Windows (PowerShell) ----------

   $AgentName = "[AGENT_NAME]"
   $Root = Get-Location
   $Staging = Join-Path $Root "output\$AgentName-workspace"
   $ZipPath = Join-Path $Root "output\$AgentName-workspace.zip"

   # A) Reset staging
   if (Test-Path $Staging) { Remove-Item -Recurse -Force $Staging }
   New-Item -ItemType Directory -Path $Staging -Force | Out-Null

   # B) Copy with exclusions (robocopy). Exit codes 0–7 = success.
   robocopy $Root $Staging /E /NFL /NDL /NJH /NJS /nc /ns /np `
     /XD node_modules dist build target coverage .next .nuxt .cache tmp `
         venv .venv __pycache__ memory logs output .git .svn .hg `
         .idea .vscode .openclaw uandai-ai `
     /XF .env secrets.json credentials.json id_rsa id_dsa `
         *.pem *.key *.p12 *.crt *.log *.tmp *.sqlite *.sqlite3 *.db

   # C) Remove any .env files that slipped in (keep .env.example)
   Get-ChildItem $Staging -Recurse -Force -File |
     Where-Object {
       $_.Name -eq '.env' -or (
         $_.Name -like '*.env' -and
         $_.Name -notlike '*.example' -and
         $_.Name -notlike '*.template'
       )
     } | Remove-Item -Force

   # D) MANDATORY pre-zip validation (must pass before step E)
   $bad = Get-ChildItem $Staging -Recurse -Force -Directory |
     Where-Object { $_.Name -in @(
       'node_modules','dist','logs','memory','output','.git','.openclaw',
       'venv','.venv','__pycache__','uandai-ai'
     )}
   if ($bad) { throw "Staging still contains forbidden dirs: $($bad.FullName)" }

   tree $Staging /f /a | Where-Object {
     $_ -notmatch '\\node_modules\\' -and $_ -notmatch '(?i)node_modules$' `
     -and $_ -notmatch '\\dist\\' -and $_ -notmatch '(?i)\\dist$' `
     -and $_ -notmatch '\\logs\\' -and $_ -notmatch '(?i)\\logs$' `
     -and $_ -notmatch '\\memory\\' -and $_ -notmatch '\\output\\' `
     -and $_ -notmatch '\\.git\\' -and $_ -notmatch '\\.openclaw\\'
   }

   # E) Create zip from staging contents only (zip root = workspace root)
   if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
   Push-Location $Staging
   Compress-Archive -Path * -DestinationPath $ZipPath -CompressionLevel Optimal
   Pop-Location

   # F) MANDATORY post-zip validation
   $verify = Join-Path $env:TEMP "uandai-zip-verify-$AgentName"
   if (Test-Path $verify) { Remove-Item -Recurse -Force $verify }
   Expand-Archive $ZipPath -DestinationPath $verify -Force
   $badZip = Get-ChildItem $verify -Recurse -Force -Directory |
     Where-Object { $_.Name -in @('node_modules','dist','logs','memory','.git','uandai-ai') }
   if ($badZip) { throw "ZIP contains forbidden dirs: $($badZip.FullName)" }
   Remove-Item -Recurse -Force $verify

   # G) Optional: remove staging folder after success
   Remove-Item -Recurse -Force $Staging

   ---------- Linux / macOS (bash) ----------

   AGENT_NAME="[AGENT_NAME]"
   ROOT="$(pwd)"
   STAGING="$ROOT/output/${AGENT_NAME}-workspace"
   ZIP="$ROOT/output/${AGENT_NAME}-workspace.zip"

   rm -rf "$STAGING" && mkdir -p "$STAGING"
   rsync -a \
     --exclude='node_modules/' --exclude='dist/' --exclude='build/' \
     --exclude='target/' --exclude='coverage/' --exclude='.next/' \
     --exclude='.nuxt/' --exclude='.cache/' --exclude='tmp/' \
     --exclude='venv/' --exclude='.venv/' --exclude='__pycache__/' \
     --exclude='memory/' --exclude='logs/' --exclude='output/' \
     --exclude='.git/' --exclude='.svn/' --exclude='.hg/' \
     --exclude='.idea/' --exclude='.vscode/' --exclude='.openclaw/' \
     --exclude='uandai-ai/' \
     --exclude='.env' --exclude='secrets.json' --exclude='credentials.json' \
     --exclude='*.pem' --exclude='*.key' --exclude='*.log' --exclude='*.tmp' \
     --exclude='*.sqlite' --exclude='*.sqlite3' --exclude='*.db' \
     "$ROOT/" "$STAGING/"

   find "$STAGING" -type d \( \
     -name node_modules -o -name dist -o -name logs -o -name memory \
     -o -name .git -o -name output -o -name .openclaw -o -name uandai-ai \) \
     -print | grep . && { echo "FORBIDDEN DIRS IN STAGING"; exit 1; }

   rm -f "$ZIP"
   (cd "$STAGING" && zip -r "$ZIP" .)

   VERIFY="$(mktemp -d)"
   unzip -q "$ZIP" -d "$VERIFY"
   find "$VERIFY" -type d \( -name node_modules -o -name dist -o -name logs \
     -o -name uandai-ai \) -print | grep . && { echo "FORBIDDEN DIRS IN ZIP"; exit 1; }
   rm -rf "$VERIFY" "$STAGING"

4. Archive naming
   Final artifact: output/[AGENT_NAME]-workspace.zip
   • Paths inside the zip must be relative to workspace root (no output/
     wrapper folder, no extra Agent-workspace/ parent unless that IS the
     project root you staged).
   • Do NOT upload a zip of the raw live workspace or of output/ itself.

5. Expected packaged layout (example)
   After extraction, tree should resemble source minus exclusions:

   AGENTS.md, SOUL.md, IDENTITY.md, package.json, package-lock.json,
   tsconfig.json, src/, scripts/, references/, skills/<skill>/src/ ...
   WITHOUT: node_modules/, dist/, logs/, .env, memory/, output/, uandai-ai/

==================================================
PHASE 3: DYNAMIC REPORTING
==================================================

After successful archive creation, output a formal report.

1. Archive Location
   Format:
   📍 Path: MEDIA:[absolute-or-relative-path-to-zip]

2. Archive Statistics
   Include:
   • Total included file count
   • Final archive size
   • Number of excluded files/directories (estimate from robocopy/rsync)

3. Dependency Tree
   Document:

   Root Setup Requirements:
   Examples:
   • npm install
   • pip install -r requirements.txt
   • go mod download

   Component / Skill Requirements:
   Examples:
   • skills/parser → npm install
   • modules/vision → pip install -r requirements.txt

4. Quick Start Guide

   Installation:
   Provide exact initialization commands.

   Examples:
   • npm install
   • pnpm install
   • pip install -r requirements.txt

   Execution:
   Provide commands for primary entry points and CLI utilities.

   Examples:
   • node index.mjs
   • python main.py
   • node scripts/run-sql.mjs

   Configuration:
   • Remind users to copy `.env.example` to `.env`
   • Identify components requiring secrets/configuration

==================================================
FINAL VALIDATION CHECKLIST
==================================================

Before completion, verify ALL of the following:

✓ Staging copy used (not direct Compress-Archive on workspace root)
✓ Pre-zip tree/validation passed with zero forbidden directories
✓ Post-zip expand validation passed
✓ No node_modules directories included
✓ No memory directories included
✓ No logs directories included
✓ No dist directories included
✓ No .env secrets included (.env.example allowed)
✓ No runtime-generated files included
✓ ZIP archive at output/[AGENT_NAME]-workspace.zip
✓ Dependency report generated
✓ Quick-start instructions generated
✓ Archive paths are portable and relative
✓ No `uandai-ai/` directory in staging or zip (`skills/`, `workspace/skills/`, or nested)
✓ Platform skill remains on trainer host (`~/.openclaw/skills/`), not in bundle

---

## Section 4 — Upload to Uandai

After packaging, upload with the [programmatic API guide](./programmatic-api.md). Exchange your API key for a JWT first — raw `uand_live_…` keys are rejected on upload.

**Default trainer path (minimal ZIP):** POST only `bundle`, `agent_name`, and `description`. Collect name and description from the user before upload. Return `agent.id` and `revision_no` from the `201` response. Complete price, duration, provider LLM, and model at `{APP_SITE_URL}/training-center/agents/manage/{agent.id}` or via `POST /agents/{id}/proposals`, then `PATCH …/proposals/{id}` with `status=submitted` when ready.

```bash
UANDAI_API_BASE_URL="${UANDAI_API_ORIGIN}/api"

# 1. Exchange API key → access JWT
RESP=$(curl -sS -X POST "$UANDAI_API_BASE_URL/v1/auth/token" \
  -H "Authorization: Bearer $UANDAI_API_KEY")
ACCESS=$(echo "$RESP" | jq -r .access_token)

# 2. Upload packaged zip (minimal multipart fields)
curl -sS -X POST "$UANDAI_API_BASE_URL/v1/agents/upload" \
  -H "Authorization: Bearer $ACCESS" \
  -F "bundle=@output/<agent-name>-workspace.zip" \
  -F "agent_name=My Agent" \
  -F "description=Marketplace description"
```

Full ZIP upload (`subscription_price`, `default_model_identifier`, provider `config_data_type_json` / `test_values_json` — URL only when required, no `{PROVIDER}_KEY`) and OpenClaw import: [programmatic API guide](./programmatic-api.md).
