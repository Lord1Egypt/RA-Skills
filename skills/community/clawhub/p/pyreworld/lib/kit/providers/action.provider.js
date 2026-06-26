"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ActionProvider = void 0;
const web3_js_1 = require("@solana/web3.js");
const torchsdk_1 = require("torchsdk");
const mapper_provider_1 = require("./mapper.provider");
const vanity_1 = require("../vanity");
const util_1 = require("../util");
class ActionProvider {
    connection;
    registryProvider;
    mapper = new mapper_provider_1.MapperProvider();
    constructor(connection, registryProvider) {
        this.connection = connection;
        this.registryProvider = registryProvider;
    }
    async createStronghold(params) {
        return (0, torchsdk_1.buildCreateVaultTransaction)(this.connection, { creator: params.creator });
    }
    async coup(params) {
        return (0, torchsdk_1.buildTransferAuthorityTransaction)(this.connection, {
            authority: params.authority,
            vault_creator: params.stronghold_creator,
            new_authority: params.new_authority,
        });
    }
    async exileAgent(params) {
        return (0, torchsdk_1.buildUnlinkWalletTransaction)(this.connection, {
            authority: params.authority,
            vault_creator: params.stronghold_creator,
            wallet_to_unlink: params.wallet_to_unlink,
        });
    }
    async fundStronghold(params) {
        return (0, torchsdk_1.buildDepositVaultTransaction)(this.connection, {
            depositor: params.depositor,
            vault_creator: params.stronghold_creator,
            amount_sol: params.amount_sol,
        });
    }
    async recruitAgent(params) {
        return (0, torchsdk_1.buildLinkWalletTransaction)(this.connection, {
            authority: params.authority,
            vault_creator: params.stronghold_creator,
            wallet_to_link: params.wallet_to_link,
        });
    }
    async withdrawAssets(params) {
        return (0, torchsdk_1.buildWithdrawTokensTransaction)(this.connection, {
            authority: params.authority,
            vault_creator: params.stronghold_creator,
            mint: params.mint,
            destination: params.destination,
            amount: params.amount,
        });
    }
    async withdrawFromStronghold(params) {
        return (0, torchsdk_1.buildWithdrawVaultTransaction)(this.connection, {
            authority: params.authority,
            vault_creator: params.stronghold_creator,
            amount_sol: params.amount_sol,
        });
    }
    async getAgentLink(wallet) {
        const link = await (0, torchsdk_1.getVaultWalletLink)(this.connection, wallet);
        return link ? this.mapper.walletLinkToAgentLink(link) : undefined;
    }
    async getComms(mint, { limit, status }) {
        const source = status === 'ascended' ? 'pool' : status ? 'bonding' : 'all';
        const result = await (0, torchsdk_1.getMessages)(this.connection, mint, limit, { source });
        return this.mapper.messagesResult(result);
    }
    async getDefectQuote(mint, amountTokens) {
        return (0, torchsdk_1.getSellQuote)(this.connection, mint, amountTokens);
    }
    async getJoinQuote(mint, amountSolLamports) {
        return (0, torchsdk_1.getBuyQuote)(this.connection, mint, amountSolLamports);
    }
    async getFaction(mint) {
        const detail = await (0, torchsdk_1.getToken)(this.connection, mint);
        return this.mapper.tokenDetailToFaction(detail);
    }
    async getFactions(params) {
        const sdkParams = params
            ? {
                limit: params.limit,
                offset: params.offset,
                status: params.status ? this.mapper.tokenStatusFilter(params.status) : undefined,
                sort: params.sort,
            }
            : undefined;
        const result = await (0, torchsdk_1.getTokens)(this.connection, sdkParams);
        const tokens = result.tokens.filter((t) => (0, vanity_1.isPyreMint)(t.mint));
        return this.mapper.tokenListResult({
            tokens: result.tokens.filter((t) => (0, vanity_1.isPyreMint)(t.mint) && !(0, util_1.isBlacklistedMint)(t.mint)),
            limit: result.limit,
            offset: result.offset,
            total: tokens.length,
        });
    }
    async getLinkedAgents(vaultAddress) {
        const vaultPubkey = new web3_js_1.PublicKey(vaultAddress);
        const filters = [
            { dataSize: 81 }, // 8 + 32 + 32 + 8 + 1
            { memcmp: { offset: 8, bytes: vaultPubkey.toBase58() } },
        ];
        const accounts = await this.connection.getProgramAccounts(torchsdk_1.PROGRAM_ID, { filters });
        return accounts.map((acc) => {
            const data = acc.account.data;
            const wallet = new web3_js_1.PublicKey(data.subarray(40, 72)).toBase58();
            const linked_at = Number(data.readBigInt64LE(72));
            return {
                address: acc.pubkey.toBase58(),
                stronghold: vaultAddress,
                wallet,
                linked_at,
            };
        });
    }
    async getMembers(mint, limit) {
        const mintPk = new web3_js_1.PublicKey(mint);
        const [bondingCurve] = (0, vanity_1.getBondingCurvePda)(mintPk);
        const [treasury] = (0, vanity_1.getTokenTreasuryPda)(mintPk);
        const [treasuryLock] = (0, vanity_1.getTreasuryLockPda)(mintPk);
        const excluded = new Set([
            bondingCurve.toString(),
            treasury.toString(),
            treasuryLock.toString(),
        ]);
        // Fetch extra to compensate for filtered-out program accounts
        const result = await (0, torchsdk_1.getHolders)(this.connection, mint, (limit ?? 10) + 5);
        result.holders = result.holders.filter((h) => !excluded.has(h.address));
        if (limit)
            result.holders = result.holders.slice(0, limit);
        return this.mapper.holdersResult(result);
    }
    async getStronghold(creator) {
        const vault = await (0, torchsdk_1.getVault)(this.connection, creator);
        return vault ? this.mapper.vaultToStronghold(vault) : undefined;
    }
    async getStrongholdForAgent(wallet) {
        const vault = await (0, torchsdk_1.getVaultForWallet)(this.connection, wallet);
        return vault ? this.mapper.vaultToStronghold(vault) : undefined;
    }
    async getWarChest(mint) {
        const info = await (0, torchsdk_1.getLendingInfo)(this.connection, mint);
        return this.mapper.lendingToWarChest(info);
    }
    async getWarLoan(mint, wallet) {
        const pos = await (0, torchsdk_1.getLoanPosition)(this.connection, mint, wallet);
        return this.mapper.loanToWarLoan(pos);
    }
    async getWarLoanQuote(mint, collateralAmount) {
        return (0, torchsdk_1.getBorrowQuote)(this.connection, mint, collateralAmount);
    }
    async getWarLoansForFaction(mint) {
        const result = await (0, torchsdk_1.getAllLoanPositions)(this.connection, mint);
        return this.mapper.allLoansResult(result);
    }
    async ascend(params) {
        return (0, torchsdk_1.buildMigrateTransaction)(this.connection, {
            mint: params.mint,
            payer: params.payer,
        });
    }
    async claimSpoils(params) {
        return (0, torchsdk_1.buildClaimProtocolRewardsTransaction)(this.connection, {
            user: params.agent,
            vault: params.stronghold,
        });
    }
    async defect(params) {
        return (0, torchsdk_1.buildSellTransaction)(this.connection, {
            mint: params.mint,
            seller: params.agent,
            amount_tokens: params.amount_tokens,
            slippage_bps: params.slippage_bps,
            message: params.message,
            vault: params.stronghold,
        });
    }
    async fud(params) {
        const MICRO_SELL_TOKENS = 10 * 1_000_000; // 10 tokens in raw units (6 decimals)
        return (0, torchsdk_1.buildSellTransaction)(this.connection, {
            mint: params.mint,
            seller: params.agent,
            amount_tokens: MICRO_SELL_TOKENS,
            message: params.message,
            vault: params.stronghold,
        });
    }
    async join(params) {
        const result = await (0, torchsdk_1.buildBuyTransaction)(this.connection, {
            mint: params.mint,
            buyer: params.agent,
            amount_sol: params.amount_sol,
            slippage_bps: params.slippage_bps,
            message: params.message,
            vault: params.stronghold,
        });
        return this.mapper.buyResult(result);
    }
    async launch(params) {
        const result = await (0, vanity_1.buildCreateFactionTransaction)(this.connection, {
            creator: params.founder,
            name: params.name,
            symbol: params.symbol,
            metadata_uri: params.metadata_uri,
            sol_target: params.sol_target,
            community_token: params.community_faction,
        });
        return this.mapper.createResult(result);
    }
    async message(params) {
        const MICRO_BUY_LAMPORTS = 1_000_000; // 0.001 SOL
        const result = await (0, torchsdk_1.buildBuyTransaction)(this.connection, {
            mint: params.mint,
            buyer: params.agent,
            amount_sol: MICRO_BUY_LAMPORTS,
            message: params.message,
            vault: params.stronghold,
        });
        return this.mapper.buyResult(result);
    }
    async rally(params) {
        return (0, torchsdk_1.buildStarTransaction)(this.connection, {
            mint: params.mint,
            user: params.agent,
            vault: params.stronghold,
        });
    }
    async raze(params) {
        return (0, torchsdk_1.buildReclaimFailedTokenTransaction)(this.connection, {
            payer: params.payer,
            mint: params.mint,
        });
    }
    async repayWarLoan(params) {
        return (0, torchsdk_1.buildRepayTransaction)(this.connection, {
            mint: params.mint,
            borrower: params.borrower,
            sol_amount: params.sol_amount,
            vault: params.stronghold,
        });
    }
    async requestWarLoan(params) {
        return (0, torchsdk_1.buildBorrowTransaction)(this.connection, {
            mint: params.mint,
            borrower: params.borrower,
            collateral_amount: params.collateral_amount,
            sol_to_borrow: params.sol_to_borrow,
            vault: params.stronghold,
        });
    }
    async scout(targetAddress) {
        try {
            const p = await this.registryProvider.getProfile(targetAddress);
            if (!p)
                return `  @${targetAddress.slice(0, 8)}: no pyre identity found`;
            const total = p.joins +
                p.defects +
                p.rallies +
                p.launches +
                p.messages +
                p.fuds +
                p.infiltrates +
                p.reinforces +
                p.war_loans +
                p.repay_loans +
                p.sieges +
                p.ascends +
                p.razes +
                p.tithes;
            const topActions = [
                { n: 'joins', v: p.joins },
                { n: 'defects', v: p.defects },
                { n: 'rallies', v: p.rallies },
                { n: 'messages', v: p.messages },
                { n: 'fuds', v: p.fuds },
                { n: 'infiltrates', v: p.infiltrates },
                { n: 'reinforces', v: p.reinforces },
                { n: 'war_loans', v: p.war_loans },
                { n: 'sieges', v: p.sieges },
            ]
                .sort((a, b) => b.v - a.v)
                .filter((a) => a.v > 0)
                .slice(0, 4)
                .map((a) => `${a.n}:${a.v}`)
                .join(', ');
            const personality = p.personality_summary || 'unknown';
            const checkpoint = p.last_checkpoint > 0
                ? new Date(p.last_checkpoint * 1000).toISOString().slice(0, 10)
                : 'never';
            const spent = (p.total_sol_spent ?? 0) / 1e9;
            const received = (p.total_sol_received ?? 0) / 1e9;
            const pnl = received - spent;
            const pnlStr = pnl >= 0 ? `+${pnl.toFixed(3)}` : pnl.toFixed(3);
            return `  @${targetAddress.slice(0, 8)}: "${personality}" | ${total} actions (${topActions}) | P&L: ${pnlStr} SOL | last seen: ${checkpoint}`;
        }
        catch {
            return `  @${targetAddress.slice(0, 8)}: lookup failed`;
        }
    }
    async siege(params) {
        return (0, torchsdk_1.buildLiquidateTransaction)(this.connection, {
            mint: params.mint,
            liquidator: params.liquidator,
            borrower: params.borrower,
            vault: params.stronghold,
        });
    }
    async tithe(params) {
        return (0, torchsdk_1.buildSwapFeesToSolTransaction)(this.connection, {
            mint: params.mint,
            payer: params.payer,
            minimum_amount_out: params.minimum_amount_out,
            harvest: true,
            sources: params.sources,
        });
    }
}
exports.ActionProvider = ActionProvider;
