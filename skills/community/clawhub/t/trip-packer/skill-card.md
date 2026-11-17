## Description:

Trip Packer helps users plan travel itineraries, produce schema-valid trip JSON, and use the trip-packer CLI to build standalone HTML map pages with optional share images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucasytoo](https://clawhub.ai/user/ucasytoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to turn destination, hotel, route, and transport details into validated itinerary data and shareable map outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run unpinned npx trip-packer commands, so normal use can execute changing external npm code.

Mitigation: Review the skill before sensitive deployments and prefer a reviewed, pinned, lockfile-managed trip-packer installation before running validation or build commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucasytoo/skills/trip-packer)
- [Trip Packer Planning Guide](planning-guide.md)
- [trip-packer JSON Schema reference](references/schema-reference.md)
- [Sample itinerary JSON](references/sample-itinerary.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON data and shell command examples; generated artifacts are itinerary JSON files, standalone HTML map pages, and optional PNG share images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and invokes the trip-packer CLI; supports linux, darwin, and win32 environments according to ClawHub metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
