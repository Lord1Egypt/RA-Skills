# Alipay+ Integration Flows

Complete workflow diagrams and integration flows for Alipay+ payment scenarios.

---

## Quick Decision Tree

```
User asks about Alipay+ integration
 |
 +-- Offline store payment?
 |   +-- Customer presents payment code, merchant scans --> ACQP CPM
 |   +-- Merchant presents dynamic QR code, customer scans --> ACQP MPM Order Code
 |   +-- Merchant presents static QR code, customer scans --> ACQP MPM Entry Code
 |
 +-- E-wallet payment?
 |   +-- Wallet presents payment code, Alipay+ sends payment request to wallet --> MPP CPM
 |   +-- Wallet scans code, sends decode request to Alipay+ --> MPP MPM Decode
 |   +-- Wallet scans code, opens Oauth aggregated code (enter mainland China scenario) --> MPP MPM Auth
 |
```

---

## Integration Workflows

### Scenario 1: ACQP New Partner Onboarding

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Select Role                                             │
│ └── ACQP (Acquirer Service Provider)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Generate Configuration                                  │
│ └── Run: generate-config.sh                                     │
│ └── Output: alipayplus-config.json template                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Fill Configuration                                      │
│ ├── Partner ID                                                  │
│ ├── Private Key                                                 │
│ ├── Certificates                                                │
│ └── Webhook URLs                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Select Scenario                                         │
│ ├── CPM (Customer-Presented Mode)                               │
│ └── MPM (Merchant-Presented Mode)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Test Signature                                          │
│ └── Run: test-signature.sh                                      │
│ └── Verify RSA2 signature generation/verification               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Configure Webhook                                       │
│ └── Run: debug-notify.sh                                        │
│ └── Test async notification reception                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Sandbox Testing                                         │
│ └── Complete end-to-end testing in sandbox environment          │
│ └── Proceed to production onboarding                            │
└─────────────────────────────────────────────────────────────────┘
```

### Scenario 2: MPP New Partner Onboarding

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Select Role                                             │
│ └── MPP (Mobile Payment Provider)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Generate Configuration                                  │
│ └── Run: generate-config.sh                                     │
│ └── Output: alipayplus-config.json template                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Fill Configuration                                      │
│ ├── Partner ID                                                  │
│ ├── Private Key                                                 │
│ ├── Certificates                                                │
│ └── MPP API Endpoints                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Select Scenario                                         │
│ ├── CPM (Customer-Presented Mode)                               │
│ └── MPM (Merchant-Presented Mode)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Test Signature                                          │
│ └── Run: test-signature.sh                                      │
│ └── Verify RSA2 signature generation/verification               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Configure MPP Endpoints                                 │
│ ├── Payment endpoint                                            │
│ ├── Inquiry endpoint                                            │
│ ├── Cancel/Refund endpoint                                      │
│ └── applyToken endpoints                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Sandbox Testing                                         │
│ └── Complete end-to-end testing in sandbox environment          │
│ └── Proceed to production onboarding                            │
└─────────────────────────────────────────────────────────────────┘
```

