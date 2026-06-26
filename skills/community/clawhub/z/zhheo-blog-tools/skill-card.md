## Description: <br>
Chats with Zhang Hong Heo's Hongmo AI assistant and searches the Zhang Hong Heo blog for articles, popular posts, tags, categories, equipment, and project pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhheo](https://clawhub.ai/user/zhheo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to chat with the blog's Hongmo AI assistant, search Zhang Hong Heo blog articles, discover popular posts, browse tags and categories, and retrieve equipment or project information from the public blog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat and fallback search send the user's prompt to a third-party public blog chatbot. <br>
Mitigation: Use the skill only when sharing the prompt with blog.zhheo.com is acceptable, and avoid entering private, sensitive, or confidential information. <br>
Risk: Returned chatbot text and reference links come from third-party blog content and may be incomplete, outdated, or misleading. <br>
Mitigation: Review returned links and claims before relying on them, and treat chatbot output as unverified third-party content. <br>
Risk: The skill depends on public blog pages and JSON endpoints that can change or become unavailable. <br>
Mitigation: When results are missing or stale, retry against the current blog pages or clearly state that the requested blog data could not be retrieved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhheo/skills/zhheo-blog-tools) <br>
- [Zhang Hong Heo Blog](https://blog.zhheo.com/) <br>
- [Article Index JSON](https://blog.zhheo.com/zhheo/post_info.json) <br>
- [RSS Feed](https://blog.zhheo.com/rss.xml) <br>
- [Tags Page](https://blog.zhheo.com/tags/) <br>
- [Equipment Page](https://blog.zhheo.com/equipment/) <br>
- [Projects Category](https://blog.zhheo.com/categories/我的项目/) <br>
- [Tags API](https://blog.zhheo.com/api/tags.json) <br>
- [Categories API](https://blog.zhheo.com/api/categories.json) <br>
- [Daily Popular Posts API](https://api.zhheo.com/HeoBlogAPI/umami/hot.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown with article links, chatbot responses, reference links, and JSON-backed result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open blog.zhheo.com, call public JSON endpoints, send the user's chat or search prompt to the blog chatbot, and return AI-generated text and links from that site.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
