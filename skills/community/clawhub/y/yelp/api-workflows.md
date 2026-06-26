# Yelp API Workflows

Use these patterns when `YELP_API_KEY` is available.

## 1) Connectivity check

```bash
curl -sS -H "Authorization: Bearer ${YELP_API_KEY}" \
  "https://api.yelp.com/v3/businesses/search?location=New%20York&term=coffee" \
  | jq '.businesses[0] | {id, alias, name, rating, review_count}'
```

If the key is missing or invalid:
- stop calling the API
- switch to page mode
- explain the tradeoff to the user

## 2) Discover candidates

```bash
curl -sS -H "Authorization: Bearer ${YELP_API_KEY}" \
  "https://api.yelp.com/v3/businesses/search?location=Chicago&term=pizza&sort_by=best_match&limit=10" \
  | jq '.businesses[] | {id, alias, name, rating, review_count, price, categories}'
```

Use location plus one or two intent filters. Do not pile on too many parameters before a first pass.

## 3) Resolve an exact business by phone

```bash
curl -sS -H "Authorization: Bearer ${YELP_API_KEY}" \
  "https://api.yelp.com/v3/businesses/search/phone?phone=%2B14159083801" \
  | jq '{id, alias, name, location, phone}'
```

Use phone match when name collisions or chain duplicates make alias resolution unreliable.

## 4) Fetch business detail and reviews

```bash
curl -sS -H "Authorization: Bearer ${YELP_API_KEY}" \
  "https://api.yelp.com/v3/businesses/${BUSINESS_ID}" \
  | jq '{id, alias, name, rating, review_count, price, transactions, hours, location}'

curl -sS -H "Authorization: Bearer ${YELP_API_KEY}" \
  "https://api.yelp.com/v3/businesses/${BUSINESS_ID}/reviews" \
  | jq '.reviews[] | {rating, text, time_created, user: .user.name}'
```

Always keep detail fields and review evidence separate in notes so stale metadata does not contaminate review interpretation.

## 5) Delivery search where supported

```bash
curl -sS -H "Authorization: Bearer ${YELP_API_KEY}" \
  "https://api.yelp.com/v3/transactions/delivery/search?location=San%20Francisco&categories=thai" \
  | jq '.businesses[] | {id, alias, name, transactions, delivery}'
```

If delivery search is unsupported in the target market, stop and say so clearly.

## Logging safety rule

- Never log raw headers or full bearer tokens.
- In `~/yelp/api/request-log.md`, keep only path, safe params, status, and timestamp.
- Safe example:

```text
GET /v3/businesses/search?location=Chicago&term=pizza -> 200
```

## Output contract

Always return:
- chosen mode: api, page, or hybrid
- shortlist or audit findings
- why the top options survived filtering
- uncertainty or freshness warnings
