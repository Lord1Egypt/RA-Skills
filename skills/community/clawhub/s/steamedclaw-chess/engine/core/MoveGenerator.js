"use strict";
/**
 * Move generation for all piece types
 *
 * This module generates all legal moves for a given position using
 * bitboard-based algorithms for performance.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateLegalMoves = generateLegalMoves;
exports.generatePseudoLegalMoves = generatePseudoLegalMoves;
exports.getMovesForPiece = getMovesForPiece;
exports.isMoveLegal = isMoveLegal;
exports.applyMoveComplete = applyMoveComplete;
const types_1 = require("../types");
const Position_1 = require("./Position");
const AttackDetector_1 = require("./AttackDetector");
const conversion_1 = require("../utils/conversion");
const Board_1 = require("./Board");
const constants_1 = require("../utils/constants");
const zobrist_1 = require("./zobrist");
/**
 * Generate all legal moves for the current position
 *
 * @param board - Board state
 * @returns Array of legal moves
 */
function generateLegalMoves(board) {
    const pseudoLegalMoves = generatePseudoLegalMoves(board);
    const currentColor = board.turn;
    // Check if the current player has a king
    const ourKingBitboard = currentColor === types_1.InternalColor.WHITE ? board.whiteKing : board.blackKing;
    if (ourKingBitboard === 0n) {
        // No king - return all pseudo-legal moves (for test scenarios)
        return pseudoLegalMoves;
    }
    // Filter to only legal moves
    return pseudoLegalMoves.filter(move => {
        // Special handling for castling - already checked in generation
        if (move.flags & types_1.MoveFlag.CASTLING) {
            return true;
        }
        // Make the move on a temporary board copy to check if it's legal
        const testBoard = (0, Board_1.copyBoard)(board);
        const originalTurn = testBoard.turn;
        makeMove(testBoard, move);
        // After making the move, check if OUR king (the one that just moved) is in check
        // makeMove switches the turn, so we need to check the OPPOSITE color
        const kingBitboardAfter = originalTurn === types_1.InternalColor.WHITE ? testBoard.whiteKing : testBoard.blackKing;
        if (kingBitboardAfter === 0n) {
            return true; // King was captured (shouldn't happen in legal game)
        }
        const kingSquare = (0, conversion_1.getLowestSetBit)(kingBitboardAfter);
        const opponentColor = originalTurn === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
        // The move is legal if our king is NOT being attacked after the move
        return !(0, AttackDetector_1.isSquareAttacked)(testBoard, kingSquare, opponentColor);
    });
}
/**
 * Apply a move to a board (mutates the board)
 * Used internally for legal move checking
 *
 * @param board - Board to modify
 * @param move - Move to apply
 */
