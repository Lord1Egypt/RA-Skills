# Fixed Output Formats (P0)

## Order Completion

```text
Order Completed
Master Order ID: <masterOrderId>
Direction: <Buy/Sell> <symbol>
Status: <status>
Filled Quantity: <filledQuantity>
Average Price: <averagePrice> USDT
Total Value: <totalValue> USDT
Maker Rate: <makerRate%>
Completion: <completionProgress>%
```

## TCA Output

```text
[<masterOrderId>]
- Avg Fill: <AvgFill> USDT
- Total Value: <TotalValue> USDT
- TWAP Slippage: <TwapSlippage%> (<saved/cost> <twapAmount> USDT)
- VWAP Slippage: <VwapSlippage%> (<saved/cost> <vwapAmount> USDT)
- Fee Savings: <FeeSavings> USDT
- Maker Rate: <MakerRate%>
```

## Output Integrity Rules

1. Do not add fields that are not returned or calculated by defined rules.
2. Keep field order stable for automation compatibility.
3. Preserve numeric precision from scripts unless explicitly requested.
