"use strict";
/**
 * Conversion utilities between square notation and internal indices
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.squareToIndex = squareToIndex;
exports.indexToSquare = indexToSquare;
exports.getFileIndex = getFileIndex;
exports.getRankIndex = getRankIndex;
exports.getFile = getFile;
exports.getRank = getRank;
exports.fileRankToIndex = fileRankToIndex;
exports.isValidSquare = isValidSquare;
exports.isValidIndex = isValidIndex;
exports.indexToBitboard = indexToBitboard;
exports.squareToBitboard = squareToBitboard;
exports.bitboardToIndices = bitboardToIndices;
exports.getLowestSetBit = getLowestSetBit;
exports.getHighestSetBit = getHighestSetBit;
exports.popCount = popCount;
exports.manhattanDistance = manhattanDistance;
exports.chebyshevDistance = chebyshevDistance;
exports.isOnEdge = isOnEdge;
exports.isAFile = isAFile;
exports.isHFile = isHFile;
exports.isRank1 = isRank1;
exports.isRank8 = isRank8;
const constants_1 = require("./constants");
// ==================== Square ↔ Index Conversion ====================
/**
 * Convert square notation (e.g., "A1", "E4") to square index (0-63)
 *
 * Board layout:
 * 56 57 58 59 60 61 62 63  (Rank 8) - A8 to H8
 * 48 49 50 51 52 53 54 55  (Rank 7)
 * ...
 *  8  9 10 11 12 13 14 15  (Rank 2)
 *  0  1  2  3  4  5  6  7  (Rank 1) - A1 to H1
 *
 * @param square - Square notation (case-insensitive)
 * @returns Square index (0-63)
 * @throws Error if square notation is invalid
 */
function squareToIndex(square) {
    const normalized = square.toUpperCase();
    if (normalized.length !== 2) {
        throw new Error(`Invalid square notation: ${square}`);
    }
    const file = normalized[0];
    const rank = normalized[1];
    const fileIndex = constants_1.COLUMNS.indexOf(file);
    const rankIndex = constants_1.ROWS.indexOf(rank);
    if (fileIndex === -1 || rankIndex === -1) {
        throw new Error(`Invalid square notation: ${square}`);
    }
    return (rankIndex * 8 + fileIndex);
}
/**
 * Convert square index (0-63) to square notation (e.g., "A1", "E4")
 *
 * @param index - Square index (0-63)
 * @returns Square notation in uppercase
 * @throws Error if index is out of range
 */
function indexToSquare(index) {
    if (index < 0 || index > 63) {
        throw new Error(`Invalid square index: ${index}`);
    }
    const fileIndex = index % 8;
    const rankIndex = Math.floor(index / 8);
    return `${constants_1.COLUMNS[fileIndex]}${constants_1.ROWS[rankIndex]}`;
}
// ==================== File/Rank Conversion ====================
/**
 * Get file index (0-7) from square index
 *
 * @param index - Square index (0-63)
 * @returns File index (0=A, 1=B, ..., 7=H)
 */
function getFileIndex(index) {
    return (index % 8);
}
/**
 * Get rank index (0-7) from square index
 *
 * @param index - Square index (0-63)
 * @returns Rank index (0=1, 1=2, ..., 7=8)
 */
function getRankIndex(index) {
    return Math.floor(index / 8);
}
/**
 * Get file from square notation
 *
 * @param square - Square notation (case-insensitive)
 * @returns File index (0-7)
 */
function getFile(square) {
    const normalized = square.toUpperCase();
    const fileIndex = constants_1.COLUMNS.indexOf(normalized[0]);
    if (fileIndex === -1) {
        throw new Error(`Invalid square notation: ${square}`);
    }
    return fileIndex;
}
/**
 * Get rank from square notation
 *
 * @param square - Square notation (case-insensitive)
 * @returns Rank index (0-7)
 */
function getRank(square) {
    const normalized = square.toUpperCase();
    const rankIndex = constants_1.ROWS.indexOf(normalized[1]);
    if (rankIndex === -1) {
        throw new Error(`Invalid square notation: ${square}`);
    }
    return rankIndex;
}
/**
 * Create square index from file and rank indices
 *
 * @param file - File index (0-7)
 * @param rank - Rank index (0-7)
 * @returns Square index (0-63)
 */
function fileRankToIndex(file, rank) {
    return (rank * 8 + file);
}
// ==================== Validation ====================
/**
 * Check if square notation is valid
 *
 * @param square - Square notation
 * @returns true if valid
 */
function isValidSquare(square) {
    if (typeof square !== 'string' || square.length !== 2) {
        return false;
    }
    const normalized = square.toUpperCase();
    const file = normalized[0];
    const rank = normalized[1];
    return constants_1.COLUMNS.includes(file) && constants_1.ROWS.includes(rank);
}
/**
 * Check if square index is valid
 *
 * @param index - Square index
 * @returns true if valid (0-63)
 */
