import { Connection, PublicKey } from "@solana/web3.js";
import { PREDICTIONS_SIZE, SURVIVAL_FLIPS, ROUNDS_BUFFER } from "./types";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

export const PROGRAM_ID = new PublicKey(
  process.env.NEXT_PUBLIC_PROGRAM_ID ||
    "7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX"
);

export const AUTHORITY = new PublicKey(
  process.env.NEXT_PUBLIC_AUTHORITY ||
    "89FeAXomb6QvvQ5CQ1cjouRAP3EDu3ZyrV13Xt2HNbLa"
);

export const RPC_URL =
  process.env.NEXT_PUBLIC_SOLANA_RPC_URL || "https://api.devnet.solana.com";

export { PREDICTIONS_SIZE, SURVIVAL_FLIPS, ROUNDS_BUFFER };

const GAME_DISCRIMINATOR = [27, 90, 166, 125, 74, 100, 121, 18];

// ---------------------------------------------------------------------------
// Connection singleton
// ---------------------------------------------------------------------------

let _connection: Connection | null = null;

export function getConnection(): Connection {
  if (!_connection) {
    _connection = new Connection(RPC_URL, "confirmed");
  }
  return _connection;
}

// ---------------------------------------------------------------------------
// PDA derivation
// ---------------------------------------------------------------------------

export function getGamePDA(): PublicKey {
  const [pda] = PublicKey.findProgramAddressSync(
    [Buffer.from("game"), AUTHORITY.toBuffer()],
    PROGRAM_ID
  );
  return pda;
}

// ---------------------------------------------------------------------------
// On-chain Game state (round-based — 782 bytes with discriminator)
// ---------------------------------------------------------------------------

export interface OnChainGameState {
  authority: PublicKey;
  usdcMint: PublicKey;
  vault: PublicKey;
  bump: number;
  vaultBump: number;
  currentRound: number;
  roundResults: number[]; // 640 bytes: 32 rounds × 20 results
  jackpotPool: bigint;
  operatorPool: bigint;
  totalEntries: number;
  totalWins: number;
  lastFlipAt: number; // unix timestamp of last flip (12h cooldown)
}

/**
 * Deserialize a Game account from raw bytes.
 *
 * Byte layout (round-based game, 782 bytes total):
 *   [0..8)      discriminator
 *   [8..40)     authority       Pubkey
 *   [40..72)    usdc_mint       Pubkey
 *   [72..104)   vault           Pubkey
 *   [104]       bump            u8
 *   [105]       vault_bump      u8
 *   [106..110)  current_round   u32 LE
 *   [110..750)  round_results   [u8; 640]  (32 rounds × 20 results)
 *   [750..758)  jackpot_pool    u64 LE
 *   [758..766)  operator_pool   u64 LE
 *   [766..770)  total_entries   u32 LE
 *   [770..774)  total_wins      u32 LE
 *   [774..782)  last_flip_at    i64 LE
 */
export function deserializeGameAccount(data: Uint8Array): OnChainGameState {
  for (let i = 0; i < 8; i++) {
    if (data[i] !== GAME_DISCRIMINATOR[i]) {
      throw new Error("Invalid game account discriminator");
    }
  }

  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  let offset = 8;

  const authority = new PublicKey(data.slice(offset, offset + 32));
  offset += 32;
  const usdcMint = new PublicKey(data.slice(offset, offset + 32));
  offset += 32;
  const vault = new PublicKey(data.slice(offset, offset + 32));
  offset += 32;

  const bump = data[offset];
  offset += 1;
  const vaultBump = data[offset];
  offset += 1;

  const currentRound = view.getUint32(offset, true);
  offset += 4;

  const roundResultsSize = ROUNDS_BUFFER * PREDICTIONS_SIZE; // 640
  const roundResults: number[] = [];
  for (let i = 0; i < roundResultsSize; i++) {
    roundResults.push(data[offset + i]);
  }
  offset += roundResultsSize;

  const jackpotPool = view.getBigUint64(offset, true);
  offset += 8;
  const operatorPool = view.getBigUint64(offset, true);
  offset += 8;

  const totalEntries = view.getUint32(offset, true);
  offset += 4;
  const totalWins = view.getUint32(offset, true);
  offset += 4;

  // last_flip_at is i64 — read as BigInt64 and convert to number (unix timestamp)
  const lastFlipAt = Number(view.getBigInt64(offset, true));

  return {
    authority,
    usdcMint,
    vault,
    bump,
    vaultBump,
    currentRound,
    roundResults,
    jackpotPool,
    operatorPool,
    totalEntries,
    totalWins,
    lastFlipAt,
  };
}

// ---------------------------------------------------------------------------
// Fetch helpers
// ---------------------------------------------------------------------------

export async function fetchGameFromChain(): Promise<OnChainGameState | null> {
  const connection = getConnection();
  const gamePDA = getGamePDA();
  const accountInfo = await connection.getAccountInfo(gamePDA);

  if (!accountInfo || !accountInfo.data) {
    return null;
  }

  return deserializeGameAccount(new Uint8Array(accountInfo.data));
}

// ---------------------------------------------------------------------------
// Ticket PDA + deserialization (99 bytes with discriminator)
// ---------------------------------------------------------------------------

