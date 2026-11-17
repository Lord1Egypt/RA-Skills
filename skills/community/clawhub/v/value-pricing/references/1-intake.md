# Intake and study design

Discover the pricing decision and relevant business context before selecting a research method. Ask the minimum useful questions; let the user leave unknowns open.

## Discovery checklist

Establish as relevant:

- offering, buyer, user, problem or job;
- business model, revenue model, billing unit, period, and commercial terms;
- customer segments and geography;
- alternatives, including current practice and no purchase;
- value drivers and how outcomes are measured;
- delivery, fulfillment, labor, support, channel, and other cost drivers;
- current pricing and the exact decision to inform;
- available evidence, source, date, access permission, and gaps;
- constraints and acceptable risk.

Do not infer segment definitions, buyer shares, value units, costs, or current terms from a generic example. Use `null` or an explicit gap when unknown.

## Source material

The user may provide public URLs or files such as product information, service descriptions, contracts, price lists, operating data, customer research, or competitor materials. Confirm the relevant scope and permission before collecting or processing non-public information. Keep raw materials outside version control and minimize personal or commercially sensitive data.

The crawler, when applicable, is limited to public same-origin HTTP(S) content. It is optional; manual source review or supplied materials may be more suitable. Record URLs, access dates, and evidence excerpts. Do not assume an offering is discoverable from a website.

## Configure the offering and comparison vocabulary

Describe the complete offer at the level relevant to the decision: product, service, deliverables, access, quality, scope, terms, or other buyer-relevant dimensions. Attach sources to claims and distinguish verified, partial, unknown, and not applicable.

Use `taxonomy.yaml` only when consistent comparison is useful. Define custom attributes and categories. Do not force a feature list on an offer that is better described by outcomes, service scope, quality, capacity, delivery, or commercial terms.

## Define segments and scenarios only when needed

Choose segments, buyer archetypes, units of value, and scenario variables only if a selected method needs them. Define bounds and shares from supplied evidence or label them as assumptions with sensitivity ranges. Do not fill a template's blank fields with invented empirical values.

## Completion

Intake is ready for method selection when the decision, offer, relevant buyers, market context, evidence, constraints, and material gaps are recorded. If key context is missing, state what cannot yet be assessed and why.
