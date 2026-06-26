## Description: <br>
Exposes a local file, folder, screenshot, or HTTP service through a temporary trycloudflare.com tunnel and verifies the public URL before sharing it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ojbkxiongdei](https://clawhub.ai/user/ojbkxiongdei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create temporary public links to local files, folders, screenshots, or localhost services and confirm those links respond correctly before sharing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary public Cloudflare links can expose private folders, files, or local services if the served path is too broad. <br>
Mitigation: Use a dedicated export folder containing only the exact content to share, avoid authenticated localhost apps, and stop the server and tunnel as soon as the link is no longer needed. <br>
Risk: A tunnel URL may be shared before the public endpoint is reachable or serving the expected content. <br>
Mitigation: Verify the local origin, tunnel registration, exact public URL status, and expected content type or length before returning the link. <br>


## Reference(s): <br>
- [Verification Checklist](references/verification-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ojbkxiongdei/trycloudflare-proxy-verify) <br>
- [Publisher Profile](https://clawhub.ai/user/ojbkxiongdei) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and verified public URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include temporary trycloudflare.com URLs after reachability verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
