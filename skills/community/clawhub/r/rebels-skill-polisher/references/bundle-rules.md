# Bundle Rules

Rules for polishing multi-skill bundles. A bundle is a directory containing sub-directories with their own SKILL.md files, plus shared infrastructure (scripts, references, config). The polisher auto-detects bundle mode — no configuration needed.

---

## Bundle Detection

Scan the target directory. It's a bundle if:

1. The directory contains a root SKILL.md **and** sub-directories with their own SKILL.md files, OR
2. The directory contains multiple sub-directories each with a SKILL.md file, OR
3. The directory contains a `shared/` directory alongside sub-directories with SKILL.md files

If none of these match → standalone mode. Apply the standard polishing flow.

**Edge case — extracted sub-skills:** If you're pointed at a single skill directory that contains multiple signs of bundle origin together (references to `$WEBCLIENT_STUDIO_CONFIG_DIR/shared/` AND cross-skill field names like `qualification_report_path` AND bundle-specific env vars), advise the user: *"This looks like an extracted bundle sub-skill. For best results, point me at the full bundle source so I can preserve cross-skill contracts."* Do not attempt to reconstruct bundle context from a flat directory.

**Note:** A single sign (e.g., a skill that happens to use a shared directory pattern) is not enough to flag. Look for multiple indicators together before advising the user. False positives here would incorrectly reject legitimate standalone skills.

---

## Bundle Polishing Flow

### Phase 1: Pre-Flight

**1. Read all SKILL.md files** in the bundle (root + all sub-skills).

**2. Build the dependency map.** Scan every SKILL.md for:

| What to scan for | Pattern | Why |
|-----------------|---------|-----|
| Field names | `--field-name`, `<field>`, `field_name` in command blocks | Another skill may read this field |
| File paths | `$WEBCLIENT_STUDIO_CONFIG_DIR/...`, relative paths | Another skill may reference this path |
| Variable names | `$SHARED`, `$BUNDLE_SOURCE`, env vars | Shared infrastructure references |
| Section headings | `## Section Name` in cross-references | Another skill may point to this section |
| Report structures | Template sections like `## Fit Assessment` | Downstream skills parse these sections |
| Tag names | `imported`, custom tags | Cross-skill flow contracts |

**Require bidirectional evidence:** A dependency is only real if one skill **writes** or **defines** something and another skill explicitly **reads** or **references** it. Generic field names that appear in multiple skills without a clear write/read relationship are coincidental — don't flag them. Exclude overly generic names (`status`, `path`, `notes`, `name`, `date`, `id`) from automatic protection unless there's explicit cross-reference evidence.

**Output:** A list of dependencies like:
```
lead-qualifier §7a → writes qualification_report_path → read by proposal-builder §3, project-onboarder §1
lead-qualifier §6 → defines report template → sections read by proposal-builder §3
pipeline-tracker §K → writes "imported" tag → read by lead-qualifier Enrichment Mode
```

**3. Identify bundle boilerplate.** Find content that appears in 2+ sub-skills. Two levels:

- **Identical boilerplate:** Content that is word-for-word the same across 2+ skills (e.g., first run guard clause, path expansion warning). Standardize the formatting and keep inline in every copy.
- **Structural boilerplate:** Content that follows the same pattern but has skill-specific differences (e.g., tools sections where `SHARED=...` is identical but the commands listed differ). Standardize the shared portion, keep the skill-specific portion as-is.

Mark these as "bundle boilerplate — standardize but keep inline."

**4. Clean stale references.** Regex sweep across all files for:
- `§X.Y` patterns (e.g., `architecture §9`, `lead-qualifier.md §5.3`)
- References to non-existent design docs (`architecture.md`, `storage.md`, `<skill-name>.md`)
- Any reference where the target file doesn't exist in the bundle directory

Remove these. They're development artifacts that confuse users.

### Phase 2: Polish Sub-Skills

Process each sub-skill **one at a time**. The order matters — polish skills that other skills depend on first (data producers before data consumers).

**For each sub-skill:**

**1. Read the SKILL.md.**

**2. Rewrite for readability.** Apply the standard rules from `references/rules.md`:
- Short paragraphs, code blocks, emoji anchors, tight tables
- Move appropriate content to references/
- **Keep protected content inline** (see rules.md for the full list)
- **Keep cross-skill data contracts inline** (anything in the dependency map)
- **Standardize bundle boilerplate** — if identical content appears in multiple skills, ensure the polished version is consistent across all copies (same wording, same formatting)

