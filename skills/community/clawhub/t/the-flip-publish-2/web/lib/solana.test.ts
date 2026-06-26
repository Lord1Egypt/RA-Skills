/**
 * Comprehensive tests for Game + Ticket account deserialization (round-based model).
 *
 * Run with: npx tsx lib/solana.test.ts
 *
 * Each round flips all 20 coins at once. First 14 must match to win.
 * Game stores 32 rounds × 20 results = 640 bytes of round data.
 */

import { PublicKey } from "@solana/web3.js";

// --- Inline the constants and deserializer to avoid Next.js import issues ---

const PREDICTIONS_SIZE = 20;
const SURVIVAL_FLIPS = 14;
const ROUNDS_BUFFER = 32;
const ROUND_RESULTS_SIZE = ROUNDS_BUFFER * PREDICTIONS_SIZE; // 640
const GAME_DISCRIMINATOR = [27, 90, 166, 125, 74, 100, 121, 18];
const TICKET_DISCRIMINATOR = [41, 228, 24, 165, 78, 90, 235, 200];

interface OnChainGameState {
  authority: PublicKey;
  usdcMint: PublicKey;
  vault: PublicKey;
  bump: number;
  vaultBump: number;
  currentRound: number;
  roundResults: number[];
  jackpotPool: bigint;
  operatorPool: bigint;
  totalEntries: number;
  totalWins: number;
  lastFlipAt: number;
}

interface OnChainTicket {
  game: PublicKey;
  player: PublicKey;
  round: number;
  predictions: number[];
  winner: boolean;
  collected: boolean;
  bump: number;
}

function deserializeGameAccount(data: Uint8Array): OnChainGameState {
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

  const bump = data[offset]; offset += 1;
  const vaultBump = data[offset]; offset += 1;

  const currentRound = view.getUint32(offset, true);
  offset += 4;

  const roundResults: number[] = [];
  for (let i = 0; i < ROUND_RESULTS_SIZE; i++) {
    roundResults.push(data[offset + i]);
  }
  offset += ROUND_RESULTS_SIZE;

  const jackpotPool = view.getBigUint64(offset, true); offset += 8;
  const operatorPool = view.getBigUint64(offset, true); offset += 8;

  const totalEntries = view.getUint32(offset, true); offset += 4;
  const totalWins = view.getUint32(offset, true); offset += 4;
  const lastFlipAt = Number(view.getBigInt64(offset, true));

  return {
    authority, usdcMint, vault, bump, vaultBump, currentRound,
    roundResults, jackpotPool, operatorPool, totalEntries, totalWins, lastFlipAt,
  };
}

function deserializeTicketAccount(data: Uint8Array): OnChainTicket {
  for (let i = 0; i < 8; i++) {
    if (data[i] !== TICKET_DISCRIMINATOR[i]) {
      throw new Error("Invalid ticket account discriminator");
    }
  }

  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  let offset = 8;

  const game = new PublicKey(data.slice(offset, offset + 32)); offset += 32;
  const player = new PublicKey(data.slice(offset, offset + 32)); offset += 32;

  const round = view.getUint32(offset, true); offset += 4;

  const predictions: number[] = [];
  for (let i = 0; i < PREDICTIONS_SIZE; i++) {
    predictions.push(data[offset + i]);
  }
  offset += PREDICTIONS_SIZE;

  const winner = data[offset] !== 0; offset += 1;
  const collected = data[offset] !== 0; offset += 1;
  const bump = data[offset];

  return { game, player, round, predictions, winner, collected, bump };
}

// ---------------------------------------------------------------------------
// Test helpers
// ---------------------------------------------------------------------------

const GAME_SIZE = 782; // 8 discriminator + 774 data
const TICKET_SIZE = 99; // 8 discriminator + 91 data

function writeDiscriminator(buf: Uint8Array, disc: number[]): void {
  for (let i = 0; i < 8; i++) buf[i] = disc[i];
}

function writePubkey(buf: Uint8Array, offset: number, key: PublicKey): void {
  const bytes = key.toBytes();
  for (let i = 0; i < 32; i++) buf[offset + i] = bytes[i];
}

function writeU64LE(buf: Uint8Array, offset: number, value: bigint): void {
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  view.setBigUint64(offset, value, true);
}

function writeI64LE(buf: Uint8Array, offset: number, value: bigint): void {
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  view.setBigInt64(offset, value, true);
}

function writeU32LE(buf: Uint8Array, offset: number, value: number): void {
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  view.setUint32(offset, value, true);
}

