#!/usr/bin/env node
'use strict';

/**
 * steamedclaw-chess helper — client-side chess strategy skill.
 *
 * Takes a FEN string on the command line, returns top-N candidate moves with
 * evaluations and a style archetype per candidate (solid, aggressive,
 * conservative, speculative, dubious, losing) derived from two measured axes:
 * soundness (centipawn delta vs. the engine's best move) and sharpness
 * (checks, null-move threat detection, and safe-reply count in the resulting
 * position). Stateless. No network. No coupling to SteamedClaw.
 *
 * @version 1.0.0
 *
 * Usage:
 *   node chess-helper.js analyze <FEN>
 *     [--depth N]       integer 1-25, default 15 (mapped to engine search depth)
 *     [--movetime MS]   integer milliseconds (soft budget; takes precedence over --depth)
 *     [--multipv N]     integer 1-5, default 5
 *
 * Exit codes:
 *   0 — analysis complete
 *   2 — invalid FEN (stdout: "err: invalid fen: <message>")
 *   4 — engine failure (stdout: "err: engine failed: <message>")
 *
 * Engine: js-chess-engine v2.4.6 (MIT), bundled under ./engine/.
 * See planning/054-chess-strategy-skill.md for design decisions.
 */

const path = require('path');
const engine = require(path.join(__dirname, 'engine', 'index.js'));

// ── Constants ────────────────────────────────────────────────────────────────

const HELPER_VERSION = '1.0.0';

// Exit codes per spec (planning/054 §4).
const EXIT_OK = 0;
const EXIT_INVALID_FEN = 2;
const EXIT_ENGINE_FAILED = 4;

// CLI flag ranges (planning/054 §4).
const DEPTH_MIN = 1;
const DEPTH_MAX = 25;
const DEPTH_DEFAULT = 15;
const MULTIPV_MIN = 1;
const MULTIPV_MAX = 5;
const MULTIPV_DEFAULT = 5;

// Engine AI level thresholds used when --movetime is specified (soft budget).
// js-chess-engine doesn't expose a native movetime primitive; we pick the
// strongest level that typically finishes inside the budget on a modern CPU.
const MOVETIME_LEVEL_THRESHOLDS = [
  { maxMs: 200, level: 2 },
  { maxMs: 1000, level: 3 },
  { maxMs: 5000, level: 4 },
  { maxMs: Infinity, level: 5 },
];

// Mapping --depth (1..25) to engine AI level (1..5). The engine's native
// "levels" already bake in base depth + extensions + quiescence; exposing a
// raw 1-25 knob is just a coarse mapping over those levels. Five buckets.
function depthToLevel(depth) {
  if (depth <= 3) return 1;
  if (depth <= 7) return 2;
  if (depth <= 12) return 3;
  if (depth <= 18) return 4;
  return 5;
}

// Mate score threshold used by the engine (999999 / 2 buffer).
const MATE_SCORE_THRESHOLD = 100000;

// Material-count threshold for endgame classification (piece count ≤ 7,
// not counting kings). Matches planning/054 §2.3.
const ENDGAME_PIECE_THRESHOLD = 7;

// Opening ends after move 14 (fullMove < 15); middlegame 15..39; endgame 40+
// or few pieces, per planning/054 §2.3.
const OPENING_MAX_FULLMOVE = 14;
const ENDGAME_MIN_FULLMOVE = 40;

// Centipawn threshold inside which opening evals are suppressed (all playable).
const OPENING_EVAL_SUPPRESS_CP = 30;

// Centipawn thresholds for tiered assessment magnitude. Shared across phases.
const SLIGHT_ADVANTAGE_CP = 200;
const CLEAR_ADVANTAGE_CP = 500;

// Centipawn gap between #1 and #2 that earns candidate #1 a "clearly best" tag.
const CLEARLY_BEST_GAP_CP = 150;

// ── Archetype thresholds (issue #555) ────────────────────────────────────────
// All expected to be tuned empirically after fleet testing (#339).

