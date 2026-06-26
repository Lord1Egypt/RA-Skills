## Description: <br>
Run agent-browser and Chrome inside Vercel Sandbox microVMs for browser automation from any Vercel-deployed app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add browser automation to Vercel-deployed applications without bundling Chrome into the app itself. It helps with screenshots, accessibility snapshots, multi-step browser workflows, scheduled checks, and reusable sandbox setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote browser automation can submit forms, navigate authenticated sites, or change account state if used without review. <br>
Mitigation: Restrict target sites and require confirmation before submitting forms or taking actions that alter account state. <br>
Risk: Vercel credentials, browser sessions, or other secrets could be exposed through client-side code, logs, or reusable sandbox snapshots. <br>
Mitigation: Keep credentials server-side, avoid logging secrets, and do not save private sessions or secrets into reusable sandbox snapshots. <br>
Risk: Unpinned browser automation dependencies or snapshot contents can change behavior between runs. <br>
Mitigation: Pin production dependencies and rebuild snapshots through a reviewed release process. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable guidance for Vercel credentials and optional sandbox snapshot IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
