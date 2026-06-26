# ThumbGate Prevention Rules: QSR WhatsApp Agent

| Rule ID | Name | Description | Severity |
| :--- | :--- | :--- | :--- |
| QSR-001 | INVENTORY_CHECK | Block confirmation of any item with inventory < 1. | Critical |
| QSR-002 | ALLERGEN_PROTOCOL | Require explicit user confirmation if "allergy" or "gluten" is mentioned. | Critical |
| QSR-003 | PRICE_MATCH | Subtotal must match the sum of individual item prices in the menu sheet. | High |
| QSR-004 | DUPLICATE_ORDER | Flag orders that are identical to a previous order within 2 minutes. | Medium |
| QSR-005 | UPSELL_ATTEMPT | Ensure at least one upsell prompt was issued for orders without a "Meal" or "Cookie". | Low |
| QSR-006 | VALID_PHONE | Do not process orders without a verified WhatsApp source ID. | High |
| QSR-007 | TAX_CALC | Tax must be exactly 8.875% (or as specified in settings). | High |
| QSR-008 | MAX_TOTAL | Block any individual order exceeding $200 without manual approval. | Medium |
| QSR-009 | STORE_HOURS | Reject orders placed outside the "store_hours" range in config. | High |
| QSR-010 | NO_PII_LOGGING | Ensure credit card details or passwords are never written to the order log. | Critical |
| QSR-011 | MOD_LIMIT | Maximum of 3 "Extra" protein modifications per sandwich. | Medium |
| QSR-012 | PICKUP_ESTIMATE | Pickup time must be at least 15 minutes from the current time. | High |
