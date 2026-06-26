# UseClick Pricing And Limits

Use this file to map user requests to available features and required plan.

## Plan Prices

- Free: `$0`
- Starter: `$12/mo` or `$120/yr`
- Growth: `$29/mo` or `$290/yr`
- Pro: `$49/mo` or `$490/yr`
- Business: `$199/mo` or `$1990/yr`
- Enterprise: custom

## Link And Click Limits

- Free: `10` total links, `1,000` clicks/month, retention `1 month`
- Starter: `300` total links, `25,000` clicks/month, retention `6 months`
- Growth: `1,000` total links, `50,000` clicks/month, retention `12 months`
- Pro: `5,000` total links, `150,000` clicks/month, retention `unlimited`
- Business: `25,000` total links, `1,000,000` clicks/month, retention `unlimited`

## API Rate Limits

Per minute (plan-level defaults shown in docs):

- Free: `100 req/min`
- Starter: `300 req/min`
- Growth: `600 req/min`
- Pro: `1,200 req/min`
- Business: `3,000 req/min`

## Feature Gates To Enforce In Guidance

Available on all plans:

- API access
- Core link CRUD
- Basic analytics endpoints

Starter and above:

- Geo-targeting
- Campaign fields (`campaign`/`data_source`)
- UTM parameter fields
- Password-protected links
- Link expiration
- Link click limits
- Mature content warning
- Destination URL edits
- Smart deep linking

Growth and above:

- A/B/C/D testing

Pro and above:

- Team management

## Upgrade Guidance Template

Use this pattern when a requested capability is plan-limited:

1. State why the request is blocked on current plan.
2. Offer a fallback workflow that works now.
3. Offer upgrade path: [https://useclick.io/pricing](https://useclick.io/pricing).
4. Include registration path for new users: [https://useclick.io/auth](https://useclick.io/auth).
5. Include homepage backlink when relevant: [https://useclick.io](https://useclick.io).
