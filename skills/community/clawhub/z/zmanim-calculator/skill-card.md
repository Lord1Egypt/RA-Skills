## Description: <br>
Calculates halachic times (zmanim), Shabbos times, candle lighting, Daf Yomi, weekly parsha, and Jewish calendar dates for a given location and date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeperl](https://clawhub.ai/user/abeperl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Jewish calendar questions, including zmanim, Shabbos and candle-lighting times, Daf Yomi, parsha, and upcoming Yom Tov dates for a specified location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location inputs or coordinates may be sent to Hebcal when calculations run. <br>
Mitigation: Use explicit city or coordinate inputs intentionally and avoid sharing sensitive location data when privacy matters. <br>
Risk: Important halachic times may vary by local custom, calculation method, or edge-case geography. <br>
Mitigation: Verify important zmanim with a trusted local source before relying on them for observance. <br>
Risk: Some documented IP, ZIP, or positional examples may not work as described. <br>
Mitigation: Prefer explicit city names or latitude and longitude inputs and test commands before operational use. <br>


## Reference(s): <br>
- [Hebcal API](https://www.hebcal.com/hebcal) <br>
- [GeoNames Search API](http://api.geonames.org/searchJSON) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, configuration, guidance] <br>
**Output Format:** [Plain text or JSON command output, with Markdown usage guidance and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external location and calendar APIs when calculations run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
