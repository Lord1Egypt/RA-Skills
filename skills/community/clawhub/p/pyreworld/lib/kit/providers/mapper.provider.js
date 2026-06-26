"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MapperProvider = void 0;
const mapper_types_1 = require("../types/mapper.types");
class MapperProvider {
    allLoansResult = (r) => ({
        positions: r.positions.map(this.loanWithKeyToWarLoan),
        pool_price_sol: r.pool_price_sol,
    });
    buyResult = (r) => ({
        transaction: r.transaction,
        additionalTransactions: r.additionalTransactions,
        message: r.message,
        migrationTransaction: r.migrationTransaction,
    });
    createResult = (r) => ({
        transaction: r.transaction,
        additionalTransactions: r.additionalTransactions,
        message: r.message,
        mint: r.mint,
        mintKeypair: r.mintKeypair,
    });
    factionStatus = (status) => mapper_types_1.STATUS_MAP[status];
    holdersResult = (r) => ({
        members: r.holders.map(this.holderToMember),
        total_members: r.total_holders,
    });
    holderToMember = (h) => ({
        address: h.address,
        balance: h.balance,
        percentage: h.percentage,
    });
    lendingToWarChest = (l) => ({
        interest_rate_bps: l.interest_rate_bps,
        max_ltv_bps: l.max_ltv_bps,
        liquidation_threshold_bps: l.liquidation_threshold_bps,
        liquidation_bonus_bps: l.liquidation_bonus_bps,
        utilization_cap_bps: l.utilization_cap_bps,
        borrow_share_multiplier: l.borrow_share_multiplier,
        total_sol_lent: l.total_sol_lent,
        active_loans: l.active_loans,
        war_chest_sol_available: l.treasury_sol_available,
        warnings: l.warnings,
    });
    loanToWarLoan = (l) => ({
        collateral_amount: l.collateral_amount,
        borrowed_amount: l.borrowed_amount,
        accrued_interest: l.accrued_interest,
        total_owed: l.total_owed,
        collateral_value_sol: l.collateral_value_sol,
        current_ltv_bps: l.current_ltv_bps,
        health: l.health,
        warnings: l.warnings,
    });
    loanWithKeyToWarLoan = (l) => ({
        ...this.loanToWarLoan(l),
        borrower: l.borrower,
    });
    messagesResult = (r) => ({
        comms: r.messages.map(this.tokenMessageToComms),
        total: r.total,
    });
    tokenDetailToFaction = (t) => ({
        mint: t.mint,
        name: t.name,
        symbol: t.symbol,
        description: t.description,
        image: t.image,
        status: this.factionStatus(t.status),
        price_sol: t.price_sol,
        price_usd: t.price_usd,
        market_cap_sol: t.market_cap_sol,
        market_cap_usd: t.market_cap_usd,
        progress_percent: t.progress_percent,
        sol_raised: t.sol_raised,
        sol_target: t.sol_target,
        total_supply: t.total_supply,
        circulating_supply: t.circulating_supply,
        tokens_in_curve: t.tokens_in_curve,
        tokens_burned: t.tokens_burned,
        war_chest_sol: t.treasury_sol_balance,
        war_chest_tokens: t.treasury_token_balance,
        total_bought_back: t.total_bought_back,
        buyback_count: t.buyback_count,
        founder: t.creator,
        members: t.holders,
        rallies: t.stars,
        created_at: t.created_at,
        last_activity_at: t.last_activity_at,
        twitter: t.twitter,
        telegram: t.telegram,
        website: t.website,
        founder_verified: t.creator_verified,
        founder_trust_tier: t.creator_trust_tier,
        founder_said_name: t.creator_said_name,
        founder_badge_url: t.creator_badge_url,
        warnings: t.warnings,
    });
    tokenListResult = (r) => ({
        factions: r.tokens.map(this.tokenSummaryToFaction),
        total: r.total,
        limit: r.limit,
        offset: r.offset,
    });
    tokenMessageToComms = (m) => ({
        signature: m.signature,
        memo: m.memo,
        sender: m.sender,
        timestamp: m.timestamp,
        sender_verified: m.sender_verified,
        sender_trust_tier: m.sender_trust_tier,
        sender_said_name: m.sender_said_name,
        sender_badge_url: m.sender_badge_url,
    });
    tokenStatus = (status) => mapper_types_1.STATUS_REVERSE[status];
    tokenStatusFilter = (status) => mapper_types_1.STATUS_FILTER_REVERSE[status];
    tokenSummaryToFaction = (t) => ({
        mint: t.mint,
        name: t.name,
        symbol: t.symbol,
        status: this.factionStatus(t.status),
        price_sol: t.price_sol,
        market_cap_sol: t.market_cap_sol,
        progress_percent: t.progress_percent,
        members: t.holders,
        created_at: t.created_at,
        last_activity_at: t.last_activity_at,
    });
    vaultToStronghold = (v) => ({
        address: v.address,
        creator: v.creator,
        authority: v.authority,
        sol_balance: v.sol_balance,
        total_deposited: v.total_deposited,
        total_withdrawn: v.total_withdrawn,
        total_spent: v.total_spent,
        total_received: v.total_received,
        linked_agents: v.linked_wallets,
        created_at: v.created_at,
    });
    walletLinkToAgentLink = (l) => ({
        address: l.address,
        stronghold: l.vault,
        wallet: l.wallet,
        linked_at: l.linked_at,
    });
}
exports.MapperProvider = MapperProvider;
