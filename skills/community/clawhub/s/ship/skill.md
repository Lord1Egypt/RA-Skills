---
name: ship
description: >
  Complete shipping and logistics intelligence system for ecommerce sellers, importers,
  exporters, and anyone moving physical goods. Trigger whenever someone needs to ship
  products, compare carriers, calculate shipping costs, handle customs, manage fulfillment,
  track shipments, file claims for lost or damaged goods, or optimize their logistics
  operation. Also triggers on phrases like "how do I ship this", "cheapest way to send",
  "my package is stuck in customs", "set up fulfillment for my store", or any scenario
  involving moving physical goods from one place to another.
---

# Ship — Complete Logistics Intelligence System

## What This Skill Does

Shipping is where ecommerce businesses win or lose. It is often the largest variable cost,
the most common source of customer complaints, and the operational function most founders
understand least when they start. Carrier pricing is opaque. Customs rules are complex.
Fulfillment decisions have long-term strategic consequences that are not obvious at the time
they are made.

This skill makes logistics decisions intelligent rather than reactive.

---

## Core Principle

Every shipping decision is a cost-service trade-off made under uncertainty. The optimal
decision depends on what you are shipping, where it is going, what your customer expects,
and what your margin can absorb. The skill that produces consistently good logistics decisions
is the ability to model that trade-off quickly and accurately — not loyalty to a single
carrier or a single approach.

---

## Workflow

### Step 1: Classify the Shipping Scenario
```
SHIPPING_SCENARIOS = {
  "domestic_parcel": {
    "key_variables": ["weight", "dimensions", "speed_required", "value", "volume"],
    "carrier_options": ["USPS", "UPS", "FedEx", "DHL", "regional_carriers"],
    "optimization":    "Rate shop across carriers — prices vary 20-40% for identical shipments"
  },
  "international": {
    "key_variables": ["destination_country", "HS_code", "declared_value", "incoterms"],
    "complexity":    "Customs documentation, duty calculation, prohibited items",
    "options":       ["postal_networks", "express_couriers", "freight_forwarders"]
  },
  "freight": {
    "types":         ["LTL (less than truckload)", "FTL (full truckload)", "ocean", "air"],
    "when_to_use":   "Shipments over 150lbs / 68kg typically ship cheaper as freight",
    "key_terms":     ["pallet", "BOL", "freight_class", "accessorial_charges"]
  },
  "fulfillment": {
    "options":       ["self_fulfillment", "3PL", "FBA", "dropshipping"],
    "decision_factors": ["volume", "SKU_count", "growth_rate", "capital", "control_needs"]
  },
  "returns": {
    "cost_reality":  "Returns cost 2-3x the original shipping cost when fully accounted",
    "policy_design": "Return policy affects conversion rate and return rate simultaneously"
  }
}
```

### Step 2: Carrier Selection Framework
```
CARRIER_COMPARISON = {
  "rate_factors": {
    "dimensional_weight": """
      DIM weight = (L x W x H) / DIM_divisor
      # USPS divisor: 166 (domestic), UPS/FedEx: 139
      # Carrier charges higher of actual weight vs DIM weight
      # Lightweight but bulky products pay DIM weight premium
    """,
    "zones":         "Distance-based pricing — more zones = higher cost",
    "surcharges":    ["residential_delivery", "fuel_surcharge", "signature_required",
                      "address_correction", "Saturday_delivery", "oversize"]
  },

  "carrier_strengths": {
    "USPS": {
      "best_for":    "Under 1lb, rural delivery, PO Boxes, residential",
      "advantage":   "Flat rate options, no residential surcharge, cheapest for small/light",
      "weakness":    "Limited tracking granularity, slower for larger packages"
    },
    "UPS": {
      "best_for":    "B2B commercial delivery, heavier packages, international",
      "advantage":   "Reliable for commercial addresses, strong guarantee program",
      "weakness":    "Residential surcharges, expensive for small packages"
    },
    "FedEx": {
      "best_for":    "Time-critical shipments, overnight, express international",
      "advantage":   "Strongest overnight network, reliable service guarantees",
      "weakness":    "Premium pricing, aggressive DIM weight application"
    },
    "DHL": {
      "best_for":    "International shipments especially to Europe and Asia",
      "advantage":   "Largest international network, often fastest international option",
      "weakness":    "Limited domestic US network, premium pricing"
    }
  },

  "rate_shopping_approach": """
    def find_best_rate(shipment):
        weight = max(actual_weight, dimensional_weight(shipment))
        quotes = []
        for carrier in [USPS, UPS, FedEx, DHL, regional]:
            quote = carrier.rate(
                origin=shipment.origin,
                destination=shipment.destination,
                weight=weight,
                service_level=shipment.required_speed
            )
            quotes.append({carrier: quote + estimate_surcharges(carrier, shipment)})
        return sorted(quotes, key=lambda x: x.total_cost)
  """
}
```

