## Description: <br>
Web Reader fetches articles and videos from supported web platforms, archives them locally, and supports follow-up analysis, summaries, and derived work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-focused agent users use this skill to fetch web articles, documents, and videos, archive them by category, and then summarize, analyze, compare, or derive follow-up material from the saved content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch URLs through scraping, headless browser, anti-detection browser, and video download tools. <br>
Mitigation: Review target URLs before execution, use only content you have permission to access, and prefer explicit confirmation before authenticated or anti-detection fetches. <br>
Risk: The skill can use logged-in browser sessions or cookies for restricted content. <br>
Mitigation: Use a dedicated browser profile when cookies are needed and avoid private or premium content unless you are authorized to archive it. <br>
Risk: The skill saves downloaded pages, images, and videos to local archive directories. <br>
Mitigation: Set the archive directory deliberately and review saved files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub Web Reader Release](https://clawhub.ai/alexxxiong/web-reader) <br>
- [README](artifact/README.md) <br>
- [Platform Strategies](artifact/references/platforms.md) <br>
- [Adding a New Platform](artifact/references/extending.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown archives, downloaded media files, optional JSON command output, and concise text summaries or analyses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local article, image, and video archives under the selected output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
