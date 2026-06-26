## Description: <br>
Generate AI music with Udio via API wrappers or browser automation, with prompt engineering and song extensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, and developers use this skill to craft Udio prompts, generate or extend AI music through browser automation or community API wrappers, and organize local project notes, seeds, and downloaded songs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode depends on a sensitive Udio session token and unofficial/internal Udio API behavior. <br>
Mitigation: Treat sb-api-auth-token like a password, avoid pasting it into chats or plain files, store it in a credential manager or environment variable, and refresh it only through the user's authenticated Udio session. <br>
Risk: Community wrapper packages receive the user's Udio token when used for API generation. <br>
Mitigation: Review the selected wrapper source and package before installation or execution, and use prompt-only or browser mode when token sharing is not acceptable. <br>
Risk: Local project memory under ~/udio/ can contain creative preferences, project details, seeds, and generated-song references. <br>
Mitigation: Review ~/udio/memory.md and project files for sensitive details before sharing, syncing, or committing local workspace content. <br>


## Reference(s): <br>
- [ClawHub Udio skill page](https://clawhub.ai/ivangdavila/udio) <br>
- [Udio](https://www.udio.com) <br>
- [Python UdioWrapper community wrapper](https://github.com/flowese/UdioWrapper) <br>
- [Node udio-wrapper community wrapper](https://github.com/josephgodwinkimani/udio-wrapper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, prompt text, setup commands, and browser or API workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local file organization under ~/udio/ and may produce code or commands that use UDIO_AUTH_TOKEN when API mode is selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
