/**
 * Ephemeral Agent Keypair
 *
 * Generates an in-process keypair that lives only in memory.
 * The authority links this wallet to their vault, and the SDK
 * uses it to sign transactions. When the process stops, the
 * private key is lost — zero key management, zero risk.
 *
 * Flow:
 *   1. const agent = createEphemeralAgent()
 *   2. Authority calls buildLinkWalletTransaction({ wallet_to_link: agent.publicKey })
 *   3. SDK uses agent.sign(tx) for all vault operations
 *   4. On shutdown, keys are GC'd. Authority unlinks the wallet.
 */
import { Keypair, Transaction, VersionedTransaction } from '@solana/web3.js';
export interface EphemeralAgent {
    /** Base58 public key — pass this to linkWallet */
    publicKey: string;
    /** Raw keypair for advanced usage */
    keypair: Keypair;
    /** Sign a transaction with the ephemeral key */
    sign(tx: Transaction | VersionedTransaction): Transaction | VersionedTransaction;
}
/**
 * Create an ephemeral agent keypair.
 *
 * The keypair exists only in memory. No file is written to disk.
 * When the process exits, the private key is permanently lost.
 *
 * @returns EphemeralAgent with publicKey, sign function, and raw keypair
 */
export declare const createEphemeralAgent: () => EphemeralAgent;
//# sourceMappingURL=ephemeral.d.ts.map