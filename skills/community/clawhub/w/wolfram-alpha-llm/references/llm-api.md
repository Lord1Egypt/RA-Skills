# Wolfram|Alpha LLM API (notes)

Primary endpoint:
- `https://www.wolframalpha.com/api/v1/llm-api`

Required parameters:
- `appid`: your AppID (or provide it as `Authorization: Bearer <AppID>`)
- `input`: query string

Core parameter:
- `maxchars`: response character limit (default ~6800)

Additional parameters supported by the LLM API (subset + passthrough from Full Results API):
- `assumption`
- `ip`, `latlong`, `timezone`, `location`
- `scantimeout`
- `units`, `currency`, `countrycode`, `languagecode`
- `width`, `maxwidth`, `plotwidth`, `mag`
- `formattimeout`, `parsetimeout`, `totaltimeout`
- `id`

Error behaviors (common):
- `400`: missing/invalid required parameters
- `403`: missing/invalid appid
- `501`: input not interpretable; body may contain suggestions

Docs:
- https://products.wolframalpha.com/llm-api/documentation
