# MPP Integration Checklist

**Role**: Mobile Payment Provider (MPP)  
**Overview**: https://docs.alipayplus.com/alipayplus/alipayplus/get_started_mpp
**CPM Integration**: https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_mpp 
**MPM Integration**: https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_mpp
**Reconciliation**: https://docs.alipayplus.com/alipayplus/alipayplus/reconcile_mpp

---

## ✅ Prerequisites

### Account & Qualifications
- [ ] Sign NDA：to cooperate with Alipay+ you need to sign a Non-Disclosure Agreement (NDA) with us.
- [ ] Complete DDQ(Due Diligence Questionnaire)
- [ ] Negotiate contract and sign cooperation agreement: once the NDA is signed, we will approach you to present the Alipay+ payment solution and business proposal, and to negotiate a contract.
- [ ] Obtain Partner ID


### Technical Preparation
- [ ] Set up an account: contact the Alipay+ Solution Architect (SA) and provide an email address. the Alipay+ SA uses the email address to help you set up an account to log in to the Alipay+ Docs center and Alipay+ Developer Center.
- [ ] Get the integration guides: once your account is set up, you can log in to the Alipay+ Docs Center and read the integration guides to familiarize yourself with the Alipay+ products and their integration workflows.
- [ ] Plan for your integration: After reading the integration guides, work with the Alipay+ SA to make an integration plan. The Alipay+ SA helps you figure out the integration scope, for example, which capabilities are required to be integrated and which are optional.
- [ ] Log in to Alipay+ Developer Center and create an application.
- [ ] Generate RSA2 key pair
- [ ] Upload public key to Alipay+ Developer Center
- [ ] Download Alipay+ public key
- [ ] Configure server environment (HTTPS required)
- [ ] Prepare publicly accessible domain name
- [ ] Configure mobile SDK (if applicable)
- [ ] Store credentials securely (environment variables, secret manager)

---

## ✅ Configuration Phase

### Sandbox Environment
- [ ] Obtain sandbox environment Partner ID from Alipay+ Developer Center
- [ ] Configure sandbox environment endpoint, e.g. `https://open-sandbox.alipayplus.com`
- [ ] Configure sandbox environment parameters
- [ ] Test sandbox connectivity
- [ ] Verify sandbox signature


### Production Environment
- [ ] Obtain production environment Partner ID
- [ ] Prepare production environment endpoint, e.g. `https://open.alipayplus.com`
- [ ] Configure production environment parameters
- [ ] Configure production certificates
- [ ] Verify production signature


---

## Development Phase

### Payment APIs

#### CPM (Customer-Presented Mode)
- [ ] Implement `pay`  (`Alipay+ → MPP`) - Alipay+ requests MPP to deduct from user account (using payment code)
- [ ] Implement `inquiryPayment`  (`Alipay+ → MPP`) - Alipay+ queries payment result
- [ ] Implement `cancelPayment`  (`Alipay+ → MPP`) - Alipay+ cancels payment
- [ ] Implement `refund`  (`Alipay+ → MPP`) - Alipay+ initiates refund
- [ ] Implement `notifyPayment` API (`/aps/api/v1/payments/notifyPayment`) - MPP notifies Alipay+ of final payment result

#### MPM (Merchant-Presented Mode)
- [ ] Implement `applyToken`  (`Alipay+ → MPP`) - MPP provides access token to Alipay+
- [ ] Implement `userInitiatedPay` API (`/aps/api/v1/payments/userInitiatedPay`) - MPP sends order code to Alipay+, Alipay+ decodes and returns payment information

### Authorization & Codes APIs
- [ ] Implement `getPaymentCode` API (`/aps/api/v1/codes/getPaymentCode`) - MPP calls this API to get payment code from Alipay+

### MPP Client SDK (Mobile Integration)
- [ ] Integrate `getCurrentRegion` - Get user's current location
- [ ] Integrate `isAlipayPlusSupportedRegion` - Check if user is in Alipay+ supported region
- [ ] Integrate `getAcceptanceMarkLogos` - Get acceptance mark logos supported by Alipay+ in specific region
- [ ] Integrate `setConfiguration` - Set initialization parameters
- [ ] Integrate `launch` - Start payment process for entry code
- [ ] Integrate `getAuthCode` - Get authorization code
- [ ] Integrate `decode` - Send decode request to MPP

