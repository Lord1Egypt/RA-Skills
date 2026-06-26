## Description: <br>
Securely input API keys and sensitive values into OpenClaw without typing them in chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apsntian](https://clawhub.ai/user/apsntian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use SecretClaw to collect API keys, tokens, passwords, and other sensitive configuration values through a temporary HTTPS form instead of placing secrets in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real secrets through a temporary Cloudflare tunnel, which may not fit every user's trust model. <br>
Mitigation: Install only when the user trusts the skill source, local openclaw and cloudflared binaries, and Cloudflare Quick Tunnel for the specific secret being entered; use a local or manual configuration method when tunnel transit is unacceptable. <br>
Risk: A generated secret-entry URL grants temporary access to submit a value for the configured key. <br>
Mitigation: Treat the URL as sensitive temporary access, share it only with the intended user, and verify the config path before submitting a secret. <br>


## Reference(s): <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Cloudflare Tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a temporary HTTPS secret-entry URL and saves the submitted value through openclaw config set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
