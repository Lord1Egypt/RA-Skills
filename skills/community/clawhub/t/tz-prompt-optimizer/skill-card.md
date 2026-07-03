## Description: <br>
Prompt Optimizer rewrites vague or draft prompts into precise, structured prompts using template matching and host-AI meta-prompting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhou22](https://clawhub.ai/user/thomaszhou22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and other prompt authors use this skill to turn rough instructions into structured prompts, choose template or LLM optimization modes, and optionally evaluate before-and-after prompt quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language activation can rewrite prompts when the user did not intend to invoke optimization. <br>
Mitigation: Keep the optimizer off by default, activate it only on explicit prompt-optimization requests, and disable it during unrelated conversation or code review. <br>
Risk: Persistent preference state can affect later prompt rewrites and may be undesirable for sensitive prompts. <br>
Mitigation: Review or remove stored optimizer state before sensitive work, and use in-conversation state where persistence is not needed. <br>
Risk: External prompt libraries are referenced while server-resolved import provenance is unavailable. <br>
Mitigation: Use vetted or pinned local library files, or switch to LLM-only mode when template-library provenance cannot be confirmed. <br>
Risk: Prompt rewriting can change user intent or introduce misleading guidance. <br>
Mitigation: Review the optimized prompt before use and rely on the skill's confirmation and iteration flow for corrections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomaszhou22/tz-prompt-optimizer) <br>
- [Prompt library categories](https://github.com/Thomaszhou22/prompt-optimizer/tree/main/references/categories) <br>
- [Lite prompt library](https://raw.githubusercontent.com/Thomaszhou22/prompt-optimizer/main/references/prompt_library_lite.json) <br>
- [Full prompt library](https://raw.githubusercontent.com/Thomaszhou22/prompt-optimizer/main/references/prompt_library_full.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain text, Markdown, or XML prompt text; optional Markdown-style quality evaluation report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optimized prompts, brief change notes, template references, confirmation prompts, and before/after quality scores.] <br>

## Skill Version(s): <br>
4.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
