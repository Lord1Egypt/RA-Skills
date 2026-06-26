import { PublicKey, Transaction, VersionedTransaction, Keypair } from '@solana/web3.js';

/**
 * Supported sports leagues
 */
type Sport = 'nba' | 'nfl' | 'mlb' | 'mls';
/**
 * Team information
 */
interface Team {
    name: string;
    abbreviation: string;
    logoUrl?: string;
    record?: string;
}
/**
 * Betting odds for a game
 */
interface GameOdds {
    /** Home team moneyline (American odds, e.g., -150) */
    homeMoneyline?: number;
    /** Away team moneyline (American odds, e.g., +130) */
    awayMoneyline?: number;
    /** Point spread (negative = home favored) */
    spread?: number;
    /** Home spread odds */
    homeSpreadOdds?: number;
    /** Away spread odds */
    awaySpreadOdds?: number;
    /** Over/under total points */
    total?: number;
    /** Over odds */
    overOdds?: number;
    /** Under odds */
    underOdds?: number;
}
/**
 * Game status
 */
type GameStatus = 'scheduled' | 'in_progress' | 'final' | 'postponed' | 'cancelled';
/**
 * Game information
 */
interface Game {
    /** Unique game identifier (e.g., "nba-2026-03-28-lal-bos") */
    id: string;
    /** Sport league */
    sport: Sport;
    /** Home team */
    homeTeam: Team;
    /** Away team */
    awayTeam: Team;
    /** Game start time (ISO 8601) */
    startTime: string;
    /** Current game status */
    status: GameStatus;
    /** Betting odds (if available) */
    odds?: GameOdds;
    /** Venue name */
    venue?: string;
    /** Home team score (if in_progress or final) */
    homeScore?: number;
    /** Away team score (if in_progress or final) */
    awayScore?: number;
}
/**
 * Response from getGames()
 */
interface GamesResponse {
    games: Game[];
    sport: Sport;
    date: string;
}

/**
 * Elo rating system data
 */
interface EloRatings {
    /** Home team Elo rating */
    homeElo: number;
    /** Away team Elo rating */
    awayElo: number;
    /** Win probability based on Elo */
    eloHomeWinProb: number;
    /** Predicted spread from Elo */
    eloSpread: number;
}
/**
 * Four Factors basketball analytics (NBA)
 */
interface FourFactors {
    home: {
        /** Effective field goal percentage */
        efg_pct: number;
        /** Turnover percentage */
        tov_pct: number;
        /** Offensive rebound percentage */
        oreb_pct: number;
        /** Free throw rate */
        ft_rate: number;
    };
    away: {
        efg_pct: number;
        tov_pct: number;
        oreb_pct: number;
        ft_rate: number;
    };
    /** Composite score for home team */
    homeComposite: number;
    /** Composite score for away team */
    awayComposite: number;
}
/**
 * Edge analysis vs market odds
 */
interface EdgeAnalysis {
    /** Whether market odds are available */
    hasOdds: boolean;
    /** Edge on home moneyline (positive = value) */
    homeEdge: number;
    /** Edge on away moneyline */
    awayEdge: number;
    /** Home bet is value */
    homeIsValue: boolean;
    /** Away bet is value */
    awayIsValue: boolean;
    /** Edge on spread bet */
    spreadEdge: number;
    /** Edge on total (over/under) */
    totalEdge?: number;
    /** Kelly fraction for home bet */
    homeKelly?: number;
    /** Kelly fraction for away bet */
    awayKelly?: number;
}
/**
 * Human-readable betting insights
 */
interface BettingInsights {
    /** Fair home moneyline (American odds) */
    fairHomeMoneyline: number;
    /** Fair away moneyline */
    fairAwayMoneyline: number;
    /** Fair spread */
    fairSpread: number;
    /** Fair total */
    fairTotal: number;
    /** Summary bullet points */
    summary: string[];
}
/**
 * Histogram bucket for score distribution
 */
interface HistogramBucket {
    /** Range label (e.g., "100-104") */
    label: string;
    /** Number of simulations in this bucket */
    count: number;
    /** Percentage of total */
    pct: number;
}
/**
 * Distribution statistics
 */
