## Description:

Structure-activity relationship analysis workflows using SciMiner's MCS-based and scaffold-based SAR APIs for file or inline table inputs, plus an AlphaFold3-based binding-mode prediction workflow for target-aware SAR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and scientific analysts use this skill to run SAR workflows over molecular structure files or inline tables, including MCS-based clustering, scaffold-based activity summaries, and target-aware binding-mode prediction when target context is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled RCSB helper can make broad outbound HTTP requests and optionally write raw responses to caller-chosen paths.

Mitigation: Run the skill in a sandboxed environment, constrain requests to approved SciMiner and RCSB endpoints, and restrict raw-output writes to a safe output directory.

Risk: Molecular structures or activity tables may be sent to external analysis services during SAR and binding-mode workflows.

Mitigation: Use only datasets approved for external processing and avoid sensitive datasets unless endpoint and data-handling controls are in place.

Risk: The skill depends on a runtime SCIMINER_API_KEY for authenticated SciMiner requests.

Mitigation: Inject the key through the gateway at runtime and do not request, print, persist, or write the credential to disk.

## Reference(s):

- [ClawHub SAR Analysis skill page](https://clawhub.ai/sciminer/skills/sar-analysis)
- [SciMiner tool API Markdown docs](https://sciminer.tech/tool_api_files/)
- [RCSB PDB Data API](https://data.rcsb.org/rest/v1)
- [RCSB PDB Search API](https://search.rcsb.org/rcsbsearch/v2)
- [RCSB PDB FASTA downloads](https://www.rcsb.org)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, API Calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries with SciMiner task history URLs and compact JSON result details when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an injected SCIMINER_API_KEY; may upload user-provided structure files and returns history_url links for successful SciMiner tasks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