function makeMove(board, move) {
    // Handle castling specially
    if (move.flags & types_1.MoveFlag.CASTLING) {
        // Move the king
        (0, Board_1.removePiece)(board, move.from);
        (0, Board_1.setPiece)(board, move.to, move.piece);
        // Move the rook
        const color = board.turn;
        if (color === types_1.InternalColor.WHITE) {
            if (move.to === constants_1.CASTLING.WHITE_SHORT.kingTo) {
                // White short castling
                (0, Board_1.removePiece)(board, constants_1.CASTLING.WHITE_SHORT.rookFrom);
                (0, Board_1.setPiece)(board, constants_1.CASTLING.WHITE_SHORT.rookTo, types_1.Piece.WHITE_ROOK);
            }
            else {
                // White long castling
                (0, Board_1.removePiece)(board, constants_1.CASTLING.WHITE_LONG.rookFrom);
                (0, Board_1.setPiece)(board, constants_1.CASTLING.WHITE_LONG.rookTo, types_1.Piece.WHITE_ROOK);
            }
        }
        else {
            if (move.to === constants_1.CASTLING.BLACK_SHORT.kingTo) {
                // Black short castling
                (0, Board_1.removePiece)(board, constants_1.CASTLING.BLACK_SHORT.rookFrom);
                (0, Board_1.setPiece)(board, constants_1.CASTLING.BLACK_SHORT.rookTo, types_1.Piece.BLACK_ROOK);
            }
            else {
                // Black long castling
                (0, Board_1.removePiece)(board, constants_1.CASTLING.BLACK_LONG.rookFrom);
                (0, Board_1.setPiece)(board, constants_1.CASTLING.BLACK_LONG.rookTo, types_1.Piece.BLACK_ROOK);
            }
        }
    }
    else if (move.flags & types_1.MoveFlag.EN_PASSANT) {
        // En passant capture
        (0, Board_1.removePiece)(board, move.from);
        (0, Board_1.setPiece)(board, move.to, move.piece);
        // Remove the captured pawn (on different square than move.to)
        const capturedPawnSquare = board.turn === types_1.InternalColor.WHITE
            ? (move.to - 8) // Captured pawn is one rank below
            : (move.to + 8); // Captured pawn is one rank above
        (0, Board_1.removePiece)(board, capturedPawnSquare);
    }
    else if (move.flags & types_1.MoveFlag.PROMOTION) {
        // Promotion
        (0, Board_1.removePiece)(board, move.from);
        if (move.capturedPiece !== types_1.Piece.EMPTY) {
            (0, Board_1.removePiece)(board, move.to);
        }
        (0, Board_1.setPiece)(board, move.to, move.promotionPiece);
    }
    else {
        // Normal move or capture
        (0, Board_1.removePiece)(board, move.from);
        if (move.capturedPiece !== types_1.Piece.EMPTY) {
            (0, Board_1.removePiece)(board, move.to);
        }
        (0, Board_1.setPiece)(board, move.to, move.piece);
    }
    // Update en passant square
    if (move.flags & types_1.MoveFlag.PAWN_DOUBLE_PUSH) {
        const epSquare = board.turn === types_1.InternalColor.WHITE
            ? (move.from + 8)
            : (move.from - 8);
        board.enPassantSquare = epSquare;
    }
    else {
        board.enPassantSquare = null;
    }
    // Switch turn (needed for isKingInCheck to check the right king)
    board.turn = board.turn === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
}
/**
 * Generate all pseudo-legal moves (may leave king in check)
 *
 * @param board - Board state
 * @returns Array of pseudo-legal moves
 */
function generatePseudoLegalMoves(board) {
    const moves = [];
    const color = board.turn;
    const friendlyPieces = color === types_1.InternalColor.WHITE ? board.whitePieces : board.blackPieces;
    const enemyPieces = color === types_1.InternalColor.WHITE ? board.blackPieces : board.whitePieces;
    // Generate moves for each piece type
    generatePawnMoves(board, moves, color, friendlyPieces, enemyPieces);
    generateKnightMoves(board, moves, color, friendlyPieces);
    generateBishopMoves(board, moves, color, friendlyPieces);
    generateRookMoves(board, moves, color, friendlyPieces);
    generateQueenMoves(board, moves, color, friendlyPieces);
    generateKingMoves(board, moves, color, friendlyPieces);
    generateCastlingMoves(board, moves, color);
    return moves;
}
/**
 * Generate pawn moves (including promotions and en passant)
 */
