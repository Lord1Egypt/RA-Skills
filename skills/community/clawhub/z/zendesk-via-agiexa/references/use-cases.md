# Zendesk use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/zendesk

## Investigate Customer Orders Faster

Match Zendesk tickets to Shopify orders so agents see the real context first.

- Apps: Zendesk, Shopify
- Tools: `ZENDESK_LIST_ZENDESK_TICKETS`, `ZENDESK_GET_ZENDESK_TICKET_BY_ID`, `ZENDESK_GET_TICKET_COMMENTS`, `ZENDESK_SEARCH_ZENDESK`

> Review my open Zendesk tickets related to Shopify orders. For each ticket, identify the customer and order using reliable identifiers, then retrieve the relevant Shopify order details where available. Include order status, fulfillment status, purchased products, and available tracking information. Summarize the issue, distinguish verified facts from customer claims, and draft an appropriate response. Do not expose another customer's data or promise a refund, replacement, or delivery date without supporting evidence.

## Find Recurring Shipping Complaints

Combine ticket trends with shipment data to surface fulfillment problems.

- Apps: Zendesk, Shopify, Shippo, ShipEngine
- Tools: `ZENDESK_SEARCH_ZENDESK`, `ZENDESK_LIST_ZENDESK_TICKETS`, `ZENDESK_GET_TICKET_COMMENTS`, `ZENDESK_GET_TICKET_METRICS`

> Analyze Zendesk tickets from the last 30 days that mention late, missing, or damaged deliveries. Match the relevant tickets to Shopify orders and available Shippo tracking information where possible. Group complaints by issue, shipment status, and available carrier information. Identify recurring patterns, quantify the affected tickets, and recommend operational improvements. Clearly distinguish carrier-confirmed delays from customer reports and do not assume that Shopify fulfillment means delivery was completed.

## Resolve Product Quality Issues

Correlate Zendesk complaints and Yotpo reviews against Shopify products.

- Apps: Zendesk, Shopify, Yotpo Reviews
- Tools: `ZENDESK_SEARCH_ZENDESK`, `ZENDESK_GET_TICKET_COMMENTS`, `ZENDESK_CREATE_SIDE_CONVERSATION`, `ZENDESK_REPLY_ZENDESK_TICKET`

> Analyze Zendesk tickets and Yotpo reviews related to products sold in my Shopify store. Identify recurring complaints about quality, durability, packaging, sizing, or product performance. Match feedback to the correct products when possible, count supporting records, and summarize representative concerns. Recommend which issues deserve investigation first and draft a response for affected customers. Do not treat an individual complaint as proof of a widespread defect, and do not publish replies or change review visibility without approval.

## Handle Subscription Support Requests

Investigate billing, cancellation, and recurring-order tickets with real subscription data.

- Apps: Zendesk, Shopify, Recharge, Seal Subscriptions
- Tools: `ZENDESK_SEARCH_ZENDESK`, `ZENDESK_GET_ZENDESK_TICKET_BY_ID`, `ZENDESK_GET_TICKET_COMMENTS`, `ZENDESK_SEARCH_ZENDESK_USERS`

> Find Zendesk tickets involving Shopify subscriptions, recurring orders, billing questions, or cancellation requests. Match each ticket to the relevant customer and subscription information from Shopify and connected subscription applications where available. Compare the customer's statement with the actual subscription status and relevant billing history. Summarize discrepancies and draft a response grounded in verified information. Do not cancel subscriptions, change billing schedules, or promise refunds unless an authorized integration supports the action and I explicitly approve it.

## Improve Customer Satisfaction Scores

Use satisfaction ratings and ticket history to understand dissatisfaction causes.

- Apps: Zendesk, Shopify
- Tools: `ZENDESK_GET_SATISFACTION_RATINGS`, `ZENDESK_GET_TICKET_METRICS`, `ZENDESK_LIST_ZENDESK_TICKETS`, `ZENDESK_GET_SATISFACTION_RATINGS_COUNT`

> Analyze Zendesk customer satisfaction ratings and associated ticket histories for the last 30 days. Group dissatisfied responses by issue type and connect them to Shopify orders, product details, or shipping information where available. Identify recurring causes of dissatisfaction, compare them with ticket volume and resolution metrics, and recommend the highest-impact improvements. Separate correlations from proven causes and avoid exposing unnecessary customer information.

