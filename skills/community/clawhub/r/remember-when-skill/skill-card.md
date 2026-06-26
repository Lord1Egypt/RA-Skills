## Description: <br>
An intelligent digital archivist skill for OpenClaw agents that monitors chat groups, captures memorable text and media, generates summaries, and persists entries to local storage via the Remember When CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericmora](https://clawhub.ai/user/ericmora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent identify, summarize, and archive memorable chat content and shared media through the local remember-when CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent archiving may store sensitive chat text and media locally. <br>
Mitigation: Restrict folder access, require confirmation before archiving or backfilling, and review archived content and metadata. <br>
Risk: Contextual enrichment can use external search tools despite local-only privacy claims. <br>
Mitigation: Disable enrichment or external-search use when local-only behavior is required. <br>
Risk: Shell access to the remember-when CLI can create or update archives and copy media. <br>
Mitigation: Grant only the required CLI and storage permissions and require confirmation for bulk or update operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ericmora/remember-when-skill) <br>
- [Remember When homepage](https://remember-when.agentic.2mes4.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the remember-when CLI binary and shell access; may write local archive files and media references.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