// Within this many cp of the best move a candidate is "sound".
const SOUND_DELTA_CP = 30;
// Between SOUND and this, a candidate is conservative/speculative (a deliberate
// eval concession); above it, dubious; above LOSING_DELTA_CP, losing.
const SPECULATIVE_DELTA_CP = 150;
const LOSING_DELTA_CP = 300;
// An opponent reply within this many cp of their best reply counts as "safe".
const SAFE_REPLY_BAND_CP = 100;
// A resulting position with at most this many safe replies is sharp/forcing.
const SHARP_MAX_SAFE_REPLIES = 2;
// Null-move threat detection: after the candidate, give the opponent a "pass"
// and re-search from the mover's side. A large eval swing vs. letting the
// opponent reply means the move created a concrete threat (win material,
// mate). The raw swing carries a position-dependent tempo baseline (the
// engine's side-to-move bonus counts once in each probe), so the test is
// RELATIVE: a candidate is a threat when its swing exceeds the median swing
// of the candidate set by this many cp.
const THREAT_SWING_ABOVE_MEDIAN_CP = 150;
// The engine's zero-window root search returns loose fail-low BOUNDS for
// non-best root moves, so the main analysis can grossly understate how bad a
// candidate is (a mate-losing move can report a ~90cp delta). The reply
// probe's best-reply score IS an exact full-window PV score, so it provides
// an independent delta estimate (relative to the best candidate's probe).
// The probe runs at a lower level and is noisy for fine distinctions, so it
// only overrides the main delta when it exceeds it by this margin.
const PROBE_DELTA_TRUST_MARGIN_CP = 100;
// Sharpness probes run at a cheaper engine level than the main analysis —
// we only need the shape of the reply distribution, not exact evals.
const PROBE_LEVEL_CAP = 3;

// ── Argument parsing ─────────────────────────────────────────────────────────

/**
 * Parse argv. Returns { subcommand, fen, depth, movetime, multipv } or throws
 * on usage errors.
 */
function parseArgs(argv) {
  // argv: [node, script, subcommand, fen, ...flags]
  if (argv.length < 4) {
    throw new Error(
      'usage: chess-helper.js analyze <FEN> [--depth N] [--movetime MS] [--multipv N]',
    );
  }
  const subcommand = argv[2];
  if (subcommand !== 'analyze') {
    throw new Error(`unknown subcommand: ${subcommand} (expected: analyze)`);
  }
  const fen = argv[3];

  let depth = DEPTH_DEFAULT;
  let movetime;
  let multipv = MULTIPV_DEFAULT;

  for (let i = 4; i < argv.length; i++) {
    const flag = argv[i];
    const val = argv[i + 1];
    if (flag === '--depth') {
      depth = parseIntInRange(val, DEPTH_MIN, DEPTH_MAX, '--depth');
      i++;
    } else if (flag === '--movetime') {
      movetime = parseIntInRange(val, 1, 600000, '--movetime');
      i++;
    } else if (flag === '--multipv') {
      multipv = parseIntInRange(val, MULTIPV_MIN, MULTIPV_MAX, '--multipv');
      i++;
    } else {
      throw new Error(`unknown flag: ${flag}`);
    }
  }

  return { subcommand, fen, depth, movetime, multipv };
}

function parseIntInRange(val, min, max, name) {
  if (val === undefined) throw new Error(`${name} requires a value`);
  const n = Number(val);
  if (!Number.isInteger(n) || n < min || n > max) {
    throw new Error(`${name} must be an integer in [${min}, ${max}], got: ${val}`);
  }
  return n;
}

// ── Phase detection ──────────────────────────────────────────────────────────

/**
 * Classify game phase from a status snapshot.
 *
 * Rules (planning/054 §2.3):
 *  - endgame: fullMove >= 40 OR non-king piece count <= 7
 *  - opening: fullMove < 15 (and not endgame)
 *  - middlegame: everything else
 *
 * @param {object} st engine status() output
 * @returns {'opening'|'middlegame'|'endgame'}
 */
function detectPhase(st) {
  const pieces = st.pieces || {};
  let nonKingCount = 0;
  for (const sq of Object.keys(pieces)) {
    const p = pieces[sq];
    if (p !== 'K' && p !== 'k') nonKingCount++;
  }
  const fullMove = st.fullMove || 1;
  if (fullMove >= ENDGAME_MIN_FULLMOVE || nonKingCount <= ENDGAME_PIECE_THRESHOLD) {
    return 'endgame';
  }
  if (fullMove <= OPENING_MAX_FULLMOVE) return 'opening';
  return 'middlegame';
}

// ── Label generation ─────────────────────────────────────────────────────────

/**
 * Classify a move's nature from before/after piece maps.
 *
 * Returns an object of boolean flags used to generate labels.
 */