### Scenario 3: Async Notification Troubleshooting (for ACQP only)

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Check Webhook Accessibility                             │
│ └── Verify webhook URL is publicly accessible                   │
│ └── Check firewall/proxy configuration                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Review Notification Logs                                │
│ └── Check webhook reception logs                                │
│ └── Identify any error patterns                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Verify Signature                                        │
│ └── Validate Alipay+ signature on notification                  │
│ └── Check certificate validity                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Check Business Logic                                    │
│ └── Verify order validation logic                               │
│ └── Check idempotency handling                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Replay Test                                             │
│ └── Run: debug-notify.sh                                        │
│ └── Replay test notifications to verify fix                     │
└─────────────────────────────────────────────────────────────────┘
```

### Scenario 4: Reconciliation Discrepancy Handling

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Download Reconciliation File                            │
│ ├── Manual download from Alipay+ SFTP server                    │
│ └── Or download from Partner Workspace                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Run Reconciliation Script                               │
│ └── Run: reconciliation.sh                                      │
│ └── Parse statement and compare with local records              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Generate Discrepancy Report                             │
│ └── Identify mismatched transactions                            │
│ └── Categorize discrepancies (missing, amount mismatch, etc.)   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Process Discrepancies                                   │
│ ├── Investigate root cause                                      │
│ ├── Apply corrections                                           │
│ └── Contact Alipay+ support if needed                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Mark Exception Orders                                   │
│ └── Flag exception orders for follow-up                         │
│ └── Document resolution for audit trail                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Payment Flow Diagrams

### ACQP CPM Flow (Customer-Presented Mode)

```
Merchant          Acquirer          Alipay+           MPP
 │                │                  │                 │
 │                │                  │  1: Render and  │
 │                │                  │     display     │
 │                │                  │     payment     │
 │                │                  │     code        │
 │                │                  │◄────────────────│
 │  2: Scan       │                  │                 │
 │     user's     │                  │                 │
 │     payment    │                  │                 │
 │     code       │                  │                 │
 │────────────────────────────────────────────────────>│
 │  3: Send       │                  │                 │
 │     payment    │                  │                 │
 │     code       │                  │                 │
 │───────────────>│                  │                 │
 │                │  4: Identify     │                 │
 │                │     the MPP and  │                 │
 │                │     route the    │                 │
 │                │     payment      │                 │
 │                │◄─────────────────│                 │
 │                │  5: Initiate a   │                 │
 │                │     payment and  │                 │
 │                │     send order   │                 │
 │                │     information  │                 │
 │                │─────────────────>│                 │
 │                │                  │  6: Decode and  │
 │                │                  │     obtain      │
 │                │                  │     customerId  │
 │                │                  │◄────────────────│
 │                │                  │  7: Initiate a  │
 │                │                  │     payment     │
 │                │                  │     with        │
 │                │                  │     customerId  │
 │                │                  │────────────────>│
 │                │                  │                 │  8: Complete
 │                │                  │                 │     payment
 │                │                  │                 │◄────────────────│
 │                │                  │  9: Return      │                 │
 │                │                  │     payment     │                 │
 │                │                  │     result      │                 │
 │                │                  │<────────────────│                 │
 │                │ 10: Return       │                 │                 │
 │                │     payment      │                 │                 │
 │                │     result       │                 │                 │
 │                │<─────────────────│                 │                 │
 │ 11: Return     │                 │                 │                 │
 │     payment    │                 │                 │                 │
 │     result     │                 │                 │                 │
 │<───────────────│                 │                 │                 │
 │                │                  │                 │                 │
 ┌────────────────┴──────────────────┴─────────────────┴─────────────────┐
 │ loop                                                                  │
 │ │               │                  │                 │                │
 │ │ 12: Inquiry   │                  │                 │                │
 │ │     payment   │                  │                 │                │
 │ │     result    │                  │                 │                │
 │ │──────────────>│                  │                 │                │
 │ │               │ 13: Inquiry      │                 │                │
 │ │               │     payment      │                 │                │
 │ │               │     result       │                 │                │
 │ │               │─────────────────>│                 │                │
 │ │               │ 14: Return       │                 │                │
 │ │               │     payment      │                 │                │
 │ │               │     result       │                 │                │
 │ │               │<─────────────────│                 │                │
 │ │ 15: Return    │                  │                 │                │
 │ │     payment   │                  │                 │                │
 │ │     result    │                  │                 │                │
 │ │<──────────────│                  │                 │                │
 │ └─────────────────────────────────────────────────────────────────────┘
 │                │                  │                 │                 │
 │                │                  │ 16: Notify      │                 │
 │                │                  │     payment     │                 │
 │                │                  │     result      │                 │
 │                │                  │<────────────────│                 │
 │                │ 17: Notify       │                 │                 │
 │                │     payment      │                 │                 │
 │                │     result       │                 │                 │
 │                │<─────────────────│                 │                 │
 │ 18: Notify     │                 │                 │                 │
 │     payment    │                 │                 │                 │
 │     result     │                 │                 │                 │
 │<───────────────│                 │                 │                 │
 │                │                  │                 │                 │
