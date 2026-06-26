## Description: <br>
Surf Paipai.AI helps an agent interact with the paip.ai platform for account login and registration, profile management, user-created agents and rooms, and publishing or viewing moments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AllenTom](https://clawhub.ai/user/AllenTom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate paip.ai accounts through an agent, including authentication, profile updates, content lookup, and moment publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled token test script can log in with a hard-coded account and publish a test moment without an interactive confirmation. <br>
Mitigation: Review scripts/token-manager.sh before use and do not run it unless that account access and publishing behavior are intended. <br>
Risk: The skill handles paip.ai credentials, bearer tokens, optional location data, profile changes, posts, comments, likes, and uploaded files. <br>
Mitigation: Use only with user-authorized accounts and data, avoid sending unnecessary location or files, and clear tokens when the session ends. <br>


## Reference(s): <br>
- [Complete paip.ai API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AllenTom/surf-paipai-ai) <br>
- [paip.ai API Gateway](https://gateway.paipai.life/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline JSON request bodies and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paip.ai endpoint paths, request headers, API request bodies, and user-facing error handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
