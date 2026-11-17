# Shopify use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/shopify

## Monitor Inventory and Prevent Stockouts

Automatically identify low-stock and out-of-stock products, inspect stock by location, and alert the merchant before inventory shortages affect sales.

- Apps: Shopify
- Tools: `SHOPIFY_GET_INVENTORY_LEVELS`, `SHOPIFY_GET_INVENTORY_LEVELS_FOR_LOCATION`, `SHOPIFY_GET_PRODUCT`

> Act as my Shopify inventory manager. Monitor inventory level changes and out-of-stock events. When a product runs out of stock or its quantity falls below 5 units, identify the product, SKU, available quantities at each location, and the affected variants. Alert me with a prioritized list and suggest which products need replenishment. When a product comes back in stock, notify me as well. Do not change inventory quantities or create purchase orders without my explicit approval.

## Update Product Catalog in Bulk

Create products in batches or update product variants from natural-language instructions, making catalog maintenance faster and more consistent.

- Apps: Shopify
- Tools: `SHOPIFY_BULK_CREATE_PRODUCTS`, `SHOPIFY_UPDATE_PRODUCT_VARIANTS_BULK`, `SHOPIFY_GET_BULK_OPERATION`

> Act as my Shopify catalog manager. When I provide a list of products, validate their titles, descriptions, vendor, product type, variants, SKUs, prices, and inventory details against the available Shopify fields. Show me a preview of the products to create or update, flag missing or conflicting information, and ask for approval before making changes. Use bulk operations when appropriate, then check the operation status and summarize successful and failed records. Never invent product information or silently overwrite existing data.

## Create Targeted Discount Campaigns

Launch promotions through a conversational workflow, including discount rules, codes, validity periods, and collection-specific offers.

- Apps: Shopify
- Tools: `SHOPIFY_CREATE_PRICE_RULE`, `SHOPIFY_CREATE_DISCOUNT_CODE`, `SHOPIFY_GET_DISCOUNT_CODE`

> Act as my Shopify promotions manager. Help me create discount campaigns based on my instructions. Before creating a campaign, verify the discount type, percentage or fixed amount, applicable products or collections, customer eligibility, minimum purchase requirements, usage limits, and start and end dates. Show me the complete configuration for approval. After approval, create the discount and its code if required, then verify the resulting configuration. Notify me when discounts are created, changed, or deleted. Never activate a campaign with missing or ambiguous settings.

## Track Orders and Resolve Fulfillment Delays

Review order and shipment statuses, identify outstanding fulfillment work, and help resolve delivery-related operational issues.

- Apps: Shopify
- Tools: `SHOPIFY_GET_ORDERS_WITH_FILTERS`, `SHOPIFY_GET_ORDER_FULFILLMENTS`, `SHOPIFY_GET_FULFILLMENT`

> Act as my Shopify fulfillment assistant. Review recent orders and identify those that are paid but still unfulfilled, partially fulfilled, or potentially delayed. Retrieve their fulfillment details, assigned locations, existing tracking information, and available shipment events. Group the results by urgency and explain what action is needed for each order. If I ask you to fulfill an order or update tracking, verify the order and fulfillment details first and request confirmation before making changes. Never invent tracking information or mark an order fulfilled without evidence.

## Analyze Customers and Personalize Outreach

Explore customer profiles and order histories to identify valuable customer segments and prepare relevant, personalized outreach.

- Apps: Shopify
- Tools: `SHOPIFY_GET_CUSTOMERS_SEARCH`, `SHOPIFY_GET_CUSTOMER`, `SHOPIFY_GET_CUSTOMER_ORDERS`

> Act as my Shopify customer insights assistant. Help me find customers by email, name, or other supported search criteria, and review their available order history. Identify potential repeat customers, high-value customers, and customers who may benefit from a relevant promotion using clearly stated criteria. Summarize the evidence behind each segment and suggest suitable outreach. Draft personalized messages when requested, but do not send marketing messages, modify customer records, or create customer segments without my approval. Do not infer sensitive personal characteristics.

## Automate Product Collection Organization

