### Skill Name: WeChat Pay Ecosystem & Integration Specialist

### Skill Description

This skill equips an Agent with comprehensive knowledge of WeChat Pay, covering its user-facing operations, technical integration methods, security protocols, and ecosystem evolution. The Agent will be able to guide users through payment processes, assist developers with API implementation, and explain the underlying architecture of Tencent's financial technology platform.

### Core Instruction Set

#### 1. User-Facing Operations

When instructing end-users, categorize operations into three primary scenarios:

- **Active Scanning (User Scans Merchant):**
    - **Scenario:** The merchant displays a QR code (static or dynamic).
    - **Action:** The user opens WeChat, selects "Scan," and scans the code.
    - **Flow:** The user enters the amount (if not fixed) and password to complete the transaction. This is common for street vendors or scanning items on a PC website (Native Pay).
- **Passive Scanning (Merchant Scans User):**
    - **Scenario:** Supermarkets, convenience stores, or transit gates.
    - **Action:** The user opens the "Money" wallet and displays the **Payment Code** (barcode/QR code).
    - **Flow:** The merchant scans the code with a device. For small amounts (typically under 1000 RMB), this is often **password-free** (免密支付) for speed.
- **In-App & Web Payments:**
    - **Scenario:** E-commerce apps, Mini Programs, or Official Accounts.
    - **Action:** The user selects "WeChat Pay" at checkout.
    - **Flow:** The app invokes the WeChat SDK, the user confirms the amount and enters their password within the WeChat interface, then returns to the merchant app.

#### 2. Technical Integration Architecture

For developer queries, break down the integration based on the platform:

- **Native Pay (PC/Offline):**
    - The merchant server generates a QR code using the WeChat Pay API. The user scans it, and the server listens for a **callback** notification to confirm the order status.
- **JSAPI Pay (Official Accounts):**
    - Used within the WeChat browser. It requires the merchant to obtain the user's `openid` and use the JS-SDK to invoke the payment window.
- **App Pay (Mobile SDK):**
    - Requires integrating the WeChat SDK into iOS/Android apps. The flow involves a pre-order creation on the merchant server, obtaining a `prepay_id`, and passing this to the mobile SDK to launch the payment.
- **Mini Program Pay:**
    - Similar to App Pay but utilizes the specific Mini Program API (`wx.requestPayment`). It relies on the user's logged-in state within the Mini Program environment.

#### 3. Security & Risk Management

The Agent must emphasize security protocols and user protection:

- **Authentication:** Explain that WeChat Pay relies on **Real-Name Verification** (linking bank cards and ID).
- **Transaction Security:**
    - **Password-Free Limits:** Inform users that small transactions (e.g., under 1000 RMB) may not require a password to improve efficiency, but this can be disabled in settings.
    - **Risk Controls:** WeChat Pay employs real-time risk monitoring. If a transaction appears suspicious (e.g., new device, unusual location), it may trigger secondary verification or block the payment.
- **Fraud Prevention:**
    - Warn users never to share their **Payment Code** (it acts like a password).
    - Advise against scanning unknown QR codes from untrusted sources to avoid phishing.

#### 4. Ecosystem & Innovation

Highlight the broader capabilities and recent developments:

- **Interconnectivity:** Note the recent interoperability with **UnionPay Cloud QuickPass** and **JD Pay**, allowing cross-platform scanning in certain contexts.
- **Biometric Payment:** Mention advanced hardware integrations like **Brush-to-Pay** (Face ID) and **Palm-to-Pay** (Palm recognition), which allow payments without a phone.
- **Cross-Border:** WeChat Pay supports multiple currencies and is widely used by international tourists in China and by Chinese tourists abroad.

### Troubleshooting & Common Issues

#### "Payment Failed" or "System Error"

- **Diagnosis:** This often indicates a network timeout, insufficient balance, or a risk control block.
- **Solution:** Advise the user to check their network connection, ensure their bank card has funds, or wait 24 hours if the account is flagged for suspicious activity.

#### "Merchant Category Not Supported"

- **Diagnosis:** The user is trying to use a credit card for a transaction type that only allows debit cards (e.g., financial products or real estate).
- **Solution:** Instruct the user to switch the payment method to "Balance" or a "Debit Card" in the payment confirmation screen.

#### Refund Delays

- **Diagnosis:** Users often expect instant refunds.
- **Explanation:** Clarify that while some refunds are instant, bank processing times can take 1-3 business days depending on the issuing bank's policy.

### Skill Extension Suggestions

#### Merchant API V3 Migration

Instruct the Agent on the differences between the legacy V2 API and the modern V3 API (which uses JSON instead of XML and improved signature mechanisms), helping developers migrate legacy systems.

#### Marketing Integration

Expand the skill to include "Cash Vouchers" and "Store Coupons" APIs, teaching how to integrate marketing tools directly into the payment flow to increase conversion rates.

#### Subscription & Withholding

Cover the "Password-Free Withholding" (Auto-debit) API, used for recurring billing scenarios like membership subscriptions or highway tolls.

