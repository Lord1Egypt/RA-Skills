# Prompt · Indicator discovery

**The API is open — no API key.**

## Purpose

Turn a plain-English concept into the correct World Bank indicator code before
fetching data, avoiding guessed codes.

## Reusable template

```
You need the World Bank indicator code for: {{concept}}.

1. Call worldbank_search_indicators with q="{{search_keywords}}" and limit={{limit}}.
2. From the {id, name} results, choose the single best match for "{{concept}}".
   Prefer {{preference}} (e.g. "current US$" over "constant", "annual %" if a rate is wanted).
3. Confirm with worldbank_indicator_metadata(indicator=<chosen id>) and verify the unit/definition.
4. Output the chosen code and name. Do NOT invent a code.
```

## Variables

| Variable | Meaning | Example |
|----------|---------|---------|
| `{{concept}}` | The metric in plain English | "GDP per person" |
| `{{search_keywords}}` | Keywords for the search | "GDP per capita" |
| `{{limit}}` | Max results | 5 |
| `{{preference}}` | Disambiguation rule | "current US$" |

## Example (filled)

```
You need the World Bank indicator code for: GDP per person.
1. Call worldbank_search_indicators with q="GDP per capita" and limit=5.
2. Choose the best match. Prefer "current US$".
3. Confirm with worldbank_indicator_metadata(indicator=NY.GDP.PCAP.CD).
4. Output: NY.GDP.PCAP.CD — GDP per capita (current US$).
```

## Bad

> "GDP per capita is `GDP.PERCAP` — let me fetch it." (invented code, no search,
> no metadata confirmation)

## Good

> Searched, found `NY.GDP.PCAP.CD` ("GDP per capita (current US$)"), confirmed
> unit via metadata, then fetched. Code is verified, not guessed.

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
