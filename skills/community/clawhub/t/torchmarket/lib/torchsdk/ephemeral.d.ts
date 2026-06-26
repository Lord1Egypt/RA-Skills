import { Keypair, Transaction, VersionedTransaction } from '@solana/web3.js';
export interface EphemeralAgent {
    publicKey: string;
    keypair: Keypair;
    sign(tx: Transaction | VersionedTransaction): Transaction | VersionedTransaction;
}
export declare const createEphemeralAgent: () => EphemeralAgent;
//# sourceMappingURL=ephemeral.d.ts.map