# Testing Guide [â](#testing-guide)

## Overview [â](#overview)

This testing guide is designed to help developers and QA teams test the **Stock Protocol Maker API** in a controlled environment. The guide explains how to simulate different order states and lifecycle scenarios using predefined quantity rules.

The mock matching engine returns consistent responses based on the order quantity values you submit. This allows you to verify various order status behaviors without requiring actual blockchain transactions or real market conditions.

## Purpose [â](#purpose)

- Validate order creation and lifecycle management
- Test order state transitions (pending, partially filled, filled, rejected, cancelled)
- Verify API responses for different scenarios
- Ensure proper error handling and edge cases
- Prepare for production deployment with confidence

## Testing Environment [â](#testing-environment)

**Base URL**: Use `{API_BASE_URL}` placeholder for your testing environment

**Authentication**: Required - Use JWT token obtained from [Authorization API](./authorization.html)

**Blockchain**: BSC Testnet (Chain ID: 97) or configured test network

## Obtaining Test Tokens [â](#obtaining-test-tokens)

Before creating orders in the testing environment, you need to obtain MOCK_USDT or MOCK_USDC test tokens. The test token contracts are deployed on BSC Testnet and provide a `faucet` function for users to obtain test tokens for free.

### Test Token Contract Addresses [â](#test-token-contract-addresses)

- **MOCK_USDT**: `0x09671802Cc9Bbf6402f2e7a07b220Aa7b43D8c91`
- **MOCK_USDC**: `0x5f3733f382ab5d464D39742Bb3840898cD24E6a0`
- **Decimals**: 18
- **Network**: BSC Testnet (Chain ID: 97)

### Method 1: Call faucet Function Using Web3 Libraries [â](#method-1-call-faucet-function-using-web3-libraries)

ethers.js
viem
web3.py
javascript
import
{ ethers }
from
'ethers'
;
const
provider
=
new
ethers.
JsonRpcProvider
(
'https://data-seed-prebsc-1-s1.binance.org:8545/'
);
const
wallet
=
new
ethers.
Wallet
(
'YOUR_PRIVATE_KEY'
, provider);
const
MOCK_USDT_ADDRESS
=
'{MOCK_USDT_ADDRESS}'
;
const
mockERC20ABI
=
[
'function faucet(uint256 amount) external'
,
'function balanceOf(address account) view returns (uint256)'
];
const
mockUSDT
=
new
ethers.
Contract
(
MOCK_USDT_ADDRESS
, mockERC20ABI, wallet);
const
amount
=
ethers.
parseUnits
(
'1000'
,
18
);
const
tx
=
await
mockUSDT.
faucet
(amount);
await
tx.
wait
();
console.
log
(
'Successfully obtained 1000 MOCK_USDT'
);

### Method 2: Using Smart Contract Explorer [â](#method-2-using-smart-contract-explorer)

