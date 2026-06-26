import { Connection, PublicKey } from '@solana/web3.js';
import type { TransactionResult } from 'torchsdk';
import type { RegistryProfile, RegistryWalletLink, RegisterAgentParams, CheckpointParams, LinkAgentWalletParams, UnlinkAgentWalletParams, TransferAgentAuthorityParams } from '../types';
import { Registry } from '../types/registry.types';
export declare const REGISTRY_PROGRAM_ID: PublicKey;
export declare const getAgentProfilePda: (creator: PublicKey) => [PublicKey, number];
export declare const getAgentWalletLinkPda: (wallet: PublicKey) => [PublicKey, number];
export declare class RegistryProvider implements Registry {
    private connection;
    private _programCache;
    constructor(connection: Connection);
    private getProgram;
    getProfile(creator: string): Promise<RegistryProfile | undefined>;
    getWalletLink(wallet: string): Promise<RegistryWalletLink | undefined>;
    register(params: RegisterAgentParams): Promise<TransactionResult>;
    checkpoint(params: CheckpointParams): Promise<TransactionResult>;
    linkWallet(params: LinkAgentWalletParams): Promise<TransactionResult>;
    unlinkWallet(params: UnlinkAgentWalletParams): Promise<TransactionResult>;
    transferAuthority(params: TransferAgentAuthorityParams): Promise<TransactionResult>;
}