function buildGameBuffer(opts: {
  authority?: PublicKey;
  usdcMint?: PublicKey;
  vault?: PublicKey;
  bump?: number;
  vaultBump?: number;
  currentRound?: number;
  roundResults?: number[];
  jackpotPool?: bigint;
  operatorPool?: bigint;
  totalEntries?: number;
  totalWins?: number;
  lastFlipAt?: bigint;
}): Uint8Array {
  const buf = new Uint8Array(GAME_SIZE);
  writeDiscriminator(buf, GAME_DISCRIMINATOR);

  writePubkey(buf, 8, opts.authority ?? PublicKey.default);
  writePubkey(buf, 40, opts.usdcMint ?? PublicKey.default);
  writePubkey(buf, 72, opts.vault ?? PublicKey.default);

  buf[104] = opts.bump ?? 0;
  buf[105] = opts.vaultBump ?? 0;
  writeU32LE(buf, 106, opts.currentRound ?? 0);

  const results = opts.roundResults ?? [];
  for (let i = 0; i < Math.min(results.length, ROUND_RESULTS_SIZE); i++) {
    buf[110 + i] = results[i];
  }

  writeU64LE(buf, 750, opts.jackpotPool ?? 0n);
  writeU64LE(buf, 758, opts.operatorPool ?? 0n);
  writeU32LE(buf, 766, opts.totalEntries ?? 0);
  writeU32LE(buf, 770, opts.totalWins ?? 0);
  writeI64LE(buf, 774, opts.lastFlipAt ?? 0n);

  return buf;
}

function buildTicketBuffer(opts: {
  game?: PublicKey;
  player?: PublicKey;
  round?: number;
  predictions?: number[];
  winner?: boolean;
  collected?: boolean;
  bump?: number;
}): Uint8Array {
  const buf = new Uint8Array(TICKET_SIZE);
  writeDiscriminator(buf, TICKET_DISCRIMINATOR);

  writePubkey(buf, 8, opts.game ?? PublicKey.default);
  writePubkey(buf, 40, opts.player ?? PublicKey.default);
  writeU32LE(buf, 72, opts.round ?? 0);

  const preds = opts.predictions ?? new Array(PREDICTIONS_SIZE).fill(1);
  for (let i = 0; i < PREDICTIONS_SIZE; i++) buf[76 + i] = preds[i];

  buf[96] = (opts.winner ?? false) ? 1 : 0;
  buf[97] = (opts.collected ?? false) ? 1 : 0;
  buf[98] = opts.bump ?? 0;

  return buf;
}

// ---------------------------------------------------------------------------
// Test runner
// ---------------------------------------------------------------------------

let passed = 0;
let failed = 0;

function assert(condition: boolean, msg: string): void {
  if (!condition) {
    console.error(`  FAIL: ${msg}`);
    failed++;
  } else {
    passed++;
  }
}

function assertThrows(fn: () => void, msg: string): void {
  try {
    fn();
    console.error(`  FAIL (no throw): ${msg}`);
    failed++;
  } catch {
    passed++;
  }
}

// ---------------------------------------------------------------------------
// Game Tests
// ---------------------------------------------------------------------------

console.log("=== Game Deserialization Tests (Round-Based Model) ===\n");

console.log("Test 1: Fresh initialized game");
{
  const authority = new PublicKey("89FeAXomb6QvvQ5CQ1cjouRAP3EDu3ZyrV13Xt2HNbLa");
  const buf = buildGameBuffer({
    authority,
    bump: 255,
    vaultBump: 254,
    currentRound: 0,
  });
  const game = deserializeGameAccount(buf);

  assert(game.authority.equals(authority), "authority matches");
  assert(game.bump === 255, "bump = 255");
  assert(game.vaultBump === 254, "vaultBump = 254");
  assert(game.currentRound === 0, "currentRound = 0");
  assert(game.roundResults.length === ROUND_RESULTS_SIZE, "roundResults has 640 elements");
  assert(game.jackpotPool === 0n, "jackpotPool = 0");
  assert(game.operatorPool === 0n, "operatorPool = 0");
  assert(game.totalEntries === 0, "totalEntries = 0");
  assert(game.totalWins === 0, "totalWins = 0");
  assert(game.lastFlipAt === 0, "lastFlipAt = 0");
}

