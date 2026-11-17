# Shopify tools via Agiexa (315)

Preview only - these become available to the agent after Agiexa launches (November 2026) and the merchant connects Shopify and turns the tools on. They cannot be called today.

Interactive explorer: https://agiexa.com/integrations/shopify

| Tool | What it does |
| --- | --- |
| `SHOPIFY_ADD_PRODUCT_TO_CUSTOM_COLLECTION` | Add a product to a custom collection by creating a collect resource |
| `SHOPIFY_ADJUST_INVENTORY_LEVEL` | Adjust the inventory level of an inventory item at a single location |
| `SHOPIFY_APPLY_FULFILLMENT_HOLD` | Applies a fulfillment hold to an open fulfillment order, halting all fulfillment work |
| `SHOPIFY_APPROVE_COMMENT` | Approves a pending comment and publishes it to a blog article, making it publicly visible to readers |
| `SHOPIFY_BULK_CREATE_PRODUCTS` | Creates many products (20-50+) in one asynchronous Shopify bulk mutation job |
| `SHOPIFY_BULK_DELETE_METAFIELDS` | Deletes multiple metafields in bulk using their owner ID, namespace, and key |
| `SHOPIFY_BULK_DELETE_METAOBJECTS` | Asynchronously delete metaobjects and their associated metafields in bulk |
| `SHOPIFY_BULK_QUERY_OPERATION` | Run a Shopify GraphQL bulk query operation and return the result file URL and operation metadata |
| `SHOPIFY_CALCULATE_REFUND` | Calculate accurate refund amounts, taxes, and transactions for a Shopify order before creating an actual refund |
| `SHOPIFY_CANCEL_APP_SUBSCRIPTION` | Cancel an app subscription in Shopify using the appSubscriptionCancel GraphQL mutation |
| `SHOPIFY_CANCEL_BULK_OPERATION` | Cancel a running Shopify bulk operation |
| `SHOPIFY_CANCEL_FULFILLMENT` | Cancels an existing fulfillment by its ID, reverting all line items to an unfulfilled state |
| `SHOPIFY_CANCEL_FULFILLMENT_ORDER` | Cancels a fulfillment order in Shopify and marks it as closed |
| `SHOPIFY_CANCEL_ORDER` | Cancels a Shopify order and optionally restocks items and sends email notifications |
| `SHOPIFY_CLOSE_ORDER` | Closes an open Shopify order |
| `SHOPIFY_COMPLETE_DRAFT_ORDER` | Complete a draft order in Shopify and transition it to an actual order |
| `SHOPIFY_CONNECT_INVENTORY_LEVEL` | Connects an inventory item to a location, establishing where the item can be stocked and fulfilled |
| `SHOPIFY_COUNT_ARTICLES` | Retrieves a count of all articles from a blog |
| `SHOPIFY_COUNT_BLOGS` | Retrieves the total count of all blogs in a Shopify store |
| `SHOPIFY_COUNT_DRAFT_ORDERS` | Retrieves a count of draft orders from a Shopify store |
| `SHOPIFY_COUNT_FULFILLMENTS` | Retrieves a count of fulfillments associated with a specific order |
| `SHOPIFY_COUNT_METAFIELDS` | Retrieves the shop-level count of metafields |
| `SHOPIFY_COUNT_PAGES` | Retrieve the total count of pages in a Shopify store |
| `SHOPIFY_COUNT_PRICE_RULES` | Retrieves a count of all price rules |
| `SHOPIFY_COUNT_PRODUCT_IMAGES` | Retrieves the total count of images for a specific Shopify product |
| `SHOPIFY_COUNT_PRODUCTS` | Retrieve a count of products in the Shopify store |
| `SHOPIFY_COUNT_PRODUCT_VARIANTS` | Retrieves the total count of variants for a Shopify product |
| `SHOPIFY_CREATE_A_METAFIELD` | Create a metafield for any Shopify resource |
| `SHOPIFY_CREATE_APP_SUBSCRIPTION` | Create a recurring or usage-based app subscription for charging Shopify merchants |
| `SHOPIFY_CREATE_ARTICLE` | Create an article for a blog in Shopify |
| `SHOPIFY_CREATE_ARTICLE_COMMENT` | Create a comment for an article in Shopify |
| `SHOPIFY_CREATE_BLOG` | Create a new blog in Shopify |
| `SHOPIFY_CREATE_CUSTOM_COLLECTION` | Create a new custom (manually curated) collection in Shopify |
| `SHOPIFY_CREATE_CUSTOMER` | Create a new customer in Shopify |
| `SHOPIFY_CREATE_CUSTOMER_ACCOUNT_ACTIVATION_URL` | Generate a one-time account activation URL for a customer whose account is in 'disabled' state (not yet activated) |
| `SHOPIFY_CREATE_CUSTOMER_ADDRESS` | Create a new address for a customer |
| `SHOPIFY_CREATE_DELEGATE_ACCESS_TOKEN` | Create a delegate access token with a subset of the parent token's permissions |
| `SHOPIFY_CREATE_DISCOUNT_CODE` | Creates a discount code for an existing price rule |
| `SHOPIFY_CREATE_DISCOUNT_CODE_BATCH` | Create a discount code creation job for batch processing |
| `SHOPIFY_CREATE_DRAFT_ORDER` | Create a draft order in Shopify |
| `SHOPIFY_CREATE_EVENT_BRIDGE_WEBHOOK_SUBSCRIPTION` | Create an AWS EventBridge webhook subscription in Shopify |
| `SHOPIFY_CREATE_FULFILLMENT` | Creates a fulfillment for one or many fulfillment orders for a specific order |
| `SHOPIFY_CREATE_FULFILLMENT_EVENT` | Creates a tracking event for a fulfillment to update shipment status |
| `SHOPIFY_CREATE_GIFT_CARD` | Create a gift card for a Shopify store |
| `SHOPIFY_CREATE_MARKETING_ENGAGEMENTS` | Create engagement data for a marketing event in Shopify |
| `SHOPIFY_CREATE_MARKETING_EVENT` | Create a marketing event in Shopify to track promotional actions |
| `SHOPIFY_CREATE_METAFIELD` | Creates a new metafield for a Shopify blog |
| `SHOPIFY_CREATE_ONE_TIME_APPLICATION_CHARGE` | Create a new one-time application charge in Shopify |
| `SHOPIFY_CREATE_ORDER` | Create a fully committed (real) order in Shopify without payment processing |
| `SHOPIFY_CREATE_ORDER_TRANSACTION` | Creates a transaction for an order to process payment operations |
| `SHOPIFY_CREATE_PAGE` | Create a static web page in Shopify |
| `SHOPIFY_CREATE_PRICE_RULE` | Creates a price rule that defines discount logic for Shopify orders |
| `SHOPIFY_CREATE_PRODUCT_METAFIELD` | Creates a new metafield for a specific Shopify product |
| `SHOPIFY_CREATE_PRODUCT_VARIANT` | Create a new product variant for an existing product |
| `SHOPIFY_CREATE_PUB_SUB_WEBHOOK_SUBSCRIPTION` | Create a Google Cloud Pub/Sub webhook subscription in Shopify |
| `SHOPIFY_CREATE_REDIRECT` | Create a URL redirect in Shopify |
| `SHOPIFY_CREATE_REFUND` | Creates a refund for a Shopify order |
| `SHOPIFY_CREATE_RESOURCE_FEEDBACK` | Creates shop-level resource feedback to notify Shopify merchants about app setup requirements or successful configuration |
| `SHOPIFY_CREATE_SCRIPT_TAG` | Create a new script tag in Shopify to load remote JavaScript into your online store |
| `SHOPIFY_CREATE_SMART_COLLECTIONS` | Create a new smart collection with automated product rules |
| `SHOPIFY_CREATES_OR_UPDATES_AN_ASSET_FOR_A_THEME` | Creates or updates a theme asset file (templates, stylesheets, scripts, or images) within a Shopify theme |
| `SHOPIFY_CREATE_STOREFRONT_ACCESS_TOKEN` | Creates a new storefront access token for unauthenticated Storefront API access |
| `SHOPIFY_CREATE_THEME` | Creates a new theme in Shopify from a ZIP file containing theme assets |
| `SHOPIFY_CREATE_WEBHOOK_SUBSCRIPTION` | Create a webhook subscription that notifies your app when specific events occur in a Shopify store |
| `SHOPIFY_DELETE_ARTICLE` | Delete an article from a blog in Shopify |
| `SHOPIFY_DELETE_BLOG` | Permanently deletes a blog from a Shopify store using its `blog_id`; this action is irreversible and requires the 'content' access scope |
| `SHOPIFY_DELETE_COLLECT` | Removes a product from a custom collection by deleting the collect |
| `SHOPIFY_DELETE_COMMENT` | Remove a comment from a Shopify blog |
| `SHOPIFY_DELETE_CUSTOMER` | Deletes a customer from the Shopify store |
| `SHOPIFY_DELETE_CUSTOMER_ADDRESS` | Removes an address from a customer's address list |
| `SHOPIFY_DELETE_DRAFT_ORDER` | Delete a draft order from Shopify |
| `SHOPIFY_DELETE_FULFILLMENT_SERVICE` | Remove an existing fulfillment service from a Shopify store |
| `SHOPIFY_DELETE_INVENTORY_LEVEL` | Deletes an inventory level of an inventory item at a location |
| `SHOPIFY_DELETE_MARKETING_EVENT` | Delete a marketing event from Shopify |
| `SHOPIFY_DELETE_METAFIELD` | Deletes a metafield by its ID from any Shopify resource |
| `SHOPIFY_DELETE_METAOBJECT` | Deletes a metaobject and its associated metafields using GraphQL mutation |
| `SHOPIFY_DELETE_METAOBJECT_DEFINITION` | Delete a metaobject definition and all its associated data |
| `SHOPIFY_DELETE_ORDER` | Permanently delete an order from Shopify |
| `SHOPIFY_DELETE_PAGE` | Delete a page from a Shopify store permanently |
| `SHOPIFY_DELETE_PRICE_RULE` | Deletes an existing price rule from the Shopify store permanently |
| `SHOPIFY_DELETE_PRODUCT` | Permanently deletes a product from a Shopify store by its product ID |
| `SHOPIFY_DELETE_PRODUCT_IMAGE` | Deletes a specific image from a product in Shopify, requiring the `product_id` of an existing product and the `image_id` of an image currently associa |
| `SHOPIFY_DELETE_PRODUCT_METAFIELD` | Deletes a specific metafield from a Shopify product using the product ID and metafield ID |
| `SHOPIFY_DELETE_PRODUCT_VARIANT` | Deletes a specific product variant from a Shopify store using its unique product ID and variant ID; this action is irreversible |
| `SHOPIFY_DELETE_REDIRECT` | Permanently deletes a URL redirect from a Shopify store |
| `SHOPIFY_DELETES_A_CUSTOM_COLLECTION` | Permanently delete a custom collection from a Shopify store |
| `SHOPIFY_DELETES_A_DISCOUNT_CODE` | Delete a discount code from a price rule |
| `SHOPIFY_DELETE_SAVED_SEARCH` | Delete a saved search in Shopify |
| `SHOPIFY_DELETE_SMART_COLLECTION` | Permanently removes a smart collection from a Shopify store using its `smart_collection_id`; this action is irreversible and requires a valid, existin |
| `SHOPIFY_DELETE_STOREFRONT_ACCESS_TOKEN` | Delete an existing storefront access token from a Shopify store |
| `SHOPIFY_DELETE_THEME` | Deletes a theme from the Shopify store by its ID |
| `SHOPIFY_DELETE_THEME_ASSET` | Delete an asset from a Shopify theme |
| `SHOPIFY_DELETE_WEBHOOK_SUBSCRIPTION` | Delete a webhook subscription and stop all future webhooks to its endpoint |
| `SHOPIFY_DELETE_WEB_PRESENCE` | Delete a web presence from Shopify |
| `SHOPIFY_DISABLE_GIFT_CARD` | Disable a gift card in Shopify |
| `SHOPIFY_ENABLE_STANDARD_METAOBJECT_DEFINITION` | Enable a standard metaobject definition from its template |
| `SHOPIFY_GET_ABANDONMENT` | Retrieves an abandonment record from Shopify using its unique ID |
| `SHOPIFY_GET_ABANDONMENT_BY_ABANDONED_CHECKOUT_ID` | Query abandonment information by abandoned checkout ID using Shopify's GraphQL Admin API |
| `SHOPIFY_GET_ACCESS_SCOPES` | Retrieves a list of access scopes associated with the access token |
| `SHOPIFY_GET_APP` | Query information about a Shopify app using the GraphQL API |
| `SHOPIFY_GET_APP_BY_HANDLE` | Query app information by handle using the Shopify Admin GraphQL API |
| `SHOPIFY_GET_APP_INSTALLATION` | Query a specific app installation on a Shopify store |
| `SHOPIFY_GET_APPLICATION_CHARGE_BY_ID` | Retrieve a single application charge by its unique identifier |
| `SHOPIFY_GET_APPLICATION_CHARGES` | Retrieves a list of one-time application charges for the current app installation |
| `SHOPIFY_GET_APPLICATION_CREDITS` | Retrieve all application credits for a shop |
| `SHOPIFY_GET_ARTICLE` | Retrieves a single article from a Shopify blog by its ID |
| `SHOPIFY_GET_BATCH_DISCOUNT_CODES` | Retrieves discount codes from a batch creation job, showing which succeeded and which failed |
| `SHOPIFY_GET_BLOG` | Retrieve a single blog by its unique identifier |
| `SHOPIFY_GET_BLOG_ARTICLE_TAGS` | Retrieve a list of all article tags from a specific blog |
| `SHOPIFY_GET_BULK_OPERATION` | Query the status and details of a Shopify bulk operation by its ID |
| `SHOPIFY_GET_CARRIER_SERVICES` | Retrieves all active carrier services configured in a Shopify store |
| `SHOPIFY_GET_CATALOGS_COUNT` | Query the count of catalogs in the Shopify store |
| `SHOPIFY_GET_CHECKOUT_PROFILE` | Retrieves a checkout profile from Shopify using its unique ID |
| `SHOPIFY_GET_CHECKOUTS_COUNT` | Retrieves a count of abandoned checkouts from the past 90 days |
| `SHOPIFY_GET_COLLECT_BY_ID` | Retrieves a specific collect by its ID |
| `SHOPIFY_GET_COLLECTION_BY_ID` | Retrieves a specific Shopify collection by its `collection_id`, optionally filtering returned data to specified `fields` |
| `SHOPIFY_GET_COLLECTION_BY_IDENTIFIER` | Query a collection by identifier (ID or handle) using the Shopify GraphQL Admin API |
| `SHOPIFY_GET_COLLECTS` | Retrieves a list of collects from a Shopify store, where a collect links a product to a custom collection |
| `SHOPIFY_GET_COLLECTS_COUNT` | Retrieves a count of collects (product-collection relationships) |
| `SHOPIFY_GET_COMMENTS_COUNT` | Retrieves a count of comments |
| `SHOPIFY_GET_CONSENT_POLICY` | Query consent policies for privacy compliance requirements |
| `SHOPIFY_GET_COUNTRIES` | Retrieve a list of countries configured in the Shopify store with tax rates and provinces |
| `SHOPIFY_GET_COUNTRIES_PARAM_COUNTRY_ID_PROVINCES_COUNT` | Retrieves a count of provinces for a country |
| `SHOPIFY_GET_COUNTRIES_PARAM_COUNTRY_ID_PROVINCES_PARAM_PROVI` | Get Province for Country |
| `SHOPIFY_GET_COUNTRY` | Retrieve a specific country by its ID from Shopify |
| `SHOPIFY_GET_COUNTRY_PROVINCES` | Retrieve a list of provinces for a specified country |
| `SHOPIFY_GET_CURRENCIES` | Retrieve a list of currencies enabled on a Shopify store |
| `SHOPIFY_GET_CUSTOM_COLLECTION_BY_ID` | Retrieve a single custom collection by its unique ID from Shopify |
| `SHOPIFY_GET_CUSTOM_COLLECTIONS` | Retrieves a list of custom collections from a Shopify store |
| `SHOPIFY_GET_CUSTOM_COLLECTIONS_COUNT` | Retrieves the total count of custom collections in a Shopify store with optional filters |
| `SHOPIFY_GET_CUSTOMER` | Retrieve a single customer by their unique identifier |
| `SHOPIFY_GET_CUSTOMER_ADDRESS` | Retrieve details of a single customer address from Shopify |
| `SHOPIFY_GET_CUSTOMER_ADDRESSES` | Retrieves all addresses associated with a specific customer |
| `SHOPIFY_GET_CUSTOMER_ORDERS` | Retrieves all orders for a specific, existing customer in Shopify using their unique customer ID |
| `SHOPIFY_GET_CUSTOMERS_COUNT` | Retrieves a count of all customers |
| `SHOPIFY_GET_CUSTOMERS_SEARCH` | Search for customers matching a supplied query |
| `SHOPIFY_GET_DISCOUNT_CODE` | Retrieves a single discount code for a price rule |
| `SHOPIFY_GET_DISCOUNT_CODE_BATCH_JOB` | Retrieves the status and progress of an asynchronous batch discount code creation job for a specific price rule |
| `SHOPIFY_GET_DISCOUNT_CODES_COUNT` | Retrieves a count of discount codes for a shop |
| `SHOPIFY_GET_DISCOUNT_CODES_LOOKUP` | Look up a discount code by its code name and retrieve its resource location and IDs |
| `SHOPIFY_GET_DRAFT_ORDER` | Retrieve detailed information for a specific draft order from a Shopify store |
| `SHOPIFY_GET_EVENT` | Retrieve a specific Shopify event by its ID |
| `SHOPIFY_GET_FULFILLMENT` | Retrieves all fulfillments (shipments) associated with a specific fulfillment order |
| `SHOPIFY_GET_FULFILLMENT_EVENTS` | Retrieves tracking events for a specific fulfillment, showing shipment status updates (e.g., in_transit, out_for_delivery, delivered) with timestamps |
| `SHOPIFY_GET_FULFILLMENT_ORDER_LOCATIONS_FOR_MOVE` | Retrieve locations that a fulfillment order can potentially move to |
| `SHOPIFY_GET_FULFILLMENT_ORDERS_FOR_ORDER` | Retrieves a list of fulfillment orders for a specific order |
| `SHOPIFY_GET_FULFILLMENT_SERVICES` | Retrieve a list of fulfillment services available on the Shopify store |
| `SHOPIFY_GET_GIFT_CARD_BY_ID` | Retrieves detailed information about a specific gift card by its ID |
| `SHOPIFY_GET_GIFT_CARDS` | Retrieve a list of gift cards from Shopify |
| `SHOPIFY_GET_GIFT_CARDS_COUNT` | Retrieves the total count of gift cards in the store |
| `SHOPIFY_GET_INVENTORY_ITEM` | Retrieves a single inventory item by ID |
| `SHOPIFY_GET_INVENTORY_ITEMS` | Retrieves a list of inventory items by specified IDs |
| `SHOPIFY_GET_INVENTORY_LEVELS` | Retrieves a list of inventory levels for specified items and locations |
| `SHOPIFY_GET_INVENTORY_LEVELS_FOR_LOCATION` | Retrieves a list of inventory levels for a specific location |
| `SHOPIFY_GET_LOCATION` | Retrieve a single location by its ID |
| `SHOPIFY_GET_LOCATIONS_COUNT` | Query the count of locations in a Shopify store using the GraphQL API |
| `SHOPIFY_GET_MARKETING_EVENT` | Retrieves detailed information about a specific marketing event by its ID |
| `SHOPIFY_GET_MARKETING_EVENTS_COUNT` | Retrieves a count of all marketing events in the store |
| `SHOPIFY_GET_METAFIELD` | Retrieve a list of metafields from a blog resource |
| `SHOPIFY_GET_METAFIELD_BY_ID` | Retrieve a single metafield from a resource by its ID |
| `SHOPIFY_GET_METAFIELDS` | Retrieve a list of metafields |
| `SHOPIFY_GET_ORDER` | Retrieve a specific order using its unique identifier |
| `SHOPIFY_GET_ORDER_FULFILLMENTS` | Retrieve fulfillments associated with a Shopify order |
| `SHOPIFY_GET_ORDER_REFUND_BY_ID` | Retrieves a specific refund by refund ID for an order |
| `SHOPIFY_GET_ORDER_REFUNDS` | Retrieves a list of all refunds for a specific order |
| `SHOPIFY_GET_ORDERS_WITH_FILTERS` | Retrieves Shopify orders filtered by dates and other filters |
| `SHOPIFY_GET_ORDER_TRANSACTIONS_COUNT` | Retrieve a count of an order's transactions in Shopify |
| `SHOPIFY_GET_PAGE_BY_ID` | Retrieve a single Shopify page by its unique ID |
| `SHOPIFY_GET_POLICIES` | Retrieve a list of the shop's policies |
| `SHOPIFY_GET_PRICE_RULE_BATCH_INFO` | Checks if batch listing is supported for a price rule and provides guidance on alternatives |
| `SHOPIFY_GET_PRICE_RULE_DISCOUNT_CODES` | Retrieve a list of discount codes for a price rule |
| `SHOPIFY_GET_PRODUCT` | Retrieves details for an existing Shopify product using its unique product ID |
| `SHOPIFY_GET_PRODUCT_IMAGE` | Retrieve a single product image by ID for a specific product |
| `SHOPIFY_GET_PRODUCT_METAFIELD` | Retrieves a specific metafield for a Shopify product using the product ID and metafield ID |
| `SHOPIFY_GET_PRODUCT_METAFIELDS` | Retrieves all metafields for a specific Shopify product |
| `SHOPIFY_GET_PRODUCTS_PAGINATED` | List products with Shopify cursor-based pagination |
| `SHOPIFY_GET_PRODUCT_VARIANT` | Retrieves detailed information about a single product variant by its ID from Shopify |
| `SHOPIFY_GET_RECURRING_APPLICATION_CHARGES` | Retrieve a list of recurring application charges for the app |
| `SHOPIFY_GET_REDIRECT_BY_ID` | Retrieve a single redirect by its ID |
| `SHOPIFY_GET_REDIRECTS` | Retrieve a list of URL redirects from a Shopify store |
| `SHOPIFY_GET_REDIRECTS_COUNT` | Retrieves a count of URL redirects in the store |
| `SHOPIFY_GET_SCRIPTTAG` | Retrieves a single script tag by its ID |
| `SHOPIFY_GET_SEGMENTS_COUNT` | Query the number of segments for a shop |
| `SHOPIFY_GET_SHIPPING_ZONES` | Retrieve all configured shipping zones with countries, provinces, tax rates, and shipping rates |
| `SHOPIFY_GET_SHOP_BILLING_ADDRESS` | Retrieves the billing address for the shop via GraphQL query |
| `SHOPIFY_GET_SMART_COLLECTION_BY_ID` | Retrieve a single smart collection by its ID |
| `SHOPIFY_GET_SMART_COLLECTIONS` | Retrieve a list of smart collections from a Shopify store |
| `SHOPIFY_GET_SMART_COLLECTIONS_COUNT` | Retrieve a count of smart collections in a Shopify store |
| `SHOPIFY_GET_STOREFRONT_ACCESS_TOKENS` | Retrieves a list of storefront access tokens that have been issued for the shop |
| `SHOPIFY_GET_TENDER_TRANSACTIONS` | Retrieve a list of tender transactions from Shopify |
| `SHOPIFY_GET_THEME` | Retrieves a single Shopify theme by its unique ID |
| `SHOPIFY_GET_THEMES` | Retrieves a list of themes from a Shopify store |
| `SHOPIFY_GET_THEMES_PARAM_THEME_ID_ASSETS` | Retrieve a single asset for a theme by its key |
| `SHOPIFY_GET_TRANSACTION` | Retrieve a specific transaction for an order |
| `SHOPIFY_GET_WEBHOOK` | Retrieves a single webhook subscription by its ID |
| `SHOPIFY_GET_WEBHOOK_SUBSCRIPTIONS_COUNT` | Query the number of webhook subscriptions for a shop |
| `SHOPIFY_GRAPH_QL_ADMIN_EXECUTE` | Execute any Shopify Admin GraphQL query or mutation with variables |
| `SHOPIFY_GRAPH_QL_COLLECTIONS` | Shopify GraphQL collections and publication-ready collection reads |
| `SHOPIFY_GRAPH_QL_CUSTOMERS` | Shopify GraphQL customers and customer search |
| `SHOPIFY_GRAPH_QL_DISCOUNTS` | Shopify GraphQL discounts and discount search |
| `SHOPIFY_GRAPH_QL_DRAFT_ORDERS` | Shopify GraphQL draft orders |
| `SHOPIFY_GRAPH_QL_INVENTORY` | Shopify GraphQL inventory items and levels |
| `SHOPIFY_GRAPH_QL_METAFIELDS_METAOBJECTS` | Canonical GraphQL read surface for metafields, metafield definitions, and metaobjects |
| `SHOPIFY_GRAPH_QL_ORDERS` | Shopify GraphQL orders and order search |
| `SHOPIFY_GRAPH_QL_PRODUCTS` | GraphQL-first product toolkit: products, variants, options, media, and publications |
| `SHOPIFY_GRAPH_QL_QUERY` | Executes a GraphQL query against the Shopify Admin API for flexible data retrieval and mutations including metafields |
| `SHOPIFY_GRAPH_QL_SHOP` | GraphQL-first shop, app installation, and configuration read action |
| `SHOPIFY_GRAPH_QL_WEBHOOKS` | Shopify GraphQL webhook subscriptions |
| `SHOPIFY_GRAPH_QL_WRITE_OPERATIONS` | Canonical GraphQL write surface for Shopify orders, customers, inventory, discounts, collections, webhooks, fulfillments, metafields, and bulk operati |
| `SHOPIFY_LIST_ARTICLE_AUTHORS` | Retrieve a list of all article authors from the store |
| `SHOPIFY_LIST_ARTICLE_TAGS` | Retrieve a list of all article tags from the store |
| `SHOPIFY_LIST_AVAILABLE_LOCALES` | Query available locales for the Shopify store using the Admin GraphQL API |
| `SHOPIFY_LIST_BLOG_ARTICLES` | Retrieves a list of all articles from a blog |
| `SHOPIFY_LIST_BLOGS` | Retrieve a list of all blogs from a Shopify store |
| `SHOPIFY_LIST_BULK_OPERATIONS` | Retrieve a paginated list of bulk operations from Shopify |
| `SHOPIFY_LIST_CHANNELS` | Retrieves a list of sales channels available in the Shopify store using GraphQL |
| `SHOPIFY_LIST_CHECKOUT_PROFILES` | Query checkout profiles from Shopify |
| `SHOPIFY_LIST_COLLECTION_PRODUCTS` | Retrieve a list of products belonging to a collection |
| `SHOPIFY_LIST_COMMENTS` | Retrieve a list of comments from Shopify |
| `SHOPIFY_LIST_CUSTOMERS` | Retrieve a list of customers from a Shopify store |
| `SHOPIFY_LIST_DRAFT_ORDERS` | Retrieve a list of draft orders from Shopify |
| `SHOPIFY_LIST_LOCATIONS` | Retrieve a list of locations for a Shopify store |
| `SHOPIFY_LIST_MARKETING_EVENTS` | Retrieves a paginated list of marketing events from a Shopify store |
| `SHOPIFY_LIST_PAGES` | Retrieve a list of all pages from a Shopify store |
| `SHOPIFY_LIST_PAYMENT_TERMS_TEMPLATES` | Query payment terms templates from Shopify using the GraphQL API |
| `SHOPIFY_LIST_PRODUCT_IMAGES` | Retrieve all images for a Shopify product |
| `SHOPIFY_LIST_PRODUCT_VARIANTS` | Retrieve all variants for a specified product |
| `SHOPIFY_LIST_RESOURCE_FEEDBACKS` | Retrieves the current resource feedback for the shop |
| `SHOPIFY_LIST_SCRIPT_TAGS` | Retrieves a list of all script tags |
| `SHOPIFY_LIST_TRANSACTIONS` | Retrieves all transactions for a specific order |
| `SHOPIFY_MARK_COMMENT_AS_NOT_SPAM` | Marks a comment as not spam in Shopify, restoring it to published or unapproved state |
| `SHOPIFY_MARK_COMMENT_AS_SPAM` | Mark a comment as spam in Shopify |
| `SHOPIFY_MODIFY_AN_EXISTING_PRODUCT_VARIANT` | Update an existing product variant in Shopify |
| `SHOPIFY_MOVE_FULFILLMENT_ORDER` | Move a fulfillment order from one merchant managed location to another |
| `SHOPIFY_PIN_METAFIELD_DEFINITION` | Pin a metafield definition in Shopify admin |
| `SHOPIFY_QUERY_APP_BY_KEY` | Query app information by API key using Shopify's GraphQL Admin API |
| `SHOPIFY_QUERY_BUSINESS_ENTITIES` | Retrieve all business entities associated with the shop |
| `SHOPIFY_QUERY_BUSINESS_ENTITY` | Query business entity information from Shopify |
| `SHOPIFY_QUERY_CATALOGS` | Queries catalogs from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_CHANNEL` | Query a single Shopify channel by ID |
| `SHOPIFY_QUERY_CONSENT_POLICY_REGIONS` | Query the list of countries and regions for which consent policies can be created in Shopify |
| `SHOPIFY_QUERY_CURRENT_APP_INSTALLATION` | Query the currently authenticated app installation on a Shopify store |
| `SHOPIFY_QUERY_CURRENT_BULK_OPERATION` | Query the current Shopify bulk operation status |
| `SHOPIFY_QUERY_CUSTOMER_ACCOUNT_PAGES` | Queries customer account pages from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_DELETION_EVENTS` | Query deletion events from Shopify |
| `SHOPIFY_QUERY_DISPUTES` | Query Shopify Payments disputes using the GraphQL Admin API |
| `SHOPIFY_QUERY_DOMAIN` | Query a specific domain by its ID from Shopify |
| `SHOPIFY_QUERY_EVENTS` | Query events from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_EVENTS_COUNT` | Query the count of events in Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_JOB` | Query a single job by its ID using Shopify's GraphQL API |
| `SHOPIFY_QUERY_METAFIELD_DEFINITION` | Query metafield definition details by ID using Shopify's GraphQL Admin API |
| `SHOPIFY_QUERY_METAFIELD_DEFINITIONS` | Query metafield definitions from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_METAFIELD_DEFINITION_TYPES` | Queries all available metafield definition types from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_NODE` | Query any Shopify resource by its global ID using the node query |
| `SHOPIFY_QUERY_NODES` | Query nodes by their IDs from the Shopify GraphQL Admin API |
| `SHOPIFY_QUERY_ONLINE_STORE` | Query online store settings from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_PRODUCT_DUPLICATE_JOB` | Query a product duplicate job by its ID using Shopify's GraphQL API |
| `SHOPIFY_QUERY_PUBLIC_API_VERSIONS` | Query available public API versions from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_PUBLICATION` | Query a single publication by ID using Shopify's GraphQL Admin API |
| `SHOPIFY_QUERY_SERVER_PIXEL` | Query the server pixel configuration in Shopify |
| `SHOPIFY_QUERY_SHOP` | Retrieve shop information using the Shopify GraphQL Admin API |
| `SHOPIFY_QUERY_SHOP_BILLING_PREFERENCES` | Query the shop's billing preferences from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_SHOPIFY_FUNCTIONS` | Query Shopify Functions owned by the API client installed on the shop |
| `SHOPIFY_QUERY_SHOP_PAY_PAYMENT_REQUEST_RECEIPTS` | Query Shop Pay payment request receipts from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_STANDARD_METAFIELD_DEFINITION_TEMPLATES` | Query standard metafield definition templates from Shopify using the GraphQL Admin API |
| `SHOPIFY_QUERY_TAXONOMY` | Query Shopify's product taxonomy using the GraphQL Admin API |
| `SHOPIFY_QUERY_WEBHOOK_SUBSCRIPTION` | Retrieve webhook subscription details by ID using the Shopify GraphQL Admin API |
| `SHOPIFY_QUERY_WEBHOOK_SUBSCRIPTIONS` | Query webhook subscriptions from Shopify using the GraphQL Admin API |
| `SHOPIFY_RECEIVE_A_SINGLE_FULFILLMENT` | Retrieve detailed information about a specific fulfillment for an order |
| `SHOPIFY_RELEASE_FULFILLMENT_HOLD` | Releases the fulfillment hold on a fulfillment order, allowing fulfillment work to proceed |
| `SHOPIFY_REOPEN_CLOSED_ORDER` | Reopens a previously closed Shopify order |
| `SHOPIFY_RESTORE_COMMENT` | Restores a previously removed comment, changing its status back to 'published' |
| `SHOPIFY_RETRIEVE_LIST_METAFIELDS_RESOURCE_S_ENDPOINT` | Retrieve metafields attached to any Shopify resource by using the resource's endpoint |
| `SHOPIFY_RETRIEVES_A_LIST_OF_PRICE_RULES` | Retrieve a list of price rules from a Shopify store |
| `SHOPIFY_RETRIEVE_SPECIFIC_FULFILLMENT_ORDER` | Retrieve a specific fulfillment order by its ID |
| `SHOPIFY_REVOKE_APP_ACCESS_SCOPES` | Revoke previously granted access scopes from an app installation |
| `SHOPIFY_RUN_BULK_MUTATION_OPERATION` | Create and run a bulk operation to import data asynchronously by executing a GraphQL mutation multiple times |
| `SHOPIFY_RUN_BULK_OPERATION_QUERY` | Create and start a Shopify GraphQL bulk operation for asynchronous data fetching |
| `SHOPIFY_SEARCHES_FOR_GIFT_CARDS` | Search for gift cards that match a supplied query |
| `SHOPIFY_SEND_CUSTOMER_INVITE` | Sends an account invitation email to a customer, allowing them to create or activate their Shopify account |
| `SHOPIFY_SEND_INVOICE` | Send an invoice email for a draft order to a customer |
| `SHOPIFY_SET_DEFAULT_CUSTOMER_ADDRESS` | Set a specific address as the default address for a customer |
| `SHOPIFY_SET_FULFILLMENT_ORDERS_DEADLINE` | Set the latest fulfillment deadline for multiple fulfillment orders |
| `SHOPIFY_SET_INVENTORY_LEVEL` | Set inventory level for an item at a location |
| `SHOPIFY_SET_METAFIELDS` | Create or update multiple metafields in a single operation using the metafieldsSet GraphQL mutation |
| `SHOPIFY_TRIGGER_SHOPIFY_FLOW` | Trigger Shopify Flow workflows that begin with the specified trigger handle |
| `SHOPIFY_UPDATE_APP_SUBSCRIPTION_LINE_ITEM` | Update the capped amount on usage-based billing for an app subscription line item |
| `SHOPIFY_UPDATE_ARTICLE` | Update an existing article in a Shopify blog |
| `SHOPIFY_UPDATE_BLOG` | Updates an existing blog's configuration in your Shopify store |
| `SHOPIFY_UPDATE_COMMENT` | Update an existing comment on a blog article in Shopify |
| `SHOPIFY_UPDATE_CUSTOM_COLLECTION` | Update an existing custom collection in Shopify |
| `SHOPIFY_UPDATE_CUSTOMER` | Update an existing customer in Shopify |
| `SHOPIFY_UPDATE_CUSTOMER_ADDRESS` | Updates an existing address for a Shopify customer |
| `SHOPIFY_UPDATE_CUSTOMERS_PARAM_CUSTOMER_ID_ADDRESSES_SET` | Performs bulk operations on multiple customer addresses |
| `SHOPIFY_UPDATE_DRAFT_ORDER` | Update an existing draft order in Shopify |
| `SHOPIFY_UPDATE_FULFILLMENT_TRACKING` | Updates tracking information (carrier company, tracking number, or custom URL) for an existing fulfillment |
| `SHOPIFY_UPDATE_GIFT_CARD` | Updates an existing gift card in Shopify |
| `SHOPIFY_UPDATE_INVENTORY_ITEM` | Updates properties of an inventory item in Shopify |
| `SHOPIFY_UPDATE_MARKETING_EVENT` | Updates an existing marketing event in Shopify |
| `SHOPIFY_UPDATE_METAFIELD_BY_ID` | Update an existing Shopify metafield by its ID |
| `SHOPIFY_UPDATE_METAFIELD_DEFINITION` | Update a Shopify metafield definition's configuration including name, description, validation rules, access settings, and capabilities |
| `SHOPIFY_UPDATE_ORDER` | Updates mutable fields on an existing Shopify order |
| `SHOPIFY_UPDATE_PAGE` | Updates an existing page in a Shopify store |
| `SHOPIFY_UPDATE_PRICE_RULE` | Update an existing price rule (discount) in Shopify |
| `SHOPIFY_UPDATE_PRODUCT_IMAGE` | Modify an existing product image |
| `SHOPIFY_UPDATE_PRODUCT_METAFIELD` | Updates an existing metafield for a specific Shopify product |
| `SHOPIFY_UPDATE_PRODUCT_VARIANTS_BULK` | Updates many product variants (20-50+) in one asynchronous Shopify bulk mutation job |
| `SHOPIFY_UPDATE_PUB_SUB_WEBHOOK_SUBSCRIPTION` | Updates a Google Cloud Pub/Sub webhook subscription configuration |
| `SHOPIFY_UPDATE_REDIRECT` | Update an existing Shopify redirect |
| `SHOPIFY_UPDATES_AN_EXISTING_DISCOUNT_CODE` | Updates the code value of an existing discount code associated with a price rule |
| `SHOPIFY_UPDATE_SCRIPT_TAG` | Modify an existing script tag in Shopify |
| `SHOPIFY_UPDATE_SMART_COLLECTION` | Update an existing smart collection |
| `SHOPIFY_UPDATE_SMART_COLLECTION_ORDER` | Updates the display order of products in a smart collection with manual sorting enabled |
| `SHOPIFY_UPDATE_THEME` | Update an existing theme's properties such as name or role |
| `SHOPIFY_UPDATE_WEBHOOK_SUBSCRIPTION` | Update a webhook subscription's configuration in Shopify |
