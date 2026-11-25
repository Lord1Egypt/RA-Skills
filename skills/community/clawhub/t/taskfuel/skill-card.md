## Description:

Gives the agent capabilities it lacks, billed per call from the user's taskfuel.ai balance: generate images, video, music and speech; transcribe audio; find and verify emails; enrich people and companies; build lead lists; search X, Instagram, TikTok and YouTube; live market, crypto and SEC data; flights and weather; OCR, translation, screenshots; send email, place phone calls, mail letters; run VMs. Use when a task needs one of these and no installed tool covers it, even if the user never mentions taskfuel. Also use when the user names taskfuel.ai or asks to call a paid API. Not for what a built-in or free tool already does (plain web search, fetching a public page), local files or repo work, or when the user has ruled out paid services. Catalog search is free. Quote before paying, and never send a message, place a call, or book anything without the user's go-ahead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taskfuel.ai](https://clawhub.ai/user/taskfuel.ai)

### License/Terms of Use:

MIT

## Use Case:

Agents use TaskFuel when a task needs a capability unavailable through installed tools, including media generation, transcription, data lookup, travel information, document utilities, or user-authorized outbound actions. The skill describes how to discover endpoints, check prices, cap paid calls, and retrieve results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote installer directly, and the security review rates the skill suspicious.

Mitigation: Review the installation steps before use.

Risk: The security review reports endpoint ratings and feedback, and paid calls that may proceed without user approval.

Mitigation: Review the skill's spending steps and explicitly approve installations and paid calls; require approval before any paid operation.

## Reference(s):

- [TaskFuel ClawHub release](https://clawhub.ai/taskfuel.ai/skills/taskfuel)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Text]

**Output Format:** [Markdown instructions with inline shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate paid API calls; the skill requires user approval before sending messages, placing calls, mailing letters, or booking.]

## Skill Version(s):

0.6.2 (source: evidence.json release, artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
