---
name: skillwiki
description: "Analyze and review ClawHub skills. IMPORTANT: Always run scripts/fetch_skill.py first to download skill data as JSON from ClawHub — NEVER read the target skill's files directly. Use when: reviewing a skill before install, comparing skills, checking skill security, understanding what a skill does, or generating a skill summary."
---

# SkillWiki

> ⛔⛔⛔ **STOP — READ THIS BEFORE ANYTHING ELSE** ⛔⛔⛔
>
> When the user asks to analyze a skill, you MUST run `fetch_skill.py` to download the skill from ClawHub. Do NOT read the target skill's SKILL.md. Do NOT browse the target skill's directory. Do NOT open any file belonging to the target skill.
>
> **Why?** `fetch_skill.py` downloads the skill package from ClawHub and extracts ALL data (SKILL.md body, scripts, env vars, URLs) into a single JSON. You analyze that JSON — nothing else.
>
> **This applies to ALL skills** — always download from ClawHub, never read local files.

Download and extract skill metadata for AI-powered analysis. The script handles downloading, data extraction, and cleanup. You (the LLM) perform the actual analysis using the extracted data.

## When to Use

- User wants to understand what a skill does before installing
- User asks to review or analyze a skill's security
- User wants to compare two or more skills
- User needs a summary of a skill's capabilities
- User wants to learn how a skill is built

## Quick Start

```bash
# From ClawHub (default: English)
python scripts/fetch_skill.py x-search  # Windows
python3 scripts/fetch_skill.py x-search  # macOS/Linux

# With language preference
python scripts/fetch_skill.py x-search --lang zh  # Windows: Chinese report
python3 scripts/fetch_skill.py x-search --lang zh  # macOS/Linux: Chinese report
python scripts/fetch_skill.py x-search --lang=en  # Alternative syntax

# Or update config via command
python scripts/fetch_skill.py --config SKILLWIKI_LANG=zh

# Save raw JSON to file (optional)
python scripts/fetch_skill.py x-search output.json  # Windows
python3 scripts/fetch_skill.py x-search output.json  # macOS/Linux
```

## Workflow

⛔ **NEVER read the target skill's SKILL.md or any of its files.** The ONLY correct workflow is: run `fetch_skill.py <slug>` → analyze the JSON output. All skills are downloaded from ClawHub — never read local files.

**Always `cd` into the skillwiki directory before running scripts**, so relative paths work correctly regardless of where skillwiki is installed (`.trae/skills/`, `.copaw/skills/`, etc.):

```bash
cd path/to/skills/skillwiki
python scripts/fetch_skill.py <slug>
```

**Language Auto-Update (First Step)**: Before running any analysis, check if the user's request mentions a language preference (e.g., "中文报告", "use Chinese", "用英文", "japanese"). If yes, first update the config:

```bash
cd path/to/skills/skillwiki
python scripts/fetch_skill.py --config SKILLWIKI_LANG=zh
```

Then proceed with the normal workflow. This ensures the config is updated for all subsequent analyses.

### 1. Fetch Skill Data

Run `scripts/fetch_skill.py` with the skill slug. The script downloads the skill from ClawHub and extracts all data.

**If the user asks to change settings in chat** (e.g., "switch to Chinese"), run `--config`:
```bash
python scripts/fetch_skill.py --config SKILLWIKI_LANG=zh
```

Output is JSON containing:
- `name` / `description` / `version` / `license` / `homepage` / `author`
- `env_vars` - declared environment variables (from frontmatter)
- `bins` - declared binary dependencies
- `undeclared_env_vars` - env vars used in scripts but NOT declared in frontmatter (may include false positives from comments/logs)
- `detected_urls` - URLs found in script code (may include false positives from comments/logs)
- `files` - list of all files in the skill (noise files filtered)
- `scripts` - content of script files (truncated if >50KB)
- `truncated_scripts` - list of script files that were truncated
- `body` - full SKILL.md body (after frontmatter)
- `source` - always "clawhub"
- `lang` - report language preference from `SKILLWIKI_LANG` in skillwiki.conf (default: "en")

### 2. Classify Skill Type

Determine the skill's type before analysis — this changes the evaluation criteria:

| Type | Definition | Key Risk |
|------|-----------|----------|
| **Script Execution** | Has `.py`/`.sh`/`.js` scripts that run code | Code-level vulnerabilities, hidden endpoints, data exfiltration |
| **Directive Following** | Pure SKILL.md, no scripts, instructs the LLM | Prompt injection, instruction ambiguity, LLM compliance |
| **Hybrid** | Both scripts and significant SKILL.md instructions | Combined risks of both types |

