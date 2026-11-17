## Description:

Fetch and export WeChat public article content through down.mptext.top API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lniosy](https://clawhub.ai/user/lniosy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflows use this skill to fetch public WeChat article URLs and save the returned article content as HTML, Markdown, plain text, or JSON for testing, analysis, summarization, or batch collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat article URLs are sent to the third-party down.mptext.top API.

Mitigation: Use only public, non-sensitive article links and avoid custom API endpoints unless they are trusted.

Risk: Downloaded article content is stored on disk and may include content the user did not intend to persist.

Mitigation: Choose a dedicated output directory and handle saved files according to the sensitivity of the source article.

Risk: Unsafe or reused output names can overwrite local files.

Mitigation: Keep basename values to simple filenames, review the target output directory, and avoid writing into directories with important existing files.

## Reference(s):

- [API Reference](references/api.md)
- [down.mptext.top public download API](https://down.mptext.top/api/public/v1/download)
- [ClawHub skill page](https://clawhub.ai/lniosy/skills/wechat-article-download-api)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands; downloaded article files may be HTML, Markdown, plain text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local output files named from the selected basename and format extension, and prints one status summary per requested format.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
