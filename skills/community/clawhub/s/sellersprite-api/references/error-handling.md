# Error Handling

## Missing API Key

If `SELLERSPRITE_SECRET_KEY` env var is not set and no config file exists:

```
Missing API key. Set SELLERSPRITE_SECRET_KEY or run: sellersprite config set secretKey <key>
```

Exits with code 1.

## Unauthorized Endpoint (ERROR_UNAUTHORIZED)

When calling an API endpoint not included in your plan, the CLI:

1. Prints a warning to stderr (does NOT exit)
2. Automatically fetches your quota to show available modules
3. Continues execution — other commands are not affected

```
[WARN] Unauthorized: 未授权 (/v1/keyword-research)
  Your plan includes:
    marketResearch (选市场-列表) — 200 remaining
    productResearch (选产品) — 190 remaining
    asinDetailWithCouponTrend (ASIN详情及优惠趋势) — 24017 remaining
  This endpoint (/v1/keyword-research) is NOT in your plan.
  Upgrade at: https://open.sellersprite.com
```

This is a non-blocking warning. The command returns an empty result for the unauthorized endpoint and continues processing available data.

## API Module Mapping

| CLI Command | Required API Module |
|---|---|
| market | marketResearch |
| product | productResearch |
| competitor | productResearch (competitor-lookup) |
| asin | asinDetailWithCouponTrend (endpoint: /with-coupon-trend) |
| keyword | keywordResearch |

Check your available modules with `sellersprite quota`.

## HTTP Errors

Network or server errors throw with the HTTP status:

```
HTTP 500: Internal Server Error
```

## Timeout

All API requests have a 30-second timeout. Aborted requests throw:

```
The operation was aborted
```
