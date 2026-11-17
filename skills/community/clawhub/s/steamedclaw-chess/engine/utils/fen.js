"use strict";
/**
 * FEN (Forsyth-Edwards Notation) parser and formatter
 *
 * FEN format: pieces turn castling enPassant halfMove fullMove
 * Example: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseFEN = parseFEN;
exports.validateFEN = validateFEN;
exports.toFEN = toFEN;
exports.getStartingFEN = getStartingFEN;
const types_1 = require("../types");
const Board_1 = require("../core/Board");
const AttackDetector_1 = require("../core/AttackDetector");
const zobrist_1 = require("../core/zobrist");
const conversion_1 = require("./conversion");
const FEN_CASTLING_RE = /^(-|[KQkq]{1,4})$/;
const FEN_EN_PASSANT_RE = /^(-|[a-h][36])$/;
/**
 * Parse a FEN string into an internal board
 *
 * @param fen - FEN string
 * @returns Internal board representation
 */
function parseFEN(fen) {
    const parts = fen.trim().split(/\s+/);
    if (parts.length !== 6) {
        throw new Error(`Invalid FEN: expected 6 parts, got ${parts.length}`);
    }
    const [piecePlacement, activeColor, castling, enPassant, halfMove, fullMove] = parts;
    const board = (0, Board_1.createEmptyBoard)();
    // Parse piece placement (ranks 8 to 1, separated by /)
    const ranks = piecePlacement.split('/');
    if (ranks.length !== 8) {
        throw new Error(`Invalid FEN: expected 8 ranks, got ${ranks.length}`);
    }
    for (let rank = 0; rank < 8; rank++) {
        const rankStr = ranks[rank];
        let file = 0;
        for (const char of rankStr) {
            if (char >= '1' && char <= '8') {
                // Empty squares
                file += parseInt(char, 10);
            }
            else {
                // Piece
                const piece = fenCharToPiece(char);
                if (piece === null) {
                    throw new Error(`Invalid FEN: unknown piece character '${char}'`);
                }
                // Convert rank/file to square index
                // FEN ranks go from 8 to 1 (top to bottom)
                // Our indices go from 0 to 63 (bottom to top, left to right)
                const squareIndex = (7 - rank) * 8 + file;
                (0, Board_1.setPiece)(board, squareIndex, piece);
                file++;
            }
        }
        if (file !== 8) {
            throw new Error(`Invalid FEN: rank ${8 - rank} has ${file} files instead of 8`);
        }
    }
    // Validate piece placement has exactly one king of each color
    let whiteKings = 0;
    let blackKings = 0;
    for (const p of board.mailbox) {
        if (p === types_1.Piece.WHITE_KING)
            whiteKings++;
        if (p === types_1.Piece.BLACK_KING)
            blackKings++;
    }
    if (whiteKings !== 1 || blackKings !== 1) {
        throw new Error(`Invalid FEN: expected exactly one white king and one black king`);
    }
    // Parse active color
    if (activeColor === 'w') {
        board.turn = types_1.InternalColor.WHITE;
    }
    else if (activeColor === 'b') {
        board.turn = types_1.InternalColor.BLACK;
    }
    else {
        throw new Error(`Invalid FEN: unknown active color '${activeColor}'`);
    }
    // Validate castling rights string
    if (!FEN_CASTLING_RE.test(castling)) {
        throw new Error(`Invalid FEN: invalid castling rights '${castling}'`);
    }
    if (castling !== '-') {
        const unique = new Set(castling.split(''));
        if (unique.size !== castling.length) {
            throw new Error(`Invalid FEN: duplicate castling rights '${castling}'`);
        }
    }
    // Parse castling rights
    board.castlingRights.whiteShort = castling.includes('K');
    board.castlingRights.whiteLong = castling.includes('Q');
    board.castlingRights.blackShort = castling.includes('k');
    board.castlingRights.blackLong = castling.includes('q');
    // Parse en passant square
    if (!FEN_EN_PASSANT_RE.test(enPassant)) {
        throw new Error(`Invalid FEN: invalid en passant square '${enPassant}'`);
    }
    if (enPassant !== '-') {
        // enPassant is lowercase by regex; squareToIndex expects uppercase.
        board.enPassantSquare = (0, conversion_1.squareToIndex)(enPassant.toUpperCase());
    }
    // Parse half-move clock (for 50-move rule)
    board.halfMoveClock = parseInt(halfMove, 10);
    if (isNaN(board.halfMoveClock)) {
        throw new Error(`Invalid FEN: invalid half-move clock '${halfMove}'`);
    }
    if (board.halfMoveClock < 0) {
        throw new Error(`Invalid FEN: half-move clock must be >= 0`);
    }
    // Parse full move number
    board.fullMoveNumber = parseInt(fullMove, 10);
    if (isNaN(board.fullMoveNumber)) {
        throw new Error(`Invalid FEN: invalid full move number '${fullMove}'`);
    }
    if (board.fullMoveNumber < 1) {
        throw new Error(`Invalid FEN: full move number must be >= 1`);
    }
    // Keep zobristHash consistent for TT caching.
    board.zobristHash = (0, zobrist_1.computeZobristHash)(board);
    // Basic legality: it cannot be the case that the side who is NOT to move is in check.
    // Example: a FEN that has "w" to move while black is already in check is not a reachable
    // game state in standard chess.
    // (The side in check must be the side to move.)
    const notToMove = board.turn === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
    const originalTurn = board.turn;
    try {
        board.turn = notToMove;
        if ((0, AttackDetector_1.isKingInCheck)(board)) {
            const side = notToMove === types_1.InternalColor.WHITE ? 'white' : 'black';
            throw new Error(`Invalid FEN: ${side} is in check but it is not ${side}'s turn`);
        }
    }
    finally {
        board.turn = originalTurn;
    }
    return board;
}
/**
 * Validate a FEN string.
 *
 * This is intended for user-provided input. It throws with a descriptive message
 * when the FEN is invalid.
 */
