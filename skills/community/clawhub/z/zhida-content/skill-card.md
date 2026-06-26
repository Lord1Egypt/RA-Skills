## Description: <br>
Searches Zhihu questions and hot-list data, then summarizes topic heat, answer competition, and content opportunities for Chinese-language creators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and agent users use this skill to search Zhihu topics, review hot questions, rank content opportunities, and generate topic suggestions from public Zhihu data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Zhihu when the local Python script runs. <br>
Mitigation: Avoid sensitive queries and use the skill only where sending those terms to Zhihu is acceptable. <br>
Risk: Zhihu endpoints may fail or be unavailable in some regions, and results may be incomplete. <br>
Mitigation: Treat empty or partial results as operational limits and validate important content decisions against Zhihu directly. <br>
Risk: Static review found no malicious behavior, but VirusTotal was still pending in the security evidence. <br>
Mitigation: Review and scan the artifact before deployment in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/zhida-content) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal text summaries or JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include Zhihu question links, follower and answer counts, estimated heat, opportunity labels, and content suggestions.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
