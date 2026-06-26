# sg-helper-match

An AI Agent Skill for searching and matching domestic helpers from [Sunrise Link](https://www.sunriselink.sg), a licensed employment agency in Singapore.

This skill lets AI agents (Claude, Cursor, GitHub Copilot, etc.) query available helper candidates on behalf of employers, filtering by budget, skills, nationality, and more.

## Install

```bash
npx skills add https://github.com/sunrise-link/sg-helper-match
```

## Quick Start

```bash
# Search for Filipino helpers with infant care experience, SGD 600–700/month
node scripts/search_helpers.mjs '{"nationality":"Philippines","minSalary":600,"maxSalary":700,"needsInfantCare":true}'
```

**Requirements:** Node.js 18+ (uses built-in `fetch`). No `npm install` needed — zero dependencies.

## What It Does

- Searches Sunrise Link's database of available domestic helpers
- Filters by nationality, salary, age, skills (childcare, elderly care, cooking, housework), language, religion, and Singapore experience
- Returns structured candidate data including skills evaluation, work history, and profile links
- Guides employers through requirements gathering when no criteria are specified

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill entry point — agent reads this for behavior instructions |
| `scripts/search_helpers.mjs` | Query script that calls the Sunrise Link public API |
| `references/field_guide.md` | Detailed field documentation — agent loads on demand |

## Search Parameters

All parameters are optional. Pass as JSON to the search script.

| Parameter | Type | Example |
|-----------|------|---------|
| `nationality` | string | `"Philippines"` |
| `religion` | string | `"Buddhism"` |
| `languages` | string[] | `["English", "Tagalog"]` |
| `minAge` / `maxAge` | number | `25` / `40` |
| `minSalary` / `maxSalary` | number | `600` / `700` |
| `hasSgExperience` | boolean | `true` |
| `needsInfantCare` | boolean | `true` |
| `needsExperiencedInfantCare` | boolean | `true` |
| `needsElderlyCare` | boolean | `true` |
| `needsExperiencedElderlyCare` | boolean | `true` |
| `needsDisabledCare` | boolean | `true` |
| `needsCooking` | boolean | `true` |
| `needsExperiencedCooking` | boolean | `true` |
| `needsHousework` | boolean | `true` |

Valid nationality values: `Myanmar`, `India`, `Indonesia`, `Philippines`, `Bangladesh`, `Cambodia`, `Laos`, `Nepal`

See `references/field_guide.md` for the full specification.

## Example

```bash
node scripts/search_helpers.mjs '{"needsExperiencedCooking":true,"maxSalary":650}'
```

```json
{
  "totalFound": 8,
  "returned": 5,
  "candidates": [
    {
      "id": 42,
      "uuid": "a1b2c3d4-...",
      "age": 28,
      "nationality": "Philippines",
      "salary": 650,
      "skills": {
        "sgEvaluated": {
          "cooking": { "willingness": true, "experienced": true, "cuisines": ["Chinese", "Western"] }
        }
      },
      "profileUrl": "https://www.sunriselink.sg/helpers/a1b2c3d4-...?utm_source=agent-skill&utm_medium=skill&utm_campaign=sg-helper-match"
    }
  ]
}
```

*(Response truncated for brevity — actual candidates include all fields.)*

## Privacy

This skill is designed with privacy as a core principle:

- **No PII returned**: The API never exposes candidate names, photos, dates of birth, contact information, home addresses, health records, or employer feedback.
- **Available candidates only**: Only candidates with `status = available` are returned.
- **Profile links for details**: Each candidate includes a `profileUrl` linking to their profile on the Sunrise Link website, where employers can view full details and arrange interviews.

## About Sunrise Link

[Sunrise Link](https://www.sunriselink.sg) is a licensed employment agency in Singapore specialising in domestic helper placement. This skill provides free candidate search as a convenience — all hiring, interviews, and contracts are handled through the agency's official platform.

## License

MIT
