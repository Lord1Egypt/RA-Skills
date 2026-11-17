"use strict";
/**
 * Internal board representation using hybrid bitboards + mailbox
 *
 * This module provides the core board state with:
 * - Bitboards for fast attack detection and piece locations
 * - Mailbox (Int8Array) for O(1) piece lookup by square
 * - Zobrist hashing for transposition table
 * - Efficient copying and comparison
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.createEmptyBoard = createEmptyBoard;
exports.createStartingBoard = createStartingBoard;
exports.setPiece = setPiece;
exports.removePiece = removePiece;
exports.getPiece = getPiece;
exports.getBitboard = getBitboard;
exports.copyBoard = copyBoard;
exports.isPieceColor = isPieceColor;
exports.getPieceColor = getPieceColor;
exports.oppositeColor = oppositeColor;
exports.isSquareEmpty = isSquareEmpty;
exports.isSquareEnemy = isSquareEnemy;
exports.isSquareFriendly = isSquareFriendly;
const types_1 = require("../types");
const constants_1 = require("../utils/constants");
/**
 * Create a new empty internal board
 *
 * @returns Empty board with no pieces
 */
function createEmptyBoard() {
    return {
        // Mailbox (64 squares, each can hold a piece enum value)
        mailbox: new Int8Array(constants_1.TOTAL_SQUARES),
        // White piece bitboards
        whitePawns: 0n,
        whiteKnights: 0n,
        whiteBishops: 0n,
        whiteRooks: 0n,
        whiteQueens: 0n,
        whiteKing: 0n,
        // Black piece bitboards
        blackPawns: 0n,
        blackKnights: 0n,
        blackBishops: 0n,
        blackRooks: 0n,
        blackQueens: 0n,
        blackKing: 0n,
        // Composite bitboards
        whitePieces: 0n,
        blackPieces: 0n,
        allPieces: 0n,
        // Game state
        turn: types_1.InternalColor.WHITE,
        castlingRights: {
            whiteShort: true,
            blackShort: true,
            whiteLong: true,
            blackLong: true,
        },
        enPassantSquare: null,
        halfMoveClock: 0,
        fullMoveNumber: 1,
        // Zobrist hash (will be computed)
        zobristHash: 0n,
        // Game status
        isCheck: false,
        isCheckmate: false,
        isStalemate: false,
    };
}
/**
 * Create a new board for the starting position
 *
 * @returns Board set up for standard chess starting position
 */
function createStartingBoard() {
    const board = createEmptyBoard();
    // White pawns (rank 2, indices 8-15)
    for (let i = 8; i < 16; i++) {
        setPiece(board, i, types_1.Piece.WHITE_PAWN);
    }
    // Black pawns (rank 7, indices 48-55)
    for (let i = 48; i < 56; i++) {
        setPiece(board, i, types_1.Piece.BLACK_PAWN);
    }
    // White pieces (rank 1, indices 0-7)
    setPiece(board, 0, types_1.Piece.WHITE_ROOK); // A1
    setPiece(board, 1, types_1.Piece.WHITE_KNIGHT); // B1
    setPiece(board, 2, types_1.Piece.WHITE_BISHOP); // C1
    setPiece(board, 3, types_1.Piece.WHITE_QUEEN); // D1
    setPiece(board, 4, types_1.Piece.WHITE_KING); // E1
    setPiece(board, 5, types_1.Piece.WHITE_BISHOP); // F1
    setPiece(board, 6, types_1.Piece.WHITE_KNIGHT); // G1
    setPiece(board, 7, types_1.Piece.WHITE_ROOK); // H1
    // Black pieces (rank 8, indices 56-63)
    setPiece(board, 56, types_1.Piece.BLACK_ROOK); // A8
    setPiece(board, 57, types_1.Piece.BLACK_KNIGHT); // B8
    setPiece(board, 58, types_1.Piece.BLACK_BISHOP); // C8
    setPiece(board, 59, types_1.Piece.BLACK_QUEEN); // D8
    setPiece(board, 60, types_1.Piece.BLACK_KING); // E8
    setPiece(board, 61, types_1.Piece.BLACK_BISHOP); // F8
    setPiece(board, 62, types_1.Piece.BLACK_KNIGHT); // G8
    setPiece(board, 63, types_1.Piece.BLACK_ROOK); // H8
    // Enable castling rights for starting position
    board.castlingRights = {
        whiteShort: true,
        whiteLong: true,
        blackShort: true,
        blackLong: true,
    };
    return board;
}
/**
 * Set a piece on the board
 *
 * @param board - Board to modify
 * @param index - Square index (0-63)
 * @param piece - Piece to place
 */
