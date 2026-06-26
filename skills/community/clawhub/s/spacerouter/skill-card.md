## Description: <br>
Route HTTP traffic through Space Router residential IP proxy network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taelimoh](https://clawhub.ai/user/taelimoh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route intentional HTTP requests through Space Router when residential IP routing, region targeting, or proxy verification is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Traffic routed through Space Router uses a third-party network path. <br>
Mitigation: Use the proxy only for intentional, non-sensitive requests and avoid internal or sensitive destinations. <br>
Risk: Session-wide proxy environment variables can unintentionally affect unrelated commands. <br>
Mitigation: Prefer per-command proxy options such as curl -x and unset proxy variables after use. <br>
Risk: Proxy credentials in SPACE_ROUTER_PROXY_URL can grant access to the service. <br>
Mitigation: Keep SPACE_ROUTER_PROXY_URL secret and avoid writing it to logs, shared shell history, or committed files. <br>
Risk: Optional SDK or CLI installation depends on third-party package provenance. <br>
Mitigation: Verify the SDK or CLI package provenance before installing optional packages. <br>


## Reference(s): <br>
- [SpaceRouter ClawHub release](https://clawhub.ai/taelimoh/spacerouter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPACE_ROUTER_PROXY_URL for proxy routing and verification.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
