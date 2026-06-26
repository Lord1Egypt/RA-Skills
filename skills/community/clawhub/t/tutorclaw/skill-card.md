## Description: <br>
AI programming tutor for the AI Agent Factory curriculum using PRIMM-Lite pedagogy. Bundles agent brain files, offline shim, and MCP server config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samiceto](https://clawhub.ai/user/samiceto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners use this skill as an AI Python programming tutor for the AI Agent Factory curriculum. It guides beginner sessions through PRIMM-Lite tutoring, live TutorClaw tools when available, and bundled offline Chapters 1-5 content when the MCP server is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests sensitive Stripe and Gemini credentials. <br>
Mitigation: Install only after confirming the publisher and use restricted, test, or least-privileged keys where possible. <br>
Risk: The package describes MCP server and configuration components that are not present in the artifact evidence. <br>
Mitigation: Verify the missing MCP server and configuration from a trusted source before enabling live TutorClaw tools. <br>
Risk: The offline fallback cannot save learner progress or execute learner-written code. <br>
Mitigation: Tell learners when the fallback is active, ask them to note their stopping point, and avoid claiming code was executed offline. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samiceto/tutorclaw) <br>
- [Publisher profile](https://clawhub.ai/user/samiceto) <br>
- [TutorClaw skill manifest](artifact/SKILL.md) <br>
- [TutorClaw identity](artifact/IDENTITY.md) <br>
- [TutorClaw agent behavior](artifact/SOUL.md) <br>
- [Offline shim workflow](artifact/tutorclaw-shim/SKILL.md) <br>
- [Chapter 1: Variables and Data Types](artifact/tutorclaw-shim/references/chapters/01-variables.md) <br>
- [Chapter 2: Loops](artifact/tutorclaw-shim/references/chapters/02-loops.md) <br>
- [Chapter 3: Functions](artifact/tutorclaw-shim/references/chapters/03-functions.md) <br>
- [Chapter 4: Data Structures](artifact/tutorclaw-shim/references/chapters/04-data-structures.md) <br>
- [Chapter 5: Working with Files](artifact/tutorclaw-shim/references/chapters/05-files.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tutoring responses with Python code examples, shell command snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live sessions depend on TutorClaw MCP tools; the offline shim can tutor Chapters 1-5 without saved progress or code execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
