## Description:

Find nearby Wikipedia articles based on geographic location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrrqd](https://clawhub.ai/user/jrrqd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover nearby Wikipedia articles for places, landmarks, museums, restaurants, and other points of interest from a current location, named place, or explicit coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise coordinates shared by a user or messaging integration may be sent to Wikipedia APIs during nearby-article searches.

Mitigation: Use a place name or approximate area when exact location sharing is not necessary.

## Reference(s):

- [Wikipedia Nearby](https://en.wikipedia.org/wiki/Special:Nearby)
- [Wikipedia Geosearch API](https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}%7C{lng}&gsradius=10000&gslimit=50&format=json)
- [ClawHub Skill Page](https://clawhub.ai/jrrqd/skills/wikipedia-nearby)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, markdown]

**Output Format:** [Markdown with inline URL and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Wikipedia article titles, distances, brief extracts, and API request examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
