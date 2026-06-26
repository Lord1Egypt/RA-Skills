## Description: <br>
Reads WeChat public-account articles by opening mp.weixin.qq.com links, extracting article text and content images, and producing a combined reading analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HanMingZhao](https://clawhub.ai/user/HanMingZhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to read WeChat articles that need both text extraction and image-aware analysis. It is intended for supplied WeChat article links and writes the extracted article data and images to a chosen local folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens a supplied article page in agent-browser and downloads discovered article images to disk. <br>
Mitigation: Use intended WeChat article links only, avoid arbitrary or untrusted pages, and choose an output folder you are comfortable writing to. <br>
Risk: Extracted article text and downloaded images may include third-party or personal content. <br>
Mitigation: Review generated summaries and downloaded files before sharing, storing, or reusing them outside the original article context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HanMingZhao/wechat-article-full-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, image files, shell commands] <br>
**Output Format:** [Markdown analysis, JSON article metadata, local image files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes article.json, image_urls.txt, and an images directory to the selected output folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
