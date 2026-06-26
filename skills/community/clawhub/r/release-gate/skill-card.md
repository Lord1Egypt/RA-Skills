## Description: <br>
Prevents bad deploys by enforcing structured sign-off before any irreversible action. Configurable checklist with named reviewers (Dev, QA, Legal, Product). Blocks execution until all required gates pass and logs every decision. Use before systemctl restarts, file deploys, database migrations, public launches, or any action that is hard to undo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferrentinomj-dev](https://clawhub.ai/user/ferrentinomj-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release managers, and AI agents use this skill to run structured deployment sign-off before hard-to-undo, customer-facing, or high-stakes changes. It provides configurable role-based checklists and logging patterns for pass or block decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the checklist helper as proof that approvals, tests, or reviews actually happened. <br>
Mitigation: Verify every checklist item with independent evidence before invoking the helper, and block the release when any required sign-off is missing or uncertain. <br>
Risk: Deployment logs may contain sensitive operational notes. <br>
Mitigation: Choose an access-controlled log path and avoid writing secrets, credentials, or unnecessary sensitive details in gate notes. <br>
Risk: A failed or skipped log write can leave the deployment decision without an audit trail. <br>
Mitigation: Confirm the log entry exists before proceeding with the irreversible action. <br>


## Reference(s): <br>
- [Release Gate on ClawHub](https://clawhub.ai/ferrentinomj-dev/release-gate) <br>
- [OWASP Secure Coding Practices Quick Reference Guide](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/) <br>
- [The Twelve-Factor App](https://12factor.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown checklists, configuration examples, and Python helper snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper can append gate decisions to a text log when invoked by an agent or workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