interface DistributionStats {
    mean: number;
    std: number;
    min: number;
    max: number;
    median: number;
    histogram: HistogramBucket[];
}
/**
 * Score distribution from Monte Carlo simulations
 */
interface ScoreDistribution {
    homeScores: DistributionStats;
    awayScores: DistributionStats;
    totals: DistributionStats;
    spreads: DistributionStats;
}
/**
 * Factor impact analysis
 */
interface FactorBreakdown {
    /** Factor name */
    name: string;
    /** Direction of impact: home, away, or neutral */
    direction: 'home' | 'away' | 'neutral' | 'total';
    /** Point impact */
    impact: number;
    /** Category: critical, high, medium, contextual */
    category: 'critical' | 'high' | 'medium' | 'contextual';
    /** Human-readable explanation */
    explanation: string;
}
/**
 * Full simulation result
 */
interface SimulationResult {
    /** Game identifier */
    gameId: string;
    /** Number of Monte Carlo iterations */
    simulationCount: number;
    homeTeamName: string;
    awayTeamName: string;
    homeTeamAbbr: string;
    awayTeamAbbr: string;
    /** Home win probability (0-1) */
    homeWinProbability: number;
    /** Away win probability (0-1) */
    awayWinProbability: number;
    /** Average projected home score */
    averageHomeScore: number;
    /** Average projected away score */
    averageAwayScore: number;
    /** Average projected total points */
    averageTotalPoints: number;
    /** Predicted spread (positive = away favored) */
    predictedSpread: number;
    /** Standard deviation of spread */
    spreadStdDev?: number;
    /** Standard deviation of total */
    totalStdDev?: number;
    /** Probability of overtime */
    overtimeProbability?: number;
    elo?: EloRatings;
    fourFactors?: FourFactors;
    edgeAnalysis?: EdgeAnalysis;
    bettingInsights?: BettingInsights;
    scoreDistribution?: ScoreDistribution;
    factorBreakdown?: FactorBreakdown[];
}
/**
 * Simulation job status
 */
type JobStatus = 'processing' | 'complete' | 'error';
/**
 * Simulation job response (for polling)
 */
interface SimulationJob {
    /** Unique job identifier */
    jobId: string;
    /** Current status */
    status: JobStatus;
    /** URL to poll for results */
    pollUrl: string;
    /** Simulation result (when complete) */
    result?: SimulationResult;
    /** Error message (when error) */
    error?: string;
    /** Estimated completion time in seconds */
    estimatedTime?: number;
}
/**
 * Options for simulate() method
 */
interface SimulateOptions {
    /** Number of Monte Carlo iterations (default: 10000) */
    count?: number;
    /** Auto-poll until complete (default: true) */
    autoPoll?: boolean;
    /** Callback for status updates during polling */
    onStatus?: (status: string, job?: SimulationJob) => void;
    /** Polling interval in ms (default: 3000) */
    pollingInterval?: number;
    /** Polling timeout in ms (default: 120000) */
    pollingTimeout?: number;
}

/**
 * Wallet adapter interface for signing transactions
 * Compatible with @solana/wallet-adapter-base
 */
interface WalletAdapter {
    /** Wallet public key */
    publicKey: PublicKey;
    /** Sign a single transaction */
    signTransaction<T extends Transaction | VersionedTransaction>(transaction: T): Promise<T>;
    /** Sign multiple transactions (optional) */
    signAllTransactions?<T extends Transaction | VersionedTransaction>(transactions: T[]): Promise<T[]>;
}
/**
 * SDK configuration options
 */