function generatePawnMoves(board, moves, color, _friendlyPieces, enemyPieces) {
    const pawns = color === types_1.InternalColor.WHITE ? board.whitePawns : board.blackPawns;
    const pawnPiece = color === types_1.InternalColor.WHITE ? types_1.Piece.WHITE_PAWN : types_1.Piece.BLACK_PAWN;
    const promotionRank = color === types_1.InternalColor.WHITE ? 7 : 0;
    const empty = ~board.allPieces;
    if (color === types_1.InternalColor.WHITE) {
        // Single push
        let singlePushBB = (0, Position_1.shiftNorth)(pawns) & empty;
        while (singlePushBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(singlePushBB);
            singlePushBB &= singlePushBB - 1n;
            const from = (to - 8);
            const toRank = (0, conversion_1.getRankIndex)(to);
            // Check for promotion
            if (toRank === promotionRank) {
                // Add all promotion moves
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.WHITE_QUEEN));
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.WHITE_ROOK));
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.WHITE_BISHOP));
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.WHITE_KNIGHT));
            }
            else {
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.NONE));
            }
        }
        // Double push
        const doublePushSource = pawns & 0x000000000000ff00n; // Rank 2
        let doublePushBB = (0, Position_1.shiftNorth)((0, Position_1.shiftNorth)(doublePushSource) & empty) & empty;
        while (doublePushBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(doublePushBB);
            doublePushBB &= doublePushBB - 1n;
            const from = (to - 16);
            moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PAWN_DOUBLE_PUSH));
        }
        // Captures north-east
        let capturesNEBB = (0, Position_1.shiftNorthEast)(pawns) & enemyPieces;
        while (capturesNEBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(capturesNEBB);
            capturesNEBB &= capturesNEBB - 1n;
            const from = (to - 9);
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const toRank = (0, conversion_1.getRankIndex)(to);
            if (toRank === promotionRank) {
                // Promotion capture
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_QUEEN));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_ROOK));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_BISHOP));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_KNIGHT));
            }
            else {
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.CAPTURE));
            }
        }
        // Captures north-west
        let capturesNWBB = (0, Position_1.shiftNorthWest)(pawns) & enemyPieces;
        while (capturesNWBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(capturesNWBB);
            capturesNWBB &= capturesNWBB - 1n;
            const from = (to - 7);
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const toRank = (0, conversion_1.getRankIndex)(to);
            if (toRank === promotionRank) {
                // Promotion capture
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_QUEEN));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_ROOK));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_BISHOP));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.WHITE_KNIGHT));
            }
            else {
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.CAPTURE));
            }
        }
        // En passant
        if (board.enPassantSquare !== null) {
            const epSquare = board.enPassantSquare;
            const epTarget = 1n << BigInt(epSquare);
            // Check if any pawn can capture en passant
            const canCaptureEP = ((0, Position_1.shiftSouthWest)(epTarget) | (0, Position_1.shiftSouthEast)(epTarget)) & pawns;
            let epBB = canCaptureEP;
            while (epBB !== 0n) {
                const from = (0, conversion_1.getLowestSetBit)(epBB);
                epBB &= epBB - 1n;
                const capturedPiece = types_1.Piece.BLACK_PAWN;
                moves.push(createMove(from, epSquare, pawnPiece, capturedPiece, types_1.MoveFlag.EN_PASSANT | types_1.MoveFlag.CAPTURE));
            }
        }
    }
    else {
        // Black pawns (move south)
        // Single push
        let singlePushBB = (0, Position_1.shiftSouth)(pawns) & empty;
        while (singlePushBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(singlePushBB);
            singlePushBB &= singlePushBB - 1n;
            const from = (to + 8);
            const toRank = (0, conversion_1.getRankIndex)(to);
            // Check for promotion
            if (toRank === promotionRank) {
                // Add all promotion moves
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.BLACK_QUEEN));
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.BLACK_ROOK));
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.BLACK_BISHOP));
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PROMOTION, types_1.Piece.BLACK_KNIGHT));
            }
            else {
                moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.NONE));
            }
        }
        // Double push
        const doublePushSource = pawns & 0x00ff000000000000n; // Rank 7
        let doublePushBB = (0, Position_1.shiftSouth)((0, Position_1.shiftSouth)(doublePushSource) & empty) & empty;
        while (doublePushBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(doublePushBB);
            doublePushBB &= doublePushBB - 1n;
            const from = (to + 16);
            moves.push(createMove(from, to, pawnPiece, types_1.Piece.EMPTY, types_1.MoveFlag.PAWN_DOUBLE_PUSH));
        }
        // Captures south-east
        let capturesSEBB = (0, Position_1.shiftSouthEast)(pawns) & enemyPieces;
        while (capturesSEBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(capturesSEBB);
            capturesSEBB &= capturesSEBB - 1n;
            const from = (to + 7);
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const toRank = (0, conversion_1.getRankIndex)(to);
            if (toRank === promotionRank) {
                // Promotion capture
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_QUEEN));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_ROOK));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_BISHOP));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_KNIGHT));
            }
            else {
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.CAPTURE));
            }
        }
        // Captures south-west
        let capturesSWBB = (0, Position_1.shiftSouthWest)(pawns) & enemyPieces;
        while (capturesSWBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(capturesSWBB);
            capturesSWBB &= capturesSWBB - 1n;
            const from = (to + 9);
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const toRank = (0, conversion_1.getRankIndex)(to);
            if (toRank === promotionRank) {
                // Promotion capture
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_QUEEN));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_ROOK));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_BISHOP));
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.PROMOTION | types_1.MoveFlag.CAPTURE, types_1.Piece.BLACK_KNIGHT));
            }
            else {
                moves.push(createMove(from, to, pawnPiece, capturedPiece, types_1.MoveFlag.CAPTURE));
            }
        }
        // En passant
        if (board.enPassantSquare !== null) {
            const epSquare = board.enPassantSquare;
            const epTarget = 1n << BigInt(epSquare);
            // Check if any pawn can capture en passant
            const canCaptureEP = ((0, Position_1.shiftNorthWest)(epTarget) | (0, Position_1.shiftNorthEast)(epTarget)) & pawns;
            let epBB = canCaptureEP;
            while (epBB !== 0n) {
                const from = (0, conversion_1.getLowestSetBit)(epBB);
                epBB &= epBB - 1n;
                const capturedPiece = types_1.Piece.WHITE_PAWN;
                moves.push(createMove(from, epSquare, pawnPiece, capturedPiece, types_1.MoveFlag.EN_PASSANT | types_1.MoveFlag.CAPTURE));
            }
        }
    }
}
/**
 * Generate knight moves
 */
