## Description: <br>
Harvests, indexes, and searches today's festivals and events in San Francisco. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assix](https://clawhub.ai/user/assix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch today's San Francisco event listings, ingest them into a local ChromaDB index, and search that index for event recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Listing or ingesting events makes live requests to sf.funcheap.com. <br>
Mitigation: Run the skill only in environments where outbound web requests are allowed, and confirm that scraping SF Funcheap is acceptable for the intended use case. <br>
Risk: Ingestion and search use a persistent local ./rag_db event index. <br>
Mitigation: Install in a virtual environment or controlled workspace, protect the local index as needed, and delete ./rag_db when the saved event index is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/assix/sanfrancisco-today-festivalevents-agent) <br>
- [SF Funcheap Today listings](https://sf.funcheap.com/today/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON from CLI commands; Markdown guidance for agent usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [List, ingest, search, and JSON CLI actions; ingestion and search use a local ./rag_db ChromaDB store.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
