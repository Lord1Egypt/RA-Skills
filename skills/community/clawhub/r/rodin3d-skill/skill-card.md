## Description: <br>
Converts input images or prompt to 3D models using Hyper3D Rodin Gen-2 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WhiteGiven](https://clawhub.ai/user/WhiteGiven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to generate 3D model assets from images or text prompts through the Hyper3D Rodin Gen-2 API. It is useful for product concepts, architectural elements, object reconstruction, and other workflows that need GLB, USDZ, FBX, OBJ, or STL output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed or handled less safely when passed through command-line flags or shared fallback credentials. <br>
Mitigation: Use your own Hyper3D key through HYPER3D_API_KEY, avoid command-line API-key flags where shell history or process listings are a concern, and do not use the shared fallback key. <br>
Risk: Images and text prompts are sent to Hyper3D for third-party processing. <br>
Mitigation: Submit only inputs that are appropriate for Hyper3D processing, and avoid confidential or regulated content unless that processing is acceptable. <br>
Risk: Downloaded model outputs and unpinned dependencies may require review before use in trusted workspaces. <br>
Mitigation: Run the skill in a virtual environment with reviewed, pinned current dependencies and download outputs into a dedicated empty directory before inspecting or importing them elsewhere. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/WhiteGiven/rodin3d-skill) <br>
- [Hyper3D Rodin task endpoint](https://api.hyper3d.com/api/v2/rodin) <br>
- [Hyper3D Rodin status endpoint](https://api.hyper3d.com/api/v2/status) <br>
- [Hyper3D Rodin download endpoint](https://api.hyper3d.com/api/v2/download) <br>
- [Hyper3D API dashboard](https://hyper3d.ai/api-dashboard) <br>
- [Example assets guide](artifact/assets/examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, shell command examples, API request handling, and downloaded 3D model files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Hyper3D API key, sends images or prompts to Hyper3D for generation, polls asynchronous task status, and can download generated model files into a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
