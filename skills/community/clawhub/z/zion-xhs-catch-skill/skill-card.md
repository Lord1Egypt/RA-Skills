## Description:

Xiaohongshu note collection tool that helps agents search by keyword, collect note text, authors, engagement counts, image URLs, and top-level comments, then output raw JSON and an HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timqin-m](https://clawhub.ai/user/timqin-m)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market researchers use this skill to guide keyword design, collect Xiaohongshu posts and comments through a logged-in browser, generate local reports, and optionally sync collected data to Howtone/Zion for further analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in browser automation can expose a Xiaohongshu account to platform enforcement or unwanted account activity.

Mitigation: Use an isolated browser profile and a non-critical account, keep collection volumes low, and review each run before execution.

Risk: The skill may run a remote Kimi WebBridge installer pipeline before controlling the local browser.

Mitigation: Independently inspect and trust the installer source before running it, or install WebBridge through a separately verified process.

Risk: Howtone/Zion sync can upload scraped text, comments, image content, and credentials-related data paths outside the local workspace.

Mitigation: Do not sync sensitive or private scraped data, review the destination project configuration, and remove plaintext or sibling credential fallback behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timqin-m/skills/zion-xhs-catch-skill)
- [Kimi WebBridge installer for macOS/Linux](https://cdn.kimi.com/webbridge/install.sh)
- [Kimi WebBridge installer for Windows](https://cdn.kimi.com/webbridge/install.ps1)
- [Kimi WebBridge Chrome extension](https://chromewebstore.google.com/detail/kimi-webbridge/fldmhceldgbpfpkbgopacenieobmligc)
- [Xiaohongshu website](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with shell commands; generated JSON data files and a local HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include output/<keyword>_<YYYYMMDD>.json and output/index.html; optional sync uploads collected records and up to three images per note to Howtone/Zion.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