function isValidIndex(index) {
    return Number.isInteger(index) && index >= 0 && index <= 63;
}
// ==================== Bitboard Helpers ====================
/**
 * Convert square index to bitboard (single bit set)
 *
 * @param index - Square index (0-63)
 * @returns Bitboard with single bit set
 */
function indexToBitboard(index) {
    return 1n << BigInt(index);
}
/**
 * Convert square notation to bitboard
 *
 * @param square - Square notation
 * @returns Bitboard with single bit set
 */
function squareToBitboard(square) {
    return indexToBitboard(squareToIndex(square));
}
/**
 * Get all set bits (square indices) from a bitboard
 *
 * @param bitboard - Bitboard to extract indices from
 * @returns Array of square indices where bits are set
 */
function bitboardToIndices(bitboard) {
    const indices = [];
    let bb = bitboard;
    while (bb !== 0n) {
        const index = getLowestSetBit(bb);
        indices.push(index);
        bb &= bb - 1n; // Clear lowest set bit
    }
    return indices;
}
// De Bruijn constant and lookup table for O(1) bit scanning
const DE_BRUIJN_64 = 0x03f79d71b4cb0a89n;
const MASK_64 = 0xffffffffffffffffn;
const DE_BRUIJN_TABLE = new Int8Array(64);
for (let i = 0; i < 64; i++) {
    DE_BRUIJN_TABLE[Number((((1n << BigInt(i)) * DE_BRUIJN_64) & MASK_64) >> 58n)] = i;
}
/**
 * Get the index of the lowest set bit in a bitboard (O(1) via De Bruijn)
 */
function getLowestSetBit(bitboard) {
    if (bitboard === 0n)
        return -1;
    const isolated = bitboard & (-bitboard);
    return DE_BRUIJN_TABLE[Number(((isolated * DE_BRUIJN_64) & MASK_64) >> 58n)];
}
/**
 * Get the index of the highest set bit in a bitboard
 */
function getHighestSetBit(bitboard) {
    if (bitboard === 0n)
        return -1;
    let bb = bitboard;
    bb |= bb >> 1n;
    bb |= bb >> 2n;
    bb |= bb >> 4n;
    bb |= bb >> 8n;
    bb |= bb >> 16n;
    bb |= bb >> 32n;
    const msb = bb - (bb >> 1n);
    return DE_BRUIJN_TABLE[Number(((msb * DE_BRUIJN_64) & MASK_64) >> 58n)];
}
/**
 * Count the number of set bits in a bitboard (population count)
 *
 * @param bitboard - Bitboard
 * @returns Number of set bits
 */
function popCount(bitboard) {
    let count = 0;
    let bb = bitboard;
    while (bb !== 0n) {
        bb &= bb - 1n; // Clear lowest set bit
        count++;
    }
    return count;
}
// ==================== Distance Calculations ====================
/**
 * Calculate Manhattan distance between two squares
 *
 * @param from - Source square index
 * @param to - Target square index
 * @returns Manhattan distance
 */
function manhattanDistance(from, to) {
    const fromFile = getFileIndex(from);
    const fromRank = getRankIndex(from);
    const toFile = getFileIndex(to);
    const toRank = getRankIndex(to);
    return Math.abs(fromFile - toFile) + Math.abs(fromRank - toRank);
}
/**
 * Calculate Chebyshev distance between two squares (king moves)
 *
 * @param from - Source square index
 * @param to - Target square index
 * @returns Chebyshev distance
 */
function chebyshevDistance(from, to) {
    const fromFile = getFileIndex(from);
    const fromRank = getRankIndex(from);
    const toFile = getFileIndex(to);
    const toRank = getRankIndex(to);
    return Math.max(Math.abs(fromFile - toFile), Math.abs(fromRank - toRank));
}
// ==================== Board Boundaries ====================
/**
 * Check if a square is on the edge of the board
 *
 * @param index - Square index
 * @returns true if on edge
 */
function isOnEdge(index) {
    const file = getFileIndex(index);
    const rank = getRankIndex(index);
    return file === 0 || file === 7 || rank === 0 || rank === 7;
}
/**
 * Check if square is on A-file
 */
function isAFile(index) {
    return getFileIndex(index) === 0;
}
/**
 * Check if square is on H-file
 */
function isHFile(index) {
    return getFileIndex(index) === 7;
}
/**
 * Check if square is on rank 1
 */
function isRank1(index) {
    return getRankIndex(index) === 0;
}
/**
 * Check if square is on rank 8
 */
function isRank8(index) {
    return getRankIndex(index) === 7;
}
//# sourceMappingURL=conversion.js.map