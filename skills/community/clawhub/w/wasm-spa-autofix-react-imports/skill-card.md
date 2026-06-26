## Description: <br>
Meticulously detects and fixes missing React/TSX imports, undefined components, and bundler runtime errors in WASM SPA build and preview workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tippyentertainment](https://clawhub.ai/user/tippyentertainment) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to analyze React/TypeScript SPA preview failures and produce targeted source patches for missing imports, undefined JSX symbols, and related bundler errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated patches can introduce incorrect imports or code changes if the missing symbol source is ambiguous. <br>
Mitigation: Review generated patches before applying them, especially in large projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tippyentertainment/wasm-spa-autofix-react-imports) <br>
- [Tasking.tech](https://tasking.tech) <br>


## Skill Output: <br>
**Output Type(s):** [code, text, guidance] <br>
**Output Format:** [JSON containing ordered patch objects, a summary, and remaining issues] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Patches are limited to proposed source edits and should be reviewed before applying.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
