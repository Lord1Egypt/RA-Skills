import type { AllLoanPositionsResult, BuyTransactionResult, CreateTokenResult, Holder, HoldersResult, LendingInfo, LoanPositionInfo, LoanPositionWithKey, MessagesResult, TokenDetail, TokenListResult, TokenMessage, TokenStatus, TokenSummary, VaultInfo, VaultWalletLinkInfo } from 'torchsdk';
import type { FactionStatus, FactionStatusFilter } from '../types';
import { Mapper } from '../types/mapper.types';
export declare class MapperProvider implements Mapper {
    allLoansResult: (r: AllLoanPositionsResult) => {
        positions: {
            borrower: string;
            collateral_amount: number;
            borrowed_amount: number;
            accrued_interest: number;
            total_owed: number;
            collateral_value_sol: number | null;
            current_ltv_bps: number | null;
            health: "healthy" | "at_risk" | "liquidatable" | "none";
            warnings: string[] | undefined;
        }[];
        pool_price_sol: number | null;
    };
    buyResult: (r: BuyTransactionResult) => {
        transaction: import("@solana/web3.js").VersionedTransaction;
        additionalTransactions: import("@solana/web3.js").VersionedTransaction[] | undefined;
        message: string;
        migrationTransaction: import("@solana/web3.js").VersionedTransaction | undefined;
    };
    createResult: (r: CreateTokenResult) => {
        transaction: import("@solana/web3.js").VersionedTransaction;
        additionalTransactions: import("@solana/web3.js").VersionedTransaction[] | undefined;
        message: string;
        mint: import("@solana/web3.js").PublicKey;
        mintKeypair: import("@solana/web3.js").Keypair;
    };
    factionStatus: (status: TokenStatus) => FactionStatus;
    holdersResult: (r: HoldersResult) => {
        members: {
            address: string;
            balance: number;
            percentage: number;
        }[];
        total_members: number;
    };
    holderToMember: (h: Holder) => {
        address: string;
        balance: number;
        percentage: number;
    };
    lendingToWarChest: (l: LendingInfo) => {
        interest_rate_bps: number;
        max_ltv_bps: number;
        liquidation_threshold_bps: number;
        liquidation_bonus_bps: number;
        utilization_cap_bps: number;
        borrow_share_multiplier: number;
        total_sol_lent: number | null;
        active_loans: number | null;
        war_chest_sol_available: number;
        warnings: string[] | undefined;
    };
    loanToWarLoan: (l: LoanPositionInfo) => {
        collateral_amount: number;
        borrowed_amount: number;
        accrued_interest: number;
        total_owed: number;
        collateral_value_sol: number | null;
        current_ltv_bps: number | null;
        health: "healthy" | "at_risk" | "liquidatable" | "none";
        warnings: string[] | undefined;
    };
    loanWithKeyToWarLoan: (l: LoanPositionWithKey) => {
        borrower: string;
        collateral_amount: number;
        borrowed_amount: number;
        accrued_interest: number;
        total_owed: number;
        collateral_value_sol: number | null;
        current_ltv_bps: number | null;
        health: "healthy" | "at_risk" | "liquidatable" | "none";
        warnings: string[] | undefined;
    };
    messagesResult: (r: MessagesResult) => {
        comms: {
            signature: string;
            memo: string;
            sender: string;
            timestamp: number;
            sender_verified: boolean | undefined;
            sender_trust_tier: "high" | "medium" | "low" | null | undefined;
            sender_said_name: string | undefined;
            sender_badge_url: string | undefined;
        }[];
        total: number;
    };
    tokenDetailToFaction: (t: TokenDetail) => {
        mint: string;
        name: string;
        symbol: string;
        description: string | undefined;
        image: string | undefined;
        status: FactionStatus;
        price_sol: number;
        price_usd: number | undefined;
        market_cap_sol: number;
        market_cap_usd: number | undefined;
        progress_percent: number;
        sol_raised: number;
        sol_target: number;
        total_supply: number;
        circulating_supply: number;
        tokens_in_curve: number;
        tokens_burned: number;
        war_chest_sol: number;
        war_chest_tokens: number;
        total_bought_back: number;
        buyback_count: number;
        founder: string;
        members: number | null;
        rallies: number;
        created_at: number;
        last_activity_at: number;
        twitter: string | undefined;
        telegram: string | undefined;
        website: string | undefined;
        founder_verified: boolean | undefined;
        founder_trust_tier: "high" | "medium" | "low" | null | undefined;
        founder_said_name: string | undefined;
        founder_badge_url: string | undefined;
        warnings: string[] | undefined;
    };
    tokenListResult: (r: TokenListResult) => {
        factions: {
            mint: string;
            name: string;
            symbol: string;
            status: FactionStatus;
            price_sol: number;
            market_cap_sol: number;
            progress_percent: number;
            members: number | null;
            created_at: number;
            last_activity_at: number;
        }[];
        total: number;
        limit: number;
        offset: number;
    };
    tokenMessageToComms: (m: TokenMessage) => {
        signature: string;
        memo: string;
        sender: string;
        timestamp: number;
        sender_verified: boolean | undefined;
        sender_trust_tier: "high" | "medium" | "low" | null | undefined;
        sender_said_name: string | undefined;
        sender_badge_url: string | undefined;
    };
    tokenStatus: (status: FactionStatus) => TokenStatus;
    tokenStatusFilter: (status: FactionStatusFilter) => import("torchsdk").TokenStatusFilter;
    tokenSummaryToFaction: (t: TokenSummary) => {
        mint: string;
        name: string;
        symbol: string;
        status: FactionStatus;
        price_sol: number;
        market_cap_sol: number;
        progress_percent: number;
        members: number | null;
        created_at: number;
        last_activity_at: number;
    };
    vaultToStronghold: (v: VaultInfo) => {
        address: string;
        creator: string;
        authority: string;
        sol_balance: number;
        total_deposited: number;
        total_withdrawn: number;
        total_spent: number;
        total_received: number;
        linked_agents: number;
        created_at: number;
    };
    walletLinkToAgentLink: (l: VaultWalletLinkInfo) => {
        address: string;
        stronghold: string;
        wallet: string;
        linked_at: number;
    };
}
