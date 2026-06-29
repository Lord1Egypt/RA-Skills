## Description: <br>
Generates Chinese-language World Cup match talking-point packs for group chat, in-person viewing, social posts, and optional phone-notification context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to prepare Chinese-language World Cup match conversation material, including quick summaries, main talking points, public-discussion themes, copyable chat lines, and social posts. When explicitly requested, it can summarize relevant phone notifications into match-context talking points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification queries may read a broad set of phone notifications when the user has not supplied app, group, or time limits. <br>
Mitigation: Use notification features only with explicit app, group, and time boundaries; omit notification-derived sections when consent or scope is unclear. <br>
Risk: Public web scraping can return blocked, partial, stale, or weakly related source pages. <br>
Mitigation: Cross-check match facts with current public sources and treat blocked or partial scrape results as diagnostics rather than factual evidence. <br>
Risk: The bundled source probe disables TLS certificate verification for HTTP fetches. <br>
Mitigation: Prefer verified browser or web-search results for factual claims, and fix TLS verification before relying on scraped output in sensitive contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/yoooclaw-world-cup-match-talk-scene) <br>
- [30-second match summary template](references/template-30s.md) <br>
- [Main match points template](references/template-main-points.md) <br>
- [Discussion topics template](references/template-discussion.md) <br>
- [Talk lines template](references/template-talk-lines.md) <br>
- [Social post template](references/template-social-post.md) <br>
- [Dongqiudi example source](https://m.dongqiudi.com/article/5943378.html) <br>
- [Zhibo8 example source](https://news.zhibo8.com/zuqiu/2026-06-17/6a320bc0bff75native.htm) <br>
- [Sina Sports example source](https://sports.sina.com.cn/g/2026-06-17/doc-inictaeq5705996.shtml) <br>
- [CCTV Sports example source](https://sports.cctv.com/2026/06/17/VIDEXr99I4FHNoCtSsO6arYx260617.shtml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chinese-language Markdown sections with concise bullets and reusable chat or social-post copy.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include uncertainty labels, public-source summaries, and relevant phone-notification signals when the user requests notification context.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
