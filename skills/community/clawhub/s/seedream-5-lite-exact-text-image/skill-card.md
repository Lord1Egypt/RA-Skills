## Description:

Uses Seedream 5.0 Lite through AI Hive to generate or edit commercial images with short titles, labels, and campaign copy, with explicit character budgets, manual proofreading, and fallback handling for text accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, and developers use this skill to draft short-text commercial posters, product benefit cards, packaging concepts, event invitations, and social media covers with Seedream 5.0 Lite. It is intended for workflows where generated text is manually checked before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated image text may contain misspellings, extra characters, mirrored text, or layout issues.

Mitigation: Manually transcribe and compare generated text against the approved copy, including spaces, punctuation, numbers, and case; use a text-free image plus design-tool overlay when exact text fails.

Risk: Using the helper requires an AI Hive API key and may upload selected reference images to AI Hive before downloading generated outputs.

Mitigation: Use only approved non-sensitive reference images, store credentials through the documented environment variable or 0600 config file, and install only when this data flow is acceptable.

Risk: Commercial claims, prices, dates, model numbers, ingredients, legal terms, or regulated statements can be inaccurate or unsuitable if generated directly into the image.

Mitigation: Treat approved copy as the only source of truth and require human final review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-exact-text-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples; generated image files and task JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper can upload selected reference images, poll AI Hive generation tasks, and download generated outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
