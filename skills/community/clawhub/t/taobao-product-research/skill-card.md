## Description: <br>
Taobao Product Research collects Taobao product information such as images, titles, prices, sales counts, review counts, shop names, and product links, then generates image-rich Excel reports for product research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redcreen](https://clawhub.ai/user/redcreen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research Taobao products by keyword and price range, collect market and competitor data, and produce local Excel reports with product images and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a browser profile that can persist Taobao login state locally. <br>
Mitigation: Use a dedicated browser profile and delete the browser_data directory when the saved session is no longer needed. <br>
Risk: The skill writes reports, images, and debug screenshots to a local output directory. <br>
Mitigation: Choose a dedicated output directory and avoid search keywords or paths that could create confusing or unintended filenames. <br>
Risk: The skill depends on npm packages and browser automation to collect data from Taobao. <br>
Mitigation: Inspect dependencies in sensitive environments and keep collection volumes modest to reduce operational and compliance risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redcreen/taobao-product-research) <br>
- [Publisher profile](https://clawhub.ai/user/redcreen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with command-line examples; generated local Excel, image, and debug screenshot files when the script runs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime script may create a browser_data directory that persists Taobao login state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
