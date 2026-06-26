export const PREDICTIONS_SIZE = 20; // Players pick 20 H/T predictions
export const SURVIVAL_FLIPS = 14;  // First 14 must match to win
export const ROUNDS_BUFFER = 32;   // Store last 32 rounds of results

export type FlipResult = 0 | 1 | 2; // 0 = not yet flipped, 1 = Heads, 2 = Tails

export type GamePhase = "not_initialized" | "active" | "offline";

export interface GameState {
  phase: GamePhase;
  jackpot: number;
  currentRound: number;
  totalEntries: number;
  totalWins: number;
  operatorPool: number;
}

export const EMPTY_GAME_STATE: GameState = {
  phase: "not_initialized",
  jackpot: 0,
  currentRound: 0,
  totalEntries: 0,
  totalWins: 0,
  operatorPool: 0,
};
