## Description: <br>
Social media cover image generator that creates HTML pages from title content and converts them to PNG images for platforms such as Xiaohongshu, WeChat Official Accounts, Weibo, Douyin, Bilibili, Zhihu, Twitter/X, Instagram, and LinkedIn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and marketing teams use this skill to generate platform-sized social media cover artwork from a title, export it as HTML, and convert it to PNG with a local Node/Puppeteer workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The conversion workflow launches a local headless Chromium browser and disables the browser sandbox. <br>
Mitigation: Run it only in trusted working directories, review generated HTML before conversion, and preserve browser sandboxing in higher-security environments when possible. <br>
Risk: The generated HTML loads snapdom from unpkg during rendering. <br>
Mitigation: Pin or vendor the snapdom dependency for controlled environments and avoid using the workflow when external network loading is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/social-media-cover-generator) <br>
- [Publisher profile](https://clawhub.ai/user/openlark) <br>
- [snapdom browser library](https://unpkg.com/@zumer/snapdom/dist/snapdom.js) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with HTML, CSS, shell commands, and generated HTML/PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates platform-specific cover dimensions and uses a local Puppeteer conversion script that expects an HTML element with id="cover".] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