```

**Key Design Points:**

| Feature | Description |
|---------|-------------|
| **User-Presented Code** | User renders payment code in MPP wallet, Merchant scans it |
| **Acquirer Routing** | Acquirer identifies the MPP and routes payment to correct Alipay+ channel |
| **Sync + Async** | Synchronous return (step 11) + Async notification (steps 16-18) for reliability |
| **Polling Loop** | Merchant can actively poll to confirm payment status (steps 12-15) |


**Reference:**
https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_acq/accept_payment#EorjE


### ACQP MPM Flow (Merchant-Presented Mode Order Code)

```
User            Merchant          ACQP              Alipay+         MPP App
 │                │                │                  │                │
 │  1: Purchase   │                │                  │                │
 │    goods       │                │                  │                │
 │───────────────>│                │                  │                │
 │                │ 2: Confirm     │                  │                │
 │                │    payment     │                  │                │
 │                │    amount      │                  │                │
 │                │────────┐       │                  │                │
 │                │<───────┘       │                  │                │
 │                │ 3: Select      │                  │                │
 │                │    Alipay+     │                  │                │
 │                │    payment     │                  │                │
 │                │────────┐       │                  │                │
 │                │<───────┘       │                  │                │
 │                │ 4: Send order  │                  │                │
 │                │    info        │                  │                │
 │                │───────────────>│                  │                │
 │                │                │ 5: Call pay API  │                │
 │                │                │    to send order │                │
 │                │                │─────────────────>│                │
 │                │                │                  │ 6: Place order │
 │                │                │                  │────────┐       │
 │                │                │                  │<───────┘       │
 │                │                │                  │ 7: Generate    │
 │                │                │                  │    QR code     │
 │                │                │                  │────────┐       │
 │                │                │                  │<───────┘       │
 │                │                │ 8: Return QR     │                │
 │                │                │    code          │                │
 │                │                │<─────────────────│                │
 │                │ 9: Return QR   │                  │                │
 │                │    code        │                  │                │
 │                │<───────────────│                  │                │
 │                │ 10: Display    │                  │                │
 │                │     QR code    │                  │                │
 │                │────────┐       │                  │                │
 │                │<───────┘       │                  │                │
 │                │                │                  │                │
 │                │                │                  │ 11: Scan QR    │
 │                │                │                  │     code       │
 │                │<───────────────────────────────────────────────────│
 │                │                │                  │                │
 ┌────────────────┴────────────────┴──────────────────┴────────────────┐
 │ loop                                                                │
 │ │                │                │                  │              │
 │ │                │ 12: Inquire    │                  │              │
 │ │                │     payment    │                  │              │
 │ │                │     result     │                  │              │
 │ │                │───────────────>│                  │              │
 │ │                │                │ 13: Call         │              │
 │ │                │                │     inquiryPay.  │              │
 │ │                │                │─────────────────>│              │
 │ │                │                │ 14: Return       │              │
 │ │                │                │     inquiryPay.  │              │
 │ │                │                │<─────────────────│              │
 │ │                │ 15: Return     │                  │              │
 │ │                │     payment    │                  │              │
 │ │                │     result     │                  │              │
 │ │                │<───────────────│                  │              │
 │ └───────────────────────────────────────────────────────────────────┘
 │                │                │                  │                │
 │                │                │                  │ 16: Decode QR  │
 │                │                │                  │     code       │
 │                │                │                  │<───────────────│
 │                │                │                  │ 17: Return     │
 │                │                │                  │     order info │
 │                │                │                  │───────────────>│
 │                │                │                  │                │
 │                │                │                  │                │
 │                │                │                  │                │────────┐ 18: Render cashier page
 │                │                │                  │                │<───────┘ 
 │  19: Confirm   │                │                  │                │
 │      payment   │                │                  │                │
 │────────────────────────────────────────────────────────────────────>│
 │                │                │                  │                │
 │                │                │                  │                │
 │                │                │                  │                │20: Process payment
 │                │                │                  │                │────────┐
 │                │                │                  │ 21: Notify     │<───────┘
 │                │                │                  │     payment    │
 │                │                │                  │     result     │
 │                │                │                  │<───────────────│
 │                │                │ 22: Call notify  │                │
 │                │                │     Payment API  │                │
 │                │                │<─────────────────│                │
 │                │ 23: Notify     │                  │                │
 │                │     payment    │                  │                │
 │                │     result     │                  │                │
 │                │<───────────────│                  │                │
 │                │                │                  │                │
```

**Key Design Points:**

| Feature | Description |
|---------|-------------|
| **Polling Mechanism** | Merchant actively polls for payment result (steps 12-15 in loop) |
| **Dual Notification** | Polling query + final async notification (steps 21-23) for reliability |
| **QR Code Bridge** | QR code connects offline merchant with user's MPP wallet app |
| **Four Phases** | Order creation → Polling → User payment → Result notification | |

**Reference:**
https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_acq/accept_payment_order_code#ghwpK


### ACQP MPM Flow (Merchant-Presented Mode Entry Code)

```
User            Merchant          ACQP              Alipay+         MPP App
 │                │                │                  │                │
 │                │                │                  │ 1: Scan QR     │
 │                │                │                  │     code       │
 │                │<───────────────────────────────────────────────────│
 │                │                │ 2: Open amount   │                │
 │                │                │    input page    │                │
 │                │<───────────────│                  │                │
 │                │                │ 3: Identify      │                │
 │                │                │    Alipay+       │                │
 │                │                │    wallet        │                │
 │                │                │────────┐         │                │
 │                │                │<───────┘         │                │
 │                │                │ 4: Render amount │                │
 │                │                │    input page    │                │
 │                │                │────────┐         │                │
 │                │                │<───────┘         │                │
 │  5: Enter      │                │                  │                │
 │     payment    │                │                  │                │
 │     amount     │                │                  │                │
 │────────────────────────────────>│                  │                │
 │                │                │ 6: Call pay API  │                │
 │                │                │    to send order │                │
 │                │                │    info          │                │
 │                │                │─────────────────>│                │
 │                │                │                  │ 7: Place order │
 │                │                │                  │────────┐       │
 │                │                │                  │<───────┘       │
 │                │                │ 8: Return        │                │
 │                │                │    paymentUrl    │                │
 │                │                │<─────────────────│                │
 │                │                │ 9: Redirect to   │                │
 │                │                │    paymentUrl    │                │
 │                │                │──────────────────────────────────>│
 │                │                │                  │                │
 ┌────────────────┴────────────────┴──────────────────┴────────────────┐
 │ loop                                                                │
 │ │                │                │                  │              │
 │ │                │ 10: Call       │                  │              │
 │ │                │     inquiryPay │                  │              │
 │ │                │     API        │                  │              │
 │ │                │───────────────>│                  │              │
 │ │                │ 11: Return     │                  │              │
 │ │                │     inquiryPay │                  │              │
 │ │                │     result     │                  │              │
 │ │                │<───────────────│                  │              │
 │ └───────────────────────────────────────────────────────────────────┘
 │                │                │                  │                │
 │                │                │                  │ 12: Render     │
 │                │                │                  │     cashier    │
 │                │                │                  │     page       │
 │                │                │                  │────────┐       │
 │                │                │                  │<───────┘       │
 │ 13: Confirm    │                │                  │                │
 │     payment    │                │                  │                │
 │────────────────────────────────────────────────────────────────────>│
 │                │                │                  │                │
 │                │                │                  │ 14: Process    │
 │                │                │                  │     payment    │
 │                │                │                  │────────┐       │
 │                │                │                  │<───────┘       │
 │                │                │                  │ 15: Notify     │
 │                │                │                  │     payment    │
 │                │                │                  │     result     │
 │                │                │                  │<───────────────│
 │                │                │ 16: Call         │                │
 │                │                │     notifyPay.   │                │
 │                │                │     API          │                │
 │                │                │<─────────────────│                │
 │                │ 17: Notify     │                  │                │
 │                │     payment    │                  │                │
 │                │     result     │                  │                │
 │                │<───────────────│                  │                │
 │                │                │                  │                │
