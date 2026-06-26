## Description: <br>
A skill to lookup video game information, prices, compatibility, and duration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanheral](https://clawhub.ai/user/ivanheral) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to look up video game details, store prices, Steam Deck or Linux compatibility, player activity, news, reviews, achievements, and playtime guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game names and Steam app IDs queried through the skill are sent to public gaming services. <br>
Mitigation: Use public game titles or app IDs, and avoid submitting sensitive internal project names or unreleased game information. <br>
Risk: Recent API responses may be cached locally for about 24 hours. <br>
Mitigation: Clear the skill cache when cached lookup results should not persist on the local machine. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivanheral/videogames) <br>
- [Steam](https://store.steampowered.com/) <br>
- [CheapShark](https://www.cheapshark.com/) <br>
- [ProtonDB](https://www.protondb.com/) <br>
- [HowLongToBeat](https://howlongtobeat.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with command examples and external links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include game names, Steam app IDs, prices, compatibility summaries, news, reviews, achievements, playtime links, and locally cached API results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
