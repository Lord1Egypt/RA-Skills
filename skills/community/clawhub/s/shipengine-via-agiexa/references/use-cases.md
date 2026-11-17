# ShipEngine use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/shipengine

## Track Shopify Orders And Deliveries

Connect Shopify order references with ShipEngine tracking details to identify delivery issues and answer customer inquiries.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_LIST_SHIPMENTS2`, `SHIPENGINE_GET_SHIPMENT_BY_EXTERNAL_ID`, `SHIPENGINE_GET_TRACKING_INFO`

> Review the ShipEngine shipments associated with my recent Shopify orders. List available Shopify order references, shipment IDs, carrier information, tracking numbers, tracking links, and latest tracking events. Identify shipments with recent movement, apparent delivery, or tracking activity that may require investigation. Do not assume a shipment is lost merely because tracking has not updated. Prepare a prioritized delivery report and draft customer-friendly updates using only verified tracking information. Do not send messages or change shipments automatically.

## Compare Shipping Rates Before Purchasing Labels

Compare available carrier rates for Shopify shipments to find suitable savings without compromising delivery expectations.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_GET_SHIPMENT_RATES`, `SHIPENGINE_GET_BULK_RATES`, `SHIPENGINE_GET_SHIPMENT_BY_ID`

> Identify Shopify-related shipments that I want to evaluate for shipping cost savings. Retrieve their ShipEngine shipment details and available rates. Compare carrier services, prices, estimated delivery times, and relevant service limitations where available. Calculate potential savings against the current rate only when both prices are known and comparable. Recommend the best option based on cost and delivery requirements, not price alone. Clearly distinguish live quotes from estimates. Do not purchase labels, cancel existing shipments, or change shipment details without my approval.

## Validate Customer Shipping Addresses

Identify potentially invalid or incomplete Shopify delivery addresses before shipping labels are purchased.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_VALIDATE_ADDRESS`, `SHIPENGINE_PARSE_ADDRESS`, `SHIPENGINE_UPDATE_SHIPMENT`

> Review the shipping addresses for the Shopify orders I specify. Use ShipEngine's address validation and parsing capabilities to identify missing fields, formatting issues, and addresses that require manual review. Show the original address, normalized result, validation findings, and associated Shopify order reference where available. Distinguish an address that needs review from one confirmed to be undeliverable. Do not overwrite customer addresses or change shipment details automatically. Prepare proposed corrections for my approval before any update is made.

## Investigate Delayed Or Missing Deliveries

Examine shipment tracking events and identify orders that may need carrier investigation or customer support follow-up.

- Apps: ShipEngine, Shopify, AfterShip
- Tools: `SHIPENGINE_GET_TRACKING_INFO`, `SHIPENGINE_GET_SHIPMENT_BY_ID`, `SHIPENGINE_LIST_SHIPMENTS2`

> Review tracking information for Shopify shipments that I specify or that have been flagged for investigation. Retrieve the latest ShipEngine tracking details and organize shipments by their actual reported tracking status and event history. Identify records with no recent progress, exception events, or other concerning information where supported by the returned data. Do not infer a delivery delay solely from missing updates, and do not promise a delivery date without reliable evidence. Prepare a report with Shopify order references, shipment IDs, carrier, tracking links, confirmed events, and recommended next steps.

## Prepare Shipping Labels In Controlled Batches

Organize eligible Shopify shipments into batches and review processing errors before label purchase.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_ADD_TO_BATCH`, `SHIPENGINE_PROCESS_BATCH_LABELS`, `SHIPENGINE_GET_BATCH_BY_ID`, `SHIPENGINE_GET_BATCH_ERRORS`

> Help me prepare a controlled shipping workflow for the Shopify orders selected for fulfillment. Review the corresponding ShipEngine shipments and identify any missing information or address concerns. Where supported, organize approved shipments or rate IDs into an existing batch. Before processing batch labels, show the shipment list, selected rates, estimated total cost, and unresolved issues. Ask for explicit approval before purchasing labels. After processing, retrieve batch details and errors where available, and report which shipments succeeded or failed. Never claim labels were purchased unless the operation result confirms it.

## Monitor Shipment Status With Webhooks

