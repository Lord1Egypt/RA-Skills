"use strict";
/**
 * Minimal, fast negamax alpha-beta search.
 *
 * Goals:
 * - Browser-friendly: bounded work, no expensive root guardrails.
 * - Deterministic.
 * - Uses TT + basic move ordering for practical strength.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Search = void 0;
const types_1 = require("../types");
const MoveGenerator_1 = require("../core/MoveGenerator");
const Board_1 = require("../core/Board");
const AttackDetector_1 = require("../core/AttackDetector");
const conversion_1 = require("../utils/conversion");
const Evaluator_1 = require("./Evaluator");
const TranspositionTable_1 = require("./TranspositionTable");
const MoveOrdering_1 = require("./MoveOrdering");
// Keep within evaluator bounds.
const INF = Evaluator_1.SCORE_MAX;
class Search {
    nodesSearched = 0;
    qMaxDepth = 4;
    checkExtension = true;
    transpositionTable;
    killerMoves;
    constructor(ttSizeMB = 16) {
        this.transpositionTable = ttSizeMB > 0 ? new TranspositionTable_1.TranspositionTable(ttSizeMB) : null;
        this.killerMoves = new MoveOrdering_1.KillerMoves();
    }
    clear() {
        this.transpositionTable?.clear();
        this.killerMoves.clear();
    }
    findBestMove(board, baseDepth, qMaxDepth = 4, checkExtension = true, options = {}) {
        this.qMaxDepth = qMaxDepth;
        this.checkExtension = checkExtension;
        this.nodesSearched = 0;
        this.transpositionTable?.newSearch();
        this.killerMoves.clear();
        const analysis = options.analysis ?? false;
        const randomness = options.randomness ?? 0;
        const moves = (0, MoveGenerator_1.generateLegalMoves)(board);
        if (moves.length === 0) {
            const inCheck = (0, AttackDetector_1.isKingInCheck)(board);
            const score = inCheck ? (Evaluator_1.SCORE_MIN + 0) : 0;
            return { move: null, score, depth: 0, nodesSearched: this.nodesSearched };
        }
        let bestMove = null;
        let bestScore = Evaluator_1.SCORE_MIN;
        let scoredMoves;
        // Iterative deepening: search depth 1..baseDepth.
        // Populates TT progressively for better move ordering at deeper levels.
        const ASPIRATION_DELTA = 25;
        for (let d = 1; d <= baseDepth; d++) {
            // Collect root scores at final depth: for analysis or randomness (both need accurate scores)
            const collectScores = (d === baseDepth) && (randomness > 0 || analysis);
            // Aspiration window: use previous iteration's score for d >= 4
            let alpha = Evaluator_1.SCORE_MIN;
            let beta = Evaluator_1.SCORE_MAX;
            let delta = ASPIRATION_DELTA;
            if (d >= 4 && bestScore > Evaluator_1.SCORE_MIN && bestScore < Evaluator_1.SCORE_MAX) {
                alpha = (bestScore - delta);
                beta = (bestScore + delta);
            }
            // Aspiration retry loop
            let iterBestMove = null;
            let iterBestScore = Evaluator_1.SCORE_MIN;
            let iterScoredMoves = null;
            while (true) {
                const pvMove = this.transpositionTable?.getBestMove(board.zobristHash) ?? null;
                const selector = new MoveOrdering_1.MoveSelector(moves, pvMove, this.killerMoves, 0);
                iterScoredMoves = collectScores ? [] : null;
                iterBestMove = null;
                iterBestScore = Evaluator_1.SCORE_MIN;
                let iterAlpha = alpha;
                let move;
                let moveIndex = 0;
                while ((move = selector.pickNext()) !== null) {
                    if ((move.flags & types_1.MoveFlag.PROMOTION) && move.promotionPiece) {
                        const isQueenPromotion = move.promotionPiece === types_1.Piece.WHITE_QUEEN ||
                            move.promotionPiece === types_1.Piece.BLACK_QUEEN;
                        if (!isQueenPromotion)
                            continue;
                    }
                    const child = (0, Board_1.copyBoard)(board);
                    (0, MoveGenerator_1.applyMoveComplete)(child, move);
                    const extension = (this.checkExtension && child.isCheck) ? 1 : 0;
                    let score;
                    if (moveIndex === 0) {
                        score = -this.negamax(child, d - 1 + extension, -beta, -iterAlpha, 1);
                    }
                    else {
                        // PVS: zero window search first
                        score = -this.negamax(child, d - 1 + extension, -iterAlpha - 1, -iterAlpha, 1);
                        // Re-search with full window if it beats alpha
                        if (score > iterAlpha && score < beta) {
                            score = -this.negamax(child, d - 1 + extension, -beta, -iterAlpha, 1);
                        }
                    }
                    moveIndex++;
                    if (iterScoredMoves) {
                        iterScoredMoves.push({ move, score });
                    }
                    if (score > iterBestScore || iterBestMove === null) {
                        iterBestScore = score;
                        iterBestMove = move;
                    }
                    if (score > iterAlpha)
                        iterAlpha = score;
                    if (iterAlpha >= beta)
                        break;
                }
                // Check aspiration window result
                if (d >= 4 && (alpha > Evaluator_1.SCORE_MIN || beta < Evaluator_1.SCORE_MAX)) {
                    if (iterBestScore <= alpha) {
                        // Fail low - widen alpha
                        delta *= 2;
                        alpha = (delta > 400) ? Evaluator_1.SCORE_MIN : Math.max(Evaluator_1.SCORE_MIN, alpha - delta);
                        continue;
                    }
                    if (iterBestScore >= beta) {
                        // Fail high - widen beta
                        delta *= 2;
                        beta = (delta > 400) ? Evaluator_1.SCORE_MAX : Math.min(Evaluator_1.SCORE_MAX, beta + delta);
                        continue;
                    }
                }
                break;
            }
            if (iterScoredMoves) {
                iterScoredMoves.sort((a, b) => b.score - a.score);
                scoredMoves = iterScoredMoves;
                // Derive best move from the sorted array — more reliable than iterBestMove
                // because iterAlpha shifts during the loop when disablePVS is true.
                if (iterScoredMoves.length > 0) {
                    bestMove = iterScoredMoves[0].move;
                    bestScore = iterScoredMoves[0].score;
                }
            }
            else if (iterBestMove) {
                bestMove = iterBestMove;
                bestScore = iterBestScore;
            }
        }
        // Apply randomness: pick randomly among moves within `randomness` cp of the best score.
        // Locked to the same quality tier as the best move: if the best move is a capture,
        // only randomize among captures — never pick a quiet move over a winning capture.
        if (randomness > 0 && scoredMoves && scoredMoves.length > 1) {
            const threshold = bestScore - randomness;
            let candidates = scoredMoves.filter(e => e.score >= threshold);
            if (candidates.length > 1) {
                const bestIsCapture = !!(scoredMoves[0].move.flags & types_1.MoveFlag.CAPTURE);
                if (bestIsCapture) {
                    const captureCandidates = candidates.filter(e => e.move.flags & types_1.MoveFlag.CAPTURE);
                    if (captureCandidates.length > 0)
                        candidates = captureCandidates;
                }
                bestMove = candidates[Math.floor(Math.random() * candidates.length)].move;
            }
        }
        return bestMove
            ? { move: bestMove, score: bestScore, depth: baseDepth, nodesSearched: this.nodesSearched, scoredMoves }
            : null;
    }
    negamax(board, depth, alpha, beta, ply) {
        this.nodesSearched++;
        if (depth <= 0) {
            return this.quiescence(board, alpha, beta, ply, 0);
        }
        // TT probe
        const tt = this.transpositionTable;
        const hash = board.zobristHash;
        let ttMove = null;
        if (tt) {
            const entry = tt.probe(hash, depth, alpha, beta, ply);
            if (entry) {
                ttMove = entry.bestMove;
                if (entry.type === TranspositionTable_1.TTEntryType.EXACT)
                    return entry.score;
                if (entry.type === TranspositionTable_1.TTEntryType.LOWER_BOUND && entry.score >= beta)
                    return entry.score;
                if (entry.type === TranspositionTable_1.TTEntryType.UPPER_BOUND && entry.score <= alpha)
                    return entry.score;
            }
        }
        const moves = (0, MoveGenerator_1.generatePseudoLegalMoves)(board);
        const selector = new MoveOrdering_1.MoveSelector(moves, ttMove, this.killerMoves, ply);
        const startAlpha = alpha;
        let bestScore = -INF;
        let bestMove = null;
        let legalMoveCount = 0;
        let move;
        while ((move = selector.pickNext()) !== null) {
            if ((move.flags & types_1.MoveFlag.PROMOTION) && move.promotionPiece) {
                const isQueenPromotion = move.promotionPiece === types_1.Piece.WHITE_QUEEN ||
                    move.promotionPiece === types_1.Piece.BLACK_QUEEN;
                if (!isQueenPromotion)
                    continue;
            }
            const child = (0, Board_1.copyBoard)(board);
            (0, MoveGenerator_1.applyMoveComplete)(child, move);
            // Skip illegal moves (own king left in check)
            if (this.isIllegalMove(child))
                continue;
            legalMoveCount++;
            const extension = (this.checkExtension && child.isCheck) ? 1 : 0;
            let score;
            if (legalMoveCount === 1) {
                // First move (PV move): search with full window
                score = -this.negamax(child, depth - 1 + extension, -beta, -alpha, ply + 1);
            }
            else {
                // PVS: search with zero window first
                score = -this.negamax(child, depth - 1 + extension, -alpha - 1, -alpha, ply + 1);
                // Re-search with full window if it beats alpha
                if (score > alpha && score < beta) {
                    score = -this.negamax(child, depth - 1 + extension, -beta, -alpha, ply + 1);
                }
            }
            if (score > bestScore || bestMove === null) {
                bestScore = score;
                bestMove = move;
            }
            if (score > alpha)
                alpha = score;
            if (alpha >= beta) {
                this.killerMoves.store(move, ply);
                break;
            }
        }
        // No legal moves: checkmate or stalemate
        if (legalMoveCount === 0) {
            if ((0, AttackDetector_1.isKingInCheck)(board))
                return Evaluator_1.SCORE_MIN + ply;
            return 0;
        }
        // TT store
        if (tt && bestMove) {
            let type = TranspositionTable_1.TTEntryType.EXACT;
            if (bestScore <= startAlpha)
                type = TranspositionTable_1.TTEntryType.UPPER_BOUND;
            else if (bestScore >= beta)
                type = TranspositionTable_1.TTEntryType.LOWER_BOUND;
            tt.store(hash, depth, bestScore, type, bestMove, ply);
        }
        return bestScore;
    }
    quiescence(board, alpha, beta, ply, qDepth) {
        this.nodesSearched++;
        // Stand-pat: evaluate before move generation
        const standPat = Evaluator_1.Evaluator.evaluate(board, board.turn, ply);
        if (standPat >= beta)
            return standPat;
        if (standPat > alpha)
            alpha = standPat;
        if (qDepth >= this.qMaxDepth)
            return standPat;
        // Generate pseudo-legal moves, collect forcing (captures + promotions)
        const allMoves = (0, MoveGenerator_1.generatePseudoLegalMoves)(board);
        const forcingMask = types_1.MoveFlag.CAPTURE | types_1.MoveFlag.PROMOTION;
        const forcing = [];
        for (let i = 0; i < allMoves.length; i++) {
            if (allMoves[i].flags & forcingMask)
                forcing.push(allMoves[i]);
        }
        const tt = this.transpositionTable;
        const ttMove = tt ? tt.getBestMove(board.zobristHash) : null;
        const selector = new MoveOrdering_1.MoveSelector(forcing, ttMove, this.killerMoves, ply);
        let bestScore = standPat;
        let legalForcingFound = false;
        let move;
        while ((move = selector.pickNext()) !== null) {
            if ((move.flags & types_1.MoveFlag.PROMOTION) && move.promotionPiece) {
                const isQueenPromotion = move.promotionPiece === types_1.Piece.WHITE_QUEEN ||
                    move.promotionPiece === types_1.Piece.BLACK_QUEEN;
                if (!isQueenPromotion)
                    continue;
            }
            const child = (0, Board_1.copyBoard)(board);
            (0, MoveGenerator_1.applyMoveComplete)(child, move);
            // Skip illegal moves
            if (this.isIllegalMove(child))
                continue;
            legalForcingFound = true;
            const score = -this.quiescence(child, -beta, -alpha, ply + 1, qDepth + 1);
            if (score > bestScore)
                bestScore = score;
            if (score >= beta)
                return score;
            if (score > alpha)
                alpha = score;
        }
        // Mate detection: if in check and no legal forcing move, check for any legal escape
        if (!legalForcingFound && (0, AttackDetector_1.isKingInCheck)(board)) {
            for (const m of allMoves) {
                // Skip forcing moves (already checked above)
                if ((m.flags & types_1.MoveFlag.CAPTURE) || (m.flags & types_1.MoveFlag.PROMOTION))
                    continue;
                const child = (0, Board_1.copyBoard)(board);
                (0, MoveGenerator_1.applyMoveComplete)(child, m);
                if (!this.isIllegalMove(child))
                    return standPat; // Has legal quiet escape
            }
            return Evaluator_1.SCORE_MIN + ply; // Checkmate
        }
        return bestScore;
    }
    /**
     * Check if a move was illegal (left own king in check) after applyMoveComplete.
     * After applyMoveComplete, board.turn has switched, so the "previous" side
     * is the opponent of board.turn.
     */
    isIllegalMove(child) {
        const prevColor = child.turn === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
        const prevKingBB = prevColor === types_1.InternalColor.WHITE ? child.whiteKing : child.blackKing;
        if (prevKingBB === 0n)
            return false;
        const prevKingSq = (0, conversion_1.getLowestSetBit)(prevKingBB);
        return (0, AttackDetector_1.isSquareAttacked)(child, prevKingSq, child.turn);
    }
}
exports.Search = Search;
//# sourceMappingURL=Search.js.map