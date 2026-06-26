## Description: <br>
Analyzes full-body pet images, videos, or media URLs through server-side APIs to identify breed or body type and fur density, then returns a drying temperature and time curve for pet care rather than medical advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, pet care operators, grooming salons, and smart pet-device builders use this skill to convert pet media into drying temperature recommendations, staged time curves, safety notes, and report-history listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet media and report metadata are sent to the Life Emergence/SMYX backend for analysis. <br>
Mitigation: Use only pet media that is acceptable for remote processing, and avoid images or videos containing people, home interiors, location clues, or other private content. <br>
Risk: The skill can silently create or reuse local identity records and store tokens locally. <br>
Mitigation: Run it in a workspace where local identity and token storage is acceptable, and clear the workspace data after use when persistence is not intended. <br>
Risk: The skill can retrieve cloud report history associated with the resolved identity. <br>
Mitigation: Use it only with identities and workspaces where report-history access is expected, especially on shared machines or shared agent environments. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-adaptive-pet-drying-temperature-analysis) <br>
- [Pet drying recommendation API documentation](references/api_doc.md) <br>
- [Shared SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with JSON payloads, report links, shell-command examples, and optional saved output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local media paths, network media URLs, pet-type selection, detail level selection, report-history listing, and optional output-file writing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