### MPP Server SDK (Server Integration)
- [ ] Integrate `CodeIdentificationService.identifyCode` - Identify whether code can be processed by Alipay+
- [ ] Integrate `CodeIdentificationService.init` - Initialize Alipay+ Server SDK

### General Features
- [ ] Implement RSA2 signature generation
- [ ] Implement RSA2 signature verification
- [ ] Implement idempotency for all payment APIs
- [ ] Implement error handling and retry mechanism
- [ ] Implement complete logging for all API calls
- [ ] Implement monitoring and alerting system

### User Interface

#### 1. Scanner Page
- [ ] Implement camera permission handling
- [ ] Display scanner overlay with frame
- [ ] Support QR code and barcode formats

#### 2. Payment Confirmation Page
- [ ] Display merchant name
- [ ] Display payment amount
- [ ] Show payment method selection
- [ ] Implement confirm/cancel buttons

#### 3. Payment Result Page
- [ ] Display success/failure status
- [ ] Show transaction details
- [ ] Implement "Redirect to merchant" navigation

#### 4. Transaction History
- [ ] List recent transactions
- [ ] Display transaction details on tap
- [ ] Implement search/filter functionality

---

## Testing Phase
Before launching your application into production, you need to pass all required test cases on Alipay+ Developer Center in the sandbox.

### Functional Testing
- [ ] Sandbox payment testing (CPM)
- [ ] Sandbox payment testing (MPM)
- [ ] Sandbox refund testing
- [ ] Async notification reception testing
- [ ] Query interface testing
- [ ] Reconciliation file download testing


### Exception Scenario Testing
- [ ] Payment timeout testing
- [ ] Duplicate payment testing
- [ ] Network exception testing
- [ ] Signature error testing
- [ ] Insufficient balance testing
- [ ] User cancellation testing


### User Experience Testing
- [ ] Payment flow smoothness
- [ ] Error message friendliness
- [ ] QR code clarity
- [ ] Page load speed
- [ ] Mobile adaptation

---

## Go-Live Checklist

### Configuration Switching
- [ ] Switch to production environment configuration
- [ ] Verify production certificates
- [ ] Launch your application into production on Alipay+ Developer Center

### Verification Testing
- [ ] Small-amount real payment testing
- [ ] Real refund testing
- [ ] Async notification verification
- [ ] Reconciliation file verification
- [ ] Review Alipay+ brand guidelines

### Monitoring & Alerting
- [ ] Configure transaction monitoring
- [ ] Configure error alerting
- [ ] Configure reconciliation alerting
- [ ] Configure certificate expiration reminder


### Documentation & Training
- [ ] Write operations manual
- [ ] Write troubleshooting procedures
- [ ] Write user operation guide
- [ ] Train customer service team
- [ ] Prepare user FAQ

---

## Daily Operations

### Daily
- [ ] Check transaction success rate
- [ ] Check error logs
- [ ] Check alert information

### Weekly
- [ ] Download reconciliation files
- [ ] Verify transaction discrepancies
- [ ] Process exception orders
- [ ] Analyze payment success rate

### Monthly
- [ ] Check certificate validity period
- [ ] Review security logs
- [ ] Update statistics


---

## FAQ

### Q: Signature verification failed?
A: Check if the key is correct, signature algorithm is RSA2, and character encoding is UTF-8

### Q: Not receiving async notifications?
A: Check if notify_url is publicly accessible, HTTPS certificate is valid, and firewall rules allow traffic

### Q: QR code cannot be recognized?
A: Check QR code size, clarity, encoding format, and error correction level settings

### Q: User reports payment success but order not updated?
A: Check async notification handling logic, idempotency implementation, and database transactions

---

**Last Updated**: 2026-03-31  
**Status**: Initial draft, pending actual integration experience
