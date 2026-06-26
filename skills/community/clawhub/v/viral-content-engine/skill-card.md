## Description: <br>
Find trending topics, create editorial-style social media graphics, and post to X/Twitter and Instagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashmonmc](https://clawhub.ai/user/ashmonmc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and social-media operators use this skill to research viral topics, generate editorial-style image assets, and prepare or run posting workflows for Instagram and X/Twitter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live posting authority for real Instagram and X/Twitter accounts. <br>
Mitigation: Review every caption, media file, destination account, and publish action before running posting commands. <br>
Risk: The skill uses account credentials and API keys for Instagram, Brave Search, OpenAI, and X/Twitter tooling. <br>
Mitigation: Use environment variables or existing authenticated tools, avoid passing Instagram passwords on the command line, and rotate credentials if they are exposed. <br>
Risk: Shell-based helper scripts construct commands from user-provided search and posting inputs. <br>
Mitigation: Avoid untrusted search text or captions until command construction is hardened, and inspect commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ashmonmc/viral-content-engine) <br>
- [OpenAI Images API endpoint used by the image generator](https://api.openai.com/v1/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external social, search, and image-generation services when the user runs the provided commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
