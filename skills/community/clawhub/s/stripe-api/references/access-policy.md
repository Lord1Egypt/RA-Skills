# Stripe access policy

An access policy limits which endpoints Stripe connections may call through Maton. Stripe doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/stripe#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Stripe: its 267 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create stripe --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/account"},
    {"method": "GET", "path": "v1/accounts"},
    {"method": "GET", "path": "v1/accounts/{id}"},
    {"method": "GET", "path": "v1/accounts/{id}/bank_accounts/{id}"},
    {"method": "GET", "path": "v1/accounts/{id}/capabilities"},
    {"method": "GET", "path": "v1/accounts/{id}/capabilities/{id}"},
    {"method": "GET", "path": "v1/accounts/{id}/external_accounts"},
    {"method": "GET", "path": "v1/accounts/{id}/external_accounts/{id}"},
    {"method": "GET", "path": "v1/accounts/{id}/people"},
    {"method": "GET", "path": "v1/accounts/{id}/people/{id}"},
    {"method": "GET", "path": "v1/accounts/{id}/persons"},
    {"method": "GET", "path": "v1/accounts/{id}/persons/{id}"},
    {"method": "GET", "path": "v1/apple_pay/domains"},
    {"method": "GET", "path": "v1/apple_pay/domains/{id}"},
    {"method": "GET", "path": "v1/application_fees"},
    {"method": "GET", "path": "v1/application_fees/{id}"},
    {"method": "GET", "path": "v1/application_fees/{id}/refunds"},
    {"method": "GET", "path": "v1/application_fees/{id}/refunds/{id}"},
    {"method": "GET", "path": "v1/apps/installs"},
    {"method": "GET", "path": "v1/apps/installs/{id}"},
    {"method": "GET", "path": "v1/balance"},
    {"method": "GET", "path": "v1/balance/history"},
    {"method": "GET", "path": "v1/balance/history/{id}"},
    {"method": "GET", "path": "v1/balance_settings"},
    {"method": "GET", "path": "v1/balance_transactions"},
    {"method": "GET", "path": "v1/balance_transactions/{id}"},
    {"method": "GET", "path": "v1/billing/alerts"},
    {"method": "GET", "path": "v1/billing/alerts/{id}"},
    {"method": "GET", "path": "v1/billing/credit_balance_summary"},
    {"method": "GET", "path": "v1/billing/credit_balance_transactions"},
    {"method": "GET", "path": "v1/billing/credit_balance_transactions/{id}"},
    {"method": "GET", "path": "v1/billing/credit_grants"},
    {"method": "GET", "path": "v1/billing/credit_grants/{id}"},
    {"method": "GET", "path": "v1/billing/feedback_options"},
    {"method": "GET", "path": "v1/billing/feedback_options/{id}"},
    {"method": "GET", "path": "v1/billing/meters"},
    {"method": "GET", "path": "v1/billing/meters/{id}"},
    {"method": "GET", "path": "v1/billing/meters/{id}/event_summaries"},
    {"method": "GET", "path": "v1/billing_portal/configurations"},
    {"method": "GET", "path": "v1/billing_portal/configurations/{id}"},
    {"method": "GET", "path": "v1/charges"},
    {"method": "GET", "path": "v1/charges/search"},
    {"method": "GET", "path": "v1/charges/{id}"},
    {"method": "GET", "path": "v1/charges/{id}/dispute"},
    {"method": "GET", "path": "v1/charges/{id}/refunds"},
    {"method": "GET", "path": "v1/charges/{id}/refunds/{id}"},
    {"method": "GET", "path": "v1/checkout/sessions"},
    {"method": "GET", "path": "v1/checkout/sessions/{id}"},
    {"method": "GET", "path": "v1/checkout/sessions/{id}/line_items"},
    {"method": "GET", "path": "v1/climate/orders"},
    {"method": "GET", "path": "v1/climate/orders/{id}"},
    {"method": "GET", "path": "v1/climate/products"},
    {"method": "GET", "path": "v1/climate/products/{id}"},
    {"method": "GET", "path": "v1/climate/suppliers"},
    {"method": "GET", "path": "v1/climate/suppliers/{id}"},
    {"method": "GET", "path": "v1/confirmation_tokens/{id}"},
    {"method": "GET", "path": "v1/country_specs"},
    {"method": "GET", "path": "v1/country_specs/{id}"},
    {"method": "GET", "path": "v1/coupons"},
    {"method": "GET", "path": "v1/coupons/{id}"},
    {"method": "GET", "path": "v1/credit_notes"},
    {"method": "GET", "path": "v1/credit_notes/preview"},
    {"method": "GET", "path": "v1/credit_notes/preview/lines"},
    {"method": "GET", "path": "v1/credit_notes/{id}"},
    {"method": "GET", "path": "v1/credit_notes/{id}/lines"},
    {"method": "GET", "path": "v1/customers"},
    {"method": "GET", "path": "v1/customers/search"},
    {"method": "GET", "path": "v1/customers/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/balance_transactions"},
    {"method": "GET", "path": "v1/customers/{id}/balance_transactions/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/bank_accounts"},
    {"method": "GET", "path": "v1/customers/{id}/bank_accounts/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/cards"},
    {"method": "GET", "path": "v1/customers/{id}/cards/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/cash_balance"},
    {"method": "GET", "path": "v1/customers/{id}/cash_balance_transactions"},
    {"method": "GET", "path": "v1/customers/{id}/cash_balance_transactions/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/discount"},
    {"method": "GET", "path": "v1/customers/{id}/payment_methods"},
    {"method": "GET", "path": "v1/customers/{id}/payment_methods/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/sources"},
    {"method": "GET", "path": "v1/customers/{id}/sources/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/subscriptions"},
    {"method": "GET", "path": "v1/customers/{id}/subscriptions/{id}"},
    {"method": "GET", "path": "v1/customers/{id}/subscriptions/{id}/discount"},
    {"method": "GET", "path": "v1/customers/{id}/tax_ids"},
    {"method": "GET", "path": "v1/customers/{id}/tax_ids/{id}"},
    {"method": "GET", "path": "v1/disputes"},
    {"method": "GET", "path": "v1/disputes/{id}"},
    {"method": "GET", "path": "v1/entitlements/active_entitlements"},
    {"method": "GET", "path": "v1/entitlements/active_entitlements/{id}"},
    {"method": "GET", "path": "v1/entitlements/features"},
    {"method": "GET", "path": "v1/entitlements/features/{id}"},
    {"method": "GET", "path": "v1/events"},
    {"method": "GET", "path": "v1/events/{id}"},
    {"method": "GET", "path": "v1/exchange_rates"},
    {"method": "GET", "path": "v1/exchange_rates/{id}"},
    {"method": "GET", "path": "v1/file_links"},
    {"method": "GET", "path": "v1/file_links/{id}"},
    {"method": "GET", "path": "v1/files"},
    {"method": "GET", "path": "v1/files/{id}"},
    {"method": "GET", "path": "v1/financial_connections/accounts"},
    {"method": "GET", "path": "v1/financial_connections/accounts/{id}"},
    {"method": "GET", "path": "v1/financial_connections/accounts/{id}/owners"},
    {"method": "GET", "path": "v1/financial_connections/sessions/{id}"},
    {"method": "GET", "path": "v1/financial_connections/transactions"},
    {"method": "GET", "path": "v1/financial_connections/transactions/{id}"},
    {"method": "GET", "path": "v1/forwarding/requests"},
    {"method": "GET", "path": "v1/forwarding/requests/{id}"},
    {"method": "GET", "path": "v1/identity/verification_reports"},
    {"method": "GET", "path": "v1/identity/verification_reports/{id}"},
    {"method": "GET", "path": "v1/identity/verification_sessions"},
    {"method": "GET", "path": "v1/identity/verification_sessions/{id}"},
    {"method": "GET", "path": "v1/invoice_payments"},
    {"method": "GET", "path": "v1/invoice_payments/{id}"},
    {"method": "GET", "path": "v1/invoice_rendering_templates"},
    {"method": "GET", "path": "v1/invoice_rendering_templates/{id}"},
    {"method": "GET", "path": "v1/invoiceitems"},
    {"method": "GET", "path": "v1/invoiceitems/{id}"},
    {"method": "GET", "path": "v1/invoices"},
    {"method": "POST", "path": "v1/invoices/create_preview"},
    {"method": "GET", "path": "v1/invoices/search"},
    {"method": "GET", "path": "v1/invoices/{id}"},
    {"method": "GET", "path": "v1/invoices/{id}/lines"},
    {"method": "GET", "path": "v1/issuing/authorizations"},
    {"method": "GET", "path": "v1/issuing/authorizations/{id}"},
    {"method": "GET", "path": "v1/issuing/cardholders"},
    {"method": "GET", "path": "v1/issuing/cardholders/{id}"},
    {"method": "GET", "path": "v1/issuing/disputes"},
    {"method": "GET", "path": "v1/issuing/disputes/{id}"},
    {"method": "GET", "path": "v1/issuing/personalization_designs"},
    {"method": "GET", "path": "v1/issuing/personalization_designs/{id}"},
    {"method": "GET", "path": "v1/issuing/physical_bundles"},
    {"method": "GET", "path": "v1/issuing/physical_bundles/{id}"},
    {"method": "GET", "path": "v1/issuing/settlements/{id}"},
    {"method": "GET", "path": "v1/issuing/tokens"},
    {"method": "GET", "path": "v1/issuing/tokens/{id}"},
    {"method": "GET", "path": "v1/issuing/transactions"},
    {"method": "GET", "path": "v1/issuing/transactions/{id}"},
    {"method": "GET", "path": "v1/link_account_sessions/{id}"},
    {"method": "GET", "path": "v1/linked_accounts"},
    {"method": "GET", "path": "v1/linked_accounts/{id}"},
    {"method": "GET", "path": "v1/linked_accounts/{id}/owners"},
    {"method": "GET", "path": "v1/mandates/{id}"},
    {"method": "GET", "path": "v1/payment_attempt_records"},
    {"method": "GET", "path": "v1/payment_attempt_records/{id}"},
    {"method": "GET", "path": "v1/payment_intents"},
    {"method": "GET", "path": "v1/payment_intents/search"},
    {"method": "GET", "path": "v1/payment_intents/{id}"},
    {"method": "GET", "path": "v1/payment_intents/{id}/amount_details_line_items"},
    {"method": "GET", "path": "v1/payment_links"},
    {"method": "GET", "path": "v1/payment_links/{id}"},
    {"method": "GET", "path": "v1/payment_links/{id}/line_items"},
    {"method": "GET", "path": "v1/payment_method_configurations"},
    {"method": "GET", "path": "v1/payment_method_configurations/{id}"},
    {"method": "GET", "path": "v1/payment_method_domains"},
    {"method": "GET", "path": "v1/payment_method_domains/{id}"},
    {"method": "GET", "path": "v1/payment_methods"},
    {"method": "GET", "path": "v1/payment_methods/{id}"},
    {"method": "GET", "path": "v1/payment_records"},
    {"method": "GET", "path": "v1/payment_records/{id}"},
    {"method": "GET", "path": "v1/payouts"},
    {"method": "GET", "path": "v1/payouts/{id}"},
    {"method": "GET", "path": "v1/plans"},
    {"method": "GET", "path": "v1/plans/{id}"},
    {"method": "GET", "path": "v1/prices"},
    {"method": "GET", "path": "v1/prices/search"},
    {"method": "GET", "path": "v1/prices/{id}"},
    {"method": "GET", "path": "v1/product_catalog/trial_offers"},
    {"method": "GET", "path": "v1/product_catalog/trial_offers/{id}"},
    {"method": "GET", "path": "v1/products"},
    {"method": "GET", "path": "v1/products/search"},
    {"method": "GET", "path": "v1/products/{id}"},
    {"method": "GET", "path": "v1/products/{id}/features"},
    {"method": "GET", "path": "v1/products/{id}/features/{id}"},
    {"method": "GET", "path": "v1/promotion_codes"},
    {"method": "GET", "path": "v1/promotion_codes/{id}"},
    {"method": "GET", "path": "v1/quotes"},
    {"method": "GET", "path": "v1/quotes/{id}"},
    {"method": "GET", "path": "v1/quotes/{id}/computed_upfront_line_items"},
    {"method": "GET", "path": "v1/quotes/{id}/line_items"},
    {"method": "GET", "path": "v1/radar/early_fraud_warnings"},
    {"method": "GET", "path": "v1/radar/early_fraud_warnings/{id}"},
    {"method": "GET", "path": "v1/radar/value_list_items"},
    {"method": "GET", "path": "v1/radar/value_list_items/{id}"},
    {"method": "GET", "path": "v1/radar/value_lists"},
    {"method": "GET", "path": "v1/radar/value_lists/{id}"},
    {"method": "GET", "path": "v1/refunds"},
    {"method": "GET", "path": "v1/refunds/{id}"},
    {"method": "GET", "path": "v1/reporting/report_runs"},
    {"method": "GET", "path": "v1/reporting/report_runs/{id}"},
    {"method": "GET", "path": "v1/reporting/report_types"},
    {"method": "GET", "path": "v1/reporting/report_types/{id}"},
    {"method": "GET", "path": "v1/reviews"},
    {"method": "GET", "path": "v1/reviews/{id}"},
    {"method": "GET", "path": "v1/setup_attempts"},
    {"method": "GET", "path": "v1/setup_intents"},
    {"method": "GET", "path": "v1/setup_intents/{id}"},
    {"method": "GET", "path": "v1/shipping_rates"},
    {"method": "GET", "path": "v1/shipping_rates/{id}"},
    {"method": "GET", "path": "v1/sigma/scheduled_query_runs"},
    {"method": "GET", "path": "v1/sigma/scheduled_query_runs/{id}"},
    {"method": "GET", "path": "v1/sources/{id}"},
    {"method": "GET", "path": "v1/sources/{id}/mandate_notifications/{id}"},
    {"method": "GET", "path": "v1/sources/{id}/source_transactions"},
    {"method": "GET", "path": "v1/sources/{id}/source_transactions/{id}"},
    {"method": "GET", "path": "v1/subscription_items"},
    {"method": "GET", "path": "v1/subscription_items/{id}"},
    {"method": "GET", "path": "v1/subscription_schedules"},
    {"method": "GET", "path": "v1/subscription_schedules/{id}"},
    {"method": "GET", "path": "v1/subscriptions"},
    {"method": "GET", "path": "v1/subscriptions/search"},
    {"method": "GET", "path": "v1/subscriptions/{id}"},
    {"method": "GET", "path": "v1/tax/associations/find"},
    {"method": "GET", "path": "v1/tax/calculations/{id}"},
    {"method": "GET", "path": "v1/tax/calculations/{id}/line_items"},
    {"method": "GET", "path": "v1/tax/locations"},
    {"method": "GET", "path": "v1/tax/locations/{id}"},
    {"method": "GET", "path": "v1/tax/registrations"},
    {"method": "GET", "path": "v1/tax/registrations/{id}"},
    {"method": "GET", "path": "v1/tax/settings"},
    {"method": "GET", "path": "v1/tax/transactions/{id}"},
    {"method": "GET", "path": "v1/tax/transactions/{id}/line_items"},
    {"method": "GET", "path": "v1/tax_codes"},
    {"method": "GET", "path": "v1/tax_codes/{id}"},
    {"method": "GET", "path": "v1/tax_ids"},
    {"method": "GET", "path": "v1/tax_ids/{id}"},
    {"method": "GET", "path": "v1/tax_rates"},
    {"method": "GET", "path": "v1/tax_rates/{id}"},
    {"method": "GET", "path": "v1/terminal/locations"},
    {"method": "GET", "path": "v1/terminal/locations/{id}"},
    {"method": "GET", "path": "v1/terminal/readers"},
    {"method": "GET", "path": "v1/terminal/readers/{id}"},
    {"method": "GET", "path": "v1/test_helpers/test_clocks"},
    {"method": "GET", "path": "v1/test_helpers/test_clocks/{id}"},
    {"method": "GET", "path": "v1/three_d_secure/authentications"},
    {"method": "GET", "path": "v1/three_d_secure/authentications/{id}"},
    {"method": "GET", "path": "v1/tokens/{id}"},
    {"method": "GET", "path": "v1/topups"},
    {"method": "GET", "path": "v1/topups/{id}"},
    {"method": "GET", "path": "v1/transfers"},
    {"method": "GET", "path": "v1/transfers/{id}"},
    {"method": "GET", "path": "v1/transfers/{id}/reversals"},
    {"method": "GET", "path": "v1/transfers/{id}/reversals/{id}"},
    {"method": "GET", "path": "v1/treasury/credit_reversals"},
    {"method": "GET", "path": "v1/treasury/credit_reversals/{id}"},
    {"method": "GET", "path": "v1/treasury/debit_reversals"},
    {"method": "GET", "path": "v1/treasury/debit_reversals/{id}"},
    {"method": "GET", "path": "v1/treasury/financial_accounts"},
    {"method": "GET", "path": "v1/treasury/financial_accounts/{id}"},
    {"method": "GET", "path": "v1/treasury/financial_accounts/{id}/features"},
    {"method": "GET", "path": "v1/treasury/inbound_transfers"},
    {"method": "GET", "path": "v1/treasury/inbound_transfers/{id}"},
    {"method": "GET", "path": "v1/treasury/outbound_payments"},
    {"method": "GET", "path": "v1/treasury/outbound_payments/{id}"},
    {"method": "GET", "path": "v1/treasury/outbound_transfers"},
    {"method": "GET", "path": "v1/treasury/outbound_transfers/{id}"},
    {"method": "GET", "path": "v1/treasury/received_credits"},
    {"method": "GET", "path": "v1/treasury/received_credits/{id}"},
    {"method": "GET", "path": "v1/treasury/received_debits"},
    {"method": "GET", "path": "v1/treasury/received_debits/{id}"},
    {"method": "GET", "path": "v1/treasury/transaction_entries"},
    {"method": "GET", "path": "v1/treasury/transaction_entries/{id}"},
    {"method": "GET", "path": "v1/treasury/transactions"},
    {"method": "GET", "path": "v1/treasury/transactions/{id}"},
    {"method": "GET", "path": "v1/webhook_endpoints"},
    {"method": "GET", "path": "v1/webhook_endpoints/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Stripe endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/account | read | account | Retrieve account. |
| POST | v1/account_links | write | account_links | Create an account link. |
| POST | v1/account_sessions | write | account_sessions | Create an Account Session. |
| GET | v1/accounts | read | accounts | List all connected accounts. |
| POST | v1/accounts | write | accounts | Create an account. |
| GET | v1/accounts/{id} | read | accounts | Retrieve account. |
| POST | v1/accounts/{id} | write | accounts | Update an account. |
| DELETE | v1/accounts/{id} | write | accounts | Delete an account. |
| POST | v1/accounts/{id}/bank_accounts | write | accounts | Create an external account. |
| GET | v1/accounts/{id}/bank_accounts/{id} | read | accounts | Retrieve an external account. |
| POST | v1/accounts/{id}/bank_accounts/{id} | write | accounts | Update a bank account. |
| DELETE | v1/accounts/{id}/bank_accounts/{id} | write | accounts | Delete an external account. |
| GET | v1/accounts/{id}/capabilities | read | accounts | List all account capabilities. |
| GET | v1/accounts/{id}/capabilities/{id} | read | accounts | Retrieve an Account Capability. |
| POST | v1/accounts/{id}/capabilities/{id} | write | accounts | Update an Account Capability. |
| GET | v1/accounts/{id}/external_accounts | read | accounts | List all external accounts. |
| POST | v1/accounts/{id}/external_accounts | write | accounts | Create an external account. |
| GET | v1/accounts/{id}/external_accounts/{id} | read | accounts | Retrieve an external account. |
| POST | v1/accounts/{id}/external_accounts/{id} | write | accounts | Update a bank account. |
| DELETE | v1/accounts/{id}/external_accounts/{id} | write | accounts | Delete an external account. |
| POST | v1/accounts/{id}/login_links | write | accounts | Create a login link. |
| GET | v1/accounts/{id}/people | read | accounts | List all persons. |
| POST | v1/accounts/{id}/people | write | accounts | Create a person. |
| GET | v1/accounts/{id}/people/{id} | read | accounts | Retrieve a person. |
| POST | v1/accounts/{id}/people/{id} | write | accounts | Update a person. |
| DELETE | v1/accounts/{id}/people/{id} | write | accounts | Delete a person. |
| GET | v1/accounts/{id}/persons | read | accounts | List all persons. |
| POST | v1/accounts/{id}/persons | write | accounts | Create a person. |
| GET | v1/accounts/{id}/persons/{id} | read | accounts | Retrieve a person. |
| POST | v1/accounts/{id}/persons/{id} | write | accounts | Update a person. |
| DELETE | v1/accounts/{id}/persons/{id} | write | accounts | Delete a person. |
| POST | v1/accounts/{id}/reject | write | accounts | Reject an account. |
| POST | v1/accounts/{id}/unreject | write | accounts | Unreject an account. |
| GET | v1/apple_pay/domains | read | apple_pay | List apple pay domains. |
| POST | v1/apple_pay/domains | write | apple_pay | Create an apple pay domain. |
| GET | v1/apple_pay/domains/{id} | read | apple_pay | Retrieve an apple pay domain. |
| DELETE | v1/apple_pay/domains/{id} | write | apple_pay | Delete an apple pay domain. |
| GET | v1/application_fees | read | application_fees | List all application fees. |
| GET | v1/application_fees/{id} | read | application_fees | Retrieve an application fee. |
| POST | v1/application_fees/{id}/refund | write | application_fees | PostApplicationFeesIdRefund. |
| GET | v1/application_fees/{id}/refunds | read | application_fees | List all application fee refunds. |
| POST | v1/application_fees/{id}/refunds | write | application_fees | Create an application fee refund. |
| GET | v1/application_fees/{id}/refunds/{id} | read | application_fees | Retrieve an application fee refund. |
| POST | v1/application_fees/{id}/refunds/{id} | write | application_fees | Update an application fee refund. |
| GET | v1/apps/installs | read | apps | List all app installs. |
| POST | v1/apps/installs | write | apps | Create an app install. |
| GET | v1/apps/installs/{id} | read | apps | Retrieve an app install. |
| POST | v1/apps/installs/{id} | write | apps | Update an app install. |
| POST | v1/apps/installs/{id}/uninstall | write | apps | Uninstall an app install. |
| GET | v1/apps/secrets | write | apps | List secrets. Kept out of read: secret payloads. |
| POST | v1/apps/secrets | write | apps | Set a Secret. |
| POST | v1/apps/secrets/delete | write | apps | Delete a Secret. |
| GET | v1/apps/secrets/find | write | apps | Find a Secret. Kept out of read: returns the plaintext secret payload. |
| GET | v1/balance | read | balance | Retrieve balance. |
| GET | v1/balance/history | read | balance | List all balance transactions. |
| GET | v1/balance/history/{id} | read | balance | Retrieve a balance transaction. |
| GET | v1/balance_settings | read | balance_settings | Retrieve balance settings. |
| POST | v1/balance_settings | write | balance_settings | Update balance settings. |
| GET | v1/balance_transactions | read | balance_transactions | List all balance transactions. |
| GET | v1/balance_transactions/{id} | read | balance_transactions | Retrieve a balance transaction. |
| GET | v1/billing/alerts | read | billing | List billing alerts. |
| POST | v1/billing/alerts | write | billing | Create a billing alert. |
| GET | v1/billing/alerts/{id} | read | billing | Retrieve a billing alert. |
| POST | v1/billing/alerts/{id}/activate | write | billing | Activate a billing alert. |
| POST | v1/billing/alerts/{id}/archive | write | billing | Archive a billing alert. |
| POST | v1/billing/alerts/{id}/deactivate | write | billing | Deactivate a billing alert. |
| GET | v1/billing/credit_balance_summary | read | billing | Retrieve the credit balance summary for a customer. |
| GET | v1/billing/credit_balance_transactions | read | billing | List credit balance transactions. |
| GET | v1/billing/credit_balance_transactions/{id} | read | billing | Retrieve a credit balance transaction. |
| GET | v1/billing/credit_grants | read | billing | List credit grants. |
| POST | v1/billing/credit_grants | write | billing | Create a credit grant. |
| GET | v1/billing/credit_grants/{id} | read | billing | Retrieve a credit grant. |
| POST | v1/billing/credit_grants/{id} | write | billing | Update a credit grant. |
| POST | v1/billing/credit_grants/{id}/expire | write | billing | Expire a credit grant. |
| POST | v1/billing/credit_grants/{id}/void | write | billing | Void a credit grant. |
| GET | v1/billing/feedback_options | read | billing | List all feedback options. |
| POST | v1/billing/feedback_options | write | billing | Create a feedback option. |
| GET | v1/billing/feedback_options/{id} | read | billing | Retrieve a feedback option. |
| POST | v1/billing/feedback_options/{id} | write | billing | Update a feedback option. |
| POST | v1/billing/feedback_options/{id}/deactivate | write | billing | Deactivate a feedback option. |
| POST | v1/billing/meter_event_adjustments | write | billing | Create a billing meter event adjustment. |
| POST | v1/billing/meter_events | write | billing | Create a billing meter event. |
| GET | v1/billing/meters | read | billing | List billing meters. |
| POST | v1/billing/meters | write | billing | Create a billing meter. |
| GET | v1/billing/meters/{id} | read | billing | Retrieve a billing meter. |
| POST | v1/billing/meters/{id} | write | billing | Update a billing meter. |
| POST | v1/billing/meters/{id}/deactivate | write | billing | Deactivate a billing meter. |
| GET | v1/billing/meters/{id}/event_summaries | read | billing | List billing meter event summaries. |
| POST | v1/billing/meters/{id}/reactivate | write | billing | Reactivate a billing meter. |
| GET | v1/billing_portal/configurations | read | billing_portal | List portal configurations. |
| POST | v1/billing_portal/configurations | write | billing_portal | Create a portal configuration. |
| GET | v1/billing_portal/configurations/{id} | read | billing_portal | Retrieve a portal configuration. |
| POST | v1/billing_portal/configurations/{id} | write | billing_portal | Update a portal configuration. |
| POST | v1/billing_portal/sessions | write | billing_portal | Create a portal session. |
| GET | v1/charges | read | charges | List all charges. |
| POST | v1/charges | write | charges | Create a charge. |
| GET | v1/charges/search | read | charges | Search charges. |
| GET | v1/charges/{id} | read | charges | Retrieve a charge. |
| POST | v1/charges/{id} | write | charges | Update a charge. |
| POST | v1/charges/{id}/capture | write | charges | Capture a charge. |
| GET | v1/charges/{id}/dispute | read | charges | Retrieve a dispute for a specified charge. |
| POST | v1/charges/{id}/dispute | write | charges | PostChargesChargeDispute. |
| POST | v1/charges/{id}/dispute/close | write | charges | PostChargesChargeDisputeClose. |
| POST | v1/charges/{id}/refund | write | charges | Create a refund. |
| GET | v1/charges/{id}/refunds | read | charges | List all refunds. |
| POST | v1/charges/{id}/refunds | write | charges | Create a refund. |
| GET | v1/charges/{id}/refunds/{id} | read | charges | Retrieves the details of an existing refund. |
| POST | v1/charges/{id}/refunds/{id} | write | charges | Update a specified refund. |
| GET | v1/checkout/sessions | read | checkout | List all Checkout Sessions. |
| POST | v1/checkout/sessions | write | checkout | Create a Checkout Session. |
| GET | v1/checkout/sessions/{id} | read | checkout | Retrieve a Checkout Session. |
| POST | v1/checkout/sessions/{id} | write | checkout | Update a Checkout Session. |
| POST | v1/checkout/sessions/{id}/expire | write | checkout | Expire a Checkout Session. |
| GET | v1/checkout/sessions/{id}/line_items | read | checkout | Retrieve a Checkout Session's line items. |
| GET | v1/climate/orders | read | climate | List orders. |
| POST | v1/climate/orders | write | climate | Create an order. |
| GET | v1/climate/orders/{id} | read | climate | Retrieve an order. |
| POST | v1/climate/orders/{id} | write | climate | Update an order. |
| POST | v1/climate/orders/{id}/cancel | write | climate | Cancel an order. |
| GET | v1/climate/products | read | climate | List products. |
| GET | v1/climate/products/{id} | read | climate | Retrieve a product. |
| GET | v1/climate/suppliers | read | climate | List suppliers. |
| GET | v1/climate/suppliers/{id} | read | climate | Retrieve a supplier. |
| GET | v1/confirmation_tokens/{id} | read | confirmation_tokens | Retrieve a ConfirmationToken. |
| GET | v1/country_specs | read | country_specs | List Country Specs. |
| GET | v1/country_specs/{id} | read | country_specs | Retrieve a Country Spec. |
| GET | v1/coupons | read | coupons | List all coupons. |
| POST | v1/coupons | write | coupons | Create a coupon. |
| GET | v1/coupons/{id} | read | coupons | Retrieve a coupon. |
| POST | v1/coupons/{id} | write | coupons | Update a coupon. |
| DELETE | v1/coupons/{id} | write | coupons | Delete a coupon. |
| GET | v1/credit_notes | read | credit_notes | List all credit notes. |
| POST | v1/credit_notes | write | credit_notes | Create a credit note. |
| GET | v1/credit_notes/preview | read | credit_notes | Preview a credit note. |
| GET | v1/credit_notes/preview/lines | read | credit_notes | Retrieve a credit note preview's line items. |
| GET | v1/credit_notes/{id} | read | credit_notes | Retrieve a credit note. |
| POST | v1/credit_notes/{id} | write | credit_notes | Update a credit note. |
| GET | v1/credit_notes/{id}/lines | read | credit_notes | Retrieve a credit note's line items. |
| POST | v1/credit_notes/{id}/void | write | credit_notes | Void a credit note. |
| POST | v1/customer_sessions | write | customer_sessions | Create a Customer Session. |
| GET | v1/customers | read | customers | List all customers. |
| POST | v1/customers | write | customers | Create a customer. |
| GET | v1/customers/search | read | customers | Search customers. |
| GET | v1/customers/{id} | read | customers | Retrieve a customer. |
| POST | v1/customers/{id} | write | customers | Update a customer. |
| DELETE | v1/customers/{id} | write | customers | Delete a customer. |
| GET | v1/customers/{id}/balance_transactions | read | customers | List customer balance transactions. |
| POST | v1/customers/{id}/balance_transactions | write | customers | Create a customer balance transaction. |
| GET | v1/customers/{id}/balance_transactions/{id} | read | customers | Retrieve a customer balance transaction. |
| POST | v1/customers/{id}/balance_transactions/{id} | write | customers | Update a customer credit balance transaction. |
| GET | v1/customers/{id}/bank_accounts | read | customers | List all bank accounts. |
| POST | v1/customers/{id}/bank_accounts | write | customers | Create a card. |
| GET | v1/customers/{id}/bank_accounts/{id} | read | customers | Retrieve a bank account. |
| POST | v1/customers/{id}/bank_accounts/{id} | write | customers | Update a card. |
| DELETE | v1/customers/{id}/bank_accounts/{id} | write | customers | Delete a customer source. |
| POST | v1/customers/{id}/bank_accounts/{id}/verify | write | customers | Verify a bank account. |
| GET | v1/customers/{id}/cards | read | customers | List all cards. |
| POST | v1/customers/{id}/cards | write | customers | Create a card. |
| GET | v1/customers/{id}/cards/{id} | read | customers | Retrieve a card. |
| POST | v1/customers/{id}/cards/{id} | write | customers | Update a card. |
| DELETE | v1/customers/{id}/cards/{id} | write | customers | Delete a customer source. |
| GET | v1/customers/{id}/cash_balance | read | customers | Retrieve a cash balance. |
| POST | v1/customers/{id}/cash_balance | write | customers | Update a cash balance's settings. |
| GET | v1/customers/{id}/cash_balance_transactions | read | customers | List cash balance transactions. |
| GET | v1/customers/{id}/cash_balance_transactions/{id} | read | customers | Retrieve a cash balance transaction. |
| GET | v1/customers/{id}/discount | read | customers | GetCustomersCustomerDiscount. |
| DELETE | v1/customers/{id}/discount | write | customers | Delete a customer discount. |
| POST | v1/customers/{id}/funding_instructions | write | customers | Create or retrieve funding instructions for a customer cash balance. |
| GET | v1/customers/{id}/payment_methods | read | customers | List a Customer's PaymentMethods. |
| GET | v1/customers/{id}/payment_methods/{id} | read | customers | Retrieve a Customer's PaymentMethod. |
| GET | v1/customers/{id}/sources | read | customers | List sources for a specified customer. |
| POST | v1/customers/{id}/sources | write | customers | Create a card. |
| GET | v1/customers/{id}/sources/{id} | read | customers | Retrieve a specified source for a given customer. |
| POST | v1/customers/{id}/sources/{id} | write | customers | Update a card. |
| DELETE | v1/customers/{id}/sources/{id} | write | customers | Delete a customer source. |
| POST | v1/customers/{id}/sources/{id}/verify | write | customers | Verify a bank account. |
| GET | v1/customers/{id}/subscriptions | read | customers | List active subscriptions. |
| POST | v1/customers/{id}/subscriptions | write | customers | Create a subscription. |
| GET | v1/customers/{id}/subscriptions/{id} | read | customers | Retrieve a subscription. |
| POST | v1/customers/{id}/subscriptions/{id} | write | customers | Update a subscription on a customer. |
| DELETE | v1/customers/{id}/subscriptions/{id} | write | customers | Cancel a subscription. |
| GET | v1/customers/{id}/subscriptions/{id}/discount | read | customers | GetCustomersCustomerSubscriptionsSubscriptionExposedIdDiscount. |
| DELETE | v1/customers/{id}/subscriptions/{id}/discount | write | customers | Delete a customer discount. |
| GET | v1/customers/{id}/tax_ids | read | customers | List all Customer tax IDs. |
| POST | v1/customers/{id}/tax_ids | write | customers | Create a Customer tax ID. |
| GET | v1/customers/{id}/tax_ids/{id} | read | customers | Retrieve a Customer tax ID. |
| DELETE | v1/customers/{id}/tax_ids/{id} | write | customers | Delete a Customer tax ID. |
| GET | v1/disputes | read | disputes | List all disputes. |
| GET | v1/disputes/{id} | read | disputes | Retrieve a dispute. |
| POST | v1/disputes/{id} | write | disputes | Update a dispute. |
| POST | v1/disputes/{id}/close | write | disputes | Close a dispute. |
| GET | v1/entitlements/active_entitlements | read | entitlements | List all active entitlements. |
| GET | v1/entitlements/active_entitlements/{id} | read | entitlements | Retrieve an active entitlement. |
| GET | v1/entitlements/features | read | entitlements | List all features. |
| POST | v1/entitlements/features | write | entitlements | Create a feature. |
| GET | v1/entitlements/features/{id} | read | entitlements | Retrieve a feature. |
| POST | v1/entitlements/features/{id} | write | entitlements | Updates a feature. |
| POST | v1/ephemeral_keys | write | ephemeral_keys | Create an ephemeral key. |
| DELETE | v1/ephemeral_keys/{id} | write | ephemeral_keys | Immediately invalidate an ephemeral key. |
| GET | v1/events | read | events | List all events. |
| GET | v1/events/{id} | read | events | Retrieve an event. |
| GET | v1/exchange_rates | read | exchange_rates | List all exchange rates. |
| GET | v1/exchange_rates/{id} | read | exchange_rates | Retrieve an exchange rate. |
| POST | v1/external_accounts/{id} | write | external_accounts | Update a bank account. |
| GET | v1/file_links | read | file_links | List all file links. |
| POST | v1/file_links | write | file_links | Create a file link. |
| GET | v1/file_links/{id} | read | file_links | Retrieve a file link. |
| POST | v1/file_links/{id} | write | file_links | Update a file link. |
| GET | v1/files | read | files | List all files. |
| GET | v1/files/{id} | read | files | Retrieve a file. |
| GET | v1/financial_connections/accounts | read | financial_connections | List Accounts. |
| GET | v1/financial_connections/accounts/{id} | read | financial_connections | Retrieve an Account. |
| POST | v1/financial_connections/accounts/{id}/disconnect | write | financial_connections | Disconnect an Account. |
| GET | v1/financial_connections/accounts/{id}/owners | read | financial_connections | List Account Owners. |
| POST | v1/financial_connections/accounts/{id}/refresh | write | financial_connections | Refresh Account data. |
| POST | v1/financial_connections/accounts/{id}/subscribe | write | financial_connections | Subscribe to data refreshes for an Account. |
| POST | v1/financial_connections/accounts/{id}/unsubscribe | write | financial_connections | Unsubscribe from data refreshes for an Account. |
| POST | v1/financial_connections/sessions | write | financial_connections | Create a Session. |
| GET | v1/financial_connections/sessions/{id} | read | financial_connections | Retrieve a Session. |
| GET | v1/financial_connections/transactions | read | financial_connections | List Transactions. |
| GET | v1/financial_connections/transactions/{id} | read | financial_connections | Retrieve a Transaction. |
| GET | v1/forwarding/requests | read | forwarding | List all ForwardingRequests. |
| POST | v1/forwarding/requests | write | forwarding | Create a ForwardingRequest. |
| GET | v1/forwarding/requests/{id} | read | forwarding | Retrieve a ForwardingRequest. |
| GET | v1/identity/verification_reports | read | identity | List VerificationReports. |
| GET | v1/identity/verification_reports/{id} | read | identity | Retrieve a VerificationReport. |
| GET | v1/identity/verification_sessions | read | identity | List VerificationSessions. |
| POST | v1/identity/verification_sessions | write | identity | Create a VerificationSession. |
| GET | v1/identity/verification_sessions/{id} | read | identity | Retrieve a VerificationSession. |
| POST | v1/identity/verification_sessions/{id} | write | identity | Update a VerificationSession. |
| POST | v1/identity/verification_sessions/{id}/cancel | write | identity | Cancel a VerificationSession. |
| POST | v1/identity/verification_sessions/{id}/redact | write | identity | Redact a VerificationSession. |
| GET | v1/invoice_payments | read | invoice_payments | List all payments for an invoice. |
| GET | v1/invoice_payments/{id} | read | invoice_payments | Retrieve an InvoicePayment. |
| GET | v1/invoice_rendering_templates | read | invoice_rendering_templates | List all invoice rendering templates. |
| GET | v1/invoice_rendering_templates/{id} | read | invoice_rendering_templates | Retrieve an invoice rendering template. |
| POST | v1/invoice_rendering_templates/{id}/archive | write | invoice_rendering_templates | Archive an invoice rendering template. |
| POST | v1/invoice_rendering_templates/{id}/unarchive | write | invoice_rendering_templates | Unarchive an invoice rendering template. |
| GET | v1/invoiceitems | read | invoiceitems | List all invoice items. |
| POST | v1/invoiceitems | write | invoiceitems | Create an invoice item. |
| GET | v1/invoiceitems/{id} | read | invoiceitems | Retrieve an invoice item. |
| POST | v1/invoiceitems/{id} | write | invoiceitems | Update an invoice item. |
| DELETE | v1/invoiceitems/{id} | write | invoiceitems | Delete an invoice item. |
| GET | v1/invoices | read | invoices | List all invoices. |
| POST | v1/invoices | write | invoices | Create an invoice. |
| POST | v1/invoices/create_preview | read | invoices | Preview an upcoming invoice without creating it. |
| GET | v1/invoices/search | read | invoices | Search invoices. |
| GET | v1/invoices/{id} | read | invoices | Retrieve an invoice. |
| POST | v1/invoices/{id} | write | invoices | Update an invoice. |
| DELETE | v1/invoices/{id} | write | invoices | Delete a draft invoice. |
| POST | v1/invoices/{id}/add_lines | write | invoices | Bulk add invoice line items. |
| POST | v1/invoices/{id}/attach_payment | write | invoices | Attach a payment to an Invoice. |
| POST | v1/invoices/{id}/finalize | write | invoices | Finalize an invoice. |
| GET | v1/invoices/{id}/lines | read | invoices | Retrieve an invoice's line items. |
| POST | v1/invoices/{id}/lines/{id} | write | invoices | Update an invoice's line item. |
| POST | v1/invoices/{id}/mark_uncollectible | write | invoices | Mark an invoice as uncollectible. |
| POST | v1/invoices/{id}/pay | write | invoices | Pay an invoice. |
| POST | v1/invoices/{id}/remove_lines | write | invoices | Bulk remove invoice line items. |
| POST | v1/invoices/{id}/send | write | invoices | Send an invoice for manual payment. |
| POST | v1/invoices/{id}/update_lines | write | invoices | Bulk update invoice line items. |
| POST | v1/invoices/{id}/void | write | invoices | Void an invoice. |
| GET | v1/issuing/authorizations | read | issuing | List all authorizations. |
| GET | v1/issuing/authorizations/{id} | read | issuing | Retrieve an authorization. |
| POST | v1/issuing/authorizations/{id} | write | issuing | Update an authorization. |
| POST | v1/issuing/authorizations/{id}/approve | write | issuing | Approve an authorization. |
| POST | v1/issuing/authorizations/{id}/decline | write | issuing | Decline an authorization. |
| GET | v1/issuing/cardholders | read | issuing | List all cardholders. |
| POST | v1/issuing/cardholders | write | issuing | Create a cardholder. |
| GET | v1/issuing/cardholders/{id} | read | issuing | Retrieve a cardholder. |
| POST | v1/issuing/cardholders/{id} | write | issuing | Update a cardholder. |
| GET | v1/issuing/cards | write | issuing | List all cards. Kept out of read: expand can return full card number and CVC. |
| POST | v1/issuing/cards | write | issuing | Create a card. |
| GET | v1/issuing/cards/{id} | write | issuing | Retrieve a card. Kept out of read: expand can return full card number and CVC. |
| POST | v1/issuing/cards/{id} | write | issuing | Update a card. |
| GET | v1/issuing/disputes | read | issuing | List all disputes. |
| POST | v1/issuing/disputes | write | issuing | Create a dispute. |
| GET | v1/issuing/disputes/{id} | read | issuing | Retrieve a dispute. |
| POST | v1/issuing/disputes/{id} | write | issuing | Update a dispute. |
| POST | v1/issuing/disputes/{id}/submit | write | issuing | Submit a dispute. |
| GET | v1/issuing/personalization_designs | read | issuing | List all personalization designs. |
| POST | v1/issuing/personalization_designs | write | issuing | Create a personalization design. |
| GET | v1/issuing/personalization_designs/{id} | read | issuing | Retrieve a personalization design. |
| POST | v1/issuing/personalization_designs/{id} | write | issuing | Update a personalization design. |
| GET | v1/issuing/physical_bundles | read | issuing | List all physical bundles. |
| GET | v1/issuing/physical_bundles/{id} | read | issuing | Retrieve a physical bundle. |
| GET | v1/issuing/settlements/{id} | read | issuing | Retrieve a settlement. |
| POST | v1/issuing/settlements/{id} | write | issuing | Update a settlement. |
| GET | v1/issuing/tokens | read | issuing | List all issuing tokens for card. |
| GET | v1/issuing/tokens/{id} | read | issuing | Retrieve an issuing token. |
| POST | v1/issuing/tokens/{id} | write | issuing | Update a token status. |
| GET | v1/issuing/transactions | read | issuing | List all transactions. |
| GET | v1/issuing/transactions/{id} | read | issuing | Retrieve a transaction. |
| POST | v1/issuing/transactions/{id} | write | issuing | Update a transaction. |
| POST | v1/link_account_sessions | write | link_account_sessions | Create a Session. |
| GET | v1/link_account_sessions/{id} | read | link_account_sessions | Retrieve a Session. |
| GET | v1/linked_accounts | read | linked_accounts | List Accounts. |
| GET | v1/linked_accounts/{id} | read | linked_accounts | Retrieve an Account. |
| POST | v1/linked_accounts/{id}/disconnect | write | linked_accounts | Disconnect an Account. |
| GET | v1/linked_accounts/{id}/owners | read | linked_accounts | List Account Owners. |
| POST | v1/linked_accounts/{id}/refresh | write | linked_accounts | Refresh Account data. |
| GET | v1/mandates/{id} | read | mandates | Retrieve a Mandate. |
| GET | v1/payment_attempt_records | read | payment_attempt_records | List Payment Attempt Records. |
| GET | v1/payment_attempt_records/{id} | read | payment_attempt_records | Retrieve a Payment Attempt Record. |
| GET | v1/payment_intents | read | payment_intents | List all PaymentIntents. |
| POST | v1/payment_intents | write | payment_intents | Create a PaymentIntent. |
| GET | v1/payment_intents/search | read | payment_intents | Search PaymentIntents. |
| GET | v1/payment_intents/{id} | read | payment_intents | Retrieve a PaymentIntent. |
| POST | v1/payment_intents/{id} | write | payment_intents | Update a PaymentIntent. |
| GET | v1/payment_intents/{id}/amount_details_line_items | read | payment_intents | List all PaymentIntent LineItems. |
| POST | v1/payment_intents/{id}/apply_customer_balance | write | payment_intents | Reconcile a customer_balance PaymentIntent. |
| POST | v1/payment_intents/{id}/cancel | write | payment_intents | Cancel a PaymentIntent. |
| POST | v1/payment_intents/{id}/capture | write | payment_intents | Capture a PaymentIntent. |
| POST | v1/payment_intents/{id}/confirm | write | payment_intents | Confirm a PaymentIntent. |
| POST | v1/payment_intents/{id}/increment_authorization | write | payment_intents | Increment an authorization. |
| POST | v1/payment_intents/{id}/verify_microdeposits | write | payment_intents | Verify microdeposits on a PaymentIntent. |
| GET | v1/payment_links | read | payment_links | List all payment links. |
| POST | v1/payment_links | write | payment_links | Create a payment link. |
| GET | v1/payment_links/{id} | read | payment_links | Retrieve payment link. |
| POST | v1/payment_links/{id} | write | payment_links | Update a payment link. |
| GET | v1/payment_links/{id}/line_items | read | payment_links | Retrieve a payment link's line items. |
| GET | v1/payment_method_configurations | read | payment_method_configurations | List payment method configurations. |
| POST | v1/payment_method_configurations | write | payment_method_configurations | Create a payment method configuration. |
| GET | v1/payment_method_configurations/{id} | read | payment_method_configurations | Retrieve payment method configuration. |
| POST | v1/payment_method_configurations/{id} | write | payment_method_configurations | Update payment method configuration. |
| GET | v1/payment_method_domains | read | payment_method_domains | List payment method domains. |
| POST | v1/payment_method_domains | write | payment_method_domains | Create a payment method domain. |
| GET | v1/payment_method_domains/{id} | read | payment_method_domains | Retrieve a payment method domain. |
| POST | v1/payment_method_domains/{id} | write | payment_method_domains | Update a payment method domain. |
| POST | v1/payment_method_domains/{id}/validate | write | payment_method_domains | Validate an existing payment method domain. |
| GET | v1/payment_methods | read | payment_methods | List PaymentMethods. |
| POST | v1/payment_methods | write | payment_methods | Create a PaymentMethod. |
| GET | v1/payment_methods/{id} | read | payment_methods | Retrieve a PaymentMethod. |
| POST | v1/payment_methods/{id} | write | payment_methods | Update a PaymentMethod. |
| POST | v1/payment_methods/{id}/attach | write | payment_methods | Attach a PaymentMethod to a Customer. |
| POST | v1/payment_methods/{id}/detach | write | payment_methods | Detach a PaymentMethod from a Customer. |
| GET | v1/payment_records | read | payment_records | List Payment Records. |
| POST | v1/payment_records/report_payment | write | payment_records | Report a payment. |
| GET | v1/payment_records/{id} | read | payment_records | Retrieve a Payment Record. |
| POST | v1/payment_records/{id}/report_payment_attempt | write | payment_records | Report a payment attempt. |
| POST | v1/payment_records/{id}/report_payment_attempt_canceled | write | payment_records | Report payment attempt canceled. |
| POST | v1/payment_records/{id}/report_payment_attempt_failed | write | payment_records | Report payment attempt failed. |
| POST | v1/payment_records/{id}/report_payment_attempt_guaranteed | write | payment_records | Report payment attempt guaranteed. |
| POST | v1/payment_records/{id}/report_payment_attempt_informational | write | payment_records | Report payment attempt informational. |
| POST | v1/payment_records/{id}/report_refund | write | payment_records | Report a refund. |
| GET | v1/payouts | read | payouts | List all payouts. |
| POST | v1/payouts | write | payouts | Create a payout. |
| GET | v1/payouts/{id} | read | payouts | Retrieve a payout. |
| POST | v1/payouts/{id} | write | payouts | Update a payout. |
| POST | v1/payouts/{id}/cancel | write | payouts | Cancel a payout. |
| POST | v1/payouts/{id}/reverse | write | payouts | Reverse a payout. |
| GET | v1/plans | read | plans | List all plans. |
| POST | v1/plans | write | plans | Create a plan. |
| GET | v1/plans/{id} | read | plans | Retrieve a plan. |
| POST | v1/plans/{id} | write | plans | Update a plan. |
| DELETE | v1/plans/{id} | write | plans | Delete a plan. |
| GET | v1/prices | read | prices | List all prices. |
| POST | v1/prices | write | prices | Create a price. |
| GET | v1/prices/search | read | prices | Search prices. |
| GET | v1/prices/{id} | read | prices | Retrieve a price. |
| POST | v1/prices/{id} | write | prices | Update a price. |
| GET | v1/product_catalog/trial_offers | read | product_catalog | List trial offers. |
| POST | v1/product_catalog/trial_offers | write | product_catalog | Create a trial offer. |
| GET | v1/product_catalog/trial_offers/{id} | read | product_catalog | Retrieve a trial offer. |
| POST | v1/product_catalog/trial_offers/{id} | write | product_catalog | Update a trial offer. |
| GET | v1/products | read | products | List all products. |
| POST | v1/products | write | products | Create a product. |
| GET | v1/products/search | read | products | Search products. |
| GET | v1/products/{id} | read | products | Retrieve a product. |
| POST | v1/products/{id} | write | products | Update a product. |
| DELETE | v1/products/{id} | write | products | Delete a product. |
| GET | v1/products/{id}/features | read | products | List all features attached to a product. |
| POST | v1/products/{id}/features | write | products | Attach a feature to a product. |
| GET | v1/products/{id}/features/{id} | read | products | Retrieve a product_feature. |
| DELETE | v1/products/{id}/features/{id} | write | products | Remove a feature from a product. |
| GET | v1/promotion_codes | read | promotion_codes | List all promotion codes. |
| POST | v1/promotion_codes | write | promotion_codes | Create a promotion code. |
| GET | v1/promotion_codes/{id} | read | promotion_codes | Retrieve a promotion code. |
| POST | v1/promotion_codes/{id} | write | promotion_codes | Update a promotion code. |
| GET | v1/quotes | read | quotes | List all quotes. |
| POST | v1/quotes | write | quotes | Create a quote. |
| GET | v1/quotes/{id} | read | quotes | Retrieve a quote. |
| POST | v1/quotes/{id} | write | quotes | Update a quote. |
| POST | v1/quotes/{id}/accept | write | quotes | Accept a quote. |
| POST | v1/quotes/{id}/cancel | write | quotes | Cancel a quote. |
| GET | v1/quotes/{id}/computed_upfront_line_items | read | quotes | Retrieve a quote's upfront line items. |
| POST | v1/quotes/{id}/finalize | write | quotes | Finalize a quote. |
| GET | v1/quotes/{id}/line_items | read | quotes | Retrieve a quote's line items. |
| GET | v1/radar/early_fraud_warnings | read | radar | List all early fraud warnings. |
| GET | v1/radar/early_fraud_warnings/{id} | read | radar | Retrieve an early fraud warning. |
| POST | v1/radar/payment_evaluations | write | radar | Create a Payment Evaluation. |
| GET | v1/radar/value_list_items | read | radar | List all value list items. |
| POST | v1/radar/value_list_items | write | radar | Create a value list item. |
| GET | v1/radar/value_list_items/{id} | read | radar | Retrieve a value list item. |
| DELETE | v1/radar/value_list_items/{id} | write | radar | Delete a value list item. |
| GET | v1/radar/value_lists | read | radar | List all value lists. |
| POST | v1/radar/value_lists | write | radar | Create a value list. |
| GET | v1/radar/value_lists/{id} | read | radar | Retrieve a value list. |
| POST | v1/radar/value_lists/{id} | write | radar | Update a value list. |
| DELETE | v1/radar/value_lists/{id} | write | radar | Delete a value list. |
| GET | v1/refunds | read | refunds | List all refunds. |
| POST | v1/refunds | write | refunds | Create a refund. |
| GET | v1/refunds/{id} | read | refunds | Retrieve a refund. |
| POST | v1/refunds/{id} | write | refunds | Update a refund. |
| POST | v1/refunds/{id}/cancel | write | refunds | Cancel a refund. |
| GET | v1/reporting/report_runs | read | reporting | List all Report Runs. |
| POST | v1/reporting/report_runs | write | reporting | Create a Report Run. |
| GET | v1/reporting/report_runs/{id} | read | reporting | Retrieve a Report Run. |
| GET | v1/reporting/report_types | read | reporting | List all Report Types. |
| GET | v1/reporting/report_types/{id} | read | reporting | Retrieve a Report Type. |
| GET | v1/reviews | read | reviews | List all open reviews. |
| GET | v1/reviews/{id} | read | reviews | Retrieve a review. |
| POST | v1/reviews/{id}/approve | write | reviews | Approve a review. |
| GET | v1/setup_attempts | read | setup_attempts | List all SetupAttempts. |
| GET | v1/setup_intents | read | setup_intents | List all SetupIntents. |
| POST | v1/setup_intents | write | setup_intents | Create a SetupIntent. |
| GET | v1/setup_intents/{id} | read | setup_intents | Retrieve a SetupIntent. |
| POST | v1/setup_intents/{id} | write | setup_intents | Update a SetupIntent. |
| POST | v1/setup_intents/{id}/cancel | write | setup_intents | Cancel a SetupIntent. |
| POST | v1/setup_intents/{id}/confirm | write | setup_intents | Confirm a SetupIntent. |
| POST | v1/setup_intents/{id}/verify_microdeposits | write | setup_intents | Verify microdeposits on a SetupIntent. |
| GET | v1/shipping_rates | read | shipping_rates | List all shipping rates. |
| POST | v1/shipping_rates | write | shipping_rates | Create a shipping rate. |
| GET | v1/shipping_rates/{id} | read | shipping_rates | Retrieve a shipping rate. |
| POST | v1/shipping_rates/{id} | write | shipping_rates | Update a shipping rate. |
| POST | v1/sigma/saved_queries/{id} | write | sigma | Update an existing Sigma Query. |
| GET | v1/sigma/scheduled_query_runs | read | sigma | List all scheduled query runs. |
| GET | v1/sigma/scheduled_query_runs/{id} | read | sigma | Retrieve a scheduled query run. |
| POST | v1/sources | write | sources | Create a source. |
| GET | v1/sources/{id} | read | sources | Retrieve a source. |
| POST | v1/sources/{id} | write | sources | Update a source. |
| GET | v1/sources/{id}/mandate_notifications/{id} | read | sources | Retrieve a Source MandateNotification. |
| GET | v1/sources/{id}/source_transactions | read | sources | List source transactions for a given source. |
| GET | v1/sources/{id}/source_transactions/{id} | read | sources | Retrieve a source transaction. |
| POST | v1/sources/{id}/verify | write | sources | Verify a given source. |
| GET | v1/subscription_items | read | subscription_items | List all subscription items. |
| POST | v1/subscription_items | write | subscription_items | Create a subscription item. |
| GET | v1/subscription_items/{id} | read | subscription_items | Retrieve a subscription item. |
| POST | v1/subscription_items/{id} | write | subscription_items | Update a subscription item. |
| DELETE | v1/subscription_items/{id} | write | subscription_items | Delete a subscription item. |
| GET | v1/subscription_schedules | read | subscription_schedules | List all schedules. |
| POST | v1/subscription_schedules | write | subscription_schedules | Create a schedule. |
| GET | v1/subscription_schedules/{id} | read | subscription_schedules | Retrieve a schedule. |
| POST | v1/subscription_schedules/{id} | write | subscription_schedules | Update a schedule. |
| POST | v1/subscription_schedules/{id}/cancel | write | subscription_schedules | Cancel a schedule. |
| POST | v1/subscription_schedules/{id}/release | write | subscription_schedules | Release a schedule. |
| GET | v1/subscriptions | read | subscriptions | List subscriptions. |
| POST | v1/subscriptions | write | subscriptions | Create a subscription. |
| GET | v1/subscriptions/search | read | subscriptions | Search subscriptions. |
| GET | v1/subscriptions/{id} | read | subscriptions | Retrieve a subscription. |
| POST | v1/subscriptions/{id} | write | subscriptions | Update a subscription. |
| DELETE | v1/subscriptions/{id} | write | subscriptions | Cancel a subscription. |
| DELETE | v1/subscriptions/{id}/discount | write | subscriptions | Delete a subscription discount. |
| POST | v1/subscriptions/{id}/migrate | write | subscriptions | Migrate a subscription. |
| POST | v1/subscriptions/{id}/pause | write | subscriptions | Pause a subscription. |
| POST | v1/subscriptions/{id}/resume | write | subscriptions | Resume a subscription. |
| GET | v1/tax/associations/find | read | tax | Find a Tax Association. |
| POST | v1/tax/calculations | write | tax | Create a Calculation. |
| GET | v1/tax/calculations/{id} | read | tax | Retrieve a Calculation. |
| GET | v1/tax/calculations/{id}/line_items | read | tax | Retrieve a Calculation's line items. |
| GET | v1/tax/locations | read | tax | List tax locations. |
| POST | v1/tax/locations | write | tax | Create a tax location. |
| GET | v1/tax/locations/{id} | read | tax | Retrieve a tax location. |
| GET | v1/tax/registrations | read | tax | List registrations. |
| POST | v1/tax/registrations | write | tax | Create a registration. |
| GET | v1/tax/registrations/{id} | read | tax | Retrieve a registration. |
| POST | v1/tax/registrations/{id} | write | tax | Update a registration. |
| GET | v1/tax/settings | read | tax | Retrieve settings. |
| POST | v1/tax/settings | write | tax | Update settings. |
| POST | v1/tax/transactions/create_from_calculation | write | tax | Create a Transaction from a Calculation. |
| POST | v1/tax/transactions/create_reversal | write | tax | Create a reversal Transaction. |
| GET | v1/tax/transactions/{id} | read | tax | Retrieve a Transaction. |
| GET | v1/tax/transactions/{id}/line_items | read | tax | Retrieve a Transaction's line items. |
| GET | v1/tax_codes | read | tax_codes | List all tax codes. |
| GET | v1/tax_codes/{id} | read | tax_codes | Retrieve a tax code. |
| GET | v1/tax_ids | read | tax_ids | List all tax IDs. |
| POST | v1/tax_ids | write | tax_ids | Create a tax ID. |
| GET | v1/tax_ids/{id} | read | tax_ids | Retrieve a tax ID. |
| DELETE | v1/tax_ids/{id} | write | tax_ids | Delete a tax ID. |
| GET | v1/tax_rates | read | tax_rates | List all tax rates. |
| POST | v1/tax_rates | write | tax_rates | Create a tax rate. |
| GET | v1/tax_rates/{id} | read | tax_rates | Retrieve a tax rate. |
| POST | v1/tax_rates/{id} | write | tax_rates | Update a tax rate. |
| GET | v1/terminal/configurations | write | terminal | List all Configurations. Kept out of read: reader Wi-Fi passwords. |
| POST | v1/terminal/configurations | write | terminal | Create a Configuration. |
| GET | v1/terminal/configurations/{id} | write | terminal | Retrieve a Configuration. Kept out of read: reader Wi-Fi passwords. |
| POST | v1/terminal/configurations/{id} | write | terminal | Update a Configuration. |
| DELETE | v1/terminal/configurations/{id} | write | terminal | Delete a Configuration. |
| POST | v1/terminal/connection_tokens | write | terminal | Create a Connection Token. |
| GET | v1/terminal/locations | read | terminal | List all Locations. |
| POST | v1/terminal/locations | write | terminal | Create a Location. |
| GET | v1/terminal/locations/{id} | read | terminal | Retrieve a Location. |
| POST | v1/terminal/locations/{id} | write | terminal | Update a Location. |
| DELETE | v1/terminal/locations/{id} | write | terminal | Delete a Location. |
| POST | v1/terminal/onboarding_links | write | terminal | Create an Onboarding Link. |
| GET | v1/terminal/readers | read | terminal | List all Readers. |
| POST | v1/terminal/readers | write | terminal | Create a Reader. |
| GET | v1/terminal/readers/{id} | read | terminal | Retrieve a Reader. |
| POST | v1/terminal/readers/{id} | write | terminal | Update a Reader. |
| DELETE | v1/terminal/readers/{id} | write | terminal | Delete a Reader. |
| POST | v1/terminal/readers/{id}/cancel_action | write | terminal | Cancel the current reader action. |
| POST | v1/terminal/readers/{id}/collect_inputs | write | terminal | Collect inputs using a Reader. |
| POST | v1/terminal/readers/{id}/collect_payment_method | write | terminal | Hand off a PaymentIntent to a Reader and collect card details. |
| POST | v1/terminal/readers/{id}/confirm_payment_intent | write | terminal | Confirm a PaymentIntent on the Reader. |
| POST | v1/terminal/readers/{id}/process_payment_intent | write | terminal | Hand-off a PaymentIntent to a Reader. |
| POST | v1/terminal/readers/{id}/process_setup_intent | write | terminal | Hand-off a SetupIntent to a Reader. |
| POST | v1/terminal/readers/{id}/refund_payment | write | terminal | Refund a Charge or a PaymentIntent in-person. |
| POST | v1/terminal/readers/{id}/set_reader_display | write | terminal | Set reader display. |
| POST | v1/terminal/refunds | write | terminal | Create a refund using a Terminal-supported device. |
| POST | v1/test_helpers/confirmation_tokens | write | test_helpers | Create a test Confirmation Token. |
| POST | v1/test_helpers/customers/{id}/fund_cash_balance | write | test_helpers | Fund a test mode cash balance. |
| POST | v1/test_helpers/issuing/authorizations | write | test_helpers | Create a test-mode authorization. |
| POST | v1/test_helpers/issuing/authorizations/{id}/capture | write | test_helpers | Capture a test-mode authorization. |
| POST | v1/test_helpers/issuing/authorizations/{id}/expire | write | test_helpers | Expire a test-mode authorization. |
| POST | v1/test_helpers/issuing/authorizations/{id}/finalize_amount | write | test_helpers | Finalize a test-mode authorization's amount. |
| POST | v1/test_helpers/issuing/authorizations/{id}/fraud_challenges/respond | write | test_helpers | Respond to fraud challenge. |
| POST | v1/test_helpers/issuing/authorizations/{id}/increment | write | test_helpers | Increment a test-mode authorization. |
| POST | v1/test_helpers/issuing/authorizations/{id}/reverse | write | test_helpers | Reverse a test-mode authorization. |
| POST | v1/test_helpers/issuing/cards/{id}/shipping/deliver | write | test_helpers | Deliver a testmode card. |
| POST | v1/test_helpers/issuing/cards/{id}/shipping/fail | write | test_helpers | Fail a testmode card. |
| POST | v1/test_helpers/issuing/cards/{id}/shipping/return | write | test_helpers | Return a testmode card. |
| POST | v1/test_helpers/issuing/cards/{id}/shipping/ship | write | test_helpers | Ship a testmode card. |
| POST | v1/test_helpers/issuing/cards/{id}/shipping/submit | write | test_helpers | Submit a testmode card. |
| POST | v1/test_helpers/issuing/personalization_designs/{id}/activate | write | test_helpers | Activate a testmode personalization design. |
| POST | v1/test_helpers/issuing/personalization_designs/{id}/deactivate | write | test_helpers | Deactivate a testmode personalization design. |
| POST | v1/test_helpers/issuing/personalization_designs/{id}/reject | write | test_helpers | Reject a testmode personalization design. |
| POST | v1/test_helpers/issuing/settlements | write | test_helpers | Create a test-mode settlement. |
| POST | v1/test_helpers/issuing/settlements/{id}/complete | write | test_helpers | Complete a test-mode settlement. |
| POST | v1/test_helpers/issuing/transactions/create_force_capture | write | test_helpers | Create a test-mode force capture. |
| POST | v1/test_helpers/issuing/transactions/create_unlinked_refund | write | test_helpers | Create a test-mode unlinked refund. |
| POST | v1/test_helpers/issuing/transactions/{id}/refund | write | test_helpers | Refund a test-mode transaction. |
| POST | v1/test_helpers/refunds/{id}/expire | write | test_helpers | Expire a pending refund. |
| POST | v1/test_helpers/terminal/readers/{id}/present_payment_method | write | test_helpers | Simulate presenting a payment method. |
| POST | v1/test_helpers/terminal/readers/{id}/succeed_input_collection | write | test_helpers | Simulate a successful input collection. |
| POST | v1/test_helpers/terminal/readers/{id}/timeout_input_collection | write | test_helpers | Simulate an input collection timeout. |
| GET | v1/test_helpers/test_clocks | read | test_helpers | List all test clocks. |
| POST | v1/test_helpers/test_clocks | write | test_helpers | Create a test clock. |
| GET | v1/test_helpers/test_clocks/{id} | read | test_helpers | Retrieve a test clock. |
| DELETE | v1/test_helpers/test_clocks/{id} | write | test_helpers | Delete a test clock. |
| POST | v1/test_helpers/test_clocks/{id}/advance | write | test_helpers | Advance a test clock. |
| POST | v1/test_helpers/treasury/inbound_transfers/{id}/fail | write | test_helpers | Test mode: Fail an InboundTransfer. |
| POST | v1/test_helpers/treasury/inbound_transfers/{id}/return | write | test_helpers | Test mode: Return an InboundTransfer. |
| POST | v1/test_helpers/treasury/inbound_transfers/{id}/succeed | write | test_helpers | Test mode: Succeed an InboundTransfer. |
| POST | v1/test_helpers/treasury/outbound_payments/{id} | write | test_helpers | Test mode: Update an OutboundPayment. |
| POST | v1/test_helpers/treasury/outbound_payments/{id}/fail | write | test_helpers | Test mode: Fail an OutboundPayment. |
| POST | v1/test_helpers/treasury/outbound_payments/{id}/post | write | test_helpers | Test mode: Post an OutboundPayment. |
| POST | v1/test_helpers/treasury/outbound_payments/{id}/return | write | test_helpers | Test mode: Return an OutboundPayment. |
| POST | v1/test_helpers/treasury/outbound_transfers/{id} | write | test_helpers | Test mode: Update an OutboundTransfer. |
| POST | v1/test_helpers/treasury/outbound_transfers/{id}/fail | write | test_helpers | Test mode: Fail an OutboundTransfer. |
| POST | v1/test_helpers/treasury/outbound_transfers/{id}/post | write | test_helpers | Test mode: Post an OutboundTransfer. |
| POST | v1/test_helpers/treasury/outbound_transfers/{id}/return | write | test_helpers | Test mode: Return an OutboundTransfer. |
| POST | v1/test_helpers/treasury/received_credits | write | test_helpers | Test mode: Create a ReceivedCredit. |
| POST | v1/test_helpers/treasury/received_debits | write | test_helpers | Test mode: Create a ReceivedDebit. |
| GET | v1/three_d_secure/authentications | read | three_d_secure | List all 3D Secure Authentications. |
| POST | v1/three_d_secure/authentications | write | three_d_secure | Create a 3DS Authentication. |
| GET | v1/three_d_secure/authentications/{id} | read | three_d_secure | Retrieve a 3DS Authentication. |
| POST | v1/three_d_secure/authentications/{id}/cancel | write | three_d_secure | Cancel a 3DS Authentication. |
| POST | v1/three_d_secure/authentications/{id}/submit | write | three_d_secure | Submit a 3DS Authentication. |
| POST | v1/tokens | write | tokens | Create a bank account token. |
| GET | v1/tokens/{id} | read | tokens | Retrieve a token. |
| GET | v1/topups | read | topups | List all top-ups. |
| POST | v1/topups | write | topups | Create a top-up. |
| GET | v1/topups/{id} | read | topups | Retrieve a top-up. |
| POST | v1/topups/{id} | write | topups | Update a top-up. |
| POST | v1/topups/{id}/cancel | write | topups | Cancel a top-up. |
| GET | v1/transfers | read | transfers | List all transfers. |
| POST | v1/transfers | write | transfers | Create a transfer. |
| GET | v1/transfers/{id} | read | transfers | Retrieve a transfer. |
| POST | v1/transfers/{id} | write | transfers | Update a transfer. |
| GET | v1/transfers/{id}/reversals | read | transfers | List all reversals. |
| POST | v1/transfers/{id}/reversals | write | transfers | Create a transfer reversal. |
| GET | v1/transfers/{id}/reversals/{id} | read | transfers | Retrieve a reversal. |
| POST | v1/transfers/{id}/reversals/{id} | write | transfers | Update a reversal. |
| GET | v1/treasury/credit_reversals | read | treasury | List all CreditReversals. |
| POST | v1/treasury/credit_reversals | write | treasury | Create a CreditReversal. |
| GET | v1/treasury/credit_reversals/{id} | read | treasury | Retrieve a CreditReversal. |
| GET | v1/treasury/debit_reversals | read | treasury | List all DebitReversals. |
| POST | v1/treasury/debit_reversals | write | treasury | Create a DebitReversal. |
| GET | v1/treasury/debit_reversals/{id} | read | treasury | Retrieve a DebitReversal. |
| GET | v1/treasury/financial_accounts | read | treasury | List all FinancialAccounts. |
| POST | v1/treasury/financial_accounts | write | treasury | Create a FinancialAccount. |
| GET | v1/treasury/financial_accounts/{id} | read | treasury | Retrieve a FinancialAccount. |
| POST | v1/treasury/financial_accounts/{id} | write | treasury | Update a FinancialAccount. |
| POST | v1/treasury/financial_accounts/{id}/close | write | treasury | Close a FinancialAccount. |
| GET | v1/treasury/financial_accounts/{id}/features | read | treasury | Retrieve FinancialAccount Features. |
| POST | v1/treasury/financial_accounts/{id}/features | write | treasury | Update FinancialAccount Features. |
| GET | v1/treasury/inbound_transfers | read | treasury | List all InboundTransfers. |
| POST | v1/treasury/inbound_transfers | write | treasury | Create an InboundTransfer. |
| GET | v1/treasury/inbound_transfers/{id} | read | treasury | Retrieve an InboundTransfer. |
| POST | v1/treasury/inbound_transfers/{id}/cancel | write | treasury | Cancel an InboundTransfer. |
| GET | v1/treasury/outbound_payments | read | treasury | List all OutboundPayments. |
| POST | v1/treasury/outbound_payments | write | treasury | Create an OutboundPayment. |
| GET | v1/treasury/outbound_payments/{id} | read | treasury | Retrieve an OutboundPayment. |
| POST | v1/treasury/outbound_payments/{id}/cancel | write | treasury | Cancel an OutboundPayment. |
| GET | v1/treasury/outbound_transfers | read | treasury | List all OutboundTransfers. |
| POST | v1/treasury/outbound_transfers | write | treasury | Create an OutboundTransfer. |
| GET | v1/treasury/outbound_transfers/{id} | read | treasury | Retrieve an OutboundTransfer. |
| POST | v1/treasury/outbound_transfers/{id}/cancel | write | treasury | Cancel an OutboundTransfer. |
| GET | v1/treasury/received_credits | read | treasury | List all ReceivedCredits. |
| GET | v1/treasury/received_credits/{id} | read | treasury | Retrieve a ReceivedCredit. |
| GET | v1/treasury/received_debits | read | treasury | List all ReceivedDebits. |
| GET | v1/treasury/received_debits/{id} | read | treasury | Retrieve a ReceivedDebit. |
| GET | v1/treasury/transaction_entries | read | treasury | List all TransactionEntries. |
| GET | v1/treasury/transaction_entries/{id} | read | treasury | Retrieve a TransactionEntry. |
| GET | v1/treasury/transactions | read | treasury | List all Transactions. |
| GET | v1/treasury/transactions/{id} | read | treasury | Retrieve a Transaction. |
| GET | v1/webhook_endpoints | read | webhook_endpoints | List all webhook endpoints. |
| POST | v1/webhook_endpoints | write | webhook_endpoints | Create a webhook endpoint. |
| GET | v1/webhook_endpoints/{id} | read | webhook_endpoints | Retrieve a webhook endpoint. |
| POST | v1/webhook_endpoints/{id} | write | webhook_endpoints | Update a webhook endpoint. |
| DELETE | v1/webhook_endpoints/{id} | write | webhook_endpoints | Delete a webhook endpoint. |
