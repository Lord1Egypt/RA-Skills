# Smile.io use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/smile-io

## Identify High-Value Shopify Customers

Combine Shopify purchase history with Smile.io points balances and VIP membership to prioritize retention.

- Apps: Smile.io, Shopify
- Tools: `SMILE_FIND_CUSTOMER`, `SMILE_GET_PROGRAM`, `SMILE_LIST_ISSUED_REWARDS`

> Analyze my Shopify customers and orders alongside Smile.io loyalty customer records. Identify high-value customers using available purchase history, order frequency, total spend, loyalty points, and VIP tier information. Create a prioritized report containing the customer identifier and purchase metrics, points balance and membership state, current VIP tier and progress toward the next tier when available, redeemable rewards, and a suggested retention or loyalty action. Separate verified data from recommendations. Do not assume that a high points balance automatically means high customer lifetime value. Do not modify customer records, adjust points, or contact customers. Present the report for review first.

## Find Customers Ready To Return

Use Shopify order recency and Smile.io balances to identify lapsed customers worth a win-back.

- Apps: Smile.io, Shopify
- Tools: `SMILE_FIND_CUSTOMER`, `SMILE_POINTS_HISTORY`, `SMILE_LIST_REWARDS`

> Find Shopify customers who previously purchased repeatedly but have not ordered recently, using the date range I specify. Match them with Smile.io loyalty profiles using reliable customer identifiers, such as email where permitted. For each customer, report the last order date and previous order count, historical spend if available, current points balance, available rewards and redemption requirements, and a suggested win-back message angle. Rank customers using observable purchase recency and frequency. Do not claim a customer is likely to churn without sufficient evidence. Respect marketing consent and communication preferences. Draft suggested campaign segments and messages, but do not send marketing communications or adjust points without approval.

## Discover Unused Loyalty Reward Opportunities

Find customers with enough points to redeem a reward who haven't used them yet.

- Apps: Smile.io, Shopify
- Tools: `SMILE_LIST_REWARDS`, `SMILE_LIST_ISSUED_REWARDS`, `SMILE_FIND_CUSTOMER`

> Analyze Smile.io customer points balances, issued rewards, and available rewards alongside Shopify customer and order data. Identify customers who have sufficient points for one or more available rewards and whose recent activity suggests a relevant opportunity to encourage redemption. Include the purchase summary, current points balance, reward name and points required, apparent eligibility based on available data, relevant restrictions or missing information, and a suggested communication. Do not assume that every available reward is issued to the customer or that every reward is eligible for every order. Prepare a reward-education campaign proposal. Do not issue rewards, change balances, or send messages without my approval.

## Reward Customers For Shipping Delays

Match delayed Shopify orders to Smile.io profiles and prepare goodwill points adjustments for approval.

- Apps: Smile.io, Shopify
- Tools: `SMILE_FIND_CUSTOMER`, `SMILE_POINTS_HISTORY`, `SMILE_ADJUST_POINTS`

> Review Shopify orders for confirmed fulfillment or delivery delays within the period I specify. Match affected customers to Smile.io loyalty profiles. Use available order and shipment information to distinguish confirmed delays from unverified suspicions. Prepare a proposed goodwill points-adjustment report with the order reference and status, customer identifier, delay evidence, existing points balance, proposed compensation amount based on a policy I provide, and the reason. If no compensation policy is provided, ask me to define one instead of inventing point amounts. Do not adjust points automatically. Present the exact customer list and proposed adjustments for my approval before making any changes.

## Increase Sales Near VIP Milestones

Find customers approaching their next VIP tier and suggest relevant products without inventing requirements.

- Apps: Smile.io, Shopify
- Tools: `SMILE_GET_PROGRAM`, `SMILE_FIND_CUSTOMER`, `SMILE_POINTS_HISTORY`

> Review my Smile.io loyalty program configuration to understand its VIP tiers, qualifying milestones, and associated perks. Compare those requirements with Shopify customer purchase information and identify customers who are close to the next tier. For each customer, show the current tier, the next tier and its documented requirements, confirmed progress, relevant purchase history, the remaining qualifying amount or activity if calculable from the available rules, and relevant products to recommend. Do not assume all Shopify revenue counts toward VIP qualification. Account for only the qualification rules that are explicitly available. Prepare a campaign proposal that communicates genuine benefits without pressuring customers to spend unnecessarily. Do not change tiers, customer records, or send campaigns without approval.

## Investigate Loyalty Points Discrepancies

Compare Smile.io points history with Shopify orders and refunds to investigate unexpected balances.