function classifyMove(fromSq, toSq, beforePieces, afterStatus) {
  const piece = beforePieces[fromSq];
  const target = beforePieces[toSq];
  const isCapture = target !== undefined;
  const isPawnMove = piece === 'P' || piece === 'p';
  const isKingMove = piece === 'K' || piece === 'k';
  const isKnightMove = piece === 'N' || piece === 'n';

  // Center squares — pawn advance or piece landing in the centre is "central".
  const CENTER = new Set(['D4', 'D5', 'E4', 'E5']);
  const isCentral = CENTER.has(toSq);

  // Castling heuristic: king moves two files.
  const fromFile = fromSq.charCodeAt(0);
  const toFile = toSq.charCodeAt(0);
  const isCastle = isKingMove && Math.abs(fromFile - toFile) === 2;

  const givesCheck = Boolean(afterStatus && afterStatus.check);
  const givesMate = Boolean(afterStatus && afterStatus.checkMate);
  const causesStalemate = Boolean(afterStatus && afterStatus.staleMate);

  return {
    isCapture,
    isPawnMove,
    isKingMove,
    isKnightMove,
    isCentral,
    isCastle,
    givesCheck,
    givesMate,
    causesStalemate,
  };
}

/**
 * Probe the opponent's replies in the position after a candidate move.
 *
 * Runs a cheap analysis on the given FEN and counts replies scoring within
 * SAFE_REPLY_BAND_CP of the best reply. Few safe replies = the position is
 * forcing. Also returns the best reply's score (opponent's perspective) so
 * the null-move threat check can compare probes at the same engine level.
 *
 * @returns {{safeReplies: number, bestReplyScore: number}|null} null if the
 *   probe failed (terminal position, engine error) — callers fall back to
 *   delta-only classification.
 */
function probeReplies(afterFen, probeLevel) {
  let probe;
  try {
    probe = engine.ai(afterFen, {
      level: probeLevel,
      play: false,
      analysis: true,
      randomness: 0,
    });
  } catch {
    return null;
  }
  if (!probe.analysis || probe.analysis.length === 0) return null;
  const bestReplyScore = probe.bestScore ?? probe.analysis[0].score;
  return {
    safeReplies: probe.analysis.filter((r) => bestReplyScore - r.score <= SAFE_REPLY_BAND_CP)
      .length,
    bestReplyScore,
  };
}

/**
 * Flip the side to move in a FEN (a "null move"). Clears the en-passant
 * square, which is no longer meaningful after a pass. Returns null on a
 * malformed FEN.
 */
function flipSideToMove(fen) {
  const parts = fen.split(' ');
  if (parts.length < 4) return null;
  parts[1] = parts[1] === 'w' ? 'b' : 'w';
  parts[3] = '-';
  return parts.join(' ');
}

/**
 * Null-move threat detection. In the position after the candidate, give the
 * opponent a "pass" and search from the mover's side again. The swing is the
 * mover's eval with the free move minus the mover's eval when the opponent
 * replies normally (negated best reply from the same-level reply probe).
 * A large positive swing means the candidate created a concrete threat.
 *
 * nullBest is returned separately because the swing alone cannot distinguish
 * "we threaten mate" (nullBest is mate-scale) from "we HANG mate"
 * (bestReplyScore is mate-scale) — both make the sum cross the mate
 * threshold. Callers must test nullBest, never the swing, for mate threats.
 *
 * @returns {{swing: number, nullBest: number}|null} null if the probe failed.
 */
function computeThreatSwing(afterFen, bestReplyScore, probeLevel) {
  const flipped = flipSideToMove(afterFen);
  if (!flipped) return null;
  let probe;
  try {
    probe = engine.ai(flipped, {
      level: probeLevel,
      play: false,
      analysis: true,
      randomness: 0,
    });
  } catch {
    return null;
  }
  const nullBest = probe.bestScore ?? probe.analysis?.[0]?.score;
  if (nullBest === undefined) return null;
  // bestReplyScore is from the opponent's perspective; negate for the
  // mover's. swing = nullBest - (-bestReplyScore).
  return { swing: nullBest + bestReplyScore, nullBest };
}

/**
 * Median of an array of numbers. Returns null on an empty array.
 */
function median(values) {
  if (values.length === 0) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
}