```

**Key Design Points:**

| Feature | Description |
|---------|-------------|
| **Merchant-Presented Code** | Merchant displays static QR code, User scans with MPP App |
| **Amount Entry** | User enters payment amount in ACQP page (step 5) |
| **Payment URL Redirect** | ACQP returns paymentUrl, redirects MPP App to cashier page (step 9) |
| **Sync + Async** | Synchronous polling (steps 10-11) + Async notification (steps 15-17) |
| **Polling Loop** | Merchant actively polls for payment result before user confirms |


**Reference:**
https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_acq/accept_payment_entry_code#XuKC3


### MPP CPM Flow (Customer-Presented Mode)

```ascii
User        Merchant    ACQP        Alipay+     Alipay+ Client SDK    MPP Server    MPP APP
 │            │          │            │                  │              │              │
 │1: Open payment code page                              │              │              │
 │────────────────────────────────────────────────────────────────────────────────────>│
 │            │          │            │                  │              │              │
 │            │          │            │                  │2:Call getAcceptanceMarkLogos│
 │            │          │            │                  │<────────────────────────────│
 │            │          │            │                  │              │              │
 │            │          │            │                  │ 3:Return result             │
 │            │          │            │                  │────────────────────────────>│
 │            │          │            │                  │              │              │
 │ 4: Display logos on payment code page                 │              │              │
 │<────────────────────────────────────────────────────────────────────────────────────│
 │            │          │            │                  │              │              │
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ sd Obtain the payment code                                                           │
│ │            │          │            │                  │             │              │
│ │ 5: Open payment code page of MPP app to request a code                             │
│ │───────────────────────────────────────────────────────────────────────────────────>│
│ │            │          │            │                  │              │             │
│ │            │          │            │                  │              │ 6: Request  │ 
│ │            │          │            │                  │              │ payment code│
│ │            │          │            │                  │              │<────────────│
│ │            │          │            │ 7: Call getPaymentCode API to   │             │
│ │            │          │            │           request payment code  │             │
│ │            │          │            │<────────────────────────────────│             │
│ │            │          │            │                  │              │             │
│ │            │          │            │ 8: Return payment code          │             │
│ │            │          │            │────────────────────────────────>│             │
│ │            │          │            │                  │              │             │
│ │            │          │            │                  │              │ 9: Return   │
                                                                         │ payment code│
