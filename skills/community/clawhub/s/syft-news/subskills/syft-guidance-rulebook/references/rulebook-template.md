# Rulebook Template

Use this if the workspace does not already have a persistent rulebook file.

## Suggested Markdown structure

```md
# User Guidance Rulebook

## Metadata

- user:
- updated_at:

## Active Rules

### RULE-001

- name:
- scope:
- kind:
- priority:
- status: active
- confirmed_at:
- source:
- rationale:

Guidance:

...

## Disabled Rules

## Pending Confirmations
```

## Confirmation workflow

Before moving anything into `Active Rules`, show the user:

- your concise summary of what you think they mean
- the proposed canonical wording
- the chosen scope and priority

Then wait for confirmation.

## Writing rule text

The stored guidance should:

- be more stable than the user's exact sentence
- be specific enough to influence output
- avoid baking in one single day's examples
- avoid hidden assumptions the user did not approve