/**
 * Combine the sharpness signals for one candidate into a verdict.
 *
 * A candidate is "sharp" when it gives check, creates a concrete threat
 * (null-move swing well above the candidate set's median swing), or leaves
 * the opponent with almost no safe replies.
 *
 * The mate-threat test uses nullBest (the mover's eval given a free move),
 * NOT the swing: a mate-scale swing can also mean the opponent mates after
 * this candidate (the hangs-mate case, handled by classifyArchetype).
 *
 * @returns {{isSharp: boolean, reason: 'check'|'mate-threat'|'threat'|'forcing'|null}}
 */
function assessSharpness({ givesCheck, safeReplies, threatSwing, nullBest, medianSwing }) {
  if (givesCheck) return { isSharp: true, reason: 'check' };
  if (nullBest !== null && nullBest >= MATE_SCORE_THRESHOLD) {
    return { isSharp: true, reason: 'mate-threat' };
  }
  if (
    threatSwing !== null &&
    medianSwing !== null &&
    threatSwing - medianSwing >= THREAT_SWING_ABOVE_MEDIAN_CP
  ) {
    return { isSharp: true, reason: 'threat' };
  }
  if (safeReplies !== null && safeReplies <= SHARP_MAX_SAFE_REPLIES) {
    return { isSharp: true, reason: 'forcing' };
  }
  return { isSharp: false, reason: null };
}

/**
 * Classify a candidate into a style archetype from two measured axes:
 * soundness (deltaCp vs. the best move) and sharpness (checks, concrete
 * threats, forcing reply structure in the resulting position).
 *
 * @param {object} p
 * @param {number} p.deltaCp     centipawn loss vs. the engine's best move (>= 0)
 * @param {boolean} p.isSharp    sharpness verdict from assessSharpness()
 * @param {boolean} p.givesMate  candidate delivers mate
 * @param {boolean} p.missesMate best move is a forced mate and this candidate is not
 * @param {boolean} p.hangsMate  opponent has a forced mate after this candidate
 * @returns {'mate'|'misses-mate'|'hangs-mate'|'aggressive'|'solid'|'conservative'|'speculative'|'dubious'|'losing'}
 */
function classifyArchetype({ deltaCp, isSharp, givesMate, missesMate, hangsMate }) {
  if (givesMate) return 'mate';
  if (missesMate) return 'misses-mate';
  if (hangsMate) return 'hangs-mate';
  if (deltaCp <= SOUND_DELTA_CP) {
    return isSharp ? 'aggressive' : 'solid';
  }
  if (deltaCp <= SPECULATIVE_DELTA_CP) {
    // A deliberate eval concession: speculative if it sharpens the game,
    // conservative if it keeps things quiet.
    return isSharp ? 'speculative' : 'conservative';
  }
  if (deltaCp <= LOSING_DELTA_CP) return 'dubious';
  return 'losing';
}

/**
 * Build the human-readable label string for one candidate: archetype with a
 * one-clause explanation, then concrete secondary descriptors.
 */
function describeCandidate(archetype, deltaCp, sharpness, classification, isClearlyBest) {
  if (archetype === 'mate') return 'delivers mate';

  const pawns = (deltaCp / 100).toFixed(1);
  const sharpDetail = {
    check: 'forcing',
    'mate-threat': 'threatens mate',
    threat: 'creates a concrete threat',
    forcing: 'opponent has few safe replies',
  }[sharpness.reason];

  const parts = [];
  switch (archetype) {
    case 'misses-mate':
      parts.push('misses the forced mate');
      break;
    case 'hangs-mate':
      parts.push('allows a forced mate — opponent mates after this');
      break;
    case 'aggressive':
      parts.push(`aggressive: ${sharpDetail}`);
      break;
    case 'solid':
      parts.push('solid: sound, keeps the position stable');
      break;
    case 'conservative':
      parts.push(`conservative: safe, ~${pawns} pawns below best, keeps it quiet`);
      break;
    case 'speculative':
      parts.push(
        `speculative: gives up ~${pawns} pawns to ${
          sharpness.reason === 'mate-threat' ? 'threaten mate' : 'sharpen the game'
        }`,
      );
      break;
    case 'dubious':
      parts.push(`dubious: ~${pawns} pawns below best`);
      break;
    case 'losing':
      parts.push(`losing: ~${pawns} pawns below best`);
      break;
  }
  if (isClearlyBest) parts.unshift('clearly best');
  if (classification.causesStalemate) parts.push('stalemates opponent — forces a draw');
  if (classification.givesCheck) parts.push('gives check');
  if (classification.isCapture) parts.push('captures material');
  if (classification.isCastle) parts.push('castles');
  return parts.join(', ');
}

