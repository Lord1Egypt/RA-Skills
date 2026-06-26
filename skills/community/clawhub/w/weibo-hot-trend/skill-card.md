## Description: <br>
获取微博热搜榜数据，返回热搜标题、热度值和跳转链接，并支持自定义获取条数（默认50条）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geniuslishengbo](https://clawhub.ai/user/geniuslishengbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve current Weibo hot-search topics, heat values, labels, and search links for social trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Weibo to fetch public trending-search data. <br>
Mitigation: Install and run it only where outbound requests to Weibo are acceptable; the security evidence found no local file, credential, or persistent background behavior. <br>
Risk: Frequent requests may trigger Weibo rate limiting or anti-abuse controls. <br>
Mitigation: Use low-frequency runs and follow the artifact guidance to leave at least 30 minutes between requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geniuslishengbo/weibo-hot-trend) <br>
- [Weibo hot search page](https://weibo.com/hot/search) <br>
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Terminal text listing ranked Weibo hot-search titles, heat values, labels, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an optional numeric result limit; defaults to 50 results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
