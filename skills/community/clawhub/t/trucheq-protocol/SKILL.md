---
name: trucheq_protocol
description: Interact with TruCheq P2P commerce protocol - browse verified marketplace listings, chat with sellers via XMTP, pay via x402 on Base
metadata:
  openclaw:
    requires:
      bins:
        - curl
      config:
        - TRUCHEQ_API_URL
        - XMTP_ENV
---

# TruCheq Protocol Agent Skill

Use this skill to help users buy and sell items through a P2P commerce protocol. Sellers are verified via World ID, listings are displayed from a marketplace API (IPFS is abstracted), and buyers pay via Coinbase x402 on Base Sepolia with encrypted XMTP chat.

## Network Configuration

- **Chain**: Base Sepolia (Chain ID: 84532)
- **Payment Token**: USDC (0x036cbd53842c5426634e7929545ec598f828a2b5)
- **XMTP Environment**: `dev` (for Base Sepolia testnet)

## Core Capabilities

### 1. Browse Marketplace

The TruCheq marketplace (`/marketplace`) displays listings from verified users and agents. All sellers have verified their identity via World ID.

**Marketplace URL:**
```
GET {TRUCHEQ_API_URL}/marketplace
```

**Note:** Agents can scrape this page to find listing CIDs. Each listing includes: cid, seller address, metadataUrl, price, and isOrbVerified flag (Orb = highest trust, Device = lower trust).

### 2. Fetch Listing Details

Get details for a specific listing by its CID (from marketplace or known listing).

```
GET {TRUCHEQ_API_URL}/api/deal/{cid}?meta={metadataUrl}
```

**Parameters:**
- `cid` - Listing content ID
- `meta` - Metadata URL (from marketplace)

**Response:**
```json
{
  "id": "Qm...",
  "seller": "0x...",
  "metadataURI": "https://...",
  "price": "300",
  "isOrbVerified": true
}
```

### 2. Purchase via x402

Use Coinbase x402 protocol to pay for a listing. Returns 402 (Payment Required) without payment, listing data with valid proof.

```
GET {TRUCHEQ_API_URL}/api/deal/{cid}/x402?meta={ipfsUrl}
```

**Without Payment (402 Response):**
```json
{
  "error": "Payment required",
  "scheme": "exact",
  "price": "300000000",
  "network": "84532",
  "asset": "USDC",
  "payTo": "0x...",
  "maxTimeoutSeconds": 300,
  "description": "TruCheq listing: ItemName - 300 USDC"
}
```

**Payment Header Format:**
```
WWW-Authenticate: x402 scheme=exact, network=eip155:84532, amount=$300000000, asset=USDC, payTo=0x...
```

### 3. Create Listing (Seller)

Upload images and create a new listing. The API handles IPFS storage internally.

```
POST {TRUCHEQ_API_URL}/api/upload
Content-Type: multipart/form-data
```

**Upload Image:**
- `type`: "image"
- `file`: Binary image file

**Create Listing:**
- `type`: "metadata"
- `metadata`: JSON object with itemName, description, price, seller, createdAt, isOrbVerified, images

### 4. Verify World ID Proof

Verify a user's World ID proof. Supports four trust levels:

```
POST {TRUCHEQ_API_URL}/api/verify
```

**Request:**
```json
{
  "devPortalPayload": {
    "nullifier_hash": "0x...",
    "proof": "0x...",
    "verification_level": "orb"
  }
}
```

**Verification Levels:**
- `orb` - Highest trust, World ID Orb biometric verification
- `secureDocument` - Government ID verification
- `document` - Basic document verification
- `device` - Lowest trust, device-based verification

### 5. XMTP Messaging

Send encrypted messages between buyers and sellers.

```
POST {TRUCHEQ_API_URL}/api/xmtp
```

**Send Message:**
```json
{
  "action": "send",
  "buyerAddress": "0x...",
  "message": "Hi, I'm interested!"
}
```

**List Conversations:**
```json
{ "action": "list-conversations" }
```

**Get Messages:**
```json
{
  "action": "messages",
  "conversationId": "..."
}
```

## Usage Flows

### Buy Item Flow
1. Browse marketplace: `GET /marketplace` to see all listings
2. Select a listing and get its details: `GET /api/deal/{cid}?meta={metadataUrl}`
3. Check `isOrbVerified` for seller trust level
4. Open XMTP chat: `POST /api/xmtp` with action "send"
5. Pay via x402: `GET /api/deal/{cid}/x402?meta={metadataUrl}` with payment proof

### Create Listing Flow (Seller)
1. Upload images: `POST /api/upload` with type=image
2. Create metadata JSON with itemName, description, price, seller address, images
3. Upload metadata: `POST /api/upload` with type=metadata
4. Share listing URL: `{baseUrl}/deal/{cid}?meta={metadataUrl}`

### Verify Seller Flow
1. Fetch listing to get seller address
2. Request seller provides World ID proof
3. Verify: `POST /api/verify` with seller's devPortalPayload

## Listing Metadata Structure

```json
{
  "itemName": "Apple Watch Ultra",
  "description": "Like new, comes with box",
  "price": "300",
  "seller": "0xabc123...",
  "createdAt": 1734567890,
  "isOrbVerified": true,
  "verificationLevel": "orb",
  "images": ["ipfs://Qm...", "ipfs://Qm..."]
}
```

## Trust Indicators

- `isOrbVerified: true` + `verificationLevel: "orb"` = Highest trust
- `verificationLevel: "secureDocument"` = Government ID verified
- `verificationLevel: "document"` = Basic document verified
- `verificationLevel: "device"` = Device-based (lowest trust)

## Error Codes

- `400` - Missing required parameters
- `402` - Payment required (x402 endpoint)
- `404` - Resource not found
- `500` - Server error

## Important Notes

- Listings stored on IPFS (behind marketplace API - no direct IPFS interaction needed)
- Payments go directly to seller (no escrow)
- Seller address from listing metadata used for XMTP
- XMTP environment is "dev" (Base Sepolia testnet)