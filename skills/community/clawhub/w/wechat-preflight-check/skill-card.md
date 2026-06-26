## Description: <br>
Checks Markdown articles before publication to a WeChat Official Account for required metadata, cover assets, image paths, unsupported wiki image links, and unlabeled fenced code blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, editors, and agents use this skill to run a local preflight check on Markdown articles before publishing them to a WeChat Official Account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checker reads the Markdown file provided by the caller and checks whether referenced local image paths exist. <br>
Mitigation: Run it only on Markdown files intended for inspection and avoid passing sensitive or unrelated files. <br>
Risk: HTTP and HTTPS cover URLs are accepted by pattern rather than fetched, so remote availability is not verified. <br>
Mitigation: Manually verify remote cover URLs before publication when availability matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chaoyang78/wechat-preflight-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text checklist results with ERROR/WARN lines and pass/fail status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads one Markdown file path and checks referenced local image paths; URL covers are accepted by pattern and not fetched.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
