## Description: <br>
Store, recall, and manage personal wine tastings and labels using natural language queries with durable image storage in a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sidvorak](https://clawhub.ai/user/sidvorak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to maintain a local personal wine archive, including tasting history, purchase context, ratings, label images, natural-language recall, export/import, and optional Telegram label sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wine history, purchase locations, notes, ratings, and label photos can reveal private personal information. <br>
Mitigation: Keep the local archive and any exports secure, especially exports that embed label images. <br>
Risk: Optional LLM intent classification can send relevant text to the configured model provider. <br>
Mitigation: Leave LLM intent classification disabled unless provider processing is acceptable for the archive content. <br>
Risk: Telegram label sharing can disclose archived label images to the wrong chat or thread. <br>
Mitigation: Use Telegram sending only for labels intended to be shared and verify the target before sending. <br>
Risk: Removing entries by ID can delete the wrong wine record. <br>
Mitigation: Double-check record IDs before using remove operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sidvorak/wine-archive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses, JSON bridge payloads, and shell command or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local SQLite records, archived label image paths, and optional external LLM or Telegram integrations.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
