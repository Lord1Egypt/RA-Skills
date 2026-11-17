## Description:

Save travel inspiration from YouTube videos, Instagram reels, blog URLs, tweets, or plain text like "want to visit Hampi" by extracting destinations, auto-tagging them by vibe and location, and storing them in memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swayamg20](https://clawhub.ai/user/swayamg20)

### License/Terms of Use:


## Use Case:

External users use this skill to save travel ideas from URLs or plain text into agent memory and recall saved destinations later, optionally filtered by tags such as vibe or region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user-provided or webpage-derived travel text, including private or sensitive URLs or notes.

Mitigation: Use explicit travel-save commands, avoid saving private or sensitive URLs or text, and review or delete saved memories through host agent memory controls when available.

Risk: Broad save triggers may cause unintended memory storage when a user forwards a link or casually mentions a destination.

Mitigation: Confirm the saved destination and source in the response, and ask a clarifying question when the destination is unclear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text save confirmations and Markdown-style lists for recall]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist destination names, tags, source URLs or text, and save dates in host agent memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