/**
 * Build the style-guide line: maps persona vocabulary to candidate numbers so
 * an agent's personality ("bold", "positional") or instructions ("play like
 * Karpov") can drive the pick directly. Empty buckets are omitted; returns
 * null when there is nothing useful to say.
 */
function buildStyleGuide(archetypes) {
  if (archetypes.length === 0) return null;
  if (archetypes[0] === 'mate') return 'style guide: mate on the board — play 1';
  const bold = [];
  const solid = [];
  const avoid = [];
  archetypes.forEach((archetype, i) => {
    const n = i + 1;
    if (archetype === 'aggressive' || archetype === 'speculative') bold.push(n);
    else if (archetype === 'solid' || archetype === 'conservative') solid.push(n);
    else avoid.push(n);
  });
  const segments = [];
  if (bold.length) segments.push(`bold/attacking → ${bold.join(', ')}`);
  if (solid.length) segments.push(`solid/positional → ${solid.join(', ')}`);
  if (avoid.length) segments.push(`avoid → ${avoid.join(', ')}`);
  return segments.length ? 'style guide: ' + segments.join(' · ') : null;
}

/**
 * Short assessment sentence from the best-move score and phase.
 */
function buildAssessment(phase, bestScoreCp, isMate, sideToMove) {
  if (isMate !== null) {
    if (isMate > 0) return `forced win for ${sideToMove}`;
    return `losing for ${sideToMove} — opponent has a forced win`;
  }
  const sign = bestScoreCp >= 0 ? '+' : '';
  const pawns = (bestScoreCp / 100).toFixed(2);
  if (phase === 'opening') {
    const magnitude = Math.abs(bestScoreCp);
    if (magnitude <= OPENING_EVAL_SUPPRESS_CP) {
      return 'quiet, roughly balanced';
    }
    if (magnitude <= SLIGHT_ADVANTAGE_CP) {
      return `quiet, ${sideToMove} ${bestScoreCp > 0 ? 'slightly better' : 'slightly worse'} (${sign}${pawns})`;
    }
    if (magnitude <= CLEAR_ADVANTAGE_CP) {
      return `${sideToMove} ${bestScoreCp > 0 ? 'better' : 'worse'} (${sign}${pawns})`;
    }
    return `${sideToMove} ${bestScoreCp > 0 ? 'winning' : 'losing'} (${sign}${pawns})`;
  }
  if (phase === 'middlegame') {
    if (Math.abs(bestScoreCp) <= 50) return 'roughly balanced';
    if (Math.abs(bestScoreCp) <= 200) {
      return `${sideToMove} ${bestScoreCp > 0 ? 'better' : 'worse'} (${sign}${pawns})`;
    }
    return `${sideToMove} ${bestScoreCp > 0 ? 'winning' : 'losing'} (${sign}${pawns})`;
  }
  // endgame
  if (Math.abs(bestScoreCp) <= 50) return 'drawn or near-drawn endgame';
  return `${sideToMove} ${bestScoreCp > 0 ? 'winning' : 'losing'} with correct play (${sign}${pawns})`;
}

// ── Formatting ───────────────────────────────────────────────────────────────

function formatUci(historyEntry) {
  // historyEntry is { FROM: TO } with uppercase squares. Convert to lowercase UCI.
  const [from, to] = Object.entries(historyEntry)[0];
  return (from + to).toLowerCase();
}

function formatEval(scoreCp, phase) {
  if (Math.abs(scoreCp) >= MATE_SCORE_THRESHOLD) {
    return scoreCp > 0 ? '#mate' : '#-mate';
  }
  if (phase === 'opening' && Math.abs(scoreCp) <= OPENING_EVAL_SUPPRESS_CP) {
    return '';
  }
  const sign = scoreCp >= 0 ? '+' : '';
  return `(${sign}${(scoreCp / 100).toFixed(2)})`;
}

// ── Core analyze flow ────────────────────────────────────────────────────────

/**
 * Run analysis for the given parsed args. Returns the formatted output string
 * on success. Throws on engine failure; callers translate to exit codes.
 */
