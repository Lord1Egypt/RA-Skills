# Schema.org Product/Offer Reference

## Product
- `@type`: Product
- `name`: string
- `description`: string
- `image`: string|array
- `sku`: string
- `brand.name`: string
- `offers`: Offer|array
- `availability`: http://schema.org/InStock | OutOfStock | PreOrder | BackOrder | LimitedAvailability

## Offer
- `@type`: Offer
- `price`: number
- `priceCurrency`: string (USD, EUR)
- `availability`: as above
- `url`: string (product variant URL)
- `itemCondition`: NewCondition | UsedCondition | RefurbishedCondition
- `sku`: string
- `validFrom`: date

Shopify examples bind to Liquid: {{ product.price }}, {{ product.available ? 'InStock' : 'OutOfStock' }}.

See https://schema.org/Product