│ │            │          │            │                  │              │────────────>│
│ │            │          │            │                  │              │             │
│ │            │          │            │                  │              │             │ 10: Display  
│ │            │          │            │                  │              │             │ payment code
│ │            │          │            │                  │              │             │<──────────┐ 
│ │            │          │            │                  │              │             │───────────┘
└──────────────────────────────────────────────────────────────────────────────────────┘
 │            │          │            │                   │              │             │
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ sd Process the payment                                                               │
│ │            │          │            │                  │              │             │
│ │            │11: Merchant scan payment code                                         │
│ │            │──────────────────────────────────────────────────────────────────────>│
│ │            │          │            │                  │              │             │
│ │            │12: Initiate payment with payment code                                 │
│ │            │─────────>│            │                  │              │             │
│ │            │          │13: Send payment request with payment code                  │
│ │            │          │───────────>│                  │              │             │
│ │            │          │            │14: Decode payment code to obtain userId       │
│ │            │          │            │────────┐         │              │             │
│ │            │          │            │<───────┘         │              │             │
│ │            │          │            │15: Call pay API to send payment request       │
│ │            │          │            │────────────────────────────────>│             │
│ │            │          │            │                  │              │16: Process  │
│ │            │          │            │                  │              │  payment    │
│ │            │          │            │                  │              │<──────────┐ │              
│ │            │          │            │                  │              │───────────┘ │              
│ │            │          │            │17: Return payment result        │             │
│ │            │          │            │<────────────────────────────────│             │
│ │            │          │18: Return payment result      │              │             │
│ │            │          │<───────────│                  │              │             │ 
│ │            │19: Return payment result                 │              │             │
│ │            │<─────────│            │                  │              │             │
│ │            │          │            │                  │              │ 20: Send    │
│ │            │          │            │                  │              │payment      │
│ │            │          │            │                  │              │result       │
│ │            │          │            │                  │              │────────────>│
│ │            │          │            │                  │              │             │ 21: Render   
│ │            │          │            │                  │              │             │ payment    
│ │            │          │            │                  │              │             │ result page
│ │            │          │            │                  │              │             │<─────────┐  
│ │            │          │            │                  │              │             │ ─────────┘  
└──────────────────────────────────────────────────────────────────────────────────────┘
```

**Key Design Points:**

| Feature | Description |
|---------|-------------|
| **Customer-Presented Code** | User displays dynamic payment code from MPP App, Merchant scans |
| **Two Phases** | sd Obtain the payment code (steps 1-10) + sd Process the payment (steps 11-21) |
| **Acceptance Mark Logos** | MPP App fetches supported payment method logos before showing code page |
| **Payment Code Generation** | MPP App → MPP Server → Alipay+ → returns payment code to user |
| **Payment Processing** | Merchant scans code → ACQP → Alipay+ → MPP Server processes payment |
| **Sync Response** | The MPP server processes the payment and returns the payment result to Alipay+ (steps 16-19) |



**Reference:**
https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_mpp/accept_payments#tGsY0



### MPP MPM Flow (Merchant-Presented Mode Order Code)

```ascii
User            Merchant/       Alipay+         Alipay+         Alipay+         MPP Server      MPP Client
                ACQP                            Client SDK      Server SDK
 │                │               │                │                │                │                │
 │                │               │                │ 1: Open Scan   │                │                │
 │                │               │                │    page        │                │                │
 │───────────────────────────────────────────────────────────────────────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 2: Call        │
 │                │               │                │                │                │    getAcceptanceMarkLogos API
 │                │               │                │<─────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │               │                │ 3: Return result for getAcceptanceMarkLogos API  │
 │                │               │                │─────────────────────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │ 4: Display logos on Scan page                    │
 │<───────────────────────────────────────────────────────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │               │                │ 5: Scan QR code                 │                │
 │                │<──────────────────────────────────────────────────────────────────────────────────│                │                │               │                │                │                │                │
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 6: Forward     │
 │                │               │                │                │                │    code value  │
 │                │               │                │                │                 <───────────────│
 │                │               │                │                │                │                │
 │                │               │                │                │ 7: Identify code value          │
 │                │               │                │                │<───────────────│                │
 │                │               │                │                │                │                │
 │                │               │                │                │ 8: Return code identification result
 │                │               │                │                │    (isSupported, postCodeMatchActionType)
 │                │               │                │                │───────────────>│                │
 │                │               │                │                │                │                │
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ alt [postMatchActionType=DECODE]                                                                   │
 │                │               │                │                │                │                │
 │                │               │ 9: Call userInitiatedPay to decode code value    │                │
 │                │               │<─────────────────────────────────────────────────│                │
 │                │               │                │                │                │                │
 │                │               │ 10: Handle internal logic by setting different values for actionType
 │                │               │<───────┐       │                │                │                │
 │                │               │────────┘       │                │                │                │
 │                │               │                │                │                │                │
 │                │               │ 11: Return actionType, sdkActionPayload, and payment information  │
 │                │               │─────────────────────────────────────────────────>│                │
 │                │               │                │                │                │                │
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ alt [actionType = HANDLE_BY_PSP]       alt [actionType = HANDLE_BY_SDK]                            │
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 12: Return     │
 │                │               │                │                │                │    payment info│
 │                │               │                │                │                │───────────────>│
 │                │               │                │                │                │                │
 │                │               │                │                │                │                │ 13: Display    
 │                │               │                │                │                │                │ cashier page
 │                │               │                │                │                │                │<───────┐       
 │                │               │                │                │                │                │────────┘       
 ├────────────────────────────────────────────────────────────────────────────────────────────────────┤
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 14: Return actionType and       
 │                │               │                │                │                │ sdkActionPayload           
 │                │               │                │                │                │───────────────>│
 │                │               │                │                │                │                │
 │                │               │                │15: Call handleAction API to pass sdkActionPayload│
 │                │               │<──────────────────────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │               │                │ 16: Take actions according to sdkActionPayload,  │
 │                │               │                │     for example, assemble and open the error page│
 │                │               │                │<───────┐       │                │                │
 │                │               │                │────────┘       │                │                │
 └────────────────────────────────────────────────────────────────────────────────────────────────────┘
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 17: Confirm    │
 │                │               │                │                │                │    payment     │
 │───────────────────────────────────────────────────────────────────────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │                │                │18: Process payment             
 │                │               │                │                │                │<───────────────│
 │                │               │                │                │                │                │
 │                │               │ 19: Notify of payment result via notifyPayment API                │
 │                │               │<─────────────────────────────────────────────────│                │
 │                │               │                │                │                │                │
 │                │ 20: Notify of payment result   │                │                │                │
 │                │ <─────────────│                │                │                │                │
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 21: Return payment result       
 │                │               │                │                │                │───────────────>│
 │                │               │                │                │                │                │
 │                │               │                │                │                │                │ 22: Display    
 │                │               │                │                │                │                │ payment    
 │                │               │                │                │                │                │ result page
 │                │               │                │                │                │                │<───────┐      
 │                │               │                │                │                │                │────────┘      
 │                │               │                │                │                │                │
 │                │ 23: Redirect to merchant result page                                              │
 │                │<──────────────────────────────────────────────────────────────────────────────────│                │                │               │                │                │                │                │
 │                │               │                │                │                │                │
 │                │ 24: Display payment result page (usually in local language)      │                │
 │                │<───────┐      │                │                │                │                │
 │                │────────┘      │                │                │                │                │
 │                │               │                │                │                │                │
