## Description:

Transforms user-provided text into one sharp, meme-style roast in the detected input language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tian-0818](https://clawhub.ai/user/tian-0818)

### License/Terms of Use:

MIT-0

## Use Case:

Users provide posts, messages, bios, ideas, or short conversations and receive one shareable roast for entertainment. Agents can use the skill when an explicit roast-style response is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to produce harsh insults and may facilitate harassment or inappropriate use against real people, workplaces, minors, or vulnerable users.

Mitigation: Use only in consensual entertainment contexts, avoid targeting vulnerable people or protected classes, and review outputs before sharing.

Risk: Broad invocation on arbitrary text can produce a roast where a user expected neutral help.

Mitigation: Invoke it only for explicit roast requests and route sensitive, support, workplace, or safety-related inputs to a non-roasting assistant.

Risk: The prompt asks for aggressive language while also prohibiting abusive, discriminatory, sensitive, and policy-violating content.

Mitigation: Keep moderation active and reject hate, threats, explicit harassment, and sensitive-topic requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tian-0818/skills/savage-roast-ai)
- [Skill documentation](artifact/SKILL.md)
- [Usage examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text, one sentence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detects Chinese input and otherwise defaults to English; no user parameters.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