function setPiece(board, index, piece) {
    // Remove any existing piece at this square first
    const existingPiece = board.mailbox[index];
    if (existingPiece !== types_1.Piece.EMPTY) {
        removePiece(board, index);
    }
    // Set piece in mailbox
    board.mailbox[index] = piece;
    if (piece === types_1.Piece.EMPTY) {
        return;
    }
    // Set bit in appropriate bitboard
    const bitboard = 1n << BigInt(index);
    switch (piece) {
        case types_1.Piece.WHITE_PAWN:
            board.whitePawns |= bitboard;
            board.whitePieces |= bitboard;
            break;
        case types_1.Piece.WHITE_KNIGHT:
            board.whiteKnights |= bitboard;
            board.whitePieces |= bitboard;
            break;
        case types_1.Piece.WHITE_BISHOP:
            board.whiteBishops |= bitboard;
            board.whitePieces |= bitboard;
            break;
        case types_1.Piece.WHITE_ROOK:
            board.whiteRooks |= bitboard;
            board.whitePieces |= bitboard;
            break;
        case types_1.Piece.WHITE_QUEEN:
            board.whiteQueens |= bitboard;
            board.whitePieces |= bitboard;
            break;
        case types_1.Piece.WHITE_KING:
            board.whiteKing |= bitboard;
            board.whitePieces |= bitboard;
            break;
        case types_1.Piece.BLACK_PAWN:
            board.blackPawns |= bitboard;
            board.blackPieces |= bitboard;
            break;
        case types_1.Piece.BLACK_KNIGHT:
            board.blackKnights |= bitboard;
            board.blackPieces |= bitboard;
            break;
        case types_1.Piece.BLACK_BISHOP:
            board.blackBishops |= bitboard;
            board.blackPieces |= bitboard;
            break;
        case types_1.Piece.BLACK_ROOK:
            board.blackRooks |= bitboard;
            board.blackPieces |= bitboard;
            break;
        case types_1.Piece.BLACK_QUEEN:
            board.blackQueens |= bitboard;
            board.blackPieces |= bitboard;
            break;
        case types_1.Piece.BLACK_KING:
            board.blackKing |= bitboard;
            board.blackPieces |= bitboard;
            break;
    }
    // Update composite bitboards
    board.allPieces = board.whitePieces | board.blackPieces;
}
/**
 * Remove a piece from the board
 *
 * @param board - Board to modify
 * @param index - Square index (0-63)
 */
function removePiece(board, index) {
    const piece = board.mailbox[index];
    if (piece === types_1.Piece.EMPTY) {
        return;
    }
    // Clear piece in mailbox
    board.mailbox[index] = types_1.Piece.EMPTY;
    // Clear bit in appropriate bitboard
    const bitboard = ~(1n << BigInt(index));
    switch (piece) {
        case types_1.Piece.WHITE_PAWN:
            board.whitePawns &= bitboard;
            board.whitePieces &= bitboard;
            break;
        case types_1.Piece.WHITE_KNIGHT:
            board.whiteKnights &= bitboard;
            board.whitePieces &= bitboard;
            break;
        case types_1.Piece.WHITE_BISHOP:
            board.whiteBishops &= bitboard;
            board.whitePieces &= bitboard;
            break;
        case types_1.Piece.WHITE_ROOK:
            board.whiteRooks &= bitboard;
            board.whitePieces &= bitboard;
            break;
        case types_1.Piece.WHITE_QUEEN:
            board.whiteQueens &= bitboard;
            board.whitePieces &= bitboard;
            break;
        case types_1.Piece.WHITE_KING:
            board.whiteKing &= bitboard;
            board.whitePieces &= bitboard;
            break;
        case types_1.Piece.BLACK_PAWN:
            board.blackPawns &= bitboard;
            board.blackPieces &= bitboard;
            break;
        case types_1.Piece.BLACK_KNIGHT:
            board.blackKnights &= bitboard;
            board.blackPieces &= bitboard;
            break;
        case types_1.Piece.BLACK_BISHOP:
            board.blackBishops &= bitboard;
            board.blackPieces &= bitboard;
            break;
        case types_1.Piece.BLACK_ROOK:
            board.blackRooks &= bitboard;
            board.blackPieces &= bitboard;
            break;
        case types_1.Piece.BLACK_QUEEN:
            board.blackQueens &= bitboard;
            board.blackPieces &= bitboard;
            break;
        case types_1.Piece.BLACK_KING:
            board.blackKing &= bitboard;
            board.blackPieces &= bitboard;
            break;
    }
    // Update composite bitboards
    board.allPieces = board.whitePieces | board.blackPieces;
}
/**
 * Get the piece at a square
 *
 * @param board - Board to query
 * @param index - Square index (0-63)
 * @returns Piece at the square
 */
function getPiece(board, index) {
    return board.mailbox[index];
}
/**
 * Get the bitboard for a specific piece type
 *
 * @param board - Board to query
 * @param piece - Piece type
 * @returns Bitboard with all pieces of this type
 */
