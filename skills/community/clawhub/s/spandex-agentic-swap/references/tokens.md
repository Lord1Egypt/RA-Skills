# Token Reference — Base

## Known addresses

| Token | Address | Decimals |
| --- | --- | --- |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6 |
| WETH | `0x4200000000000000000000000000000000000006` | 18 |
| ETH (native) | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 |

## Amount conversion

The spanDEX API expects `inputAmount` and `outputAmount` as integer strings in base units (not decimal). Convert before calling the API.

Formula: `amount × 10^decimals`, result as an integer string.

### USDC (6 decimals)

| Human | Base units |
| --- | --- |
| 1 USDC | `1000000` |
| 5 USDC | `5000000` |
| 10 USDC | `10000000` |
| 100 USDC | `100000000` |

### WETH / ETH (18 decimals)

| Human | Base units |
| --- | --- |
| 0.001 WETH | `1000000000000000` |
| 0.01 WETH | `10000000000000000` |
| 0.1 WETH | `100000000000000000` |
| 1 WETH | `1000000000000000000` |
