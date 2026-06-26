/**
 * Sports Pronostics Skill pour OpenClaw
 * Fournit des données football en temps réel pour les pronostics
 */

const RAPIDAPI_KEY  = process.env.RAPIDAPI_KEY;
const RAPIDAPI_HOST = process.env.RAPIDAPI_HOST || "free-api-live-football-data.p.rapidapi.com";
const BASE_URL      = `https://${RAPIDAPI_HOST}`;

// IDs des ligues européennes principales
const LEAGUES = {
  "ligue 1": "175",
  "premier league": "152",
  "champions league": "244",
  "la liga": "302",
  "bundesliga": "197",
  "serie a": "207",
  "ligue europa": "245",
  "liga": "302"
};

async function fetchFootball(endpoint, params = {}) {
  const url = new URL(`${BASE_URL}/${endpoint}`);
  Object.entries(params).forEach(([k, v]) => url.searchParams.append(k, v));

  const res = await fetch(url.toString(), {
    headers: {
      "X-RapidAPI-Key":  RAPIDAPI_KEY,
      "X-RapidAPI-Host": RAPIDAPI_HOST
    }
  });

  if (!res.ok) throw new Error(`API Error ${res.status}: ${await res.text()}`);
  return res.json();
}

// ── Fonctions de données ────────────────────────────────────────────────────

async function getUpcomingMatches(leagueName, count = 10) {
  const leagueId = LEAGUES[leagueName.toLowerCase()] || leagueName;
  const data = await fetchFootball("football-get-upcoming-matches-by-league", {
    leagueId,
    count
  });
  return data;
}

async function getLiveScores() {
  return fetchFootball("football-get-all-live-scores");
}

async function getTeamRecentMatches(teamId, count = 10) {
  return fetchFootball("football-get-matches-by-team-by-season", {
    teamId,
    count
  });
}

async function getHeadToHead(team1Id, team2Id, count = 8) {
  return fetchFootball("football-get-head2head", {
    team1Id,
    team2Id,
    count
  });
}

async function getStandings(leagueName) {
  const leagueId = LEAGUES[leagueName.toLowerCase()] || leagueName;
  return fetchFootball("football-get-standings-by-league", { leagueId });
}

async function getMatchLineups(matchId) {
  return fetchFootball("football-get-match-lineups", { matchId });
}

async function getMatchStats(matchId) {
  return fetchFootball("football-get-match-statistics", { matchId });
}

async function getMatchOdds(matchId) {
  return fetchFootball("football-get-match-odds", { matchId });
}

async function getAllLeagues() {
  return fetchFootball("football-get-all-leagues");
}

// ── Formatage de l'analyse ──────────────────────────────────────────────────

function formatMatchAnalysis(match, teamAStats, teamBStats, h2h, odds) {
  const homeTeam = match.homeTeam?.name || "Équipe domicile";
  const awayTeam = match.awayTeam?.name || "Équipe extérieur";
  const date     = match.date || "Date inconnue";

  let analysis = `\n⚽ **${homeTeam} vs ${awayTeam}**\n📅 ${date}\n\n`;

  // Forme récente
  if (teamAStats?.length) {
    const recentA = teamAStats.slice(0, 5);
    const formA = recentA.map(m => {
      const isHome = m.homeTeam?.id === match.homeTeam?.id;
      const scored   = isHome ? m.homeScore : m.awayScore;
      const conceded = isHome ? m.awayScore : m.homeScore;
      return scored > conceded ? "V" : scored === conceded ? "N" : "D";
    }).join("");
    analysis += `📊 **Forme ${homeTeam}** : ${formA}\n`;
  }

  if (teamBStats?.length) {
    const recentB = teamBStats.slice(0, 5);
    const formB = recentB.map(m => {
      const isAway = m.awayTeam?.id === match.awayTeam?.id;
      const scored   = isAway ? m.awayScore : m.homeScore;
      const conceded = isAway ? m.homeScore : m.awayScore;
      return scored > conceded ? "V" : scored === conceded ? "N" : "D";
    }).join("");
    analysis += `📊 **Forme ${awayTeam}** : ${formB}\n`;
  }

  // H2H
  if (h2h?.length) {
    analysis += `\n🔁 **H2H (${h2h.length} derniers)**\n`;
    h2h.slice(0, 5).forEach(m => {
      analysis += `  • ${m.homeTeam?.name} ${m.homeScore}-${m.awayScore} ${m.awayTeam?.name}\n`;
    });
  }

  // Cotes
  if (odds) {
    analysis += `\n💰 **Cotes** : 1: ${odds["1"] || "?"} | X: ${odds["X"] || "?"} | 2: ${odds["2"] || "?"}\n`;
  }

  analysis += `\n🎯 **Pronostics suggérés** :\n`;
  analysis += `_(Demande-moi "analyse complète ${homeTeam} vs ${awayTeam}" pour tous les marchés détaillés)_\n`;

  return analysis;
}

// ── Export du skill OpenClaw ────────────────────────────────────────────────

export default {
  name: "sports-pronostics",
  description: "Pronostics et analyses de matchs de football en temps réel",
  version: "1.0.0",

  // Déclencheurs : ces phrases activent le skill
  triggers: [
    "pronostic", "pari", "match", "foot", "football", "ligue 1",
    "premier league", "champions league", "bundesliga", "serie a", "la liga",
    "score", "analyse match", "btts", "over under", "cotes",
    "prochains matchs", "live score", "en direct"
  ],

  // Outils disponibles que OpenClaw peut appeler
  tools: {
    getUpcomingMatches: {
      description: "Matchs à venir pour une ligue",
      params: ["leagueName", "count"],
      fn: getUpcomingMatches
    },
    getLiveScores: {
      description: "Scores en direct",
      params: [],
      fn: getLiveScores
    },
    getTeamRecentMatches: {
      description: "Derniers matchs d'une équipe",
      params: ["teamId", "count"],
      fn: getTeamRecentMatches
    },
    getHeadToHead: {
      description: "Historique h2h entre deux équipes",
      params: ["team1Id", "team2Id", "count"],
      fn: getHeadToHead
    },
    getStandings: {
      description: "Classement d'une ligue",
      params: ["leagueName"],
      fn: getStandings
    },
    getMatchLineups: {
      description: "Compositions d'un match",
      params: ["matchId"],
      fn: getMatchLineups
    },
    getMatchStats: {
      description: "Statistiques détaillées d'un match",
      params: ["matchId"],
      fn: getMatchStats
    },
    getMatchOdds: {
      description: "Cotes d'un match",
      params: ["matchId"],
      fn: getMatchOdds
    },
    getAllLeagues: {
      description: "Liste toutes les ligues disponibles",
      params: [],
      fn: getAllLeagues
    }
  }
};
