## Description:

Harvests, indexes, and searches today's festivals and events in San Francisco.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assix](https://clawhub.ai/user/assix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current San Francisco event listings, index them locally, and search for relevant activities such as free events or festivals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes network requests to SF Funcheap during listing or ingest actions.

Mitigation: Run it only in environments where outbound requests to that public source are acceptable.

Risk: Ingest actions persist harvested event data in a local ChromaDB database under ./rag_db.

Mitigation: Review local storage expectations and clean or isolate ./rag_db when persistence is not desired.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Use a virtual environment with pinned versions for requests, beautifulsoup4, and chromadb.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/assix/skills/sanfrancisco-today-festivalevents-agent)
- [Publisher profile](https://clawhub.ai/user/assix)
- [SF Funcheap Today](https://sf.funcheap.com/today/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [CLI text, JSON, and markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local ChromaDB database under ./rag_db during ingest operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
