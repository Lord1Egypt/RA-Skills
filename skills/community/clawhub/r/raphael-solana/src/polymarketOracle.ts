// Polymarket weather arb — read-only oracle layer
// No auth required for any function in this file.

export type CityKey = "nyc" | "london" | "seoul" | "chicago" | "dallas" | "miami" | "paris" | "toronto" | "seattle"

export type CityConfig = {
  lat: number
  lon: number
  slugName: string
  label: string
  tz: string
}

export const CITIES: Record<CityKey, CityConfig> = {
  nyc:     { lat: 40.7128, lon: -74.0060, slugName: "nyc",     label: "New York City", tz: "America/New_York"    },
  london:  { lat: 51.5074, lon: -0.1278,  slugName: "london",  label: "London",        tz: "Europe/London"       },
  seoul:   { lat: 37.5665, lon: 126.9780, slugName: "seoul",   label: "Seoul",         tz: "Asia/Seoul"          },
  chicago: { lat: 41.8781, lon: -87.6298, slugName: "chicago", label: "Chicago",       tz: "America/Chicago"     },
  dallas:  { lat: 32.7767, lon: -96.7970, slugName: "dallas",  label: "Dallas",        tz: "America/Chicago"     },
  miami:   { lat: 25.7617, lon: -80.1918, slugName: "miami",   label: "Miami",         tz: "America/New_York"    },
  paris:   { lat: 48.8566, lon:  2.3522,  slugName: "paris",   label: "Paris",         tz: "Europe/Paris"        },
  toronto: { lat: 43.6532, lon: -79.3832, slugName: "toronto", label: "Toronto",       tz: "America/Toronto"     },
  seattle: { lat: 47.6062, lon: -122.3321,slugName: "seattle", label: "Seattle",       tz: "America/Los_Angeles" },
}

// ── Types ─────────────────────────────────────────────────────────────────────

export type WeatherForecast = {
  forecastHighF: number
  fetchedAt: number
}

export type PolymarketBracket = {
  label: string          // "40-41°F" | "33°F or below" | "48°F or higher"
  lo: number             // lower bound inclusive; -Infinity for lower terminal
  hi: number             // upper bound inclusive; +Infinity for upper terminal
  yesTokenId: string
  conditionId: string
  isTerminal: boolean
  acceptingOrders: boolean
  closeTimeUtc: Date
}

export type PricedBracket = PolymarketBracket & {
  askPrice: number       // price you pay to buy YES (0–1)
  fairValue: number      // our calculated probability (0–1)
  edge: number           // fairValue − askPrice
}

// ── Helpers ───────────────────────────────────────────────────────────────────

// Date → "february-25-2026"
export const formatDateSlug = (d: Date): string => {
  const months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
  return `${months[d.getMonth()]}-${d.getDate()}-${d.getFullYear()}`
}

// Abramowitz & Stegun erf approximation (max error ~1.5e-7)
const erf = (x: number): number => {
  const sign = x < 0 ? -1 : 1
  x = Math.abs(x)
  const t = 1 / (1 + 0.3275911 * x)
  const poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))))
  return sign * (1 - poly * Math.exp(-x * x))
}

// P(X ≤ x) where X ~ N(mu, sigma²)
const normalCDF = (x: number, mu: number, sigma: number): number => {
  if (!isFinite(x)) return x > 0 ? 1 : 0
  return 0.5 * (1 + erf((x - mu) / (sigma * Math.SQRT2)))
}

// P(reported high falls in bracket [lo, hi]) using half-integer boundaries
// e.g. "40-41°F" bracket: P(39.5 ≤ X < 41.5) = CDF(41.5) − CDF(39.5)
const bracketFairValue = (lo: number, hi: number, mu: number, sigma: number): number => {
  const loCDF = lo === -Infinity ? 0 : normalCDF(lo - 0.5, mu, sigma)
  const hiCDF = hi === Infinity  ? 1 : normalCDF(hi + 0.5, mu, sigma)
  return Math.max(0, Math.min(1, hiCDF - loCDF))
}

// sigma grows with time-to-resolution: same-day ≈ 2°F, next-day ≈ 4°F
export const forecastSigmaF = (hoursUntilClose: number): number => {
  if (hoursUntilClose <= 6)  return 2
  if (hoursUntilClose >= 30) return 4
  return 2 + ((hoursUntilClose - 6) / 24) * 2
}

// ── Open-Meteo ────────────────────────────────────────────────────────────────

export const fetchOpenMeteoForecast = async (city: CityKey): Promise<WeatherForecast> => {
  const c = CITIES[city]
  const url = `https://api.open-meteo.com/v1/forecast` +
    `?latitude=${c.lat}&longitude=${c.lon}` +
    `&daily=temperature_2m_max` +
    `&temperature_unit=fahrenheit` +
    `&timezone=${encodeURIComponent(c.tz)}` +
    `&forecast_days=2`

  const res = await fetch(url)
  if (!res.ok) throw new Error(`Open-Meteo failed for ${city} (${res.status}): ${await res.text()}`)

  const data = await res.json() as { daily?: { temperature_2m_max?: number[] } }
  const forecastHighF = data.daily?.temperature_2m_max?.[0]
  if (forecastHighF == null) throw new Error(`Open-Meteo: no temperature data for ${city}`)

  return { forecastHighF, fetchedAt: Date.now() }
}

// ── Polymarket Gamma API ───────────────────────────────────────────────────────

