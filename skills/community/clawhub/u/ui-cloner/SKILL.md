---
name: ui-cloner
description: "Analyzes UI screenshots and generates a reusable .skill file that captures the product's complete design system. Triggers when the user provides UI screenshots (single or multiple pages of the same product) and wants to clone, reproduce, or extract a design system from them. Input: one or more image file paths or a directory. Output: a ready-to-install .skill file encapsulating design tokens, component specs, layout structure, visual style, and interaction patterns. The generated skill can then be used (optionally invoking ui-ux-pro-max) to recreate the UI in any target tech stack."
---

# UI Cloner

Analyze UI screenshots from one product and generate a reusable `.skill` file that fully captures its design system — so anyone can reproduce the same UI in any technology stack.

## When to Use

- User says "clone this UI", "copy this design", "reproduce this page", "extract design system from screenshots"
- User provides one or more screenshots and wants to build something similar
- User wants to reverse-engineer a product's visual language into a reusable format

## Workflow

### Step 1 — Collect Inputs

Ask the user for:
1. **Image source**: a single image path, multiple paths, or a directory
2. **Product name**: used as the generated skill name (e.g. `notion`, `linear`, `stripe-dashboard`)
3. **Brief description** (optional): what the product does — helps contextualize component naming

If the user already provided these in their message, skip asking and proceed.

**Output location**: Determine the save path for the generated skill:
- If the user is currently in a project directory (i.e., the working directory has source files, a package.json, or similar), save the skill **inside the project** at `.claude/skills/{product-name}-ui/` and package the `.skill` file there as well.
- Only fall back to the global skills directory (`~/.claude/skills/`) if there is no identifiable project directory.
- Always tell the user where the skill will be saved before proceeding.

### Step 2 — Analyze Screenshots

For each image, use `mcp__zai-mcp-server__ui_to_artifact` with `output_type: "spec"` to extract design specifications.

Then use `mcp__zai-mcp-server__ui_to_artifact` with `output_type: "description"` to get a plain-language description of each page's purpose and structure.

Analyze all screenshots together as pages of the **same product**. Synthesize findings across images — do not treat them as independent designs.

For the complete list of analysis dimensions and what to extract from each, see → `references/analysis-guide.md`

### Step 3 — Synthesize Design System

From all screenshots combined, produce:

- **Design Tokens**: unified color palette, typography scale, spacing system, border radius, shadow levels
- **Component Inventory**: every distinct UI component identified, with its variants and states
- **Layout Patterns**: grid/flex structures, page templates, navigation patterns
- **Visual Style**: detected style(s) from the taxonomy in `references/analysis-guide.md`
- **Interaction Patterns**: inferred from visual cues (hover states, focus rings, loading indicators, transitions)

When tokens conflict across pages (e.g. different button colors), document all variants — do not discard information.

### Step 4 — Generate the Skill

Create a new skill directory at the path the user specifies (default: same directory as input images, or current working directory).

Skill directory name: `{product-name}-ui`

File structure to create:
```
{product-name}-ui/
├── SKILL.md                    # Main skill file (use references/skill-template.md)
└── references/
    ├── design-tokens.md        # Colors, typography, spacing, radius, shadows
    ├── components.md           # Component inventory with specs and variants
    ├── layout.md               # Page layouts, grid systems, navigation structure
    └── style-guide.md          # Visual style, interaction patterns, UX principles
```

Populate each file with the synthesized data from Step 3.

For the SKILL.md content and structure of each reference file, see → `references/skill-template.md`

### Step 5 — Visual Verification (Optional)

Ask the user:

> "Would you like me to generate a sample page using this design system and compare it visually against your original screenshots to verify accuracy before packaging?"

If the user agrees:
1. Use the draft skill files with `ui-ux-pro-max` to generate a representative page (e.g. the main page from the screenshots) in the user's preferred tech stack (ask if unknown).
2. Take or ask the user to provide a screenshot of the rendered output.
3. Use `mcp__zai-mcp-server__ui_diff_check` to compare the generated page against the original reference screenshot:
   - `expected_image_source`: the original reference screenshot
   - `actual_image_source`: the rendered output screenshot
   - `prompt`: "Compare these two UI screenshots. Identify discrepancies in colors, typography, spacing, component shapes, layout structure, and overall visual style. List each difference with its severity (critical / minor)."
4. Based on the diff report:
   - For **critical** differences (wrong colors, missing components, broken layout): update the relevant reference file in the skill (`design-tokens.md`, `components.md`, or `layout.md`) to correct the spec.
   - For **minor** differences: document them as known variations in `style-guide.md`.
5. Repeat the verify → diff → correct cycle until no critical differences remain, or the user is satisfied.

If the user declines, skip this step and proceed directly to packaging.

### Step 6 — Package as .skill File

Once the design system is verified (or the user skips verification), package the skill.

Run the packager with the determined output path from Step 1:
```bash
python3 /Users/zhenyangze/.claude/skills/skill-creator/scripts/package_skill.py {product-name}-ui {output-dir}
```

Report the output path of the generated `.skill` file to the user.

### Step 7 — Confirm and Offer Next Step

Tell the user:
- The `.skill` file path and where it was saved (project-local or global)
- A summary of what was captured (N colors, N components, detected style, N pages analyzed)
- Offer to immediately use the generated skill to build the UI: "Would you like me to use this skill now to recreate the UI in a specific tech stack?"

If the user says yes, invoke `ui-ux-pro-max` with the generated skill's design tokens and component specs as context, and ask for their preferred tech stack.

## Notes

- Multiple screenshots = same product, different pages. Always merge into one unified design system.
- Never discard design information when synthesizing — document variants rather than averaging.
- The generated skill must be self-contained: someone with no access to the original screenshots should be able to use it to faithfully reproduce the UI.
- Tech stack is intentionally left open — the generated skill describes the design, not the implementation.
- **Save location priority**: always prefer project-local (`.claude/skills/`) over global (`~/.claude/skills/`) to avoid polluting the user's global environment. Only use global as a fallback when no project directory is detected.
- **Visual verification**: the diff-and-correct loop (Step 5) is optional but strongly recommended for high-fidelity reproduction. Always ask the user before running it.
