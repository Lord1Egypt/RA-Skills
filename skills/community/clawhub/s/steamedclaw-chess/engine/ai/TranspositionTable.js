"use strict";
/**
 * Transposition Table for js-chess-engine v2
 *
 * Stores previously evaluated positions to avoid re-computation.
 * Uses Zobrist hashing for position identification.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TranspositionTable = exports.TTEntryType = void 0;
exports.getRecommendedTTSize = getRecommendedTTSize;
const Evaluator_1 = require("./Evaluator");
const environment_1 = require("../utils/environment");
/** Threshold for detecting mate scores. */
const MATE_THRESHOLD = 500;
/**
 * Get recommended TT size for a given AI level and environment
 *
 * NOTE: TT size directly affects AI strength. Larger TT = better move ordering
 * and fewer re-searches, which improves play quality at higher depths.
 *
 * @param level - AI difficulty level (1-5)
 * @returns Recommended TT size in MB
 */
function getRecommendedTTSize(level) {
    if ((0, environment_1.isNodeEnvironment)()) {
        // Node.js - more generous memory allocation
        const nodeSizes = {
            1: 0.5, // Level 1: 0.5 MB
            2: 1, // Level 2: 1 MB
            3: 4, // Level 3: 4 MB (default)
            4: 16, // Level 4: 16 MB
            5: 40, // Level 5: 40 MB
        };
        return nodeSizes[level] ?? 4;
    }
    else {
        // Browser - modern-device-friendly allocation (reasonable for 2024+ devices)
        const browserSizes = {
            1: 0.25, // Level 1: 0.25 MB (ultra-lightweight)
            2: 0.5, // Level 2: 0.5 MB (mobile-friendly)
            3: 2, // Level 3: 2 MB (balanced default)
            4: 8, // Level 4: 8 MB (strong performance)
            5: 20, // Level 5: 20 MB (maximum strength)
        };
        return browserSizes[level] ?? 2;
    }
}
/**
 * Normalize a mate score for TT storage by removing the current ply component.
 * Mate scores use SCORE_MIN + ply (mated) or SCORE_MAX - ply (mating).
 * We store the distance-from-this-node instead.
 */
function adjustMateScoreForStorage(score, ply) {
    if (score > Evaluator_1.SCORE_MAX - MATE_THRESHOLD)
        return score + ply;
    if (score < Evaluator_1.SCORE_MIN + MATE_THRESHOLD)
        return score - ply;
    return score;
}
/**
 * Denormalize a mate score retrieved from TT by adding the current ply.
 */
function adjustMateScoreForRetrieval(score, ply) {
    if (score > Evaluator_1.SCORE_MAX - MATE_THRESHOLD)
        return score - ply;
    if (score < Evaluator_1.SCORE_MIN + MATE_THRESHOLD)
        return score + ply;
    return score;
}
/**
 * Types of transposition table entries
 */
var TTEntryType;
(function (TTEntryType) {
    TTEntryType[TTEntryType["EXACT"] = 0] = "EXACT";
    TTEntryType[TTEntryType["LOWER_BOUND"] = 1] = "LOWER_BOUND";
    TTEntryType[TTEntryType["UPPER_BOUND"] = 2] = "UPPER_BOUND";
})(TTEntryType || (exports.TTEntryType = TTEntryType = {}));
/**
 * Transposition Table
 *
 * Implements a hash table with replacement strategy for storing
 * previously evaluated positions.
 */
