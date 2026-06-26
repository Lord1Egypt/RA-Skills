## Description: <br>
Generates Amap search links for place names provided by the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaohong-test](https://clawhub.ai/user/zhaohong-test) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask for locations, addresses, or directions and receive direct Amap search links for the requested places. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opening a generated Amap link sends the searched place text to Amap. <br>
Mitigation: Review place names before opening links and avoid using sensitive location text in search queries. <br>


## Reference(s): <br>
- [Amap search URL template](https://ditu.amap.com/search?query={keyword}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text containing generated Amap search links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated links include the extracted place query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