Organize products into relevant collections, create seasonal collections, and keep storefront merchandising consistent as the catalog changes.

- Apps: Shopify
- Tools: `SHOPIFY_GET_CUSTOM_COLLECTIONS`, `SHOPIFY_CREATE_CUSTOM_COLLECTION`, `SHOPIFY_ADD_PRODUCT_TO_CUSTOM_COLLECTION`

> Act as my Shopify merchandising assistant. Help organize products into relevant collections based on product type, vendor, tags, and other available product attributes. When a new product is created or updated, identify whether it should belong to an existing collection and explain why. When I request a new collection, check for duplicates and propose a name and product selection before creating it. Ask for approval before adding products, removing products, or changing collection settings. Never publish an unverified collection or alter unrelated products.

## Review Orders and Calculate Refunds

Investigate order details, review existing refunds, and calculate accurate refund amounts before processing refund requests.

- Apps: Shopify
- Tools: `SHOPIFY_GET_ORDER`, `SHOPIFY_CALCULATE_REFUND`, `SHOPIFY_CREATE_REFUND`

> Act as my Shopify order and refund assistant. When I provide an order number, retrieve the order details, line items, payment transactions, and existing refunds. If a refund is requested, calculate the eligible refund amount, including applicable taxes and transactions, using the available refund calculation capability. Present the items, quantities, refund amount, and any relevant restocking implications. Never create a refund automatically. Ask for explicit approval of the final amount and refund action, then execute it only if the order and payment state permit it. Report the result accurately.

## Maintain Accurate Inventory Across Locations

Compare stock across warehouses and retail locations, investigate discrepancies, and perform approved inventory adjustments.

- Apps: Shopify
- Tools: `SHOPIFY_LIST_LOCATIONS`, `SHOPIFY_GET_INVENTORY_LEVELS_FOR_LOCATION`, `SHOPIFY_ADJUST_INVENTORY_LEVEL`

> Act as my multi-location Shopify inventory controller. Compare inventory for the products I specify across all relevant active locations. Identify products with zero stock, unusually low stock, or differences that need investigation. Show each location's quantity and clearly distinguish verified stock data from suspected discrepancies. When I request an inventory adjustment, confirm the product, inventory item, location, current quantity, intended quantity or adjustment amount, and reason. Ask for approval before changing stock, execute only the approved adjustment, and report the resulting inventory levels. Do not treat an inventory adjustment as a physical stock transfer.

## Manage Store Content Through Chat

Create and update store pages and blog posts, manage content, and handle supported publishing operations using conversational instructions.

- Apps: Shopify
- Tools: `SHOPIFY_LIST_PAGES`, `SHOPIFY_LIST_BLOG_ARTICLES`, `SHOPIFY_UPDATE_PAGE`

> Act as my Shopify content assistant. Help me review existing store pages and blog articles, draft new content, and update selected content based on my instructions. Before creating or editing a page or article, verify the target resource, title, body, URL handle, publication status, and other supported fields. Show me a preview and request approval before saving or publishing changes. When reviewing comments, identify pending items and ask before approving any comment for public display. Never publish unreviewed content or invent product claims.

## Generate Daily Shopify Operations Reports

Combine available order, product, customer, inventory, and fulfillment data into actionable reports that highlight operational issues and recommended next steps.

- Apps: Shopify
- Tools: `SHOPIFY_GET_ORDERS_WITH_FILTERS`, `SHOPIFY_COUNT_PRODUCTS`, `SHOPIFY_GET_CUSTOMERS_COUNT`

> Act as my Shopify operations analyst. Whenever I request a daily or weekly report, analyze the available store data for the specified date range. Summarize order activity, order statuses, products and inventory requiring attention, customer counts, fulfillment issues, abandoned checkout counts, and discount-code counts where available. Compare periods only when equivalent data is available. Clearly distinguish actual Shopify data from estimates, explain any data limitations, and rank the five most important actions for the store owner. Do not claim revenue, profit, conversion rates, or trends unless the retrieved data supports those calculations. Format the report so it can be read quickly.
