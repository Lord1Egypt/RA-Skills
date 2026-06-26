"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/index.ts
var index_exports = {};
__export(index_exports, {
  ApiError: () => ApiError,
  EDGEBETS_API_URL: () => EDGEBETS_API_URL,
  EdgeBetsClient: () => EdgeBetsClient,
  EdgeBetsError: () => EdgeBetsError,
  InsufficientBalanceError: () => InsufficientBalanceError,
  NetworkError: () => NetworkError,
  PRICE_USDC: () => PRICE_USDC,
  PRICE_USDC_RAW: () => PRICE_USDC_RAW,
  PaymentRequiredError: () => PaymentRequiredError,
  PollingTimeoutError: () => PollingTimeoutError,
  SimulationFailedError: () => SimulationFailedError,
  TREASURY_WALLET: () => TREASURY_WALLET,
  USDC_MINT: () => USDC_MINT,
  WalletNotConfiguredError: () => WalletNotConfiguredError,
  createClient: () => createClient
});
module.exports = __toCommonJS(index_exports);

// src/client.ts
var import_web32 = require("@solana/web3.js");

// src/constants.ts
var EDGEBETS_API_URL = "https://api.edgebets.fun/api/v1";
var TREASURY_WALLET = "DuDLnnPzzRo8Yi9AKFEE7rsESVyTzQVPgC6h3FXYaDB4";
var USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v";
var USDC_DECIMALS = 6;
var PRICE_USDC = 0.5;
var PRICE_USDC_RAW = 5e5;
var DEFAULT_RPC_ENDPOINT = "https://api.mainnet-beta.solana.com";
var DEFAULT_POLLING_INTERVAL = 3e3;
var DEFAULT_POLLING_TIMEOUT = 12e4;
var DEFAULT_SIMULATION_COUNT = 1e4;
var GAMES_ENDPOINTS = {
  nba: "games/basketball",
  nfl: "games/football",
  mlb: "games/baseball",
  mls: "games/soccer"
};
var SIMULATION_ENDPOINTS = {
  nba: "x402/simulate/nba",
  nfl: "x402/simulate/nfl",
  mlb: "x402/simulate/mlb",
  mls: "x402/simulate/mls"
};
var X402_VERSION = 1;
var SOLANA_NETWORK = "solana-mainnet";

// src/utils/errors.ts
var EdgeBetsError = class _EdgeBetsError extends Error {
  constructor(message, code, statusCode, details) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
    this.name = "EdgeBetsError";
    Object.setPrototypeOf(this, _EdgeBetsError.prototype);
  }
};
var PaymentRequiredError = class _PaymentRequiredError extends EdgeBetsError {
  constructor(paymentInfo) {
    super(
      `Payment required: ${paymentInfo.amount / 1e6} ${paymentInfo.currency}`,
      "PAYMENT_REQUIRED",
      402,
      paymentInfo
    );
    this.paymentInfo = paymentInfo;
    this.name = "PaymentRequiredError";
    Object.setPrototypeOf(this, _PaymentRequiredError.prototype);
  }
};
var InsufficientBalanceError = class _InsufficientBalanceError extends EdgeBetsError {
  constructor(required, available) {
    super(
      `Insufficient USDC balance: required ${required}, available ${available}`,
      "INSUFFICIENT_BALANCE",
      void 0,
      { required, available }
    );
    this.required = required;
    this.available = available;
    this.name = "InsufficientBalanceError";
    Object.setPrototypeOf(this, _InsufficientBalanceError.prototype);
  }
};
var WalletNotConfiguredError = class _WalletNotConfiguredError extends EdgeBetsError {
  constructor() {
    super(
      "Wallet not configured. Pass a wallet to EdgeBetsClient constructor.",
      "WALLET_NOT_CONFIGURED"
    );
    this.name = "WalletNotConfiguredError";
    Object.setPrototypeOf(this, _WalletNotConfiguredError.prototype);
  }
};
var PollingTimeoutError = class _PollingTimeoutError extends EdgeBetsError {
  constructor(jobId, timeout) {
    super(
      `Simulation polling timed out after ${timeout}ms`,
      "POLLING_TIMEOUT",
      void 0,
      { jobId, timeout }
    );
    this.name = "PollingTimeoutError";
    Object.setPrototypeOf(this, _PollingTimeoutError.prototype);
  }
};
var SimulationFailedError = class _SimulationFailedError extends EdgeBetsError {
  constructor(jobId, reason) {
    super(
      reason || "Simulation failed",
      "SIMULATION_FAILED",
      void 0,
      { jobId, reason }
    );
    this.name = "SimulationFailedError";
    Object.setPrototypeOf(this, _SimulationFailedError.prototype);
  }
};
var ApiError = class _ApiError extends EdgeBetsError {
  constructor(message, statusCode, details) {
    super(message, "API_ERROR", statusCode, details);
    this.name = "ApiError";
    Object.setPrototypeOf(this, _ApiError.prototype);
  }
};
var NetworkError = class _NetworkError extends EdgeBetsError {
  constructor(message, cause) {
    super(message, "NETWORK_ERROR", void 0, { cause: cause?.message });
    this.name = "NetworkError";
    Object.setPrototypeOf(this, _NetworkError.prototype);
  }
};