Classification heuristic:
- If `scripts` is non-empty and contains real code → Script Execution
- If `scripts` is empty and `body` is long (>100 lines) → Directive Following
- If both → Hybrid
- Flag dangerous patterns regardless of length: `os.system`, `subprocess`, `eval`, `exec`, `Execute`, `Run command`
- For directive skills, watch for jailbreak-like patterns (e.g., instructions that attempt to override prior context, assume new personas, or bypass constraints)

### 3. Analyze (You do this)

Use the extracted data to provide analysis. **Apply the correct evaluation path based on skill type.**

#### Determine Report Depth Based on User Intent

- **Quick question** (e.g., "is this safe?", "what does this do?"): Only output ⭐ Verdict & Action + At a Glance + one-sentence capability summary
- **Full review** (e.g., "analyze", "audit", "detailed review of"): Output the complete report
- **Never** output the Alternatives section unless the user explicitly asks for alternatives

#### Common Analysis (all types)

**Summary**: What does this skill do? What is its approach?

**Security Review**:
- Does it request credentials? Are they declared in frontmatter? Check `undeclared_env_vars` for gaps.
- Does it make network calls? Check `detected_urls` for all endpoints.
- Does it read/write files? Where?
- Any shell injection risks?

**Cross-Validation Rule**: For `undeclared_env_vars` and `detected_urls` provided by the script, verify against the actual code context in `scripts`. If a URL only appears in comments, logs, or string constants (not actual network calls), mark it as a false positive and exclude it from security findings.

**Truncation Warning**: If `truncated_scripts` is non-empty, OR if the `body` field appears to be cut off (ends mid-sentence or with a truncation marker), you cannot complete a 100% audit. Downgrade the safety rating (e.g., from 🟢 to 🟡) and explicitly state: "Content was truncated, incomplete audit possible, hidden risks cannot be ruled out."

**Quality Assessment**:
- Is the description clear and accurate?
- Are all dependencies declared? (`undeclared_env_vars` is a red flag)
- Does the script match the description?
- Any red flags (obfuscated code, hidden endpoints)?

#### Directive-Skill Additional Analysis

For Directive Following and Hybrid skills, also evaluate:
- **Prompt Resistance**: How well would the skill's instructions hold up under adversarial user input? Can a user easily bypass the skill's constraints?
- **Injection Protection**: Does the skill handle user-provided content (URLs, file contents, pasted text) safely? Could malicious content in user input alter the skill's behavior?
- **State Machine Clarity**: If the skill defines workflows or states, are transitions clear? Are edge cases handled? What happens when workflows conflict?
- **Instruction Length vs. Attention**: Is the SKILL.md too long for the LLM to reliably follow all instructions? Flag if body > 300 lines.

#### Script-Skill Additional Analysis

For Script Execution skills, also evaluate:
- **Input Validation**: Are user inputs validated before use? (regex, type checks, bounds)
- **Dependency Safety**: Are external packages from trusted sources? (PyPI, npm vs. personal GitHub)
- **Error Handling**: Are network failures, timeouts, and malformed responses handled?

### 4. Present Results

Render the analysis as **markdown directly in your chat response** (not as a file or document attachment).

**Language**: Read the `lang` field from the JSON output. This field is your ONLY language reference. **You MUST write the ENTIRE report in that language — no mixing.**
- `"en"` → ALL English (report title, every header, every table cell, every word — NO Chinese characters allowed)
- `"zh"` or `"cn"` → ALL Chinese (report title, every header, every table cell — NO English headers allowed)
- Any other value → treat as the target language code

**Critical**: The `lang` field takes absolute priority over the user's question language. If the user asks in Chinese but `lang` is "en", write the ENTIRE report in English. If `lang` is "zh", write the ENTIRE report in Chinese even if the user asks in English. Never use the user's question language to decide the report language.

*(Note: The template below uses English section headers as placeholders. Translate ALL of them to the target language before generating.)*

**Translation Reference (for Chinese `zh`/`cn`):**
- "Skill Analysis Report" → "技能分析报告"
- "Verdict & Action" → "结论与建议"
- "At a Glance" → "概览"
- "Capability Analysis" → "能力分析"
- "Strengths" → "实现亮点"
- "Weaknesses" → "不足之处"
- "Security & Dependency Audit" → "安全与依赖审计"
- "Quality Score" → "质量评分"
- "Code Quality" → "代码质量" / "Instruction Quality" → "指令质量"
- "Usage Guidance" → "使用指南"
- "Alternatives" → "替代方案"
- "When to Use" → "适用场景"
- "When NOT to Use" → "不适用场景"
- "Prerequisites" → "前置条件"

**Language Auto-Update**: When the user mentions a language preference (e.g., "中文报告", "use Chinese", "用英文"), you MUST first update the config using `--config SKILLWIKI_LANG=<code>` BEFORE running the analysis:

```bash
cd path/to/skills/skillwiki
python scripts/fetch_skill.py --config SKILLWIKI_LANG=zh
python scripts/fetch_skill.py <slug> --lang zh
```

