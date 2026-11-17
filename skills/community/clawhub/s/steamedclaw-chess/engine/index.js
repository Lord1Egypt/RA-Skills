"use strict";
/**
 * js-chess-engine v2
 *
 * Public API for chess game management
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Game = void 0;
exports.moves = moves;
exports.status = status;
exports.getFen = getFen;
exports.move = move;
exports.aiMove = aiMove;
exports.ai = ai;
const Board_1 = require("./core/Board");
const MoveGenerator_1 = require("./core/MoveGenerator");
const AttackDetector_1 = require("./core/AttackDetector");
const fen_1 = require("./utils/fen");
const conversion_1 = require("./utils/conversion");
const TranspositionTable_1 = require("./ai/TranspositionTable");
const APIAdapter_1 = require("./adapters/APIAdapter");
const AIEngine_1 = require("./ai/AIEngine");
// Export types for TypeScript users
__exportStar(require("./types"), exports);
/**
 * Main Game class - manages chess game state and moves
 */
class Game {
    board;
    history = [];
    aiEngine;
    /**
     * Create a new game
     *
     * @param configuration - Optional board configuration (JSON object, FEN string, or undefined for new game)
     */
    constructor(configuration) {
        this.aiEngine = new AIEngine_1.AIEngine();
        if (!configuration) {
            // New game with standard starting position
            this.board = (0, Board_1.createStartingBoard)();
        }
        else if (typeof configuration === 'string') {
            // FEN string
            (0, fen_1.validateFEN)(configuration);
            this.board = (0, fen_1.parseFEN)(configuration);
        }
        else {
            // BoardConfig object
            this.board = (0, APIAdapter_1.configToBoard)(configuration);
        }
    }
    /**
     * Make a move
     *
     * @param from - From square (case-insensitive, e.g., 'E2' or 'e2')
     * @param to - To square (case-insensitive, e.g., 'E4' or 'e4')
     * @returns Board configuration after the move
     */
    move(from, to) {
        const fromNorm = (0, APIAdapter_1.normalizeSquare)(from);
        const toNorm = (0, APIAdapter_1.normalizeSquare)(to);
        const fromIndex = (0, conversion_1.squareToIndex)(fromNorm);
        const toIndex = (0, conversion_1.squareToIndex)(toNorm);
        // Find the matching legal move
        const legalMoves = (0, MoveGenerator_1.generateLegalMoves)(this.board);
        const move = legalMoves.find(m => m.from === fromIndex && m.to === toIndex);
        if (!move) {
            throw new Error(`Invalid move from ${fromNorm} to ${toNorm}`);
        }
        // Record move in history
        const historyEntry = { [fromNorm]: toNorm };
        this.history.push(historyEntry);
        // Apply the move
        (0, MoveGenerator_1.applyMoveComplete)(this.board, move);
        return (0, APIAdapter_1.boardToConfig)(this.board);
    }
    /**
     * Get all legal moves, optionally filtered by from-square
     *
     * @param from - Optional from square to filter moves
     * @returns Map of from-squares to array of to-squares
     */
    moves(from) {
        if (from) {
            const fromNorm = (0, APIAdapter_1.normalizeSquare)(from);
            const fromIndex = (0, conversion_1.squareToIndex)(fromNorm);
            const pieceMoves = (0, MoveGenerator_1.getMovesForPiece)(this.board, fromIndex);
            const toSquares = (0, APIAdapter_1.movesFromSquare)(pieceMoves, fromIndex);
            return { [fromNorm]: toSquares };
        }
        else {
            const allMoves = (0, MoveGenerator_1.generateLegalMoves)(this.board);
            return (0, APIAdapter_1.movesToMap)(allMoves);
        }
    }
    /**
     * Set a piece on a square
     *
     * @param square - Square to place piece (case-insensitive)
     * @param piece - Piece symbol (K, Q, R, B, N, P, k, q, r, b, n, p)
     */
    setPiece(square, piece) {
        const squareNorm = (0, APIAdapter_1.normalizeSquare)(square);
        const squareIndex = (0, conversion_1.squareToIndex)(squareNorm);
        const pieceEnum = (0, APIAdapter_1.symbolToPiece)(piece);
        (0, Board_1.setPiece)(this.board, squareIndex, pieceEnum);
    }
    /**
     * Remove a piece from a square
     *
     * @param square - Square to remove piece from (case-insensitive)
     */
    removePiece(square) {
        const squareNorm = (0, APIAdapter_1.normalizeSquare)(square);
        const squareIndex = (0, conversion_1.squareToIndex)(squareNorm);
        (0, Board_1.removePiece)(this.board, squareIndex);
    }
    /**
     * Get move history
     *
     * @returns Array of history entries with board state after each move
     */
    getHistory() {
        const result = [];
        // Replay all moves from the beginning
        const startingBoard = typeof this.board === 'string'
            ? (0, fen_1.parseFEN)(this.board)
            : (0, Board_1.createStartingBoard)();
        const tempBoard = (0, Board_1.copyBoard)(startingBoard);
        for (const move of this.history) {
            const [from, to] = Object.entries(move)[0];
            const fromIndex = (0, conversion_1.squareToIndex)(from);
            const toIndex = (0, conversion_1.squareToIndex)(to);
            const legalMoves = (0, MoveGenerator_1.generateLegalMoves)(tempBoard);
            const matchingMove = legalMoves.find(m => m.from === fromIndex && m.to === toIndex);
            if (matchingMove) {
                (0, MoveGenerator_1.applyMoveComplete)(tempBoard, matchingMove);
                const config = (0, APIAdapter_1.boardToConfig)(tempBoard);
                result.push({ ...config, move });
            }
        }
        return result;
    }
    /**
     * Export current board state as JSON configuration
     *
     * @returns Board configuration object
     */
    exportJson() {
        const cfg = (0, APIAdapter_1.boardToConfig)(this.board);
        this.updateConfigStatusFromBoard(this.board, cfg);
        return cfg;
    }
    /**
     * Export current board state as FEN string
     *
     * @returns FEN string
     */
    exportFEN() {
        return (0, fen_1.toFEN)(this.board);
    }
    /**
     * Print board to console (Unicode chess pieces)
     */
    printToConsole() {
        process.stdout.write('\n');
        for (let rank = 7; rank >= 0; rank--) {
            process.stdout.write(`${rank + 1}`);
            for (let file = 0; file < 8; file++) {
                const index = rank * 8 + file;
                const piece = this.board.mailbox[index];
                const isWhiteSquare = (rank + file) % 2 === 0;
                const symbol = pieceToUnicode(piece, isWhiteSquare);
                process.stdout.write(symbol);
            }
            process.stdout.write('\n');
        }
        process.stdout.write(' ABCDEFGH\n');
    }
    /**
     * Make an AI move (v1 compatible - returns only the move)
     *
     * @deprecated Use `ai()` instead. This method will be removed in v3.0.0.
     * @param level - AI level (1-5, default 3)
     * @returns The played move object (e.g., {"E2": "E4"})
     */
    aiMove(level = 3) {
        // Validate level
        if (level < 1 || level > 5) {
            throw new Error('AI level must be between 1 and 5');
        }
        // Use recommended TT size for the level (browser-safe defaults)
        const ttSizeMB = (0, TranspositionTable_1.getRecommendedTTSize)(level);
        // Find best move
        const bestMove = this.aiEngine.findBestMove(this.board, level, ttSizeMB);
        if (!bestMove) {
            // No legal moves available - game must be finished (checkmate or stalemate)
            throw new Error('Game is already finished');
        }
        // Record move in history
        const fromSquare = (0, conversion_1.indexToSquare)(bestMove.from);
        const toSquare = (0, conversion_1.indexToSquare)(bestMove.to);
        const historyEntry = { [fromSquare]: toSquare };
        this.history.push(historyEntry);
        // Apply the move
        (0, MoveGenerator_1.applyMoveComplete)(this.board, bestMove);
        return historyEntry;
    }
    /**
     * Make an AI move and return both move and board state
     *
     * @param options - Optional configuration object
     * @param options.level - AI difficulty level (1-5, default: 3). Values > 5 are clamped to 5.
     * @param options.play - Whether to apply the move to the game (default: true). If false, only returns the move without modifying game state.
     * @param options.ttSizeMB - Transposition table size in MB (0 to disable, min 0.25 MB). Default: auto-scaled by level (e.g., level 3: 2 MB Node.js, 1 MB browser)
     * @param options.randomness - Centipawn threshold for move variety. The engine picks randomly
     *   among all moves scoring within this many centipawns of the best move.
     *   Makes the engine less predictable without playing blunders.
     *   Default: 0 (fully deterministic). Set to a positive value for variety.
     *
     *   Reference values:
     *     0   – fully deterministic (default; same position always plays the same move)
     *     10  – very subtle (only nearly-identical moves ever swap)
     *     30  – slight variety (moves within ~½ pawn of best may vary)
     *     80  – noticeable (moves within ~1½ pawns of best may vary; fun casual play)
     *     200 – chaotic (may play obviously weaker moves; not recommended)
     * @returns Object containing the move and board configuration (current state if play=false, updated state if play=true)
     */
    ai(options = {}) {
        const requestedLevel = options.level ?? 3;
        const level = Math.max(1, Math.min(5, requestedLevel));
        const play = options.play ?? true;
        const analysis = options.analysis ?? false;
        // Allow 0 to disable TT, or >= 0.25 MB
        // Default: auto-scaled by AI level (lower levels use less memory, higher levels use more)
        const defaultSize = (0, TranspositionTable_1.getRecommendedTTSize)(level);
        const ttSizeMB = options.ttSizeMB === 0 ? 0 : Math.max(0.25, options.ttSizeMB ?? defaultSize);
        // Validate level (requested value)
        if (requestedLevel < 1 || requestedLevel > 5) {
            throw new Error('AI level must be between 1 and 5');
        }
        // Validate depth overrides
        if (options.depth) {
            const d = options.depth;
            if (d.base !== undefined && (!Number.isInteger(d.base) || d.base < 1)) {
                throw new Error('depth.base must be an integer > 0');
            }
            if (d.extended !== undefined && (!Number.isInteger(d.extended) || d.extended < 0 || d.extended > 3)) {
                throw new Error('depth.extended must be an integer between 0 and 3');
            }
            if (d.quiescence !== undefined && (!Number.isInteger(d.quiescence) || d.quiescence < 0)) {
                throw new Error('depth.quiescence must be an integer >= 0');
            }
            if (d.check !== undefined && typeof d.check !== 'boolean') {
                throw new Error('depth.check must be a boolean');
            }
        }
        // Validate randomness
        if (options.randomness !== undefined) {
            if (typeof options.randomness !== 'number' || !isFinite(options.randomness) || options.randomness < 0) {
                throw new Error('randomness must be a non-negative number');
            }
        }
        // Find best move (optionally with analysis)
        const searchResult = analysis
            ? this.aiEngine.findBestMoveDetailed(this.board, { level: level, ttSizeMB, depth: options.depth, analysis: true, randomness: options.randomness })
            : null;
        const bestMove = searchResult ? searchResult.move : this.aiEngine.findBestMove(this.board, level, ttSizeMB, options.depth, options.randomness);
        if (!bestMove) {
            // No legal moves available - game must be finished (checkmate or stalemate)
            throw new Error('Game is already finished');
        }
        // Create move entry
        const fromSquare = (0, conversion_1.indexToSquare)(bestMove.from);
        const toSquare = (0, conversion_1.indexToSquare)(bestMove.to);
        const historyEntry = { [fromSquare]: toSquare };
        const analysisFields = (analysis && searchResult?.scoredMoves)
            ? {
                analysis: searchResult.scoredMoves.map(({ move, score }) => {
                    const from = (0, conversion_1.indexToSquare)(move.from);
                    const to = (0, conversion_1.indexToSquare)(move.to);
                    const historyMove = { [from]: to };
                    return { move: historyMove, score };
                }),
                depth: searchResult.depth,
                nodesSearched: searchResult.nodesSearched,
                bestScore: searchResult.score,
            }
            : undefined;
        if (!play) {
            // Return move without applying it, with current board state.
            // Still return a consistent status snapshot.
            const cfg = (0, APIAdapter_1.boardToConfig)(this.board);
            this.updateConfigStatusFromBoard(this.board, cfg);
            return { move: historyEntry, board: cfg, ...(analysisFields ?? {}) };
        }
        // Record move in history and apply it
        this.history.push(historyEntry);
        (0, MoveGenerator_1.applyMoveComplete)(this.board, bestMove);
        const cfg = (0, APIAdapter_1.boardToConfig)(this.board);
        this.updateConfigStatusFromBoard(this.board, cfg);
        return {
            move: historyEntry,
            board: cfg,
            ...(analysisFields ?? {}),
        };
    }
    updateConfigStatusFromBoard(board, cfg) {
        // The internal engine doesn't always keep the public BoardConfig status fields
        // (check/checkMate/staleMate/isFinished) in sync after applying a move.
        // These flags are part of the public API and are used heavily in tests.
        const inCheck = (0, AttackDetector_1.isKingInCheck)(board);
        const moves = (0, MoveGenerator_1.generateLegalMoves)(board);
        const isMate = inCheck && moves.length === 0;
        const isStalemate = !inCheck && moves.length === 0;
        cfg.check = inCheck;
        cfg.checkMate = isMate;
        cfg.staleMate = isStalemate;
        cfg.isFinished = isMate || isStalemate;
    }
}
exports.Game = Game;
/**
 * Helper function to convert piece enum to Unicode symbol for printing
 */
