## Description:

Universal smart search and storage triage for codebases, local files, documents, and archives using full-text, path, and semantic media search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthet1x](https://clawhub.ai/user/synthet1x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to search codebases, documents, local files, archives, and configured media collections. It provides relevant paths and content snippets while helping users manage indexing scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexing may send private media or search data to a configurable embedding destination.

Mitigation: Verify the embedding destination before use and restrict indexing to storage you intend to include.

Risk: Indexing may include files outside the intended scope.

Mitigation: Confirm the target directory and scope before indexing, and keep broad system locations out of the indexed area.

## Reference(s):

- [Smart Storage Triage on ClawHub](https://clawhub.ai/synthet1x/skills/smart-storage-triage)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text search results and Markdown guidance, with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include file paths, content snippets, line or page references, and semantic match scores.]

## Skill Version(s):

1.6.0 (source: release evidence and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
