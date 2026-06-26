# Freight Tracking



### Step 1 — Parse Response

Extract from `awb.shipmentSummary`:

| Field | Key |
|-------|-----|
| AWB | `awb.awb` |
| Origin | `awb.shipmentSummary.origin` |
| Origin name | `awb.shipmentSummary.originStationName` |
| Destination | `awb.shipmentSummary.destination` |
| Destination name | `awb.shipmentSummary.destinationStationName` |
| Total pieces | `awb.shipmentSummary.statedPieces` |
| Total weight (kg) | `awb.shipmentSummary.statedWeight` |
| Service | `awb.shipmentSummary.product` |
| Handling codes | `awb.shipmentSummary.handlingCodes` |
| Shipper | `awb.shipmentSummary.shipperName` |
| Consignee | `awb.shipmentSummary.consigneeName` |
| Latest stage | Key in `awb.shipmentSummary.stageSummary` with value `"ACTIVE"`, strip `STAGE_` prefix |
| Events | `awb.shipmentHistory` (chronological array) |


### Step 2 — Multiple AWBs

1. Pass up to 10 AWBs in the array
2. Show summary table with all results
3. Each row contains its own `<details>` expandable block

## Edge Cases

- **Empty response:** AWB not found — return "AWB not found"
- **Multiple AWBs:** Loop through array, one `<details>` block per AWB
- **No latest event:** Fall back to last item in `shipmentHistory`

## Notes

- AWB format: `XXX-XXXXXXX` (3 digits, hyphen, 7 digits) — enter with or without hyphen
- Public endpoint works without login/authentication
- Times are in airport local timezone (`transactionDate`) and UTC (`transactionDateUtc`)