function pieceToUnicode(piece, isWhiteSquare) {
    const symbols = {
        0: isWhiteSquare ? '\u2588' : '\u2591', // EMPTY - filled/light block
        1: '\u2659', // WHITE_PAWN ♙
        2: '\u2658', // WHITE_KNIGHT ♘
        3: '\u2657', // WHITE_BISHOP ♗
        4: '\u2656', // WHITE_ROOK ♖
        5: '\u2655', // WHITE_QUEEN ♕
        6: '\u2654', // WHITE_KING ♔
        7: '\u265F', // BLACK_PAWN ♟
        8: '\u265E', // BLACK_KNIGHT ♞
        9: '\u265D', // BLACK_BISHOP ♝
        10: '\u265C', // BLACK_ROOK ♜
        11: '\u265B', // BLACK_QUEEN ♛
        12: '\u265A', // BLACK_KING ♚
    };
    return symbols[piece] || (isWhiteSquare ? '\u2588' : '\u2591');
}
// ==================== Stateless Functions ====================
/**
 * Get all legal moves for a position
 *
 * @param config - Board configuration or FEN string
 * @returns Map of from-squares to array of to-squares
 */
function moves(config) {
    const game = new Game(config);
    return game.moves();
}
/**
 * Get board status
 *
 * @param config - Board configuration or FEN string
 * @returns Board configuration with current status
 */
