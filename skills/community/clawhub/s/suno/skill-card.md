## Description: <br>
Generate AI music with Suno via API or browser, with prompt engineering and song extensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, musicians, and developers use this skill to craft Suno prompts, write structured lyrics, generate or extend songs through hosted APIs or browser automation, and track successful project patterns locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, and related creative content may be sent to Suno, aimusicapi.ai, or EvoLink during generation. <br>
Mitigation: Use only services you trust with the creative content being generated, and avoid sending private or sensitive lyrics or project notes. <br>
Risk: Hosted API generation can consume paid credits or quota. <br>
Mitigation: Confirm before generation actions that may spend credits, and use prompt-only or browser testing workflows when appropriate. <br>
Risk: API keys could be exposed if copied into plain text files or source code. <br>
Mitigation: Store API keys in environment variables or a system keychain, and do not write them into the skill memory or project files. <br>
Risk: Local project memory under ~/suno/ can contain preferences, prompts, lyrics, and generated song tracking. <br>
Mitigation: Inspect, restrict, or remove ~/suno/ when prompts, lyrics, or project notes are private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/suno) <br>
- [Suno create page](https://suno.com/create) <br>
- [AI Music API](https://aimusicapi.ai) <br>
- [EvoLink](https://evolink.ai) <br>
- [Skill homepage](https://clawic.com/skills/suno) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, API request examples, and browser automation steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local project memory under ~/suno/ and third-party music generation services when the user chooses API or browser generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