- Apps: Smile.io, Shopify
- Tools: `SMILE_POINTS_HISTORY`, `SMILE_FIND_CUSTOMER`, `SMILE_GET_PROGRAM`, `SMILE_ADJUST_POINTS`

> Investigate a loyalty points discrepancy for the customer or customers I specify. Retrieve the Smile.io points history and compare available earn, spend, and manual adjustment transactions with relevant Shopify orders, refunds, and customer activity. Report the current points balance, relevant transactions and timestamps, matching order or refund references where available, possible missing, duplicated, or unexpected transactions, evidence supporting each suspected discrepancy, and a recommended next step. Do not assume that every Shopify order earns points or that every refund reverses points automatically. Use the loyalty program's available rules when accessible. Do not adjust points or claim a discrepancy is confirmed unless the evidence supports it. Ask for approval before making any manual adjustment.

## Create Smarter Loyalty Reward Offers

Align Smile.io rewards with Shopify catalog and purchase patterns for commercially sensible offers.

- Apps: Smile.io, Shopify
- Tools: `SMILE_LIST_REWARDS`, `SMILE_GET_PROGRAM`, `SMILE_LIST_ISSUED_REWARDS`

> Analyze the available Smile.io rewards and point costs alongside my Shopify product catalog and available sales information. Identify rewards that align with popular products, customer purchase patterns, and the goals I specify, such as repeat purchases or higher order frequency. For each potential offer, summarize the reward type and points required, relevant products or customer segments, available eligibility and redemption information, potential customer benefit, and business considerations plus the information needed to estimate profitability. Do not invent product margins, reward redemption rates, or incremental revenue. If the available data is insufficient to assess profitability, explain what is missing. Recommend which existing rewards to emphasize. Do not create or modify reward rules unless a connected capability explicitly supports it and I approve the change.

## Compare Loyalty Program Performance

Relate Smile.io points activity and VIP tiers to Shopify repeat-purchase and revenue metrics.

- Apps: Smile.io, Shopify
- Tools: `SMILE_POINTS_HISTORY`, `SMILE_GET_PROGRAM`, `SMILE_LIST_ISSUED_REWARDS`, `SMILE_FIND_CUSTOMER`

> Analyze Shopify order history and available customer purchase metrics alongside Smile.io points transactions, reward options, and VIP program configuration. Compare loyalty activity with purchase behavior for the date range I specify. Include repeat-purchase behavior among customers with loyalty profiles, orders and spend associated with matched records, points earned, redeemed, and manually adjusted where available, VIP tier distribution and progress, potential relationships between loyalty activity and repeat purchases, and data limitations plus recommended experiments. Clearly define the denominator and date range for each metric. Do not claim that the loyalty program caused a change in sales based only on correlation. Present the findings in an executive summary and recommend measurable tests for improving loyalty engagement.

## Find Customers With Expiring Rewards

Flag issued rewards with confirmed expiry so customers get a timely reminder.

- Apps: Smile.io, Shopify
- Tools: `SMILE_LIST_ISSUED_REWARDS`, `SMILE_FIND_CUSTOMER`, `SMILE_LIST_REWARDS`

> Review Smile.io issued rewards for customers matched to Shopify profiles. Identify rewards with a confirmed expiration date or other documented time-sensitive restriction. Compare those records with recent Shopify purchase activity to prioritize relevant opportunities. For each match, provide the customer identifier, issued reward and current status, confirmed expiration date or restriction if available, relevant purchase history, and a suggested reminder message. Do not assume that a reward expires unless its status or rules explicitly confirm that. Do not confuse an available reward with a reward already issued to a customer. Prepare a reminder campaign proposal and flag missing expiration information. Do not send messages or issue rewards without approval.

## Prepare Personalized Loyalty Campaigns

Build targeted loyalty segments from Shopify behavior and Smile.io data, with a Slack brief when connected.

- Apps: Smile.io, Shopify, Slack
- Tools: `SMILE_FIND_CUSTOMER`, `SMILE_GET_PROGRAM`, `SMILE_LIST_REWARDS`, `SMILE_LIST_ISSUED_REWARDS`

> Build a loyalty campaign plan using Shopify customer and order data alongside Smile.io points balances, transaction history, available rewards, and VIP tier information. Segment eligible customers into groups such as repeat purchasers with unused points, customers approaching a documented VIP milestone, previously active customers who have not purchased recently, and customers with available issued rewards. For each segment, provide its selection criteria, approximate audience size, supporting data, recommended offer, and a draft message. Do not assume that every customer can receive marketing communications. Respect consent and suppression requirements, and do not invent discounts or reward eligibility. If Slack is connected, prepare a campaign brief for the marketing channel. Ask for approval before posting the brief, adjusting points, or sending customer communications.