function validateFEN(fen) {
    // parseFEN already performs full validation and throws on any error.
    parseFEN(fen);
}
/**
 * Convert an internal board to a FEN string
 *
 * @param board - Internal board
 * @returns FEN string
 */
function toFEN(board) {
    const parts = [];
    // 1. Piece placement (ranks 8 to 1)
    const rankStrings = [];
    for (let rank = 7; rank >= 0; rank--) {
        let rankStr = '';
        let emptyCount = 0;
        for (let file = 0; file < 8; file++) {
            const squareIndex = rank * 8 + file;
            const piece = board.mailbox[squareIndex];
            if (piece === types_1.Piece.EMPTY) {
                emptyCount++;
            }
            else {
                if (emptyCount > 0) {
                    rankStr += emptyCount.toString();
                    emptyCount = 0;
                }
                rankStr += pieceToFenChar(piece);
            }
        }
        if (emptyCount > 0) {
            rankStr += emptyCount.toString();
        }
        rankStrings.push(rankStr);
    }
    parts.push(rankStrings.join('/'));
    // 2. Active color
    parts.push(board.turn === types_1.InternalColor.WHITE ? 'w' : 'b');
    // 3. Castling rights
    let castling = '';
    if (board.castlingRights.whiteShort)
        castling += 'K';
    if (board.castlingRights.whiteLong)
        castling += 'Q';
    if (board.castlingRights.blackShort)
        castling += 'k';
    if (board.castlingRights.blackLong)
        castling += 'q';
    parts.push(castling || '-');
    // 4. En passant square
    if (board.enPassantSquare !== null) {
        parts.push((0, conversion_1.indexToSquare)(board.enPassantSquare).toLowerCase());
    }
    else {
        parts.push('-');
    }
    // 5. Half-move clock
    parts.push(board.halfMoveClock.toString());
    // 6. Full move number
    parts.push(board.fullMoveNumber.toString());
    return parts.join(' ');
}
/**
 * Convert a FEN character to a piece enum
 *
 * @param char - FEN character (K, Q, R, B, N, P, k, q, r, b, n, p)
 * @returns Piece enum value or null if invalid
 */
function fenCharToPiece(char) {
    switch (char) {
        case 'K': return types_1.Piece.WHITE_KING;
        case 'Q': return types_1.Piece.WHITE_QUEEN;
        case 'R': return types_1.Piece.WHITE_ROOK;
        case 'B': return types_1.Piece.WHITE_BISHOP;
        case 'N': return types_1.Piece.WHITE_KNIGHT;
        case 'P': return types_1.Piece.WHITE_PAWN;
        case 'k': return types_1.Piece.BLACK_KING;
        case 'q': return types_1.Piece.BLACK_QUEEN;
        case 'r': return types_1.Piece.BLACK_ROOK;
        case 'b': return types_1.Piece.BLACK_BISHOP;
        case 'n': return types_1.Piece.BLACK_KNIGHT;
        case 'p': return types_1.Piece.BLACK_PAWN;
        default: return null;
    }
}
/**
 * Convert a piece enum to a FEN character
 *
 * @param piece - Piece enum value
 * @returns FEN character
 */
function pieceToFenChar(piece) {
    switch (piece) {
        case types_1.Piece.WHITE_KING: return 'K';
        case types_1.Piece.WHITE_QUEEN: return 'Q';
        case types_1.Piece.WHITE_ROOK: return 'R';
        case types_1.Piece.WHITE_BISHOP: return 'B';
        case types_1.Piece.WHITE_KNIGHT: return 'N';
        case types_1.Piece.WHITE_PAWN: return 'P';
        case types_1.Piece.BLACK_KING: return 'k';
        case types_1.Piece.BLACK_QUEEN: return 'q';
        case types_1.Piece.BLACK_ROOK: return 'r';
        case types_1.Piece.BLACK_BISHOP: return 'b';
        case types_1.Piece.BLACK_KNIGHT: return 'n';
        case types_1.Piece.BLACK_PAWN: return 'p';
        default: return '';
    }
}
/**
 * Get FEN for starting position
 *
 * @returns FEN string for standard chess starting position
 */
function getStartingFEN() {
    return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
}
//# sourceMappingURL=fen.js.map