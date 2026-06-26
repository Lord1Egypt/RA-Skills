## Description: <br>
Target Research creates small-molecule drug target research reports covering target biology, druggability, competitive landscape, patents, safety, and structured scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drtony1](https://clawhub.ai/user/drtony1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and drug discovery teams use this skill to investigate a named biological target and prepare a structured small-molecule target assessment. It supports target triage by organizing evidence on biology, assay availability, structures, pipelines, patents, safety, literature, and differentiation strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and retrieved target intelligence may be sent to PatSnap LifeScience MCP services and, when needed, web search. <br>
Mitigation: Use only approved PatSnap accounts and avoid confidential commercial or biomedical strategy data unless account terms and internal policy allow it. <br>
Risk: The skill depends on a PatSnap API key and connected PatSnap LifeScience MCP services. <br>
Mitigation: Configure credentials through the agent environment, restrict access to authorized users, and rotate or revoke keys according to local secrets policy. <br>
Risk: The artifact describes copying generated reports to Google Drive, while the security evidence notes that claimed backup behavior was not supported by the inspected artifact. <br>
Mitigation: Verify any rclone destination and storage behavior in the runtime environment before relying on cloud backup or storing sensitive reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drtony1/target-research) <br>
- [Data sources](references/data-sources.md) <br>
- [Analysis prompts](references/analysis-prompts.md) <br>
- [Report template](references/report-template.md) <br>
- [UniProt](https://www.uniprot.org/) <br>
- [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/) <br>
- [RCSB PDB](https://www.rcsb.org/) <br>
- [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/) <br>
- [KEGG Pathway](https://www.kegg.jp/kegg/pathway.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [HTML report and structured Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local HTML report and a concise scored summary; artifact text also describes optional rclone upload to Google Drive.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
