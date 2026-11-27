# Square access policy

An access policy limits which endpoints Square connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/squareup#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Square: its 154 read-only endpoints, plus deny rules for the 1 write endpoint a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create squareup --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v2/bank-accounts"},
    {"method": "GET", "path": "v2/bank-accounts/by-v1-id/{id}"},
    {"method": "GET", "path": "v2/bank-accounts/{id}"},
    {"method": "GET", "path": "v2/bookings/custom-attribute-definitions"},
    {"method": "GET", "path": "v2/bookings/custom-attribute-definitions/{id}"},
    {"method": "GET", "path": "v2/bookings/{id}/custom-attributes"},
    {"method": "GET", "path": "v2/bookings/{id}/custom-attributes/{id}"},
    {"method": "GET", "path": "v2/bookings"},
    {"method": "POST", "path": "v2/bookings/availability/search"},
    {"method": "POST", "path": "v2/bookings/bulk-retrieve"},
    {"method": "GET", "path": "v2/bookings/business-booking-profile"},
    {"method": "GET", "path": "v2/bookings/location-booking-profiles"},
    {"method": "GET", "path": "v2/bookings/location-booking-profiles/{id}"},
    {"method": "GET", "path": "v2/bookings/team-member-booking-profiles"},
    {"method": "POST", "path": "v2/bookings/team-member-booking-profiles/bulk-retrieve"},
    {"method": "GET", "path": "v2/bookings/team-member-booking-profiles/{id}"},
    {"method": "GET", "path": "v2/bookings/{id}"},
    {"method": "GET", "path": "v2/cards"},
    {"method": "GET", "path": "v2/cards/{id}"},
    {"method": "GET", "path": "v2/cash-drawers/shifts"},
    {"method": "GET", "path": "v2/cash-drawers/shifts/{id}"},
    {"method": "GET", "path": "v2/cash-drawers/shifts/{id}/events"},
    {"method": "POST", "path": "v2/catalog/batch-retrieve"},
    {"method": "GET", "path": "v2/catalog/info"},
    {"method": "GET", "path": "v2/catalog/list"},
    {"method": "GET", "path": "v2/catalog/object/{id}"},
    {"method": "POST", "path": "v2/catalog/search"},
    {"method": "POST", "path": "v2/catalog/search-catalog-items"},
    {"method": "GET", "path": "v2/channels"},
    {"method": "POST", "path": "v2/channels/bulk-retrieve"},
    {"method": "GET", "path": "v2/channels/{id}"},
    {"method": "GET", "path": "v2/online-checkout/location-settings/{id}"},
    {"method": "GET", "path": "v2/online-checkout/merchant-settings"},
    {"method": "GET", "path": "v2/online-checkout/payment-links"},
    {"method": "GET", "path": "v2/online-checkout/payment-links/{id}"},
    {"method": "GET", "path": "v2/customers/custom-attribute-definitions"},
    {"method": "GET", "path": "v2/customers/custom-attribute-definitions/{id}"},
    {"method": "GET", "path": "v2/customers/{id}/custom-attributes"},
    {"method": "GET", "path": "v2/customers/{id}/custom-attributes/{id}"},
    {"method": "GET", "path": "v2/customers/groups"},
    {"method": "GET", "path": "v2/customers/groups/{id}"},
    {"method": "GET", "path": "v2/customers"},
    {"method": "POST", "path": "v2/customers/bulk-retrieve"},
    {"method": "POST", "path": "v2/customers/search"},
    {"method": "GET", "path": "v2/customers/{id}"},
    {"method": "GET", "path": "v2/customers/segments"},
    {"method": "GET", "path": "v2/customers/segments/{id}"},
    {"method": "GET", "path": "v2/devices"},
    {"method": "GET", "path": "v2/devices/{id}"},
    {"method": "GET", "path": "v2/disputes"},
    {"method": "GET", "path": "v2/disputes/{id}"},
    {"method": "GET", "path": "v2/disputes/{id}/evidence"},
    {"method": "GET", "path": "v2/disputes/{id}/evidence/{id}"},
    {"method": "GET", "path": "v2/employees"},
    {"method": "GET", "path": "v2/employees/{id}"},
    {"method": "GET", "path": "v2/events/types"},
    {"method": "GET", "path": "v2/gift-cards/activities"},
    {"method": "GET", "path": "v2/gift-cards"},
    {"method": "POST", "path": "v2/gift-cards/from-gan"},
    {"method": "POST", "path": "v2/gift-cards/from-nonce"},
    {"method": "GET", "path": "v2/gift-cards/{id}"},
    {"method": "GET", "path": "v2/inventory/adjustment-reasons"},
    {"method": "POST", "path": "v2/inventory/adjustment-reasons/retrieve"},
    {"method": "GET", "path": "v2/inventory/adjustment/{id}"},
    {"method": "GET", "path": "v2/inventory/adjustments/{id}"},
    {"method": "POST", "path": "v2/inventory/batch-retrieve-changes"},
    {"method": "POST", "path": "v2/inventory/batch-retrieve-counts"},
    {"method": "POST", "path": "v2/inventory/changes/batch-retrieve"},
    {"method": "POST", "path": "v2/inventory/counts/batch-retrieve"},
    {"method": "GET", "path": "v2/inventory/physical-count/{id}"},
    {"method": "GET", "path": "v2/inventory/physical-counts/{id}"},
    {"method": "GET", "path": "v2/inventory/{id}"},
    {"method": "GET", "path": "v2/inventory/{id}/changes"},
    {"method": "GET", "path": "v2/invoices"},
    {"method": "POST", "path": "v2/invoices/search"},
    {"method": "GET", "path": "v2/invoices/{id}"},
    {"method": "GET", "path": "v2/labor/break-types"},
    {"method": "GET", "path": "v2/labor/break-types/{id}"},
    {"method": "GET", "path": "v2/labor/employee-wages"},
    {"method": "GET", "path": "v2/labor/employee-wages/{id}"},
    {"method": "POST", "path": "v2/labor/scheduled-shifts/search"},
    {"method": "GET", "path": "v2/labor/scheduled-shifts/{id}"},
    {"method": "POST", "path": "v2/labor/shifts/search"},
    {"method": "GET", "path": "v2/labor/shifts/{id}"},
    {"method": "GET", "path": "v2/labor/team-member-wages"},
    {"method": "GET", "path": "v2/labor/team-member-wages/{id}"},
    {"method": "POST", "path": "v2/labor/timecards/search"},
    {"method": "GET", "path": "v2/labor/timecards/{id}"},
    {"method": "GET", "path": "v2/labor/workweek-configs"},
    {"method": "GET", "path": "v2/locations/custom-attribute-definitions"},
    {"method": "GET", "path": "v2/locations/custom-attribute-definitions/{id}"},
    {"method": "GET", "path": "v2/locations/{id}/custom-attributes"},
    {"method": "GET", "path": "v2/locations/{id}/custom-attributes/{id}"},
    {"method": "GET", "path": "v2/locations"},
    {"method": "GET", "path": "v2/locations/{id}"},
    {"method": "POST", "path": "v2/loyalty/accounts/search"},
    {"method": "GET", "path": "v2/loyalty/accounts/{id}"},
    {"method": "POST", "path": "v2/loyalty/events/search"},
    {"method": "GET", "path": "v2/loyalty/programs"},
    {"method": "GET", "path": "v2/loyalty/programs/{id}"},
    {"method": "POST", "path": "v2/loyalty/programs/{id}/calculate"},
    {"method": "GET", "path": "v2/loyalty/programs/{id}/promotions"},
    {"method": "GET", "path": "v2/loyalty/programs/{id}/promotions/{id}"},
    {"method": "POST", "path": "v2/loyalty/rewards/search"},
    {"method": "GET", "path": "v2/loyalty/rewards/{id}"},
    {"method": "GET", "path": "v2/merchants/custom-attribute-definitions"},
    {"method": "GET", "path": "v2/merchants/custom-attribute-definitions/{id}"},
    {"method": "GET", "path": "v2/merchants/{id}/custom-attributes"},
    {"method": "GET", "path": "v2/merchants/{id}/custom-attributes/{id}"},
    {"method": "GET", "path": "v2/merchants"},
    {"method": "GET", "path": "v2/merchants/{id}"},
    {"method": "POST", "path": "oauth2/token/status"},
    {"method": "GET", "path": "v2/orders/custom-attribute-definitions"},
    {"method": "GET", "path": "v2/orders/custom-attribute-definitions/{id}"},
    {"method": "GET", "path": "v2/orders/{id}/custom-attributes"},
    {"method": "GET", "path": "v2/orders/{id}/custom-attributes/{id}"},
    {"method": "POST", "path": "v2/orders/batch-retrieve"},
    {"method": "POST", "path": "v2/orders/search"},
    {"method": "GET", "path": "v2/orders/{id}"},
    {"method": "GET", "path": "v2/payments"},
    {"method": "GET", "path": "v2/payments/{id}"},
    {"method": "GET", "path": "v2/payouts"},
    {"method": "GET", "path": "v2/payouts/{id}"},
    {"method": "GET", "path": "v2/payouts/{id}/payout-entries"},
    {"method": "GET", "path": "v2/refunds"},
    {"method": "GET", "path": "v2/refunds/{id}"},
    {"method": "GET", "path": "v2/sites"},
    {"method": "GET", "path": "v2/sites/{id}/snippet"},
    {"method": "POST", "path": "v2/subscriptions/search"},
    {"method": "GET", "path": "v2/subscriptions/{id}"},
    {"method": "GET", "path": "v2/subscriptions/{id}/events"},
    {"method": "GET", "path": "v2/team-members/jobs"},
    {"method": "GET", "path": "v2/team-members/jobs/{id}"},
    {"method": "POST", "path": "v2/team-members/search"},
    {"method": "GET", "path": "v2/team-members/{id}"},
    {"method": "GET", "path": "v2/team-members/{id}/wage-setting"},
    {"method": "POST", "path": "v2/terminals/actions/search"},
    {"method": "GET", "path": "v2/terminals/actions/{id}"},
    {"method": "POST", "path": "v2/terminals/checkouts/search"},
    {"method": "GET", "path": "v2/terminals/checkouts/{id}"},
    {"method": "POST", "path": "v2/terminals/refunds/search"},
    {"method": "GET", "path": "v2/terminals/refunds/{id}"},
    {"method": "GET", "path": "v2/locations/{id}/transactions"},
    {"method": "GET", "path": "v2/locations/{id}/transactions/{id}"},
    {"method": "POST", "path": "v2/transfer-orders/search"},
    {"method": "GET", "path": "v2/transfer-orders/{id}"},
    {"method": "GET", "path": "v1/{id}/orders"},
    {"method": "GET", "path": "v1/{id}/orders/{id}"},
    {"method": "POST", "path": "v2/vendors/bulk-retrieve"},
    {"method": "POST", "path": "v2/vendors/search"},
    {"method": "GET", "path": "v2/vendors/{id}"},
    {"method": "GET", "path": "v2/webhooks/event-types"},
    {"method": "GET", "path": "v2/webhooks/subscriptions"},
    {"method": "GET", "path": "v2/webhooks/subscriptions/{id}"}
  ],
  "deny": [
    {"method": "GET", "path": "v2/devices/codes"}
  ]
}
```

## Endpoints

The Square endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v2/apple-pay/domains | write | applepay | Activates a domain for use with Apple Pay on the Web and Square. |
| GET | v2/bank-accounts | read | bankaccounts | Returns a list of BankAccount objects linked to a Square account. |
| POST | v2/bank-accounts | write | bankaccounts | Store a bank account on file for a square account. |
| GET | v2/bank-accounts/by-v1-id/{id} | read | bankaccounts | Returns details of a BankAccount identified by V1 bank account ID. |
| GET | v2/bank-accounts/{id} | read | bankaccounts | Retrieve details of a BankAccount bank account linked to a Square account. |
| POST | v2/bank-accounts/{id}/disable | write | bankaccounts | Disable a bank account. |
| GET | v2/bookings/custom-attribute-definitions | read | bookingcustomattributes | Get all bookings custom attribute definitions. |
| POST | v2/bookings/custom-attribute-definitions | write | bookingcustomattributes | Creates a bookings custom attribute definition. |
| GET | v2/bookings/custom-attribute-definitions/{id} | read | bookingcustomattributes | Retrieves a bookings custom attribute definition. |
| PUT | v2/bookings/custom-attribute-definitions/{id} | write | bookingcustomattributes | Updates a bookings custom attribute definition. |
| DELETE | v2/bookings/custom-attribute-definitions/{id} | write | bookingcustomattributes | Deletes a bookings custom attribute definition. |
| POST | v2/bookings/custom-attributes/bulk-delete | write | bookingcustomattributes | Bulk deletes bookings custom attributes. |
| POST | v2/bookings/custom-attributes/bulk-upsert | write | bookingcustomattributes | Bulk upserts bookings custom attributes. |
| GET | v2/bookings/{id}/custom-attributes | read | bookingcustomattributes | Lists a booking's custom attributes. |
| GET | v2/bookings/{id}/custom-attributes/{id} | read | bookingcustomattributes | Retrieves a bookings custom attribute. |
| PUT | v2/bookings/{id}/custom-attributes/{id} | write | bookingcustomattributes | Upserts a bookings custom attribute. |
| DELETE | v2/bookings/{id}/custom-attributes/{id} | write | bookingcustomattributes | Deletes a bookings custom attribute. |
| GET | v2/bookings | read | bookings | Retrieve a collection of bookings. |
| POST | v2/bookings | write | bookings | Creates a booking. |
| POST | v2/bookings/availability/search | read | bookings | Searches for availabilities for booking. |
| POST | v2/bookings/bulk-retrieve | read | bookings | Bulk-Retrieves a list of bookings by booking IDs. |
| GET | v2/bookings/business-booking-profile | read | bookings | Retrieves a seller's booking profile. |
| GET | v2/bookings/location-booking-profiles | read | bookings | Lists location booking profiles of a seller. |
| GET | v2/bookings/location-booking-profiles/{id} | read | bookings | Retrieves a seller's location booking profile. |
| GET | v2/bookings/team-member-booking-profiles | read | bookings | Lists booking profiles for team members. |
| POST | v2/bookings/team-member-booking-profiles/bulk-retrieve | read | bookings | Retrieves one or more team members' booking profiles. |
| GET | v2/bookings/team-member-booking-profiles/{id} | read | bookings | Retrieves a team member's booking profile. |
| GET | v2/bookings/{id} | read | bookings | Retrieves a booking. |
| PUT | v2/bookings/{id} | write | bookings | Updates a booking. |
| POST | v2/bookings/{id}/cancel | write | bookings | Cancels an existing booking. |
| GET | v2/cards | read | cards | Retrieves a list of cards owned by the account making the request. |
| POST | v2/cards | write | cards | Adds a card on file to an existing merchant. |
| GET | v2/cards/{id} | read | cards | Retrieves details for a specific Card. |
| POST | v2/cards/{id}/disable | write | cards | Disables the card, preventing any further updates or charges. |
| GET | v2/cash-drawers/shifts | read | cashdrawers | Provides the details for all of the cash drawer shifts for a location in a date range. |
| GET | v2/cash-drawers/shifts/{id} | read | cashdrawers | Provides the summary details for a single cash drawer shift. |
| GET | v2/cash-drawers/shifts/{id}/events | read | cashdrawers | Provides a paginated list of events for a single cash drawer shift. |
| POST | v2/catalog/batch-delete | write | catalog | Deletes a set of CatalogItems based on the provided list of target IDs and returns a set of successfully deleted IDs in the response. |
| POST | v2/catalog/batch-retrieve | read | catalog | Returns a set of objects based on the provided ID. |
| POST | v2/catalog/batch-upsert | write | catalog | Creates or updates up to 10,000 target objects based on the provided list of objects. |
| POST | v2/catalog/images | write | catalog | Uploads an image file to be represented by a CatalogImage object that can be linked to an existing CatalogObject instance. |
| PUT | v2/catalog/images/{id} | write | catalog | Uploads a new image file to replace the existing one in the specified CatalogImage object. |
| GET | v2/catalog/info | read | catalog | Retrieves information about the Square Catalog API, such as batch size limits that can be used by the BatchUpsertCatalogObjects endpoint. |
| GET | v2/catalog/list | read | catalog | Returns a list of all CatalogObjects of the specified types in the catalog. |
| POST | v2/catalog/object | write | catalog | Creates a new or updates the specified CatalogObject. |
| GET | v2/catalog/object/{id} | read | catalog | Returns a single CatalogItem as a CatalogObject based on the provided ID. |
| DELETE | v2/catalog/object/{id} | write | catalog | Deletes a single CatalogObject based on the provided ID and returns the set of successfully deleted IDs in the response. |
| POST | v2/catalog/search | read | catalog | Searches for CatalogObject of any type by matching supported search attribute values, excluding custom attribute values on items or item variations, against one or more of... |
| POST | v2/catalog/search-catalog-items | read | catalog | Searches for catalog items or item variations by matching supported search attribute values, including custom attribute values, against one or more of the specified query filters. |
| POST | v2/catalog/update-item-modifier-lists | write | catalog | Updates the CatalogModifierList objects that apply to the targeted CatalogItem without having to perform an upsert on the entire item. |
| POST | v2/catalog/update-item-taxes | write | catalog | Updates the CatalogTax objects that apply to the targeted CatalogItem without having to perform an upsert on the entire item. |
| GET | v2/channels | read | channels | ListChannels. |
| POST | v2/channels/bulk-retrieve | read | channels | BulkRetrieveChannels. |
| GET | v2/channels/{id} | read | channels | RetrieveChannel. |
| POST | v2/locations/{id}/checkouts | write | checkout | Links a checkoutId to a checkout_page_url that customers are directed to in order to provide their payment information using a payment processing workflow hosted on connect.squareup.com. |
| GET | v2/online-checkout/location-settings/{id} | read | checkout | Retrieves the location-level settings for a Square-hosted checkout page. |
| PUT | v2/online-checkout/location-settings/{id} | write | checkout | Updates the location-level settings for a Square-hosted checkout page. |
| GET | v2/online-checkout/merchant-settings | read | checkout | Retrieves the merchant-level settings for a Square-hosted checkout page. |
| PUT | v2/online-checkout/merchant-settings | write | checkout | Updates the merchant-level settings for a Square-hosted checkout page. |
| GET | v2/online-checkout/payment-links | read | checkout | Lists all payment links. |
| POST | v2/online-checkout/payment-links | write | checkout | Creates a Square-hosted checkout page. |
| GET | v2/online-checkout/payment-links/{id} | read | checkout | Retrieves a payment link. |
| PUT | v2/online-checkout/payment-links/{id} | write | checkout | Updates a payment link. |
| DELETE | v2/online-checkout/payment-links/{id} | write | checkout | Deletes a payment link. |
| GET | v2/customers/custom-attribute-definitions | read | customercustomattributes | Lists the customer-related custom attribute definitions that belong to a Square seller account. |
| POST | v2/customers/custom-attribute-definitions | write | customercustomattributes | Creates a customer-related custom attribute definition for a Square seller account. |
| GET | v2/customers/custom-attribute-definitions/{id} | read | customercustomattributes | Retrieves a customer-related custom attribute definition from a Square seller account. |
| PUT | v2/customers/custom-attribute-definitions/{id} | write | customercustomattributes | Updates a customer-related custom attribute definition for a Square seller account. |
| DELETE | v2/customers/custom-attribute-definitions/{id} | write | customercustomattributes | Deletes a customer-related custom attribute definition from a Square seller account. |
| POST | v2/customers/custom-attributes/bulk-upsert | write | customercustomattributes | Creates or updates custom attributes for customer profiles as a bulk operation. |
| GET | v2/customers/{id}/custom-attributes | read | customercustomattributes | Lists the custom attributes associated with a customer profile. |
| GET | v2/customers/{id}/custom-attributes/{id} | read | customercustomattributes | Retrieves a custom attribute associated with a customer profile. |
| POST | v2/customers/{id}/custom-attributes/{id} | write | customercustomattributes | Creates or updates a custom attribute for a customer profile. |
| DELETE | v2/customers/{id}/custom-attributes/{id} | write | customercustomattributes | Deletes a custom attribute associated with a customer profile. |
| GET | v2/customers/groups | read | customergroups | Retrieves the list of customer groups of a business. |
| POST | v2/customers/groups | write | customergroups | Creates a new customer group for a business. |
| GET | v2/customers/groups/{id} | read | customergroups | Retrieves a specific customer group as identified by the group_id value. |
| PUT | v2/customers/groups/{id} | write | customergroups | Updates a customer group as identified by the group_id value. |
| DELETE | v2/customers/groups/{id} | write | customergroups | Deletes a customer group as identified by the group_id value. |
| GET | v2/customers | read | customers | Lists customer profiles associated with a Square account. |
| POST | v2/customers | write | customers | Creates a new customer for a business. |
| POST | v2/customers/bulk-create | write | customers | Creates multiple customer profiles for a business. |
| POST | v2/customers/bulk-delete | write | customers | Deletes multiple customer profiles. |
| POST | v2/customers/bulk-retrieve | read | customers | Retrieves multiple customer profiles. |
| POST | v2/customers/bulk-update | write | customers | Updates multiple customer profiles. |
| POST | v2/customers/search | read | customers | Searches the customer profiles associated with a Square account using one or more supported query filters. |
| GET | v2/customers/{id} | read | customers | Returns details for a single customer. |
| PUT | v2/customers/{id} | write | customers | Updates a customer profile. |
| DELETE | v2/customers/{id} | write | customers | Deletes a customer profile from a business. |
| POST | v2/customers/{id}/cards | write | customers | Adds a card on file to an existing customer. |
| DELETE | v2/customers/{id}/cards/{id} | write | customers | Removes a card on file from a customer. |
| PUT | v2/customers/{id}/groups/{id} | write | customers | Adds a group membership to a customer. |
| DELETE | v2/customers/{id}/groups/{id} | write | customers | Removes a group membership from a customer. |
| GET | v2/customers/segments | read | customersegments | Retrieves the list of customer segments of a business. |
| GET | v2/customers/segments/{id} | read | customersegments | Retrieves a specific customer segment as identified by the segment_id value. |
| GET | v2/devices | read | devices | List devices associated with the merchant. |
| GET | v2/devices/codes | write | devices | Lists all DeviceCodes associated with the merchant. Kept out of read: returns device pairing codes (credentials). |
| POST | v2/devices/codes | write | devices | Creates a DeviceCode that can be used to login to a Square Terminal device to enter the connected terminal mode. |
| GET | v2/devices/codes/{id} | write | devices | Retrieves DeviceCode with the associated ID. Kept out of read: returns device pairing codes (credentials). |
| GET | v2/devices/{id} | read | devices | Retrieves Device with the associated device_id. |
| GET | v2/disputes | read | disputes | Returns a list of disputes associated with a particular account. |
| GET | v2/disputes/{id} | read | disputes | Returns details about a specific dispute. |
| POST | v2/disputes/{id}/accept | write | disputes | Accepts the loss on a dispute. |
| GET | v2/disputes/{id}/evidence | read | disputes | Returns a list of evidence associated with a dispute. |
| POST | v2/disputes/{id}/evidence-files | write | disputes | Uploads a file to use as evidence in a dispute challenge. |
| POST | v2/disputes/{id}/evidence-text | write | disputes | Uploads text to use as evidence for a dispute challenge. |
| GET | v2/disputes/{id}/evidence/{id} | read | disputes | Returns the metadata for the evidence specified in the request URL path. |
| DELETE | v2/disputes/{id}/evidence/{id} | write | disputes | Removes specified evidence from a dispute. |
| POST | v2/disputes/{id}/submit-evidence | write | disputes | Submits evidence to the cardholder's bank. |
| GET | v2/employees | read | employees | ListEmployees. |
| GET | v2/employees/{id} | read | employees | RetrieveEmployee. |
| POST | v2/events | write | events | Search for Square API events that occur within a 28-day timeframe. |
| PUT | v2/events/disable | write | events | Disables events to prevent them from being searchable. |
| PUT | v2/events/enable | write | events | Enables events to make them searchable. |
| GET | v2/events/types | read | events | Lists all event types that you can subscribe to as webhooks or query using the Events API. |
| GET | v2/gift-cards/activities | read | giftcardactivities | Lists gift card activities. |
| POST | v2/gift-cards/activities | write | giftcardactivities | Creates a gift card activity to manage the balance or state of a gift card. |
| GET | v2/gift-cards | read | giftcards | Lists all gift cards. |
| POST | v2/gift-cards | write | giftcards | Creates a digital gift card or registers a physical (plastic) gift card. |
| POST | v2/gift-cards/from-gan | read | giftcards | Retrieves a gift card using the gift card account number (GAN). |
| POST | v2/gift-cards/from-nonce | read | giftcards | Retrieves a gift card using a secure payment token that represents the gift card. |
| GET | v2/gift-cards/{id} | read | giftcards | Retrieves a gift card using the gift card ID. |
| POST | v2/gift-cards/{id}/link-customer | write | giftcards | Links a customer to a gift card, which is also referred to as adding a card on file. |
| POST | v2/gift-cards/{id}/unlink-customer | write | giftcards | Unlinks a customer from a gift card, which is also referred to as removing a card on file. |
| GET | v2/inventory/adjustment-reasons | read | inventory | Returns the standard and custom inventory adjustment reasons available to the seller. |
| POST | v2/inventory/adjustment-reasons/create | write | inventory | Creates a custom inventory adjustment reason. |
| POST | v2/inventory/adjustment-reasons/delete | write | inventory | Soft deletes a custom inventory adjustment reason. |
| POST | v2/inventory/adjustment-reasons/restore | write | inventory | Restores a soft-deleted custom inventory adjustment reason. |
| POST | v2/inventory/adjustment-reasons/retrieve | read | inventory | Returns the inventory adjustment reason identified by the provided reason_id. |
| PUT | v2/inventory/adjustment-reasons/update | write | inventory | Updates a custom inventory adjustment reason. |
| GET | v2/inventory/adjustment/{id} | read | inventory | Deprecated version of RetrieveInventoryAdjustment after the endpoint URL is updated to conform to the standard convention. |
| PUT | v2/inventory/adjustments/update | write | inventory | Applies an update to the provided adjustment. |
| GET | v2/inventory/adjustments/{id} | read | inventory | Returns the InventoryAdjustment object with the provided adjustment_id. |
| POST | v2/inventory/batch-change | write | inventory | Deprecated version of BatchChangeInventory after the endpoint URL is updated to conform to the standard convention. |
| POST | v2/inventory/batch-retrieve-changes | read | inventory | Deprecated version of BatchRetrieveInventoryChanges after the endpoint URL is updated to conform to the standard convention. |
| POST | v2/inventory/batch-retrieve-counts | read | inventory | Deprecated version of BatchRetrieveInventoryCounts after the endpoint URL is updated to conform to the standard convention. |
| POST | v2/inventory/changes/batch-create | write | inventory | Applies adjustments and counts to the provided item quantities. |
| POST | v2/inventory/changes/batch-retrieve | read | inventory | Returns historical physical counts and adjustments based on the provided filter criteria. |
| POST | v2/inventory/counts/batch-retrieve | read | inventory | Returns current counts for the provided CatalogObjects at the requested Locations. |
| GET | v2/inventory/physical-count/{id} | read | inventory | Deprecated version of RetrieveInventoryPhysicalCount after the endpoint URL is updated to conform to the standard convention. |
| GET | v2/inventory/physical-counts/{id} | read | inventory | Returns the InventoryPhysicalCount object with the provided physical_count_id. |
| GET | v2/inventory/{id} | read | inventory | Retrieves the current calculated stock count for a given CatalogObject at a given set of Locations. |
| GET | v2/inventory/{id}/changes | read | inventory | Returns a set of physical counts and inventory adjustments for the provided CatalogObject at the requested Locations. |
| GET | v2/invoices | read | invoices | Returns a list of invoices for a given location. |
| POST | v2/invoices | write | invoices | Creates a draft invoice for an order created using the Orders API. |
| POST | v2/invoices/search | read | invoices | Searches for invoices from a location specified in the filter. |
| GET | v2/invoices/{id} | read | invoices | Retrieves an invoice by invoice ID. |
| PUT | v2/invoices/{id} | write | invoices | Updates an invoice. |
| DELETE | v2/invoices/{id} | write | invoices | Deletes the specified invoice. |
| POST | v2/invoices/{id}/attachments | write | invoices | Uploads a file and attaches it to an invoice. |
| DELETE | v2/invoices/{id}/attachments/{id} | write | invoices | Removes an attachment from an invoice and permanently deletes the file. |
| POST | v2/invoices/{id}/cancel | write | invoices | Cancels an invoice. |
| POST | v2/invoices/{id}/publish | write | invoices | Publishes the specified draft invoice. |
| GET | v2/labor/break-types | read | labor | Returns a paginated list of BreakType instances for a business. |
| POST | v2/labor/break-types | write | labor | Creates a new BreakType. |
| GET | v2/labor/break-types/{id} | read | labor | Returns a single BreakType specified by id. |
| PUT | v2/labor/break-types/{id} | write | labor | Updates an existing BreakType. |
| DELETE | v2/labor/break-types/{id} | write | labor | Deletes an existing BreakType. |
| GET | v2/labor/employee-wages | read | labor | Returns a paginated list of EmployeeWage instances for a business. |
| GET | v2/labor/employee-wages/{id} | read | labor | Returns a single EmployeeWage specified by id. |
| POST | v2/labor/scheduled-shifts | write | labor | Creates a scheduled shift by providing draft shift details such as job ID, team member assignment, and start and end times. |
| POST | v2/labor/scheduled-shifts/bulk-publish | write | labor | Publishes 1 - 100 scheduled shifts. |
| POST | v2/labor/scheduled-shifts/search | read | labor | Returns a paginated list of scheduled shifts, with optional filter and sort settings. |
| GET | v2/labor/scheduled-shifts/{id} | read | labor | Retrieves a scheduled shift by ID. |
| PUT | v2/labor/scheduled-shifts/{id} | write | labor | Updates the draft shift details for a scheduled shift. |
| POST | v2/labor/scheduled-shifts/{id}/publish | write | labor | Publishes a scheduled shift. |
| POST | v2/labor/shifts | write | labor | Creates a new Shift. |
| POST | v2/labor/shifts/search | read | labor | Returns a paginated list of Shift records for a business. |
| GET | v2/labor/shifts/{id} | read | labor | Returns a single Shift specified by id. |
| PUT | v2/labor/shifts/{id} | write | labor | Updates an existing Shift. |
| DELETE | v2/labor/shifts/{id} | write | labor | Deletes a Shift. |
| GET | v2/labor/team-member-wages | read | labor | Returns a paginated list of TeamMemberWage instances for a business. |
| GET | v2/labor/team-member-wages/{id} | read | labor | Returns a single TeamMemberWage specified by id. |
| POST | v2/labor/timecards | write | labor | Creates a new Timecard. |
| POST | v2/labor/timecards/search | read | labor | Returns a paginated list of Timecard records for a business. |
| GET | v2/labor/timecards/{id} | read | labor | Returns a single Timecard specified by id. |
| PUT | v2/labor/timecards/{id} | write | labor | Updates an existing Timecard. |
| DELETE | v2/labor/timecards/{id} | write | labor | Deletes a Timecard. |
| GET | v2/labor/workweek-configs | read | labor | Returns a list of WorkweekConfig instances for a business. |
| PUT | v2/labor/workweek-configs/{id} | write | labor | Updates a WorkweekConfig. |
| GET | v2/locations/custom-attribute-definitions | read | locationcustomattributes | Lists the location-related custom attribute definitions that belong to a Square seller account. |
| POST | v2/locations/custom-attribute-definitions | write | locationcustomattributes | Creates a location-related custom attribute definition for a Square seller account. |
| GET | v2/locations/custom-attribute-definitions/{id} | read | locationcustomattributes | Retrieves a location-related custom attribute definition from a Square seller account. |
| PUT | v2/locations/custom-attribute-definitions/{id} | write | locationcustomattributes | Updates a location-related custom attribute definition for a Square seller account. |
| DELETE | v2/locations/custom-attribute-definitions/{id} | write | locationcustomattributes | Deletes a location-related custom attribute definition from a Square seller account. |
| POST | v2/locations/custom-attributes/bulk-delete | write | locationcustomattributes | Deletes custom attributes for locations as a bulk operation. |
| POST | v2/locations/custom-attributes/bulk-upsert | write | locationcustomattributes | Creates or updates custom attributes for locations as a bulk operation. |
| GET | v2/locations/{id}/custom-attributes | read | locationcustomattributes | Lists the custom attributes associated with a location. |
| GET | v2/locations/{id}/custom-attributes/{id} | read | locationcustomattributes | Retrieves a custom attribute associated with a location. |
| POST | v2/locations/{id}/custom-attributes/{id} | write | locationcustomattributes | Creates or updates a custom attribute for a location. |
| DELETE | v2/locations/{id}/custom-attributes/{id} | write | locationcustomattributes | Deletes a custom attribute associated with a location. |
| GET | v2/locations | read | locations | Provides details about all of the seller's locations, including those with an inactive status. |
| POST | v2/locations | write | locations | Creates a location. |
| GET | v2/locations/{id} | read | locations | Retrieves details of a single location. |
| PUT | v2/locations/{id} | write | locations | Updates a location. |
| POST | v2/loyalty/accounts | write | loyalty | Creates a loyalty account. |
| POST | v2/loyalty/accounts/search | read | loyalty | Searches for loyalty accounts in a loyalty program. |
| GET | v2/loyalty/accounts/{id} | read | loyalty | Retrieves a loyalty account. |
| POST | v2/loyalty/accounts/{id}/accumulate | write | loyalty | Adds points earned from a purchase to a loyalty account. |
| POST | v2/loyalty/accounts/{id}/adjust | write | loyalty | Adds points to or subtracts points from a buyer's account. |
| POST | v2/loyalty/events/search | read | loyalty | Searches for loyalty events. |
| GET | v2/loyalty/programs | read | loyalty | Returns a list of loyalty programs in the seller's account. |
| GET | v2/loyalty/programs/{id} | read | loyalty | Retrieves the loyalty program in a seller's account, specified by the program ID or the keyword main. |
| POST | v2/loyalty/programs/{id}/calculate | read | loyalty | Calculates the number of points a buyer can earn from a purchase. |
| GET | v2/loyalty/programs/{id}/promotions | read | loyalty | Lists the loyalty promotions associated with a loyalty program. |
| POST | v2/loyalty/programs/{id}/promotions | write | loyalty | Creates a loyalty promotion for a loyalty program. |
| GET | v2/loyalty/programs/{id}/promotions/{id} | read | loyalty | Retrieves a loyalty promotion. |
| POST | v2/loyalty/programs/{id}/promotions/{id}/cancel | write | loyalty | Cancels a loyalty promotion. |
| POST | v2/loyalty/rewards | write | loyalty | Creates a loyalty reward. |
| POST | v2/loyalty/rewards/search | read | loyalty | Searches for loyalty rewards. |
| GET | v2/loyalty/rewards/{id} | read | loyalty | Retrieves a loyalty reward. |
| DELETE | v2/loyalty/rewards/{id} | write | loyalty | Deletes a loyalty reward by doing the following: - Returns the loyalty points back to the loyalty account. |
| POST | v2/loyalty/rewards/{id}/redeem | write | loyalty | Redeems a loyalty reward. |
| GET | v2/merchants/custom-attribute-definitions | read | merchantcustomattributes | Lists the merchant-related custom attribute definitions that belong to a Square seller account. |
| POST | v2/merchants/custom-attribute-definitions | write | merchantcustomattributes | Creates a merchant-related custom attribute definition for a Square seller account. |
| GET | v2/merchants/custom-attribute-definitions/{id} | read | merchantcustomattributes | Retrieves a merchant-related custom attribute definition from a Square seller account. |
| PUT | v2/merchants/custom-attribute-definitions/{id} | write | merchantcustomattributes | Updates a merchant-related custom attribute definition for a Square seller account. |
| DELETE | v2/merchants/custom-attribute-definitions/{id} | write | merchantcustomattributes | Deletes a merchant-related custom attribute definition from a Square seller account. |
| POST | v2/merchants/custom-attributes/bulk-delete | write | merchantcustomattributes | Deletes custom attributes for a merchant as a bulk operation. |
| POST | v2/merchants/custom-attributes/bulk-upsert | write | merchantcustomattributes | Creates or updates custom attributes for a merchant as a bulk operation. |
| GET | v2/merchants/{id}/custom-attributes | read | merchantcustomattributes | Lists the custom attributes associated with a merchant. |
| GET | v2/merchants/{id}/custom-attributes/{id} | read | merchantcustomattributes | Retrieves a custom attribute associated with a merchant. |
| POST | v2/merchants/{id}/custom-attributes/{id} | write | merchantcustomattributes | Creates or updates a custom attribute for a merchant. |
| DELETE | v2/merchants/{id}/custom-attributes/{id} | write | merchantcustomattributes | Deletes a custom attribute associated with a merchant. |
| GET | v2/merchants | read | merchants | Provides details about the merchant associated with a given access token. |
| GET | v2/merchants/{id} | read | merchants | Retrieves the Merchant object for the given merchant_id. |
| POST | oauth2/revoke | write | oauth | Revokes an access token generated with the OAuth flow. |
| POST | oauth2/token | write | oauth | Returns an OAuth access token and refresh token using the authorization_code or refresh_token grant type. |
| POST | oauth2/token/status | read | oauth | Returns information about an OAuth access token or an application’s [personal access... |
| GET | v2/orders/custom-attribute-definitions | read | ordercustomattributes | Lists the order-related custom attribute definitions that belong to a Square seller account. |
| POST | v2/orders/custom-attribute-definitions | write | ordercustomattributes | Creates an order-related custom attribute definition. |
| GET | v2/orders/custom-attribute-definitions/{id} | read | ordercustomattributes | Retrieves an order-related custom attribute definition from a Square seller account. |
| PUT | v2/orders/custom-attribute-definitions/{id} | write | ordercustomattributes | Updates an order-related custom attribute definition for a Square seller account. |
| DELETE | v2/orders/custom-attribute-definitions/{id} | write | ordercustomattributes | Deletes an order-related custom attribute definition from a Square seller account. |
| POST | v2/orders/custom-attributes/bulk-delete | write | ordercustomattributes | Deletes order custom attributes as a bulk operation. |
| POST | v2/orders/custom-attributes/bulk-upsert | write | ordercustomattributes | Creates or updates order custom attributes as a bulk operation. |
| GET | v2/orders/{id}/custom-attributes | read | ordercustomattributes | Lists the custom attributes associated with an order. |
| GET | v2/orders/{id}/custom-attributes/{id} | read | ordercustomattributes | Retrieves a custom attribute associated with an order. |
| POST | v2/orders/{id}/custom-attributes/{id} | write | ordercustomattributes | Creates or updates a custom attribute for an order. |
| DELETE | v2/orders/{id}/custom-attributes/{id} | write | ordercustomattributes | Deletes a custom attribute associated with a customer profile. |
| POST | v2/orders | write | orders | Creates a new order that can include information about products for purchase and settings to apply to the purchase. |
| POST | v2/orders/batch-retrieve | read | orders | Retrieves a set of orders by their IDs. |
| POST | v2/orders/calculate | write | orders | Enables applications to preview order pricing without creating an order. |
| POST | v2/orders/clone | write | orders | Creates a new order, in the DRAFT state, by duplicating an existing order. |
| POST | v2/orders/search | read | orders | Search all orders for one or more locations. |
| GET | v2/orders/{id} | read | orders | Retrieves an Order by ID. |
| PUT | v2/orders/{id} | write | orders | Updates an open order by adding, replacing, or deleting fields. |
| POST | v2/orders/{id}/pay | write | orders | Pay for an order using one or more approved payments or settle an order with a total of 0. |
| GET | v2/payments | read | payments | Retrieves a list of payments taken by the account making the request. |
| POST | v2/payments | write | payments | Creates a payment using the provided source. |
| POST | v2/payments/cancel | write | payments | Cancels (voids) a payment identified by the idempotency key that is specified in the request. |
| GET | v2/payments/{id} | read | payments | Retrieves details for a specific payment. |
| PUT | v2/payments/{id} | write | payments | Updates a payment with the APPROVED status. |
| POST | v2/payments/{id}/cancel | write | payments | Cancels (voids) a payment. |
| POST | v2/payments/{id}/complete | write | payments | Completes (captures) a payment. |
| GET | v2/payouts | read | payouts | Retrieves a list of all payouts for the default location. |
| GET | v2/payouts/{id} | read | payouts | Retrieves details of a specific payout identified by a payout ID. |
| GET | v2/payouts/{id}/payout-entries | read | payouts | Retrieves a list of all payout entries for a specific payout. |
| GET | v2/refunds | read | refunds | Retrieves a list of refunds for the account making the request. |
| POST | v2/refunds | write | refunds | Refunds a payment. |
| GET | v2/refunds/{id} | read | refunds | Retrieves a specific refund using the refund_id. |
| GET | v2/sites | read | sites | Lists the Square Online sites that belong to a seller. |
| GET | v2/sites/{id}/snippet | read | snippets | Retrieves your snippet from a Square Online site. |
| POST | v2/sites/{id}/snippet | write | snippets | Adds a snippet to a Square Online site or updates the existing snippet on the site. |
| DELETE | v2/sites/{id}/snippet | write | snippets | Removes your snippet from a Square Online site. |
| POST | v2/subscriptions | write | subscriptions | Enrolls a customer in a subscription. |
| POST | v2/subscriptions/bulk-swap-plan | write | subscriptions | Schedules a plan variation change for all active subscriptions under a given plan variation. |
| POST | v2/subscriptions/search | read | subscriptions | Searches for subscriptions. |
| GET | v2/subscriptions/{id} | read | subscriptions | Retrieves a specific subscription. |
| PUT | v2/subscriptions/{id} | write | subscriptions | Updates a subscription by modifying or clearing subscription field values. |
| DELETE | v2/subscriptions/{id}/actions/{id} | write | subscriptions | Deletes a scheduled action for a subscription. |
| POST | v2/subscriptions/{id}/billing-anchor | write | subscriptions | Changes the billing anchor date for a subscription. |
| POST | v2/subscriptions/{id}/cancel | write | subscriptions | Schedules a CANCEL action to cancel an active subscription. |
| GET | v2/subscriptions/{id}/events | read | subscriptions | Lists all events for a specific subscription. |
| POST | v2/subscriptions/{id}/pause | write | subscriptions | Schedules a PAUSE action to pause an active subscription. |
| POST | v2/subscriptions/{id}/resume | write | subscriptions | Schedules a RESUME action to resume a paused or a deactivated subscription. |
| POST | v2/subscriptions/{id}/swap-plan | write | subscriptions | Schedules a SWAP_PLAN action to swap a subscription plan variation in an existing subscription. |
| POST | v2/team-members | write | team | Creates a single TeamMember object. |
| POST | v2/team-members/bulk-create | write | team | Creates multiple TeamMember objects. |
| POST | v2/team-members/bulk-update | write | team | Updates multiple TeamMember objects. |
| GET | v2/team-members/jobs | read | team | Lists jobs in a seller account. |
| POST | v2/team-members/jobs | write | team | Creates a job in a seller account. |
| GET | v2/team-members/jobs/{id} | read | team | Retrieves a specified job. |
| PUT | v2/team-members/jobs/{id} | write | team | Updates the title or tip eligibility of a job. |
| POST | v2/team-members/search | read | team | Returns a paginated list of TeamMember objects for a business. |
| GET | v2/team-members/{id} | read | team | Retrieves a TeamMember object for the given TeamMember.id. |
| PUT | v2/team-members/{id} | write | team | Updates a single TeamMember object. |
| GET | v2/team-members/{id}/wage-setting | read | team | Retrieves a WageSetting object for a team member specified by TeamMember.id. |
| PUT | v2/team-members/{id}/wage-setting | write | team | Creates or updates a WageSetting object. |
| POST | v2/terminals/actions | write | terminal | Creates a Terminal action request and sends it to the specified device. |
| POST | v2/terminals/actions/search | read | terminal | Retrieves a filtered list of Terminal action requests created by the account making the request. |
| GET | v2/terminals/actions/{id} | read | terminal | Retrieves a Terminal action request by action_id. |
| POST | v2/terminals/actions/{id}/cancel | write | terminal | Cancels a Terminal action request if the status of the request permits it. |
| POST | v2/terminals/actions/{id}/dismiss | write | terminal | Dismisses a Terminal action request if the status and type of the request permits it. |
| POST | v2/terminals/checkouts | write | terminal | Creates a Terminal checkout request and sends it to the specified device to take a payment for the requested amount. |
| POST | v2/terminals/checkouts/search | read | terminal | Returns a filtered list of Terminal checkout requests created by the application making the request. |
| GET | v2/terminals/checkouts/{id} | read | terminal | Retrieves a Terminal checkout request by checkout_id. |
| POST | v2/terminals/checkouts/{id}/cancel | write | terminal | Cancels a Terminal checkout request if the status of the request permits it. |
| POST | v2/terminals/checkouts/{id}/dismiss | write | terminal | Dismisses a Terminal checkout request if the status and type of the request permits it. |
| POST | v2/terminals/refunds | write | terminal | Creates a request to refund an Interac payment completed on a Square Terminal. |
| POST | v2/terminals/refunds/search | read | terminal | Retrieves a filtered list of Interac Terminal refund requests created by the seller making the request. |
| GET | v2/terminals/refunds/{id} | read | terminal | Retrieves an Interac Terminal refund object by ID. |
| POST | v2/terminals/refunds/{id}/cancel | write | terminal | Cancels an Interac Terminal refund request by refund request ID if the status of the request permits it. |
| POST | v2/terminals/refunds/{id}/dismiss | write | terminal | Dismisses a Terminal refund request if the status and type of the request permits it. |
| GET | v2/locations/{id}/transactions | read | transactions | Lists transactions for a particular location. |
| GET | v2/locations/{id}/transactions/{id} | read | transactions | Retrieves details for a single transaction. |
| POST | v2/transfer-orders | write | transferorder | Creates a new transfer order in DRAFT status. |
| POST | v2/transfer-orders/search | read | transferorder | Searches for transfer orders using filters. |
| GET | v2/transfer-orders/{id} | read | transferorder | Retrieves a specific TransferOrder by ID. |
| PUT | v2/transfer-orders/{id} | write | transferorder | Updates an existing transfer order. |
| DELETE | v2/transfer-orders/{id} | write | transferorder | Deletes a transfer order in DRAFT status. |
| POST | v2/transfer-orders/{id}/cancel | write | transferorder | Cancels a transfer order in STARTED or PARTIALLY_RECEIVED status. |
| POST | v2/transfer-orders/{id}/receive | write | transferorder | Records receipt of CatalogItemVariations for a transfer order. |
| POST | v2/transfer-orders/{id}/start | write | transferorder | Changes a DRAFT transfer order to STARTED status. |
| GET | v1/{id}/orders | read | v1transactions | Provides summary information for a merchant's online store orders. |
| GET | v1/{id}/orders/{id} | read | v1transactions | Provides comprehensive information for a single online store order, including the order's history. |
| PUT | v1/{id}/orders/{id} | write | v1transactions | Updates the details of an online store order. |
| POST | v2/vendors/bulk-create | write | vendors | Creates one or more Vendor objects to represent suppliers to a seller. |
| POST | v2/vendors/bulk-retrieve | read | vendors | Retrieves one or more vendors of specified Vendor IDs. |
| PUT | v2/vendors/bulk-update | write | vendors | Updates one or more of existing Vendor objects as suppliers to a seller. |
| POST | v2/vendors/create | write | vendors | Creates a single Vendor object to represent a supplier to a seller. |
| POST | v2/vendors/search | read | vendors | Searches for vendors using a filter against supported Vendor properties and a supported sorter. |
| GET | v2/vendors/{id} | read | vendors | Retrieves the vendor of a specified Vendor ID. |
| PUT | v2/vendors/{id} | write | vendors | Updates an existing Vendor object as a supplier to a seller. |
| GET | v2/webhooks/event-types | read | webhooksubscriptions | Lists all webhook event types that can be subscribed to. |
| GET | v2/webhooks/subscriptions | read | webhooksubscriptions | Lists all webhook subscriptions owned by your application. |
| POST | v2/webhooks/subscriptions | write | webhooksubscriptions | Creates a webhook subscription. |
| GET | v2/webhooks/subscriptions/{id} | read | webhooksubscriptions | Retrieves a webhook subscription identified by its ID. |
| PUT | v2/webhooks/subscriptions/{id} | write | webhooksubscriptions | Updates a webhook subscription. |
| DELETE | v2/webhooks/subscriptions/{id} | write | webhooksubscriptions | Deletes a webhook subscription. |
| POST | v2/webhooks/subscriptions/{id}/signature-key | write | webhooksubscriptions | Updates a webhook subscription by replacing the existing signature key with a new one. |
| POST | v2/webhooks/subscriptions/{id}/test | write | webhooksubscriptions | Tests a webhook subscription by sending a test event to the notification URL. |
