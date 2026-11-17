## Description:

Manages customer review collection, auto-replies, alerts, reports, review monitoring, sentiment analysis, and competitor comparison across Naver Place, Google, Baemin, and Coupang.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT

## Use Case:

External business operators and their agents use this skill to monitor customer reviews, generate draft replies, detect negative reviews, produce weekly review reports, and compare competitor review performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord alert and report flows may execute shell commands built from untrusted review text.

Mitigation: Do not enable Discord alerts or scheduled runs until command execution is changed to argument-array APIs and review JSON is validated.

Risk: Customer review data storage and Discord sharing are under-disclosed.

Mitigation: Document what customer data is stored locally and what data is sent to Discord before commercial deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/review-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Node.js commands and JSON configuration; scripts produce local JSON review, reply, alert-state, and report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a configured review-manager config.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
