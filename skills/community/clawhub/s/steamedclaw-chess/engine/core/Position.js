"use strict";
/**
 * Advanced bitboard operations and position utilities
 *
 * This module provides fast bitboard manipulation for move generation
 * and attack detection.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.KNIGHT_ATTACKS = exports.KING_ATTACKS = exports.NOT_RANK_8 = exports.NOT_RANK_1 = exports.NOT_GH_FILE = exports.NOT_AB_FILE = exports.NOT_H_FILE = exports.NOT_A_FILE = exports.EDGE_MASK = exports.ANTI_DIAGONAL_MASKS = exports.DIAGONAL_MASKS = exports.RANK_MASKS = exports.FILE_MASKS = void 0;
exports.shiftNorth = shiftNorth;
exports.shiftSouth = shiftSouth;
exports.shiftEast = shiftEast;
exports.shiftWest = shiftWest;
exports.shiftNorthEast = shiftNorthEast;
exports.shiftNorthWest = shiftNorthWest;
exports.shiftSouthEast = shiftSouthEast;
exports.shiftSouthWest = shiftSouthWest;
exports.getFileMask = getFileMask;
exports.getRankMask = getRankMask;
exports.getDiagonalMask = getDiagonalMask;
exports.getAntiDiagonalMask = getAntiDiagonalMask;
exports.getRookAttacks = getRookAttacks;
exports.getBishopAttacks = getBishopAttacks;
exports.getQueenAttacks = getQueenAttacks;
exports.initializeAttackTables = initializeAttackTables;
exports.getKingAttacks = getKingAttacks;
exports.getKnightAttacks = getKnightAttacks;
exports.getWhitePawnAttacks = getWhitePawnAttacks;
exports.getBlackPawnAttacks = getBlackPawnAttacks;
exports.getWhitePawnsAttacks = getWhitePawnsAttacks;
exports.getBlackPawnsAttacks = getBlackPawnsAttacks;
const conversion_1 = require("../utils/conversion");
// ==================== Bitboard Masks ====================
/**
 * File masks (A-H files)
 */
exports.FILE_MASKS = [
    0x0101010101010101n, // A-file
    0x0202020202020202n, // B-file
    0x0404040404040404n, // C-file
    0x0808080808080808n, // D-file
    0x1010101010101010n, // E-file
    0x2020202020202020n, // F-file
    0x4040404040404040n, // G-file
    0x8080808080808080n, // H-file
];
/**
 * Rank masks (1-8 ranks)
 */
exports.RANK_MASKS = [
    0x00000000000000ffn, // Rank 1
    0x000000000000ff00n, // Rank 2
    0x0000000000ff0000n, // Rank 3
    0x00000000ff000000n, // Rank 4
    0x000000ff00000000n, // Rank 5
    0x0000ff0000000000n, // Rank 6
    0x00ff000000000000n, // Rank 7
    0xff00000000000000n, // Rank 8
];
/**
 * Diagonal masks (A1-H8 diagonals)
 */
exports.DIAGONAL_MASKS = [
    0x0000000000000001n,
    0x0000000000000102n,
    0x0000000000010204n,
    0x0000000001020408n,
    0x0000000102040810n,
    0x0000010204081020n,
    0x0001020408102040n,
    0x0102040810204080n,
    0x0204081020408000n,
    0x0408102040800000n,
    0x0810204080000000n,
    0x1020408000000000n,
    0x2040800000000000n,
    0x4080000000000000n,
    0x8000000000000000n,
];
/**
 * Anti-diagonal masks (H1-A8 diagonals)
 */
exports.ANTI_DIAGONAL_MASKS = [
    0x0000000000000080n,
    0x0000000000008040n,
    0x0000000000804020n,
    0x0000000080402010n,
    0x0000008040201008n,
    0x0000804020100804n,
    0x0080402010080402n,
    0x8040201008040201n,
    0x4020100804020100n,
    0x2010080402010000n,
    0x1008040201000000n,
    0x0804020100000000n,
    0x0402010000000000n,
    0x0201000000000000n,
    0x0100000000000000n,
];
/**
 * Edge masks
 */
exports.EDGE_MASK = 0xff818181818181ffn;
exports.NOT_A_FILE = 0xfefefefefefefefen;
exports.NOT_H_FILE = 0x7f7f7f7f7f7f7f7fn;
exports.NOT_AB_FILE = 0xfcfcfcfcfcfcfcfcn;
exports.NOT_GH_FILE = 0x3f3f3f3f3f3f3f3fn;
exports.NOT_RANK_1 = 0xffffffffffffff00n;
exports.NOT_RANK_8 = 0x00ffffffffffffffn;
// ==================== Bitboard Shifting ====================
/**
 * Shift bitboard north (towards rank 8)
 */
