## Description: <br>
贴吧帖子爬虫 - 从百度贴吧抓取帖子内容并导出为 Markdown（支持图片下载、楼中楼解析）。Tieba thread crawler - crawl Tieba threads to Markdown with images and sub-posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuxiaoji](https://clawhub.ai/user/fuxiaoji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and command-line users use this skill to crawl public Baidu Tieba threads by URL or thread ID and export posts, sub-posts, and optional images into a local Markdown archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool contacts Baidu Tieba and downloads public thread content and optional images to local storage. <br>
Mitigation: Run it only for content you are comfortable fetching locally, choose the output directory deliberately, and use --no-images when image downloads are unnecessary. <br>
Risk: Large threads or image-heavy threads can consume significant disk space. <br>
Mitigation: Monitor the selected output directory and use --no-images or a controlled output location for large crawls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuxiaoji/tieba-spider) <br>
- [Baidu Tieba thread URL pattern](https://tieba.baidu.com/p/7487460366) <br>
- [Baidu Tieba mobile API endpoint](http://c.tieba.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; the tool writes a Markdown file and optional image files to a local output directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. Accepts a Tieba thread URL or numeric thread ID, optional output directory, image download toggle, sub-post toggle, and request delay.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
