## Description:

Use when the user asks to optimize, improve, or rewrite a prompt, or when a vague request needs to be turned into a precise instruction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and AI assistant users use this skill to convert vague requests into precise prompts, rewrite existing prompts, select template or LLM-only optimization modes, and optionally evaluate prompt quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local prompt-template JSON files and save optimizer settings under memory/prompt_optimizer_state.json.

Mitigation: Install it only in environments where local template reads and preference storage are acceptable, and review the files it can access before enabling template-first mode.

Risk: Standalone installation asks users to append instruction text to persistent assistant configuration files.

Mitigation: Review the standalone instructions and target configuration file before appending them to a persistent assistant rules file.

Risk: The template libraries are external resources referenced by the artifact.

Mitigation: Fetch external template libraries only from a trusted source and verify their contents before use.

## Reference(s):

- [Prompt Optimizer ClawHub Release](https://clawhub.ai/thomaszhou22/skills/tz-prompt-optimizer)
- [Prompt Library Lite](https://raw.githubusercontent.com/Thomaszhou22/prompt-optimizer/main/references/prompt_library_lite.json)
- [Prompt Library Full](https://raw.githubusercontent.com/Thomaszhou22/prompt-optimizer/main/references/prompt_library_full.json)
- [Prompt Template Categories](https://github.com/Thomaszhou22/prompt-optimizer/tree/main/references/categories)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text, Markdown, or XML prompt rewrites, with optional quality evaluation summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may use local template JSON files and save optimizer preferences when the host environment supports those capabilities.]

## Skill Version(s):

4.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
