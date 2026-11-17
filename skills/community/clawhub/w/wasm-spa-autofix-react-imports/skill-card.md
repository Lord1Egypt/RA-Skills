## Description:

Meticulously detects and fixes missing React/TSX imports, undefined components, and bundler runtime errors in the WASM SPA build/preview pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tippyentertainment](https://clawhub.ai/user/tippyentertainment)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to diagnose React preview failures and generate focused source patches for missing imports, undefined JSX components, and related bundler runtime errors in WASM SPA projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stubs can hide missing real components when no import source is found.

Mitigation: Review any proposed stubs and replace them with project components when an authoritative source exists.

Risk: Automated import patches can select the wrong source for ambiguous JSX symbols.

Mitigation: Inspect proposed patches against project conventions and rerun the preview or type checks before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tippyentertainment/skills/wasm-spa-autofix-react-imports)
- [Tasking.tech platform](https://tasking.tech)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON object containing ordered patch descriptions, a summary, and remaining issues.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Patches are expected to be limited to import edits and small stubs when no reliable import source exists.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
