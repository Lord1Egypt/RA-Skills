## Description: <br>
Gives AI agents persistent identity and shared memory across runtimes, devices, and sessions using a Git-native memory hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingcharleslzy-ai](https://clawhub.ai/user/kingcharleslzy-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to set up a private Git-backed memory hub so multiple AI agents can share stable persona, user preferences, and durable session context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists agent-written context to a Git repository, which can expose secrets, credentials, raw transcripts, or sensitive personal or business data if agents write them into memory. <br>
Mitigation: Keep the repository private, define what may be stored before first use, prohibit secrets and sensitive raw logs, and review commits periodically. <br>


## Reference(s): <br>
- [Template repo](https://github.com/kingcharleslzy-ai/agent-soul) <br>
- [ClawHub skill page](https://clawhub.ai/kingcharleslzy-ai/soul-sharing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and python3; stores selected memory events in a user-controlled Git repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