// src/services/games.ts
var GamesService = class {
  constructor(config) {
    this.config = config;
  }
  /**
   * Get today's games for a sport
   */
  async getGames(sport) {
    const endpoint = GAMES_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/today`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
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
      const games = Array.isArray(data) ? data : data.games || [];
      return this.normalizeGames(games, sport);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        `Failed to fetch ${sport.toUpperCase()} games`,
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Get tomorrow's games for a sport
   */
  async getTomorrowGames(sport) {
    const endpoint = GAMES_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/tomorrow`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
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
      const games = Array.isArray(data) ? data : data.games || [];
      return this.normalizeGames(games, sport);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        `Failed to fetch ${sport.toUpperCase()} games`,
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Get details for a specific game
   */
  async getGameDetails(sport, gameId) {
    const endpoint = GAMES_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/${gameId}`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
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
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Normalize games array from API response
   */
  normalizeGames(games, sport) {
    return games.map((game) => this.normalizeGame(game, sport));
  }
  /**
   * Normalize a single game from API response
   */
  normalizeGame(game, sport) {
    const g = game;
    return {
      id: String(g.id || g.gameId || g.game_id || ""),
      sport,
      homeTeam: {
        name: String(g.homeTeam || g.home_team || g.home?.name || ""),
        abbreviation: String(g.homeTeamAbbr || g.home_abbr || g.home?.abbreviation || ""),
        logoUrl: g.homeTeamLogo
      },
      awayTeam: {
        name: String(g.awayTeam || g.away_team || g.away?.name || ""),
        abbreviation: String(g.awayTeamAbbr || g.away_abbr || g.away?.abbreviation || ""),
        logoUrl: g.awayTeamLogo
      },
      startTime: String(g.startTime || g.start_time || g.gameTime || ""),
      status: this.normalizeStatus(g.status),
      venue: g.venue,
      homeScore: typeof g.homeScore === "number" ? g.homeScore : void 0,
      awayScore: typeof g.awayScore === "number" ? g.awayScore : void 0,
      odds: g.odds ? this.normalizeOdds(g.odds) : void 0
    };
  }
  /**
   * Normalize game status
   */
  normalizeStatus(status) {
    const s = String(status).toLowerCase();
    if (s.includes("progress") || s.includes("live")) return "in_progress";
    if (s.includes("final") || s.includes("completed")) return "final";
    if (s.includes("postponed")) return "postponed";
    if (s.includes("cancelled") || s.includes("canceled")) return "cancelled";
    return "scheduled";
  }
  /**
   * Normalize odds object
   */
  normalizeOdds(odds) {
    return {
      homeMoneyline: typeof odds.homeMoneyline === "number" ? odds.homeMoneyline : void 0,
      awayMoneyline: typeof odds.awayMoneyline === "number" ? odds.awayMoneyline : void 0,
      spread: typeof odds.spread === "number" ? odds.spread : void 0,
      total: typeof odds.total === "number" ? odds.total : void 0,
      overOdds: typeof odds.overOdds === "number" ? odds.overOdds : void 0,
      underOdds: typeof odds.underOdds === "number" ? odds.underOdds : void 0
    };
  }
};

// src/services/payment.ts
var import_web3 = require("@solana/web3.js");
var import_spl_token = require("@solana/spl-token");
var PaymentService = class {
  constructor(config) {
    this.config = config;
    this.connection = new import_web3.Connection(config.rpcEndpoint, "confirmed");
    this.usdcMint = new import_web3.PublicKey(USDC_MINT);
    this.treasuryWallet = new import_web3.PublicKey(TREASURY_WALLET);
  }
  /**
   * Check if a wallet is configured
   */
  hasWallet() {
    return this.config.wallet !== null;
  }
  /**
   * Get the public key of the configured wallet
   */
  getPublicKey() {
    if (!this.config.wallet) {
      throw new WalletNotConfiguredError();
    }
    if ("publicKey" in this.config.wallet && this.config.wallet.publicKey instanceof import_web3.PublicKey) {
      return this.config.wallet.publicKey;
    }
    return this.config.wallet.publicKey;
  }
  /**
   * Check USDC and SOL balance
   */
  async checkBalance() {
    const publicKey = this.getPublicKey();
    try {
      const solBalance = await this.connection.getBalance(publicKey);
      const sol = solBalance / 1e9;
      const usdcAta = await (0, import_spl_token.getAssociatedTokenAddress)(this.usdcMint, publicKey);
      let usdc = 0;
      try {
        const tokenAccount = await (0, import_spl_token.getAccount)(this.connection, usdcAta);
        usdc = Number(tokenAccount.amount) / Math.pow(10, USDC_DECIMALS);
      } catch {
        usdc = 0;
      }
      return {
        usdc,
        sol,
        sufficient: usdc >= PRICE_USDC
      };
    } catch (error) {
      throw new NetworkError(
        "Failed to check balance",
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Send USDC payment to treasury
   * Returns the transaction signature
   */
  async sendPayment() {
    if (!this.config.wallet) {
      throw new WalletNotConfiguredError();
    }
    const publicKey = this.getPublicKey();
    const balance = await this.checkBalance();
    if (!balance.sufficient) {
      throw new InsufficientBalanceError(PRICE_USDC, balance.usdc);
    }
    try {
      const senderAta = await (0, import_spl_token.getAssociatedTokenAddress)(this.usdcMint, publicKey);
      const recipientAta = await (0, import_spl_token.getAssociatedTokenAddress)(this.usdcMint, this.treasuryWallet);
      const transferInstruction = (0, import_spl_token.createTransferInstruction)(
        senderAta,
        recipientAta,
        publicKey,
        BigInt(PRICE_USDC_RAW),
        [],
        import_spl_token.TOKEN_PROGRAM_ID
      );
      const transaction = new import_web3.Transaction().add(transferInstruction);
      const { blockhash, lastValidBlockHeight } = await this.connection.getLatestBlockhash();
      transaction.recentBlockhash = blockhash;
      transaction.feePayer = publicKey;
      let signature;
      if (this.config.wallet instanceof import_web3.Keypair) {
        signature = await (0, import_web3.sendAndConfirmTransaction)(
          this.connection,
          transaction,
          [this.config.wallet]
        );
      } else {
        const wallet = this.config.wallet;
        const signedTx = await wallet.signTransaction(transaction);
        signature = await this.connection.sendRawTransaction(signedTx.serialize());
        await this.connection.confirmTransaction({
          signature,
          blockhash,
          lastValidBlockHeight
        });
      }
      if (this.config.debug) {
        console.log(`[EdgeBets] Payment sent: ${signature}`);
      }
      return signature;
    } catch (error) {
      throw new NetworkError(
        "Failed to send USDC payment",
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Build x402 payment proof header value
   */
  buildPaymentProof(signature) {
    const proof = {
      x402Version: X402_VERSION,
      network: SOLANA_NETWORK,
      payload: {
        signature,
        payer: this.getPublicKey().toBase58()
      }
    };
    return Buffer.from(JSON.stringify(proof)).toString("base64");
  }
  /**
   * Get the treasury wallet address
   */
  getTreasuryWallet() {
    return TREASURY_WALLET;
  }
  /**
   * Get the simulation price in USDC
   */
  getPrice() {
    return PRICE_USDC;
  }
};

// src/utils/polling.ts
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
async function pollUntilComplete(pollFn, options) {
  const { interval, timeout, onStatus } = options;
  const startTime = Date.now();
  let lastJob;
  while (Date.now() - startTime < timeout) {
    try {
      const job = await pollFn();
      lastJob = job;
      if (onStatus) {
        onStatus(job.status, job);
      }
      if (job.status === "complete") {
        return job;
      }
      if (job.status === "error") {
        throw new SimulationFailedError(job.jobId, job.error);
      }
      await sleep(interval);
    } catch (error) {
      if (error instanceof SimulationFailedError) {
        throw error;
      }
      if (onStatus) {
        onStatus("retrying", lastJob);
      }
      await sleep(interval);
    }
  }
  throw new PollingTimeoutError(lastJob?.jobId || "unknown", timeout);
}

// src/services/simulation.ts
var SimulationService = class {
  constructor(config, paymentService) {
    this.config = config;
    this.paymentService = paymentService;
  }
  /**
   * Run a full simulation with automatic payment handling
   *
   * Flow:
   * 1. Request simulation → receive 402
   * 2. Send USDC payment → get signature
   * 3. Retry with X-Payment header → get job_id
   * 4. Poll until complete → return result
   */
  async simulate(sport, gameId, options = {}) {
    const {
      count = DEFAULT_SIMULATION_COUNT,
      autoPoll = true,
      onStatus,
      pollingInterval = this.config.pollingInterval,
      pollingTimeout = this.config.pollingTimeout
    } = options;
    if (this.config.debug) {
      console.log(`[EdgeBets] Starting simulation for ${sport}/${gameId}`);
    }
    if (onStatus) onStatus("requesting");
    if (onStatus) onStatus("paying");
    const signature = await this.paymentService.sendPayment();
    if (this.config.debug) {
      console.log(`[EdgeBets] Payment confirmed: ${signature}`);
    }
    if (onStatus) onStatus("starting");
    const job = await this.startSimulationWithPayment(sport, gameId, signature, count);
    if (this.config.debug) {
      console.log(`[EdgeBets] Simulation started: ${job.jobId}`);
    }
    if (!autoPoll) {
      if (job.result) {
        return job.result;
      }
      throw new SimulationFailedError(job.jobId, "Auto-poll disabled and no immediate result");
    }
    if (onStatus) onStatus("processing", job);
    const completedJob = await pollUntilComplete(
      () => this.pollResult(job.jobId),
      {
        interval: pollingInterval,
        timeout: pollingTimeout,
        onStatus: (status, j) => {
          if (this.config.debug) {
            console.log(`[EdgeBets] Poll status: ${status}`);
          }
          if (onStatus) onStatus(status, j);
        }
      }
    );
    if (!completedJob.result) {
      throw new SimulationFailedError(job.jobId, "Simulation completed but no result returned");
    }
    if (this.config.debug) {
      console.log(`[EdgeBets] Simulation complete!`);
    }
    return completedJob.result;
  }
  /**
   * Start a simulation with payment proof
   * Returns job for manual polling
   */
  async startSimulationWithPayment(sport, gameId, paymentSignature, count = DEFAULT_SIMULATION_COUNT) {
    const endpoint = SIMULATION_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/${gameId}`;
    const paymentProof = this.paymentService.buildPaymentProof(paymentSignature);
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Payment": paymentProof
        },
        body: JSON.stringify({ count })
      });
      if (response.status === 402) {
        const data2 = await response.json();
        throw new PaymentRequiredError({
          amount: data2.accepts?.[0]?.amount || 5e5,
          recipient: data2.accepts?.[0]?.recipient || "",
          currency: "USDC",
          network: "solana-mainnet"
        });
      }
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Simulation request failed: ${response.status}`,
          response.status,
          errorData
        );
      }
      const data = await response.json();
      return this.normalizeJobResponse(data);
    } catch (error) {
      if (error instanceof ApiError || error instanceof PaymentRequiredError) {
        throw error;
      }
      throw new NetworkError(
        "Failed to start simulation",
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Poll for simulation result
   */
  async pollResult(jobId) {
    const url = `${this.config.apiBaseUrl}/x402/result/${jobId}`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Poll request failed: ${response.status}`,
          response.status,
          errorData
        );
      }
      const data = await response.json();
      return this.normalizeJobResponse(data);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        `Failed to poll result for job ${jobId}`,
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Get x402 quote/requirements
   */
  async getQuote() {
    const url = `${this.config.apiBaseUrl}/x402/quote`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
      const data = await response.json();
      return {
        price: (data.accepts?.[0]?.amount || 5e5) / 1e6,
        currency: "USDC",
        network: "solana-mainnet",
        recipient: data.accepts?.[0]?.recipient || this.paymentService.getTreasuryWallet()
      };
    } catch (error) {
      throw new NetworkError(
        "Failed to get quote",
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Normalize job response from API
   */
  normalizeJobResponse(data) {
    const status = this.normalizeJobStatus(data.status || data.complete);
    const result = data.simulation;
    return {
      jobId: String(data.job_id || data.jobId || ""),
      status,
      pollUrl: String(data.poll_url || data.pollUrl || ""),
      error: data.error,
      estimatedTime: typeof data.estimated_time === "number" ? data.estimated_time : void 0,
      result: status === "complete" && result ? this.normalizeSimulationResult(result) : void 0
    };
  }
  /**
   * Normalize job status
   */
  normalizeJobStatus(status) {
    if (status === true || status === "complete" || status === "completed") {
      return "complete";
    }
    if (status === "error" || status === "failed") {
      return "error";
    }
    return "processing";
  }
  /**
   * Normalize simulation result from API
   */
  normalizeSimulationResult(data) {
    return {
      gameId: String(data.gameId || data.game_id || ""),
      simulationCount: Number(data.simulationCount || data.simulation_count || 1e4),
      homeTeamName: String(data.homeTeamName || data.home_team_name || ""),
      awayTeamName: String(data.awayTeamName || data.away_team_name || ""),
      homeTeamAbbr: String(data.homeTeamAbbr || data.home_team_abbr || ""),
      awayTeamAbbr: String(data.awayTeamAbbr || data.away_team_abbr || ""),
      homeWinProbability: Number(data.homeWinProbability || data.home_win_probability || 0),
      awayWinProbability: Number(data.awayWinProbability || data.away_win_probability || 0),
      averageHomeScore: Number(data.averageHomeScore || data.average_home_score || 0),
      averageAwayScore: Number(data.averageAwayScore || data.average_away_score || 0),
      averageTotalPoints: Number(data.averageTotalPoints || data.average_total_points || 0),
      predictedSpread: Number(data.predictedSpread || data.predicted_spread || 0),
      spreadStdDev: data.spreadStdDev,
      totalStdDev: data.totalStdDev,
      overtimeProbability: data.overtimeProbability,
      elo: data.elo,
      fourFactors: data.fourFactors,
      edgeAnalysis: data.edgeAnalysis,
      bettingInsights: data.bettingInsights,
      scoreDistribution: data.scoreDistribution,
      factorBreakdown: data.factorBreakdown
    };
  }
};

// src/services/picks.ts
var PicksService = class {
  constructor(config) {
    this.config = config;
  }
  /**
   * Get today's pick of the day (FREE)
   *
   * If the game has already been played, suggests checking back at 2 AM Central.
   */
  async getTodaysPick() {
    const url = `${this.config.apiBaseUrl}/picks/today`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Failed to fetch pick: ${response.status}`,
          response.status,
          errorData
        );
      }
      const data = await response.json();
      return this.normalizePickResponse(data);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        "Failed to fetch today's pick",
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Get track record and recent picks (FREE)
   */
  async getTrackRecord(limit = 30) {
    const url = `${this.config.apiBaseUrl}/picks/track-record?limit=${limit}`;
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Failed to fetch track record: ${response.status}`,
          response.status,
          errorData
        );
      }
      const data = await response.json();
      return this.normalizeTrackRecord(data);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(
        "Failed to fetch track record",
        error instanceof Error ? error : void 0
      );
    }
  }
  /**
   * Normalize pick response from API
   */
  normalizePickResponse(data) {
    const hasPick = Boolean(data.has_pick);
    const isTodaysPick = Boolean(data.is_todays_pick);
    const pick = data.pick ? this.normalizePick(data.pick) : void 0;
    let message = data.message;
    let nextPickTime;
    if (pick && pick.result && pick.result !== "pending") {
      message = `Today's pick (${pick.pick}) has already been graded: ${pick.result.toUpperCase()}. New pick available at 2 AM Central.`;
      nextPickTime = "2:00 AM Central";
    } else if (!isTodaysPick && hasPick) {
      message = message || "Showing yesterday's pick. New pick available at 2 AM Central.";
      nextPickTime = "2:00 AM Central";
    }
    return {
      hasPick,
      isTodaysPick,
      pick,
      message,
      nextPickTime
    };
  }
  /**
   * Normalize a single pick
   */
  normalizePick(data) {
    return {
      date: String(data.date || ""),
      sport: String(data.sport || ""),
      gameId: String(data.game_id || data.gameId || ""),
      homeTeam: String(data.home_team || data.homeTeam || ""),
      awayTeam: String(data.away_team || data.awayTeam || ""),
      pickType: data.pick_type || data.pickType || "moneyline",
      pick: String(data.pick || ""),
      pickValue: typeof data.pick_value === "number" ? data.pick_value : void 0,
      odds: typeof data.odds === "number" ? data.odds : void 0,
      winProbability: Number(data.win_probability || data.winProbability || 0),
      edge: typeof data.edge === "number" ? data.edge : void 0,
      confidence: data.confidence || "medium",
      analysis: data.analysis,
      gameTime: data.game_time || data.gameTime,
      result: data.result,
      finalScore: data.final_score || data.finalScore
    };
  }
  /**
   * Normalize track record from API
   */
  normalizeTrackRecord(data) {
    const recentPicks = Array.isArray(data.recent_picks || data.recentPicks) ? (data.recent_picks || data.recentPicks).map(
      (p) => this.normalizePick(p)
    ) : [];
    return {
      wins: Number(data.wins || 0),
      losses: Number(data.losses || 0),
      pushes: Number(data.pushes || 0),
      totalPicks: Number(data.total_picks || data.totalPicks || 0),
      winRate: Number(data.win_rate || data.winRate || 0),
      streak: Number(data.streak || 0),
      streakType: data.streak_type || data.streakType || "W",
      recentPicks
    };
  }
};