function analyze({ fen, depth, movetime, multipv }) {
  // Step 1: validate FEN. engine.status() throws on malformed input.
  let statusBefore;
  try {
    statusBefore = engine.status(fen);
  } catch (err) {
    const e = new Error(err.message || String(err));
    e.kind = 'invalid_fen';
    throw e;
  }

  // If the position is already finished (mate/stalemate), emit a terminal
  // message rather than asking the engine for a move it cannot produce.
  if (statusBefore.checkMate) {
    return [
      'candidates:',
      '  (none — position is checkmate)',
      `phase: ${detectPhase(statusBefore)}`,
      `assessment: checkmate — ${statusBefore.turn} has been mated`,
      '',
    ].join('\n');
  }
  if (statusBefore.staleMate) {
    return [
      'candidates:',
      '  (none — position is stalemate)',
      `phase: ${detectPhase(statusBefore)}`,
      'assessment: stalemate — drawn',
      '',
    ].join('\n');
  }

  // Step 2: choose engine level. movetime wins over depth.
  let level;
  if (movetime !== undefined) {
    level = MOVETIME_LEVEL_THRESHOLDS.find((b) => movetime <= b.maxMs).level;
  } else {
    level = depthToLevel(depth);
  }

  // Step 3: run engine in analysis mode.
  let result;
  try {
    result = engine.ai(fen, {
      level,
      play: false,
      analysis: true,
      randomness: 0,
    });
  } catch (err) {
    const e = new Error(err.message || String(err));
    e.kind = 'engine_failed';
    throw e;
  }

  if (!result.analysis || result.analysis.length === 0) {
    const e = new Error('engine returned no analysis');
    e.kind = 'engine_failed';
    throw e;
  }

  // Step 4: take top-N candidates. Engine returns them sorted best→worst.
  const topN = result.analysis.slice(0, multipv);

  // Step 5: per-candidate classification — post-move status for concrete
  // flags (check/mate/stalemate), then a cheap sharpness probe on the
  // resulting position (safe-reply count).
  const phase = detectPhase(statusBefore);
  const bestScoreCp = result.bestScore ?? topN[0].score;
  const sideToMove = statusBefore.turn;
  const mateDetected =
    Math.abs(bestScoreCp) >= MATE_SCORE_THRESHOLD ? Math.sign(bestScoreCp) : null;
  const probeLevel = Math.min(level, PROBE_LEVEL_CAP);

  const enriched = topN.map((candidate, idx) => {
    const [fromSq, toSq] = Object.entries(candidate.move)[0];
    // Apply the move against a fresh Game instance to read post-move status.
    // Game.move() returns a BoardConfig with stale check/mate/stalemate flags
    // in js-chess-engine v2.4.6; exportJson() recomputes them.
    let afterStatus = null;
    let afterFen = null;
    try {
      const g = new engine.Game(fen);
      g.move(fromSq, toSq);
      afterStatus = g.exportJson();
      afterFen = g.exportFEN();
    } catch {
      // Classifier tolerates a null afterStatus / missing probe.
    }
    const classification = classifyMove(fromSq, toSq, statusBefore.pieces || {}, afterStatus);
    let safeReplies = null;
    let bestReplyScore = null;
    let threatSwing = null;
    let nullBest = null;
    if (afterFen && !classification.givesMate && !classification.causesStalemate) {
      const replies = probeReplies(afterFen, probeLevel);
      if (replies) {
        safeReplies = replies.safeReplies;
        bestReplyScore = replies.bestReplyScore;
        // Null-move probe is skipped when the candidate gives check — passing
        // with the king en prise is not a legal position to search.
        if (!classification.givesCheck) {
          const threat = computeThreatSwing(afterFen, replies.bestReplyScore, probeLevel);
          if (threat) {
            threatSwing = threat.swing;
            nullBest = threat.nullBest;
          }
        }
      }
    }
    const missesMate =
      bestScoreCp >= MATE_SCORE_THRESHOLD && candidate.score < MATE_SCORE_THRESHOLD;
    return {
      candidate,
      classification,
      safeReplies,
      bestReplyScore,
      threatSwing,
      nullBest,
      missesMate,
    };
  });

  // Post-loop, cross-candidate corrections:
  //
  // hangs-mate: a mate-scale best reply means the OPPONENT mates after this
  // candidate. Only differentiating when at least one candidate doesn't hang
  // mate — if every move loses to mate, relative deltas are all that's left.
  //
  // delta correction: the main analysis reports loose bounds for non-best
  // root moves (zero-window root search), so a blunder can masquerade as a
  // small concession. The probe's best-reply score is an exact PV score at
  // probe level; the probe-implied delta (relative to the best candidate's
  // probe) overrides the main delta when it is larger by a clear margin.
  const bestReply0 = enriched.length > 0 ? enriched[0].bestReplyScore : null;
  const anyNonHanging = enriched.some(
    (c) => c.bestReplyScore === null || c.bestReplyScore < MATE_SCORE_THRESHOLD,
  );
  enriched.forEach((c) => {
    c.hangsMate =
      anyNonHanging && c.bestReplyScore !== null && c.bestReplyScore >= MATE_SCORE_THRESHOLD;
    let deltaCp = Math.abs(bestScoreCp - c.candidate.score);
    if (c.bestReplyScore !== null && bestReply0 !== null) {
      const probeDelta = c.bestReplyScore - bestReply0;
      if (probeDelta > deltaCp + PROBE_DELTA_TRUST_MARGIN_CP) deltaCp = probeDelta;
    }
    c.deltaCp = deltaCp;
  });

  // Sharpness is judged relative to the candidate set: the median null-move
  // swing carries the position's tempo baseline; a genuine threat sticks out
  // above it.
  const medianSwing = median(enriched.map((c) => c.threatSwing).filter((s) => s !== null));
  enriched.forEach((c) => {
    c.sharpness = assessSharpness({
      givesCheck: c.classification.givesCheck,
      safeReplies: c.safeReplies,
      threatSwing: c.threatSwing,
      nullBest: c.nullBest,
      medianSwing,
    });
  });

  const archetypes = enriched.map((c) =>
    classifyArchetype({
      deltaCp: c.deltaCp,
      isSharp: c.sharpness.isSharp,
      givesMate: c.classification.givesMate,
      missesMate: c.missesMate,
      hangsMate: c.hangsMate,
    }),
  );

  const lines = ['candidates:'];
  enriched.forEach((c, idx) => {
    const uci = formatUci(c.candidate.move);
    const isClearlyBest =
      idx === 0 &&
      topN.length > 1 &&
      Math.abs(bestScoreCp) < MATE_SCORE_THRESHOLD &&
      bestScoreCp - topN[1].score >= CLEARLY_BEST_GAP_CP;
    const labels = describeCandidate(
      archetypes[idx],
      c.deltaCp,
      c.sharpness,
      c.classification,
      isClearlyBest,
    );
    // A hangs-mate candidate's main-analysis score is a meaningless bound;
    // show the honest probe-derived eval (renders as #-mate).
    const evalStr = c.hangsMate
      ? formatEval(-c.bestReplyScore, phase)
      : formatEval(c.candidate.score, phase);
    const parts = [`  ${idx + 1}. ${uci}`];
    if (evalStr) parts.push(evalStr);
    parts.push('— ' + labels);
    lines.push(parts.join('  '));
  });

  const styleGuide = buildStyleGuide(archetypes);
  if (styleGuide) lines.push(styleGuide);
  lines.push(`phase: ${phase}`);
  lines.push(`assessment: ${buildAssessment(phase, bestScoreCp, mateDetected, sideToMove)}`);
  lines.push('');
  return lines.join('\n');
}

