## Description: <br>
Formats WeChat draft articles by refining text, adding Markdown structure, and rendering themed HTML output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlgzs](https://clawhub.ai/user/tlgzs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and social media operators use this skill to turn WeChat article drafts into polished Markdown and styled HTML previews with a selected theme. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The formatter runs local Python and writes Markdown and HTML files that may contain sensitive draft content. <br>
Mitigation: Run it only in a trusted workspace and review generated files before sharing the HTML. <br>
Risk: Theme selection can read unintended local files if arbitrary path-like theme names are used. <br>
Mitigation: Use only the listed theme CSS filenames and avoid passing arbitrary paths as themes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tlgzs/wechat-article-formatter-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown draft, generated HTML file, and a short completion message with the selected theme and preview path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates draft_article.md and a timestamped HTML file under output_articles; defaults to theme_orange.css when no theme is specified.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
