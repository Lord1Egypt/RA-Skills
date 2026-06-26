## Description: <br>
Search and download visual reference images from Pexels to inspire image or video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vdkroon](https://clawhub.ai/user/vdkroon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and creative agents use this skill to search Pexels for visual references, download candidate images, and use them as style, mood, composition, or palette inputs before generating image or video assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Pexels API key and makes network requests to Pexels. <br>
Mitigation: Install only when the user is comfortable providing PEXELS_API_KEY and allowing Pexels image search and download requests. <br>
Risk: The script removes ref_* files and refs_meta.json from the selected output directory before each search. <br>
Mitigation: Use the default /tmp/visual-refs path or a dedicated empty folder for output. <br>
Risk: Downloaded references can influence generated image or video assets. <br>
Mitigation: Ask the agent to show references first when the user wants to choose which images influence generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vdkroon/visual-references) <br>
- [Pexels API documentation](https://pexels.com/api) <br>
- [Pexels Search API endpoint](https://api.pexels.com/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; downloaded JPG files and refs_meta.json metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEXELS_API_KEY and writes references to /tmp/visual-refs by default.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