// ── Entry point ──────────────────────────────────────────────────────────────

function main(argv) {
  let args;
  try {
    args = parseArgs(argv);
  } catch (err) {
    process.stdout.write('err: ' + err.message + '\n');
    // Usage / flag errors are not "invalid FEN" nor "engine failure";
    // exit 1 to distinguish them from the spec's 0/2/4 codes.
    return 1;
  }

  try {
    const out = analyze(args);
    process.stdout.write(out);
    return EXIT_OK;
  } catch (err) {
    if (err.kind === 'invalid_fen') {
      process.stdout.write('err: invalid fen: ' + err.message + '\n');
      return EXIT_INVALID_FEN;
    }
    process.stdout.write('err: engine failed: ' + (err.message || String(err)) + '\n');
    return EXIT_ENGINE_FAILED;
  }
}

// Export for unit tests. Only invoke main() when run as a script.
module.exports = {
  HELPER_VERSION,
  parseArgs,
  detectPhase,
  classifyMove,
  classifyArchetype,
  assessSharpness,
  median,
  describeCandidate,
  buildStyleGuide,
  probeReplies,
  flipSideToMove,
  computeThreatSwing,
  buildAssessment,
  formatEval,
  formatUci,
  analyze,
  main,
};

if (require.main === module) {
  process.exit(main(process.argv));
}
