# Codex CLI Specific Guidance (Additions)

Use this file when the skill is running inside Codex CLI. These additions complement the generic guidance in SKILL.md.

## Autonomy and Completion
- Prefer end-to-end execution in one pass: explore → plan → implement → verify.
- Avoid asking for long upfront plans or preambles; if planning is needed, request a brief plan and then proceed.
- Encourage reasonable assumptions when blocked, but require explicit questions for true blockers.
- Ask for completion with concrete edits rather than only analysis (unless analysis is explicitly requested).

## Tooling Preferences
- Prefer `rg` / `rg --files` for search and `apply_patch` for single-file edits.
- If multiple reads/searches are needed, batch or parallelize tool calls when supported.
- Avoid raw shell commands when a dedicated tool exists (if the harness provides tools).
- Avoid repetitive micro-edits; read enough context and batch logical changes.

## Parallel Tool Calling
- If parallel tool calls are supported, enable them and use `multi_tool_use.parallel`.
- Decide all needed files/resources up front and read them together.
- Avoid sequential reads unless the next file truly depends on the previous result.
- Prefer call ordering: function_call → function_call → function_call_output → function_call_output.

## Output Style
- Ask for concise final reports; avoid dumping full files.
- Reference paths and summarize changes instead of pasting large code blocks.
- Ask for a brief verification summary (what was run, what passed/failed).

## UI/Frontend Work
- Request verification (screenshot comparison) when visual changes are expected.
- Ask for explicit design direction if not provided (typography, layout, color, constraints).

## Code Quality Guardrails
- Preserve existing behavior unless change is explicitly intended.
- Avoid broad try/catch or silent failures; surface errors consistently with repo patterns.
- Maintain type safety; avoid unnecessary casts or weakening types.
- Reuse existing helpers/patterns before adding new abstractions.