const TICKET_DISCRIMINATOR = [41, 228, 24, 165, 78, 90, 235, 200];

export function getTicketPDA(
  gamePDA: PublicKey,
  player: PublicKey,
  round: number
): PublicKey {
  const buf = Buffer.alloc(4);
  buf.writeUInt32LE(round);
  const [pda] = PublicKey.findProgramAddressSync(
    [
      Buffer.from("ticket"),
      gamePDA.toBuffer(),
      player.toBuffer(),
      buf,
    ],
    PROGRAM_ID
  );
  return pda;
}

export interface OnChainTicket {
  game: PublicKey;
  player: PublicKey;
  round: number;
  predictions: number[];
  winner: boolean;
  collected: boolean;
  bump: number;
}

/**
 * Deserialize a Ticket account from raw bytes.
 *
 * Byte layout (99 bytes total):
 *   [0..8)    discriminator
 *   [8..40)   game           Pubkey
 *   [40..72)  player         Pubkey
 *   [72..76)  round          u32 LE
 *   [76..96)  predictions    [u8; 20]  — first 14 checked for survival
 *   [96]      winner         bool
 *   [97]      collected      bool
 *   [98]      bump           u8
 */
export function deserializeTicketAccount(data: Uint8Array): OnChainTicket {
  for (let i = 0; i < 8; i++) {
    if (data[i] !== TICKET_DISCRIMINATOR[i]) {
      throw new Error("Invalid ticket account discriminator");
    }
  }

  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  let offset = 8;

  const game = new PublicKey(data.slice(offset, offset + 32));
  offset += 32;
  const player = new PublicKey(data.slice(offset, offset + 32));
  offset += 32;

  const round = view.getUint32(offset, true);
  offset += 4;

  const predictions: number[] = [];
  for (let i = 0; i < PREDICTIONS_SIZE; i++) {
    predictions.push(data[offset + i]);
  }
  offset += PREDICTIONS_SIZE;

  const winner = data[offset] !== 0;
  offset += 1;
  const collected = data[offset] !== 0;
  offset += 1;
  const bump = data[offset];

  return {
    game,
    player,
    round,
    predictions,
    winner,
    collected,
    bump,
  };
}

export async function fetchTicketFromChain(
  playerPubkey: PublicKey,
  round: number
): Promise<OnChainTicket | null> {
  const connection = getConnection();
  const gamePDA = getGamePDA();
  const ticketPDA = getTicketPDA(gamePDA, playerPubkey, round);
  const accountInfo = await connection.getAccountInfo(ticketPDA);

  if (!accountInfo || !accountInfo.data) {
    return null;
  }

  return deserializeTicketAccount(new Uint8Array(accountInfo.data));
}

// ---------------------------------------------------------------------------
// Round results helpers
// ---------------------------------------------------------------------------

/** Get the 20 results for a specific round. Returns empty array if not yet flipped. */
export function getRoundResults(
  game: OnChainGameState,
  round: number
): number[] {
  if (round >= game.currentRound) return []; // not yet flipped
  if (game.currentRound - round > ROUNDS_BUFFER) return []; // expired
  const baseIdx = (round % ROUNDS_BUFFER) * PREDICTIONS_SIZE;
  return game.roundResults.slice(baseIdx, baseIdx + PREDICTIONS_SIZE);
}

/** Compute ticket status from game state and ticket. */
export function computeTicketStatus(
  game: OnChainGameState,
  ticket: OnChainTicket
): {
  status: string;
  results: number[];
  flipped: boolean;
  score: number;
  survived: boolean;
  comparisons: {
    index: number;
    predicted: string;
    actual: string;
    match: boolean;
  }[];
} {
  const flipped = game.currentRound > ticket.round;
  const results = flipped ? getRoundResults(game, ticket.round) : [];

  let score = 0;
  let survived = true;
  const comparisons: {
    index: number;
    predicted: string;
    actual: string;
    match: boolean;
  }[] = [];

  if (flipped && results.length === PREDICTIONS_SIZE) {
    for (let i = 0; i < PREDICTIONS_SIZE; i++) {
      const predicted = flipToStr(ticket.predictions[i]);
      const actual = flipToStr(results[i]);
      const match = predicted === actual;
      if (i < SURVIVAL_FLIPS) {
        if (match) {
          score++;
        } else {
          survived = false;
        }
      }
      comparisons.push({ index: i, predicted, actual, match });
    }
  }

  let status: string;
  if (ticket.winner && ticket.collected) {
    status = "WINNER_COLLECTED";
  } else if (ticket.winner) {
    status = "WINNER";
  } else if (!flipped) {
    status = "WAITING";
  } else if (survived && score === SURVIVAL_FLIPS) {
    status = "ALL_CORRECT";
  } else {
    status = "ELIMINATED";
  }

  return {
    status,
    results,
    flipped,
    score,
    survived,
    comparisons,
  };
}

// ---------------------------------------------------------------------------
// Formatting helpers
// ---------------------------------------------------------------------------

/** Convert raw USDC lamports (6 decimals) to a display number. */
export function formatJackpot(lamports: bigint): number {
  return Number(lamports) / 1_000_000;
}

/** Convert flip result to display character. */
export function flipToStr(r: number): string {
  return r === 1 ? "H" : r === 2 ? "T" : "?";
}
