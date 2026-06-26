## Description: <br>
Generates public one-shot or time-limited download links for files using a local Express server exposed through Cloudflare Tunnel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitman86r](https://clawhub.ai/user/hitman86r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to share a local file through a temporary public download link without moving it into a persistent cloud storage service. The skill is intended for deliberate file sharing where the user controls the file, TTL, server secret, and tunnel endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally exposes selected files through an internet-reachable temporary file-sharing service. <br>
Mitigation: Use only for files intended for public-link sharing, verify the exact file and TTL before generating a link, and stop the Node server and Cloudflare Tunnel when finished. <br>
Risk: The /generate and /status endpoints depend on SHARE_SECRET for protection. <br>
Mitigation: Set a strong SHARE_SECRET and prefer the x-share-secret header instead of placing secrets in URLs. <br>
Risk: Copied files may remain in the shared directory if a sharing flow is interrupted. <br>
Mitigation: Periodically inspect the shared directory and remove leftover copies that should no longer be available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitman86r/share-onetime-link) <br>
- [Cloudflare Zero Trust dashboard](https://one.dash.cloudflare.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces tokenized public download links with a user-selected TTL; files are deleted after download or expiry.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
