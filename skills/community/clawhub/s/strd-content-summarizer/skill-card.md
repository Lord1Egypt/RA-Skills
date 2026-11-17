## Description:

Fetches URLs or raw text and produces structured Markdown summaries with extractive key sentences, metadata, and AI enhancement prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content teams use this skill to triage, repurpose, or prepare articles and text for newsletters, research workflows, and LLM-assisted summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL scripts can fetch arbitrary locations, including sensitive internal or authenticated sources if a user supplies them.

Mitigation: Use only public, non-sensitive URLs or raw text; do not provide localhost, internal network, cloud metadata, file://, authenticated, or confidential sources.

Risk: Generated summaries and extracted content may be written to shared temporary storage.

Mitigation: Set OUTPUT_DIR to a private directory for sensitive workflows and delete generated summary files when they are no longer needed.

Risk: Generated AI enhancement prompts may contain untrusted source content.

Mitigation: Review prompts before using them with any tool-enabled agent and treat copied source content as untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/strd-content-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown written to files and printed to the terminal]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [URL summaries are saved under OUTPUT_DIR, defaulting to /tmp/summaries; extracted URL text is capped at 15,000 characters before prompt generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
