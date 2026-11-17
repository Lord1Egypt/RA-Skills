"use strict";
/**
 * Attack detection for chess positions
 *
 * This module provides fast attack detection using bitboards for:
 * - Checking if a square is under attack
 * - Detecting check and checkmate
 * - Generating attack bitboards
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.isSquareAttacked = isSquareAttacked;
exports.isKingInCheck = isKingInCheck;
exports.getAttackedSquares = getAttackedSquares;
exports.getAttackers = getAttackers;
exports.wouldLeaveKingInCheck = wouldLeaveKingInCheck;
const types_1 = require("../types");
const Position_1 = require("./Position");
const conversion_1 = require("../utils/conversion");
/**
 * Check if a square is attacked by a specific color
 *
 * @param board - Board to check
 * @param square - Square index to check
 * @param attackerColor - Color of attacking pieces
 * @returns true if square is attacked by attackerColor
 */
function isSquareAttacked(board, square, attackerColor) {
    const attackers = attackerColor === types_1.InternalColor.WHITE ? board.whitePieces : board.blackPieces;
    // Check pawn attacks
    // IMPORTANT: `getWhitePawnAttacks(square)` returns the squares a *white pawn on `square`*
    // would attack (north-east/north-west). For attack detection we need the inverse mapping:
    // which pawn squares could attack `square`.
    // That means:
    //  - to see if `square` is attacked by WHITE pawns, look for WHITE pawns on the squares
    //    that a BLACK pawn from `square` would attack (south-east/south-west), i.e. potential
    //    white pawn origins.
    //  - to see if `square` is attacked by BLACK pawns, look for BLACK pawns on the squares
    //    that a WHITE pawn from `square` would attack (north-east/north-west), i.e. potential
    //    black pawn origins.
    const pawnAttackOrigins = attackerColor === types_1.InternalColor.WHITE
        ? (0, Position_1.getBlackPawnAttacks)(square)
        : (0, Position_1.getWhitePawnAttacks)(square);
    const pawns = attackerColor === types_1.InternalColor.WHITE ? board.whitePawns : board.blackPawns;
    if ((pawnAttackOrigins & pawns) !== 0n) {
        return true;
    }
    // Check knight attacks
    const knightAttacks = (0, Position_1.getKnightAttacks)(square);
    const knights = attackerColor === types_1.InternalColor.WHITE ? board.whiteKnights : board.blackKnights;
    if ((knightAttacks & knights) !== 0n) {
        return true;
    }
    // Check bishop and queen diagonal attacks
    const bishopAttacks = (0, Position_1.getBishopAttacks)(square, board.allPieces);
    const bishops = attackerColor === types_1.InternalColor.WHITE ? board.whiteBishops : board.blackBishops;
    const queens = attackerColor === types_1.InternalColor.WHITE ? board.whiteQueens : board.blackQueens;
    if ((bishopAttacks & (bishops | queens)) !== 0n) {
        return true;
    }
    // Check rook and queen straight attacks
    const rookAttacks = (0, Position_1.getRookAttacks)(square, board.allPieces);
    const rooks = attackerColor === types_1.InternalColor.WHITE ? board.whiteRooks : board.blackRooks;
    if ((rookAttacks & (rooks | queens)) !== 0n) {
        return true;
    }
    // Check king attacks
    const kingAttacks = (0, Position_1.getKingAttacks)(square);
    const king = attackerColor === types_1.InternalColor.WHITE ? board.whiteKing : board.blackKing;
    if ((kingAttacks & king) !== 0n) {
        return true;
    }
    return false;
}
/**
 * Check if the current player's king is in check
 *
 * @param board - Board to check
 * @returns true if king is in check
 */
function isKingInCheck(board) {
    const kingBitboard = board.turn === types_1.InternalColor.WHITE ? board.whiteKing : board.blackKing;
    if (kingBitboard === 0n) {
        return false; // No king (shouldn't happen in real game)
    }
    const kingSquare = (0, conversion_1.getLowestSetBit)(kingBitboard);
    const opponentColor = board.turn === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
    return isSquareAttacked(board, kingSquare, opponentColor);
}
/**
 * Get all squares attacked by a specific color
 *
 * @param board - Board to check
 * @param attackerColor - Color of attacking pieces
 * @returns Bitboard of all attacked squares
 */
