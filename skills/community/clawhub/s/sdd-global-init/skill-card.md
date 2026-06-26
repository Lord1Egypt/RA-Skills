## Description: <br>
Initializes an SDD workspace by selecting a working directory, scanning the codebase, and generating global documentation for project overview, architecture, technical constraints, existing features, and indexes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize a structured SDD knowledge base for a selected workspace. It scans project files, asks the user to confirm an outline, then writes Chinese global spec documents and optional diagram assets under spec/global. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans a selected workspace and may read unrelated private project information if the wrong directory is chosen. <br>
Mitigation: Select only the intended workspace and review the generated outline before confirming document generation. <br>
Risk: Project details may be included in prompts passed to /gen-image for diagram generation. <br>
Mitigation: Avoid running image generation on sensitive repositories unless sharing project-derived diagram prompts is acceptable. <br>
Risk: Generated SDD documents may contain incorrect or incomplete summaries of the codebase. <br>
Mitigation: Review the proposed outline and generated documents before using them for planning or implementation decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mahingbun-dev/sdd-global-init) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Chinese status text, Markdown spec files, JSON workspace configuration, and generated PNG diagram files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates spec/global documentation after user outline confirmation and may call /gen-image for diagram generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