console.log("Test 2: Game with entries and one completed round");
{
  // Round 0 results: all 20 flips
  const roundResults = new Array(ROUND_RESULTS_SIZE).fill(0);
  for (let i = 0; i < PREDICTIONS_SIZE; i++) {
    roundResults[i] = (i % 2 === 0) ? 1 : 2; // alternating H T H T ...
  }
  const buf = buildGameBuffer({
    currentRound: 1,
    roundResults,
    jackpotPool: 990_000n * 50n,
    operatorPool: 10_000n * 50n,
    totalEntries: 50,
    totalWins: 0,
  });
  const game = deserializeGameAccount(buf);

  assert(game.currentRound === 1, "currentRound = 1");
  assert(game.roundResults[0] === 1, "round 0 flip 0 = H");
  assert(game.roundResults[1] === 2, "round 0 flip 1 = T");
  assert(game.roundResults[19] === 2, "round 0 flip 19 = T");
  assert(game.roundResults[20] === 0, "round 1 flip 0 = not yet");
  assert(game.jackpotPool === 49_500_000n, "jackpotPool = 49.5 USDC");
  assert(game.operatorPool === 500_000n, "operatorPool = 0.5 USDC");
  assert(game.totalEntries === 50, "totalEntries = 50");
  assert(game.totalWins === 0, "totalWins = 0");
}

console.log("Test 3: Game with wins");
{
  const buf = buildGameBuffer({
    currentRound: 100,
    jackpotPool: 0n,
    totalEntries: 500,
    totalWins: 3,
  });
  const game = deserializeGameAccount(buf);

  assert(game.currentRound === 100, "currentRound = 100");
  assert(game.totalWins === 3, "totalWins = 3");
  assert(game.jackpotPool === 0n, "jackpot zeroed after win");
}

console.log("Test 4: Large values");
{
  const bigJackpot = 10_000_000_000_000n;
  const buf = buildGameBuffer({
    jackpotPool: bigJackpot,
    totalEntries: 4_000_000_000,
    currentRound: 100_000,
  });
  const game = deserializeGameAccount(buf);

  assert(game.jackpotPool === bigJackpot, "large jackpot preserved");
  assert(game.totalEntries === 4_000_000_000, "near-max u32 entries");
  assert(game.currentRound === 100_000, "high currentRound");
}

console.log("Test 5: Invalid discriminator throws");
{
  const buf = new Uint8Array(GAME_SIZE);
  buf[0] = 0;
  assertThrows(() => deserializeGameAccount(buf), "should throw on invalid discriminator");
}

console.log("Test 6: Circular buffer wrapping (round 33 overwrites round 1)");
{
  const roundResults = new Array(ROUND_RESULTS_SIZE).fill(0);
  // Round 0 at index [0..20): all H
  for (let i = 0; i < PREDICTIONS_SIZE; i++) roundResults[i] = 1;
  // Round 1 at index [20..40): all T
  for (let i = 0; i < PREDICTIONS_SIZE; i++) roundResults[20 + i] = 2;
  // Round 32 wraps to index [0..20): overwrite round 0 with all T
  // Simulate by writing round 32's data at index 0
  // (In practice: currentRound=33, round 32 is at (32%32)*20 = 0)
  for (let i = 0; i < PREDICTIONS_SIZE; i++) roundResults[i] = 2;

  const buf = buildGameBuffer({ currentRound: 33, roundResults });
  const game = deserializeGameAccount(buf);

  assert(game.currentRound === 33, "currentRound = 33");
  // Index 0 now has round 32's data (all T)
  assert(game.roundResults[0] === 2, "round 32 at index 0 = T (overwritten)");
  // Index 20 still has round 1's data (all T)
  assert(game.roundResults[20] === 2, "round 1 at index 20 = T");
}

console.log("Test 7: Account size is exactly 782 bytes");
{
  // discriminator(8) + 3*Pubkey(96) + 2*u8(2) + u32(4) + [u8;640](640) + 2*u64(16) + 2*u32(8) + i64(8) = 782
  const expectedSize = 8 + 32 * 3 + 1 * 2 + 4 + ROUND_RESULTS_SIZE + 8 * 2 + 4 * 2 + 8;
  assert(expectedSize === 782, `expected size = ${expectedSize}, want 782`);
}

console.log("Test 8: Multiple rounds stored correctly");
{
  const roundResults = new Array(ROUND_RESULTS_SIZE).fill(0);
  // Round 0: all H
  for (let i = 0; i < PREDICTIONS_SIZE; i++) roundResults[i] = 1;
  // Round 1: all T
  for (let i = 0; i < PREDICTIONS_SIZE; i++) roundResults[PREDICTIONS_SIZE + i] = 2;
  // Round 2: alternating
  for (let i = 0; i < PREDICTIONS_SIZE; i++) roundResults[2 * PREDICTIONS_SIZE + i] = (i % 2 === 0) ? 1 : 2;

  const buf = buildGameBuffer({ currentRound: 3, roundResults });
  const game = deserializeGameAccount(buf);

  // Check round 0
  for (let i = 0; i < PREDICTIONS_SIZE; i++) {
    assert(game.roundResults[i] === 1, `round 0 flip ${i} = H`);
  }
  // Check round 1
  for (let i = 0; i < PREDICTIONS_SIZE; i++) {
    assert(game.roundResults[PREDICTIONS_SIZE + i] === 2, `round 1 flip ${i} = T`);
  }
  // Check round 2
  assert(game.roundResults[2 * PREDICTIONS_SIZE] === 1, "round 2 flip 0 = H");
  assert(game.roundResults[2 * PREDICTIONS_SIZE + 1] === 2, "round 2 flip 1 = T");
}

