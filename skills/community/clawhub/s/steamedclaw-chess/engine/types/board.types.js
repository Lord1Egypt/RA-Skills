"use strict";
/**
 * Board-related types for js-chess-engine
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.InternalColor = exports.Piece = void 0;
/**
 * Internal piece representation
 */
var Piece;
(function (Piece) {
    Piece[Piece["EMPTY"] = 0] = "EMPTY";
    Piece[Piece["WHITE_PAWN"] = 1] = "WHITE_PAWN";
    Piece[Piece["WHITE_KNIGHT"] = 2] = "WHITE_KNIGHT";
    Piece[Piece["WHITE_BISHOP"] = 3] = "WHITE_BISHOP";
    Piece[Piece["WHITE_ROOK"] = 4] = "WHITE_ROOK";
    Piece[Piece["WHITE_QUEEN"] = 5] = "WHITE_QUEEN";
    Piece[Piece["WHITE_KING"] = 6] = "WHITE_KING";
    Piece[Piece["BLACK_PAWN"] = 7] = "BLACK_PAWN";
    Piece[Piece["BLACK_KNIGHT"] = 8] = "BLACK_KNIGHT";
    Piece[Piece["BLACK_BISHOP"] = 9] = "BLACK_BISHOP";
    Piece[Piece["BLACK_ROOK"] = 10] = "BLACK_ROOK";
    Piece[Piece["BLACK_QUEEN"] = 11] = "BLACK_QUEEN";
    Piece[Piece["BLACK_KING"] = 12] = "BLACK_KING";
})(Piece || (exports.Piece = Piece = {}));
/**
 * Internal color representation
 */
var InternalColor;
(function (InternalColor) {
    InternalColor[InternalColor["WHITE"] = 0] = "WHITE";
    InternalColor[InternalColor["BLACK"] = 1] = "BLACK";
})(InternalColor || (exports.InternalColor = InternalColor = {}));
//# sourceMappingURL=board.types.js.map