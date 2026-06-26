# CPQ Vertical Presets

Starting defaults for common CPQ verticals. The Builder Agent selects the closest preset based on the DOMAIN.md, then overrides with customer-specific data.

## How to Select a Preset

Read the DOMAIN.md and match against these signals:

| Signal in DOMAIN.md | Preset |
|---|---|
| Products are fabricated, assembled, or engineered-to-order | **Manufacturing / BOM** |
| Products are catalog items sold in bulk or by case/pallet | **Wholesale / Distribution** |
| Products are equipment bundled with installation, maintenance, or labor | **Services / Equipment Integrator** |
| None of the above clearly fit | **No preset** — use the mapping rules with no defaults |

## Manufacturing / BOM

Businesses that fabricate, assemble, or engineer products to order. Equipment manufacturers, custom fabricators, OEM suppliers.

### Default Product Structure
- Products are assemblies or parent items
- Accessories/parts are child items with compatibility constraints
- Options are engineering specs (size, capacity, material, voltage, finish)
- Some items are standard catalog, others are engineered-to-order

### Default Pricing
```json
{
  "quoteSettings": {
    "currency": "USD",
    "taxEnabled": false,
    "defaultTerms": "net30",
    "markup": 0.35,
    "quoteFormat": "itemized"
  }
}
```

### Typical Business Rules
- Equipment requires specific accessories (size/model matched)
- Certain options are incompatible (e.g., voltage vs control panel)
- Engineered items need vendor RFQ before quoting
- Non-standard terms require management approval
- Quotes include scope of work section

### Typical Roles
- Sales Engineer — creates and configures quotes
- Sales Manager / Director — approves terms, manages pipeline
- Purchasing — verifies vendor pricing
- Engineering — reviews custom configurations

---

## Wholesale / Distribution

Businesses that buy from manufacturers and sell to customers. Distributors, dealers, resellers, authorized dealers.

### Default Product Structure
- Products are catalog items with fixed SKUs
- Options are simple variants (size, color, packaging)
- Pricing comes from vendor price lists updated periodically
- Volume tiers and customer class pricing are common

### Default Pricing
```json
{
  "quoteSettings": {
    "currency": "USD",
    "taxEnabled": true,
    "taxLabel": "Sales Tax",
    "taxRate": 0.07,
    "defaultTerms": "net30",
    "markup": 0.40,
    "quoteFormat": "itemized"
  }
}
```

### Typical Business Rules
- Products may have minimum order quantities
- Volume pricing tiers apply at quantity thresholds
- Customer class (retail vs wholesale) affects pricing
- Backorder items flagged but still quotable
- Credit check required for new customers above threshold

### Typical Roles
- Sales Rep — creates quotes, manages accounts
- Sales Manager — approves discounts, manages pricing
- Warehouse — checks availability, manages stock

---

## Services / Equipment Integrator

Businesses that sell equipment bundled with installation, maintenance, and ongoing service. Water treatment companies, HVAC contractors, industrial equipment integrators.

### Default Product Structure
- Products are a mix of equipment and services
- Equipment has catalog pricing; services have labor rates
- PM (Preventive Maintenance) contracts are recurring revenue
- Accessories and consumables are tied to parent equipment
- Installation is typically bundled or quoted separately

### Default Pricing
```json
{
  "quoteSettings": {
    "currency": "USD",
    "taxEnabled": false,
    "defaultTerms": "net30",
    "availableTerms": ["net30", "net45", "milestone"],
    "markup": 0.375,
    "quoteFormat": "itemized"
  }
}
```

### Typical Business Rules
- Equipment requires installation service (liability-driven)
- Equipment requires specific accessories (functional dependency)
- Consumables recommended with PM contracts
- Non-standard terms require director approval
- PM renewals re-priced annually from current vendor lists
- Service agreements required before installation can be scheduled

### Typical Roles
- Sales Engineer — configures equipment + service packages
- Sales Director — approves terms, reports on pipeline
- PM Manager — manages renewals, reprices contracts
- Customer Service — processes POs, creates service agreements
- Purchasing — verifies vendor pricing, manages RFQs

---

## Using Presets

The Builder Agent:

1. Reads the DOMAIN.md
2. Identifies the closest preset
3. Starts with the preset's defaults for `quoteSettings` and typical rule patterns
4. Overrides with specifics from DOMAIN.md (exact products, exact prices, exact rules)
5. Notes the selected preset in `config.metadata.verticalPreset`

If the DOMAIN.md contradicts a preset default, the DOMAIN.md wins. Presets are starting points, not constraints.

If no preset fits, the Builder Agent uses the mapping rules with no defaults — every field comes directly from DOMAIN.md.

