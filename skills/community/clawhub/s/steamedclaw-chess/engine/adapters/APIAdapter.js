"use strict";
/**
 * API Adapter for converting between internal and external representations
 *
 * Internal format uses:
 * - Square indices (0-63)
 * - Piece enums
 * - InternalColor enum
 *
 * External format (v1 API) uses:
 * - Square strings (A1-H8)
 * - Piece symbols (K, Q, R, B, N, P, k, q, r, b, n, p)
 * - Color strings ('white', 'black')
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.boardToConfig = boardToConfig;
exports.configToBoard = configToBoard;
exports.configToFEN = configToFEN;
exports.movesToMap = movesToMap;
exports.movesFromSquare = movesFromSquare;
exports.pieceToSymbol = pieceToSymbol;
exports.symbolToPiece = symbolToPiece;
exports.colorToInternal = colorToInternal;
exports.internalToColor = internalToColor;
exports.normalizeSquare = normalizeSquare;
const types_1 = require("../types");
const conversion_1 = require("../utils/conversion");
/**
 * Convert internal board to public board configuration
 *
 * @param board - Internal board representation
 * @returns Public board configuration (v1 API format)
 */
function boardToConfig(board) {
    const pieces = {};
    // Convert mailbox to pieces object
    for (let i = 0; i < 64; i++) {
        const piece = board.mailbox[i];
        if (piece !== types_1.Piece.EMPTY) {
            const square = (0, conversion_1.indexToSquare)(i);
            const symbol = pieceToSymbol(piece);
            if (symbol) {
                pieces[square] = symbol;
            }
        }
    }
    return {
        pieces,
        turn: board.turn === types_1.InternalColor.WHITE ? 'white' : 'black',
        isFinished: board.isCheckmate || board.isStalemate,
        check: board.isCheck,
        checkMate: board.isCheckmate,
        staleMate: board.isStalemate,
        castling: { ...board.castlingRights },
        enPassant: board.enPassantSquare !== null ? (0, conversion_1.indexToSquare)(board.enPassantSquare) : null,
        halfMove: board.halfMoveClock,
        fullMove: board.fullMoveNumber,
    };
}
/**
 * Convert public board configuration to internal board
 *
 * @param config - Public board configuration
 * @returns Internal board representation
 */
function configToBoard(config) {
    // We'll use FEN conversion for this as it's more straightforward
    // First convert config to FEN, then parse FEN to internal board
    // However, for simplicity, we can also build it directly
    const { parseFEN } = require('../utils/fen');
    const fen = configToFEN(config);
    return parseFEN(fen);
}
/**
 * Convert board configuration to FEN string
 *
 * @param config - Public board configuration
 * @returns FEN string
 */
function configToFEN(config) {
    // Build piece placement string
    const ranks = [];
    for (let rank = 7; rank >= 0; rank--) {
        let rankStr = '';
        let emptyCount = 0;
        for (let file = 0; file < 8; file++) {
            const square = (0, conversion_1.indexToSquare)((rank * 8 + file));
            const piece = config.pieces[square];
            if (!piece) {
                emptyCount++;
            }
            else {
                if (emptyCount > 0) {
                    rankStr += emptyCount.toString();
                    emptyCount = 0;
                }
                rankStr += piece;
            }
        }
        if (emptyCount > 0) {
            rankStr += emptyCount.toString();
        }
        ranks.push(rankStr);
    }
    const piecePlacement = ranks.join('/');
    const activeColor = config.turn === 'white' ? 'w' : 'b';
    let castling = '';
    if (config.castling.whiteShort)
        castling += 'K';
    if (config.castling.whiteLong)
        castling += 'Q';
    if (config.castling.blackShort)
        castling += 'k';
    if (config.castling.blackLong)
        castling += 'q';
    if (!castling)
        castling = '-';
    const enPassant = config.enPassant ? config.enPassant.toLowerCase() : '-';
    const halfMove = config.halfMove.toString();
    const fullMove = config.fullMove.toString();
    return `${piecePlacement} ${activeColor} ${castling} ${enPassant} ${halfMove} ${fullMove}`;
}
/**
 * Convert internal moves to public moves map
 *
 * @param moves - Array of internal moves
 * @returns Public moves map (from-square -> [to-squares])
 */
function movesToMap(moves) {
    const movesMap = {};
    for (const move of moves) {
        const fromSquare = (0, conversion_1.indexToSquare)(move.from);
        const toSquare = (0, conversion_1.indexToSquare)(move.to);
        if (!movesMap[fromSquare]) {
            movesMap[fromSquare] = [];
        }
        movesMap[fromSquare].push(toSquare);
    }
    return movesMap;
}
/**
 * Convert internal moves from a specific square to array of to-squares
 *
 * @param moves - Array of internal moves
 * @param fromIndex - From square index
 * @returns Array of to-square strings
 */
function movesFromSquare(moves, fromIndex) {
    return moves
        .filter(move => move.from === fromIndex)
        .map(move => (0, conversion_1.indexToSquare)(move.to));
}
/**
 * Convert piece enum to piece symbol
 *
 * @param piece - Internal piece enum
 * @returns Piece symbol or null if empty
 */
function pieceToSymbol(piece) {
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
        default: return null;
    }
}
/**
 * Convert piece symbol to piece enum
 *
 * @param symbol - Piece symbol
 * @returns Internal piece enum
 */
function symbolToPiece(symbol) {
    switch (symbol) {
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
    }
}
/**
 * Convert color string to internal color
 *
 * @param color - Color string
 * @returns Internal color enum
 */
function colorToInternal(color) {
    return color === 'white' ? types_1.InternalColor.WHITE : types_1.InternalColor.BLACK;
}
/**
 * Convert internal color to color string
 *
 * @param color - Internal color enum
 * @returns Color string
 */
function internalToColor(color) {
    return color === types_1.InternalColor.WHITE ? 'white' : 'black';
}
/**
 * Normalize square string to uppercase (A1-H8)
 * V1 API accepts case-insensitive input
 *
 * @param square - Square string (case-insensitive)
 * @returns Normalized uppercase square string
 */
function normalizeSquare(square) {
    return square.toUpperCase();
}
//# sourceMappingURL=APIAdapter.js.map