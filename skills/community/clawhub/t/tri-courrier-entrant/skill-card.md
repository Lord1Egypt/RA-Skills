## Description: <br>
Trie un mail entrant pour déterminer s'il concerne la comptabilité, extrait les pièces jointes exploitables et normalise les informations d'en-tête utiles pour les étapes suivantes du pipeline comptable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, accounting teams, and workflow agents use this skill as the first step in an accounting pipeline to decide whether an incoming email should be processed and to prepare a clean initial dossier for downstream document analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input mail JSON can contain sensitive accounting email body text, sender details, message IDs, and attachment paths. <br>
Mitigation: Use the skill only in the accounting-mail pipeline and handle inputs and outputs under the same access controls as sensitive accounting records. <br>
Risk: The skill classifies relevance from attachment formats and accounting keywords without reading attachment contents. <br>
Mitigation: Send relevant attachments to the downstream document-analysis step before making accounting decisions from the attachment content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trendex/tri-courrier-entrant) <br>
- [Publisher profile](https://clawhub.ai/user/trendex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON classification metadata with normalized email fields, selected attachments, ignored attachments, and a relevance reason.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes a mail JSON payload from stdin or a local JSON file path and does not perform network access, persistence, or file mutation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
