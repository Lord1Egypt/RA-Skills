## Description: <br>
Parse, validate, compare, sort, bump, and filter semantic versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to validate semantic-version strings, compare and sort releases, choose the latest matching release, and propose version bumps for SemVer-based projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper is scoped to Semantic Versioning and may not match calendar, date-based, or custom release schemes. <br>
Mitigation: Use it for SemVer-based projects only, and review results manually when a project uses a different versioning policy. <br>
Risk: The skill runs a bundled local Python script, which may require source review in strict environments. <br>
Mitigation: Review the bundled script and publisher provenance before deployment where local executable code requires approval. <br>


## Reference(s): <br>
- [Semver Manager on ClawHub](https://clawhub.ai/charlie-morrison/semver-manager) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown responses showing validation results, comparisons, sorted versions, filtered matches, latest versions, or bumped version strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python utility runs locally and accepts SemVer strings, comparison constraints, bump parts, optional prerelease tags, and output format selection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
