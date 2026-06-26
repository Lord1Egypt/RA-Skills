#!/usr/bin/env node
// get-games.js — fetch games from Azuro REST API and display main market odds
// Usage:
//   node get-games.js [sport-slug] [league-slug] [count]   # browse by sport/league
//   node get-games.js --search "<query>" [count]           # search by team/match name
//   node get-games.js --list-sports                        # list all available sports and leagues
// Examples:
//   node get-games.js                              # top 20 games all sports
//   node get-games.js basketball nba 10            # NBA only
//   node get-games.js football laliga 5            # LaLiga (slug: laliga)
//   node get-games.js football premier-league 10   # Premier League
//   node get-games.js ice-hockey nhl 5             # NHL
//   node get-games.js --search "Real Madrid" 5     # search by team name
//   node get-games.js --search "Celtics" 3         # search by team name
//   node get-games.js --list-sports                # show all sports+leagues with exact slugs
//
// IMPORTANT: sport and league args must be exact API slugs (e.g. ice-hockey, laliga).
// If unsure of the slug, use --list-sports to see all available options,
// or use --search to find games by team/league name.
//
// Uses @azuro-org/dictionaries to identify the correct main market condition
// and translate outcomeIds to human-readable labels — same as the original subgraph version.

const { getMarketName, getSelectionName } = require('@azuro-org/dictionaries')
const https = require('https')

// ─── Constants ───────────────────────────────────────────────────────────────
const API_HOST        = 'api.onchainfeed.org'
const SPORTS_PATH     = '/api/v1/public/market-manager/sports'
const CONDITIONS_PATH = '/api/v1/public/market-manager/conditions-by-game-ids'
const SEARCH_PATH     = '/api/v1/public/market-manager/search'
const NAVIGATION_PATH = '/api/v1/public/market-manager/navigation'
const ENVIRONMENT     = 'PolygonUSDT'

// Verified main market names from @azuro-org/dictionaries
const MAIN_MARKET_NAMES = new Set([
  'Match Winner',
  'Full Time Result',
  'Winner',
  'Fight Winner',
  'Whole game - Full time result Goal',
])

const SPORT_SLUG_ALIASES = {
  'hockey': 'ice-hockey', 'nhl': 'ice-hockey', 'ice-hockey': 'ice-hockey', 'icehockey': 'ice-hockey',
  'soccer': 'football', 'basketball': 'basketball', 'nba': 'basketball',
  'mma': 'mma', 'baseball': 'baseball', 'mlb': 'baseball',
  'american-football': 'american-football', 'nfl': 'american-football',
}

// ─── Args ────────────────────────────────────────────────────────────────────
const args        = process.argv.slice(2)
const listSports  = args.includes('--list-sports')
const searchIdx   = args.indexOf('--search')
const searchQuery = searchIdx !== -1 ? args[searchIdx + 1] : null
const countArgS   = searchIdx !== -1 ? args[searchIdx + 2] : null

const positional    = searchQuery ? [] : args
const [sportSlugRaw, leagueSlugRaw, countArg] = positional
const sportSlug     = sportSlugRaw ? (SPORT_SLUG_ALIASES[sportSlugRaw.toLowerCase()] || sportSlugRaw.toLowerCase()) : null
const isLeagueCount = leagueSlugRaw && !isNaN(leagueSlugRaw)
const leagueSlug    = !isLeagueCount && leagueSlugRaw ? leagueSlugRaw.toLowerCase() : null
const count         = parseInt(countArgS) || parseInt(countArg) || (isLeagueCount ? parseInt(leagueSlugRaw) : 20)

// ─── HTTP helpers ─────────────────────────────────────────────────────────────
function getJson(path) {
  return new Promise((resolve, reject) => {
    https.get({ hostname: API_HOST, path, headers: { Accept: 'application/json' } }, res => {
      let raw = ''
      res.on('data', c => { raw += c })
      res.on('end', () => { try { resolve(JSON.parse(raw)) } catch (e) { reject(new Error('Parse error: ' + raw.slice(0, 200))) } })
    }).on('error', reject)
  })
}

