## Description: <br>
OpenClaw SEO-GEO Workflow is a receipt-driven runbook for daily ClawLite/OpenClaw SEO and generative engine optimization operations across topic discovery, content production, publishing QA, and patrol checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SEO operations teams use this skill to run or inspect the OpenClaw daily SEO/GEO workflow, verify publish readiness, diagnose blocked blog delivery, and report live QA or patrol status from durable receipts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow commands can affect production publishing or main-site content when explicit override flags or deploy settings are used. <br>
Mitigation: Require explicit user approval before commands that write to the main site or deploy to production, and verify deploy evidence plus live QA before reporting publication success. <br>
Risk: Provider credentials and connector data are needed for some live patrol, ranking, analytics, and indexing checks. <br>
Mitigation: Keep provider credentials scoped and report missing connector data as skipped, needs data, or pass with warnings rather than silent success. <br>
Risk: Local staging, source publish, or build success can be mistaken for a live production publication. <br>
Mitigation: Inspect durable JSON and Markdown receipts and distinguish staged, built, deployed, and live-QA-verified states in user-facing responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/seo-geo-workflow-for-clawlite) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, status explanations, and receipt paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses receipt-first status reporting and requires explicit evidence before claiming production publication.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