const parseBracketRange = (label: string): [number, number] => {
  const range = label.match(/^(\d+)-(\d+)°F$/)
  if (range) return [parseInt(range[1]), parseInt(range[2])]

  const below = label.match(/^(\d+)°F or below$/)
  if (below) return [-Infinity, parseInt(below[1])]

  const above = label.match(/^(\d+)°F or higher$/)
  if (above) return [parseInt(above[1]), Infinity]

  // Celsius variants (London, Paris, Seoul, Toronto)
  const rangeC = label.match(/^(-?\d+)-(-?\d+)°C$/)
  if (rangeC) {
    const loC = parseInt(rangeC[1]), hiC = parseInt(rangeC[2])
    return [loC * 9/5 + 32, hiC * 9/5 + 32]
  }

  throw new Error(`Cannot parse bracket: "${label}"`)
}

export const fetchPolymarketWeatherBrackets = async (
  city: CityKey,
  date: Date,
): Promise<PolymarketBracket[]> => {
  const c = CITIES[city]
  const slug = `highest-temperature-in-${c.slugName}-on-${formatDateSlug(date)}`
  const url = `https://gamma-api.polymarket.com/events?slug=${slug}`

  const res = await fetch(url, { headers: { Accept: "application/json" } })
  if (!res.ok) throw new Error(`Gamma API failed (${res.status}): ${await res.text()}`)

  const events = await res.json() as Array<{
    markets?: Array<{
      conditionId: string
      groupItemTitle?: string
      clobTokenIds?: string[]
      acceptingOrders?: boolean
      endDate?: string
    }>
  }>

  if (!events.length || !events[0].markets?.length) return []

  const brackets: PolymarketBracket[] = []
  for (const m of events[0].markets) {
    const label = m.groupItemTitle ?? ""
    if (!label || !m.clobTokenIds?.length) continue

    try {
      const [lo, hi] = parseBracketRange(label)
      brackets.push({
        label,
        lo,
        hi,
        yesTokenId: m.clobTokenIds[0],
        conditionId: m.conditionId,
        isTerminal: lo === -Infinity || hi === Infinity,
        acceptingOrders: m.acceptingOrders ?? false,
        closeTimeUtc: m.endDate ? new Date(m.endDate) : new Date(),
      })
    } catch {
      // skip brackets with unrecognised formats
    }
  }

  return brackets.sort((a, b) => (isFinite(a.lo) ? a.lo : -999) - (isFinite(b.lo) ? b.lo : -999))
}

// ── CLOB Pricing ─────────────────────────────────────────────────────────────

const fetchAskPrice = async (tokenId: string): Promise<number | null> => {
  try {
    const res = await fetch(
      `https://clob.polymarket.com/price?token_id=${tokenId}&side=sell`,
      { headers: { Accept: "application/json" } },
    )
    if (!res.ok) return null
    const data = await res.json() as { price?: string }
    const p = parseFloat(data.price ?? "")
    return isNaN(p) ? null : p
  } catch {
    return null
  }
}

export const priceBrackets = async (
  brackets: PolymarketBracket[],
  forecastHighF: number,
  sigmaF: number,
): Promise<PricedBracket[]> => {
  const askPrices = await Promise.all(brackets.map(b => fetchAskPrice(b.yesTokenId)))

  return brackets
    .map((b, i) => {
      const askPrice = askPrices[i]
      if (askPrice === null) return null
      const fairValue = bracketFairValue(b.lo, b.hi, forecastHighF, sigmaF)
      return { ...b, askPrice, fairValue, edge: fairValue - askPrice } as PricedBracket
    })
    .filter((b): b is PricedBracket => b !== null)
    .sort((a, b) => b.edge - a.edge)
}

// ── Top-level: scan all brackets for a city ───────────────────────────────────

export type CityOpportunity = {
  city: CityKey
  forecastHighF: number
  sigmaF: number
  targetBracket: PricedBracket | null   // best bracket if edge qualifies
  allBrackets: PricedBracket[]
  skippedReason: string | null
  scannedAt: number
}

export const scanCity = async (
  city: CityKey,
  date: Date,
  minEdge: number,
  minFairValue: number,
): Promise<CityOpportunity> => {
  const base: Omit<CityOpportunity, "targetBracket" | "allBrackets" | "skippedReason"> & Partial<CityOpportunity> = {
    city,
    forecastHighF: 0,
    sigmaF: 0,
    scannedAt: Date.now(),
  }

  // 1. Forecast
  const forecast = await fetchOpenMeteoForecast(city)
  base.forecastHighF = forecast.forecastHighF

  // 2. Market brackets
  const rawBrackets = await fetchPolymarketWeatherBrackets(city, date)
  if (!rawBrackets.length) {
    return { ...base, targetBracket: null, allBrackets: [], sigmaF: 0,
      skippedReason: "no_market" } as CityOpportunity
  }

  // 3. Time-to-close guard (30-min buffer)
  const closeTimes = rawBrackets.map(b => b.closeTimeUtc.getTime())
  const closeTimeMs = Math.min(...closeTimes)
  const msUntilClose = closeTimeMs - Date.now()
  if (msUntilClose < 30 * 60 * 1000) {
    return { ...base, targetBracket: null, allBrackets: [], sigmaF: 0,
      skippedReason: "market_closing_soon" } as CityOpportunity
  }

  const hoursUntilClose = msUntilClose / 3_600_000
  const sigmaF = forecastSigmaF(hoursUntilClose)
  base.sigmaF = sigmaF

  // 4. Price non-terminal brackets only
  const tradeable = rawBrackets.filter(b => !b.isTerminal && b.acceptingOrders)
  const priced = await priceBrackets(tradeable, forecast.forecastHighF, sigmaF)

  // 5. Find best opportunity
  const best = priced.find(b => b.edge >= minEdge && b.fairValue >= minFairValue) ?? null

  return {
    ...base,
    sigmaF,
    targetBracket: best,
    allBrackets: priced,
    skippedReason: best ? null : "no_edge",
  } as CityOpportunity
}
