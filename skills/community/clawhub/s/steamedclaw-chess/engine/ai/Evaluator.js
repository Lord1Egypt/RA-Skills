"use strict";
/**
 * Fast, deterministic evaluation.
 *
 * Design goals:
 * - Cheap (called at every leaf).
 * - Stable (no expensive strategic features).
 * - Returns a score from the perspective of `playerColor`.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Evaluator = exports.SCORE_MAX = exports.SCORE_MIN = void 0;
const types_1 = require("../types");
// Mate bounds used by search.
exports.SCORE_MIN = -1_000_000;
exports.SCORE_MAX = 1_000_000;
// Basic piece values (centipawns)
const V = {
    [types_1.Piece.EMPTY]: 0,
    [types_1.Piece.WHITE_PAWN]: 100,
    [types_1.Piece.BLACK_PAWN]: 100,
    [types_1.Piece.WHITE_KNIGHT]: 320,
    [types_1.Piece.BLACK_KNIGHT]: 320,
    [types_1.Piece.WHITE_BISHOP]: 320,
    [types_1.Piece.BLACK_BISHOP]: 320,
    [types_1.Piece.WHITE_ROOK]: 500,
    [types_1.Piece.BLACK_ROOK]: 500,
    [types_1.Piece.WHITE_QUEEN]: 900,
    [types_1.Piece.BLACK_QUEEN]: 900,
    [types_1.Piece.WHITE_KING]: 0,
    [types_1.Piece.BLACK_KING]: 0,
};
// Tiny PSTs (values from White perspective, A1..H8).
const PST_PAWN = new Int16Array([
    0, 0, 0, 0, 0, 0, 0, 0,
    10, 10, 10, 10, 10, 10, 10, 10,
    2, 2, 4, 6, 6, 4, 2, 2,
    1, 1, 2, 8, 8, 2, 1, 1,
    0, 0, 0, 6, 6, 0, 0, 0,
    1, 1, 1, -2, -2, 1, 1, 1,
    1, 1, 1, -4, -4, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0,
]);
const PST_KNIGHT = new Int16Array([
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 6, 6, 5, 0, -10,
    -10, 2, 6, 8, 8, 6, 2, -10,
    -10, 0, 6, 8, 8, 6, 0, -10,
    -10, 2, 4, 6, 6, 4, 2, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]);
const PST_BISHOP = new Int16Array([
    -10, -5, -5, -5, -5, -5, -5, -10,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 3, 5, 5, 3, 0, -5,
    -5, 2, 5, 7, 7, 5, 2, -5,
    -5, 0, 5, 7, 7, 5, 0, -5,
    -5, 2, 3, 5, 5, 3, 2, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -10, -5, -5, -5, -5, -5, -5, -10,
]);
const PST_ROOK = new Int16Array([
    0, 0, 2, 4, 4, 2, 0, 0,
    0, 0, 2, 4, 4, 2, 0, 0,
    0, 0, 2, 4, 4, 2, 0, 0,
    0, 0, 2, 4, 4, 2, 0, 0,
    0, 0, 2, 4, 4, 2, 0, 0,
    2, 2, 4, 6, 6, 4, 2, 2,
    5, 5, 5, 7, 7, 5, 5, 5,
    0, 0, 2, 4, 4, 2, 0, 0,
]);
const PST_QUEEN = new Int16Array([
    -10, -5, -5, -2, -2, -5, -5, -10,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 2, 2, 2, 2, 0, -5,
    -2, 0, 2, 3, 3, 2, 0, -2,
    -2, 0, 2, 3, 3, 2, 0, -2,
    -5, 0, 2, 2, 2, 2, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -10, -5, -5, -2, -2, -5, -5, -10,
]);
const PST_KING = new Int16Array([
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    10, 10, 0, 0, 0, 0, 10, 10,
    20, 30, 10, 0, 0, 10, 30, 20,
]);
function mirrorSquare(sq) {
    const rank = (sq / 8) | 0;
    const file = sq & 7;
    return (7 - rank) * 8 + file;
}
function pst(piece, square) {
    const isWhite = piece >= types_1.Piece.WHITE_PAWN && piece <= types_1.Piece.WHITE_KING;
    const sq = isWhite ? mirrorSquare(square) : square;
    switch (piece) {
        case types_1.Piece.WHITE_PAWN:
        case types_1.Piece.BLACK_PAWN:
            return PST_PAWN[sq];
        case types_1.Piece.WHITE_KNIGHT:
        case types_1.Piece.BLACK_KNIGHT:
            return PST_KNIGHT[sq];
        case types_1.Piece.WHITE_BISHOP:
        case types_1.Piece.BLACK_BISHOP:
            return PST_BISHOP[sq];
        case types_1.Piece.WHITE_ROOK:
        case types_1.Piece.BLACK_ROOK:
            return PST_ROOK[sq];
        case types_1.Piece.WHITE_QUEEN:
        case types_1.Piece.BLACK_QUEEN:
            return PST_QUEEN[sq];
        case types_1.Piece.WHITE_KING:
        case types_1.Piece.BLACK_KING:
            return PST_KING[sq];
        default:
            return 0;
    }
}
class Evaluator {
    static evaluate(board, playerColor, plyFromRoot = 0) {
        if (board.isCheckmate) {
            const losing = board.turn === playerColor;
            return losing ? (exports.SCORE_MIN + plyFromRoot) : (exports.SCORE_MAX - plyFromRoot);
        }
        if (board.isStalemate)
            return 0;
        let white = 0;
        let black = 0;
        const mb = board.mailbox;
        for (let sq = 0; sq < 64; sq++) {
            const p = mb[sq];
            if (!p)
                continue;
            const val = (V[p] ?? 0) + pst(p, sq);
            if (p <= types_1.Piece.WHITE_KING)
                white += val;
            else
                black += val;
        }
        const scoreFromWhite = white - black;
        return playerColor === types_1.InternalColor.WHITE ? scoreFromWhite : -scoreFromWhite;
    }
}
exports.Evaluator = Evaluator;
//# sourceMappingURL=Evaluator.js.map