# Skill Search Workflow

A complete workflow for searching, installing, and validating skills from multiple sources.

## Prerequisites

Ensure CLI tools are available before searching.

**Check CLI availability:**
```bash
# Check skills.sh (runs via npx, no install needed)
npx skills --version

# Check clawhub (requires global install)
clawhub --version 2>/dev/null || echo "Not installed"
```

**Install CLI tools:**
```bash
# Skills.sh CLI (Vercel) - No installation needed, runs directly via npx
# Just use: npx skills <command>

# ClawHub CLI (OpenClaw) - Requires global installation
npm i -g clawhub
# or
pnpm add -g clawhub
```

---

## Step 1: Local Search

Search locally installed skills first:

```bash
python scripts/search_skills.py --intent ${OUTPUT_DIR}/01-intent.md --output ${OUTPUT_DIR}/02-local.md
```

## Step 2: Registry Search (Dual-track)

Search both skill registries:

**Skills.sh (Vercel ecosystem):**
```bash
npx skills find <capability>
```

**ClawHub (OpenClaw ecosystem, semantic search):**
```bash
clawhub search "<capability>"
```

## Step 3: Merge Results

Combine all sources into `${OUTPUT_DIR}/02-candidates.md`:
- Deduplicate by skill name/function
- Mark source: `[local]`, `[skills.sh]`, or `[ClawHub]`
- Sort by relevance score

See template: [templates/02-candidates.md](templates/02-candidates.md)

---

## Step 4: Skill Selection

Use `AskUserQuestion` tool to let user select:
- **A**: Recommended skill(s) from search results
- **B**: Alternative selection from the list
- **C**: Native abilities only (no skill needed)
- **D**: Additional requirements (then re-search)

> **Note**: If selected skill is not installed locally, proceed to Step 5.

---

## Step 5: Skill Install (Conditional)

Only if selected skill is from registry (not local):

**Skills.sh:**
```bash
npx skills add <slug> -g -y
```

**ClawHub:**
```bash
clawhub install <slug>
```

## Step 6: Verify Installation

Verify the skill was installed correctly:

```bash
python scripts/verify_skill.py --skill ./skills/<skill-name> --output ${OUTPUT_DIR}/02-verify.md
```

**Verification checks:**
- Directory exists
- SKILL.md exists
- SKILL.md has valid frontmatter (name, description)
- No file corruption

**Results:**
- ✅ **PASS**: Skill installed correctly → Continue to Step 7
- ❌ **FAIL**: Installation failed → Return to Step 4 for alternative

## Step 7: Security Audit

Run automated security audit on installed skill:

```bash
python scripts/audit_skill.py --skill ./skills/<skill-name> --output ${OUTPUT_DIR}/02-audit.md
```

**Results:**
- 🟢 **PASS**: No high-risk patterns → Skill ready to use
- 🔴 **REJECT**: High-risk detected → Remove the malicious skill and return to Step 4

---

## Output Files

| File | Description |
|------|-------------|
| `02-local.md` | Local search results |
| `02-candidates.md` | Merged candidates from all sources |
| `02-verify.md` | Installation verification report |
| `02-audit.md` | Security audit report |

## Flow Summary

```
Step 1: Local Search
    ↓
Step 2: Registry Search (skills.sh + ClawHub)
    ↓
Step 3: Merge Results → 02-candidates.md
    ↓
Step 4: Skill Selection (Checkpoint)
    ↓ (if registry skill)
Step 5: Install
    ↓
Step 6: Verify Installation
    ├── PASS → Continue
    └── FAIL → Return to Step 4
    ↓
Step 7: Security Audit
    ├── PASS → Skill ready
    └── REJECT → Remove and return to Step 4
```