function getBitboard(board, piece) {
    switch (piece) {
        case types_1.Piece.WHITE_PAWN: return board.whitePawns;
        case types_1.Piece.WHITE_KNIGHT: return board.whiteKnights;
        case types_1.Piece.WHITE_BISHOP: return board.whiteBishops;
        case types_1.Piece.WHITE_ROOK: return board.whiteRooks;
        case types_1.Piece.WHITE_QUEEN: return board.whiteQueens;
        case types_1.Piece.WHITE_KING: return board.whiteKing;
        case types_1.Piece.BLACK_PAWN: return board.blackPawns;
        case types_1.Piece.BLACK_KNIGHT: return board.blackKnights;
        case types_1.Piece.BLACK_BISHOP: return board.blackBishops;
        case types_1.Piece.BLACK_ROOK: return board.blackRooks;
        case types_1.Piece.BLACK_QUEEN: return board.blackQueens;
        case types_1.Piece.BLACK_KING: return board.blackKing;
        default: return 0n;
    }
}
/**
 * Copy a board (efficient struct copy)
 *
 * @param source - Source board
 * @returns New board with same state
 */
function copyBoard(source) {
    return {
        // Copy mailbox
        mailbox: new Int8Array(source.mailbox),
        // Copy bitboards (primitives, so direct copy)
        whitePawns: source.whitePawns,
        whiteKnights: source.whiteKnights,
        whiteBishops: source.whiteBishops,
        whiteRooks: source.whiteRooks,
        whiteQueens: source.whiteQueens,
        whiteKing: source.whiteKing,
        blackPawns: source.blackPawns,
        blackKnights: source.blackKnights,
        blackBishops: source.blackBishops,
        blackRooks: source.blackRooks,
        blackQueens: source.blackQueens,
        blackKing: source.blackKing,
        whitePieces: source.whitePieces,
        blackPieces: source.blackPieces,
        allPieces: source.allPieces,
        // Copy game state
        turn: source.turn,
        castlingRights: { ...source.castlingRights },
        enPassantSquare: source.enPassantSquare,
        halfMoveClock: source.halfMoveClock,
        fullMoveNumber: source.fullMoveNumber,
        zobristHash: source.zobristHash,
        isCheck: source.isCheck,
        isCheckmate: source.isCheckmate,
        isStalemate: source.isStalemate,
    };
}
/**
 * Check if a piece belongs to a specific color
 *
 * @param piece - Piece to check
 * @param color - Color to check
 * @returns true if piece is of the given color
 */
function isPieceColor(piece, color) {
    if (piece === types_1.Piece.EMPTY) {
        return false;
    }
    if (color === types_1.InternalColor.WHITE) {
        return piece >= types_1.Piece.WHITE_PAWN && piece <= types_1.Piece.WHITE_KING;
    }
    else {
        return piece >= types_1.Piece.BLACK_PAWN && piece <= types_1.Piece.BLACK_KING;
    }
}
/**
 * Get the color of a piece
 *
 * @param piece - Piece to check
 * @returns Color of the piece, or null if empty
 */
function getPieceColor(piece) {
    if (piece === types_1.Piece.EMPTY) {
        return null;
    }
    return piece >= types_1.Piece.WHITE_PAWN && piece <= types_1.Piece.WHITE_KING
        ? types_1.InternalColor.WHITE
        : types_1.InternalColor.BLACK;
}
/**
 * Get the opposite color
 *
 * @param color - Color
 * @returns Opposite color
 */
function oppositeColor(color) {
    return color === types_1.InternalColor.WHITE ? types_1.InternalColor.BLACK : types_1.InternalColor.WHITE;
}
/**
 * Check if a square is empty
 *
 * @param board - Board to check
 * @param index - Square index
 * @returns true if square is empty
 */
function isSquareEmpty(board, index) {
    return board.mailbox[index] === types_1.Piece.EMPTY;
}
/**
 * Check if a square is occupied by an enemy piece
 *
 * @param board - Board to check
 * @param index - Square index
 * @param color - Our color
 * @returns true if square has enemy piece
 */
function isSquareEnemy(board, index, color) {
    const piece = board.mailbox[index];
    if (piece === types_1.Piece.EMPTY) {
        return false;
    }
    const pieceColor = getPieceColor(piece);
    return pieceColor !== null && pieceColor !== color;
}
/**
 * Check if a square is occupied by a friendly piece
 *
 * @param board - Board to check
 * @param index - Square index
 * @param color - Our color
 * @returns true if square has friendly piece
 */
function isSquareFriendly(board, index, color) {
    const piece = board.mailbox[index];
    if (piece === types_1.Piece.EMPTY) {
        return false;
    }
    return isPieceColor(piece, color);
}
//# sourceMappingURL=Board.js.map