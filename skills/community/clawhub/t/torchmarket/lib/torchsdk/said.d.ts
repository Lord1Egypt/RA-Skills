/**
 * SAID Protocol integration
 *
 * Verify wallet reputation and confirm transactions for SAID feedback.
 */
import { Connection } from '@solana/web3.js';
import { SaidVerification, ConfirmResult } from './types';
/**
 * Check SAID verification status for a wallet.
 *
 * @param wallet - Wallet address to verify
 * @returns Verification status including trust tier
 */
export declare const verifySaid: (wallet: string) => Promise<SaidVerification>;
/**
 * Confirm a transaction on-chain and determine event type.
 *
 * After an agent submits a transaction, call this to verify it succeeded
 * and determine the event type for reputation tracking.
 *
 * @param connection - Solana RPC connection
 * @param signature - Transaction signature to confirm
 * @param wallet - Wallet address that signed the transaction
 * @returns Confirmation result with event type
 */
export declare const confirmTransaction: (connection: Connection, signature: string, wallet: string) => Promise<ConfirmResult>;
//# sourceMappingURL=said.d.ts.map