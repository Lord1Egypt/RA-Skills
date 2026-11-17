## Description:

答8道修仙情境题，测定你的本命灵根（天/双/三/四/全/变异），生成专属道友帖和道号，还可导出帖码供后续技能复用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dora233](https://clawhub.ai/user/dora233)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a Simplified Chinese fantasy quiz, score eight scenario answers, and produce a fictional spiritual-root result with a reusable result code. It supports local HTML UI, step-by-step chat, and plain-text answer-string workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The UI workflow can generate a local HTML page and open it in the user's default browser or HTML handler.

Mitigation: In restricted environments, review or disable the auto-open workflow and use the chat or plain-text workflow instead.

Risk: The generated result code is designed to be shared as quiz output and may be reused by downstream skills.

Mitigation: Treat the result code as non-secret entertainment output, not as an authentication token or private identifier.

Risk: Users may over-read the quiz result as a factual personal assessment.

Mitigation: Keep the fictional entertainment disclaimer visible in generated cards and avoid presenting results as real-world advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dora233/skills/sk-61b00e213202)
- [Linggen setting canon](artifact/references/canon.md)
- [Regression prompts and expected results](artifact/references/test-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional local HTML file generation and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fictional quiz results, a daoist-style post, a display name, and a shareable result code.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact data/meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
