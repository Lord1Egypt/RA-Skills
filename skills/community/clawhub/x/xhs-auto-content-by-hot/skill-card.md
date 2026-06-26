## Description: <br>
Automatically generates Xiaohongshu content by selecting a Baidu hot topic, drafting a short post, calling Seedream-4.5 for images, and saving a complete content package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18923236683](https://clawhub.ai/user/18923236683) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and social-media operators use this skill to turn Baidu trending topics or a supplied topic into Xiaohongshu-ready posts with titles, body copy, generated images, and saved output files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to store a real image API key in generate.py, which can expose credentials. <br>
Mitigation: Use a temporary, limited-scope key supplied through an environment variable or secret store, and rotate any key already written into the source file. <br>
Risk: The skill makes network calls to Baidu and Volcengine services during execution. <br>
Mitigation: Review service use, data handling expectations, and network access before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18923236683/xhs-auto-content-by-hot) <br>
- [Publisher profile](https://clawhub.ai/user/18923236683) <br>
- [Baidu hot topic API endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime) <br>
- [Volcengine image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown-style agent response with shell commands, generated image files, JSON files, and text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Xiaohongshu post text, image paths, xhs_content.json, selected_topic.txt, generated_images.json, and generated PNG images.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
