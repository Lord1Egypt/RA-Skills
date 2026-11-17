# Shopify triggers via Agiexa (45)

Preview only - events that will be able to start an agent run after Agiexa launches (November 2026).

| Trigger | When it fires |
| --- | --- |
| `SHOPIFY_BULK_OPERATION_FINISHED` | Triggers when a bulk operation started by this app finishes, whether it completed, failed, was canceled or expired |
| `SHOPIFY_COLLECTION_CREATED` | Triggers when a collection is created |
| `SHOPIFY_COLLECTION_DELETED` | Triggers when a collection is deleted |
| `SHOPIFY_COLLECTION_UPDATED` | Triggers when a collection's own fields change, and also when a product is added to or removed from a manual collection |
| `SHOPIFY_CUSTOMER_SEGMENT_CREATED` | Triggers when a customer segment is created |
| `SHOPIFY_CUSTOMER_SEGMENT_DELETED` | Triggers when a customer segment is deleted |
| `SHOPIFY_CUSTOMER_SEGMENT_UPDATED` | Triggers when a customer segment is renamed or its query is edited |
| `SHOPIFY_DISCOUNT_CODE_ADDED` | Triggers when a redeemable code is added to a discount, once per code |
| `SHOPIFY_DISCOUNT_CODE_REMOVED` | Triggers when a redeemable code is removed from a discount, once per code |
| `SHOPIFY_DISCOUNT_CREATED` | Triggers when a discount is created, whether it applies automatically or through a code |
| `SHOPIFY_DISCOUNT_DELETED` | Triggers when a discount is deleted |
| `SHOPIFY_DISCOUNT_UPDATED` | Triggers when a discount is edited, and when it reaches its scheduled start or end and `status` changes |
| `SHOPIFY_INVENTORY_ITEM_CREATED` | Triggers when an inventory item is created, which Shopify does once per new product variant |
| `SHOPIFY_INVENTORY_ITEM_DELETED` | Triggers when an inventory item is deleted, which happens for each variant of a deleted product |
| `SHOPIFY_INVENTORY_ITEM_UPDATED` | Triggers when an inventory item's stock-keeping fields change, such as its SKU, unit cost, weight or customs codes |
| `SHOPIFY_INVENTORY_LEVEL_UPDATED` | Triggers when the quantity of an inventory item changes at a location, in either direction, once per location affected |
| `SHOPIFY_INVENTORY_SHIPMENT_CREATED` | Triggers when a shipment is created against a stock transfer, once per consignment |
| `SHOPIFY_INVENTORY_SHIPMENT_IN_TRANSIT` | Triggers when a stock shipment is marked in transit |
| `SHOPIFY_INVENTORY_SHIPMENT_ITEMS_RECEIVED` | Triggers when items from a stock shipment are received, once per receiving step |
| `SHOPIFY_INVENTORY_SHIPMENT_TRACKING_UPDATED` | Triggers when the carrier tracking on a stock shipment is set or changed |
| `SHOPIFY_INVENTORY_STOCKED_AT_LOCATION` | Triggers when an inventory item starts being stocked at a location |
| `SHOPIFY_INVENTORY_TRANSFER_READY_TO_SHIP` | Triggers when a stock transfer between the merchant's locations is marked ready to ship, before any shipment exists against it |
| `SHOPIFY_INVENTORY_UNSTOCKED_AT_LOCATION` | Triggers when an inventory item stops being stocked at a location, either because the merchant deactivated it there or because the product was deleted |
| `SHOPIFY_LOCATION_ACTIVATED` | Triggers when a location is activated and can hold stock and fulfil orders again |
| `SHOPIFY_LOCATION_CREATED` | Triggers when a location is added to the store |
| `SHOPIFY_LOCATION_DEACTIVATED` | Triggers when a location is deactivated |
| `SHOPIFY_LOCATION_DELETED` | Triggers when a location is deleted |
| `SHOPIFY_LOCATION_UPDATED` | Triggers when a location's own details change, such as its name, address or fulfilment settings |
| `SHOPIFY_MARKET_CREATED` | Triggers when a market is created |
| `SHOPIFY_MARKET_UPDATED` | Triggers when a market is renamed, activated or otherwise changed |
| `SHOPIFY_METAFIELD_DEFINITION_CREATED` | Triggers when a metafield definition is created, i.e |
| `SHOPIFY_METAFIELD_DEFINITION_DELETED` | Triggers when a metafield definition is deleted |
| `SHOPIFY_METAFIELD_DEFINITION_UPDATED` | Triggers when a metafield definition's name, description, validations, pinning or storefront access change |
| `SHOPIFY_PRODUCT_CREATED` | Triggers when a product is created, from the admin, the API, an import or an app |
| `SHOPIFY_PRODUCT_DELETED` | Triggers when a product is deleted |
| `SHOPIFY_PRODUCT_UPDATED` | Triggers when any field of a product changes, as one delivery per edit rather than one per field |
| `SHOPIFY_PRODUCT_VARIANT_BACK_IN_STOCK` | Triggers when a variant's stock crosses back above zero across every location, not on every restock |
| `SHOPIFY_PRODUCT_VARIANT_OUT_OF_STOCK` | Triggers when a variant's stock crosses to zero across every location, not on every sale |
| `SHOPIFY_SHIPPING_PROFILE_CREATED` | Triggers when a shipping profile is created |
| `SHOPIFY_SHIPPING_PROFILE_DELETED` | Triggers when a shipping profile is deleted |
| `SHOPIFY_SHIPPING_PROFILE_UPDATED` | Triggers when a shipping profile is renamed, or its zones, rates or product assignments change |
| `SHOPIFY_SHOP_SETTINGS_UPDATED` | Triggers when the store's own record changes — its address, currency, timezone, plan, tax or checkout settings |
| `SHOPIFY_STORE_LANGUAGE_ADDED` | Triggers when a language is added to the store |
| `SHOPIFY_STORE_LANGUAGE_REMOVED` | Triggers when a language is removed from the store, taking its stored translations with it |
| `SHOPIFY_STORE_LANGUAGE_UPDATED` | Triggers when a store language is published or unpublished |
