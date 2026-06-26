import type { Sport, Game, ResolvedConfig } from '../types';
import { GAMES_ENDPOINTS } from '../constants';
import { ApiError, NetworkError } from '../utils/errors';

/**
 * Games service for fetching game data
 */
export class GamesService {
  constructor(private config: ResolvedConfig) {}

  /**
   * Get today's games for a sport
   */
  async getGames(sport: Sport): Promise<Game[]> {
    const endpoint = GAMES_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/today`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Failed to fetch games: ${response.status}`,
          response.status,
          errorData
        );
      }

      const data = await response.json();

      // Normalize response - API may return games array directly or nested
      const games = Array.isArray(data) ? data : (data.games || []);

      return this.normalizeGames(games, sport);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        `Failed to fetch ${sport.toUpperCase()} games`,
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Get tomorrow's games for a sport
   */
  async getTomorrowGames(sport: Sport): Promise<Game[]> {
    const endpoint = GAMES_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/tomorrow`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Failed to fetch games: ${response.status}`,
          response.status,
          errorData
        );
      }

      const data = await response.json();
      const games = Array.isArray(data) ? data : (data.games || []);

      return this.normalizeGames(games, sport);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        `Failed to fetch ${sport.toUpperCase()} games`,
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Get details for a specific game
   */
  async getGameDetails(sport: Sport, gameId: string): Promise<Game> {
    const endpoint = GAMES_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/${gameId}`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Failed to fetch game: ${response.status}`,
          response.status,
          errorData
        );
      }

      const data = await response.json();
      return this.normalizeGame(data, sport);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        `Failed to fetch game ${gameId}`,
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Normalize games array from API response
   */
  private normalizeGames(games: unknown[], sport: Sport): Game[] {
    return games.map((game) => this.normalizeGame(game, sport));
  }

  /**
   * Normalize a single game from API response
   */
  private normalizeGame(game: unknown, sport: Sport): Game {
    const g = game as Record<string, unknown>;

    return {
      id: String(g.id || g.gameId || g.game_id || ''),
      sport,
      homeTeam: {
        name: String(g.homeTeam || g.home_team || (g.home as Record<string, unknown>)?.name || ''),
        abbreviation: String(g.homeTeamAbbr || g.home_abbr || (g.home as Record<string, unknown>)?.abbreviation || ''),
        logoUrl: g.homeTeamLogo as string | undefined,
      },
      awayTeam: {
        name: String(g.awayTeam || g.away_team || (g.away as Record<string, unknown>)?.name || ''),
        abbreviation: String(g.awayTeamAbbr || g.away_abbr || (g.away as Record<string, unknown>)?.abbreviation || ''),
        logoUrl: g.awayTeamLogo as string | undefined,
      },
      startTime: String(g.startTime || g.start_time || g.gameTime || ''),
      status: this.normalizeStatus(g.status),
      venue: g.venue as string | undefined,
      homeScore: typeof g.homeScore === 'number' ? g.homeScore : undefined,
      awayScore: typeof g.awayScore === 'number' ? g.awayScore : undefined,
      odds: g.odds ? this.normalizeOdds(g.odds as Record<string, unknown>) : undefined,
    };
  }

  /**
   * Normalize game status
   */
  private normalizeStatus(status: unknown): Game['status'] {
    const s = String(status).toLowerCase();
    if (s.includes('progress') || s.includes('live')) return 'in_progress';
    if (s.includes('final') || s.includes('completed')) return 'final';
    if (s.includes('postponed')) return 'postponed';
    if (s.includes('cancelled') || s.includes('canceled')) return 'cancelled';
    return 'scheduled';
  }

  /**
   * Normalize odds object
   */
  private normalizeOdds(odds: Record<string, unknown>): Game['odds'] {
    return {
      homeMoneyline: typeof odds.homeMoneyline === 'number' ? odds.homeMoneyline : undefined,
      awayMoneyline: typeof odds.awayMoneyline === 'number' ? odds.awayMoneyline : undefined,
      spread: typeof odds.spread === 'number' ? odds.spread : undefined,
      total: typeof odds.total === 'number' ? odds.total : undefined,
      overOdds: typeof odds.overOdds === 'number' ? odds.overOdds : undefined,
      underOdds: typeof odds.underOdds === 'number' ? odds.underOdds : undefined,
    };
  }
}