function generateKnightMoves(board, moves, color, friendlyPieces) {
    const knights = color === types_1.InternalColor.WHITE ? board.whiteKnights : board.blackKnights;
    const knightPiece = color === types_1.InternalColor.WHITE ? types_1.Piece.WHITE_KNIGHT : types_1.Piece.BLACK_KNIGHT;
    let knightsBB = knights;
    while (knightsBB !== 0n) {
        const from = (0, conversion_1.getLowestSetBit)(knightsBB);
        const attacks = (0, Position_1.getKnightAttacks)(from) & ~friendlyPieces;
        let attacksBB = attacks;
        while (attacksBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(attacksBB);
            attacksBB &= attacksBB - 1n;
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const flags = capturedPiece !== types_1.Piece.EMPTY ? types_1.MoveFlag.CAPTURE : types_1.MoveFlag.NONE;
            moves.push(createMove(from, to, knightPiece, capturedPiece, flags));
        }
        knightsBB &= knightsBB - 1n; // Clear lowest bit
    }
}
/**
 * Generate bishop moves
 */
function generateBishopMoves(board, moves, color, friendlyPieces) {
    const bishops = color === types_1.InternalColor.WHITE ? board.whiteBishops : board.blackBishops;
    const bishopPiece = color === types_1.InternalColor.WHITE ? types_1.Piece.WHITE_BISHOP : types_1.Piece.BLACK_BISHOP;
    let bishopsBB = bishops;
    while (bishopsBB !== 0n) {
        const from = (0, conversion_1.getLowestSetBit)(bishopsBB);
        const attacks = (0, Position_1.getBishopAttacks)(from, board.allPieces) & ~friendlyPieces;
        let attacksBB = attacks;
        while (attacksBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(attacksBB);
            attacksBB &= attacksBB - 1n;
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const flags = capturedPiece !== types_1.Piece.EMPTY ? types_1.MoveFlag.CAPTURE : types_1.MoveFlag.NONE;
            moves.push(createMove(from, to, bishopPiece, capturedPiece, flags));
        }
        bishopsBB &= bishopsBB - 1n;
    }
}
/**
 * Generate rook moves
 */
function generateRookMoves(board, moves, color, friendlyPieces) {
    const rooks = color === types_1.InternalColor.WHITE ? board.whiteRooks : board.blackRooks;
    const rookPiece = color === types_1.InternalColor.WHITE ? types_1.Piece.WHITE_ROOK : types_1.Piece.BLACK_ROOK;
    let rooksBB = rooks;
    while (rooksBB !== 0n) {
        const from = (0, conversion_1.getLowestSetBit)(rooksBB);
        const attacks = (0, Position_1.getRookAttacks)(from, board.allPieces) & ~friendlyPieces;
        let attacksBB = attacks;
        while (attacksBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(attacksBB);
            attacksBB &= attacksBB - 1n;
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const flags = capturedPiece !== types_1.Piece.EMPTY ? types_1.MoveFlag.CAPTURE : types_1.MoveFlag.NONE;
            moves.push(createMove(from, to, rookPiece, capturedPiece, flags));
        }
        rooksBB &= rooksBB - 1n;
    }
}
/**
 * Generate queen moves
 */