```

**Key Design Points:**

| Feature | Description |
|---------|-------------|
| **Merchant-Presented Code** | Merchant displays QR code (dynamic), User scans with MPP App |
| **QR Code Decoding** | MPP Client → MPP Server → Alipay+ Server SDK decodes QR to identify code |
| **Conditional Flow** | alt [postMatchActionType=DECODE] with nested alt [actionType = HANDLE_BY_PSP / HANDLE_BY_SDK] |
| **User Payment Flow** | User confirms payment in MPP Client cashier page |
| **Payment Processing** | MPP Client → MPP Server processes payment, notifies Alipay+ via notifyPayment API |
| **Seven Entities** | User, Merchant/ACQP, Alipay+, Alipay+ Client SDK, Alipay+ Server SDK, MPP Server, MPP Client |
| **24 Steps Total** | Complete flow from scan to payment result display |


**Reference:**
https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_mpp/accept_payments#imyfn


### MPP MPM Flow (Merchant-Presented Mode Entry Code)

```ascii
User            Merchant/       Alipay+         Alipay+         Alipay+         MPP Server      MPP Client
                ACQP                            Client SDK      Server SDK
 │                │               │                │                │                │                │
 │ 1: Open Scan   │               │                │                │                │                │
 │    page        │               │                │                │                │                │
 │───────────────────────────────────────────────────────────────────────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │ 2: Call        │                │                │
 │                │               │                │    getAcceptanceMarkLogos API   │                │
 │                │               │                │<─────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │               │                │ 3: Return result for getAcceptanceMarkLogos API  │
 │                │               │                │─────────────────────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │ 4: Display    │                │                │                │                │
 │                │    logos on   │                │                │                │                │
 │                │    Scan page  │                │                │                │                │
 │<───────────────────────────────────────────────────────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │ 5: Scan QR    │                │                │                │                │
 │                │    code       │                │                │                │                │
 │                │<──────────────────────────────────────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 6: Forward     │
 │                │               │                │                │                │    code value  │
 │                │               │                │                │                │<───────────────│
 │                │               │                │                │                │                │
 │                │               │                │                │ 7: Identify    │                │
 │                │               │                │                │    code value  │                │
 │                │               │                │                │<───────────────│                │
 │                │               │                │                │                │                │
 │                │               │                │                │ 8: Return code │                │
 │                │               │                │                │    identification result        │
 │                │               │                │                │    (isSupported, postMatchActionType)
 │                │               │                │                │───────────────>│                │
 │                │               │                │                │                │                │
