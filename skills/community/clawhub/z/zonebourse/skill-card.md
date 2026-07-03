## Description: <br>
Fetches ZoneBourse stock slugs, categorized news article links, and article metadata and content using local Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredguile](https://clawhub.ai/user/fredguile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-analysis users can use this skill to look up ZoneBourse stock identifiers, retrieve recent news links by category, and extract article dates, titles, content, and paywall status for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to export and persist ZoneBourse session cookies in a local plaintext file. <br>
Mitigation: Treat cookies.txt like a password: do not share it, commit it, back it up to shared storage, or leave it readable by other users; rotate or log out the ZoneBourse session if the file may have been exposed. <br>


## Reference(s): <br>
- [Zonebourse skill page](https://clawhub.ai/fredguile/zonebourse) <br>
- [Publisher profile](https://clawhub.ai/user/fredguile) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts return stock slugs, categorized article URLs, and article fields including date, title, content, paywall status, URL, and errors when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
