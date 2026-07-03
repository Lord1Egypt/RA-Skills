---
name: stripe-direct-connection
description: "Stripe Direct Connection: Stripe payments, subscriptions, invoicing, refunds, disputes, and balance. Use when an agent needs stripe direct connection, launch saas subscription billing with recurring prices and hosted payment links, automate customer onboarding and crm to stripe sync, generate stripe checkout payment links for e commerce orders, run customer support refund workflows with reason tracking, cancel subscription, subscription, create coupon through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/stripe-direct-connection
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/stripe-direct-connection"}}
---
# Stripe Direct Connection

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Connect your AI agents to Stripe in seconds. The Stripe Direct Connection plugs straight into Stripe's official hosted MCP server, giving agents full read/write control over customers, products, prices, subscriptions, invoices, refunds, payment links, coupons, and disputes — no SDK install, no integration code, just one credential.

Use it to launch SaaS subscription billing with recurring monthly or annual prices, automate accounts receivable by issuing and finalizing invoices, generate hosted Stripe Checkout payment links for e-commerce orders, run customer-support refund flows with reason tracking, manage promotional coupon campaigns, and retrieve real-time account balances. The integration also supports Stripe's full query syntax for searching payment intents, charges, customers, and invoices, plus an interactive integration recommender that maps your business requirements to the right Stripe products (Checkout, Elements, Billing, Connect). Built for agentic workflows in SaaS billing, e-commerce, marketplace payments, donation processing, and finance automation.

## When To Use
- Use this skill for `Stripe Direct Connection` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: stripe direct connection, launch saas subscription billing with recurring prices and hosted payment links, automate customer onboarding and crm to stripe sync, generate stripe checkout payment links for e commerce orders, run customer support refund workflows with reason tracking, cancel subscription, subscription, create coupon.
- Supported action names: `cancel_subscription`, `create_coupon`, `create_customer`, `create_invoice`, `create_invoice_item`, `create_payment_link`, `create_price`, `create_product`, `create_refund`, `fetch_stripe_resources`, `finalize_invoice`, `get_stripe_account_info`, `list_coupons`, `list_customers`, `list_disputes`, `list_invoices`, `list_payment_intents`, `list_prices`, `list_products`, `list_subscriptions`, `retrieve_balance`, `search_stripe_documentation`, `search_stripe_resources`, `send_stripe_mcp_feedback`, `stripe_integration_recommender`, `update_dispute`, `update_subscription`.

## Use Cases
- Launch SaaS subscription billing with recurring prices and hosted payment links
- Automate customer onboarding and CRM-to-Stripe sync
- Generate Stripe Checkout payment links for e-commerce orders
- Run customer-support refund workflows with reason tracking
- Issue and finalize invoices for accounts receivable automation
- Resolve Stripe disputes and submit evidence to the bank
- Manage promotional coupons and discount campaigns
- Retrieve real-time Stripe account balances and payment intent history
- Search customers
- charges
- invoices
- and subscriptions with Stripe's query syntax
- Audit recent refunds and payment intents for finance reporting
- Plan new Stripe integrations with the interactive integration recommender
- Update or cancel subscriptions mid-cycle with proration control

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `27`.
x402 availability: not enabled for this product.

