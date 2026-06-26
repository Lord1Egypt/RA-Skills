## Description: <br>
A skill for performing sequence alignment using the NCBI BLAST API, supporting nucleotide and protein sequence comparison against major biological databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, bioinformatics practitioners, and data analysts use this skill to run bounded NCBI BLAST sequence similarity searches and return alignment results with explicit parameters, assumptions, and caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because the bundle includes executable Python and high-impact behavior requiring human review before installation. <br>
Mitigation: Install only in an expected ClawHub or development environment, review commands before execution, and keep audit logging or confirmation around staff actions. <br>
Risk: The skill sends query sequences to the external NCBI BLAST service and can write output files. <br>
Mitigation: Use non-sensitive sequence inputs, respect NCBI rate and usage guidance, and constrain output paths to the workspace. <br>


## Reference(s): <br>
- [BLAST Documentation](references/blast_docs.md) <br>
- [NCBI BLAST API Guide](references/ncbi_api_guide.md) <br>
- [NCBI BLAST Help](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs) <br>
- [NCBI Usage Policies](https://www.ncbi.nlm.nih.gov/home/about/policies/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, files, shell commands, guidance] <br>
**Output Format:** [Plain text, JSON, CSV, or Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write results to a user-selected output file and may call the external NCBI BLAST service.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
