## Description: <br>
Check campsite availability on Recreation.gov for federal campgrounds, including National Park Service, USDA Forest Service, BLM, and other federal sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanrea](https://clawhub.ai/user/seanrea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Campers, travel planners, and agents use this skill to check federal campground availability across one or more Recreation.gov campground IDs, filter by site type and amenities, and return booking status for requested dates. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Campground IDs, dates, and amenity filters are sent to Recreation.gov when checking availability. <br>
Mitigation: Use only the search details needed for the campsite lookup and review Recreation.gov directly before making plans. <br>
Risk: Availability changes quickly and returned results may no longer match the official booking state. <br>
Mitigation: Confirm availability on the official Recreation.gov page before booking or relying on travel plans. <br>


## Reference(s): <br>
- [Recreation.gov Availability API Notes](references/api-notes.md) <br>
- [Recreation.gov](https://www.recreation.gov) <br>
- [RIDB Portal](https://ridb.recreation.gov) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Plain text status summaries or JSON arrays from the CLI, with optional Markdown guidance from the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include campground IDs, campground names, booking URLs, availability counts, status summaries, and optionally individual site ranges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
