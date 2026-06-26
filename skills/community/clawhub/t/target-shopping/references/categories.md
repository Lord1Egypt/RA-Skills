# Common Target category N-IDs

Target's category pages live at `https://www.target.com/c/<slug>/-/N-<id>`.
The `N-<id>` is what `plp_search_v2` accepts as its `category` param.

Combine a category with a narrow keyword to scope a search — useful when
generic catalog-wide keyword search drowns fresh-grocery hits in
shelf-stable matches (e.g. searching "chicken breast" returns canned
chicken first; scoping to Fresh Chicken returns raw breasts).

Pattern:

```bash
uv run python -m scripts.search "chicken breast" --category 4tgi7
```

All IDs below were verified against the public category pages on
2026-05-17. They occasionally rotate — if a category returns 0 results,
re-derive by visiting `target.com/c/<slug>` and reading the `N-` from the
URL.

## Grocery

| Section | N-ID |
| --- | --- |
| Grocery (root) | `5xt1a` |
| Grocery Deals | `k4uyq` |

### Fresh

| Sub-category | N-ID |
| --- | --- |
| Fresh Meat & Seafood | `5xsyh` |
| └ Fresh Chicken | `4tgi7` |
| └ Fresh Beef | `4tgi8` |
| └ Fresh Pork | `4tgi2` |
| └ Fresh Turkey | `4tghz` |
| └ Fresh Fish & Shellfish | `4tgi0` |
| └ Bacon, Hot Dogs & Sausage | `crmcy` |
| └ Ham | `f2cgx` |
| └ Plant-Based Meat Alternatives | `4tgi3` |
| Produce | `u7fty` |
| └ Fresh Fruit | `4tglt` |
| └ Fresh Vegetables | `4tglh` |
| └ Organic Produce | `h6rph` |
| └ Packaged & Prepared Produce | `yvtbp` |
| Dairy, Eggs & Cheese | `5xszm` |
| Deli | `5hp74` |
| Bakery & Bread | `5xt19` |

### Shelf-stable

| Sub-category | N-ID |
| --- | --- |
| Pantry | `5xt13` |
| └ Cooking Oil | `4u9ly` |
| └ Herbs, Spices & Seasonings | `5xszu` |
| └ Sauces, Gravies & Marinades | `4tg6h` |
| └ Condiments | `5xszw` |
| └ Rice, Grains & Dried Beans | `5xsyc` |
| └ Canned & Packaged Goods | `5xt05` |
| └ Pasta | `h92hn` |
| └ Pasta & Pizza Sauces | `uttuw` |
| └ Baking Ingredients | `4u9lv` |
| └ Soup | `5xszx` |
| └ Spreads, Jams & Nut Butters | `5xszr` |
| └ Sugar & Sweeteners | `5xt0u` |
| Breakfast & Cereal | `wo2mp` |
| Snacks | `5xsy9` |
| Beverages | `5xt0r` |
| └ Coffee | `4yi5p` |
| └ Wine, Beer & Liquor | `5n5q6` |
| Frozen Foods | `5xszd` |
| International Foods | `j06h7` |
| Candy | `5xt0d` |

## When keyword search isn't enough

If a fresh-grocery keyword search returns canned/shelf-stable items at the
top, **combine the keyword with the matching fresh sub-category N-ID**.
Examples:

```bash
# Returns raw chicken breasts, not canned chicken:
uv run python -m scripts.search "chicken breast" --category 4tgi7

# Lemons that are actually fruit, not cleaning wipes:
uv run python -m scripts.search "lemon" --category 4tglt

# Garlic powder from Herbs & Spices, skipping all the garlic-adjacent
# household products:
uv run python -m scripts.search "garlic powder" --category 5xszu
```

## Caveats

- Some fresh items (deli, hot bar, fresh-baked) are **store-pickup only**
  in some markets — the catalog will show them but `fulfillment` will
  report no shipping. Verify with `scripts.fulfillment <tcin> --zip <z>`.
- Not all stores carry the full fresh assortment. Pass `--store-id` so
  prices and availability match what the user can actually pick up.
- These N-IDs cover the most common cooking/meal-prep needs. For other
  departments (toys, apparel, electronics), derive by visiting
  `target.com/c/<department>` and copying the `N-<id>` from the URL.