## Draft Accurate Support Responses

Personalized replies built on verified Shopify and connected-app data.

- Apps: Zendesk, Shopify
- Tools: `ZENDESK_GET_ZENDESK_TICKET_BY_ID`, `ZENDESK_GET_TICKET_COMMENTS`, `ZENDESK_APPLY_ZENDESK_MACRO`, `ZENDESK_REPLY_ZENDESK_TICKET`

> Review selected Zendesk tickets and gather relevant information from Shopify and connected integrations where available. Draft concise, empathetic responses that directly address the customer's issue. Use verified order, product, fulfillment, subscription, or review information as appropriate. Clearly identify missing information and avoid unsupported promises about refunds, delivery dates, replacements, or policy exceptions. Show me the final response before posting it publicly to the customer.

## Escalate High-Impact Problems

Group related tickets into structured escalations for the right team.

- Apps: Zendesk, Shopify, Slack
- Tools: `ZENDESK_LIST_ZENDESK_TICKETS`, `ZENDESK_GET_PROBLEMS`, `ZENDESK_CREATE_ZENDESK_TICKET`, `ZENDESK_MERGE_ZENDESK_TICKETS`

> Review open Zendesk tickets and identify issues that may require escalation, such as repeated delivery failures, recurring product defects, disputed subscription charges, or multiple complaints about the same Shopify product. Group related tickets when reliable evidence supports the connection. Prepare an escalation summary with ticket references, affected products or orders, evidence, customer impact, and recommended next steps. Create a new ticket or update an existing one only after showing me the proposed changes for approval.

## Improve Help Center Coverage

Turn repeated ticket questions into proposed help-center articles.

- Apps: Zendesk, Shopify
- Tools: `ZENDESK_LIST_ZENDESK_TICKETS`, `ZENDESK_SEARCH_HELP_CENTER_ARTICLES`, `ZENDESK_LIST_HELP_CENTER_CONTENT`, `ZENDESK_GET_TICKET_COMMENTS`

> Analyze recurring questions in Zendesk tickets and search the available Zendesk Help Center content for relevant existing articles. Compare common customer questions with Shopify product information and published store policies where accessible. Identify missing or unclear guidance and recommend new articles or improvements. Draft article outlines and answers using verified information, clearly flagging anything that needs confirmation. Do not publish policy changes or promise capabilities that the store does not support.

## Automate Ticket Organization Safely

Improve categorization with tags, macros, and views - previewed before any change.

- Apps: Zendesk, Shopify
- Tools: `ZENDESK_GET_MACROS`, `ZENDESK_GET_VIEWS`, `ZENDESK_CREATE_VIEWS_PREVIEW`, `ZENDESK_UPDATE_TICKETS_TAGS`

> Analyze Zendesk tickets related to Shopify orders and identify opportunities to improve ticket categorization. Recommend consistent tags and groupings for shipping issues, product questions, returns, subscription questions, and payment concerns. Review existing macros and views before proposing changes. Show examples of tickets that would match each proposed rule and preview the expected effects where supported. Do not create, modify, or delete production workflows until I approve the exact changes.

## Prepare a Daily Support Briefing

A daily report on ticket load, recurring issues, and connected Shopify context.

- Apps: Zendesk, Shopify, Slack
- Tools: `ZENDESK_LIST_ZENDESK_TICKETS`, `ZENDESK_GET_TICKETS_COUNT`, `ZENDESK_GET_TICKET_METRICS`, `ZENDESK_GET_SATISFACTION_RATINGS`, `ZENDESK_GET_INCREMENTAL_TICKETS`

> Prepare a daily support briefing using available Zendesk tickets, comments, ticket metrics, and satisfaction ratings. Include open and recently created tickets, recurring customer complaints, unresolved high-impact issues, and relevant resolution metrics. Match tickets with Shopify orders, available shipping data, Yotpo reviews, or subscription information when the relevant integrations are connected and records can be matched. Highlight the three most important actions for today, explain the evidence, and identify any missing data. Do not claim an issue has been resolved until its status confirms it.
