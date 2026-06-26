"use strict";
/**
 * Anchor event parsing for torch_market transactions.
 *
 * UIs can call `parseLoanRepaidEvents(tx)` / `parseShortClosedEvents(tx)`
 * after a successful repay / close_short to learn whether the position was
 * fully settled. When the corresponding `fully_repaid` / `fully_closed` flag
 * is true, the program also closes the position PDA and refunds rent — so the
 * UI should re-render "no active loan/short" rather than "zeroed loan/short".
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseShortClosedEvents = exports.parseLoanRepaidEvents = void 0;
exports.parseEvents = parseEvents;
const anchor_1 = require("@coral-xyz/anchor");
const torch_market_json_1 = __importDefault(require("./torch_market.json"));
const coder = new anchor_1.BorshEventCoder(torch_market_json_1.default);
/**
 * Extract every emitted event with the given name from a parsed transaction.
 * Returns [] if the tx is null, has no logs, or contains no matching events.
 *
 * Anchor events are written to `Program data: <base64>` log lines.
 * BorshEventCoder decodes the discriminator + payload.
 */
function parseEvents(tx, eventName) {
    const logs = tx?.meta?.logMessages;
    if (!logs?.length)
        return [];
    const events = [];
    for (const log of logs) {
        const m = /^Program data: (.+)$/.exec(log);
        if (!m)
            continue;
        try {
            const decoded = coder.decode(m[1]);
            if (decoded && decoded.name === eventName) {
                events.push(decoded.data);
            }
        }
        catch {
            // Not every "Program data" line is one of our events.
        }
    }
    return events;
}
const parseLoanRepaidEvents = (tx) => parseEvents(tx, 'LoanRepaid');
exports.parseLoanRepaidEvents = parseLoanRepaidEvents;
const parseShortClosedEvents = (tx) => parseEvents(tx, 'ShortClosed');
exports.parseShortClosedEvents = parseShortClosedEvents;
//# sourceMappingURL=events.js.map