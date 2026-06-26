## Description: <br>
Imports safety regulations and standards into a safety-review knowledge base with PDF extraction, clause splitting, batch import, and validation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyz9827](https://clawhub.ai/user/cyz9827) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Safety and compliance teams use this skill to add regulations, standards, and policy documents to a safety-review knowledge base, including extracting source text, preparing import manifests, splitting clauses, and validating imported records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imports can overwrite existing records and replace clause data in the local safety-review database. <br>
Mitigation: Back up the database, verify KB_PATH points to the intended file, check existing records before import, and validate imported records afterward. <br>
Risk: The activation scope is broader than the import-only workflow requires. <br>
Mitigation: Invoke the skill only for safety knowledge-base import tasks and review manifests, document-number matches, and clause-splitting results before executing imports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyz9827/safety-kb-import) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON manifests and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes import, extraction, clause-splitting, schema, and validation workflows for a local safety-review knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
