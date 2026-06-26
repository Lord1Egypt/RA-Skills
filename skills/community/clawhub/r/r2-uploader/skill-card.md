## Description: <br>
Uses the Wrangler CLI to upload files to Cloudflare R2 object storage and return public access URLs, including single-file uploads, direct uploads from remote URLs, and batch uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redisread](https://clawhub.ai/user/redisread) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload local files, remote URL content, or batches of files to a configured Cloudflare R2 bucket and return the resulting public URL. It is intended for workflows where the user explicitly wants an agent to operate Wrangler against their Cloudflare account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload files through the user's Wrangler and Cloudflare account, including broad file sets or unintended sensitive files. <br>
Mitigation: Require explicit confirmation of the exact files, bucket, object path, and public accessibility before upload; avoid broad directories and sensitive folders. <br>
Risk: The skill includes deletion and bucket-management commands that can modify Cloudflare R2 resources. <br>
Mitigation: Require explicit approval before running delete or bucket-management commands, and verify the target bucket and object path before execution. <br>


## Reference(s): <br>
- [r2-uploader ClawHub page](https://clawhub.ai/redisread/r2-uploader) <br>
- [Advanced usage](references/advanced.md) <br>
- [Error handling guide](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and returned URL strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands depend on Wrangler CLI access, R2 bucket configuration, and optional custom domain settings.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
