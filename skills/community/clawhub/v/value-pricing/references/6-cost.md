# Delivery economics and cost-to-serve

Use this phase when delivery economics constrain pricing, packaging, scope, or channel decisions. Cost analysis informs feasibility; it does not by itself determine what buyers will pay.

## Gather relevant inputs

Identify costs tied to the selected offer and billing basis. Depending on the business, these may include materials, labor, production, inventory, fulfillment, returns, hosting, data or usage, onboarding, support, account management, payment processing, channel fees, sales, and fixed capacity. Do not ask for irrelevant categories.

For each amount or driver, record currency, period, unit, source, date, allocation method, and confidence. Separate measured values, estimates, and gaps. Read supplied records only with the user's authorization and keep raw materials out of version control.

Where transaction or operational data can support it, estimate cost drivers from observed activity. Do not make an allocation look measured when it is a convention. Include labor and support where material, and test ranges when the data are incomplete.

## Model and interpret

Configure `costs.yaml` for the selected model. Convert units and periods explicitly. Compute contribution or margin only where the revenue basis and cost coverage are compatible. Show the effect of uncertain costs, capacity, utilization, channel terms, and volume assumptions where relevant.

The included `cost_model.py` expects a specific structured schema and is optional. Do not run it until the inputs required by that schema are configured. For other cost structures, use a transparent calculation suited to the business.

## Report

State cost coverage, allocation rules, assumptions, ranges, and gaps. Explain which costs are incremental, fixed, or shared and how that affects interpretation. Do not turn a cost floor into a customer value claim.
