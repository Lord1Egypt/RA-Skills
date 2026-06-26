# Offer Check Template

## Query patterns

For each product:

1. `<product name> offer <location> supermarket`
2. `<product name> <chain> offer <location>` (for each preferred chain)
3. `<alias> offer <location>` (for aliases)

## Validation rules

Count a hit as valid when at least 2 points are clear:
- Product name or alias is explicit
- Store/chain is explicit
- Date range is currently valid
- Price or discount is shown

## Output format

- ✅ **<Product>** at **<Store>**: <Price/Discount>, valid until <Date>  
  Source: <URL>

If no valid hit:
- "No reliable nearby offers found today."
