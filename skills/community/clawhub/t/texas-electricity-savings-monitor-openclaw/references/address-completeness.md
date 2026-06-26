# Address Completeness

Use this reference when deciding whether to continue the lookup, ask a follow-up question, show candidate addresses, or build the Personalized Energy address page.

## Minimum fields for destination URL generation

Treat the address as ready only when all of these are true:

- `street` is present and includes a street number plus street name.
- `city` is present.
- `zipcode` is present.
- `state` is `TX` or can be safely defaulted to `TX`.

The destination URL format requires:

`https://www.personalized.energy/electricity-rates/texas/{city_lower}/{zipcode}/{urlencoded_street}?source=skills`

Do not generate the URL until the address meets that threshold.

## Unit and apartment handling

Treat `unit` as conditionally required.

Ask for `unit` when any of these are true:

- The user already mentioned apartment, apt, unit, suite, building, or lot language without a specific identifier.
- The user entered conflicting or repeated unit text and the exact unit cannot be trusted yet.
- The matched address candidates differ only by unit.
- The service address is likely to be multi-family and a missing unit could change plan availability or ESIID matching.

If the user appears to live at a single-family residence and there is no evidence that a unit is needed, continue without it.

## Incomplete address patterns

Ask for the narrowest missing information.

- Street missing: ask for the full street number and street name.
- City missing: ask for the Texas city.
- ZIP missing: ask for the ZIP code.
- City and ZIP missing: ask for both in one question.
- Street present but not specific enough: ask for the full service address.

## Ambiguity rules

Treat the address as ambiguous when:

- Multiple candidate addresses match the same street text.
- The same street appears in different Texas cities or ZIP codes.
- The lookup returns several units or buildings for the same base address.

When ambiguous:

- Show the choices in plain English.
- Ask the user to confirm the exact address.
- Do not guess.

## Candidate selection rules

After a candidate lookup succeeds:

- Always show the candidate addresses as a numbered list.
- Ask the user to reply with the matching number or the full matching address.
- If the user says none of the candidates are correct, ask for the full correct Texas service address.
- Do not proceed to ESIID lookup, plan lookup, or destination URL generation until one candidate is confirmed.

## Follow-up prompt patterns

Use concise prompts such as:

- `Please send the full Texas service address, including city and ZIP code if available.`
- `I need the city and ZIP code to check the correct Texas service address.`
- `If this is an apartment or unit address, please include the apartment or unit number too.`
- `I found more than one possible address. Please confirm which one is your exact Texas service address.`
