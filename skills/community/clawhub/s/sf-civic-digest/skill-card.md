## Description:

SF Civic Digest helps agents collect San Francisco government, civic, and local journalism data and synthesize district, neighborhood, street, or topic-specific civic digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sgillen](https://clawhub.ai/user/sgillen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and civic researchers use this skill to monitor San Francisco public meetings, planning notices, permits, 311 trends, lobbying activity, local journalism, and public actions. Agents use the collected data to produce daily or weekly civic digests and answer neighborhood-specific questions.

### Deployment Geography for Use:

United States (San Francisco, California civic data)

## Known Risks and Mitigations:

Risk: The skill reads a local civic preference profile that may contain exact addresses, watched locations, or sensitive people-of-interest notes.

Mitigation: Keep USER.md limited to necessary civic context and avoid storing sensitive personal details unless they are required for the digest.

Risk: The skill fetches many public web sources and may create local JSON archives or state files.

Mitigation: Run it without elevated privileges and review generated local files before sharing reports or archives.

Risk: Dependency installation can affect the host environment.

Mitigation: Install dependencies in a pinned or isolated environment before running the scripts.

## Reference(s):

- [SF Residential Build Timelines Reference](references/sf-build-timelines.md)
- [SF Supervisorial Districts Reference](references/sf-districts.md)
- [SF Legistar RSS Feed](https://sfgov.legistar.com/Feed.ashx?M=C&ID=17442&GUID=EEE85B7C-1A1C-4A56-873E-355A0A0DE5C3&Mode=All&Format=rss)
- [SF Open Data API Pattern](https://data.sfgov.org/resource/{id}.json?$where=supervisor_district=)
- [SF Assessor-Recorder Search](https://recorder.sfgov.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown narrative reports with supporting JSON data outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts require absolute paths and may keep local JSON archives or state files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
