# Vaultline API Examples

## Live storage tiers

- `open`
- `private`

Do not use `encrypted` as a live tier yet. Treat it as coming soon.

## Upload: open

```http
PUT /v1/files/workspace/demo.txt
content-type: text/plain
content-length: 18
x-storage-tier: open
```

Open is also the default when `x-storage-tier` is omitted.

## Upload: private

Required headers:
- `x-storage-tier: private`
- `x-auth-wallet`
- `x-auth-timestamp`
- `x-auth-signature`

Optional headers:
- `x-owner-wallet`
- `x-allowed-wallets`

Example:

```http
PUT /v1/files/workspace/secret.txt
content-type: text/plain
content-length: 20
x-storage-tier: private
x-auth-wallet: 0xYourWallet
x-auth-timestamp: 1715576400000
x-auth-signature: 0x...
```

## Private auth message format

```text
Vaultline auth
method:PUT
path:workspace/secret.txt
wallet:0xYourWallet
timestamp:1715576400000
```

The signed message must match:
- HTTP method
- file path without the host
- wallet address
- timestamp header

## Read: open

Open files:
- small reads may return directly
- larger reads may return `402` first

## Read: private

Private reads require wallet auth headers even when the file is below the free-read threshold.

If the wallet is not authorized:
- unauthenticated request -> `401`
- authenticated but unauthorized wallet -> `403`

## Pay-and-retry pattern

For paid operations:
1. send the request normally
2. if the response is `402`, parse the `payment-required` header
3. create/sign the x402 payment payload
4. retry the same request with the payment header
5. expect the normal route response
