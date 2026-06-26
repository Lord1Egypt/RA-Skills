# PassKit Extended Patterns

Overflow reference for the `passkit` skill. Contains advanced patterns that exceed the main skill file's scope.

A single `PKPaymentRequest` can set only one optional advanced payment request
type, such as `recurringPaymentRequest`, `automaticReloadPaymentRequest`,
`deferredPaymentRequest`, Apple Pay Later availability, or
`multiTokenContexts`.

## Contents

- [Recurring Payment Requests](#recurring-payment-requests)
- [Coupon Code Support](#coupon-code-support)
- [Multi-Merchant Payments](#multi-merchant-payments)
- [Deferred Payments](#deferred-payments)
- [Building Pass Bundles](#building-pass-bundles)
- [Updating Passes with Push Notifications](#updating-passes-with-push-notifications)
- [SwiftUI Payment Flow](#swiftui-payment-flow)

## Recurring Payment Requests

Set up subscription-style recurring payments with `PKRecurringPaymentRequest`.

```swift
import PassKit

func createSubscriptionRequest() -> PKPaymentRequest {
    let request = PKPaymentRequest()
    request.merchantIdentifier = "merchant.com.example.app"
    request.countryCode = "US"
    request.currencyCode = "USD"
    request.supportedNetworks = [.visa, .masterCard, .amex]
    request.merchantCapabilities = .threeDSecure

    let monthlyItem = PKRecurringPaymentSummaryItem(
        label: "Monthly Subscription",
        amount: NSDecimalNumber(string: "9.99")
    )
    monthlyItem.intervalUnit = .month
    monthlyItem.intervalCount = 1

    request.paymentSummaryItems = [
        monthlyItem,
        PKPaymentSummaryItem(
            label: "My Service",
            amount: NSDecimalNumber(string: "9.99")
        )
    ]

    let recurringRequest = PKRecurringPaymentRequest(
        paymentDescription: "Monthly Premium",
        regularBilling: monthlyItem,
        managementURL: URL(string: "https://example.com/manage")!
    )
    recurringRequest.billingAgreement = "You will be charged $9.99/month."
    request.recurringPaymentRequest = recurringRequest

    return request
}
```

## Coupon Code Support

Enable coupon codes on the payment sheet and handle validation.
`PKPaymentRequestCouponCodeUpdate` requires a `[PKShippingMethod]`; pass current
or updated methods, or `[]` when unchanged.

```swift
func createRequestWithCoupons() -> PKPaymentRequest {
    let request = createPaymentRequest()
    request.supportsCouponCode = true
    request.couponCode = "" // pre-fill if known
    return request
}

// Handle coupon code entry in the delegate
extension PaymentCoordinator: PKPaymentAuthorizationControllerDelegate {
    func paymentAuthorizationController(
        _ controller: PKPaymentAuthorizationController,
        didChangeCouponCode couponCode: String,
        handler completion: @escaping (PKPaymentRequestCouponCodeUpdate) -> Void
    ) {
        Task {
            do {
                let discount = try await validateCoupon(couponCode)
                let updatedItems = applyDiscount(discount)
                completion(PKPaymentRequestCouponCodeUpdate(
                    errors: nil,
                    paymentSummaryItems: updatedItems,
                    shippingMethods: currentShippingMethods
                ))
            } catch {
                let couponError = PKPaymentRequest.paymentCouponCodeInvalidError(
                    localizedDescription: "Invalid coupon code."
                )
                completion(PKPaymentRequestCouponCodeUpdate(
                    errors: [couponError],
                    paymentSummaryItems: originalItems,
                    shippingMethods: currentShippingMethods
                ))
            }
        }
    }
}
```

## Multi-Merchant Payments

Request separate payment tokens for multiple merchants in one transaction using `PKPaymentTokenContext`.

```swift
func createMultiMerchantRequest() -> PKPaymentRequest {
    let request = PKPaymentRequest()
    request.merchantIdentifier = "merchant.com.example.platform"
    request.countryCode = "US"
    request.currencyCode = "USD"
    request.supportedNetworks = [.visa, .masterCard, .amex]
    request.merchantCapabilities = .threeDSecure

    request.paymentSummaryItems = [
        PKPaymentSummaryItem(
            label: "Hotel Stay",
            amount: NSDecimalNumber(string: "299.00")
        ),
        PKPaymentSummaryItem(
            label: "Car Rental",
            amount: NSDecimalNumber(string: "89.00")
        ),
        PKPaymentSummaryItem(
            label: "Travel Platform",
            amount: NSDecimalNumber(string: "388.00")
        )
    ]

    let hotelContext = PKPaymentTokenContext(
        merchantIdentifier: "merchant.com.example.hotel",
        externalIdentifier: "hotel-booking-123",
        merchantName: "Example Hotel",
        merchantDomain: "hotel.example.com",
        amount: NSDecimalNumber(string: "299.00")
    )

    let carContext = PKPaymentTokenContext(
        merchantIdentifier: "merchant.com.example.carrental",
        externalIdentifier: "car-rental-456",
        merchantName: "Example Car Rental",
        merchantDomain: "carrental.example.com",
        amount: NSDecimalNumber(string: "89.00")
    )

    request.multiTokenContexts = [hotelContext, carContext]
    return request
}
```

## Deferred Payments

Set up payments that charge later, such as hotel bookings or pre-orders.

```swift
func createDeferredPaymentRequest() -> PKPaymentRequest {
    let request = createPaymentRequest()

    let deferredDate = Calendar.current.date(
        byAdding: .day, value: 14, to: Date()
    )!

    let deferredBilling = PKDeferredPaymentSummaryItem(
        label: "Hotel Stay (charged at check-in)",
        amount: NSDecimalNumber(string: "299.00")
    )
    deferredBilling.deferredDate = deferredDate

    let deferredRequest = PKDeferredPaymentRequest(
        paymentDescription: "Hotel Booking - Check-in",
        deferredBilling: deferredBilling,
        managementURL: URL(string: "https://example.com/bookings")!
    )
    deferredRequest.freeCancellationDate = deferredDate
    deferredRequest.freeCancellationDateTimeZone = .current

    request.deferredPaymentRequest = deferredRequest
    return request
}
```

## Building Pass Bundles

A distributable pass is a signed `.pkpass` bundle. Keep the app-side PassKit
code separate from server-side pass generation, but check these fields when a
pass fails to add:

- `passTypeIdentifier` matches the Pass Type ID certificate.
- `teamIdentifier` matches the Apple Developer team that owns the certificate.
- `serialNumber` is unique for that pass type; updating a pass uses the same
  `passTypeIdentifier` and `serialNumber`.
- `manifest.json` includes SHA-1 hashes for every source file, and `signature`
  is a PKCS #7 detached signature over the manifest.
- `.pkpasses` bundles contain up to 10 `.pkpass` files and use the
  `application/vnd.apple.pkpasses` MIME type.

## Updating Passes with Push Notifications

Passes in Wallet can receive push notifications to trigger an update. The flow:

1. The pass JSON includes a `webServiceURL` and `authenticationToken`
2. When the pass is added to Wallet, the device registers with your server
3. To update, send a production APNs pass-update push with an empty JSON payload
4. The device calls your `webServiceURL` to fetch the updated `.pkpass` bundle

The pass-update web service authenticates registration, unregister, and pass
download requests with `authenticationToken`; use the device library identifier
when returning the serial numbers of updated passes. You can update any pass
contents except the authentication token and serial number.

### Server Endpoints (your web service must implement)

| Method | Path | Purpose |
|---|---|---|
| POST | `/v1/devices/{deviceId}/registrations/{passTypeId}/{serialNumber}` | Register device for updates |
| DELETE | `/v1/devices/{deviceId}/registrations/{passTypeId}/{serialNumber}` | Unregister device |
| GET | `/v1/devices/{deviceId}/registrations/{passTypeId}` | Get serial numbers of updated passes |
| GET | `/v1/passes/{passTypeId}/{serialNumber}` | Download the latest pass |

### Checking for Updates In-App

```swift
import PassKit

let library = PKPassLibrary()

// Replace an existing pass with updated data
func updatePass(newPassData: Data) {
    guard let updatedPass = try? PKPass(data: newPassData) else { return }
    if library.containsPass(updatedPass) {
        let replaced = library.replacePass(with: updatedPass)
        if !replaced {
            // Fall back to add-pass UI or report a recoverable update failure.
        }
    }
}
```

## SwiftUI Payment Flow

A complete SwiftUI payment view with availability check, button, and processing.

```swift
import SwiftUI
import PassKit

struct PaymentView: View {
    @State private var paymentStatus: PaymentStatus = .idle
    @State private var coordinator: PaymentCoordinator?

    private var canPay: Bool {
        PKPaymentAuthorizationController.canMakePayments(
            usingNetworks: [.visa, .masterCard, .amex],
            capabilities: .threeDSecure
        )
    }

    var body: some View {
        VStack {
            OrderSummaryView()

            if canPay {
                PayWithApplePayButton(.buy) {
                    processPayment()
                }
                .payWithApplePayButtonStyle(.black)
                .frame(height: 48)
            } else {
                Button("Checkout with Card") {
                    // Fallback payment flow
                }
                .buttonStyle(.borderedProminent)
            }

            if case .error(let message) = paymentStatus {
                Text(message)
                    .foregroundStyle(.red)
                    .font(.caption)
            }
        }
        .padding()
    }

    @MainActor
    private func processPayment() {
        coordinator = PaymentCoordinator { result in
            paymentStatus = result
        }
        coordinator?.startPayment()
    }
}

enum PaymentStatus {
    case idle
    case processing
    case success
    case error(String)
}
```
