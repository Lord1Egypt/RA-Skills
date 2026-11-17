## Description:

Look up concert setlists and live-music history via setlist.fm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Music fans and researchers use the skill to find setlists and concert histories by artist, venue, date, city, or tour, and to retrieve recorded song lists for a show.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attendance tools can change the user's setlist.fm account despite the skill's read-only description.

Mitigation: Use lookup tools by default; invoke an attendance change only when the user explicitly requests that specific change. Disable attendance tools or browser access when they are unnecessary.

Risk: The skill requires a setlist.fm API key, and the external server's credential handling and runtime safeguards are not verified by the bundled documentation.

Mitigation: Keep the API key private and use a reviewed, pinned server version.

## Reference(s):

- [setlist-mcp on npm](https://www.npmjs.com/package/setlist-mcp)
- [setlist-mcp repository (linked by the skill documentation)](https://github.com/chrischall/setlist-mcp)
- [setlist.fm API key information](https://www.setlist.fm/settings/api)
- [setlist.fm API terms](https://www.setlist.fm/help/api-terms)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise concert and setlist information with followable setlist.fm source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include artist, venue, date, tour, songs, and source links; some concert records may have no songs logged.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
