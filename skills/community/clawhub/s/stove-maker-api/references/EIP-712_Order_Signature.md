# EIP-712 Order Signature [â](#eip-712-order-signature)

## Overview [â](#overview)

Before creating an order, Makers need to sign the order data using the EIP-712 standard. EIP-712 is Ethereum's structured data signing standard that allows users to clearly see the data being signed.

## Contract Addresses [â](#contract-addresses)

BSC Testnet
BSC Mainnet
text
Chain ID:      97
RFQSettlement: 0xCB310C56A19078aA969A922f382613d932D89D83

Test Tokens
For MOCK stablecoin addresses and how to obtain them in the test environment, please refer to
Testing Guide

## EIP-712 Domain [â](#eip-712-domain)

The Domain defines the signing context, including contract name, version, chain ID, and verifying contract address.

ethers.js
viem
javascript
const
domain
=
{
name:
"RFQSettlement"
,
version:
"1"
,
chainId:
"<Chain ID>"
,
verifyingContract:
"<RFQSettlement Contract Address>"
}

## Order Type Definition [â](#order-type-definition)

The order data structure contains the following fields:

ethers.js
viem
javascript
const
types
=
{
Order: [
{ name:
"maker"
, type:
"address"
},
{ name:
"principal"
, type:
"address"
},
{ name:
"isBuy"
, type:
"bool"
},
{ name:
"ticker"
, type:
"string"
},
{ name:
"exchange"
, type:
"uint16"
},
{ name:
"asset"
, type:
"address"
},
{ name:
"price"
, type:
"uint256"
},
{ name:
"quantity"
, type:
"uint256"
},
{ name:
"incentive"
, type:
"uint256"
},
{ name:
"deadline"
, type:
"uint256"
},
{ name:
"nonce"
, type:
"uint256"
}
]
}

### Field Description [â](#field-description)

