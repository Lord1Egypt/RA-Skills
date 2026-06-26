## Description: <br>
Generate stable or random image placeholder URLs, with optional downloads, using https://picsum.photos for UI mockups, documentation, tests, and demos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hicoldcat](https://clawhub.ai/user/hicoldcat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to create reproducible or random placeholder image URLs for UI mockups, documentation, demos, and tests. It can also guide optional image downloads when a local file is explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded placeholder images come from an external network service and should not be treated as trusted executable content. <br>
Mitigation: Prefer URL-only output; when downloads are requested, save to a project-local or temporary path and treat files as untrusted data. <br>
Risk: Random placeholder URLs can make tests, snapshots, or documentation change unexpectedly. <br>
Mitigation: Use seed-based Picsum URLs when reproducibility matters. <br>


## Reference(s): <br>
- [Picsum Photos](https://picsum.photos) <br>
- [ClawHub skill page](https://clawhub.ai/hicoldcat/random-image-placeholder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown containing generated URLs, selected parameters, optional helper commands, and optional saved file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers deterministic seed URLs for reproducible tests and URL-only output unless downloads are explicitly requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
