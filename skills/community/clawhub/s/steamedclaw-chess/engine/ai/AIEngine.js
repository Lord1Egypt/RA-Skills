"use strict";
/**
 * AI Engine for js-chess-engine v2
 *
 * Orchestrates the AI search and provides level-based difficulty settings.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.AIEngine = void 0;
const Search_1 = require("./Search");
const MoveGenerator_1 = require("../core/MoveGenerator");
const types_1 = require("../types");
/**
 * AI level to depth mapping
 * Based on v1 behavior for compatibility
 */
const LEVEL_CONFIG = {
    // NOTE: Depth is the single biggest speed lever.
    // These values are intentionally conservative for browser-friendliness.
    // Tuning note (2026-02): lower levels intentionally omit tactical extensions
    // (check extensions + deep quiescence) so they're easier to beat.
    1: { baseDepth: 1, extendedDepth: 0, checkExtension: false, qMaxDepth: 0 }, // Beginner
    2: { baseDepth: 2, extendedDepth: 0, checkExtension: true, qMaxDepth: 0 }, // Easy
    3: { baseDepth: 2, extendedDepth: 1, checkExtension: true, qMaxDepth: 1 }, // Intermediate (default)
    4: { baseDepth: 3, extendedDepth: 2, checkExtension: true, qMaxDepth: 2 }, // Advanced
    5: { baseDepth: 4, extendedDepth: 3, checkExtension: true, qMaxDepth: 4 }, // Expert (unchanged)
};
/**
 * AI Engine class
 * Manages AI move selection and search
 */
class AIEngine {
    search;
    currentTTSize = 16;
    constructor() {
        this.search = new Search_1.Search(this.currentTTSize);
    }
    /**
     * Find the best move for the current position
     *
     * @param board - Current board state
    * @param level - AI difficulty level (1-5, default 3)
     * @param ttSizeMB - Transposition table size in MB (0 to disable, min 0.25 MB, auto-scaled by level)
     * @returns Best move found by the AI
     */
    findBestMove(board, level = 3, ttSizeMB = 16, depth, randomness) {
        const result = this.findBestMoveDetailed(board, { level, ttSizeMB, depth, analysis: false, randomness });
        return result ? result.move : null;
    }
    /**
     * Find the best move, including optional analysis (root move scores).
     *
     * Used by the public `ai(..., { analysis: true })` API.
     */
    findBestMoveDetailed(board, options = {}) {
        const level = options.level ?? 3;
        const ttSizeMB = options.ttSizeMB ?? 16;
        // Recreate search if TT size changed
        if (ttSizeMB !== this.currentTTSize) {
            this.currentTTSize = ttSizeMB;
            this.search = new Search_1.Search(ttSizeMB);
        }
        // Get depth configuration for this level, then apply overrides
        const config = LEVEL_CONFIG[level];
        const baseDepth = options.depth?.base ?? config.baseDepth;
        const extendedDepth = options.depth?.extended ?? config.extendedDepth;
        const qMaxDepth = options.depth?.quiescence ?? config.qMaxDepth;
        const checkExtension = options.depth?.check ?? config.checkExtension;
        // Pick an effective depth based on current position complexity.
        // This keeps early/midgame conservative, but lets endgames search deeper.
        const effectiveDepth = this.getAdaptiveDepth(board, baseDepth, extendedDepth);
        // On move 1 (both white and black), inject opening randomness so two AIs
        // never play the same game. All reasonable first moves score within this range.
        // Only applies when randomness was not explicitly set by the caller.
        const OPENING_RANDOMNESS = 5;
        const effectiveRandomness = options.randomness === undefined && board.fullMoveNumber === 1
            ? OPENING_RANDOMNESS
            : (options.randomness ?? 0);
        // Perform search
        return this.search.findBestMove(board, effectiveDepth, qMaxDepth, checkExtension, {
            analysis: options.analysis ?? false,
            randomness: effectiveRandomness,
        });
    }
    /**
    * Get the search depth for a given AI level
     *
    * @param level - AI level (1-5)
     * @returns Depth configuration
     */
    static getLevelDepth(level) {
        return LEVEL_CONFIG[level];
    }
    /**
     * Adaptive depth heuristic.
     *
     * Contract:
     * - Input: board + baseDepth (from level)
     * - Output: adjusted depth (>= 1)
     *
    * Heuristic goals:
    * - Never search shallower than the requested level depth.
    * - If there are very few root legal moves (tactical / constrained), allow +1.
    * - If the position is simplified (few pieces), allow +1 or +2.
     */
    getAdaptiveDepth(board, baseDepth, allowedExtendedDepth) {
        if (allowedExtendedDepth <= 0)
            return Math.max(1, baseDepth);
        // Root branching factor (legal moves only)
        const rootMoves = (0, MoveGenerator_1.generateLegalMoves)(board).length;
        // Material simplification proxy: count non-empty pieces.
        // (Mailbox is Int8Array, so iterating it is cheap.)
        let pieceCount = 0;
        for (const p of board.mailbox) {
            if (p !== types_1.Piece.EMPTY)
                pieceCount++;
        }
        let depth = baseDepth;
        // Simplified endgames: search deeper.
        // 32 pieces = starting position. Kings-only = 2.
        if (pieceCount <= 10)
            depth += 2;
        else if (pieceCount <= 18)
            depth += 1;
        // Constrained positions: deeper can be affordable and tactically valuable.
        if (rootMoves <= 12)
            depth += 1;
        // Safety rails
        if (depth < baseDepth)
            depth = baseDepth;
        if (depth < 1)
            depth = 1;
        const maxDepth = baseDepth + allowedExtendedDepth;
        if (depth > maxDepth)
            depth = maxDepth;
        return depth;
    }
}
exports.AIEngine = AIEngine;
//# sourceMappingURL=AIEngine.js.map