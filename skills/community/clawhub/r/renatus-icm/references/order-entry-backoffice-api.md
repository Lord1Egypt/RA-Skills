# Renatus Back Office Order Entry API

This reference is a sanitized, capture-derived map of the Renatus **Orders** page. It records endpoint paths, parameter names, status counts, and JSON key shapes only. It contains no captured credentials, identifiers, addresses, payment data, or response records.

## Safety Boundary

- The capture showed authenticated browser transport through `backoffice.myrenatus.com`; use a current, logged-in Chrome/Brave CDP session. Do not reuse values from the HAR.
- Read calls use `GET /api/queryproxy/execute?url=<target-path>` with target-specific parameters appended to the proxy request.
- Command calls use `POST /api/commandproxy/execute?url=<target-path>` with JSON bodies. The observed browser requests used `x-requested-with` and an XSRF header.
- `POST` endpoints below can create a lead or save an order. They are external actions: run a dry-run/read preflight first and do not call them unless the user explicitly approves the exact customer, products, payment method, and submission state.
- Do not replay captured payloads. Build values from the live browser session and the authorized order only.

## Capture Scope

The July 22, 2026 order-entry capture contains 78 network entries. All 50 query-proxy calls and all four command-proxy calls returned HTTP 200. It covers the Orders page, lead/customer selection, product and payment lookup, and one successful order-container save.

## Read Endpoints

| Target path | Parameters observed | Use |
|---|---|---|
| `/api/orders/customersList` | `Value` | Customer search/list |
| `/api/orders/sellersList` | `Value` | Seller search/list |
| `/api/orders/containers/search` | `CurrentPage`, `PageSize`, `SortDirection`, `SortField`, `TotalCount`, `UserId`, `StatusFilter[n][Join]`, `StatusFilter[n][Data][Item]`, `StatusFilter[n][Data][Operation]` | Existing order-container list |
| `/api/orders/products` | — | Product catalog |
| `/api/orders/agreements` | — | Agreement catalog |
| `/api/orders/availableproductsforcustomer` | `BuyerLeadId`, `IsInternational`, `LeadCountryCode` | Products eligible for the selected customer |
| `/api/orderpayments/downpayments` | `CountryCode`, `ProductIds[]` | Down-payment options for selected products |
| `/api/paymentMethod/getUserPaymentMethods` | `CurrentDate`, `UserId` | Saved payment methods |
| `/api/marketinglead/validatelead` | `Value` | Lead validation |
| `/api/userprofile/current` | — | Current authenticated user |

The page also loads campaign/status, settings, domain, notification, grid-filter, and event-status data. Those calls are contextual UI support, not required order-entry mutations.

## Observed Command Endpoints and Payload Shapes

### `POST /api/marketingLead/customerbyleadid`

Observed twice, returning HTTP 200. JSON shape:

```json
{ "Value": "string", "Key": "string" }
```

### `POST /api/guestRegistration/addcustomer`

Observed once, returning HTTP 200. This can create a customer/lead. JSON key shape:

```text
LeadId, OwnerId, Phone{CountryId, Number},
Address{AddressLine1, AddressLine2, City, State, PostalCode, Country},
Email, FirstName, LastName, SourceId,
IsGuest, IsCustomer, OptIn, CanSms, IsInternationalCustomer
```

### `POST /api/orders/saveordercontainer`

Observed once, returning HTTP 200. This is the order write. Its JSON body has the top-level shape:

```text
Request{
  CustomerUserId,
  Customer{CustomerUserId, CustomerId, Email, FirstName, LastName, Phone{}, Address{}, ParentId, ParentName, Name, IsGuest, Owner, OwnerId, SourceId, ConsentTypeId, IsInternationalCustomer, ...},
  Orders[{OrderId, OrderItems[{OrderId, Id, ProductId, ProductLogo, ProductDescription, IsCommissionable, ProductName, ProductTypeId, AssignedCost, RegularCost, DiscountedCost, DownPaymentAmount, CourseProductTypes, PaymentCycles, HasBilling, TaxRate, ...}]}],
  PaymentOptions[{PaymentMethodId, CCNumber, CCName, CCSecurityCode, CCExpiration, CCCardType, Amount, LastFour, PaymentInfo, TypeId, Type, Address{}, SaveForFuture, IsCardForBilling, IsExisting, ...}],
  BillingItem, Payments, IsSubmitted, IsOrderForMyself, IsBillingOrder, IsOrderInEditMode,
  AggrementSignedInLanguage, AggrementSignedByName,
  OrderAgreements[{OrderId, ProductId, ProductTypeId, AgreementId, AgreementFileName, AgreementTypeId, AgreementTypeName, LastActionById, LastActionByName, AgreementSigned}],
  IgnoreSignature, IPAddress, SavedDateTime, SendEmailToCustomer, EnteredByUserProfileId
}
```

`PaymentOptions` includes payment-related fields. Do not log, copy, or persist their values outside the live approved transaction.

## Observed Order-Entry Sequence

The relevant successful sequence was:

1. Load customer/seller and existing order-container lists.
2. Load `/api/orders/products` and `/api/orders/agreements`.
3. Resolve a selected customer with `customerbyleadid`.
4. Create a customer through `guestRegistration/addcustomer` when needed.
5. Resolve the created/selected customer again with `customerbyleadid`.
6. Read eligible products, down-payment options, and saved payment methods.
7. Save the assembled order through `saveordercontainer`.

## Operational Preflight and Verification

1. Confirm the browser is open to `backoffice.myrenatus.com` and the intended staff user is logged in.
2. Confirm the target customer, products, prices, agreements, payment method, email preference, and whether the order is a draft or submitted order.
3. Perform only the read endpoints first; stop on authentication, CSRF, validation, or data-mismatch failures.
4. Before `saveordercontainer`, obtain explicit authorization for the exact write. Never infer payment or submission values.
5. After a successful write, re-read `/api/orders/containers/search` and verify the expected order state exactly once. Do not retry a write after a timeout until server state is checked.

## Known Limits

This capture establishes route and request-key shapes, but it is not a reusable payment or order template. It does not authorize automated ordering, and it must not be used to reconstruct customer, payment, or agreement values from captured traffic.