interface EdgeBetsConfig {
    /**
     * Solana wallet for signing payments
     * Can be a Keypair or a wallet adapter
     */
    wallet?: WalletAdapter | Keypair;
    /**
     * Solana RPC endpoint
     * @default "https://api.mainnet-beta.solana.com"
     */
    rpcEndpoint?: string;
    /**
     * EdgeBets API base URL
     * @default "https://api.edgebets.fun/api/v1"
     */
    apiBaseUrl?: string;
    /**
     * Polling interval for simulation results (ms)
     * @default 3000
     */
    pollingInterval?: number;
    /**
     * Polling timeout (ms)
     * @default 120000
     */
    pollingTimeout?: number;
    /**
     * Enable debug logging
     * @default false
     */
    debug?: boolean;
    /**
     * Maximum concurrent simulations
     * @default 1
     */
    maxConcurrent?: number;
    /**
     * Minimum delay between requests in ms
     * @default 2000
     */
    delayBetween?: number;
}
/**
 * Balance check result
 */
interface BalanceResult {
    /** USDC balance in human-readable units */
    usdc: number;
    /** SOL balance for transaction fees */
    sol: number;
    /** Whether balance is sufficient for a simulation ($0.50) */
    sufficient: boolean;
}

/**
 * Pick of the day data
 */
interface DailyPick {
    /** Pick date (YYYY-MM-DD) */
    date: string;
    /** Sport (nba, nfl, mlb, mls) */
    sport: string;
    /** Game ID */
    gameId: string;
    /** Home team name */
    homeTeam: string;
    /** Away team name */
    awayTeam: string;
    /** Pick type: moneyline, spread, or total */
    pickType: 'moneyline' | 'spread' | 'total';
    /** The actual pick (team name for ML/spread, "over"/"under" for total) */
    pick: string;
    /** Pick value (spread points or total line) */
    pickValue?: number;
    /** Odds for the pick (American format) */
    odds?: number;
    /** Win probability from simulation */
    winProbability: number;
    /** Edge vs market */
    edge?: number;
    /** Confidence level */
    confidence: 'high' | 'medium' | 'low';
    /** Brief analysis */
    analysis?: string;
    /** Game start time */
    gameTime?: string;
    /** Result after game: win, loss, push, or pending */
    result?: 'win' | 'loss' | 'push' | 'pending';
    /** Actual final score */
    finalScore?: string;
}
/**
 * Response from getTodaysPick()
 */
interface TodaysPickResponse {
    /** Whether a pick is available */
    hasPick: boolean;
    /** Whether this is today's pick (vs yesterday's) */
    isTodaysPick?: boolean;
    /** The pick data */
    pick?: DailyPick;
    /** Status message */
    message?: string;
    /** When the next pick will be available */
    nextPickTime?: string;
}
/**
 * Track record statistics
 */
interface TrackRecord {
    /** Total wins */
    wins: number;
    /** Total losses */
    losses: number;
    /** Total pushes */
    pushes: number;
    /** Total picks made */
    totalPicks: number;
    /** Win rate percentage */
    winRate: number;
    /** Current streak (positive = wins, negative = losses) */
    streak: number;
    /** Streak type: "W" or "L" */
    streakType: 'W' | 'L';
    /** Recent picks */
    recentPicks: DailyPick[];
}

/**
 * EdgeBets SDK Client
 *
 * Main entry point for interacting with the EdgeBets API.
 * Handles games fetching, payments, and simulations.
 *
 * @example
 * ```typescript
 * import { EdgeBetsClient } from '@edgebets/sdk';
 * import { Keypair } from '@solana/web3.js';
 *
 * const client = new EdgeBetsClient({
 *   wallet: Keypair.fromSecretKey(...),
 *   debug: true,
 * });
 *
 * // Get today's NBA games (FREE)
 * const games = await client.getGames('nba');
 *
 * // Run simulation ($0.50 USDC)
 * const result = await client.simulate('nba', games[0].id);
 * ```
 */
