## Description: <br>
Fetches current Weibo hot-search topics across realtime, lifestyle, entertainment, and social-event categories and returns structured trend data. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[miaoxingjun](https://clawhub.ai/user/miaoxingjun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts can use this skill to retrieve public Weibo trend lists for monitoring current topics, entertainment trends, social events, and lifestyle discussion themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom URLs cause the local browser to visit a user-specified page. <br>
Mitigation: Prefer the built-in Weibo category options and use custom URLs only when that destination is intentional. <br>
Risk: High-frequency scraping may violate site terms, trigger blocking, or conflict with local policy. <br>
Mitigation: Keep scraping frequency reasonable and confirm use complies with Weibo's terms and applicable policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miaoxingjun/weiborealhot) <br>
- [Weibo Hot Search](https://s.weibo.com/top/summary) <br>
- [Selenium Documentation](https://www.selenium.dev/documentation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON data, shell commands, guidance] <br>
**Output Format:** [JSON object or human-readable text listing Weibo hot-search titles and heat values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns status code, message, and a list of title and hot-value pairs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
