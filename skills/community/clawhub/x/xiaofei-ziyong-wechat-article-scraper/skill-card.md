## Description: <br>
微信公众号文章抓取工具，从 mp.weixin.qq.com 抓取公开文章的文字、图片和视频预览，解析内容块顺序，下载图片，并准备按原顺序写入飞书知识库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengzi53](https://clawhub.ai/user/mengzi53) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations users can use this skill to extract authorized public WeChat article content, produce structured text or Markdown, download article images, and prepare Feishu knowledge-base imports. Users should confirm they are allowed to scrape and reuse each article before running it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags anti-bot browser evasion and weak URL scoping for WeChat scraping. <br>
Mitigation: Run only against trusted, authorized mp.weixin.qq.com article links, start with --dry-run, and review the skill before installation or use. <br>
Risk: Downloaded article images may contain sensitive or copyrighted material and are cached locally. <br>
Mitigation: Use a controlled cache directory, confirm reuse rights, and delete the image cache after the import or review is complete. <br>
Risk: Feishu document operations can create or overwrite content, and imported images may require manual repositioning because media is appended at the end. <br>
Mitigation: Verify the Feishu destination before writing, inspect dry-run or JSON output first, and manually adjust image placement in the Feishu editor. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mengzi53/xiaofei-ziyong-wechat-article-scraper) <br>
- [WeChat public article domain](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON with local image files and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Google Chrome; scrape_and_import.py supports --dry-run, --cache-dir, and --output-json.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
