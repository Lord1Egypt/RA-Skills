# Shipping Cost Model Quality Checklist

Before delivering results, verify each item:

---

## Cost completeness
- [ ] Carrier base rate included (not just list price — use commercial/negotiated if available)?
- [ ] DIM weight calculated and compared to actual weight?
- [ ] Fuel surcharge applied (12–15% for UPS/FedEx)?
- [ ] Residential surcharge included (if shipping to homes)?
- [ ] Peak/seasonal surcharges noted (if Q4 or high-volume period)?
- [ ] Pick-pack labor included in per-order cost?
- [ ] Packaging materials (box, filler, tape, inserts) included?
- [ ] Return shipping drag allocated per order?
- [ ] Reship/replacement cost factored in?

## Calculation accuracy
- [ ] Billable weight = max(actual weight, DIM weight)?
- [ ] Zone-weighted average uses real order distribution (not equal weighting)?
- [ ] Fuel surcharge calculated on base rate (not total)?
- [ ] Free-shipping threshold modeled with order distribution data?
- [ ] Margin impact shown as % of CM, not just dollar amount?

## Assumption transparency
- [ ] Every input labeled with confidence level (✅ / ⚠️ / ❓)?
- [ ] Rate sources cited (invoice, rate calculator, published rate card)?
- [ ] Zone distribution source identified (analytics, estimate, or assumption)?
- [ ] Low-confidence inputs flagged in results?

## Decision usefulness
- [ ] Results framed as absorb / threshold / pass-through / switch?
- [ ] Zone-level breakdown included (not just national average)?
- [ ] Threshold scenarios tested with real order value distribution?
- [ ] Specific actions recommended based on numbers?
- [ ] Risk flags highlighted (DIM weight, zone concentration, seasonal risk)?

## Common error check
- [ ] Not using Zone 2 rate as "average" when orders span all zones?
- [ ] Fuel surcharge not forgotten (it applies to almost every UPS/FedEx shipment)?
- [ ] Residential surcharge not missed (most DTC orders ship to homes)?
- [ ] DIM weight not ignored for bulky-but-light products?
- [ ] Return shipping cost not excluded from per-order economics?
- [ ] Seasonal surcharges noted if analysis covers Q4 period?
