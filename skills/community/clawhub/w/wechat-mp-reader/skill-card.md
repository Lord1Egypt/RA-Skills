## Description: <br>
Read WeChat official account articles. Use the built-in browser tool to open the page and extract body text. Always append ?scene=1 to the URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernylinville](https://clawhub.ai/user/bernylinville) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to read user-provided WeChat official account article URLs through an agent browser and return the article body text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill rewrites WeChat article URLs and extracts page text through a browser helper. <br>
Mitigation: Use it only for articles you are allowed to access and review the normalized URL before extraction. <br>
Risk: The source may be installed from a mutable main-branch URL. <br>
Mitigation: Prefer a reviewed or pinned install source before operational use. <br>
Risk: Bulk or restricted content extraction may violate site or content access expectations. <br>
Mitigation: Avoid bulk scraping and restricted content; use the skill for user-provided articles with appropriate access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bernylinville/wechat-mp-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with browser command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns extracted article body text from the loaded page; no local files are produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
