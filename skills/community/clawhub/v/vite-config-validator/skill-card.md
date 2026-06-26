## Description: <br>
Validate Vite configuration files (JSON-exported) for structural correctness, build settings, server security, resolve/CSS hygiene, plugin deprecations, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit JSON-exported Vite configuration snapshots, enforce configuration standards in CI, and review vite.config.ts changes for correctness and security hygiene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exporting a Vite config with Node executes that project's configuration code. <br>
Mitigation: Only run the documented export command on repositories you trust, or run it in a sandbox for untrusted pull requests. <br>
Risk: Strict mode can turn warnings into blocking CI failures before a team has calibrated the rule set. <br>
Mitigation: Run without --strict first and review findings before making the validator a required CI gate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/vite-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional text, summary, or JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces validation findings, rule explanations, summaries, and suggested fixes for JSON-exported Vite configs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
