import type {
  Sport,
  SimulationResult,
  SimulationJob,
  SimulateOptions,
  ResolvedConfig,
} from '../types';
import {
  SIMULATION_ENDPOINTS,
  DEFAULT_SIMULATION_COUNT,
} from '../constants';
import {
  ApiError,
  NetworkError,
  PaymentRequiredError,
  SimulationFailedError,
} from '../utils/errors';
import { pollUntilComplete } from '../utils/polling';
import { PaymentService } from './payment';

/**
 * Simulation service for running Monte Carlo simulations
 */
export class SimulationService {
  constructor(
    private config: ResolvedConfig,
    private paymentService: PaymentService
  ) {}

  /**
   * Run a full simulation with automatic payment handling
   *
   * Flow:
   * 1. Request simulation → receive 402
   * 2. Send USDC payment → get signature
   * 3. Retry with X-Payment header → get job_id
   * 4. Poll until complete → return result
   */
  async simulate(
    sport: Sport,
    gameId: string,
    options: SimulateOptions = {}
  ): Promise<SimulationResult> {
    const {
      count = DEFAULT_SIMULATION_COUNT,
      autoPoll = true,
      onStatus,
      pollingInterval = this.config.pollingInterval,
      pollingTimeout = this.config.pollingTimeout,
    } = options;

    if (this.config.debug) {
      console.log(`[EdgeBets] Starting simulation for ${sport}/${gameId}`);
    }

    // Step 1: Request simulation (will get 402)
    if (onStatus) onStatus('requesting');

    // Step 2: Send payment
    if (onStatus) onStatus('paying');
    const signature = await this.paymentService.sendPayment();

    if (this.config.debug) {
      console.log(`[EdgeBets] Payment confirmed: ${signature}`);
    }

    // Step 3: Start simulation with payment proof
    if (onStatus) onStatus('starting');
    const job = await this.startSimulationWithPayment(sport, gameId, signature, count);

    if (this.config.debug) {
      console.log(`[EdgeBets] Simulation started: ${job.jobId}`);
    }

    // Step 4: Poll for results (or return job if autoPoll is false)
    if (!autoPoll) {
      if (job.result) {
        return job.result;
      }
      throw new SimulationFailedError(job.jobId, 'Auto-poll disabled and no immediate result');
    }

    if (onStatus) onStatus('processing', job);

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
        },
      }
    );

    if (!completedJob.result) {
      throw new SimulationFailedError(job.jobId, 'Simulation completed but no result returned');
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
  async startSimulationWithPayment(
    sport: Sport,
    gameId: string,
    paymentSignature: string,
    count: number = DEFAULT_SIMULATION_COUNT
  ): Promise<SimulationJob> {
    const endpoint = SIMULATION_ENDPOINTS[sport];
    const url = `${this.config.apiBaseUrl}/${endpoint}/${gameId}`;
    const paymentProof = this.paymentService.buildPaymentProof(paymentSignature);

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Payment': paymentProof,
        },
        body: JSON.stringify({ count }),
      });

      // Still got 402? Payment verification failed
      if (response.status === 402) {
        const data = await response.json();
        throw new PaymentRequiredError({
          amount: data.accepts?.[0]?.amount || 500000,
          recipient: data.accepts?.[0]?.recipient || '',
          currency: 'USDC',
          network: 'solana-mainnet',
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
        'Failed to start simulation',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Poll for simulation result
   */
  async pollResult(jobId: string): Promise<SimulationJob> {
    const url = `${this.config.apiBaseUrl}/x402/result/${jobId}`;

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
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Get x402 quote/requirements
   */
  async getQuote(): Promise<{
    price: number;
    currency: string;
    network: string;
    recipient: string;
  }> {
    const url = `${this.config.apiBaseUrl}/x402/quote`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      return {
        price: (data.accepts?.[0]?.amount || 500000) / 1000000,
        currency: 'USDC',
        network: 'solana-mainnet',
        recipient: data.accepts?.[0]?.recipient || this.paymentService.getTreasuryWallet(),
      };
    } catch (error) {
      throw new NetworkError(
        'Failed to get quote',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Normalize job response from API
   */
  private normalizeJobResponse(data: Record<string, unknown>): SimulationJob {
    const status = this.normalizeJobStatus(data.status || data.complete);
    const result = data.simulation as Record<string, unknown> | undefined;

    return {
      jobId: String(data.job_id || data.jobId || ''),
      status,
      pollUrl: String(data.poll_url || data.pollUrl || ''),
      error: data.error as string | undefined,
      estimatedTime: typeof data.estimated_time === 'number' ? data.estimated_time : undefined,
      result: status === 'complete' && result ? this.normalizeSimulationResult(result) : undefined,
    };
  }

  /**
   * Normalize job status
   */
  private normalizeJobStatus(status: unknown): SimulationJob['status'] {
    if (status === true || status === 'complete' || status === 'completed') {
      return 'complete';
    }
    if (status === 'error' || status === 'failed') {
      return 'error';
    }
    return 'processing';
  }

  /**
   * Normalize simulation result from API
   */
  private normalizeSimulationResult(data: Record<string, unknown>): SimulationResult {
    return {
      gameId: String(data.gameId || data.game_id || ''),
      simulationCount: Number(data.simulationCount || data.simulation_count || 10000),
      homeTeamName: String(data.homeTeamName || data.home_team_name || ''),
      awayTeamName: String(data.awayTeamName || data.away_team_name || ''),
      homeTeamAbbr: String(data.homeTeamAbbr || data.home_team_abbr || ''),
      awayTeamAbbr: String(data.awayTeamAbbr || data.away_team_abbr || ''),
      homeWinProbability: Number(data.homeWinProbability || data.home_win_probability || 0),
      awayWinProbability: Number(data.awayWinProbability || data.away_win_probability || 0),
      averageHomeScore: Number(data.averageHomeScore || data.average_home_score || 0),
      averageAwayScore: Number(data.averageAwayScore || data.average_away_score || 0),
      averageTotalPoints: Number(data.averageTotalPoints || data.average_total_points || 0),
      predictedSpread: Number(data.predictedSpread || data.predicted_spread || 0),
      spreadStdDev: data.spreadStdDev as number | undefined,
      totalStdDev: data.totalStdDev as number | undefined,
      overtimeProbability: data.overtimeProbability as number | undefined,
      elo: data.elo as SimulationResult['elo'],
      fourFactors: data.fourFactors as SimulationResult['fourFactors'],
      edgeAnalysis: data.edgeAnalysis as SimulationResult['edgeAnalysis'],
      bettingInsights: data.bettingInsights as SimulationResult['bettingInsights'],
      scoreDistribution: data.scoreDistribution as SimulationResult['scoreDistribution'],
      factorBreakdown: data.factorBreakdown as SimulationResult['factorBreakdown'],
    };
  }
}