// src/utils/queue.ts
var RequestQueue = class {
  constructor(maxConcurrent = 1, delayBetween = 2e3) {
    this.queue = [];
    this.running = 0;
    this.lastRequestTime = 0;
    this.maxConcurrent = maxConcurrent;
    this.delayBetween = delayBetween;
  }
  /**
   * Add a task to the queue and wait for its result
   */
  async add(task) {
    return new Promise((resolve, reject) => {
      const wrappedTask = async () => {
        try {
          const now = Date.now();
          const timeSinceLastRequest = now - this.lastRequestTime;
          if (timeSinceLastRequest < this.delayBetween) {
            await sleep(this.delayBetween - timeSinceLastRequest);
          }
          this.lastRequestTime = Date.now();
          const result = await task();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      };
      this.queue.push(wrappedTask);
      this.processQueue();
    });
  }
  /**
   * Process queued tasks respecting concurrency limits
   */
  async processQueue() {
    if (this.running >= this.maxConcurrent || this.queue.length === 0) {
      return;
    }
    const task = this.queue.shift();
    if (!task) return;
    this.running++;
    try {
      await task();
    } finally {
      this.running--;
      this.processQueue();
    }
  }
  /**
   * Get current queue status
   */
  getStatus() {
    return {
      queued: this.queue.length,
      running: this.running
    };
  }
};

// src/client.ts
var DEFAULT_MAX_CONCURRENT = 1;
var DEFAULT_DELAY_BETWEEN = 2e3;
var EdgeBetsClient = class {
  constructor(config = {}) {
    this.config = this.resolveConfig(config);
    this.gamesService = new GamesService(this.config);
    this.paymentService = new PaymentService(this.config);
    this.simulationService = new SimulationService(this.config, this.paymentService);
    this.picksService = new PicksService(this.config);
    this.simulationQueue = new RequestQueue(
      this.config.maxConcurrent,
      this.config.delayBetween
    );
    if (this.config.debug) {
      console.log("[EdgeBets] Client initialized");
      console.log(`[EdgeBets] API: ${this.config.apiBaseUrl}`);
      console.log(`[EdgeBets] RPC: ${this.config.rpcEndpoint}`);
      console.log(`[EdgeBets] Wallet: ${this.config.wallet ? "configured" : "not configured"}`);
      console.log(`[EdgeBets] Rate limit: ${this.config.maxConcurrent} concurrent, ${this.config.delayBetween}ms delay`);
    }
  }
  /**
   * Resolve configuration with defaults
   */
  resolveConfig(config) {
    return {
      wallet: config.wallet || null,
      rpcEndpoint: config.rpcEndpoint || DEFAULT_RPC_ENDPOINT,
      apiBaseUrl: config.apiBaseUrl || EDGEBETS_API_URL,
      pollingInterval: config.pollingInterval || DEFAULT_POLLING_INTERVAL,
      pollingTimeout: config.pollingTimeout || DEFAULT_POLLING_TIMEOUT,
      debug: config.debug || false,
      maxConcurrent: config.maxConcurrent || DEFAULT_MAX_CONCURRENT,
      delayBetween: config.delayBetween || DEFAULT_DELAY_BETWEEN
    };
  }
  // ============================================
  // GAMES (FREE - no payment required)
  // ============================================
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
  async getGames(sport) {
    return this.gamesService.getGames(sport);
  }
  /**
   * Get tomorrow's games for a sport
   *
   * @param sport - The sport to get games for
   * @returns Array of games
   */
  async getTomorrowGames(sport) {
    return this.gamesService.getTomorrowGames(sport);
  }
  /**
   * Get details for a specific game
   *
   * @param sport - The sport
   * @param gameId - Game identifier
   * @returns Game details
   */
  async getGameDetails(sport, gameId) {
    return this.gamesService.getGameDetails(sport, gameId);
  }
  // ============================================
  // SIMULATIONS (PAID - $0.50 USDC)
  // ============================================
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
  async simulate(sport, gameId, options) {
    return this.simulationQueue.add(
      () => this.simulationService.simulate(sport, gameId, options)
    );
  }
  /**
   * Get current queue status
   *
   * @returns Object with queued and running counts
   */
  getQueueStatus() {
    return this.simulationQueue.getStatus();
  }
  /**
   * Start a simulation and get job for manual polling
   * (Advanced use case - prefer simulate() for most cases)
   *
   * @param sport - The sport
   * @param gameId - Game identifier
   * @returns Simulation job with polling URL
   */
  async startSimulation(sport, gameId) {
    const signature = await this.paymentService.sendPayment();
    return this.simulationService.startSimulationWithPayment(sport, gameId, signature);
  }
  /**
   * Poll for simulation result
   *
   * @param jobId - Job identifier from startSimulation
   * @returns Simulation job with current status
   */
  async pollResult(jobId) {
    return this.simulationService.pollResult(jobId);
  }
  // ============================================
  // PICKS (FREE - no payment required)
  // ============================================
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
  async getTodaysPick() {
    return this.picksService.getTodaysPick();
  }
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
  async getTrackRecord(limit = 30) {
    return this.picksService.getTrackRecord(limit);
  }
  // ============================================
  // PAYMENTS & WALLET
  // ============================================
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
  async checkBalance() {
    return this.paymentService.checkBalance();
  }
  /**
   * Get simulation price quote
   *
   * @returns Price information
   */
  async getQuote() {
    return this.simulationService.getQuote();
  }
  /**
   * Check if wallet is configured
   */
  hasWallet() {
    return this.paymentService.hasWallet();
  }
  /**
   * Get treasury wallet address
   */
  getTreasuryWallet() {
    return this.paymentService.getTreasuryWallet();
  }
  /**
   * Get simulation price in USDC
   */
  getPrice() {
    return this.paymentService.getPrice();
  }
};
function createClient(secretKey, config = {}) {
  const keypair = import_web32.Keypair.fromSecretKey(
    secretKey instanceof Uint8Array ? secretKey : Uint8Array.from(secretKey)
  );
  return new EdgeBetsClient({ ...config, wallet: keypair });
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  ApiError,
  EDGEBETS_API_URL,
  EdgeBetsClient,
  EdgeBetsError,
  InsufficientBalanceError,
  NetworkError,
  PRICE_USDC,
  PRICE_USDC_RAW,
  PaymentRequiredError,
  PollingTimeoutError,
  SimulationFailedError,
  TREASURY_WALLET,
  USDC_MINT,
  WalletNotConfiguredError,
  createClient
});
