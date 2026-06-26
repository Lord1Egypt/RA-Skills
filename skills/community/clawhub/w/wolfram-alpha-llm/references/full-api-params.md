# Full Results API parameter reference (pointer)

The Wolfram|Alpha LLM API supports many parameters from the Full Results API. When you need deeper control (formatting, location, timeouts, units, etc.), consult:

- https://products.wolframalpha.com/api/documentation?scrollTo=parameter-reference

High-signal parameters to consider for LLM workflows:

## Disambiguation
- `assumption` (repeatable): choose a specific interpretation.

## Context & localization
- `units`: control unit system.
- `currency`: currency code.
- `countrycode`, `languagecode`.
- `timezone`.
- location (choose one): `ip` OR `latlong` OR `location`.

## Performance / timeouts
- `scantimeout`, `parsetimeout`, `formattimeout`, `totaltimeout`.

## Output sizing (mostly relevant for images; still useful sometimes)
- `width`, `maxwidth`, `plotwidth`, `mag`.