function getAttackedSquares(board, attackerColor) {
    let attacked = 0n;
    // Pawn attacks
    const pawns = attackerColor === types_1.InternalColor.WHITE ? board.whitePawns : board.blackPawns;
    if (attackerColor === types_1.InternalColor.WHITE) {
        // White pawns attack north-east and north-west
        attacked |= ((pawns & 0xfefefefefefefefen) << 9n); // North-East (not on H-file)
        attacked |= ((pawns & 0x7f7f7f7f7f7f7f7fn) << 7n); // North-West (not on A-file)
    }
    else {
        // Black pawns attack south-east and south-west
        attacked |= ((pawns & 0xfefefefefefefefen) >> 7n); // South-East (not on H-file)
        attacked |= ((pawns & 0x7f7f7f7f7f7f7f7fn) >> 9n); // South-West (not on A-file)
    }
    // Knight attacks
    const knights = attackerColor === types_1.InternalColor.WHITE ? board.whiteKnights : board.blackKnights;
    let knightsBB = knights;
    while (knightsBB !== 0n) {
        const sq = (0, conversion_1.getLowestSetBit)(knightsBB);
        attacked |= (0, Position_1.getKnightAttacks)(sq);
        knightsBB &= knightsBB - 1n; // Clear lowest bit
    }
    // Bishop attacks
    const bishops = attackerColor === types_1.InternalColor.WHITE ? board.whiteBishops : board.blackBishops;
    let bishopsBB = bishops;
    while (bishopsBB !== 0n) {
        const sq = (0, conversion_1.getLowestSetBit)(bishopsBB);
        attacked |= (0, Position_1.getBishopAttacks)(sq, board.allPieces);
        bishopsBB &= bishopsBB - 1n;
    }
    // Rook attacks
    const rooks = attackerColor === types_1.InternalColor.WHITE ? board.whiteRooks : board.blackRooks;
    let rooksBB = rooks;
    while (rooksBB !== 0n) {
        const sq = (0, conversion_1.getLowestSetBit)(rooksBB);
        attacked |= (0, Position_1.getRookAttacks)(sq, board.allPieces);
        rooksBB &= rooksBB - 1n;
    }
    // Queen attacks
    const queens = attackerColor === types_1.InternalColor.WHITE ? board.whiteQueens : board.blackQueens;
    let queensBB = queens;
    while (queensBB !== 0n) {
        const sq = (0, conversion_1.getLowestSetBit)(queensBB);
        attacked |= (0, Position_1.getQueenAttacks)(sq, board.allPieces);
        queensBB &= queensBB - 1n;
    }
    // King attacks
    const king = attackerColor === types_1.InternalColor.WHITE ? board.whiteKing : board.blackKing;
    if (king !== 0n) {
        const kingSquare = (0, conversion_1.getLowestSetBit)(king);
        attacked |= (0, Position_1.getKingAttacks)(kingSquare);
    }
    return attacked;
}
/**
 * Get all pieces attacking a specific square
 *
 * @param board - Board to check
 * @param square - Square being attacked
 * @param attackerColor - Color of attacking pieces
 * @returns Bitboard of all pieces attacking the square
 */
function getAttackers(board, square, attackerColor) {
    let attackers = 0n;
    // Pawn attackers
    const pawnAttackOrigins = attackerColor === types_1.InternalColor.WHITE
        ? (0, Position_1.getBlackPawnAttacks)(square)
        : (0, Position_1.getWhitePawnAttacks)(square);
    const pawns = attackerColor === types_1.InternalColor.WHITE ? board.whitePawns : board.blackPawns;
    attackers |= pawnAttackOrigins & pawns;
    // Knight attackers
    const knightAttacks = (0, Position_1.getKnightAttacks)(square);
    const knights = attackerColor === types_1.InternalColor.WHITE ? board.whiteKnights : board.blackKnights;
    attackers |= knightAttacks & knights;
    // Bishop and queen diagonal attackers
    const bishopAttacks = (0, Position_1.getBishopAttacks)(square, board.allPieces);
    const bishops = attackerColor === types_1.InternalColor.WHITE ? board.whiteBishops : board.blackBishops;
    const queens = attackerColor === types_1.InternalColor.WHITE ? board.whiteQueens : board.blackQueens;
    attackers |= bishopAttacks & (bishops | queens);
    // Rook and queen straight attackers
    const rookAttacks = (0, Position_1.getRookAttacks)(square, board.allPieces);
    const rooks = attackerColor === types_1.InternalColor.WHITE ? board.whiteRooks : board.blackRooks;
    attackers |= rookAttacks & (rooks | queens);
    // King attackers
    const kingAttacks = (0, Position_1.getKingAttacks)(square);
    const king = attackerColor === types_1.InternalColor.WHITE ? board.whiteKing : board.blackKing;
    attackers |= kingAttacks & king;
    return attackers;
}
/**
 * Check if moving a piece would leave the king in check (pinned piece detection)
 *
 * @param board - Board state
 * @param from - Square piece is moving from
 * @param to - Square piece is moving to
 * @returns true if move would leave king in check
 */
