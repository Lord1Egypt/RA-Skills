## Description: <br>
Generate professional presentation slides from a topic or outline, including complete decks users can view, edit, and download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DophinL](https://clawhub.ai/user/DophinL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate editable presentation decks from a topic, outline, or key points through YouMind. It is useful when an agent should create, monitor, and return a hosted slide deck link rather than manually drafting slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation content is sent to YouMind and stored in a YouMind board. <br>
Mitigation: Avoid submitting confidential, regulated, or customer-sensitive content unless the user is comfortable with YouMind processing and storing it. <br>
Risk: The skill depends on the YouMind npm CLI and an API key. <br>
Mitigation: Install the CLI only from a trusted source and configure YOUMIND_API_KEY locally rather than pasting secrets into chat. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DophinL/youmind-slides-generator) <br>
- [YouMind](https://youmind.com?utm_source=youmind-slides-generator) <br>
- [YouMind CLI](https://www.npmjs.com/package/@youmind-ai/cli) <br>
- [Setup](references/setup.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Long-Running Tasks](references/long-running-tasks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and hosted YouMind links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the YouMind CLI and a locally configured YOUMIND_API_KEY; slide generation sends presentation content to YouMind and stores the resulting deck in a YouMind board.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
