## Description:

小红书笔记批量下载。通过已登录 Chrome 的 DevTools Protocol 自动化下载小红书笔记（图片+文字）到本地。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilixiong](https://clawhub.ai/user/weilixiong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and run a Python-based workflow that downloads Xiaohongshu note text and images from a logged-in Chrome browser session into local folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Chrome tab through CDP, which grants automation access to the browser session.

Mitigation: Use a dedicated Chrome profile for Xiaohongshu, keep remote debugging bound to localhost, and close unrelated sensitive tabs before running the script.

Risk: Note folder names are derived from note titles and can write outside the intended save folder if path components are not contained.

Mitigation: Sanitize note folder names and verify every output path stays under SAVE_DIR before creating folders or writing files.

Risk: Large batch downloads can fail or be rate-limited during repeated page navigation and media requests.

Mitigation: Run downloads in smaller batches and increase waits or scroll counts only after checking that the target account content is loading as expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilixiong/skills/xhs-download)
- [Xiaohongshu website](https://www.xiaohongshu.com/)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated script downloads note text and images into one folder per note when executed by the user.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