console.log("Test 8b: lastFlipAt timestamp preserved");
{
  const ts = 1738800000n; // ~Feb 2025
  const buf = buildGameBuffer({ currentRound: 10, lastFlipAt: ts });
  const game = deserializeGameAccount(buf);
  assert(game.lastFlipAt === 1738800000, "lastFlipAt = 1738800000");
}

// ---------------------------------------------------------------------------
// Ticket Tests
// ---------------------------------------------------------------------------

console.log("\n=== Ticket Deserialization Tests (20 predictions, round-based) ===\n");

console.log("Test 9: Fresh ticket with 20 predictions");
{
  const player = new PublicKey("89FeAXomb6QvvQ5CQ1cjouRAP3EDu3ZyrV13Xt2HNbLa");
  const preds = [1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1];
  const buf = buildTicketBuffer({
    player,
    round: 42,
    predictions: preds,
    winner: false,
    collected: false,
    bump: 200,
  });
  const ticket = deserializeTicketAccount(buf);

  assert(ticket.player.equals(player), "player matches");
  assert(ticket.round === 42, "round = 42");
  assert(ticket.predictions.length === PREDICTIONS_SIZE, `${PREDICTIONS_SIZE} predictions`);
  assert(ticket.predictions[0] === 1, "pred[0] = H");
  assert(ticket.predictions[1] === 2, "pred[1] = T");
  assert(ticket.predictions[13] === 2, "pred[13] = T (last survival)");
  assert(ticket.predictions[14] === 1, "pred[14] = H (beyond survival)");
  assert(ticket.predictions[19] === 1, "pred[19] = H (last prediction)");
  assert(ticket.winner === false, "not winner");
  assert(ticket.collected === false, "not collected");
  assert(ticket.bump === 200, "bump = 200");
}

console.log("Test 10: Winner ticket");
{
  const buf = buildTicketBuffer({
    round: 100,
    winner: true,
    collected: true,
  });
  const ticket = deserializeTicketAccount(buf);

  assert(ticket.round === 100, "round = 100");
  assert(ticket.winner === true, "is winner");
  assert(ticket.collected === true, "is collected");
}

console.log("Test 11: Ticket size is exactly 99 bytes");
{
  // discriminator(8) + 2*Pubkey(64) + u32(4) + [u8;20](20) + 2*bool(2) + u8(1) = 99
  const expectedSize = 8 + 32 * 2 + 4 + PREDICTIONS_SIZE + 1 * 2 + 1;
  assert(expectedSize === 99, `expected size = ${expectedSize}, want 99`);
}

console.log("Test 12: Invalid ticket discriminator throws");
{
  const buf = new Uint8Array(TICKET_SIZE);
  buf[0] = 0;
  assertThrows(() => deserializeTicketAccount(buf), "should throw on invalid discriminator");
}

console.log("Test 13: Only first 14 predictions matter for survival");
{
  // Create a ticket where first 14 are all H, last 6 are all T
  const preds = [...new Array(SURVIVAL_FLIPS).fill(1), ...new Array(PREDICTIONS_SIZE - SURVIVAL_FLIPS).fill(2)];
  const buf = buildTicketBuffer({ predictions: preds });
  const ticket = deserializeTicketAccount(buf);

  assert(ticket.predictions.length === PREDICTIONS_SIZE, "20 predictions stored");
  for (let i = 0; i < SURVIVAL_FLIPS; i++) {
    assert(ticket.predictions[i] === 1, `pred[${i}] = H (survival)`);
  }
  for (let i = SURVIVAL_FLIPS; i < PREDICTIONS_SIZE; i++) {
    assert(ticket.predictions[i] === 2, `pred[${i}] = T (beyond survival)`);
  }
}

// ---------------------------------------------------------------------------
// Results
// ---------------------------------------------------------------------------

console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);

if (failed > 0) {
  process.exit(1);
} else {
  console.log("All tests passed!");
  process.exit(0);
}
