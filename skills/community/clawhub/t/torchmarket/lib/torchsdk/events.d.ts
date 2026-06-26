/**
 * Anchor event parsing for torch_market transactions.
 *
 * UIs can call `parseLoanRepaidEvents(tx)` / `parseShortClosedEvents(tx)`
 * after a successful repay / close_short to learn whether the position was
 * fully settled. When the corresponding `fully_repaid` / `fully_closed` flag
 * is true, the program also closes the position PDA and refunds rent — so the
 * UI should re-render "no active loan/short" rather than "zeroed loan/short".
 */
import { BN } from '@coral-xyz/anchor';
import { ParsedTransactionWithMeta, PublicKey } from '@solana/web3.js';
export interface LoanRepaidEvent {
    mint: PublicKey;
    user: PublicKey;
    sol_repaid: BN;
    interest_paid: BN;
    collateral_returned: BN;
    fully_repaid: boolean;
}
export interface ShortClosedEvent {
    mint: PublicKey;
    user: PublicKey;
    tokens_returned: BN;
    interest_paid_tokens: BN;
    sol_returned: BN;
    fully_closed: boolean;
}
/**
 * Extract every emitted event with the given name from a parsed transaction.
 * Returns [] if the tx is null, has no logs, or contains no matching events.
 *
 * Anchor events are written to `Program data: <base64>` log lines.
 * BorshEventCoder decodes the discriminator + payload.
 */
export declare function parseEvents<T = unknown>(tx: ParsedTransactionWithMeta | null | undefined, eventName: string): T[];
export declare const parseLoanRepaidEvents: (tx: ParsedTransactionWithMeta | null | undefined) => LoanRepaidEvent[];
export declare const parseShortClosedEvents: (tx: ParsedTransactionWithMeta | null | undefined) => ShortClosedEvent[];
//# sourceMappingURL=events.d.ts.map