function status(config) {
    const game = new Game(config);
    return game.exportJson();
}
/**
 * Get FEN string for a position
 *
 * @param config - Board configuration or FEN string
 * @returns FEN string
 */
function getFen(config) {
    const game = new Game(config);
    return game.exportFEN();
}
/**
 * Make a move on a board
 *
 * @param config - Board configuration or FEN string
 * @param from - From square
 * @param to - To square
 * @returns Board configuration after the move
 */
function move(config, from, to) {
    const game = new Game(config);
    return game.move(from, to);
}
/**
 * Make an AI move (v1 compatible - returns only the move)
 *
 * @deprecated Use `ai()` instead. This function will be removed in v3.0.0.
 * @param config - Board configuration or FEN string
 * @param level - AI level (1-5, default 3)
 * @returns The played move object (e.g., {"E2": "E4"})
 */
function aiMove(config, level = 3) {
    const game = new Game(config);
    return game.aiMove(level);
}
/**
 * Make an AI move and return both move and board state
 *
 * @param config - Board configuration or FEN string
 * @param options - Optional configuration object
 * @param options.level - AI difficulty level (1-5, default: 3)
 * @param options.play - Whether to apply the move to the game (default: true). If false, only returns the move without modifying game state.
 * @param options.ttSizeMB - Transposition table size in MB (0 to disable, min 0.25 MB). Default: auto-scaled by level (e.g., level 3: 2 MB Node.js, 1 MB browser)
 * @returns Object containing the move and board configuration (current state if play=false, updated state if play=true)
 */
function ai(config, options = {}) {
    const game = new Game(config);
    return game.ai(options);
}
//# sourceMappingURL=index.js.map