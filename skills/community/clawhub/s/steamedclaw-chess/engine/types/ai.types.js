"use strict";
/**
 * AI and search-related types for js-chess-engine
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TTEntryType = void 0;
// ==================== Transposition Table Types ====================
/**
 * Transposition table entry type
 */
var TTEntryType;
(function (TTEntryType) {
    TTEntryType[TTEntryType["EXACT"] = 0] = "EXACT";
    TTEntryType[TTEntryType["LOWERBOUND"] = 1] = "LOWERBOUND";
    TTEntryType[TTEntryType["UPPERBOUND"] = 2] = "UPPERBOUND";
})(TTEntryType || (exports.TTEntryType = TTEntryType = {}));
//# sourceMappingURL=ai.types.js.map