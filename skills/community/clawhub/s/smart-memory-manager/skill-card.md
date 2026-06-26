## Description: <br>
Intelligent memory management for agents with short/long-term memory layering, semantic search, auto summarization, RAG enhancement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ayalili](https://clawhub.ai/user/Ayalili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add, search, summarize, list, clear, save, and load short-term, long-term, and important memories for long-running conversations, RAG applications, assistants, and customer-support agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memory files may contain private conversation context or other sensitive data. <br>
Mitigation: Avoid storing secrets, credentials, regulated data, or sensitive conversation history, and keep memory files in a dedicated private directory. <br>
Risk: Loading memory from local files may reintroduce stale, incorrect, or sensitive context into an agent session. <br>
Mitigation: Review memory files before loading them and clear or edit entries that are no longer appropriate. <br>
Risk: Saving memory can overwrite files that the runtime is allowed to write. <br>
Mitigation: Use an explicit persistence path in a dedicated memory directory and verify the path before save operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ayalili/smart-memory-manager) <br>
- [Zod v3.22.4 for Deno](https://deno.land/x/zod@v3.22.4/mod.ts) <br>
- [Deno standard encoding hex module](https://deno.land/std@0.214.0/encoding/hex.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, configuration, guidance] <br>
**Output Format:** [JSON result objects and Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns action-specific success flags, memory records, counts, summaries, error messages, and file paths for persistence actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
