## Description:

Fetches current public job listings from a selected Acxiom, LiveRamp, or Magnite careers board and reports source and coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epistemedeus](https://clawhub.ai/user/epistemedeus)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and recruiting teams use this skill to collect public vacancies from one supported employer board and check whether the returned listing is complete, partial, or unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live public career sites can fail or return an incomplete listing.

Mitigation: Check the reported source and coverage before treating the rows as a complete set of vacancies.

Risk: The skill makes live requests to named careers sites and can write a caller-specified output file.

Mitigation: Run it only when those site requests and the selected output location are acceptable.

Risk: Running the bundled recipe directly reads multiple boards instead of the selected one.

Mitigation: Use the installed one-board command unless multi-board collection is intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/epistemedeus/skills/public-careers-board)
- [Ashby public job posting API](https://developers.ashbyhq.com/docs/public-job-posting-api)
- [Magnite careers page](https://www.magnite.com/careers/)
- [Bundled recipe source pins](references/pins.json)
- [Magnite source pins](references/source-pins.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON observation with job rows and coverage; agent-readable summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rows include title, location, job URL, source, and fetch time; coverage distinguishes complete, partial, empty, and failed reads. Requires Node.js 22.22.2 or newer.]

## Skill Version(s):

0.1.3 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
