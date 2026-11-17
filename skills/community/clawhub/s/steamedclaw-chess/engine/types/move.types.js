"use strict";
/**
 * Move-related types for js-chess-engine
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.MoveOrderType = exports.CastlingType = exports.PromotionPiece = exports.MoveFlag = void 0;
// ==================== Internal Types ====================
/**
 * Move flags for special moves
 */
var MoveFlag;
(function (MoveFlag) {
    MoveFlag[MoveFlag["NONE"] = 0] = "NONE";
    MoveFlag[MoveFlag["EN_PASSANT"] = 1] = "EN_PASSANT";
    MoveFlag[MoveFlag["CASTLING"] = 2] = "CASTLING";
    MoveFlag[MoveFlag["PROMOTION"] = 4] = "PROMOTION";
    MoveFlag[MoveFlag["PAWN_DOUBLE_PUSH"] = 8] = "PAWN_DOUBLE_PUSH";
    MoveFlag[MoveFlag["CAPTURE"] = 16] = "CAPTURE";
})(MoveFlag || (exports.MoveFlag = MoveFlag = {}));
/**
 * Promotion piece type
 */
var PromotionPiece;
(function (PromotionPiece) {
    PromotionPiece[PromotionPiece["QUEEN"] = 5] = "QUEEN";
    PromotionPiece[PromotionPiece["ROOK"] = 4] = "ROOK";
    PromotionPiece[PromotionPiece["BISHOP"] = 3] = "BISHOP";
    PromotionPiece[PromotionPiece["KNIGHT"] = 2] = "KNIGHT";
})(PromotionPiece || (exports.PromotionPiece = PromotionPiece = {}));
/**
 * Castling type
 */
var CastlingType;
(function (CastlingType) {
    CastlingType[CastlingType["NONE"] = 0] = "NONE";
    CastlingType[CastlingType["WHITE_SHORT"] = 1] = "WHITE_SHORT";
    CastlingType[CastlingType["WHITE_LONG"] = 2] = "WHITE_LONG";
    CastlingType[CastlingType["BLACK_SHORT"] = 3] = "BLACK_SHORT";
    CastlingType[CastlingType["BLACK_LONG"] = 4] = "BLACK_LONG";
})(CastlingType || (exports.CastlingType = CastlingType = {}));
/**
 * Move ordering types
 */
var MoveOrderType;
(function (MoveOrderType) {
    MoveOrderType[MoveOrderType["TT_MOVE"] = 1000000] = "TT_MOVE";
    MoveOrderType[MoveOrderType["WINNING_CAPTURE"] = 100000] = "WINNING_CAPTURE";
    MoveOrderType[MoveOrderType["KILLER_1"] = 90000] = "KILLER_1";
    MoveOrderType[MoveOrderType["KILLER_2"] = 80000] = "KILLER_2";
    MoveOrderType[MoveOrderType["HISTORY"] = 0] = "HISTORY";
    MoveOrderType[MoveOrderType["LOSING_CAPTURE"] = -10000] = "LOSING_CAPTURE";
})(MoveOrderType || (exports.MoveOrderType = MoveOrderType = {}));
//# sourceMappingURL=move.types.js.map