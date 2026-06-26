# ACQP Integration Checklist

**Role**: Acquirer Service Provider  
**Overview**: https://docs.alipayplus.com/alipayplus/alipayplus/get_started_acq
**CPM Integration**: https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_acq
**MPM Integration**: https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_acq
**Reconciliation**: https://docs.alipayplus.com/alipayplus/alipayplus/reconcile_acq

---

## Prerequisites

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

---

## Configuration Phase

### Sandbox Environment
- [ ] Obtain sandbox environment Partner ID from Alipay+ Developer Center
- [ ] Configure sandbox environment parameters
- [ ] Test sandbox connectivity
- [ ] Verify sandbox signature

### Production Environment
- [ ] Obtain production environment Partner ID
- [ ] Configure production environment parameters
- [ ] Configure production certificates
- [ ] Verify production signature

### Webhook Configuration
- [ ] Configure notify_url (HTTPS)
- [ ] Verify webhook receiving functionality
- [ ] Implement signature verification logic

---

## Development Phase

### Payment APIs

#### CPM (Customer-Presented Mode)
- [ ] Implement `pay` API (`/aps/api/v1/payments/pay`) - Customer presents payment code, ACQP requests Alipay+ to deduct
- [ ] Implement `inquiryPayment` API (`/aps/api/v1/payments/inquiryPayment`) - Query payment status
- [ ] Implement `cancelPayment` API (`/aps/api/v1/payments/cancelPayment`) - Cancel payment on timeout
- [ ] Implement `refund` API (`/aps/api/v1/payments/refund`) - Initiate refund
- [ ] Implement `notifyPayment` webhook - Receive payment result notification from Alipay+

#### MPM (Merchant-Presented Mode)
- [ ] Implement `pay` API (entry code) (`/aps/api/v1/payments/pay`) - Merchant presents entry code
- [ ] Implement `pay` API (order code) (`/aps/api/v1/payments/pay`) - Merchant presents order code
- [ ] Implement `inquiryPayment` API (`/aps/api/v1/payments/inquiryPayment`) - Query payment status
- [ ] Implement `cancelPayment` API (`/aps/api/v1/payments/cancelPayment`) - Cancel payment on timeout
- [ ] Implement `refund` API (`/aps/api/v1/payments/refund`) - Initiate refund
- [ ] Implement `notifyPayment` webhook - Receive payment result notification from Alipay+

### Merchant Registration APIs
- [ ] Implement `registration` API (`/aps/api/v1/merchants/registration`) - Register/update merchant
- [ ] Implement `inquiryRegistrationStatus` API (`/aps/api/v1/merchants/inquiryRegistrationStatus`) - Query registration status
- [ ] Implement `notifyRegistrationStatus` webhook - Receive merchant registration result

### Dispute APIs
- [ ] Implement `responseRetrieval` API (`/aps/api/v1/disputes/responseRetrieval`) - Respond to retrieval request
- [ ] Implement `responseEscalation` API (`/aps/api/v1/disputes/responseEscalation`) - Respond to escalation request
- [ ] Implement `initiateRetrieval` webhook - Receive retrieval request from Alipay+
- [ ] Implement `initiateEscalation` webhook - Receive escalation request from Alipay+

### Common Features
- [ ] Implement RSA2 signature generation
- [ ] Implement RSA2 signature verification
- [ ] Implement idempotency handling for all payment APIs
- [ ] Implement error handling and retry mechanism
- [ ] Implement comprehensive logging for all API calls
- [ ] Implement monitoring and alerting system

---

## Testing Phase
Before launching your application into production, you need to pass all required test cases on Alipay+ Developer Center in the sandbox.

### Functional Testing
- [ ] Sandbox payment test (CPM)
- [ ] Sandbox payment test (MPM)
- [ ] Sandbox refund test
- [ ] Asynchronous notification receiving test
- [ ] Query API test
- [ ] Reconciliation file download test (manual download from sandbox SFTP)

### Exception Scenario Testing
- [ ] Payment timeout test
- [ ] Duplicate payment test
- [ ] Network exception test
- [ ] Signature error test
- [ ] Insufficient balance test
- [ ] User cancellation test

### Performance Testing
- [ ] Concurrent payment test
- [ ] Response time test
- [ ] System load test

---

## Go-Live Checklist

### Configuration Switch
- [ ] Switch to production environment configuration
- [ ] Configure production notify_url
- [ ] Verify production certificates
- [ ] Launch your application into production on Alipay+ Developer Center


### Verification Testing
- [ ] Small-amount real payment test
- [ ] Real refund test
- [ ] Asynchronous notification verification
- [ ] Reconciliation file verification

### Monitoring & Alerting
- [ ] Configure transaction monitoring
- [ ] Configure error alerting
- [ ] Configure reconciliation alerting
- [ ] Configure certificate expiration reminder

### Documentation & Training
- [ ] Write operations manual
- [ ] Write troubleshooting procedures
- [ ] Train customer service team
- [ ] Prepare user FAQ

---

## Daily Operations

### Daily
- [ ] Check transaction success rate
- [ ] Check error logs
- [ ] Check alert information

### Weekly
- [ ] Download reconciliation files from SFTP/Partner Workspace
- [ ] Run reconciliation script for difference comparison
- [ ] Verify transaction differences
- [ ] Handle exception orders

### Monthly
- [ ] Check certificate validity period
- [ ] Review security logs
- [ ] Update statistics

---

## FAQ

### Q: Signature verification failed?
A: Check if the key is correct, if the signature algorithm is RSA2, and if the character encoding is UTF-8

### Q: Not receiving asynchronous notifications?
A: Check if notify_url is publicly accessible, if the HTTPS certificate is valid, and if the firewall allows traffic

### Q: Reconciliation file download failed?
A: Check if the date format, file type, and permissions are correct

---

**Last Updated**: 2026-03-31  
**Status**: Initial draft, pending actual integration experience