function shiftNorth(bb) {
    return (bb & exports.NOT_RANK_8) << 8n;
}
/**
 * Shift bitboard south (towards rank 1)
 */
function shiftSouth(bb) {
    return (bb & exports.NOT_RANK_1) >> 8n;
}
/**
 * Shift bitboard east (towards H-file)
 */
function shiftEast(bb) {
    return (bb & exports.NOT_H_FILE) << 1n;
}
/**
 * Shift bitboard west (towards A-file)
 */
function shiftWest(bb) {
    return (bb & exports.NOT_A_FILE) >> 1n;
}
/**
 * Shift bitboard north-east
 */
function shiftNorthEast(bb) {
    return (bb & exports.NOT_H_FILE & exports.NOT_RANK_8) << 9n;
}
/**
 * Shift bitboard north-west
 */
function shiftNorthWest(bb) {
    return (bb & exports.NOT_A_FILE & exports.NOT_RANK_8) << 7n;
}
/**
 * Shift bitboard south-east
 */
function shiftSouthEast(bb) {
    return (bb & exports.NOT_H_FILE & exports.NOT_RANK_1) >> 7n;
}
/**
 * Shift bitboard south-west
 */
function shiftSouthWest(bb) {
    return (bb & exports.NOT_A_FILE & exports.NOT_RANK_1) >> 9n;
}
// ==================== Square Bitboard Helpers ====================
/**
 * Get file mask for a square
 */
function getFileMask(index) {
    const file = (0, conversion_1.getFileIndex)(index);
    return exports.FILE_MASKS[file];
}
/**
 * Get rank mask for a square
 */
function getRankMask(index) {
    const rank = (0, conversion_1.getRankIndex)(index);
    return exports.RANK_MASKS[rank];
}
/**
 * Get diagonal mask for a square (A1-H8 direction)
 */
function getDiagonalMask(index) {
    const file = (0, conversion_1.getFileIndex)(index);
    const rank = (0, conversion_1.getRankIndex)(index);
    const diagonalIndex = 7 + rank - file;
    return exports.DIAGONAL_MASKS[diagonalIndex];
}
/**
 * Get anti-diagonal mask for a square (H1-A8 direction)
 */
function getAntiDiagonalMask(index) {
    const file = (0, conversion_1.getFileIndex)(index);
    const rank = (0, conversion_1.getRankIndex)(index);
    const antiDiagonalIndex = rank + file;
    return exports.ANTI_DIAGONAL_MASKS[antiDiagonalIndex];
}
// ==================== Precomputed Ray Tables ====================
// Direction indices: 0=North, 1=South, 2=East, 3=West, 4=NE, 5=NW, 6=SE, 7=SW
// "Positive" rays (toward higher bits): North(0), East(2), NE(4), NW(5)
// "Negative" rays (toward lower bits): South(1), West(3), SE(6), SW(7)
const RAY_TABLE = Array.from({ length: 8 }, () => new Array(64));
function initRayTables() {
    const directions = [8, -8, 1, -1, 9, 7, -7, -9];
    for (let dirIdx = 0; dirIdx < 8; dirIdx++) {
        const dir = directions[dirIdx];
        for (let sq = 0; sq < 64; sq++) {
            let attacks = 0n;
            let current = sq;
            while (true) {
                const next = current + dir;
                if (next < 0 || next > 63)
                    break;
                const cf = current % 8;
                const nf = next % 8;
                const fd = Math.abs(nf - cf);
                // Validate wrap: horizontal needs fd=1, vertical fd=0, diagonal fd=1
                if (dir === 1 || dir === -1) {
                    if (fd !== 1)
                        break;
                }
                else if (dir === 8 || dir === -8) {
                    if (fd !== 0)
                        break;
                }
                else {
                    if (fd !== 1)
                        break;
                }
                attacks |= 1n << BigInt(next);
                current = next;
            }
            RAY_TABLE[dirIdx][sq] = attacks;
        }
    }
}
initRayTables();
// Positive direction rays: first blocker = lowest set bit
// Negative direction rays: first blocker = highest set bit
function positiveRay(dirIdx, square, occupied) {
    const ray = RAY_TABLE[dirIdx][square];
    const blockers = ray & occupied;
    if (blockers === 0n)
        return ray;
    const first = (0, conversion_1.getLowestSetBit)(blockers);
    return ray ^ RAY_TABLE[dirIdx][first];
}
function negativeRay(dirIdx, square, occupied) {
    const ray = RAY_TABLE[dirIdx][square];
    const blockers = ray & occupied;
    if (blockers === 0n)
        return ray;
    const first = (0, conversion_1.getHighestSetBit)(blockers);
    return ray ^ RAY_TABLE[dirIdx][first];
}
function getRookAttacks(square, occupied) {
    return (positiveRay(0, square, occupied) | // North
        negativeRay(1, square, occupied) | // South
        positiveRay(2, square, occupied) | // East
        negativeRay(3, square, occupied) // West
    );
}
function getBishopAttacks(square, occupied) {
    return (positiveRay(4, square, occupied) | // NE
        positiveRay(5, square, occupied) | // NW
        negativeRay(6, square, occupied) | // SE
        negativeRay(7, square, occupied) // SW
    );
}
function getQueenAttacks(square, occupied) {
    return getRookAttacks(square, occupied) | getBishopAttacks(square, occupied);
}
// ==================== King and Knight Attacks ====================
/**
 * Pre-computed king attack bitboards for each square
 */
