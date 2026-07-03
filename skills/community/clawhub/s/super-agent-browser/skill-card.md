## Description: <br>
Super Agent Browser guides agents in using the agent-browser CLI for deterministic headless browser automation with accessibility-tree snapshots, ref-based interactions, session isolation, state persistence, and network control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation-focused agents use this skill to navigate sites, fill forms, extract page data, manage isolated browser sessions, persist browser state, and control network behavior through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved authentication state, cookies, and localStorage values can expose sensitive account access. <br>
Mitigation: Keep saved state files out of repositories and logs, use least-privilege test accounts, and avoid loading real authenticated sessions unless required. <br>
Risk: Browser automation can take actions in live web applications or authenticated sessions. <br>
Mitigation: Review target sites and proposed commands before execution, prefer isolated sessions, and use test environments or accounts for risky workflows. <br>


## Reference(s): <br>
- [Agent Browser homepage](https://github.com/vercel-labs/agent-browser) <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce browser snapshots, extracted text or attributes, screenshots, PDFs, cookies, storage values, and network request information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
