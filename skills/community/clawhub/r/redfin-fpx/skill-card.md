## Description:

Query redfin.com (US real-estate portal) from a shell with the fpx CLI (@fetchproxy/cli) instead of running the redfin-mcp server — resolve locations/addresses, search for-sale listings, read property detail (price, beds/baths, price history, tax history), market trends, comparable rentals, climate risk, photos, and (signed-in) saved homes and saved searches, via one-shot calls through a signed-in browser tab. Use when you want Redfin data without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the skill to query Redfin property, market, history, rental, climate-risk, and photo data from shell scripts without running a separate MCP server. Signed-in users can also retrieve their saved homes and saved searches.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The saved-homes workflow may leave private account data in a predictable temporary file.

Mitigation: Write saved-home data to a user-private file with restrictive permissions and remove it when processing is complete.

## Reference(s):

- [Redfin stingray endpoint guide](references/stingray-endpoints.md)
- [Redfin](https://www.redfin.com)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [fetchproxy extension information](https://github.com/chrischall/fetchproxy#extension)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redfin JSON responses use an envelope that should be checked for a successful result before relying on its payload.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
