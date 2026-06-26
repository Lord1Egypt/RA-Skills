## Description: <br>
Audit Svelte and SvelteKit components for performance, accessibility, reactive statement usage, store design, and SSR compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Svelte and SvelteKit projects before production, with emphasis on component quality, accessibility, rendering performance, store design, and SSR safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may require the agent to read source files, routes, stores, configuration files, and package metadata from the current project. <br>
Mitigation: Run it only from the intended project directory and avoid exposing unrelated or sensitive repositories in the working tree. <br>
Risk: Findings can be incomplete or include false positives because the skill relies on pattern-based review and agent judgment. <br>
Mitigation: Validate recommendations with Svelte tooling, tests, and human code review before changing production code. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit report with prioritized findings, tables, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only project inspection guidance; no files are modified by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