declare class EdgeBetsClient {
    private config;
    private gamesService;
    private paymentService;
    private simulationService;
    private picksService;
    private simulationQueue;
    constructor(config?: EdgeBetsConfig);
    /**
     * Resolve configuration with defaults
     */
    private resolveConfig;
    /**
     * Get today's games for a sport
     *
     * @param sport - The sport to get games for ('nba', 'nfl', 'mlb', 'mls')
     * @returns Array of games
     *
     * @example
     * ```typescript
     * const games = await client.getGames('nba');
     * console.log(`Found ${games.length} NBA games today`);
     * ```
     */
    getGames(sport: Sport): Promise<Game[]>;
    /**
     * Get tomorrow's games for a sport
     *
     * @param sport - The sport to get games for
     * @returns Array of games
     */
    getTomorrowGames(sport: Sport): Promise<Game[]>;
    /**
     * Get details for a specific game
     *
     * @param sport - The sport
     * @param gameId - Game identifier
     * @returns Game details
     */
    getGameDetails(sport: Sport, gameId: string): Promise<Game>;
    /**
     * Run a Monte Carlo simulation for a game
     *
     * This method handles the full x402 payment flow:
     * 1. Sends USDC payment to treasury
     * 2. Starts simulation with payment proof
     * 3. Polls until complete
     * 4. Returns result
     *
     * Rate limited to prevent overwhelming the API.
     * Default: 1 concurrent request, 2s delay between requests.
     *
     * @param sport - The sport ('nba', 'nfl', 'mlb', 'mls')
     * @param gameId - Game identifier
     * @param options - Simulation options
     * @returns Simulation result
     *
     * @example
     * ```typescript
     * const result = await client.simulate('nba', 'nba-2026-03-28-lal-bos', {
     *   onStatus: (status) => console.log(`Status: ${status}`),
     * });
     *
     * console.log(`Home win: ${(result.homeWinProbability * 100).toFixed(1)}%`);
     * console.log(`Total: ${result.averageTotalPoints.toFixed(1)}`);
     * ```
     */
    simulate(sport: Sport, gameId: string, options?: SimulateOptions): Promise<SimulationResult>;
    /**
     * Get current queue status
     *
     * @returns Object with queued and running counts
     */
    getQueueStatus(): {
        queued: number;
        running: number;
    };
    /**
     * Start a simulation and get job for manual polling
     * (Advanced use case - prefer simulate() for most cases)
     *
     * @param sport - The sport
     * @param gameId - Game identifier
     * @returns Simulation job with polling URL
     */
    startSimulation(sport: Sport, gameId: string): Promise<SimulationJob>;
    /**
     * Poll for simulation result
     *
     * @param jobId - Job identifier from startSimulation
     * @returns Simulation job with current status
     */
    pollResult(jobId: string): Promise<SimulationJob>;
    /**
     * Get today's pick of the day (FREE)
     *
     * Returns the daily expert pick with analysis.
     * If the game has been played, indicates when the next pick will be available.
     *
     * @returns Today's pick response
     *
     * @example
     * ```typescript
     * const pick = await client.getTodaysPick();
     * if (pick.hasPick) {
     *   console.log(`Today's pick: ${pick.pick.pick} (${pick.pick.confidence})`);
     *   console.log(`Win probability: ${(pick.pick.winProbability * 100).toFixed(1)}%`);
     * } else {
     *   console.log(pick.message);  // "New pick available at 2 AM Central"
     * }
     * ```
     */
    getTodaysPick(): Promise<TodaysPickResponse>;
    /**
     * Get track record and recent picks (FREE)
     *
     * @param limit - Number of recent picks to include (default 30)
     * @returns Track record statistics
     *
     * @example
     * ```typescript
     * const record = await client.getTrackRecord();
     * console.log(`Record: ${record.wins}-${record.losses}`);
     * console.log(`Win rate: ${record.winRate}%`);
     * console.log(`Current streak: ${record.streak}${record.streakType}`);
     * ```
     */
    getTrackRecord(limit?: number): Promise<TrackRecord>;
    /**
     * Check wallet balance (USDC and SOL)
     *
     * @returns Balance information
     *
     * @example
     * ```typescript
     * const balance = await client.checkBalance();
     * console.log(`USDC: ${balance.usdc}`);
     * console.log(`SOL: ${balance.sol}`);
     * console.log(`Can simulate: ${balance.sufficient}`);
     * ```
     */
    checkBalance(): Promise<BalanceResult>;
    /**
     * Get simulation price quote
     *
     * @returns Price information
     */
    getQuote(): Promise<{
        price: number;
        currency: string;
        network: string;
        recipient: string;
    }>;
    /**
     * Check if wallet is configured
     */
    hasWallet(): boolean;
    /**
     * Get treasury wallet address
     */
    getTreasuryWallet(): string;
    /**
     * Get simulation price in USDC
     */
    getPrice(): number;
}
/**
 * Create an EdgeBets client from a secret key
 *
 * @param secretKey - Solana wallet secret key (Uint8Array or number array)
 * @param config - Additional configuration
 * @returns Configured EdgeBets client
 *
 * @example
 * ```typescript
 * import { createClient } from '@edgebets/sdk';
 * import fs from 'fs';
 *
 * const secretKey = JSON.parse(fs.readFileSync('~/.config/solana/id.json', 'utf-8'));
 * const client = createClient(secretKey, { debug: true });
 * ```
 */