class TranspositionTable {
    table;
    size;
    currentAge = 0;
    hits = 0;
    misses = 0;
    /**
     * Create a new transposition table
     *
     * @param sizeMB - Size in megabytes (default: 16MB)
     */
    constructor(sizeMB = 16) {
        // Each entry is approximately 40 bytes
        const entrySize = 40;
        const bytesPerMB = 1024 * 1024;
        const totalBytes = sizeMB * bytesPerMB;
        // Use power of 2 for efficient modulo with bitwise AND
        this.size = Math.pow(2, Math.floor(Math.log2(totalBytes / entrySize)));
        this.table = new Array(this.size).fill(null);
    }
    /**
     * Store a position in the transposition table
     *
     * @param zobristHash - Position hash
     * @param depth - Search depth
     * @param score - Position score
     * @param type - Entry type
     * @param bestMove - Best move found
     */
    store(zobristHash, depth, score, type, bestMove, ply = 0) {
        const index = this.getIndex(zobristHash);
        const existingEntry = this.table[index];
        // Replacement strategy: always replace if:
        // 1. Slot is empty
        // 2. Same position (hash match)
        // 3. New entry has greater depth
        // 4. Entry is from previous search (old age)
        const shouldReplace = !existingEntry ||
            existingEntry.zobristHash === zobristHash ||
            depth >= existingEntry.depth ||
            existingEntry.age < this.currentAge;
        if (shouldReplace) {
            this.table[index] = {
                zobristHash,
                depth,
                score: adjustMateScoreForStorage(score, ply),
                type,
                bestMove,
                age: this.currentAge,
            };
        }
    }
    /**
     * Probe the transposition table
     *
     * @param zobristHash - Position hash
     * @param depth - Current search depth
     * @param alpha - Alpha bound
     * @param beta - Beta bound
     * @returns Entry if found and usable, null otherwise
     */
    probe(zobristHash, depth, alpha, beta, ply = 0) {
        const index = this.getIndex(zobristHash);
        const entry = this.table[index];
        // Check if entry exists and matches hash
        if (!entry || entry.zobristHash !== zobristHash) {
            this.misses++;
            return null;
        }
        // Entry must be from sufficient depth to be usable
        if (entry.depth < depth) {
            this.misses++;
            return null;
        }
        // Adjust mate scores for the current ply
        const adjustedScore = adjustMateScoreForRetrieval(entry.score, ply);
        // Count hits only when usable for pruning / exact score.
        switch (entry.type) {
            case TTEntryType.EXACT:
                this.hits++;
                return { ...entry, score: adjustedScore };
            case TTEntryType.LOWER_BOUND:
                // Fail-high (score >= beta)
                if (adjustedScore >= beta) {
                    this.hits++;
                    return { ...entry, score: adjustedScore };
                }
                break;
            case TTEntryType.UPPER_BOUND:
                // Fail-low (score <= alpha)
                if (adjustedScore <= alpha) {
                    this.hits++;
                    return { ...entry, score: adjustedScore };
                }
                break;
        }
        // Not usable for pruning, but still return for move ordering.
        return { ...entry, score: adjustedScore };
    }
    /**
     * Get best move from transposition table (for move ordering)
     *
     * @param zobristHash - Position hash
     * @returns Best move if found, null otherwise
     */
    getBestMove(zobristHash) {
        const index = this.getIndex(zobristHash);
        const entry = this.table[index];
        if (entry && entry.zobristHash === zobristHash) {
            return entry.bestMove;
        }
        return null;
    }
    /**
     * Clear the transposition table
     */
    clear() {
        this.table.fill(null);
        this.currentAge = 0;
        this.hits = 0;
        this.misses = 0;
    }
    /**
     * Increment search age (call at start of new search)
     */
    newSearch() {
        this.currentAge++;
    }
    /**
     * Get index for a hash value
     *
     * @param hash - Zobrist hash
     * @returns Table index
     */
    getIndex(hash) {
        // Use bitwise AND for fast modulo with power of 2
        return Number(hash & BigInt(this.size - 1));
    }
    /**
     * Get cache statistics
     *
     * @returns Statistics object
     */
    getStats() {
        const total = this.hits + this.misses;
        const hitRate = total > 0 ? this.hits / total : 0;
        return {
            hits: this.hits,
            misses: this.misses,
            hitRate,
            size: this.size,
        };
    }
}
exports.TranspositionTable = TranspositionTable;
//# sourceMappingURL=TranspositionTable.js.map