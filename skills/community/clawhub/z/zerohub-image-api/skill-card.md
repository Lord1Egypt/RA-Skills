## Description: <br>
zeroHub image generation API skill that uses a user-provided ZEROHUB_API_KEY to check balance, submit image generation jobs, poll results, and optionally download generated images to a user-selected directory with HTTPS, zeroHub-host, and size limits by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenzihao0731](https://clawhub.ai/user/chenzihao0731) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to connect agents or scripts to the zeroHub image generation API, including balance checks, image generation task submission, polling, and controlled download of generated image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive ZEROHUB_API_KEY for API calls. <br>
Mitigation: Provide the key through the ZEROHUB_API_KEY environment variable, avoid command tracing or logs that expose it, and install only if you trust zeroHub. <br>
Risk: Generated image downloads create files in a local output directory. <br>
Mitigation: Choose the output directory intentionally and rely on the default user-specified directory behavior rather than writing to unspecified locations. <br>
Risk: Relaxing download controls can allow untrusted hosts or HTTP URLs. <br>
Mitigation: Keep the default HTTPS and zeroHub-host restrictions for normal use; avoid --allowed-host or --allow-http with untrusted URLs. <br>


## Reference(s): <br>
- [zeroHub homepage](https://zerohub.zhyy.ltd) <br>
- [zeroHub API documentation](https://zerohub.zhyy.ltd/docs) <br>
- [ClawHub skill page](https://clawhub.ai/chenzihao0731/zerohub-image-api) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chenzihao0731) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command output; optional downloaded image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZEROHUB_API_KEY for API calls and writes downloaded files only to the user-specified output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
