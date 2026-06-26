---
name: wooshpay
description: |
  WooshPay Payment Gateway Integration. For creating payments, checking order status, processing refunds, and managing checkout sessions.
  Use scenarios:
  - Create Payment Intent (direct channel payment link)
  - Create Checkout Session (WooshPay hosted checkout page)
  - Query Order Status
  - Process Refunds
  Requires WOOSHPAY_API_KEY environment variable to be configured
---

# WooshPay Payment Management

## Quick Start

### 1. Get Your API Key

Please refer to the official documentation: https://docs.wooshpay.com/3647644m0

### 2. Set API Key

```bash
export WOOSHPAY_API_KEY="your_base64_encoded_api_key"
```

Get your API Key from WooshPay merchant dashboard (Base64 encoded).

### 3. Use the Scripts

## Supported Operations

### 1. Create Payment Intent

Create a payment and get direct channel payment URL (e.g., MoMo, VCB bank).

```bash
python3 scripts/create_payment.py
```

Interactive input: amount, currency, payment method, buyer info, return URL.

**Returns**: Direct payment URL for the selected channel.

### 2. Create Checkout Session

Create a hosted checkout page where customers can select payment method.

```bash
python3 scripts/create_checkout.py
```

Interactive input: product name, description, price, currency, quantity, payment methods, success/cancel URLs.

**Returns**: WooshPay checkout URL to send to customer.

### 3. Query Order Status

Check payment status by order ID.

```bash
python3 scripts/get_payment.py
```

Input: Payment Intent ID (pi_xxxxxx).

### 4. Process Refund

Initiate a refund for a completed payment.

```bash
python3 scripts/refund.py
```

⚠️ Note: Not all payments support refunds. Please confirm with WooshPay support first.

Interactive input: Payment Intent ID, refund reason, amount (optional, default = full refund).

### 5. Cancel Order

Cancel an unpaid payment order.

```bash
python3 scripts/cancel_payment.py
```

## Supported Payment Methods

For the complete list of supported payment methods, please refer to:
https://docs.wooshpay.com/3948703m0

### Common Payment Methods

| Method | Region | Type |
|--------|--------|------|
| momo | Vietnam | Wallet |
| vietcombank | Vietnam | Bank |
| zalo | Vietnam | Wallet |
| shopeepay | Vietnam/SEA | Wallet |
| atome | SEA | Buy Now Pay Later |
| touchngo | Malaysia | Wallet |
| gopay | Indonesia | Wallet |
| ovo | Indonesia | Wallet |
| alipay | China | Wallet |
| alipay_hk | Hong Kong | Wallet |
| wechat_pay | China | Wallet |
| kakao_pay | South Korea | Wallet |
| dana | Indonesia | Wallet |
| boost | Malaysia | Wallet |
| grabpay | SEA | Wallet |
| gcash | Philippines | Wallet |
| true_money | Thailand | Wallet |
| union_pay | China | Card |
| visa | Global | Card |
| mastercard | Global | Card |
| bancontact | Europe | Bank Redirect |
| ideal | Europe | Bank Redirect |
| klarna | Europe | Buy Now Pay Later |

## Supported Currencies

VND, USD, MYR, CNY, EUR, GBP, THB, SGD, IDR, HKD, KRW, PHP, and more.

See: https://docs.wooshpay.com/2447438m0

## Order Status

| Status | Description |
|--------|-------------|
| requires_payment_method | Waiting for payment |
| requires_confirmation | Pending confirmation |
| requires_action | Requires action |
| processing | Processing |
| succeeded | Payment succeeded |
| canceled | Canceled |
| failed | Failed |

## Refund Reasons

| Reason | Description |
|--------|-------------|
| requested_by_customer | Customer requested refund |
| duplicate | Duplicate charge |
| fraudulent | Fraudulent transaction |
| requested_by_merchant | Merchant requested refund |

## Important Notes

- Amount is in smallest currency unit (e.g., VND = cents, USD = cents)
- Currency codes are uppercase (ISO 4217)
- API Key must be Base64 encoded
- Not all payments support refunds - check with WooshPay first

## API Documentation

- Getting Started: https://docs.wooshpay.com/3647644m0
- Payment Methods: https://docs.wooshpay.com/3948703m0
- Supported Currencies: https://docs.wooshpay.com/2447438m0