Configure and review shipping event subscriptions to support more responsive fulfillment monitoring.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_LIST_WEBHOOKS`, `SHIPENGINE_LIST_WEBHOOK_EVENTS`, `SHIPENGINE_CREATE_WEBHOOK`, `SHIPENGINE_START_TRACKING`

> Review my ShipEngine webhook configuration and available event types. Identify which events would be useful for monitoring Shopify-related shipment creation, tracking progress, delivery, and shipping exceptions, based on the event types actually available. Prepare a proposed webhook configuration with its purpose, callback URL, and relevant event selection. Ask for approval before creating, updating, or deleting any webhook. If testing is requested, explain that a simulated event may be sent to the configured external callback. Report the actual result and do not claim that Shopify has processed an event unless that is confirmed by available evidence.

## Manage Shipping Exceptions And Shipment Changes

Review shipment issues and prepare carefully scoped updates or cancellations when a Shopify order requires intervention.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_GET_SHIPMENT_BY_ID`, `SHIPENGINE_GET_TRACKING_INFO`, `SHIPENGINE_UPDATE_SHIPMENT`, `SHIPENGINE_CANCEL_SHIPMENT`

> Investigate the shipping issue associated with the Shopify order or ShipEngine shipment I specify. Retrieve the shipment details and relevant tracking information, then determine whether an address correction, shipment update, or cancellation is supported by the available data and actions. Explain the likely consequences and any information still needed. Show the exact shipment ID and proposed change before acting. Ask for explicit approval before updating or cancelling a shipment. After the operation, report the actual result and any limitations. Do not assume that a cancellation will reverse carrier charges or that a corrected shipment will automatically update the Shopify order.

## Optimize Packages And Warehouse Operations

Review package definitions and warehouse records to identify shipping configuration improvements for Shopify fulfillment.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_LIST_PACKAGES`, `SHIPENGINE_LIST_WAREHOUSES`, `SHIPENGINE_UPDATE_PACKAGE`, `SHIPENGINE_UPDATE_WAREHOUSE`

> Audit my ShipEngine package types and warehouse records for the Shopify fulfillment workflow. List existing packages, dimensions, identifiers, warehouse addresses, and other relevant details available from the account. Compare these settings with the shipment requirements I provide and identify missing, inconsistent, or potentially inefficient configurations. Recommend package definitions or warehouse updates only when supported by the available data. Do not assume a package is suitable based on dimensions alone or delete existing warehouse records automatically. Request approval before creating, updating, or deleting any configuration.

## Investigate Batch Processing And Label Errors

Review shipment batches and processing errors to identify orders blocked from label creation or fulfillment.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_LIST_BATCHES2`, `SHIPENGINE_GET_BATCH_BY_ID`, `SHIPENGINE_GET_BATCH_ERRORS`, `SHIPENGINE_GET_BATCH_BY_EXTERNAL_ID`

> Review my ShipEngine shipping batches and identify batches or shipments with processing errors. Retrieve batch details, external batch references, and available error information. Match affected shipments to Shopify order references where possible. Group issues by error type and severity, and recommend the next step for each case. Distinguish confirmed errors from suspected causes and do not retry or purchase labels automatically. Prepare an approval-ready recovery plan showing the relevant batch IDs, shipment IDs, estimated costs where available, and required corrections.

## Build A Daily Shopify Shipping Report

Consolidate shipment tracking, shipping costs, address issues, and fulfillment exceptions into one operational dashboard report.

- Apps: ShipEngine, Shopify
- Tools: `SHIPENGINE_LIST_SHIPMENTS2`, `SHIPENGINE_GET_TRACKING_INFO`, `SHIPENGINE_GET_SHIPMENT_RATES`, `SHIPENGINE_GET_BATCH_ERRORS`

> Prepare a daily shipping operations report for my Shopify store using available ShipEngine data. Summarize shipments, tracking activity, available shipping costs, address-validation concerns, batch processing errors, and shipments requiring investigation. Include Shopify order references wherever they are present in the shipment records. Identify potential shipping cost savings only when comparable rate information is available. Prioritize issues by customer impact and operational urgency, and provide clear next steps. Distinguish confirmed facts from estimates and recommendations. Do not purchase labels, cancel shipments, or modify shipping records without my explicit approval.
