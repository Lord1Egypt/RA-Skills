// Polymarket weather arbitrage strategy
// Edge: NOAA/Open-Meteo forecasts are more accurate than crowd pricing at trade time.
// We buy underpriced YES brackets and hold until daily resolution at ~$1.

import { scanCity, CITIES, formatDateSlug } from "./polymarketOracle.ts"
import { loadEvmWallet } from "./evmWallet.ts"
import { placeOrder, getOpenOrders, getUsdcBalance } from "./polymarketClob.ts"
import type { CityKey } from "./polymarketOracle.ts"
import type { PolymarketWeatherConfig, PolymarketWeatherReading } from "./types.ts"

const log = (msg: string) => console.log(`[polymarket_arb] ${msg}`)

// ── Tick ──────────────────────────────────────────────────────────────────────

export const runPolymarketWeatherArbTick = async (
  config: PolymarketWeatherConfig,
  onReading: (readings: PolymarketWeatherReading[]) => void,
): Promise<void> => {
  const today = new Date()
  const readings: PolymarketWeatherReading[] = []

  try {
    const wallet = config.dryRun ? null : await loadEvmWallet(config.walletName)

    // Open positions — skip any city already positioned
    const openOrders = wallet ? await getOpenOrders(wallet).catch(() => []) : []
    const positionedTokenIds = new Set(openOrders.map(o => o.asset_id))

    // USDC balance — checked once per tick
    const usdcBalance = wallet ? await getUsdcBalance(wallet.address).catch(() => 0) : 0
    if (wallet) log(`USDC balance: $${usdcBalance.toFixed(2)}`)

    for (const city of config.cities as CityKey[]) {
      const cityLabel = CITIES[city]?.label ?? city
      const reading: PolymarketWeatherReading = {
        city,
        forecastHighF: 0,
        sigmaF: 0,
        targetBracket: null,
        bestEdge: null,
        orderId: null,
        skippedReason: null,
        scannedAt: Date.now(),
      }

      try {
        const result = await scanCity(city, today, config.minEdge, config.minFairValue)
        reading.forecastHighF = result.forecastHighF
        reading.sigmaF        = result.sigmaF
        reading.targetBracket = result.targetBracket?.label ?? null
        reading.bestEdge      = result.targetBracket?.edge ?? null

        if (result.skippedReason) {
          reading.skippedReason = result.skippedReason
          log(`${cityLabel}: skipped (${result.skippedReason})`)
          readings.push(reading)
          continue
        }

        const best = result.targetBracket!
        log(
          `${cityLabel}: forecast ${result.forecastHighF}°F | ` +
          `bracket "${best.label}" | fair ${(best.fairValue * 100).toFixed(1)}% | ` +
          `ask ${(best.askPrice * 100).toFixed(1)}% | edge ${(best.edge * 100).toFixed(1)}%`
        )

        // Already positioned in this bracket? Skip.
        if (positionedTokenIds.has(best.yesTokenId)) {
          reading.skippedReason = "already_positioned"
          log(`${cityLabel}: already have an open position — skipping`)
          readings.push(reading)
          continue
        }

        const tradeSize = Math.min(config.tradeAmountUsdc, config.maxPositionUsdc)

        if (config.dryRun) {
          log(
            `[dry-run] Would buy ${tradeSize} USDC of "${best.label}" YES @ ${best.askPrice.toFixed(3)} ` +
            `(${formatDateSlug(today)})`
          )
        } else {
          // Hard guards before execution
          if (usdcBalance < tradeSize) {
            reading.skippedReason = "insufficient_usdc"
            log(`${cityLabel}: insufficient USDC ($${usdcBalance.toFixed(2)} < $${tradeSize}) — skipping`)
            readings.push(reading)
            continue
          }

          const order = await placeOrder(wallet!, best.yesTokenId, best.askPrice, tradeSize)
          reading.orderId = order.orderId
          log(`✅ ${cityLabel}: order placed — ${order.orderId} | ${tradeSize} USDC @ ${best.askPrice.toFixed(3)}`)
        }
      } catch (err) {
        reading.skippedReason = "error"
        log(`${cityLabel}: error — ${err instanceof Error ? err.message : String(err)}`)
      }

      readings.push(reading)
    }
  } catch (err) {
    log(`tick error: ${err instanceof Error ? err.message : String(err)}`)
  }

  onReading(readings)
}