declare function createClient(secretKey: Uint8Array | number[], config?: Omit<EdgeBetsConfig, 'wallet'>): EdgeBetsClient;

/**
 * Base error class for EdgeBets SDK
 */
declare class EdgeBetsError extends Error {
    code: string;
    statusCode?: number | undefined;
    details?: Record<string, unknown> | undefined;
    constructor(message: string, code: string, statusCode?: number | undefined, details?: Record<string, unknown> | undefined);
}
/**
 * Payment required error (402)
 */
declare class PaymentRequiredError extends EdgeBetsError {
    paymentInfo: {
        amount: number;
        recipient: string;
        currency: string;
        network: string;
    };
    constructor(paymentInfo: {
        amount: number;
        recipient: string;
        currency: string;
        network: string;
    });
}
/**
 * Insufficient balance error
 */
declare class InsufficientBalanceError extends EdgeBetsError {
    required: number;
    available: number;
    constructor(required: number, available: number);
}
/**
 * Wallet not configured error
 */
declare class WalletNotConfiguredError extends EdgeBetsError {
    constructor();
}
/**
 * Polling timeout error
 */
declare class PollingTimeoutError extends EdgeBetsError {
    constructor(jobId: string, timeout: number);
}
/**
 * Simulation failed error
 */
declare class SimulationFailedError extends EdgeBetsError {
    constructor(jobId: string, reason?: string);
}
/**
 * API error (non-402 HTTP errors)
 */
declare class ApiError extends EdgeBetsError {
    constructor(message: string, statusCode: number, details?: Record<string, unknown>);
}
/**
 * Network/connection error
 */
declare class NetworkError extends EdgeBetsError {
    constructor(message: string, cause?: Error);
}

/**
 * EdgeBets API base URL
 */
declare const EDGEBETS_API_URL = "https://api.edgebets.fun/api/v1";
/**
 * Treasury wallet for receiving payments
 */
declare const TREASURY_WALLET = "DuDLnnPzzRo8Yi9AKFEE7rsESVyTzQVPgC6h3FXYaDB4";
/**
 * USDC token mint on Solana mainnet
 */
declare const USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v";
/**
 * Price per simulation in USDC (human-readable)
 */
declare const PRICE_USDC = 0.5;
/**
 * Price per simulation in raw USDC units (with 6 decimals)
 */
declare const PRICE_USDC_RAW = 500000;

export { ApiError, type BalanceResult, type BettingInsights, type DailyPick, type DistributionStats, EDGEBETS_API_URL, type EdgeAnalysis, EdgeBetsClient, type EdgeBetsConfig, EdgeBetsError, type EloRatings, type FactorBreakdown, type FourFactors, type Game, type GameOdds, type GameStatus, type GamesResponse, type HistogramBucket, InsufficientBalanceError, type JobStatus, NetworkError, PRICE_USDC, PRICE_USDC_RAW, PaymentRequiredError, PollingTimeoutError, type ScoreDistribution, type SimulateOptions, SimulationFailedError, type SimulationJob, type SimulationResult, type Sport, TREASURY_WALLET, type Team, type TodaysPickResponse, type TrackRecord, USDC_MINT, type WalletAdapter, WalletNotConfiguredError, createClient };