function generateQueenMoves(board, moves, color, friendlyPieces) {
    const queens = color === types_1.InternalColor.WHITE ? board.whiteQueens : board.blackQueens;
    const queenPiece = color === types_1.InternalColor.WHITE ? types_1.Piece.WHITE_QUEEN : types_1.Piece.BLACK_QUEEN;
    let queensBB = queens;
    while (queensBB !== 0n) {
        const from = (0, conversion_1.getLowestSetBit)(queensBB);
        const attacks = (0, Position_1.getQueenAttacks)(from, board.allPieces) & ~friendlyPieces;
        let attacksBB = attacks;
        while (attacksBB !== 0n) {
            const to = (0, conversion_1.getLowestSetBit)(attacksBB);
            attacksBB &= attacksBB - 1n;
            const capturedPiece = (0, Board_1.getPiece)(board, to);
            const flags = capturedPiece !== types_1.Piece.EMPTY ? types_1.MoveFlag.CAPTURE : types_1.MoveFlag.NONE;
            moves.push(createMove(from, to, queenPiece, capturedPiece, flags));
        }
        queensBB &= queensBB - 1n;
    }
}
/**
 * Generate king moves (excluding castling)
 */
function generateKingMoves(board, moves, color, friendlyPieces) {
    const king = color === types_1.InternalColor.WHITE ? board.whiteKing : board.blackKing;
    const kingPiece = color === types_1.InternalColor.WHITE ? types_1.Piece.WHITE_KING : types_1.Piece.BLACK_KING;
    if (king === 0n)
        return;
    const from = (0, conversion_1.getLowestSetBit)(king);
    const attacks = (0, Position_1.getKingAttacks)(from) & ~friendlyPieces;
    let attacksBB = attacks;
    while (attacksBB !== 0n) {
        const to = (0, conversion_1.getLowestSetBit)(attacksBB);
        attacksBB &= attacksBB - 1n;
        const capturedPiece = (0, Board_1.getPiece)(board, to);
        const flags = capturedPiece !== types_1.Piece.EMPTY ? types_1.MoveFlag.CAPTURE : types_1.MoveFlag.NONE;
        moves.push(createMove(from, to, kingPiece, capturedPiece, flags));
    }
}
/**
 * Generate castling moves
 */