**3. Update cross-skill references.** Check the dependency map:
- If content was moved to references/, find all skills that reference it
- For **already-polished skills**: update the reference to point to the new location
- For **not-yet-polished skills**: add to the "pending fixes" list (don't edit them yet — they'll change when polished)

**4. Run regression check.** Verify the polished output:
- Every field name in the dependency map still appears (or has been correctly moved with updated references)
- Every file path still resolves
- Every cross-skill reference is valid
- No protected content was moved to references/
- Bundle boilerplate matches the standardized version

**5. Audit the rewrite.** Run the full audit checklist from `references/audit-guide.md`, including the bundle-specific regression checks.

**6. Output:** Present the polished SKILL.md, any new reference files, and the audit report. Wait for user approval before overwriting.

### Phase 3: Cross-Validation

After all sub-skills are polished:

**1. Rebuild the dependency map** from all polished files.

**2. Compare against the original map.** Every dependency should still resolve. If something broke, identify which polish step caused it and fix.

**3. Process remaining pending fixes.** Any cross-reference updates queued for the last skill polished should have been applied. Verify they're correct.

**4. Verify bundle boilerplate consistency.** Check that identical content across skills is still word-for-word the same after all polishes.

**5. Output the final cross-validation report.**

---

## Pending Fixes Pattern

When content is moved from skill A (already polished) and skill B (not yet polished) depends on it:

```
After polishing skill A:
  - Moved report template to references/report-template.md
  - Dependency map shows skill B §3 references this template
  - Skill B is not yet polished → add to pending fixes:
    "skill B §3: update report template reference to point to A/references/report-template.md"

When polishing skill B:
  - Check pending fixes list
  - Apply the fix: update the reference in skill B's polished output
  - Regression check: verify the reference now points to the correct location
  - Remove from pending fixes list
```

**Important:** Only fix references in already-polished skills. Don't edit not-yet-polished skills — their content will change during their own polish pass. The pending fixes list ensures nothing is forgotten.

---

## Dependency Map Format

Present the dependency map to the user before polishing begins. Example:

```
🔗 Dependency Map

Field contracts:
• lead-qualifier writes: qualification_report_path, client_dir_path, research_notes, pitch_notes
  → proposal-builder reads: qualification_report_path, research_notes
  → project-onboarder reads: qualification_report_path, client_dir_path
  → pipeline-tracker reads: research_notes, pitch_notes (display)

• proposal-builder writes: proposal_report_path, proposal_summary, proposal_date
  → project-onboarder reads: proposal_report_path, proposal_summary
  → pipeline-tracker reads: proposal_summary (display)

• project-onboarder writes: project_path
  → pipeline-tracker reads: project_path (display)

Tag contracts:
• pipeline-tracker writes: "imported" tag → lead-qualifier reads (Enrichment Mode)

Report structure contracts:
• lead-qualifier defines report template → proposal-builder reads sections

Bundle boilerplate (identical in 4 skills):
• First run guard clause
• Path expansion warning
• Tools section (partial — commands differ per skill)
```

This gives the user visibility into what the polisher will protect and why.

---

## Polishing Order

When dependencies exist, polish data producers before data consumers:

1. Skills that write fields/paths/tags that others read
2. Skills that define report structures or templates others parse
3. Skills that are entry points (triggered first in the user flow)
4. Root SKILL.md (last — it references all sub-skills)

If there's no clear dependency order, any order works. Just be consistent and do one at a time.

---

## Root SKILL.md Protection

The root SKILL.md is the bundle's entry point and router. During polish:

- **Preserve the routing table** — this is dispatch logic the LLM uses to select sub-skills. Reformat for readability (code block, tight columns) but don't remove entries or consolidate intent descriptions.
- **Preserve routing rules** — "Ambiguous intent" defaults and "No match" behavior are behavioral contracts. Keep inline.
- **Preserve infrastructure overview** — the "How It Works" section explaining storage, dependencies, and requirements is the only architectural overview in the bundle. Don't move it to references/.
- **Don't add redundant sections** — the routing table already serves as "When to Use". Don't add a separate trigger phrases section to the root.
- **Polish last** — the root references all sub-skills. Polish it after all sub-skills are done so cross-references are accurate.

---

## Known Limitations

- **Nested bundles:** If a bundle has sub-skills that themselves contain sub-skills (three or more levels deep), the single-level detection won't find the inner bundle. Advise the user to polish nested bundles separately.
- **Circular dependencies:** If skill A and skill B both write and read each other's fields, the polishing order guidance doesn't fully resolve the ordering. In practice, process whichever skill has more downstream dependents first. The pending fixes pattern handles the rest.
