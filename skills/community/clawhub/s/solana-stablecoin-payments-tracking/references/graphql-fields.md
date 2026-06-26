# Solana stablecoin transfers — GraphQL reference

## Mint addresses (filter)

| Token | MintAddress |
|-------|----------------|
| USDT (SPL) | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |
| USDC (SPL) | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

The subscription filters `Transfer.Currency.MintAddress` with `in: [USDT, USDC]` and `Instruction.Program.Method` with `notIncludesCaseInsensitive: "swap"` (excludes methods whose name contains "swap", case-insensitive).

## Subscription (streaming)

```graphql
subscription StablecoinTransfers {
  Solana {
    Transfers(
      where: {
        Transfer: {
          Currency: {
            MintAddress: {
              in: [
                "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
              ]
            }
          }
        }
        Instruction: {
          Program: {
            Method: { notIncludesCaseInsensitive: "swap" }
          }
        }
      }
    ) {
      Transfer {
        Amount
        AmountInUSD
        Sender { Address Owner }
        Receiver { Address Owner }
        Currency { Symbol Name MintAddress }
      }
      Instruction { Program { Method } }
      Block { Time Height Slot }
      Transaction {
        Signature
        Signer
        Fee
        FeeInUSD
        FeePayer
      }
    }
  }
}
```

## Field notes

- **Transfer.Amount** — Token amount (API-defined scale; display with enough decimals for stablecoins).
- **Transfer.AmountInUSD** — USD notion of transfer when Bitquery provides it.
- **Sender / Receiver** — `Address` is typically the token account; `Owner` is the wallet owning that account.
- **Transaction.Fee** — Network fee in chain-native units (SOL/lamports per Bitquery schema).
- **Transaction.FeeInUSD** — Fee expressed in USD when available.
- **Instruction.Program.Method** — High-level method name for the instruction path.

If Bitquery returns a validation error on `where`, check the latest Solana transfers schema in Bitquery docs and adjust the `where` object only.
