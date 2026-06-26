## Description: <br>
Fetch handwritten notes, sketches, and drawings from a reMarkable tablet via Cloud API (rmapi), then process content by refining artwork with AI image generation, extracting handwritten text to memory or journal files, or using sketches as input for other workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolmanns](https://clawhub.ai/user/coolmanns) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to bring selected reMarkable tablet notes, sketches, drawings, and journal entries into project workflows for interpretation, refinement, documentation, or memory capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can access and download notes or sketches from reMarkable Cloud once authenticated. <br>
Mitigation: Use a dedicated sharing folder, explicit share tag, or starred-item workflow, and preview matched files before downloading. <br>
Risk: Extracted handwriting may contain private or sensitive content before it is saved to memory or project files. <br>
Mitigation: Review interpreted handwriting before saving it to memory, journals, or project documentation. <br>
Risk: The rmapi token in ~/.rmapi enables future automatic access. <br>
Mitigation: Protect or remove ~/.rmapi when automatic access is no longer intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolmanns/remarkable-tablet) <br>
- [reMarkable desktop connection](https://my.remarkable.com/connect/desktop) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide fetching PDF or PNG tablet exports, interpreting handwriting, saving notes, or refining sketches with image generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
