# Seasonal Inventory Plan — Quality Checklist

Use this checklist before delivering a seasonal inventory plan. Every item should be confirmed or explicitly noted as not applicable.

## Data Quality

- [ ] Historical data covers at least 12 months (24+ preferred for seasonal decomposition)
- [ ] Data includes at least one full seasonal cycle
- [ ] Stockout periods identified and demand estimated for those periods
- [ ] Promotional spikes flagged with promotion dates documented
- [ ] Data gaps identified and interpolated or excluded with documentation
- [ ] Units and revenue are consistent (no mixed currencies or time zones)
- [ ] Returns/cancellations netted from demand figures

## Seasonal Decomposition

- [ ] Decomposition model chosen (multiplicative vs. additive) with rationale
- [ ] Base trend calculated and stated as annual growth rate
- [ ] Seasonal indices calculated for every period in the planning cycle
- [ ] Indices normalized to average 1.0 across the full cycle
- [ ] Residual variation calculated for safety stock sizing
- [ ] Products grouped by seasonal profile (sharp peak, broad season, dual peak, etc.)
- [ ] Products with insufficient data flagged and given category-level indices

## Demand Forecast

- [ ] Forward forecast generated for every period in the planning horizon
- [ ] Trend adjustment applied to seasonal indices (not just repeating last year)
- [ ] Confidence intervals provided showing forecast uncertainty range
- [ ] Known adjustments applied (promotions, launches, channel changes, price changes)
- [ ] Forecast validated against common sense — no obviously impossible values
- [ ] Peak period forecasts specifically reviewed for reasonableness

## Inventory Targets

- [ ] Cycle stock calculated for each period based on demand and replenishment frequency
- [ ] Safety stock calibrated per period based on demand variability (not uniform)
- [ ] Peak periods carry higher safety stock than trough periods
- [ ] Pipeline stock accounted for based on lead times
- [ ] Target inventory position calculated for each period (cycle + safety + pipeline)
- [ ] Peak inventory position validated against warehouse capacity
- [ ] Service level targets stated and used in safety stock calculation

## Reorder Calendar

- [ ] Every reorder includes: order date, quantity, expected arrival, demand period covered
- [ ] Lead times are supplier-specific (not generic averages)
- [ ] Lead time variability buffer included in order timing
- [ ] Pre-season buys phased across multiple orders where possible
- [ ] Blind buy risk identified for orders placed before demand signals available
- [ ] Supplier MOQs validated against order quantities
- [ ] In-season replenishment triggers defined with specific quantity and timing

## Cash Flow

- [ ] Total pre-season investment calculated and stated
- [ ] Cash flow phased by month showing when payments are due
- [ ] Peak cash requirement identified and validated against available funding
- [ ] Revenue timing mapped against investment timeline
- [ ] Cash flow constraints acknowledged if they limit optimal inventory position

## Post-Season Strategy

- [ ] Markdown start date or trigger defined before the season begins
- [ ] Progressive markdown schedule with specific dates and discount depths
- [ ] Sell-through targets set for each markdown stage
- [ ] Final liquidation deadline established
- [ ] Liquidation channel identified (marketplace, wholesale, donation)
- [ ] Financial impact of markdown plan estimated (recovered revenue vs. margin loss)

## Constraint Validation

- [ ] Warehouse capacity checked against peak inventory position
- [ ] Supplier minimums and maximums validated against order quantities
- [ ] Shelf life / expiration checked against hold time through season
- [ ] Shipping capacity confirmed for peak receiving periods
- [ ] Any constraint violations documented with plan adjustments

## Risk Assessment

- [ ] Demand exceeds forecast scenario planned (replenishment strategy)
- [ ] Demand falls short scenario planned (earlier markdown trigger)
- [ ] Supplier delay contingency identified (alternative sources, air freight)
- [ ] Storage overflow contingency identified (offsite, delayed delivery)
- [ ] Each risk includes likelihood, impact, and specific mitigation action

## Report Quality

- [ ] Executive summary states peak season, total investment, and projected outcomes
- [ ] All periods included in forecast and inventory target tables
- [ ] Reorder calendar is actionable (specific dates, quantities, suppliers)
- [ ] Post-season markdown calendar includes specific trigger points
- [ ] Next steps include specific dates and responsible parties
- [ ] Plan follows the output template structure