1. Visit BSC Testnet Explorer: [https://testnet.bscscan.com/](https://testnet.bscscan.com/)
2. Search for MOCK_USDT contract address: `0x09671802Cc9Bbf6402f2e7a07b220Aa7b43D8c91`
3. Go to "Contract" tab and click "Write Contract"
4. Connect your MetaMask wallet (ensure you're on BSC Testnet)
5. Find the `faucet` function
6. Enter amount (Note: must include 18 decimals, e.g., `1000000000000000000000` for 1000 USDT)
7. Click "Write" button and confirm transaction

### Important Notes [â](#important-notes)

- No quantity limit per `faucet` call, but obtain reasonable amounts based on testing needs
- Ensure your wallet has sufficient BNB testnet tokens to pay gas fees
- BNB testnet tokens can be obtained from BSC Testnet Faucet: [https://testnet.bnbchain.org/faucet-smart](https://testnet.bnbchain.org/faucet-smart)
- MOCK_USDC can be obtained the same way as MOCK_USDT, just replace the contract address

## Order Quantity Rules [â](#order-quantity-rules)

To simulate different order states, use the following quantity patterns when creating orders:

### Market-Specific Rules [â](#market-specific-rules)

- No minimum quantity restrictions for US stocks
- Can use any quantity following the patterns below

### Quantity Patterns [â](#quantity-patterns)

### 1. Pending Orders (Awaiting Fill) [â](#_1-pending-orders-awaiting-fill)

**Pattern**: Quantities ending in `1` (e.g., 1, 10, 100, 1000, 10000)

**Expected Behavior**:

- Order is created and remains in `pending` state
- No fills are executed
- Order stays on the order book waiting for takers

**Use Case**: Test order creation and order book listing

**Example Quantities**:

1, 10, 100, 1000, 10000

---

### 2. Partially Filled Orders [â](#_2-partially-filled-orders)

**Pattern**: Quantities ending in `2` (e.g., 2, 20, 200, 2000, 20000)

**Expected Behavior**:

- Order is created and immediately partially filled
- Order status becomes `partially_filled`
- Remaining quantity stays on order book
- Fill records are generated

**Use Case**: Test partial execution and remaining quantity tracking

**Example Quantities**:

2, 20, 200, 2000, 20000

---

### 3. Rejected Orders [â](#_3-rejected-orders)

**Pattern**: Quantities ending in `3` (e.g., 3, 30, 300, 3000, 30000)

**Expected Behavior**:

- Order is rejected by the system
- Order status becomes `rejected`
- No fills are executed
- Error message is returned

**Use Case**: Test error handling and rejection scenarios

**Example Quantities**:

3, 30, 300, 3000, 30000

---

### 4. Partially Cancelled Orders [â](#_4-partially-cancelled-orders)

**Pattern**: Quantities ending in `4` (e.g., 4, 40, 400, 4000, 40000)

**Expected Behavior**:

- Order is created and partially filled
- Remaining quantity is automatically cancelled
- Order status becomes `cancelled`
- Fill records show partial execution before cancellation

**Use Case**: Test cancellation with partial fills

**Example Quantities**:

4, 40, 400, 4000, 40000

---

### 5. Fully Cancelled Orders [â](#_5-fully-cancelled-orders)

**Pattern**: Quantities ending in `5` (e.g., 5, 50, 500, 5000, 50000)

**Expected Behavior**:

- Order is created without any fills
- Order is immediately cancelled
- Order status becomes `cancelled`
- No fill records are generated

**Use Case**: Test full cancellation without execution

**Example Quantities**:

5, 50, 500, 5000, 50000

---

### 6. Fully Filled Orders [â](#_6-fully-filled-orders)

**Pattern**: Quantities ending in `6` (e.g., 6, 60, 600, 6000, 60000)

**Expected Behavior**:

- Order is created and immediately fully filled
- Order status becomes `filled`
- Complete fill records are generated
- No remaining quantity on order book

**Use Case**: Test complete order execution

**Example Quantities**:

6, 60, 600, 6000, 60000

---

## Testing Matrix [â](#testing-matrix)

| Quantity | Last Digit | Expected Status | Filled Qty | Remaining Qty | Description |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | `pending` | 0 | 1 | Order awaiting fill |
| 2 | 2 | `partially_filled` | ~1 | ~1 | Partial execution |
| 3 | 3 | `rejected` | 0 | 0 | Order rejected |
| 4 | 4 | `cancelled` | ~2 | 0 | Partial fill then cancelled |
| 5 | 5 | `cancelled` | 0 | 0 | Fully cancelled |
| 6 | 6 | `filled` | 6 | 0 | Fully executed |

## Query Order Status [â](#query-order-status)

After creating orders, query their status using:

```bash
curl -X GET "{API_BASE_URL}/api/v1/orders/{order_id}" \
     -H "Authorization: Bearer {JWT_TOKEN}"
```

Or list all orders:

```bash
curl -X GET "{API_BASE_URL}/api/v1/orders?status=pending" \
     -H "Authorization: Bearer {JWT_TOKEN}"
```

## Best Practices [â](#best-practices)

### 1. Test All States [â](#_1-test-all-states)

Create a comprehensive test suite covering all quantity patterns:

- 1 order for each pattern (1, 2, 3, 4, 5, 6)
- Multiple quantities per pattern (10, 100, 1000)
- Different tickers and sides (buy/sell)

### 2. Verify State Transitions [â](#_2-verify-state-transitions)

Monitor order state changes:

- Check initial state after creation
- Query status after expected transitions
- Verify fill records match expected behavior

### 3. Test Error Scenarios [â](#_3-test-error-scenarios)

- Invalid quantities (negative, zero)
- Invalid prices
- Expired orders
- Insufficient balance (if applicable)

### 4. Clean Up Test Data [â](#_4-clean-up-test-data)

After testing, cancel pending orders:

```bash
curl -X DELETE "{API_BASE_URL}/api/v1/orders/{order_id}" \
     -H "Authorization: Bearer {JWT_TOKEN}"
```

## Order Status Reference [â](#order-status-reference)

| Status | Description | Can Cancel | Has Fills |
| --- | --- | --- | --- |
| `pending` | Order on book, awaiting fill | Yes | No |
| `partially_filled` | Order partially executed | Yes | Yes |
| `filled` | Order fully executed | No | Yes |
| `cancelled` | Order cancelled by user/system | No | Maybe |
| `rejected` | Order rejected by system | No | No |
| `expired` | Order expired (past expiry time) | No | Maybe |

## Troubleshooting [â](#troubleshooting)

### Issue: Order not created [â](#issue-order-not-created)

**Solution**: Check authentication token, verify all required fields, ensure quantity follows valid pattern

### Issue: Unexpected order status [â](#issue-unexpected-order-status)

**Solution**: Verify quantity last digit matches expected pattern, check order query timing

### Issue: Cannot query order [â](#issue-cannot-query-order)

**Solution**: Ensure order_id is correct, verify authentication, check order hasn't expired

### Issue: Fill records missing [â](#issue-fill-records-missing)

**Solution**: Only orders with quantities ending in 2, 4, or 6 have fills in testing environment

## Additional Resources [â](#additional-resources)

- [Authorization API](./authorization.html) - Obtain JWT token
- [Create Order API](./orders/create.html) - Order creation details
- [Query Orders API](./orders/query.html) - Order query endpoints
- [Cancel Order API](./orders/cancel.html) - Order cancellation

## Support [â](#support)

For testing environment issues or questions:

- Check API response error messages
- Review this testing guide
- Contact development team with order IDs and timestamps

---

**Note**: This testing guide applies only to testing/sandbox environments. Production environments use real blockchain transactions and market conditions.
