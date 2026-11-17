## Description:

Shopping memory that holds lists, purchases, prices, and "last time I bought X" so agents can help with errands, restocks, and budget questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain shopping lists, recall recent purchases, compare last-known prices, and plan restocks for household or business errands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping lists, purchase history, store names, prices, and restock notes are sent to BlueColumn/Supabase-hosted services.

Mitigation: Avoid recording sensitive household or business details unless the user has reviewed the provider's retention and deletion policies and is comfortable with remote storage.

Risk: The skill requires a BlueColumn API key for authenticated API calls.

Mitigation: Store the API key in the BLUECOLUMN_API_KEY environment variable and avoid placing credentials directly in prompts, logs, or shared files.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends shopping notes, purchase history, store names, prices, and restock notes to BlueColumn/Supabase-hosted services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
