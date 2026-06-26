## Description: <br>
Collects Xiaohongshu notes by keyword through Kimi WebBridge browser automation, exports JSON and HTML reports, and can optionally sync collected data to Howtone/Zion for further analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timqin-m](https://clawhub.ai/user/timqin-m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and market researchers use this skill to design focused Xiaohongshu search keywords, collect note and comment data from an authenticated browser session, generate local reports, and optionally send collected records to Howtone/Zion for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses authenticated browser automation and can install or start Kimi WebBridge to control a local browser session. <br>
Mitigation: Review the WebBridge installer separately, use a disposable Xiaohongshu account, keep crawl limits low, and avoid high-frequency repeated runs. <br>
Risk: The skill can store Xiaohongshu cookies and Howtone/Zion sync tokens in local plaintext files. <br>
Mitigation: Keep cookies.json and .zion/credentials.yaml out of source control, avoid passing tokens through shared shell history, and rotate credentials after use. <br>
Risk: Optional sync uploads scraped Xiaohongshu content and images to Howtone/Zion using broad project credentials. <br>
Mitigation: Sync only data the user intends to upload, verify the target project credentials before syncing, and review generated JSON files before transfer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/timqin-m/zion-xhs-catch-skill) <br>
- [Kimi WebBridge installer](https://cdn.kimi.com/webbridge/install.sh) <br>
- [Kimi WebBridge Chrome extension](https://chromewebstore.google.com/detail/kimi-webbridge/fldmhceldgbpfpkbgopacenieobmligc) <br>
- [Xiaohongshu website](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated runs produce JSON data files and a local HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local cookies, Howtone/Zion credentials, scraped Xiaohongshu content, image URLs, and optional uploaded image assets.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
