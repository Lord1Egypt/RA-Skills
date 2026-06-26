## Description: <br>
Validates Vitest config and workspace files for syntax, deprecated options, plugin conflicts, and best-practice issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check Vitest and Vite test configuration files before committing or auditing test setup changes. It reports syntax, compatibility, performance, and best-practice findings without executing JavaScript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex-based static validation can miss dynamic Vitest config behavior or complex TypeScript patterns. <br>
Mitigation: Treat findings as best-effort guidance and manually review important config changes. <br>
Risk: The validator reads local config paths supplied by the user. <br>
Mitigation: Run it only against intended Vitest or Vite config files in the workspace; scanner evidence reports no network, credential, persistence, or file-mutation behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/vitest-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Human-readable text, JSON, or one-line PASS/WARN/FAIL summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate pass, validation failure, or file/read/parse errors; strict mode treats warnings as errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
