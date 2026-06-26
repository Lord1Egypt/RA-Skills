# Error Handling and Limits

## Common failure modes

| Symptom | Likely cause | Better move |
|---------|--------------|-------------|
| 401-style auth failure | Missing or invalid `TM_API_KEY` | Re-export the key and re-run a minimal search |
| Empty but valid result | Filters too narrow or locale mismatch | Remove one filter, then retry with `locale=*` |
| Huge noisy result set | Query too broad | Add `city`, `countryCode`, `classificationName`, `venueId`, or `attractionId` |
| Missing expected pages | Deep paging boundary hit | Narrow the filters instead of pushing `page` higher |
| Confusing venue or city | Cross-market listing or broad keyword | Read `_embedded.venues` from a detail request |

## Documented limits

- Default quota: 5000 API calls per day
- Rate limit: 5 requests per second
- Deep paging: supported only while `size * page < 1000`

## Good recovery pattern

1. Retry with `size=1`.
2. Remove optional filters one at a time.
3. Confirm the event or venue exists with a keyword-only query.
4. Save the strongest ID and continue with detail endpoints.
