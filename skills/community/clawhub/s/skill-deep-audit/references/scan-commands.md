# Scan command reference

> Command bodies extracted from SKILL.md to keep the body within the length
> budget (D4-E6). Decision rules live in [check-rules.md](./check-rules.md).

## Code-size stats (prerequisite for D7)

Used by SKILL.md Step 2.4. Judgement rules: see check-rules.md D7-W2 / D7-W3.

```bash
# Number of script files (covers mixed skills: .js/.cjs/.mjs/.ts)
find {skill-path}/scripts -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) 2>/dev/null | grep -v node_modules | wc -l

# Total line count (-r prevents hang on no-match)
find {skill-path} \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) | grep -v node_modules | xargs -r wc -l 2>/dev/null | tail -1
```

## Skill-on-skill dependency extraction (D7-W2 three-step join)

```bash
# (1) List all suspicious import candidates (module names only; ownership resolved later)
grep -rnE "^\s*(from [a-zA-Z_][a-zA-Z0-9_]* import|import [a-zA-Z_][a-zA-Z0-9_]*)" {skill-path}/scripts/ 2>/dev/null

# (1b) sys.path injection / skill-root concatenation — the physical evidence of
#      which skill an import actually belongs to
grep -rnE "sys\.path\.insert.*skills/|_skill_root|skills/[a-z-]+/scripts" {skill-path}/scripts/ 2>/dev/null

# (2) subprocess calls into another skill's scripts (by path)
grep -rnE "skills/[a-z-]+/scripts|_skill_root.*scripts" {skill-path} 2>/dev/null | grep -v __pycache__

# (3) Explicit declaration in SKILL.md
grep -nE "metadata.*requires|depends on .* skill|requires the .* skill|use .* skill" {skill-path}/SKILL.md 2>/dev/null
```

Then: deduplicate, apply the three-step join to fix ownership, annotate each
dependency's purpose, run the existence check (D7-W2), and write the result into
report section "VI. Skill Dependencies".

> Stdlib and well-known PyPI packages (`os` / `sys` / `json` / `re` /
> `requests` / `openpyxl` …) are excluded from ownership judgement.
