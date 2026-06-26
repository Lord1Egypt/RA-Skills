# Onboarding Data Schema

## File Location

`data/user-settings.json`

## Schema Definition

```json
{
  "onboarding": {
    "completed": "boolean",
    "language_set": "boolean",
    "steps_completed": ["string"]
  }
}
```

## Onboarding Steps

| Step ID | Display Name | Required | Description |
|---------|--------------|----------|-------------|
| language_selection | Language Selection | true | User selects preferred language |
| profile_setup | Profile Setup | true | User provides gender, height, weight, birth date |
| feature_intro | Feature Introduction | false | Overview of available features |
| completion | Completion | true | User confirms onboarding complete |

## Step Completion Tracking

```json
{
  "onboarding": {
    "completed": false,
    "language_set": true,
    "steps_completed": [
      "language_selection",
      "profile_setup"
    ]
  }
}
```

## Completion Criteria

Onboarding is considered complete when:
1. All required steps are in `steps_completed`
2. User confirms completion or interacts with any other skill
3. `onboarding.completed` is set to `true`

## Auto-Trigger Conditions

Onboarding flow starts when:
```
NOT exists(data/user-settings.json) OR
user_settings.onboarding.completed == false
```

## Step State Machine

```
[None] -> language_selection -> profile_setup -> feature_intro -> completion
           |                   |               |
           |                   |               +-> skip -> [Resume normal flow]
           |                   |
           |                   +-> skip -> [Resume normal flow]
           |
           +-> skip -> [Resume normal flow]
```

## Integration with Profile

When `profile_setup` step completes:
- Check if `data/profile.json` has valid values
- If yes, mark step as complete
- If no, prompt user again with `/profile` command
