## Description:

Use inline buttons when communicating with Rahul on Telegram to reduce typing and force crisp decisions for confirmations, choices, scheduling, approvals, and next-step selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rahulsinghalchicago](https://clawhub.ai/user/rahulsinghalchicago)

### License/Terms of Use:


## Use Case:

Agents use this skill when communicating with Rahul over Telegram and asking for simple choices, confirmations, scheduling decisions, approvals, or next-step selection. It guides the agent to use concise inline button layouts and edit the original Telegram message after a selection instead of asking for free-text replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inline buttons may be used for cases that require free-text input or more than a few options, which can make the Telegram interaction less useful.

Mitigation: Use buttons only for simple decisions, ask for text input when a value must be entered, and summarize large option sets before offering a small follow-up choice.

Risk: Automatic edits after a button click may not match a user's expected Telegram interaction style.

Mitigation: Review the NO_REPLY convention and message-edit behavior before deployment, as recommended by the security guidance.

Risk: Duplicate or stale callbacks could repeat a completed action if the surrounding agent flow does not honor the skill's callback guidance.

Mitigation: Ignore callbacks after the original message has been finalized and the selection has already been committed.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance for Telegram prompt text, inline button layouts, and post-selection behavior.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not produce executable code, credentials, persistent storage, or shell commands.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