exports.KING_ATTACKS = new Array(64);
/**
 * Pre-computed knight attack bitboards for each square
 */
exports.KNIGHT_ATTACKS = new Array(64);
/**
 * Initialize pre-computed attack tables
 */
function initializeAttackTables() {
    // Initialize king attacks
    for (let sq = 0; sq < 64; sq++) {
        let attacks = 0n;
        const sqBit = 1n << BigInt(sq);
        // King can move one square in all 8 directions
        attacks |= shiftNorth(sqBit);
        attacks |= shiftSouth(sqBit);
        attacks |= shiftEast(sqBit);
        attacks |= shiftWest(sqBit);
        attacks |= shiftNorthEast(sqBit);
        attacks |= shiftNorthWest(sqBit);
        attacks |= shiftSouthEast(sqBit);
        attacks |= shiftSouthWest(sqBit);
        exports.KING_ATTACKS[sq] = attacks;
    }
    // Initialize knight attacks
    for (let sq = 0; sq < 64; sq++) {
        let attacks = 0n;
        const sqBit = 1n << BigInt(sq);
        // Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular
        const nnw = shiftNorth(shiftNorth(shiftWest(sqBit)));
        const nne = shiftNorth(shiftNorth(shiftEast(sqBit)));
        const nee = shiftEast(shiftEast(shiftNorth(sqBit)));
        const see = shiftEast(shiftEast(shiftSouth(sqBit)));
        const sse = shiftSouth(shiftSouth(shiftEast(sqBit)));
        const ssw = shiftSouth(shiftSouth(shiftWest(sqBit)));
        const sww = shiftWest(shiftWest(shiftSouth(sqBit)));
        const nww = shiftWest(shiftWest(shiftNorth(sqBit)));
        attacks = nnw | nne | nee | see | sse | ssw | sww | nww;
        exports.KNIGHT_ATTACKS[sq] = attacks;
    }
}
// Initialize on module load
initializeAttackTables();
/**
 * Get king attacks for a square
 */
function getKingAttacks(square) {
    const attacks = exports.KING_ATTACKS[square];
    return attacks !== undefined ? attacks : 0n;
}
/**
 * Get knight attacks for a square
 */
function getKnightAttacks(square) {
    const attacks = exports.KNIGHT_ATTACKS[square];
    return attacks !== undefined ? attacks : 0n;
}
// ==================== Pawn Attacks ====================
/**
 * Get white pawn attacks for a square
 */
function getWhitePawnAttacks(square) {
    const sqBit = 1n << BigInt(square);
    return shiftNorthEast(sqBit) | shiftNorthWest(sqBit);
}
/**
 * Get black pawn attacks for a square
 */
function getBlackPawnAttacks(square) {
    const sqBit = 1n << BigInt(square);
    return shiftSouthEast(sqBit) | shiftSouthWest(sqBit);
}
/**
 * Get all white pawn attacks from a bitboard of white pawns
 */
function getWhitePawnsAttacks(pawns) {
    return shiftNorthEast(pawns) | shiftNorthWest(pawns);
}
/**
 * Get all black pawn attacks from a bitboard of black pawns
 */
function getBlackPawnsAttacks(pawns) {
    return shiftSouthEast(pawns) | shiftSouthWest(pawns);
}
//# sourceMappingURL=Position.js.map