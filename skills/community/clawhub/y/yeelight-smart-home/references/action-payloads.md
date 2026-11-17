# Action Payloads

Use this file only as a routing index. The payload contract has been split into smaller references so the AI can load the narrowest file.

## Load These Instead

- Common action row, target type rules, light parameters, property vocabulary, and contract lookup: `references/payload-shapes.md`.
- Scene create/update recipe conversion and lighting-design scene rows: `references/scene-recipes.md`.
- Automation conditions, repeat rules, actions, and lighting-design automation rows: `references/automation-recipes.md`.
- Full lighting design import structure: `references/lighting-design-import.md`.

## Rule

Before guessing nested action, condition, item, operation, button-event, or lighting design JSON, use Runtime intent lookup:

```json
{
  "intent": "intent.explain",
  "parameters": {
    "intent": "scene.update"
  }
}
```

In `invoke --stdin` responses, read the contract under `result.intentExplanation`. Use returned `requestSchema`, `payloadGuide.payloadShape`, `requestSchema.examples`, `nextStep`, `editablePayload`, or `updateShape` as authoritative. Do not retry guessed variants blindly.
