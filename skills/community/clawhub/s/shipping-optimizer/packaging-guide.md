# Packaging Optimization Guide

## DIM Weight Fundamentals

### How DIM Weight Is Calculated
```
DIM Weight (lbs) = (Length × Width × Height) ÷ DIM Factor

DIM Factors:
- UPS Domestic: 139
- FedEx Domestic: 139
- USPS (rigid boxes): 166
- USPS (soft-side/poly mailers): Actual weight applies (no DIM)
```

You pay whichever is greater: actual weight OR DIM weight.

### When DIM Weight Hurts You Most
DIM weight creates the biggest overcharges when you're shipping:
- Lightweight apparel (t-shirts, hoodies) in large boxes
- Small electronics in padded rigid boxes
- Single units of product in a box sized for 3 units
- Products shipped with excessive void fill

### The DIM Weight Break-Even Formula
Find the maximum volume your product must fit in to avoid a DIM surcharge:

```
Max Volume (cubic inches) = Actual Weight (lbs) × DIM Factor

Example: 1.2 lb product, UPS DIM factor 139
Max Volume = 1.2 × 139 = 166.8 cubic inches
→ Box must be ≤ 166.8 cubic inches
→ Suitable box: 6" × 5" × 5" = 150 cubic inches ✅
→ Current box: 10" × 8" × 6" = 480 cubic inches → DIM weight = 3.45 lbs ❌
```

---

## Box Sizing Strategy

### The "Good, Better, Best" Box Audit
For each product you ship:

1. **Good:** The box you're currently using (often oversized)
2. **Better:** The smallest box that fits the product with minimal void fill
3. **Best:** Custom-sized box OR flexible packaging (poly mailer) if product allows

### Minimum Viable Box Set
Most ecommerce brands need only 4–6 box sizes:
- Extra small: 6" × 4" × 2" (accessories, small electronics)
- Small: 8" × 6" × 4" (shoes, single units of medium products)
- Medium: 12" × 9" × 6" (bundles, medium apparel)
- Large: 14" × 12" × 8" (multi-unit, heavier products)
- Flat rate option: USPS Regional Rate boxes for specific weight/zone combos

Having 12+ box sizes creates warehouse confusion and picking errors. More is not better.

### When to Use Poly Mailers
Poly mailers have zero DIM weight (actual weight only for USPS) and no rigid structure, making them dramatically cheaper for eligible products:

**Good for poly mailers:**
- Folded apparel (t-shirts, leggings, light hoodies)
- Flat items (posters, documents, fabric goods)
- Soft goods (plush toys, blankets if compressible)
- Non-fragile accessories

**Not suitable for poly mailers:**
- Glass, ceramics, rigid electronics
- Items that cannot be folded or compressed
- Products where presentation in the box is part of the experience (premium gifting)
- Multi-unit orders with fragile components

### Padded Mailers vs. Rigid Boxes
For semi-fragile items (jewelry, small electronics, beauty products):
- Padded bubble mailers are often a middle ground: still qualify for USPS actual weight (no DIM), provide cushioning, and are cheaper than small rigid boxes
- Test with 10–20 shipments to verify the product survives transit before fully switching

---

## Void Fill Efficiency

Excessive void fill has two costs:
1. It increases the package size → higher DIM weight
2. It adds weight (foam peanuts weigh more than you think at scale)

### Void Fill Cost Comparison (per cubic foot)
| Material | Cost | DIM impact |
|----------|------|-----------|
| Air pillows | $0.01–0.03 | High (adds volume) |
| Bubble wrap | $0.03–0.08 | High |
| Foam peanuts | $0.02–0.05 | High + adds weight |
| Kraft paper crumple | $0.005–0.02 | Medium |
| Custom molded inserts | $0.15–0.50 | None (no extra space) |
| Form-fitting secondary packaging | Variable | None |

**Best practice:** Design the product packaging to minimize the need for void fill. A product that fits snugly in its box needs less void fill and has lower DIM weight.

---

## Packaging Design for Shipping Cost Reduction

### Principles
1. **Right-size the box** — Product should have no more than 1" of clearance on each side (minimum protection) to 2–3" for fragile items.
2. **Reduce height** — In DIM weight calculations, reducing height often has the biggest impact since products are typically wider than tall.
3. **Stackable secondary packaging** — If your product can ship in its retail packaging (with outer protection), you eliminate the additional shipping box.
4. **Custom packaging for high-volume products** — If you ship 1,000+ units/month of a product, custom-sized boxes pay back in 3–6 months through DIM weight savings.

### Custom Box ROI Calculation
```
Annual DIM overcharge = Monthly shipments × 12 × $/shipment DIM premium
Custom box setup cost = $500–3,000 (tooling + minimum order)
Monthly box price difference = Standard box price − Custom box price (often similar or lower at volume)

ROI breakeven = Custom box setup cost ÷ Annual DIM overcharge

Example:
- 2,000 shipments/month × 12 = 24,000 shipments/year
- DIM premium: $3.00/shipment
- Annual DIM cost: $72,000
- Custom box setup: $1,500
- Breakeven: $1,500 ÷ $72,000 = 0.25 months → Instant ROI
```

---

## Packaging Checklist for New Products

Before setting a box size for any new product:

1. Measure the product accurately (L × W × H in final packaged state)
2. Calculate DIM weight for your proposed box in each carrier system
3. Determine if poly mailer is appropriate (product flexibility, fragility)
4. Select the smallest box that provides adequate protection with ≤2" clearance per side
5. Calculate the per-shipment DIM premium vs. a smaller box
6. Order a test run of 20–50 boxes and verify transit damage rate before committing to full inventory
7. Document the selected box size in your product SKU setup so picking errors are minimized
