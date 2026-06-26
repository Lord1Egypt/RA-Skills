"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.StateProvider = void 0;
const web3_js_1 = require("@solana/web3.js");
const vanity_1 = require("../vanity");
const util_1 = require("../util");
// Pre-warm imports — resolved once, cached as module-level promises
const splTokenImport = Promise.resolve().then(() => __importStar(require('@solana/spl-token')));
const torchsdkImport = Promise.resolve().then(() => __importStar(require('torchsdk')));
const EMPTY_COUNTS = {
    join: 0,
    defect: 0,
    rally: 0,
    launch: 0,
    message: 0,
    reinforce: 0,
    war_loan: 0,
    repay_loan: 0,
    siege: 0,
    ascend: 0,
    raze: 0,
    tithe: 0,
    infiltrate: 0,
    fud: 0,
};
class StateProvider {
    connection;
    registry;
    publicKey;
    _state = null;
    checkpointConfig = null;
    ticksSinceCheckpoint = 0;
    // Lazy vault — undefined = not resolved, null = resolved to nothing
    _vaultCreator = undefined;
    _stronghold = undefined;
    _vaultPromise = null;
    constructor(connection, registry, publicKey) {
        this.connection = connection;
        this.registry = registry;
        this.publicKey = publicKey;
    }
    get state() {
        return this._state;
    }
    get initialized() {
        return this._state?.initialized ?? false;
    }
    get tick() {
        return this._state?.tick ?? 0;
    }
    setCheckpointConfig(config) {
        this.checkpointConfig = config;
    }
    async resolveVault() {
        if (this._vaultCreator !== undefined)
            return;
        if (!this._vaultPromise) {
            this._vaultPromise = (async () => {
                const { getVaultForWallet } = await torchsdkImport;
                try {
                    const vault = await getVaultForWallet(this.connection, this.publicKey);
                    if (vault) {
                        this._vaultCreator = vault.creator;
                        this._stronghold = {
                            address: vault.address,
                            creator: vault.creator,
                            authority: vault.authority,
                            sol_balance: vault.sol_balance,
                            total_deposited: vault.total_deposited,
                            total_withdrawn: vault.total_withdrawn,
                            total_spent: vault.total_spent,
                            total_received: vault.total_received,
                            linked_agents: vault.linked_wallets,
                            created_at: vault.created_at,
                        };
                    }
                    else {
                        this._vaultCreator = null;
                        this._stronghold = null;
                    }
                }
                catch {
                    this._vaultCreator = null;
                    this._stronghold = null;
                }
                this._vaultPromise = null;
            })();
        }
        return this._vaultPromise;
    }
    async getVaultCreator() {
        await this.resolveVault();
        return this._vaultCreator ?? null;
    }
    async getStronghold() {
        await this.resolveVault();
        return this._stronghold ?? null;
    }
    async init() {
        if (!this._state?.initialized) {
            const state = {
                publicKey: this.publicKey,
                tick: 0,
                actionCounts: { ...EMPTY_COUNTS },
                activeLoans: new Set(),
                founded: [],
                rallied: new Set(),
                voted: new Set(),
                sentiment: new Map(),
                recentHistory: [],
                personalitySummary: null,
                totalSolSpent: 0,
                totalSolReceived: 0,
                initialized: false,
            };
            // Fire vault resolution in background — don't block init
            this.resolveVault();
            try {
                const profile = await this.registry.getProfile(this.publicKey);
                if (profile) {
                    state.personalitySummary = profile.personality_summary || null;
                    state.totalSolSpent = profile.total_sol_spent;
                    state.totalSolReceived = profile.total_sol_received;
                    state.actionCounts.join = Math.max(state.actionCounts.join, profile.joins);
                    state.actionCounts.defect = Math.max(state.actionCounts.defect, profile.defects);
                    state.actionCounts.rally = Math.max(state.actionCounts.rally, profile.rallies);
                    state.actionCounts.launch = Math.max(state.actionCounts.launch, profile.launches);
                    state.actionCounts.message = Math.max(state.actionCounts.message, profile.messages);
                    state.actionCounts.reinforce = Math.max(state.actionCounts.reinforce, profile.reinforces);
                    state.actionCounts.fud = Math.max(state.actionCounts.fud, profile.fuds);
                    state.actionCounts.infiltrate = Math.max(state.actionCounts.infiltrate, profile.infiltrates);
                    state.actionCounts.war_loan = Math.max(state.actionCounts.war_loan, profile.war_loans);
                    state.actionCounts.repay_loan = Math.max(state.actionCounts.repay_loan, profile.repay_loans);
                    state.actionCounts.siege = Math.max(state.actionCounts.siege, profile.sieges);
                    state.actionCounts.ascend = Math.max(state.actionCounts.ascend, profile.ascends);
                    state.actionCounts.raze = Math.max(state.actionCounts.raze, profile.razes);
                    state.actionCounts.tithe = Math.max(state.actionCounts.tithe, profile.tithes);
                    const totalFromCheckpoint = Object.values(state.actionCounts).reduce((a, b) => a + b, 0);
                    state.tick = totalFromCheckpoint;
                }
            }
            catch { }
            state.initialized = true;
            this._state = state;
        }
        return this._state;
    }
    async record(action, mint, description) {
        if (!this._state)
            throw new Error('State not initialized — call init() first');
        this._state.tick++;
        this._state.actionCounts[action]++;
        this.ticksSinceCheckpoint++;
        if (action === 'launch' && mint) {
            this._state.founded.push(mint);
        }
        if (mint) {
            this.updateSentiment(action, mint);
        }
        if (description) {
            this._state.recentHistory.push(description);
            if (this._state.recentHistory.length > 20) {
                this._state.recentHistory = this._state.recentHistory.slice(-20);
            }
        }
        // Sync P&L from vault every 10 ticks
        if (this._state.tick % 10 === 0) {
            this.syncPnl();
        }
        if (this.checkpointConfig && this.ticksSinceCheckpoint >= this.checkpointConfig.interval) {
            this.ticksSinceCheckpoint = 0;
            this.onCheckpointDue?.();
        }
    }
    updateSentiment(action, mint) {
        if (!this._state)
            return;
        const current = this._state.sentiment.get(mint) ?? 0;
        const SENTIMENT_DELTAS = {
            join: 0.1,
            reinforce: 0.15,
            defect: -0.2,
            rally: 0.3,
            infiltrate: -0.5,
            message: 0.05,
            fud: -0.15,
            war_loan: 0.1,
            launch: 0.3,
        };
        const delta = SENTIMENT_DELTAS[action] ?? 0;
        if (delta !== 0) {
            this._state.sentiment.set(mint, Math.max(-10, Math.min(10, current + delta)));
        }
    }
    onCheckpointDue = null;
    /** Sync totalSolSpent/Received from on-chain vault data (fresh read) */
    async syncPnl() {
        if (!this._state)
            return;
        try {
            const { getVaultForWallet } = await torchsdkImport;
            const vault = await getVaultForWallet(this.connection, this.publicKey);
            if (vault) {
                this._state.totalSolSpent = Math.round(vault.total_spent * 1e9);
                this._state.totalSolReceived = Math.round(vault.total_received * 1e9);
            }
        }
        catch { }
    }
    async getHoldings() {
        const { TOKEN_2022_PROGRAM_ID } = await splTokenImport;
        const walletPk = new web3_js_1.PublicKey(this.publicKey);
        // Parallel scan: wallet + vault
        const stronghold = await this.getStronghold();
        const scanWallet = this.connection
            .getParsedTokenAccountsByOwner(walletPk, { programId: TOKEN_2022_PROGRAM_ID })
            .then((r) => r.value)
            .catch(() => []);
        const scanVault = stronghold
            ? this.connection
                .getParsedTokenAccountsByOwner(new web3_js_1.PublicKey(stronghold.address), {
                programId: TOKEN_2022_PROGRAM_ID,
            })
                .then((r) => r.value)
                .catch(() => [])
            : Promise.resolve([]);
        const [walletValues, vaultValues] = await Promise.all([scanWallet, scanVault]);
        const holdings = new Map();
        for (const a of [...walletValues, ...vaultValues]) {
            const mint = a.account.data.parsed.info.mint;
            const balance = Number(a.account.data.parsed.info.tokenAmount.amount ?? 0);
            if (balance > 0 && (0, vanity_1.isPyreMint)(mint) && !(0, util_1.isBlacklistedMint)(mint)) {
                holdings.set(mint, (holdings.get(mint) ?? 0) + balance);
            }
        }
        return holdings;
    }
    async getBalance(mint) {
        const holdings = await this.getHoldings();
        return holdings.get(mint) ?? 0;
    }
    getSentiment(mint) {
        return this._state?.sentiment.get(mint) ?? 0;
    }
    get sentimentMap() {
        return this._state?.sentiment ?? new Map();
    }
    get history() {
        return this._state?.recentHistory ?? [];
    }
    hasVoted(mint) {
        return this._state?.voted.has(mint) ?? false;
    }
    hasRallied(mint) {
        return this._state?.rallied.has(mint) ?? false;
    }
    markVoted(mint) {
        this._state?.voted.add(mint);
    }
    markRallied(mint) {
        this._state?.rallied.add(mint);
    }
    serialize() {
        return !this._state
            ? {
                publicKey: this.publicKey,
                vaultCreator: null,
                tick: 0,
                actionCounts: { ...EMPTY_COUNTS },
                holdings: {},
                activeLoans: [],
                founded: [],
                rallied: [],
                voted: [],
                sentiment: {},
                recentHistory: [],
                personalitySummary: null,
                totalSolSpent: 0,
                totalSolReceived: 0,
            }
            : {
                publicKey: this._state.publicKey,
                vaultCreator: this._vaultCreator ?? null,
                tick: this._state.tick,
                actionCounts: { ...this._state.actionCounts },
                holdings: {},
                activeLoans: Array.from(this._state.activeLoans),
                founded: [...this._state.founded],
                rallied: Array.from(this._state.rallied),
                voted: Array.from(this._state.voted),
                sentiment: Object.fromEntries(this._state.sentiment),
                recentHistory: this._state.recentHistory.slice(-20),
                personalitySummary: this._state.personalitySummary,
                totalSolSpent: this._state.totalSolSpent,
                totalSolReceived: this._state.totalSolReceived,
            };
    }
    hydrate(saved) {
        if (saved.vaultCreator) {
            this._vaultCreator = saved.vaultCreator;
        }
        this._state = {
            publicKey: saved.publicKey,
            tick: saved.tick,
            actionCounts: { ...EMPTY_COUNTS, ...saved.actionCounts },
            activeLoans: new Set(saved.activeLoans),
            founded: [...saved.founded],
            rallied: new Set(saved.rallied),
            voted: new Set(saved.voted),
            sentiment: new Map(Object.entries(saved.sentiment)),
            recentHistory: [...saved.recentHistory],
            personalitySummary: saved.personalitySummary,
            totalSolSpent: saved.totalSolSpent,
            totalSolReceived: saved.totalSolReceived,
            initialized: true,
        };
    }
}
exports.StateProvider = StateProvider;