function postJson(path, body) {
  return new Promise((resolve, reject) => {
    const data = Buffer.from(JSON.stringify(body))
    const req  = https.request(
      { hostname: API_HOST, path, method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': data.length } },
      res => { let raw = ''; res.on('data', c => { raw += c }); res.on('end', () => { try { resolve(JSON.parse(raw)) } catch (e) { reject(new Error('Parse error: ' + raw.slice(0, 200))) } }) }
    )
    req.on('error', reject); req.write(data); req.end()
  })
}

// ─── Extract games from /sports response ─────────────────────────────────────
function extractGames(data, stateName) {
  const games = []
  for (const sport of (data.sports || [])) {
    for (const country of (sport.countries || [])) {
      for (const league of (country.leagues || [])) {
        for (const game of (league.games || [])) {
          games.push({ ...game, state: stateName, sportName: sport.name, leagueName: league.name })
        }
      }
    }
  }
  return games
}

// ─── Main ─────────────────────────────────────────────────────────────────────
;(async () => {
  let allGames = []

  // ── List sports mode ──────────────────────────────────────────────────────
  if (listSports) {
    console.log('\n⏳ Fetching available sports and leagues...')
    try {
      const nav = await getJson(`${NAVIGATION_PATH}?environment=${ENVIRONMENT}`)
      for (const sport of (nav.sports || [])) {
        console.log(`\n🏅 ${sport.name} (slug: "${sport.sport?.slug || sport.slug}")`)
        for (const country of (sport.countries || [])) {
          for (const league of (country.leagues || [])) {
            if (league.activeGamesCount > 0) {
              console.log(`   ${league.name} — slug: "${league.slug}" (${league.activeGamesCount} games)`)
            }
          }
        }
      }
    } catch (e) { console.error('Failed to fetch navigation:', e.message); process.exit(1) }
    process.exit(0)
  }

  if (searchQuery) {
    // ── Search mode ──────────────────────────────────────────────────────────
    console.log(`🔍 Searching for: "${searchQuery}"...`)
    try {
      const params = new URLSearchParams({ environment: ENVIRONMENT, request: searchQuery, page: '1', perPage: String(Math.max(count * 2, 20)) })
      const res    = await getJson(`${SEARCH_PATH}?${params.toString()}`)
      allGames     = (res.games || []).map(g => ({
        ...g,
        state:      g.state || 'Prematch',
        sportName:  g.sport?.name || 'Unknown',
        leagueName: g.league?.name || 'Unknown',
      }))
      if (res.total > 0) console.log(`   Found ${res.total} result(s)`)
    } catch (e) { console.error('Search failed:', e.message); process.exit(1) }
  } else {
    // ── Browse mode ──────────────────────────────────────────────────────────
    const base = { environment: ENVIRONMENT, orderBy: 'turnover', orderDirection: 'desc', numberOfGames: String(count) }
    if (sportSlug)  base.sportSlug  = sportSlug
    if (leagueSlug) base.leagueSlug = leagueSlug

    try {
      const [live, prematch] = await Promise.all([
        getJson(`${SPORTS_PATH}?${new URLSearchParams({ ...base, gameState: 'Live' }).toString()}`),
        getJson(`${SPORTS_PATH}?${new URLSearchParams({ ...base, gameState: 'Prematch' }).toString()}`),
      ])
      allGames = [...extractGames(live, 'Live'), ...extractGames(prematch, 'Prematch')]
    } catch (e) { console.error('Failed to fetch games:', e.message); process.exit(1) }
  }

  if (!allGames.length) { console.log('No games found.'); process.exit(0) }

  // Deduplicate, keep up to count
  const seen = new Set(), games = []
  for (const g of allGames) {
    const id = String(g.gameId)
    if (!seen.has(id)) { seen.add(id); games.push(g) }
    if (games.length >= count) break
  }

  // ── Fetch conditions (all markets) for all games ──────────────────────────
  let conditionsMap = {}
  try {
    const res = await postJson(CONDITIONS_PATH, { gameIds: games.map(g => g.gameId), environment: ENVIRONMENT })
    for (const cond of (res.conditions || [])) {
      const gid = String(cond.game?.gameId)
      if (!conditionsMap[gid]) conditionsMap[gid] = []
      conditionsMap[gid].push(cond)
    }
  } catch (e) { console.error('Failed to fetch conditions:', e.message); process.exit(1) }

  // ── Build results using dictionaries to identify main market ─────────────
  // CRITICAL: Use @azuro-org/dictionaries getMarketName() to identify the correct
  // main market condition. Do NOT guess by title string — the API returns many
  // conditions per game (totals, handicap, etc.) and only the dictionary correctly
  // identifies which outcomeId belongs to which market.
  const results = []
  for (const game of games) {
    const gid        = String(game.gameId)
    const conditions = (conditionsMap[gid] || []).filter(c => c.state === 'Active')
    if (!conditions.length) continue

    let mainCond      = null
    let mainMarketName = null

    for (const cond of conditions) {
      if (!cond.outcomes?.length) continue
      try {
        const name = getMarketName({ outcomeId: parseInt(cond.outcomes[0].outcomeId) })
        if (MAIN_MARKET_NAMES.has(name)) { mainCond = cond; mainMarketName = name; break }
      } catch (_) {}
    }
    if (!mainCond) continue // skip games with no active main market

    const parts      = game.participants || []
    const selections = (mainCond.outcomes || []).map(o => {
      let sel
      try { sel = getSelectionName({ outcomeId: parseInt(o.outcomeId), withPoint: true }) } catch (_) { sel = String(o.outcomeId) }
      const label = sel === '1' ? (parts[0]?.name || 'Team 1')
                  : sel === '2' ? (parts[1]?.name || 'Team 2')
                  : 'Draw'
      return { label, odds: parseFloat(o.odds).toFixed(2), outcomeId: parseInt(o.outcomeId), conditionId: mainCond.conditionId }
    })

    if (!selections.length) continue

    const startsAt = parseInt(game.startsAt)
    const d = new Date(startsAt * 1000)
    const kickoff = d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', timeZone: 'Europe/Madrid' })
      + ', ' + d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Madrid' })

    results.push({ gameId: gid, title: game.title, state: game.state, kickoff, startsAt, sport: game.sportName, league: game.leagueName, market: mainMarketName, selections })
  }

  if (!results.length) { console.log('No games with active main market found.'); process.exit(0) }

  // ── Human-readable output ─────────────────────────────────────────────────
  let currentSport = ''
  results.forEach((g, i) => {
    if (g.sport !== currentSport) { currentSport = g.sport; console.log('\n' + g.sport + ' — ' + g.league) }
    const status   = g.state === 'Live' ? '[LIVE 🔴]' : `[Prematch, ${g.kickoff}]`
    const oddsLine = g.selections.map(s => `${s.label} ${s.odds}`).join(' | ')
    console.log(`${i + 1}. ${g.title}  ${status}`)
    console.log(`   ${g.market}: ${oddsLine}`)
  })

  console.log('\n---JSON---')
  console.log(JSON.stringify(results))

})().catch(e => { console.error('Fatal error:', e.message); process.exit(1) })
