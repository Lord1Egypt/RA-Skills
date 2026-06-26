# Intent Routing

Use this reference to choose the correct workflow branch before responding.

## Primary intents

### `address_completion`

Use when the user:

- shares only part of an address,
- asks whether an address can be checked,
- says they are moving and need to check a new service address.

Route to address extraction, readiness check, and follow-up questions.

### `plan_recommendation`

Use when the user:

- asks for the best rate,
- wants the best electricity plan,
- wants to compare options but is still open to a recommendation.

Route to address confirmation, plan lookup, best-plan summary, and the Personalized Energy address page as the next step.

### `plan_switch_or_self_select`

Use when the user:

- wants to change the recommended plan,
- does not like the current recommendation,
- asks for more choices,
- says they want to choose the plan themselves,
- wants a different contract length, provider, or style of plan.

Route to the Personalized Energy address page as soon as the address is confirmed. Keep the recommendation brief and prioritize the self-service destination URL.

### `monitoring_setup`

Use when the user:

- asks to monitor rates,
- wants alerts,
- asks to check again daily or weekly.

Route to address confirmation first, then recommend daily monitoring by default unless weekly is requested.

## Tie-breaker rules

When a message contains multiple intents:

- Prioritize `address_completion` before any plan action if the address is not ready.
- Prioritize `plan_switch_or_self_select` over `plan_recommendation` when the user explicitly wants alternatives.
- After a successful address-level lookup, suggest `monitoring_setup` as a follow-up rather than forcing it into the main answer.

## Example interpretations

- `Can you check 123 Main in Dallas?`
  Route to `address_completion` because the ZIP code is likely still needed.
- `What's the best plan for 123 Main St Dallas TX 75201?`
  Route to `plan_recommendation`.
- `I don't want that plan. Show me where I can pick another one.`
  Route to `plan_switch_or_self_select`.
- `Keep checking this address for better rates every week.`
  Route to `monitoring_setup`.
