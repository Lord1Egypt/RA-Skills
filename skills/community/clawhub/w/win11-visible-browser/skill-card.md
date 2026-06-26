## Description: <br>
Guides an agent in controlling, diagnosing, and repairing a visible Windows 11 Edge/Chrome browser from OpenClaw in WSL2 via CDP while keeping the user in the loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pe4atnik](https://clawhub.ai/user/pe4atnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when OpenClaw running in WSL2 needs a visible Windows 11 Edge or Chrome session for browsing tasks that require existing browser state, human oversight, login, 2FA, captcha handling, CDP diagnostics, or repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CDP access can expose browser state, logged-in sessions, sensitive tabs, and account actions. <br>
Mitigation: Prefer a dedicated browser profile, close sensitive tabs before diagnostics, keep the browser visible, and require explicit approval before account, payment, form, or other state-changing actions. <br>
Risk: A CDP relay exposed beyond WSL/Hyper-V could allow unintended remote browser control. <br>
Mitigation: Keep CDP on Windows localhost, scope the relay firewall rule to the WSL/Hyper-V CIDR, and never expose the CDP relay to the LAN or Internet. <br>
Risk: Repair flows may change OpenClaw configuration, Windows firewall or portproxy state, browser processes, or persistent Scheduled Tasks. <br>
Mitigation: Run read-only diagnostics first, ask for explicit approval before changes, state rollback steps, and use documented rollback commands such as removing the Scheduled Task, portproxy rule, and firewall rule. <br>
Risk: Visible browser automation can consume memory and CDP stability budget, especially with many tabs, iframes, workers, or reCAPTCHA targets. <br>
Mitigation: Run the read-only browser budget helper before non-trivial browser work, avoid tab fan-out, reuse a small number of agent-owned tabs, archive useful URLs, and leave existing user tabs untouched unless the user approves cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pe4atnik/win11-visible-browser) <br>
- [Setup reference](artifact/references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with bash and PowerShell command snippets, JSON configuration examples, and bundled helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for visible browser control and diagnostics; state-changing actions require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