function generateCastlingMoves(board, moves, color) {
    const opponentColor = color === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
    if (color === types_1.InternalColor.WHITE) {
        // White short castling (O-O)
        if (board.castlingRights.whiteShort &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.WHITE_SHORT.kingFrom) === types_1.Piece.WHITE_KING &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.WHITE_SHORT.rookFrom) === types_1.Piece.WHITE_ROOK &&
            (0, Board_1.isSquareEmpty)(board, 5) && // F1
            (0, Board_1.isSquareEmpty)(board, 6) && // G1
            !(0, AttackDetector_1.isSquareAttacked)(board, 4, opponentColor) && // E1 not in check
            !(0, AttackDetector_1.isSquareAttacked)(board, 5, opponentColor) && // F1 not attacked
            !(0, AttackDetector_1.isSquareAttacked)(board, 6, opponentColor) // G1 not attacked
        ) {
            moves.push(createMove(constants_1.CASTLING.WHITE_SHORT.kingFrom, constants_1.CASTLING.WHITE_SHORT.kingTo, types_1.Piece.WHITE_KING, types_1.Piece.EMPTY, types_1.MoveFlag.CASTLING));
        }
        // White long castling (O-O-O)
        if (board.castlingRights.whiteLong &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.WHITE_LONG.kingFrom) === types_1.Piece.WHITE_KING &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.WHITE_LONG.rookFrom) === types_1.Piece.WHITE_ROOK &&
            (0, Board_1.isSquareEmpty)(board, 1) && // B1
            (0, Board_1.isSquareEmpty)(board, 2) && // C1
            (0, Board_1.isSquareEmpty)(board, 3) && // D1
            !(0, AttackDetector_1.isSquareAttacked)(board, 4, opponentColor) && // E1 not in check
            !(0, AttackDetector_1.isSquareAttacked)(board, 3, opponentColor) && // D1 not attacked
            !(0, AttackDetector_1.isSquareAttacked)(board, 2, opponentColor) // C1 not attacked
        ) {
            moves.push(createMove(constants_1.CASTLING.WHITE_LONG.kingFrom, constants_1.CASTLING.WHITE_LONG.kingTo, types_1.Piece.WHITE_KING, types_1.Piece.EMPTY, types_1.MoveFlag.CASTLING));
        }
    }
    else {
        // Black short castling (O-O)
        if (board.castlingRights.blackShort &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.BLACK_SHORT.kingFrom) === types_1.Piece.BLACK_KING &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.BLACK_SHORT.rookFrom) === types_1.Piece.BLACK_ROOK &&
            (0, Board_1.isSquareEmpty)(board, 61) && // F8
            (0, Board_1.isSquareEmpty)(board, 62) && // G8
            !(0, AttackDetector_1.isSquareAttacked)(board, 60, opponentColor) && // E8 not in check
            !(0, AttackDetector_1.isSquareAttacked)(board, 61, opponentColor) && // F8 not attacked
            !(0, AttackDetector_1.isSquareAttacked)(board, 62, opponentColor) // G8 not attacked
        ) {
            moves.push(createMove(constants_1.CASTLING.BLACK_SHORT.kingFrom, constants_1.CASTLING.BLACK_SHORT.kingTo, types_1.Piece.BLACK_KING, types_1.Piece.EMPTY, types_1.MoveFlag.CASTLING));
        }
        // Black long castling (O-O-O)
        if (board.castlingRights.blackLong &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.BLACK_LONG.kingFrom) === types_1.Piece.BLACK_KING &&
            (0, Board_1.getPiece)(board, constants_1.CASTLING.BLACK_LONG.rookFrom) === types_1.Piece.BLACK_ROOK &&
            (0, Board_1.isSquareEmpty)(board, 57) && // B8
            (0, Board_1.isSquareEmpty)(board, 58) && // C8
            (0, Board_1.isSquareEmpty)(board, 59) && // D8
            !(0, AttackDetector_1.isSquareAttacked)(board, 60, opponentColor) && // E8 not in check
            !(0, AttackDetector_1.isSquareAttacked)(board, 59, opponentColor) && // D8 not attacked
            !(0, AttackDetector_1.isSquareAttacked)(board, 58, opponentColor) // C8 not attacked
        ) {
            moves.push(createMove(constants_1.CASTLING.BLACK_LONG.kingFrom, constants_1.CASTLING.BLACK_LONG.kingTo, types_1.Piece.BLACK_KING, types_1.Piece.EMPTY, types_1.MoveFlag.CASTLING));
        }
    }
}
/**
 * Helper to create a move object
 */
function createMove(from, to, piece, capturedPiece, flags, promotionPiece) {
    return {
        from,
        to,
        piece,
        capturedPiece,
        flags,
        promotionPiece,
    };
}
/**
 * Get all legal moves for a specific piece
 *
 * @param board - Board state
 * @param square - Square of the piece
 * @returns Array of legal moves for that piece
 */
function getMovesForPiece(board, square) {
    const allMoves = generateLegalMoves(board);
    return allMoves.filter(move => move.from === square);
}
/**
 * Check if a move is legal
 *
 * @param board - Board state
 * @param from - From square
 * @param to - To square
 * @returns true if move is legal
 */
function isMoveLegal(board, from, to) {
    const legalMoves = generateLegalMoves(board);
    return legalMoves.some(move => move.from === from && move.to === to);
}
/**
 * Apply a move to the board with full state updates (mutates the board)
 * Updates turn, castling rights, en passant, move counters, and game status
 *
 * @param board - Board state to modify
 * @param move - Move to apply
 * @returns The applied move
 */
