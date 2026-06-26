## Description: <br>
Deprecated SciVerse Agent Tools gives OpenClaw agents SciVerse academic-paper metadata search, semantic chunk retrieval, and byte-range content reading; new installs should migrate to academic-retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciverse](https://clawhub.ai/user/sciverse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this deprecated skill to retrieve academic paper metadata, RAG-ready semantic chunks, and source text ranges from SciVerse. New deployments should migrate to academic-retrieval under the same publisher. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends paper searches, document IDs, requested byte ranges, and the configured SciVerse API token to SciVerse endpoints. <br>
Mitigation: Install only when that data sharing is acceptable, keep SCIVERSE_API_TOKEN scoped and protected, and use trusted SciVerse API endpoints. <br>
Risk: This slug is deprecated and the 0.1.x line will not receive new features or fixes. <br>
Mitigation: Prefer migrating new deployments to academic-retrieval as the skill documentation and security guidance recommend. <br>


## Reference(s): <br>
- [SciVerse homepage](https://sciverse.space) <br>
- [ClawHub skill page](https://clawhub.ai/sciverse/sciverse-agent-tools) <br>
- [Academic retrieval migration target](https://clawhub.ai/academic-retrieval) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, configuration, guidance] <br>
**Output Format:** [JSON responses containing paper metadata, semantic chunks, and UTF-8 text ranges, plus Markdown guidance for installation, configuration, and migration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCIVERSE_API_TOKEN and can optionally use SCIVERSE_BASE_URL for SciVerse API endpoints.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
