---
name: parse-qr
description: >
  Parse crypto payment QR codes from screenshots or text. Supports EIP-681
  (Ethereum/EVM), Solana Pay, Stellar URI, and plain wallet addresses. Use
  when user shares a QR code image, pastes a payment URI, or says "scan
  this QR", "parse this payment link", or "read this QR code". Extracts
  address, chain, token, and amount.
metadata:
  author: rozo
  version: 0.1.0
---

# Parse Payment QR Code

## Instructions

Parse QR code content from screenshots or pasted URIs into structured payment data.

### Step 1: Get QR content

If the user shares a QR code image, you (the agent) read the QR code from the screenshot and extract the text content.
If the user pastes a URI string, use it directly.

**Note:** The `parse-qr.js` script parses URI strings — it does not decode images. The agent is responsible for reading the QR code from the image and extracting the text before passing it to the parser.

### Step 2: Parse

```bash
node scripts/dist/parse-qr.js "<qr_content>"
```

### Supported Formats

| Format | URI Scheme | Example |
|--------|-----------|---------|
| EIP-681 (EVM) | `ethereum:` | `ethereum:0x833.../transfer?address=0x5aA...&uint256=1000000` |
| Solana Pay | `solana:` | `solana:9wFF...?amount=10.25&spl-token=EPjF...` |
| Stellar URI | `web+stellar:` | `web+stellar:pay?destination=GC56...&amount=100&asset_code=USDC` |
| Plain address | (none) | `0x742d...`, `7xKX...`, `GC56...`, `CBHK...` |

### Step 3: Present parsed result

Show the extracted fields:
- **Address**: recipient wallet
- **Chain**: detected chain (or ask if EVM)
- **Token**: USDC/USDT if detected from contract address
- **Amount**: if present in the URI

If the QR contains a full payment request (address + amount + token), offer to proceed with payment using the `send-payment` skill.

If the QR contains only an address, ask the user for the amount.

## Examples

### Example 1: EIP-681 ERC-20
QR content: `ethereum:0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913/transfer?address=0x5aAe...&uint256=1000000`

Parsed: Base USDC, recipient 0x5aAe..., 1.00 USDC (1000000 raw, 6 decimals)

### Example 2: Solana Pay with USDC
QR content: `solana:9wFF...?amount=10.25&spl-token=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

Parsed: Solana, recipient 9wFF..., 10.25 USDC

### Example 3: Stellar URI
QR content: `web+stellar:pay?destination=GC56...&amount=100&asset_code=USDC`

Parsed: Stellar G-wallet, 100 USDC

### Example 4: Plain address
QR content: `0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6`

Parsed: EVM address (chain unknown — ask user)
