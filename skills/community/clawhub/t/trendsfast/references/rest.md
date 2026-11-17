# TrendsFast REST recipes

The base URL is `https://trendsfast.com`. Every call sends
`Authorization: Bearer $TRENDSFAST_API_KEY`, so the key stays in the environment. The
commands run in bash or zsh with curl. The contract is
https://trendsfast.com/v3/openapi.json.

## Free reads

The brand and its `context_id`:

```bash
curl -sS https://trendsfast.com/v3/trends/context \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY"
```

The credit balance:

```bash
curl -sS https://trendsfast.com/v3/trends/wallet \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY"
```

The price of a product before you run it. Swap `customers` for `niche`, `competitors`,
`formats` or `search`, or drop `&product=…` for a read without a product:

```bash
curl -sS "https://trendsfast.com/v3/trends/quote?operation=niche&product=customers" \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY"
```

## Run a product

Make the `request_id` first and keep it; a retry of this call reuses it. Set
`max_credits` to the product's price from the quote.

```bash
REQUEST_ID=$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')
echo "request_id: $REQUEST_ID"
curl -sS -X POST https://trendsfast.com/v3/trends/niche \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<EOF
{
  "request_id": "$REQUEST_ID",
  "max_credits": 10,
  "input": { "product": "customers", "context_id": "<context_id>" }
}
EOF
```

Replace `<context_id>` with the value from `/v3/trends/context`.

## Read a niche the user typed

Without a confirmed brand, read the index against a typed niche. Leave out the product:
a typed niche is never collected, so a product would cost its full price for an
index-only read.

```bash
REQUEST_ID=$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')
curl -sS -X POST https://trendsfast.com/v3/trends/niche \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<EOF
{
  "request_id": "$REQUEST_ID",
  "max_credits": 3,
  "input": {
    "niche": {
      "description": "Scheduling software for independent dental clinics",
      "url": "https://example.com"
    }
  }
}
EOF
```

## What is trending everywhere

No brand needed:

```bash
REQUEST_ID=$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')
curl -sS -X POST https://trendsfast.com/v3/trends/global \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<EOF
{
  "request_id": "$REQUEST_ID",
  "max_credits": 1,
  "input": { "lookback_hours": 72, "limit": 10 }
}
EOF
```

## Recover and page

A lost response, by the `request_id` you kept:

```bash
curl -sS https://trendsfast.com/v3/trends/requests/$REQUEST_ID \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY"
```

A saved result, and its next page with the `next_cursor` it returned:

```bash
curl -sS "https://trendsfast.com/v3/trends/results/<result_id>?cursor=<next_cursor>" \
  -H "Authorization: Bearer $TRENDSFAST_API_KEY"
```

These reads are free and start no research.
