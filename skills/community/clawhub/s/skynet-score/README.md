# Skynet Score

CertiK Skynet skill for searching blockchain projects and interpreting public project score results.

Use `scripts/skynet_score.py` as the default entrypoint to inspect project score search results with the CertiK public project API.

## Files

- `SKILL.md`: agent-facing instructions and answer workflow
- `scripts/skynet_score.py`: CLI wrapper for the public project search endpoint

## Quick Start

Run commands from this directory:

```bash
python3 scripts/skynet_score.py --keyword "uniswap"
```

Fallback with `curl`:

```bash
curl -sG "https://open.api.certik.com/projects" \
  -H "Accept: application/json, text/plain, */*" \
  --data-urlencode "keyword=uniswap"
```

## Typical Use Cases

- Search for a project by keyword or approximate name
- Return the overall Skynet score and tier
- Compare score breakdown fields across candidate projects
- Check when a project score was last updated

## Workflow

1. Extract the project keyword from the user request.
2. Run the bundled Python script first.
3. If multiple matches are returned, list the best candidates instead of guessing.
4. When a clear match exists, summarize the project name, overall score, tier, update time, and the most relevant component scores.

## Important Fields

- `score`: overall Skynet score
- `tier`: score tier
- `updatedAt`: last update time
- `scoreCodeSecurity`: code security score
- `scoreCommunity`: community score
- `scoreFundamental`: fundamentals score
- `scoreGovernance`: governance score
- `scoreMarket`: market score
- `scoreOperation`: operations score

## API Notes

- Endpoint: `GET https://open.api.certik.com/projects`
- Required query parameter: `keyword`
- Rate limit guidance in `SKILL.md` applies when integrating the public endpoint directly

## Output Notes

- Do not invent a score when there is no project match.
- If there are several close matches, present candidates and ask the user which one they mean.
- Keep the overall score first and the component scores second.
