/**
 * Pyre vanity mint address grinder
 *
 * Grinds for Solana keypairs whose base58 address ends with "pyre".
 * This is how we distinguish pyre faction tokens from regular torch tokens —
 * no registry program needed, just check the mint suffix.
 */
import { Connection, PublicKey, Keypair } from '@solana/web3.js';
import type { CreateTokenResult, CreateTokenParams } from 'torchsdk';
export declare const getBondingCurvePda: (mint: PublicKey) => [PublicKey, number];
export declare const getTokenTreasuryPda: (mint: PublicKey) => [PublicKey, number];
export declare const getTreasuryLockPda: (mint: PublicKey) => [PublicKey, number];
/** Grind for a keypair whose base58 address ends with "pr" (pyre) */
export declare const grindPyreMint: (maxAttempts?: number) => Keypair;
/** Check if a mint address is a pyre faction (ends with "pr") */
export declare const isPyreMint: (mint: string) => boolean;
export declare const buildCreateFactionTransaction: (connection: Connection, params: CreateTokenParams) => Promise<CreateTokenResult>;
