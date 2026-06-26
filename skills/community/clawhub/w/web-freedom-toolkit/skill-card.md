## Description: <br>
Universal Server-Side Web Freedom Toolkit. Harmonizes Scrapling (Self-Healing Fetch), curl_cffi (TLS Impersonation), and DrissionPage (D-Mode) for undetectable browsing on restricted VPS environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Biogod2020](https://clawhub.ai/user/Biogod2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to fetch web content and run browser automation in restricted server environments, including TLS impersonation, stealth fetching, and full Chromium interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad browser automation, browser takeover, and local relay capabilities that are riskier than ordinary web fetching. <br>
Mitigation: Run it only in an isolated environment such as a VM or disposable container, and avoid using browser profiles that contain accounts, cookies, or sensitive local state. <br>
Risk: Scripts may attach to local Chromium DevTools endpoints, forward local ports, launch Chromium with no-sandbox flags, make outbound web requests, and write local report files. <br>
Mitigation: Review the scripts and execution commands before enabling them, restrict allowed targets and outbound network access, and monitor local ports and generated files during use. <br>
Risk: The release is marked suspicious by the server security evidence because its stealth-oriented web automation behavior can be misused. <br>
Mitigation: Install only when the intended workflow specifically requires high-risk browser automation and keep model invocation disabled unless a human has approved each action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Biogod2020/web-freedom-toolkit) <br>
- [Security Explained](SECURITY_EXPLAINED.md) <br>
- [ClawHub Standards](CLAW_HUB_STANDARDS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/text outputs from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON reports under the skill assets directory when scripts are executed.] <br>

## Skill Version(s): <br>
8.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
