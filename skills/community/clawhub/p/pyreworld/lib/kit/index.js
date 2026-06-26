"use strict";
/**
 * Pyre Kit — Agent-first faction warfare on Torch Market
 *
 * Game-semantic wrapper over torchsdk. Torch Market IS the game engine.
 * This kit translates protocol primitives into faction warfare language
 * so agents think in factions, not tokens.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TOTAL_SUPPLY = exports.TOKEN_MULTIPLIER = exports.LAMPORTS_PER_SOL = exports.PROGRAM_ID = exports.grindPyreMint = exports.isPyreMint = exports.startVaultPnlTracker = exports.getDexVaults = exports.getDexPool = exports.createEphemeralAgent = exports.getBlacklistedMints = exports.isBlacklistedMint = exports.blacklistMints = exports.getAgentWalletLinkPda = exports.getAgentProfilePda = exports.REGISTRY_PROGRAM_ID = exports.RegistryProvider = exports.StateProvider = exports.MapperProvider = exports.IntelProvider = exports.ActionProvider = exports.PyreKit = void 0;
const action_provider_1 = require("./providers/action.provider");
const intel_provider_1 = require("./providers/intel.provider");
const registry_provider_1 = require("./providers/registry.provider");
const state_provider_1 = require("./providers/state.provider");
// ─── Top-level Kit ────────────────────────────────────────────────
class PyreKit {
    connection;
    actions;
    intel;
    registry;
    state;
    constructor(connection, publicKey) {
        this.connection = connection;
        this.registry = new registry_provider_1.RegistryProvider(connection);
        this.state = new state_provider_1.StateProvider(connection, this.registry, publicKey);
        this.actions = new action_provider_1.ActionProvider(connection, this.registry);
        this.intel = new intel_provider_1.IntelProvider(connection, this.actions);
        // Wire auto-checkpoint callback
        this.state.onCheckpointDue = () => this.onCheckpointDue?.();
    }
    /** Callback fired when checkpoint interval is reached */
    onCheckpointDue = null;
    /** Configure auto-checkpoint behavior */
    setCheckpointConfig(config) {
        this.state.setCheckpointConfig(config);
    }
    /**
     * Execute an action with deferred state tracking.
     * On first call, initializes state from chain instead of executing.
     *
     * Returns { result, confirm }. Call confirm() after the transaction
     * is signed and confirmed on-chain. This records the action in state
     * (tick, sentiment, holdings, auto-checkpoint).
     *
     * For read-only methods (getFactions, getComms, etc.), confirm is a no-op.
     */
    async exec(provider, method, ...args) {
        // First exec: initialize state
        if (!this.state.initialized) {
            await this.state.init();
            return { result: null, confirm: async () => { } };
        }
        const target = provider === 'actions' ? this.actions : this.intel;
        const fn = target[method];
        if (typeof fn !== 'function')
            throw new Error(`Unknown method: ${provider}.${String(method)}`);
        const result = await fn.call(target, ...args);
        // Build confirm callback for state-mutating actions
        const trackedAction = provider === 'actions' ? this.methodToAction(method) : null;
        const confirm = trackedAction
            ? async () => {
                const mint = args[0]?.mint;
                const message = args[0]?.message;
                const description = message
                    ? `${trackedAction} ${mint?.slice(0, 8) ?? '?'} — "${message}"`
                    : `${trackedAction} ${mint?.slice(0, 8) ?? '?'}`;
                await this.state.record(trackedAction, mint, description);
            }
            : async () => { }; // no-op for reads
        return { result, confirm };
    }
    /** Map action method names to tracked action types */
    methodToAction(method) {
        const map = {
            join: 'join',
            defect: 'defect',
            rally: 'rally',
            launch: 'launch',
            message: 'message',
            fud: 'fud',
            requestWarLoan: 'war_loan',
            repayWarLoan: 'repay_loan',
            siege: 'siege',
            ascend: 'ascend',
            raze: 'raze',
            tithe: 'tithe',
        };
        return map[method] ?? null;
    }
}
exports.PyreKit = PyreKit;
// ─── Providers ────────────────────────────────────────────────────
var action_provider_2 = require("./providers/action.provider");
Object.defineProperty(exports, "ActionProvider", { enumerable: true, get: function () { return action_provider_2.ActionProvider; } });
var intel_provider_2 = require("./providers/intel.provider");
Object.defineProperty(exports, "IntelProvider", { enumerable: true, get: function () { return intel_provider_2.IntelProvider; } });
var mapper_provider_1 = require("./providers/mapper.provider");
Object.defineProperty(exports, "MapperProvider", { enumerable: true, get: function () { return mapper_provider_1.MapperProvider; } });
var state_provider_2 = require("./providers/state.provider");
Object.defineProperty(exports, "StateProvider", { enumerable: true, get: function () { return state_provider_2.StateProvider; } });
var registry_provider_2 = require("./providers/registry.provider");
Object.defineProperty(exports, "RegistryProvider", { enumerable: true, get: function () { return registry_provider_2.RegistryProvider; } });
Object.defineProperty(exports, "REGISTRY_PROGRAM_ID", { enumerable: true, get: function () { return registry_provider_2.REGISTRY_PROGRAM_ID; } });
Object.defineProperty(exports, "getAgentProfilePda", { enumerable: true, get: function () { return registry_provider_2.getAgentProfilePda; } });
Object.defineProperty(exports, "getAgentWalletLinkPda", { enumerable: true, get: function () { return registry_provider_2.getAgentWalletLinkPda; } });
// ─── Utilities ────────────────────────────────────────────────────
var util_1 = require("./util");
Object.defineProperty(exports, "blacklistMints", { enumerable: true, get: function () { return util_1.blacklistMints; } });
Object.defineProperty(exports, "isBlacklistedMint", { enumerable: true, get: function () { return util_1.isBlacklistedMint; } });
Object.defineProperty(exports, "getBlacklistedMints", { enumerable: true, get: function () { return util_1.getBlacklistedMints; } });
Object.defineProperty(exports, "createEphemeralAgent", { enumerable: true, get: function () { return util_1.createEphemeralAgent; } });
Object.defineProperty(exports, "getDexPool", { enumerable: true, get: function () { return util_1.getDexPool; } });
Object.defineProperty(exports, "getDexVaults", { enumerable: true, get: function () { return util_1.getDexVaults; } });
Object.defineProperty(exports, "startVaultPnlTracker", { enumerable: true, get: function () { return util_1.startVaultPnlTracker; } });
// ─── Vanity ───────────────────────────────────────────────────────
var vanity_1 = require("./vanity");
Object.defineProperty(exports, "isPyreMint", { enumerable: true, get: function () { return vanity_1.isPyreMint; } });
Object.defineProperty(exports, "grindPyreMint", { enumerable: true, get: function () { return vanity_1.grindPyreMint; } });
// ─── Re-export torchsdk constants for convenience ─────────────────
var torchsdk_1 = require("torchsdk");
Object.defineProperty(exports, "PROGRAM_ID", { enumerable: true, get: function () { return torchsdk_1.PROGRAM_ID; } });
Object.defineProperty(exports, "LAMPORTS_PER_SOL", { enumerable: true, get: function () { return torchsdk_1.LAMPORTS_PER_SOL; } });
Object.defineProperty(exports, "TOKEN_MULTIPLIER", { enumerable: true, get: function () { return torchsdk_1.TOKEN_MULTIPLIER; } });
Object.defineProperty(exports, "TOTAL_SUPPLY", { enumerable: true, get: function () { return torchsdk_1.TOTAL_SUPPLY; } });
