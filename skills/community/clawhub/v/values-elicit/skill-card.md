## Description: <br>
Runs a Moral Graph Elicitation interview when the user expresses a strong feeling, goal, norm, or difficult choice, then stores the resulting values card in the configured local values store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klingefjord](https://clawhub.ai/user/klingefjord) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to conduct a structured values interview, capture a source of meaning, and write it as a reusable local values card. The skill is intended for value-laden situations such as difficult choices, strong feelings, goals, norms, or requests to clarify what the user cares about. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive personal values cards and full interview transcripts in a persistent local values store. <br>
Mitigation: Set AGENT_VALUES_DIR to a location you control, review or delete transcripts and cards after sessions, and avoid syncing the store to places where sensitive personal material should not live. <br>
Risk: Approving the optional USER.md snippet can cause future agents to consult personal values during value-laden tasks. <br>
Mitigation: Approve the snippet only if you want this behavior, and remove the snippet or VALUES.md reference later if future-agent access is no longer appropriate. <br>
Risk: Generated values cards can be incomplete, stale, or too narrow for later decisions. <br>
Mitigation: Review generated cards before relying on them, update or delete outdated cards, and ask the user when no card clearly applies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/klingefjord/values-elicit) <br>
- [Publisher Profile](https://clawhub.ai/user/klingefjord) <br>
- [Sources of Meaning, Attention Policies, and Card Format](artifact/references/cards.md) <br>
- [Conversation Flow](artifact/references/conversation.md) <br>
- [Values User Profile Snippet](artifact/references/USER_MD_SNIPPET.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Brief chat guidance plus Markdown values cards, Markdown transcripts, a rebuilt VALUES.md summary, and local setup/configuration updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cards and transcripts under AGENT_VALUES_DIR or ~/.openclaw/values, may append an optional USER.md snippet with user approval, and rebuilds VALUES.md with a Node helper.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