function wouldLeaveKingInCheck(board, from, to) {
    const piece = board.mailbox[from];
    const capturedPiece = board.mailbox[to];
    const color = board.turn;
    // Make the move temporarily
    board.mailbox[from] = types_1.Piece.EMPTY;
    board.mailbox[to] = piece;
    // Update bitboards
    const fromBit = 1n << BigInt(from);
    const toBit = 1n << BigInt(to);
    const moveBits = fromBit | toBit;
    // Save original bitboard state
    let originalPieceBB;
    let originalCapturedBB = null;
    // Update piece bitboard
    switch (piece) {
        case types_1.Piece.WHITE_PAWN:
            originalPieceBB = board.whitePawns;
            board.whitePawns = (board.whitePawns & ~fromBit) | toBit;
            break;
        case types_1.Piece.WHITE_KNIGHT:
            originalPieceBB = board.whiteKnights;
            board.whiteKnights = (board.whiteKnights & ~fromBit) | toBit;
            break;
        case types_1.Piece.WHITE_BISHOP:
            originalPieceBB = board.whiteBishops;
            board.whiteBishops = (board.whiteBishops & ~fromBit) | toBit;
            break;
        case types_1.Piece.WHITE_ROOK:
            originalPieceBB = board.whiteRooks;
            board.whiteRooks = (board.whiteRooks & ~fromBit) | toBit;
            break;
        case types_1.Piece.WHITE_QUEEN:
            originalPieceBB = board.whiteQueens;
            board.whiteQueens = (board.whiteQueens & ~fromBit) | toBit;
            break;
        case types_1.Piece.WHITE_KING:
            originalPieceBB = board.whiteKing;
            board.whiteKing = (board.whiteKing & ~fromBit) | toBit;
            break;
        case types_1.Piece.BLACK_PAWN:
            originalPieceBB = board.blackPawns;
            board.blackPawns = (board.blackPawns & ~fromBit) | toBit;
            break;
        case types_1.Piece.BLACK_KNIGHT:
            originalPieceBB = board.blackKnights;
            board.blackKnights = (board.blackKnights & ~fromBit) | toBit;
            break;
        case types_1.Piece.BLACK_BISHOP:
            originalPieceBB = board.blackBishops;
            board.blackBishops = (board.blackBishops & ~fromBit) | toBit;
            break;
        case types_1.Piece.BLACK_ROOK:
            originalPieceBB = board.blackRooks;
            board.blackRooks = (board.blackRooks & ~fromBit) | toBit;
            break;
        case types_1.Piece.BLACK_QUEEN:
            originalPieceBB = board.blackQueens;
            board.blackQueens = (board.blackQueens & ~fromBit) | toBit;
            break;
        case types_1.Piece.BLACK_KING:
            originalPieceBB = board.blackKing;
            board.blackKing = (board.blackKing & ~fromBit) | toBit;
            break;
        default:
            originalPieceBB = 0n;
    }
    // Update captured piece bitboard if there's a capture
    if (capturedPiece !== types_1.Piece.EMPTY) {
        switch (capturedPiece) {
            case types_1.Piece.WHITE_PAWN:
                originalCapturedBB = board.whitePawns;
                board.whitePawns &= ~toBit;
                break;
            case types_1.Piece.WHITE_KNIGHT:
                originalCapturedBB = board.whiteKnights;
                board.whiteKnights &= ~toBit;
                break;
            case types_1.Piece.WHITE_BISHOP:
                originalCapturedBB = board.whiteBishops;
                board.whiteBishops &= ~toBit;
                break;
            case types_1.Piece.WHITE_ROOK:
                originalCapturedBB = board.whiteRooks;
                board.whiteRooks &= ~toBit;
                break;
            case types_1.Piece.WHITE_QUEEN:
                originalCapturedBB = board.whiteQueens;
                board.whiteQueens &= ~toBit;
                break;
            case types_1.Piece.BLACK_PAWN:
                originalCapturedBB = board.blackPawns;
                board.blackPawns &= ~toBit;
                break;
            case types_1.Piece.BLACK_KNIGHT:
                originalCapturedBB = board.blackKnights;
                board.blackKnights &= ~toBit;
                break;
            case types_1.Piece.BLACK_BISHOP:
                originalCapturedBB = board.blackBishops;
                board.blackBishops &= ~toBit;
                break;
            case types_1.Piece.BLACK_ROOK:
                originalCapturedBB = board.blackRooks;
                board.blackRooks &= ~toBit;
                break;
            case types_1.Piece.BLACK_QUEEN:
                originalCapturedBB = board.blackQueens;
                board.blackQueens &= ~toBit;
                break;
        }
    }
    // Update composite bitboards
    const originalWhitePieces = board.whitePieces;
    const originalBlackPieces = board.blackPieces;
    const originalAllPieces = board.allPieces;
    board.whitePieces = board.whitePawns | board.whiteKnights | board.whiteBishops |
        board.whiteRooks | board.whiteQueens | board.whiteKing;
    board.blackPieces = board.blackPawns | board.blackKnights | board.blackBishops |
        board.blackRooks | board.blackQueens | board.blackKing;
    board.allPieces = board.whitePieces | board.blackPieces;
    // Check if king is in check
    const inCheck = isKingInCheck(board);
    // Undo the move
    board.mailbox[from] = piece;
    board.mailbox[to] = capturedPiece;
    // Restore bitboards
    switch (piece) {
        case types_1.Piece.WHITE_PAWN:
            board.whitePawns = originalPieceBB;
            break;
        case types_1.Piece.WHITE_KNIGHT:
            board.whiteKnights = originalPieceBB;
            break;
        case types_1.Piece.WHITE_BISHOP:
            board.whiteBishops = originalPieceBB;
            break;
        case types_1.Piece.WHITE_ROOK:
            board.whiteRooks = originalPieceBB;
            break;
        case types_1.Piece.WHITE_QUEEN:
            board.whiteQueens = originalPieceBB;
            break;
        case types_1.Piece.WHITE_KING:
            board.whiteKing = originalPieceBB;
            break;
        case types_1.Piece.BLACK_PAWN:
            board.blackPawns = originalPieceBB;
            break;
        case types_1.Piece.BLACK_KNIGHT:
            board.blackKnights = originalPieceBB;
            break;
        case types_1.Piece.BLACK_BISHOP:
            board.blackBishops = originalPieceBB;
            break;
        case types_1.Piece.BLACK_ROOK:
            board.blackRooks = originalPieceBB;
            break;
        case types_1.Piece.BLACK_QUEEN:
            board.blackQueens = originalPieceBB;
            break;
        case types_1.Piece.BLACK_KING:
            board.blackKing = originalPieceBB;
            break;
    }
    if (originalCapturedBB !== null) {
        switch (capturedPiece) {
            case types_1.Piece.WHITE_PAWN:
                board.whitePawns = originalCapturedBB;
                break;
            case types_1.Piece.WHITE_KNIGHT:
                board.whiteKnights = originalCapturedBB;
                break;
            case types_1.Piece.WHITE_BISHOP:
                board.whiteBishops = originalCapturedBB;
                break;
            case types_1.Piece.WHITE_ROOK:
                board.whiteRooks = originalCapturedBB;
                break;
            case types_1.Piece.WHITE_QUEEN:
                board.whiteQueens = originalCapturedBB;
                break;
            case types_1.Piece.BLACK_PAWN:
                board.blackPawns = originalCapturedBB;
                break;
            case types_1.Piece.BLACK_KNIGHT:
                board.blackKnights = originalCapturedBB;
                break;
            case types_1.Piece.BLACK_BISHOP:
                board.blackBishops = originalCapturedBB;
                break;
            case types_1.Piece.BLACK_ROOK:
                board.blackRooks = originalCapturedBB;
                break;
            case types_1.Piece.BLACK_QUEEN:
                board.blackQueens = originalCapturedBB;
                break;
        }
    }
    board.whitePieces = originalWhitePieces;
    board.blackPieces = originalBlackPieces;
    board.allPieces = originalAllPieces;
    return inCheck;
}
//# sourceMappingURL=AttackDetector.js.map