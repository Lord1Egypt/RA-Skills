import { CheckpointParams, LinkAgentWalletParams, RegisterAgentParams, RegistryProfile, RegistryWalletLink, TransactionResult, TransferAgentAuthorityParams, UnlinkAgentWalletParams } from '../types';
export interface Registry {
    getProfile(creator: string): Promise<RegistryProfile | undefined>;
    getWalletLink(wallet: string): Promise<RegistryWalletLink | undefined>;
    register(params: RegisterAgentParams): Promise<TransactionResult>;
    checkpoint(params: CheckpointParams): Promise<TransactionResult>;
    linkWallet(params: LinkAgentWalletParams): Promise<TransactionResult>;
    unlinkWallet(params: UnlinkAgentWalletParams): Promise<TransactionResult>;
    transferAuthority(params: TransferAgentAuthorityParams): Promise<TransactionResult>;
}