alt [postMatchActionType=OPEN_URL]│                │                │                │                │
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 9: Return      │         
 │                │               │                │                │                │ identification result        
 │                │               │                │                │                │───────────────>│
 │                │               │                │                │                │                │
 │                │               │                │ 10: Call launch API of Alipay+ client SDK        │
 │                │               │                │<─────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │ 11: Redirect  │                │                │                │                │
 │                │     user to   │                │                │                │                │
 │                │     merchant  │                │                │                │                │
 │                │     page      │                │                │                │                │
 │                │<───────────────────────────────│                │                │                │
 │                │               │                │                │                │                │
 │                │ 12: Display   │                │                │                │                │
 │                │     amount    │                │                │                │                │
 │                │     input     │                │                │                │                │
 │                │     page      │                │                │                │                │
 │                │<──────────────┐                │                │                │                │
 │                │───────────────┘                │                │                │                │
 │                │               │                │                │                │                │
 │ 13: Enter      │               │                │                │                │                │
 │     payment    │               │                │                │                │                │
 │     amount     │               │                │                │                │                │
 │───────────────>│               │                │                │                │                │
 │                │               │                │                │                │                │
 │                │ 14: Place     │                │                │                │                │
 │                │     order     │                │                │                │                │
 │                │──────────────>│                │                │                │                │
 │                │               │                │                │                │                │
 │                │               │ 15: Construct  │                │                │                │
 │                │               │     order code │                │                │                │
 │                │               │     URL        │                │                │                │
 │                │               │<───────────┐   │                │                │                │
 │                │               │────────────┘   │                │                │                │
 │                │               │                │                │                │                │
 │                │ 16: Return    │                │                │                │                │
 │                │     order     │                │                │                │                │
 │                │     code URL  │                │                │                │                │
 │                │<───────────────                │                │                │                │
 │                │               │                │                │                │                │
 │                │ 17: Pass      │                │                │                │                │
 │                │     order     │                │                │                │                │
 │                │     code URL  │                │                │                │                │
 │                │────────────────────────────────>                │                │                │
 │                │               │                │                │                │                │
 │                │               │                │ 18: Intercept  │                │                │
 │                │               │                │     URL and    │                │                │
 │                │               │                │     obtain     │                │                │
 │                │               │                │     code value │                │                │
 │                │               │                │<─────────────┐ │                │                │
 │                │               │                │──────────────┘ │                │                │
 │                │               │                │                │                │                │
 │                │               │                │ 19: Call       │                │                │
 │                │               │                │     decode API │                │                │
 │                │               │                │     of Alipay+ │                │                │
 │                │               │                │     client SDK │                │                │
 │                │               │                │     to send    │                │                │
 │                │               │                │     code value │                │                │
 │                │               │                │─────────────────────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 20: Send       │
 │                │               │                │                │                │     decoding   │
 │                │               │                │                │                │     request    │
 │                │               │                │                │                │<───────────────│
 │                │               │                │                │                │                │
 │                │               │ 21: Call       │                │                │                │
 │                │               │     userInitiatedPay API        │                │                │
 │                │               │     to decode  │                │                │                │
 │                │               │     code value │                │                │                │
 │                │               │<─────────────────────────────────────────────────│                │
 │                │               │                │                │                │                │
 │                │               │ 22: Handle     │                │                │                │
 │                │               │     internal   │                │                │                │
 │                │               │     logic by   │                │                │                │
 │                │               │     setting    │                │                │                │
 │                │               │     different  │                │                │                │
 │                │               │     values for │                │                │                │
 │                │               │     actionType │                │                │                │
 │                │               │<──────┐        │                │                │                │
 │                │               │───────┘        │                │                │                │
 │                │               │                │                │                │                │
 │                │               │ 23: Return     │                │                │                │
 │                │               │     actionType,│                │                │                │
 │                │               │     sdkActionPayload, and       │                │                │
 │                │               │     payment    │                │                │                │
 │                │               │     information│                │                │                │
 │                │               │─────────────────────────────────────────────────>│                │
 │                │               │                │                │                │                │
 │                │               ┌───────────────────────────────────────────────────────────────────┐
 │                │               │    alt [actionType = HANDLE_BY_PSP]              │                │
 │                │               │                │                │                │                │
 │                │               │                │                │ 24: Return     │                │
 │                │               │                │                │     payment    │                │
 │                │               │                │                │     information│                │
 │                │               │                │                │────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 25: Display    │
 │                │               │                │                │                │     cashier    │
 │                │               │                │                │                │     page       │
 │                │               │                │                │                │<──────┐        │
 │                │               │                │                │                │───────┘        │
 │                │               │                │                │                │                │
 │                │               │───────────────────────────────────────────────────────────────────│ 
 │                │               │ else [actionType = HANDLE_BY_SDK]                                 │
 │                │               │                │                │                │                │
 │                │               │                │                │ 26: Return     │                │
 │                │               │                │                │     actionType │                │
 │                │               │                │                │     and        │                │
 │                │               │                │                │     sdkActionPayload            │
 │                │               │                │                │────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │ 27: Execute    │                │                │
 │                │               │                │     callback   │                │                │
 │                │               │                │     of decode  │                │                │
 │                │               │                │     API to     │                │                │
 │                │               │                │     pass       │                │                │
 │                │               │                │     sdkActionPayload            │                │
 │                │               │                 <─────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │               │                │ 28: Take       │                │                │
 │                │               │                │     actions    │                │                │
 │                │               │                │     according  │                │                │
 │                │               │                │     to         │                │                │
 │                │               │                │     sdkActionPayload, for       │                │
 │                │               │                │     example,   │                │                │
 │                │               │                │     assemble   │                │                │
 │                │               │                │     and open   │                │                │
 │                │               │                │     the error  │                │                │
 │                │               │                │     page       │                │                │
 │                │               │                │<──────────────┐│                │                │                
 │                │               │                │───────────────┘│                │                │                
 │                │               └───────────────────────────────────────────────────────────────────┘
 end
 │                │               │                │                │                │                │
 │ 29: Confirm    │               │                │                │                │                │
 │     payment    │               │                │                │                │                │
 │───────────────────────────────────────────────────────────────────────────────────────────────────>│
 │                │               │                │                │                │                │
 │                │               │                │                │                │ 30: Process    │
 │                │               │                │                │                │     payment    │
 │                │               │                │                │                │<───────────────│
 │                │               │                │                │                │                │
 │                │               │                │                 31: Notify of   │33: Return payment result
 │                │               │                │                │ payment        │───────────────>│
 │                │               │                │                │ result via     │                │
 │                │               │                │                │ notifyPayment API               │
 │                │               │<─────────────────────────────────────────────────│                │
 │                │               │                │                │                │                │
 │                │ 32:Notify of  │                │                │                │                │
 │                │    payment    │                │                │                │                │ 
 │                │    result     │                │                │                │                │    
 │                │<──────────────│                │                │                │                │
 │                │               │                │                │                │                │  34: Display    
 │                │               │                │                │                │                │  payment    
 │                │               │                │                │                │                │  result    
 │                │               │                │                │                │                │  page     
 │                │               │                │                │                │                │<──────┐       
 │                │               │                │                │                │                │───────┘       
 │                │               │                │                │                │                │
 │                │               │                │                │                │                │
 │                │               │                │ 35: (Recommended) Execute callback of decode API │
 │                │               │                │<─────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │ 36: Redirect  │                │                │                │                │
 │                │     to        │                │                │                │                │
 │                │     merchant  │                │                │                │                │
 │                │     result    │                │                │                │                │
 │                │     page      │                │                │                │                │
 │                │<──────────────────────────────────────────────────────────────────────────────────│
 │                │               │                │                │                │                │
 │                │ 37: Display   │                │                │                │                │
 │                │     payment   │                │                │                │                │
 │                │     result    │                │                │                │                │
 │                │     page      │                │                │                │                │
 │                │     (usually  │                │                │                │                │
 │                │     in local  │                │                │                │                │
 │                │     language) │                │                │                │                │
 │                │<───────────┐  │                │                │                │                │
 │                │────────────┘  │                │                │                │                │
 │                │               │                │                │                │                │