For detailed field descriptions, please refer to [Create Order - Request Parameters](./create.html#request-parameters)

## Complete Example [â](#complete-example)

ethers.js
viem
javascript
import
{ ethers }
from
'ethers'
// 1. Connect wallet
const
provider
=
new
ethers.
BrowserProvider
(window.ethereum)
const
signer
=
await
provider.
getSigner
()
const
userAddress
=
await
signer.
getAddress
()
// 2. Get chain ID
const
network
=
await
provider.
getNetwork
()
const
chainId
=
Number
(network.chainId)
// 3. Get nonce and maker address from backend API
const
jwtToken
=
"your_jwt_token"
const
nonceResponse
=
await
fetch
(
'/api/v1/orders/maker/next-nonce'
, {
headers: {
'Authorization'
:
`Bearer ${
jwtToken
}`
}
})
const
{
maker
,
next_nonce
}
=
(
await
nonceResponse.
json
()).data
// 4. Define Domain
const
domain
=
{
name:
"RFQSettlement"
,
version:
"1"
,
chainId:
"<Chain ID>"
,
verifyingContract:
"<RFQSettlement Contract Address>"
}
// 5. Define order types
const
types
=
{
Order: [
{ name:
"maker"
, type:
"address"
},
{ name:
"principal"
, type:
"address"
},
{ name:
"isBuy"
, type:
"bool"
},
{ name:
"ticker"
, type:
"string"
},
{ name:
"exchange"
, type:
"uint16"
},
{ name:
"asset"
, type:
"address"
},
{ name:
"price"
, type:
"uint256"
},
{ name:
"quantity"
, type:
"uint256"
},
{ name:
"incentive"
, type:
"uint256"
},
{ name:
"deadline"
, type:
"uint256"
},
{ name:
"nonce"
, type:
"uint256"
}
]
}
// 6. Build order data
const
order
=
{
maker: maker,
principal: userAddress,
isBuy:
true
,
ticker:
"AAPL"
,
exchange:
0
,
asset:
"<USDT Contract Address>"
,
price: ethers.
parseUnits
(
"150.5"
,
18
),
// 18 decimals
quantity:
"100"
,
// Integer
incentive: ethers.
parseUnits
(
"1.0"
,
18
),
// 18 decimals
deadline: Math.
floor
(Date.
now
()
/
1000
)
+
86400
*
30
,
// Expires in 30 days
nonce: next_nonce
}
// 7. Sign
const
signature
=
await
signer.
signTypedData
(domain, types, order)
// 8. Submit order
const
response
=
await
fetch
(
'/api/v1/orders'
, {
method:
'POST'
,
headers: {
'Content-Type'
:
'application/json'
,
'Authorization'
:
`Bearer ${
jwtToken
}`
},
body:
JSON
.
stringify
({
order: {
maker: order.maker,
principal: order.principal,
is_buy: order.isBuy,
ticker: order.ticker,
exchange: order.exchange,
asset: order.asset,
price: order.price.
toString
(),
quantity: order.quantity,
incentive: order.incentive.
toString
(),
deadline: order.deadline,
nonce: order.nonce
},
signature: signature
})
})
const
result
=
await
response.
json
()
console.
log
(
'Order created successfully:'
, result)

## Complete JSON Examples [â](#complete-json-examples)

### Request Examples [â](#request-examples)

Buy Order
Sell Order
json
{
"order"
: {
"maker"
:
"0x1234567890123456789012345678901234567890"
,
"principal"
:
"0x1234567890123456789012345678901234567890"
,
"is_buy"
:
true
,
"ticker"
:
"AAPL"
,
"exchange"
:
0
,
"asset"
:
"<USDT Contract Address>"
,
"price"
:
"150500000000000000000"
,
"quantity"
:
"100"
,
"incentive"
:
"1000000000000000000"
,
"deadline"
:
1735689600
,
"nonce"
:
1
},
"signature"
:
"0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef12"
}

### Response Example [â](#response-example)

```json
{
  "code": 0,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "maker": "0x1234567890123456789012345678901234567890",
    "principal": "0x1234567890123456789012345678901234567890",
    "is_buy": true,
    "ticker": "AAPL",
    "exchange": 0,
    "asset": "<USDT Contract Address>",
    "price": "150500000000000000000",
    "quantity": "100",
    "incentive": "1000000000000000000",
    "deadline": 1735689600,
    "nonce": 1,
    "signature": "0x1234567890abcdef...",
    "order_hash": "0xabcdef1234567890...",
    "status": "pending",
    "filled_quantity": "0",
    "created_at": "2025-01-17T03:00:24Z",
    "updated_at": "2025-01-17T03:00:24Z"
  }
}
```

## Important Notes [â](#important-notes)

### 1. Nonce Management [â](#_1-nonce-management)

- Each order must use a unique nonce
- Must be obtained from the backend API, see [Query Nonce](./nonce.html)
- Nonce is used to prevent replay attacks

### 2. Authorization Check [â](#_2-authorization-check)

Token authorization is required before creating orders:

Buy Order Authorization
Sell Order Authorization
javascript
// Buy order: Authorize USDT/USDC
await
usdtContract.
approve
(rfqSettlementAddress, ethers.MaxUint256)

### 3. Deadline Setting [â](#_3-deadline-setting)

- Deadline must be at least current time + 720 hours (30 days)
- Recommend setting longer validity for limit orders to ensure sufficient time for execution
- Use Unix timestamp (seconds)

```javascript
const deadline = Math.floor(Date.now() / 1000) + 86400 * 30  // 30 days later
```

### 4. Price and Fees [â](#_4-price-and-fees)

- Use [Estimate Order Fee](./estimate.html) endpoint to get accurate price and fees
- Price needs to consider exchange rate conversion
- incentive (fee) must be >= estimated fee, otherwise the order will not be executed

## Related Endpoints [â](#related-endpoints)

- [Get Nonce](./nonce.html) - Get the next available nonce
- [Estimate Order Fee](./estimate.html) - Get order price and fee estimation
- [Create Order](./create.html) - Submit signed order