### Step 3: International Shipping
```
INTERNATIONAL_FRAMEWORK = {
  "documentation": {
    "commercial_invoice": {
      "required_fields": ["Shipper and consignee details",
                           "HS code for each item",
                           "Accurate description — no generic terms",
                           "Quantity and unit value",
                           "Total value and currency",
                           "Country of origin",
                           "Incoterms"],
      "common_mistakes":  ["Undervaluing to reduce duty — customs fraud, serious penalties",
                            "Vague descriptions like 'gift' or 'sample'",
                            "Missing HS codes"]
    }
  },

  "duty_and_tax_calculation": {
    "formula": """
      CIF = product_value + shipping_cost + insurance
      import_duty = CIF * duty_rate(HS_code, destination_country)
      import_tax = (CIF + import_duty) * VAT_rate(destination_country)
      total_landed = CIF + import_duty + import_tax + customs_processing_fee
    """,
    "de_minimis": "Many countries exempt low-value shipments from duty — check threshold",
    "DDU_vs_DDP": {
      "DDU": "Delivered Duty Unpaid — customer pays duty on arrival. Common source of complaints.",
      "DDP": "Delivered Duty Paid — you pay duty upfront. Better customer experience, more complex."
    }
  },

  "prohibited_items": "Check destination country restrictions before shipping — not all carriers
                        publish complete lists. Lithium batteries, cosmetics, food, plants,
                        and medications all have specific rules."
}
```

### Step 4: Fulfillment Strategy
```
FULFILLMENT_DECISION = {
  "self_fulfillment": {
    "when_appropriate": "Under 50-100 orders per day, high SKU complexity, early stage",
    "true_cost":        "Include: labor time, packaging materials, shipping supplies,
                          space cost, error rate, opportunity cost of founder time",
    "system_needs":     ["Shipping software for rate comparison and label printing",
                          "Inventory management",
                          "Order management connected to store"]
  },

  "third_party_logistics": {
    "when_to_consider":  "100+ orders per day, or when fulfillment consumes founder time",
    "cost_components":   ["Receiving fee per unit inbound",
                           "Storage fee per cubic foot per month",
                           "Pick and pack fee per order",
                           "Shipping cost (often discounted vs retail)"],
    "evaluation_criteria": ["Location relative to customer base",
                              "Technology integration with your platform",
                              "Minimum volume requirements",
                              "Specialty capabilities if needed"]
  },

  "FBA": {
    "advantages":  "Prime badge, Amazon handles everything, customer trust",
    "disadvantages": "Inventory trapped if issues arise, limited brand control,
                      long-term storage fees, commingling risk",
    "cost_reality": "FBA fees plus storage often total 30-40% of revenue for many products"
  }
}
```

### Step 5: Claims and Exceptions
```
CLAIMS_FRAMEWORK = {
  "lost_shipment": {
    "timeline":     "File claim after carrier trace period — typically 7-15 business days",
    "documentation": ["Tracking number and full shipment details",
                       "Proof of value — invoice or purchase receipt",
                       "Proof of shipment — carrier receipt"],
    "coverage":     "Carriers cover declared value up to their free coverage limit.
                     Declared value insurance above that limit must be purchased."
  },

  "damaged_shipment": {
    "critical":     "Document damage immediately — photograph before unpacking fully",
    "process":      ["Keep all original packaging",
                     "Photograph damage from multiple angles",
                     "File claim within carrier deadline — usually 24-48 hours for visible damage",
                     "Request inspection if carrier requires it"]
  },

  "packaging_standards": {
    "principle":    "Carriers will deny claims if packaging is deemed inadequate",
    "rules":        ["Box must be structurally sound — no reusing damaged boxes",
                     "2 inches of cushioning material on all sides",
                     "Void fill prevents movement inside box",
                     "Double box for fragile items",
                     "Mark fragile — does not guarantee handling but supports claim"]
  }
}
```

---

## Shipping Cost Optimization
```
COST_OPTIMIZATION = {
  "volume_discounts":   "Carrier rates drop significantly at volume thresholds — negotiate early",
  "cubic_pricing":      "USPS offers cubic pricing for dense packages — often 40-60% cheaper",
  "zone_skipping":      "Ship in bulk to regional hub, inject into local network for last mile",
  "packaging_optimization": "Reducing package dimensions by 1 inch can change DIM weight tier",
  "negotiation":        "FedEx and UPS negotiate — even 100 packages per week has leverage",
  "multi_carrier":      "Rate shop every shipment — no carrier is cheapest for all scenarios"
}
```

---

## Quality Check Before Delivering

- [ ] Dimensional weight calculated for relevant shipments
- [ ] All surcharges included in carrier comparison — not just base rate
- [ ] International documentation checklist provided
- [ ] Duty and tax calculation includes all components
- [ ] Fulfillment recommendation based on actual volume and cost analysis
- [ ] Claims guidance specific to carrier and damage type
- [ ] Insurance coverage assessed against shipment value