function applyMoveComplete(board, move) {
    const { from, to, piece, capturedPiece, flags, promotionPiece } = move;
    // Snapshot state needed for incremental hash updates
    const oldEnPassant = board.enPassantSquare;
    const oldCastling = { ...board.castlingRights };
    // Reset en passant square (will be set if this is a double pawn push)
    board.enPassantSquare = null;
    // Handle captures (+hash)
    if (capturedPiece !== types_1.Piece.EMPTY) {
        // Remove captured piece from board and hash
        (0, Board_1.removePiece)(board, to);
        board.zobristHash = (0, zobrist_1.updateHashCapture)(board.zobristHash, capturedPiece, to);
        board.halfMoveClock = 0;
    }
    else {
        board.halfMoveClock++;
    }
    // Handle en passant capture (+hash)
    if (flags & types_1.MoveFlag.EN_PASSANT) {
        const captureSquare = board.turn === types_1.InternalColor.WHITE ? to - 8 : to + 8;
        const capturedPawn = board.turn === types_1.InternalColor.WHITE ? types_1.Piece.BLACK_PAWN : types_1.Piece.WHITE_PAWN;
        (0, Board_1.removePiece)(board, captureSquare);
        board.zobristHash = (0, zobrist_1.updateHashCapture)(board.zobristHash, capturedPawn, captureSquare);
        board.halfMoveClock = 0;
    }
    // Handle castling rook move (+hash)
    if (flags & types_1.MoveFlag.CASTLING) {
        if (to === constants_1.CASTLING.WHITE_SHORT.kingTo) {
            (0, Board_1.removePiece)(board, constants_1.CASTLING.WHITE_SHORT.rookFrom);
            (0, Board_1.setPiece)(board, constants_1.CASTLING.WHITE_SHORT.rookTo, types_1.Piece.WHITE_ROOK);
            board.zobristHash = (0, zobrist_1.updateHashMove)(board.zobristHash, types_1.Piece.WHITE_ROOK, constants_1.CASTLING.WHITE_SHORT.rookFrom, constants_1.CASTLING.WHITE_SHORT.rookTo);
        }
        else if (to === constants_1.CASTLING.WHITE_LONG.kingTo) {
            (0, Board_1.removePiece)(board, constants_1.CASTLING.WHITE_LONG.rookFrom);
            (0, Board_1.setPiece)(board, constants_1.CASTLING.WHITE_LONG.rookTo, types_1.Piece.WHITE_ROOK);
            board.zobristHash = (0, zobrist_1.updateHashMove)(board.zobristHash, types_1.Piece.WHITE_ROOK, constants_1.CASTLING.WHITE_LONG.rookFrom, constants_1.CASTLING.WHITE_LONG.rookTo);
        }
        else if (to === constants_1.CASTLING.BLACK_SHORT.kingTo) {
            (0, Board_1.removePiece)(board, constants_1.CASTLING.BLACK_SHORT.rookFrom);
            (0, Board_1.setPiece)(board, constants_1.CASTLING.BLACK_SHORT.rookTo, types_1.Piece.BLACK_ROOK);
            board.zobristHash = (0, zobrist_1.updateHashMove)(board.zobristHash, types_1.Piece.BLACK_ROOK, constants_1.CASTLING.BLACK_SHORT.rookFrom, constants_1.CASTLING.BLACK_SHORT.rookTo);
        }
        else if (to === constants_1.CASTLING.BLACK_LONG.kingTo) {
            (0, Board_1.removePiece)(board, constants_1.CASTLING.BLACK_LONG.rookFrom);
            (0, Board_1.setPiece)(board, constants_1.CASTLING.BLACK_LONG.rookTo, types_1.Piece.BLACK_ROOK);
            board.zobristHash = (0, zobrist_1.updateHashMove)(board.zobristHash, types_1.Piece.BLACK_ROOK, constants_1.CASTLING.BLACK_LONG.rookFrom, constants_1.CASTLING.BLACK_LONG.rookTo);
        }
    }
    // Move the piece (+hash)
    (0, Board_1.removePiece)(board, from);
    board.zobristHash = (0, zobrist_1.updateHashMove)(board.zobristHash, piece, from, to);
    // Handle promotion (piece identity at destination changes)
    if (flags & types_1.MoveFlag.PROMOTION && promotionPiece) {
        // updateHashMove added the pawn at `to`, swap it with promotion piece.
        board.zobristHash = (0, zobrist_1.removePieceFromHash)(board.zobristHash, piece, to);
        board.zobristHash = (0, zobrist_1.addPieceToHash)(board.zobristHash, promotionPiece, to);
        (0, Board_1.setPiece)(board, to, promotionPiece);
    }
    else {
        (0, Board_1.setPiece)(board, to, piece);
    }
    // Reset half-move clock on pawn moves
    if (piece === types_1.Piece.WHITE_PAWN || piece === types_1.Piece.BLACK_PAWN) {
        board.halfMoveClock = 0;
    }
    // Handle double pawn push (set en passant square)
    if (flags & types_1.MoveFlag.PAWN_DOUBLE_PUSH) {
        const enPassantSquare = board.turn === types_1.InternalColor.WHITE ? from + 8 : from - 8;
        board.enPassantSquare = enPassantSquare;
    }
    // Update castling rights
    updateCastlingRights(board, from, to, piece);
    // Update hash for castling/en-passant state
    board.zobristHash = (0, zobrist_1.updateHashEnPassant)(board.zobristHash, oldEnPassant, board.enPassantSquare);
    board.zobristHash = (0, zobrist_1.updateHashCastling)(board.zobristHash, oldCastling.whiteShort, board.castlingRights.whiteShort, oldCastling.whiteLong, board.castlingRights.whiteLong, oldCastling.blackShort, board.castlingRights.blackShort, oldCastling.blackLong, board.castlingRights.blackLong);
    // Switch turn (+hash)
    board.turn = board.turn === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
    board.zobristHash = (0, zobrist_1.toggleSide)(board.zobristHash);
    // Increment full move number after black's move
    if (board.turn === types_1.InternalColor.WHITE) {
        board.fullMoveNumber++;
    }
    // Update game status (check, checkmate, stalemate)
    updateGameStatus(board);
    return move;
}
/**
 * Update castling rights after a move
 *
 * @param board - Board state
 * @param from - From square
 * @param to - To square
 * @param piece - Piece that moved
 */
