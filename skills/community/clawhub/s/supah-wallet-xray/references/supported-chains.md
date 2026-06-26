# Supported Chains — SUPAH Wallet X-Ray

| Chain | Explorer API | Native Token |
|-------|-------------|--------------|
| Ethereum | Etherscan | ETH |
| Base | Basescan | ETH |
| BSC | BscScan | BNB |
| Polygon | PolygonScan | MATIC |
| Arbitrum | Arbiscan | ETH |
| Optimism | Optimistic Etherscan | ETH |
| Avalanche | Snowtrace | AVAX |
| Fantom | FtmScan | FTM |

## Additional chains supported via GoPlusLabs:
Cronos, Gnosis, Celo, Moonbeam, Harmony, zkSync Era, Linea, Scroll, Mantle, Blast, Mode, Manta

## Default Chain
If no chain is specified, **Ethereum** is used as the default.

## ENS Resolution
The skill automatically resolves ENS names (.eth) and returns the underlying address.

## Data Sources
- **GoPlusLabs**: Malicious address detection, approval risks, phishing flags
- **Block Explorer APIs**: Transaction history, balances, token transfers
- **DexScreener**: Contract/pair detection
- **ENS Ideas API**: ENS name resolution