```

**Key Design Points:**

| Feature | Description |
|---------|-------------|
| **Merchant-Presented Code** | Merchant displays QR code (static entry code), User scans with MPP App |
| **Entry Code Flow** | postMatchActionType=OPEN_URL triggers redirect to merchant page for amount entry |
| **Conditional Flow** | alt [postMatchActionType=OPEN_URL] with nested alt [actionType = HANDLE_BY_PSP / HANDLE_BY_SDK] |
| **Amount Entry** | User enters payment amount on merchant page (step 13) |
| **Order Code Construction** | Merchant/ACQP constructs order code URL after amount entry |
| **Decode Phase** | MPP Client decodes order code via Alipay+ SDK (steps 19-23) |
| **Payment Confirmation** | User confirms payment in MPP Client cashier page (step 29) |
| **Payment Processing** | MPP Client → MPP Server processes payment, notifies Alipay+ via notifyPayment API |
| **Seven Entities** | User, Merchant/ACQP, Alipay+, Alipay+ Client SDK, Alipay+ Server SDK, MPP Server, MPP Client |
| **37 Steps Total** | Complete flow from scan to payment result display |


**Reference:**
https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_mpp/accept_payments#xSovW



### MPP MPM Flow (Aggregated code payments in the Chinese mainland)

**Reference:**
https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_mpp/accept_payments#dRpox


**Key Design Points:**

| Feature | Description |
|---------|-------------|
| **Merchant-Presented Code** | Merchant displays QR code (static entry code), User scans with MPP App |
| **QR Code Recognition** | MPP Server calls Alipay+ Server SDK to identify code type before routing |
| **Conditional Branching** | Flow determined by `isSupported` and `postCodeMatchActionType` flags |
| **OAuth Redirect Chain** | MPP Client → Merchant Page → Alipay OAuth URL → MPP Client with URL interception |
| **Token Exchange** | Two-step process: `getAuthCode` → `applyToken` to obtain accessToken and customerId |
| **User Identity Creation** | Alipay+ creates Alipay UserId linked to MPP customerId for payment |
| **Client SDK Interception** | Alipay+ Client SDK intercepts redirects (OAuth, order code) to keep flow in-app |
| **Cashier Page** | MPP Client displays native payment confirmation UI |
| **Async Notification Chain** | Payment result propagates: MPP Server → Alipay+ → Merchant/ACQP |
| **Localized Result Page** | Final redirect to Merchant page in local language |
| **In-App Experience** | User completes entire flow within MPP Client without app switching |
| **Multi-Party Architecture** | 6 core roles (User, Merchant/ACQP, Alipay+, Client/Server SDKs, MPP Server, MPP Client) with clear responsibility boundaries |


---

## Related Documents

- **API Reference**: api-reference.md
- **Signature Guide**: signature-guide.md
- **Webhook Guide**: webhook-guide.md
- **Reconciliation Guide**: reconciliation-guide.md

---