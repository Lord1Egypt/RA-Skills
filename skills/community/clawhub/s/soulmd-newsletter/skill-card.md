## Description: <br>
Fetches and displays the latest edition from the SoulMD newsletter RSS feed, including title, date, link, and a brief excerpt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meastt](https://clawhub.ai/user/meastt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or agents use this skill to retrieve the latest SoulMD newsletter edition from the public RSS feed and surface its title, date, link, subscribe URL, and excerpt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Buttondown to fetch the public SoulMD RSS feed and may save a small local last-seen marker. <br>
Mitigation: Install only if outbound access to Buttondown and a local state file under ~/.openclaw are acceptable for the target environment. <br>
Risk: The packaged files appear swapped or malformed, which may prevent the skill from running as intended. <br>
Mitigation: Verify the package contents and file layout before relying on the skill operationally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meastt/soulmd-newsletter) <br>
- [SoulMD newsletter RSS feed](https://buttondown.com/soulmd/rss) <br>
- [SoulMD newsletter subscribe page](https://buttondown.com/soulmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text with labeled newsletter fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a local last-seen marker under ~/.openclaw when checking for new editions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
