## Description:

Automates Chaoxing Xuexitong homework workflows, including scanning assignments, resolving homework URLs, fetching question templates, saving or submitting answers, and preparing handwritten-image answer uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallwhiteman](https://clawhub.ai/user/smallwhiteman)

### License/Terms of Use:


## Use Case:

External users operating their own Chaoxing Xuexitong accounts can use this skill to find pending homework, generate editable answer files, temporarily save responses, and explicitly submit completed homework. The handwritten-image pipeline supports rendering text answers into PNGs, uploading them to Chaoxing, and saving HTML image answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs real actions on a Chaoxing homework account, including final submission.

Mitigation: Use only with an account you control, review generated answer files before saving, and require the documented explicit confirmation step before final submission.

Risk: Chaoxing session cookies may be exposed through unvalidated URLs, raw Cookie headers, or plaintext uploads.

Mitigation: Avoid untrusted homework URLs, protect and rotate the cookie after using the handwritten upload path, and prefer a fixed version that validates Chaoxing HTTPS hosts and removes the global raw Cookie header.

Risk: Dependency and update behavior can change runtime behavior if dependencies or remote version checks are not controlled.

Mitigation: Pin dependencies, review the installed version before use, and disable update checks when deterministic execution is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallwhiteman/skills/xuexitong-homework-submit)
- [Publisher profile](https://clawhub.ai/user/smallwhiteman)
- [Chaoxing Xuexitong homework API](https://mooc1-api.chaoxing.com/work/stu-work)
- [Chaoxing notice file upload endpoint](http://notice.chaoxing.com/pc/files/uploadNoticeFile)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files, Markdown, Code]

**Output Format:** [Markdown guidance with shell commands, JSON templates/results, PNG files, uploaded image URLs, and HTML answer snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Chaoxing session cookie and writes local run artifacts such as work.json, answers_text.json, uploads.json, answers_html.json, save_result.json, and pending_scan.json.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