function updateCastlingRights(board, from, to, piece) {
    // If king moves, lose all castling rights for that color
    if (piece === types_1.Piece.WHITE_KING) {
        board.castlingRights.whiteShort = false;
        board.castlingRights.whiteLong = false;
    }
    else if (piece === types_1.Piece.BLACK_KING) {
        board.castlingRights.blackShort = false;
        board.castlingRights.blackLong = false;
    }
    // If rook moves from starting square, lose castling right for that side
    if (piece === types_1.Piece.WHITE_ROOK) {
        if (from === constants_1.CASTLING.WHITE_SHORT.rookFrom) {
            board.castlingRights.whiteShort = false;
        }
        else if (from === constants_1.CASTLING.WHITE_LONG.rookFrom) {
            board.castlingRights.whiteLong = false;
        }
    }
    else if (piece === types_1.Piece.BLACK_ROOK) {
        if (from === constants_1.CASTLING.BLACK_SHORT.rookFrom) {
            board.castlingRights.blackShort = false;
        }
        else if (from === constants_1.CASTLING.BLACK_LONG.rookFrom) {
            board.castlingRights.blackLong = false;
        }
    }
    // If rook is captured, lose castling right for that side
    if (to === constants_1.CASTLING.WHITE_SHORT.rookFrom) {
        board.castlingRights.whiteShort = false;
    }
    else if (to === constants_1.CASTLING.WHITE_LONG.rookFrom) {
        board.castlingRights.whiteLong = false;
    }
    else if (to === constants_1.CASTLING.BLACK_SHORT.rookFrom) {
        board.castlingRights.blackShort = false;
    }
    else if (to === constants_1.CASTLING.BLACK_LONG.rookFrom) {
        board.castlingRights.blackLong = false;
    }
}
/**
 * Update game status (check, checkmate, stalemate)
 *
 * @param board - Board state
 */
function updateGameStatus(board) {
    const currentColor = board.turn;
    const kingBitboard = currentColor === types_1.InternalColor.WHITE ? board.whiteKing : board.blackKing;
    if (kingBitboard === 0n) {
        board.isCheck = false;
        board.isCheckmate = false;
        board.isStalemate = false;
        return;
    }
    const kingSquare = (0, conversion_1.getLowestSetBit)(kingBitboard);
    // Check if the current player's king is attacked by the OPPONENT
    const opponentColor = currentColor === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
    const inCheck = (0, AttackDetector_1.isSquareAttacked)(board, kingSquare, opponentColor);
    // Fast status update — only sets isCheck.
    // IMPORTANT: isCheckmate and isStalemate are NOT set here to avoid recursive
    // generateLegalMoves() calls (applyMoveComplete -> updateGameStatus -> generateLegalMoves).
    // The search detects mate/stalemate via moves.length === 0.
    // The public API (Game class) patches these flags via updateConfigStatusFromBoard().
    board.isCheck = inCheck;
    board.isCheckmate = false;
    board.isStalemate = false;
}
//# sourceMappingURL=MoveGenerator.js.map