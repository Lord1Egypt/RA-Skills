## Description:

Check campsite availability on recreation.gov for federal campgrounds, including National Parks, USFS, and BLM sites, using campground IDs from ridb-search or recreation.gov URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanrea](https://clawhub.ai/user/seanrea)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to have an agent check federal campground availability on Recreation.gov for specified campground IDs and dates, including filters for site type, amenities, and consecutive nights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Availability changes constantly and may be stale by booking time.

Mitigation: Verify availability on Recreation.gov before booking.

Risk: Bulk searches or amenity filters can make extra Recreation.gov API calls.

Mitigation: Use reasonable query volume and apply amenity filters selectively.

Risk: The skill relies on public Recreation.gov endpoints that may change.

Mitigation: Review API errors and confirm important results in the Recreation.gov site before acting on them.

## Reference(s):

- [Recreation.gov Availability API Notes](references/api-notes.md)
- [Recreation.gov](https://www.recreation.gov)
- [RIDB Portal](https://ridb.recreation.gov)
- [ClawHub Skill Page](https://clawhub.ai/seanrea/skills/recgov-availability)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-text status summaries or JSON, with shell commands for running the checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Recreation.gov booking URLs and campsite availability ranges; amenity filters may trigger extra per-site API calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
