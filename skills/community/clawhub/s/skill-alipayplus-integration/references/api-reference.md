# Alipay+ API Reference

Complete API parameter reference for Alipay+ payment integration.

> ⚠️ **CHECK DOCS FIRST**: This file contains endpoint lists only. For request/response schemas, field descriptions, and examples, fetch the official docs using the links below.


---

## ACQP API (Acquirer Service Provider)

### Payment APIs

| API Name | Endpoint | Direction | Description | Documentation |
|----------|----------|-----------|-------------|-------------|
| `pay` (CPM) | `/aps/api/v1/payments/pay` | ACQP → Alipay+ | Customer presents payment code, ACQP requests Alipay+ to deduct from user account | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/pay_user_presented_mode |
| `pay` (MPM-entry code) | `/aps/api/v1/payments/pay` | ACQP → Alipay+ | Merchant presents payment code (entry code), ACQP requests Alipay+ to place order | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/pay_entry_code |
| `pay` (MPM-order code) | `/aps/api/v1/payments/pay` | ACQP → Alpay+ | Merchant presents payment code (order code), ACQP requests Alipay+ to place order | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/pay_order_code |
| `inquiryPayment` | `/aps/api/v1/payments/inquiryPayment` | ACQP → Alipay+ | Proactively query payment status when payment result not received for extended period | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/inquiry_payment |
| `cancelPayment` | `/aps/api/v1/payments/cancelPayment` | ACQP → Alipay+ | Proactively cancel payment when payment timeout or result not received | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/cancel_payment |
| `refund` | `/aps/api/v1/payments/refund` | ACQP → Alipay+ | Initiate refund for successful payment | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/refund |
| `notifyPayment` | Webhook | Alipay+ → ACQP | Alipay+ notifies ACQP of final payment result (success/failure) | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/notify_payment |

### Merchant Registration APIs

| API Name | Endpoint | Direction | Description | Documentation |
|----------|----------|-----------|-------------|-------------|
| `registration` | `/aps/api/v1/merchants/registration` | ACQP → Alipay+ | Register new merchant or update existing merchant information | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/registration |
| `inquiryRegistrationStatus` | `/aps/api/v1/merchants/inquiryRegistrationStatus` | ACQP → Alipay+ | Query merchant registration status | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/inquiry_registration_status |
| `notifyRegistrationStatus` | Webhook | Alipay+ → ACQP | Alipay+ notifies ACQP of merchant registration result | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/notify_registration_status |

### Dispute APIs

| API Name | Endpoint | Direction | Description | Documentation |
|----------|----------|-----------|-------------|-------------|
| `responseRetrieval` | `/aps/api/v1/disputes/responseRetrieval` | ACQP → Alipay+ | Respond to Alipay+ retrieval request, provide required information | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/response_retrieval |
| `responseEscalation` | `/aps/api/v1/disputes/responseEscalation` | ACQP → Alipay+ | Respond to Alipay+ escalation request, provide relevant information | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/response_escalation |
| `initiateRetrieval` | ACQP Endpoint | Alipay+ → ACQP | Alipay+ initiates retrieval request to ACQP | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/initiate_retrieval |
| `initiateEscalation` | ACQP Endpoint | Alipay+ → ACQP | Alipay+ initiates dispute escalation request to ACQP | https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/initiate_escalation |

---

## MPP API (Mobile Payment Provider)

### Payment APIs

| API Name | Endpoint | Direction | Description | Documentation |
|----------|----------|-----------|-------------|-------------|
| `pay` (CPM) | MPP Endpoint | Alipay+ -> MPP | User presents payment code, Alipay+ requests MPP to deduct from user account | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/pay |
| `inquiryPayment` | MPP Endpoint | Alipay+ -> MPP | Alipay+ queries payment status from MPP when payment result not received | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/inquiry_payment |
| `cancelPayment` | MPP Endpoint | Alipay+ -> MPP | Alipay+ cancels payment when payment timeout or result not received | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/cancel_payment |
| `refund` | MPP Endpoint |  Alipay+ -> MPP| Alipay+ initiates refund for a successful payment | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/refund |
| `notifyPayment` | `/aps/api/v1/payments/notifyPayment` | MPP -> Alipay+ | MPP notifies Alipay+ of final payment result (success/failure) | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/notify_payment |


### Authorization & Codes APIs

| API Name | Endpoint | Direction | Description | Documentation |
|----------|----------|-----------|-------------|-------------|
| `applyToken` (MPM) | MPP Endpoint | Alipay+ → MPP | MPP provides access token to Alipay+ | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/apply_token |
| `getPaymentCode` (CPM) | `/aps/api/v1/codes/getPaymentCode` | MPP → Alipay+ | MPP calls this API to get payment code from Alipay+ | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/get_payment_code |
| `userInitiatedPay` (MPM) | `/aps/api/v1/payments/userInitiatedPay` | MPP → Alipay+ | MPP sends order code to Alipay+, Alipay+ decodes and returns payment information | https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/pay_private_order_code |


### Client SDK (Mobile Integration)

| API Name | Platform | Direction | Description | Documentation |
|----------|----------|-----------|-------------|-------------|
| `getCurrentRegion` | Android | MPP app → Client SDK | Get user's current location | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/get_current_region_android |
| `getCurrentRegion` | iOS | MPP app → Client SDK | Get user's current location | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/get_current_region_ios |
| `isAlipayPlusSupportedRegion` | Android | MPP app → Client SDK | Check if user is in Alipay+ supported region | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/supported_region_android |
| `isAlipayPlusSupportedRegion` | iOS | MPP app → Client SDK | Check if user is in Alipay+ supported region | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/supported_region_ios |
| `getAcceptanceMarkLogos` | Android | MPP app → Client SDK | Get acceptance mark logos supported by Alipay+ in specific region | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/get_logos_android |
| `getAcceptanceMarkLogos` | iOS | MPP app → Client SDK | Get acceptance mark logos supported by Alipay+ in specific region | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/get_logos_ios |
| `setConfiguration` | Android | MPP app → Client SDK | Set initialization parameters | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/android_get_configuration |
| `setConfiguration` | iOS | MPP app → Client SDK | Set initialization parameters | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/ios_get_configuration |
| `launch` | Android | MPP app → Client SDK | Start payment process for entry code | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/android_launch |
| `launch` | iOS | MPP app → Client SDK | Start payment process for entry code | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/ios_launch?role=MPP&product=Payment1&version=1.3.0 |
| `getAuthCode` | Android | Client SDK → MPP app | Get authorization code | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/android_get_auth_code |
| `getAuthCode` | iOS | Client SDK → MPP app | Get authorization code | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/ios_get_auth_code |
| `decode` | Android | Client SDK → MPP app | Send decode request to MPP | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/android_decode |
| `decode` | iOS | Client SDK → MPP app | Send decode request to MPP | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/ios_decode |

### Server SDK (Server Integration)

| API Name | Direction | Description | Documentation |
|----------|-----------|-------------|-------------| 
| `CodeIdentificationService.identifyCode` | MPP server → Server SDK | Identify whether code can be processed by Alipay+ | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/identify_code |
| `CodeIdentificationService.init` | MPP server → Server SDK | Initialize Alipay+ Server SDK | https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/init |

---

## Related Documentation

- **ACQP API Documentation**: https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile
- **MPP API Documentation**: https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp
- **MPP SDK Documentation**: https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp

---

_For detailed parameter schemas and request/response examples, refer to the official Alipay+ documentation links above._
