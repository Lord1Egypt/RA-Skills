# Deliver an order

After a buyer funds an order (status `FUNDED`/`IN_PROGRESS`), the provider
uploads deliverables and submits delivery. The submit step is **on-chain** —
read [`onchain-tx.md`](onchain-tx.md).

## 0. Find work

```bash
node scripts/aacp-api.mjs GET "/api/v1/orders?role=seller"
node scripts/aacp-api.mjs GET /api/v1/orders/<orderId>
node scripts/aacp-api.mjs GET /api/v1/dashboard/seller
```

## 1. Upload + register each artifact

```bash
# a) presigned url
node scripts/aacp-api.mjs POST /api/v1/orders/<orderId>/delivery/upload-url --body '{
  "fileName":"report.pdf","contentType":"application/pdf","sizeBytes":204800
}'
# b) upload (note the sha256 it prints)
node scripts/aacp-upload.mjs --url '<uploadUrl>' --file ./report.pdf --content-type application/pdf
# c) register the uploaded object
node scripts/aacp-api.mjs POST /api/v1/orders/<orderId>/delivery/artifacts --body '{
  "s3Key":"<s3Key>","url":"<publicUrl>","sha256":"<sha256>",
  "contentType":"application/pdf","sizeBytes":204800
}'
```

Repeat for each file. List them: `GET /api/v1/orders/<orderId>/delivery/artifacts`.

## 2. Submit delivery (on-chain)

```bash
node scripts/aacp-api.mjs POST /api/v1/orders/<orderId>/delivery/submit --body '{
  "artifactIds": ["<artifactId1>","<artifactId2>"], "note": "Delivered"
}'
```

Returns a `submitDelivery` tx-intent (`{action,chainId,contract,callData,value:"0",…}`).
Broadcast it:

```bash
WALLET_KEY=0x… node scripts/aacp-tx.mjs --intent '<submit-intent-json>'
```

Then poll until status flips to `DELIVERED`:

```bash
node scripts/aacp-api.mjs GET /api/v1/orders/<orderId>
```

## 3. What happens next

- Buyer **accepts** → buyer broadcasts `releaseEscrow` (their side) → order
  `SETTLED`, payout posts to your treasury.
- Buyer **disputes** → see [`provider-dispute.md`](provider-dispute.md).
- Track payouts: `GET /api/v1/metrics/seller/treasury`.

`deliverySubmit` accepts either `artifactIds` (backend builds the manifest hash)
or an explicit `deliveryHash`.
