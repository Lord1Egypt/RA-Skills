## Description: <br>
Extracts shopping and payment intent from the current conversation and returns a structured JSON summary, either by using a trusted local payment-intent summarizer when available or by analyzing the conversation context directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhc1111](https://clawhub.ai/user/xhc1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to summarize shopping or payment-related details from the current conversation into a compact JSON result. It is intended for intent extraction and summary only, not for making purchases or executing payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local payment-intent command, if present, could be untrusted or behave differently from the skill documentation. <br>
Mitigation: Allow command-based summarization only with a trusted local payment-intent tool; otherwise use direct conversation-context analysis. <br>
Risk: Shopping or payment intent summaries can expose sensitive purchase or payment-related details from the conversation. <br>
Mitigation: Summarize only the current conversation context and avoid reading external session files or cross-session data. <br>
Risk: The skill identifies intent but may be mistaken when conversation context is ambiguous. <br>
Mitigation: Use conservative classification when uncertain and return hasIntent false when no clear shopping or payment intent is present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xhc1111/shopping-intent-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON object with boolean, enum, string, null, and summary fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The summary field is expected to be concise Chinese text; when no shopping or payment intent is detected, hasIntent is false.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