- `cancel_subscription` (action slug: `cancel-subscription`): This tool will cancel a subscription in Stripe. It takes the following arguments: - subscription (str, required): The ID of the subscription to cancel. Price: `5` credits. Parameters: `subscription`.
- `create_coupon` (action slug: `create-coupon`): This tool will create a coupon in Stripe. It takes several arguments: - name (str): The name of the coupon. Only use one of percent_off or amount_off, not both: - percent_off (number, optional): The percentage discount to apply (between 0 and 100). - amount_off (number, optional): The amount to subtract from an invoice (in currency minor units, e.g. cents for USD and yen for JPY). Optional arguments for duration. Use if specific duration is desired, otherwise default to 'once'. - duration (str, optional): How long the discount will last ('once', 'repeating', or 'forever'). Defaults to 'once'. - duration_in_months (number, optional): The number of months the discount will last if duration is repeating. Price: `5` credits. Parameters: `amount_off`, `currency`, `duration`, `duration_in_months`, `name`, `percent_off`.
- `create_customer` (action slug: `create-customer`): This tool will create a customer in Stripe. It takes two arguments: - name (str): The name of the customer. - email (str, optional): The email of the customer. Price: `5` credits. Parameters: `email`, `name`.
- `create_invoice` (action slug: `create-invoice`): This tool will create an invoice in Stripe. It takes two arguments: - customer (str): The ID of the customer to create the invoice for. - days_until_due (int, optional): The number of days until the invoice is due. Price: `5` credits. Parameters: `customer`, `days_until_due`.
- `create_invoice_item` (action slug: `create-invoice-item`): This tool will create an invoice item in Stripe. It takes three arguments: - customer (str): The ID of the customer to create the invoice item for. - price (str): The ID of the price to create the invoice item for. - invoice (str): The ID of the invoice to create the invoice item for. Price: `5` credits. Parameters: `customer`, `invoice`, `price`.
- `create_payment_link` (action slug: `create-payment-link`): This tool will create a payment link in Stripe. It takes two arguments: - price (str): The ID of the price to create the payment link for. - quantity (int): The quantity of the product to include in the payment link. Price: `5` credits. Parameters: `price`, `quantity`.
- `create_price` (action slug: `create-price`): This tool will create a price in Stripe. If a product has not already been specified, a product should be created first. It takes three arguments: - product (str): The ID of the product to create the price for. - unit_amount (int): The unit amount of the price in currency minor units, e.g. cents for USD and yen for JPY. - currency (str): The currency of the price. Price: `5` credits. Parameters: `currency`, `product`, `recurring`, `unit_amount`.
- `create_product` (action slug: `create-product`): This tool will create a product in Stripe. It takes two arguments: - name (str): The name of the product. - description (str, optional): The description of the product. Price: `5` credits. Parameters: `description`, `name`.
- `create_refund` (action slug: `create-refund`): This tool will refund a payment intent in Stripe. It takes three arguments: - payment_intent (str): The ID of the payment intent to refund. - amount (int, optional): The amount to refund in currency minor units, e.g. cents for USD and yen for JPY. - reason (str, optional): The reason for the refund. Options: "duplicate", "fraudulent", "requested_by_customer". Price: `5` credits. Parameters: `amount`, `payment_intent`, `reason`.
- `fetch_stripe_resources` (action slug: `fetch-stripe-resources`): Retrieve Stripe object details by ID. IMPORTANT: Only call this tool after search_stripe_resources is called to get specific object IDs. Do not use this tool to discover or search for objects. This tool fetches the object information from Stripe including all available fields. It is only able to fetch the following resources (prefixes): - Payment Intents (pi_) - Charges (ch_) - Invoices (in_) - Prices (price_) - Products (prod_) - Subscriptions (sub_) - Customers (cus_) It takes one argument: - id (str): The unique identifier for the Stripe object (e.g. cus_123, pi_123). Note that any amount returned is in currency minor units, e.g. cents for USD and yen for JPY. Price: `5` credits. Parameters: `id`.
- `finalize_invoice` (action slug: `finalize-invoice`): This tool will finalize an invoice in Stripe. It takes one argument: - invoice (str): The ID of the invoice to finalize. Price: `5` credits. Parameters: `invoice`.
- `get_stripe_account_info` (action slug: `get-stripe-account-info`): This will get the account info for the logged in Stripe account. Price: `5` credits. Parameters: none.
- `list_coupons` (action slug: `list-coupons`): This tool will fetch a list of Coupons from Stripe. It takes one optional argument: - limit (int, optional): The number of coupons to return. Price: `5` credits. Parameters: `limit`.
- `list_customers` (action slug: `list-customers`): This tool will fetch a list of Customers from Stripe. It takes two arguments: - limit (int, optional): The number of customers to return. - email (str, optional): A case-sensitive filter on the list based on the customer's email field. Price: `5` credits. Parameters: `email`, `limit`.
- `list_disputes` (action slug: `list-disputes`): This tool will fetch a list of disputes in Stripe. It takes the following arguments: - charge (string, optional): Only return disputes associated to the charge specified by this charge ID. - payment_intent (string, optional): Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID. Price: `5` credits. Parameters: `charge`, `limit`, `payment_intent`.
- `list_invoices` (action slug: `list-invoices`): This tool will fetch a list of Invoices from Stripe. It takes two arguments: - customer (str, optional): The ID of the customer to list invoices for. - limit (int, optional): The number of invoices to return. Price: `5` credits. Parameters: `customer`, `limit`.
- `list_payment_intents` (action slug: `list-payment-intents`): This tool will list payment intents in Stripe. It takes two arguments: - customer (str, optional): The ID of the customer to list payment intents for. - limit (int, optional): The number of payment intents to return. Note that the payment intent amount returned is in currency minor units, e.g. cents for USD and yen for JPY. Price: `5` credits. Parameters: `customer`, `limit`.
- `list_prices` (action slug: `list-prices`): This tool will fetch a list of Prices from Stripe. It takes two arguments. - product (str, optional): The ID of the product to list prices for. - limit (int, optional): The number of prices to return. Note that the price unit_amount returned is in currency minor units, e.g. cents for USD and yen for JPY. Price: `5` credits. Parameters: `limit`, `product`.
- `list_products` (action slug: `list-products`): This tool will fetch a list of Products from Stripe. It takes one optional argument: - limit (int, optional): The number of products to return. Price: `5` credits. Parameters: `limit`.
- `list_subscriptions` (action slug: `list-subscriptions`): This tool will list all subscriptions in Stripe. It takes four arguments: - customer (str, optional): The ID of the customer to list subscriptions for. - price (str, optional): The ID of the price to list subscriptions for. - status (str, optional): The status of the subscriptions to list. - limit (int, optional): The number of subscriptions to return. Price: `5` credits. Parameters: `customer`, `limit`, `price`, `status`.
- `retrieve_balance` (action slug: `retrieve-balance`): This tool will retrieve the balance from Stripe. It takes no input. Price: `5` credits. Parameters: none.
- `search_stripe_documentation` (action slug: `search-stripe-documentation`): Search the Stripe documentation for the given question and language. It takes two arguments: - question (str): The user question to search an answer for in the Stripe documentation. - language (str, optional): The programming language to search for in the the documentation. Price: `5` credits. Parameters: `language`, `question`, `search_only_api_ref`.
- `search_stripe_resources` (action slug: `search-stripe-resources`): This tool can be used to search for specific Stripe resources using a custom Stripe query syntax. It is only able to search for the following resources: customers, payment_intents, charges, invoices, prices, products, subscriptions. It returns a maximum of 100 results. IMPORTANT: For most use cases, prefer using the specific `list_` tools (e.g., `list_customers`, `list_payment_intents`) when you know the resource type you need. Only use this search tool when you need to: - Search across multiple resource types simultaneously - Search by field values that aren't supported by list tools - Use complex query syntax that isn't supported by list tools It takes one argument: - query (str): The query consisting of the Stripe resource to query for and the query clause in Stripe's custom query syntax to query metadata for. Note that any amount returned is in currency minor units, e.g. cents for USD and yen for JPY. Price: `5` credits. Parameters: `query`.
- `send_stripe_mcp_feedback` (action slug: `send-stripe-mcp-feedback`): Submit feedback from user or agent about Stripe's MCP server tools. Valid: "the search tool returned irrelevant results", "I wish there was a tool for X" Invalid: Stripe API complaints, AI model issues, IDE/environment problems - Only call when feedback clearly targets MCP tools. - If feedback is about one specific tool, include its name in tool_name. - If feedback is from user, quote their exact message and set source to "user". - If a tool didn't follow your expectations as an agent, set source to "agent". Price: `5` credits. Parameters: `context`, `quote`, `sentiment`, `source`, `tool_name`.
- `stripe_integration_recommender` (action slug: `stripe-integration-recommender`): Guides users through Stripe integration planning via interactive Q&A. Analyzes payment requirements and recommends the appropriate Stripe products (Checkout, Elements, Billing, Connect, etc.) with step-by-step implementation guidance. WHEN TO USE: Call this tool when the user expresses: - Payment keywords: "payments", "checkout", "billing", "subscriptions", "invoices" - Commercial intent: "sell", "monetize", "charge users", "e-commerce" - Stripe mention: User references "Stripe" directly IMPORTANT BEHAVIOR: - You may call this tool with partial information—the tool will ask clarifying questions. Do not wait until you have complete requirements. - Once a plan is in progress, stay in the Q&A flow until completion. If the user asks for clarification or advice (e.g., "what's best for me?"), answer them, then continue with the plan. Only exit early if the user explicitly requests it or the tool returns an unrecoverable error. - When the tool returns type="question", present the question to the user exactly as provided. PARAMETERS: - plan_id (optional): Required for continuing/updating. Omit when starting new plan. - answer (required): For new plans, provide summary. For existing plans, provide user response. Accepts option selections ('Option 1'), natural language, clarifying questions, or 'UNKNOWN'. - notes (optional): Technical context you've observed (e.g., "Python/Flask backend", "user wants minimal code to go live quickly", "already has Stripe SDK installed"). Returns JSON: - type="question": Plan in progress. Contains `question` to present to user and `plan_id` to include in next call. - type="summary": plan_id, status, summary (blueprints, prerequisites, sample_code) - type="error": status, error (code, message, user_visible, agent_guidance) WORKFLOW: - New plan: Call without plan_id + answer → Present question EXACTLY → Get answer → Call with plan_id + answer → Repeat - Continue plan: Present question EXACTLY → Analyze code → Formulate answer → Get approval → Call with plan_id + answer + notes → Repeat LIMITATIONS: - Generates integration guidance only; does not execute code or create Stripe resources. - Cannot modify completed or expired plans—start a new plan instead. Price: `5` credits. Parameters: `answer`, `notes`, `plan_id`.
- `update_dispute` (action slug: `update-dispute`): When you receive a dispute, contacting your customer is always the best first step. If that doesn't work, you can submit evidence to help resolve the dispute in your favor. This tool helps. It takes the following arguments: - dispute (string): The ID of the dispute to update - evidence (object, optional): Evidence to upload for the dispute. - cancellation_policy_disclosure (string) - cancellation_rebuttal (string) - duplicate_charge_explanation (string) - uncategorized_text (string, optional): Any additional evidence or statements. - submit (boolean, optional): Whether to immediately submit evidence to the bank. If false, evidence is staged on the dispute. Price: `5` credits. Parameters: `dispute`, `evidence`, `submit`.
- `update_subscription` (action slug: `update-subscription`): This tool will update an existing subscription in Stripe. If changing an existing subscription item, the existing subscription item has to be set to deleted and the new one has to be added. It takes the following arguments: - subscription (str, required): The ID of the subscription to update. - proration_behavior (str, optional): Determines how to handle prorations when the subscription items change. Options: 'create_prorations', 'none', 'always_invoice', 'none_implicit'. - items (array, optional): A list of subscription items to update, add, or remove. Each item can have the following properties: - id (str, optional): The ID of the subscription item to modify. - price (str, optional): The ID of the price to switch to. - quantity (int, optional): The quantity of the plan to subscribe to. - deleted (bool, optional): Whether to delete this item. Price: `5` credits. Parameters: `items`, `proration_behavior`, `subscription`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "stripe-direct-connection"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "stripe-direct-connection"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "stripe-direct-connection"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "stripe-direct-connection"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "stripe-direct-connection"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "stripe-direct-connection"
  }
}
```

## Call This Tool
Product slug: `stripe-direct-connection`

Marketplace page: https://www.agentpmt.com/marketplace/stripe-direct-connection

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Stripe-Direct-Connection",
    "arguments": {
      "action": "cancel_subscription",
      "subscription": "example subscription"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "stripe-direct-connection",
  "parameters": {
    "action": "cancel_subscription",
    "subscription": "example subscription"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `cancel_subscription` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/stripe-direct-connection
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
