---
name: wolfram-alpha-llm
description: Delegate precise, formalizable computations and factual lookups to Wolfram|Alpha via its LLM API (HTTP) to get verified results and reduce arithmetic/modeling errors. Use for numeric calculations, unit conversions, symbolic algebra/calculus, equation solving, statistics/probability, date/time math, finance/math with currency, and structured data queries (e.g., population, chemistry/physics constants, astronomy facts). Use when you want short, LLM-friendly text output (optionally within a character budget), need to resolve ambiguous interpretations via assumptions, or want location/units/language-specific results.
metadata:
  openclaw:
    emoji: "📐"
    requires:
      bins:
        - python3
      env:
        - WOLFRAM_APP_ID
---

# Wolfram|Alpha (LLM API) skill

Use the bundled wrapper script to call Wolfram|Alpha's **LLM API** and return concise, model-ingestible results.

## Preconditions

- Environment variable **`WOLFRAM_APP_ID`** must be set (your Wolfram|Alpha AppID). If it is not set, ask your human to set it (do not guess or hardcode keys).

## Quick start

Run:

```bash
# default: cache ON (7d), auth via bearer header (keeps AppID out of URL)
python3 skills/wolfram-alpha-llm/scripts/wa_llm.py \
  --input "solve x^2 + 3x + 2 = 0"
```

## What to send as `--input`

- Prefer **short English keyword-style** queries when possible.
- If the user asked in another language, translate to English for the API call, then answer in the user’s original language.
- When you need an exact computation, be explicit (e.g., `integrate sin(x)^2 from 0 to pi`).

## Core parameters (use these most)

- `--input` (required): the query.
- `--maxchars` (optional, default 2500): cap response length.
- `--units` (optional): set units system, if needed for conversions/physics (`metric` is often a good default when unspecified).
- `--assumption` (optional, repeatable): disambiguate when WA returns irrelevant interpretation or offers assumptions.

## High-value optional parameters (use when relevant)

- Localization / context:
  - `--countrycode`, `--languagecode`
  - `--timezone`
  - One of: `--ip` | `--latlong` | `--location` (pick exactly one)
- Finance:
  - `--currency` (e.g., `USD`, `EUR`)
- Performance / robustness:
  - `--scantimeout`, `--parsetimeout`, `--formattimeout`, `--totaltimeout`

## Output handling guidance

- Treat output as *computed evidence*: quote the key result, then add minimal interpretation.
- If the result is too long/noisy, rerun with a smaller `--maxchars`.
  - Heuristic: for simple conversions / arithmetic / single-value answers, try `--maxchars 800`.
  - Keep default `--maxchars 2500` for most multi-line or explanation-heavy results.
- If the interpretation is wrong:
  1) retry with `--assumption ...` (use WA-provided suggestions when available),
  2) only then rephrase/simplify `--input`.

## Wrapper script

- Script: `skills/wolfram-alpha-llm/scripts/wa_llm.py`
- Auth:
  - default `--auth bearer`: sends `Authorization: Bearer <AppID>` header (keeps AppID out of the URL)
  - `--auth query`: sends `appid` as URL parameter
- Cache:
  - default `--cache on` with `--cache-ttl 604800` (7d)
  - stores best-effort results in: `~/.cache/openclaw-wolfram-alpha/`
- Returns:
  - stdout: API text body
  - stderr: errors, HTTP status context

For parameter details and error behaviors, see:
- `skills/wolfram-alpha-llm/references/llm-api.md`
- `skills/wolfram-alpha-llm/references/full-api-params.md`