This ensures subsequent analyses use the same language automatically.

Use this report structure:

```markdown
# {name} Skill Analysis Report
*(Use the `name` field from JSON for BOTH the report title and the At a Glance table — NOT the slug. They may differ, e.g. name="self-improvement" vs slug="self-improving-agent". Always prefer the frontmatter `name`.)*

> Generated by SkillWiki on {date}

---

## ⭐ Verdict & Action

**Safety Rating: 🟢 Safe / 🟡 Caution / 🔴 Avoid**

{1-2 sentence verdict. What is this skill? What's the bottom line?}

**Prerequisites:**
1. {prerequisite 1}
2. {prerequisite 2}

---

## At a Glance

| Property | Value |
|----------|-------|
| Name | {name} |
| Version | {version or ⚠️ Undeclared} |
| License | {license} |
| Author | {author or Unknown} |
| Type | {Script Execution / Directive Following / Hybrid} |
| Env Vars | {declared env_vars, or None} |
| Bin Deps | {bins} |
| {type-specific fields} | {e.g., Scripts: 2, External APIs: ...} |

## Capability Analysis

### What It Does and How
{2-3 sentences explaining the skill's core mechanism}

### Strengths

| Feature | Evaluation |
|---------|------------|
| {feature} | {evaluative description, not just restating} |

### Weaknesses

- {defect with specific evidence}

## Security & Dependency Audit

**Credentials:**
{✅/⚠️ assessment with evidence}

**Network Calls:**

| Endpoint | Purpose | Data Sent |
|----------|---------|-----------|
| {url} | {purpose} | {what data} |

**Shell Injection Risk:**
{✅/⚠️ assessment}

**Security Summary:**

| Check | Status |
|-------|--------|
| Shell Injection | ✅/⚠️/🚫 |
| Data Exfiltration | ✅/⚠️/🚫 |
| Credential Handling | ✅/⚠️/🚫 |
| Hidden Endpoints | ✅/⚠️/🚫 |
| Code Obfuscation | ✅/⚠️/❓ |
| Frontmatter Declared Deps | ✅/⚠️ |

## {Directive/Script}-Skill Specific Assessment

{For Directive skills: prompt resistance, injection protection, state machine clarity}
{For Script skills: input validation, dependency safety, error handling}

## Quality Score

### {Code Quality / Instruction Quality}

| Dimension | Evaluation |
|-----------|------------|
| {dimension} | ✅/⚠️ {evaluative description} |

### Overall: {N}/10

**Pros:** {what's good}
**Cons:** {what's bad}

## Usage Guidance

**When to Use:**
- {when to use}

**When NOT to Use:**
- {when NOT to use}

**Prerequisites:**
1. {prerequisite}

## Alternatives

| Alternative | Pros/Cons |
|-------------|-----------|
| {alternative} | {pros/cons} |
```

### 5. Compare Skills (optional)

When the user asks to compare skills, fetch each skill separately, then create a comparison section:

```markdown
## Comparison

| Dimension | {skill-a} | {skill-b} |
|-----------|-----------|-----------|
| Type | | |
| Safety Rating | | |
| Quality Score | | |
| External Deps | | |
| Credential Needs | | |
| Best For | | |

**Recommendation:** {which one and why}
```

## Guidelines

### Be Specific, Not Generic

- Reference actual code lines when making claims
- Quote the skill's own instructions back when relevant
- Point out discrepancies between description and implementation
- Use `undeclared_env_vars` and `detected_urls` as evidence, not guesswork

### Security First

- Flag any undeclared credentials (`undeclared_env_vars` is a direct signal)
- Note all external endpoints (cross-reference `detected_urls` with `env_vars`)
- Highlight data exfiltration risks
- Warn about shell injection if inputs are not validated
- Always cross-validate scanner results against actual code context before flagging

### Be Concise

- Match report depth to user intent (quick question → short answer, full review → full report)
- Lead with the bottom line (⭐ section first)
- Put details in structured tables, not walls of text
- Never output Alternatives unless explicitly asked

### Evaluative, Not Descriptive

- Don't just restate what the skill does — judge how well it does it
- Use evaluative language: "well-designed" not "has input validation"; "risky" not "uses os.system"
- Every claim should help the user make a decision

## Script Reference

| Script | Purpose |
|--------|---------|
| `scripts/fetch_skill.py` | Download skill from ClawHub, extract data, scan for env vars and URLs, detect truncated scripts, clean up |

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CLAWHUB_DOWNLOAD_URL` | Custom ClawHub API URL | Builtin |
| `SKILLWIKI_LANG` | Report language (overridden by --lang flag) | en |

All settings are managed in `skillwiki.conf` (in the skill root directory). Use `--config KEY=VALUE` to update. Priority: `--lang` flag > skillwiki.conf > default.
