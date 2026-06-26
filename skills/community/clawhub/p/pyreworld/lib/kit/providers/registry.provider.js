"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.RegistryProvider = exports.getAgentWalletLinkPda = exports.getAgentProfilePda = exports.REGISTRY_PROGRAM_ID = void 0;
const web3_js_1 = require("@solana/web3.js");
const anchor_1 = require("@coral-xyz/anchor");
const pyre_world_json_1 = __importDefault(require("../pyre_world.json"));
exports.REGISTRY_PROGRAM_ID = new web3_js_1.PublicKey(pyre_world_json_1.default.address);
const AGENT_SEED = 'pyre_agent';
const AGENT_WALLET_SEED = 'pyre_agent_wallet';
const getAgentProfilePda = (creator) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(AGENT_SEED), creator.toBuffer()], exports.REGISTRY_PROGRAM_ID);
exports.getAgentProfilePda = getAgentProfilePda;
const getAgentWalletLinkPda = (wallet) => web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(AGENT_WALLET_SEED), wallet.toBuffer()], exports.REGISTRY_PROGRAM_ID);
exports.getAgentWalletLinkPda = getAgentWalletLinkPda;
const makeDummyProvider = (connection, payer) => new anchor_1.AnchorProvider(connection, {
    publicKey: payer,
    signTransaction: async (t) => t,
    signAllTransactions: async (t) => t,
}, {});
async function finalizeTransaction(connection, tx, feePayer) {
    const { blockhash } = await connection.getLatestBlockhash();
    const message = new web3_js_1.TransactionMessage({
        payerKey: feePayer,
        recentBlockhash: blockhash,
        instructions: tx.instructions,
    }).compileToV0Message();
    return new web3_js_1.VersionedTransaction(message);
}
class RegistryProvider {
    connection;
    _programCache = new Map();
    constructor(connection) {
        this.connection = connection;
    }
    getProgram(payer) {
        const key = payer.toBase58();
        let program = this._programCache.get(key);
        if (!program) {
            const provider = makeDummyProvider(this.connection, payer);
            program = new anchor_1.Program(pyre_world_json_1.default, provider);
            this._programCache.set(key, program);
        }
        return program;
    }
    async getProfile(creator) {
        const creatorPk = new web3_js_1.PublicKey(creator);
        const [profilePda] = (0, exports.getAgentProfilePda)(creatorPk);
        const program = this.getProgram(creatorPk);
        try {
            const account = await program.account.agentProfile.fetch(profilePda);
            return {
                address: profilePda.toBase58(),
                creator: account.creator.toBase58(),
                authority: account.authority.toBase58(),
                linked_wallet: account.linkedWallet.toBase58(),
                personality_summary: account.personalitySummary,
                last_checkpoint: account.lastCheckpoint.toNumber(),
                joins: account.joins.toNumber(),
                defects: account.defects.toNumber(),
                rallies: account.rallies.toNumber(),
                launches: account.launches.toNumber(),
                messages: account.messages.toNumber(),
                fuds: account.fuds.toNumber(),
                infiltrates: account.infiltrates.toNumber(),
                reinforces: account.reinforces.toNumber(),
                war_loans: account.warLoans.toNumber(),
                repay_loans: account.repayLoans.toNumber(),
                sieges: account.sieges.toNumber(),
                ascends: account.ascends.toNumber(),
                razes: account.razes.toNumber(),
                tithes: account.tithes.toNumber(),
                created_at: account.createdAt.toNumber(),
                bump: account.bump,
                total_sol_spent: account.totalSolSpent?.toNumber() ?? 0,
                total_sol_received: account.totalSolReceived?.toNumber() ?? 0,
            };
        }
        catch {
            return undefined;
        }
    }
    async getWalletLink(wallet) {
        const walletPk = new web3_js_1.PublicKey(wallet);
        const [linkPda] = (0, exports.getAgentWalletLinkPda)(walletPk);
        const program = this.getProgram(walletPk);
        try {
            const account = await program.account.agentWalletLink.fetch(linkPda);
            return {
                address: linkPda.toBase58(),
                profile: account.profile.toBase58(),
                wallet: account.wallet.toBase58(),
                linked_at: account.linkedAt.toNumber(),
                bump: account.bump,
            };
        }
        catch {
            return undefined;
        }
    }
    async register(params) {
        const creator = new web3_js_1.PublicKey(params.creator);
        const [profile] = (0, exports.getAgentProfilePda)(creator);
        const [walletLink] = (0, exports.getAgentWalletLinkPda)(creator);
        const program = this.getProgram(creator);
        const tx = new web3_js_1.Transaction();
        const ix = await program.methods.register()
            .accounts({ creator, profile, walletLink, systemProgram: web3_js_1.SystemProgram.programId })
            .instruction();
        tx.add(ix);
        const versionedTx = await finalizeTransaction(this.connection, tx, creator);
        return {
            transaction: versionedTx,
            message: `Register agent profile [${profile.toBase58()}]`,
        };
    }
    async checkpoint(params) {
        const signer = new web3_js_1.PublicKey(params.signer);
        const creatorPk = new web3_js_1.PublicKey(params.creator);
        const [profile] = (0, exports.getAgentProfilePda)(creatorPk);
        const program = this.getProgram(signer);
        const args = {
            joins: new anchor_1.BN(params.joins),
            defects: new anchor_1.BN(params.defects),
            rallies: new anchor_1.BN(params.rallies),
            launches: new anchor_1.BN(params.launches),
            messages: new anchor_1.BN(params.messages),
            fuds: new anchor_1.BN(params.fuds),
            infiltrates: new anchor_1.BN(params.infiltrates),
            reinforces: new anchor_1.BN(params.reinforces),
            warLoans: new anchor_1.BN(params.war_loans),
            repayLoans: new anchor_1.BN(params.repay_loans),
            sieges: new anchor_1.BN(params.sieges),
            ascends: new anchor_1.BN(params.ascends),
            razes: new anchor_1.BN(params.razes),
            tithes: new anchor_1.BN(params.tithes),
            personalitySummary: params.personality_summary,
            totalSolSpent: new anchor_1.BN(params.total_sol_spent),
            totalSolReceived: new anchor_1.BN(params.total_sol_received),
        };
        const tx = new web3_js_1.Transaction();
        const ix = await program.methods.checkpoint(args)
            .accounts({ signer, profile, systemProgram: web3_js_1.SystemProgram.programId })
            .instruction();
        tx.add(ix);
        const versionedTx = await finalizeTransaction(this.connection, tx, signer);
        return {
            transaction: versionedTx,
            message: `Checkpoint agent [${profile.toBase58()}]`,
        };
    }
    async linkWallet(params) {
        const authority = new web3_js_1.PublicKey(params.authority);
        const creatorPk = new web3_js_1.PublicKey(params.creator);
        const walletToLink = new web3_js_1.PublicKey(params.wallet_to_link);
        const [profile] = (0, exports.getAgentProfilePda)(creatorPk);
        const [walletLink] = (0, exports.getAgentWalletLinkPda)(walletToLink);
        const program = this.getProgram(authority);
        const tx = new web3_js_1.Transaction();
        const ix = await program.methods.linkWallet()
            .accounts({
            authority,
            profile,
            walletToLink,
            walletLink,
            systemProgram: web3_js_1.SystemProgram.programId,
        })
            .instruction();
        tx.add(ix);
        const versionedTx = await finalizeTransaction(this.connection, tx, authority);
        return {
            transaction: versionedTx,
            message: `Link wallet ${walletToLink.toBase58()} to agent [${profile.toBase58()}]`,
        };
    }
    async unlinkWallet(params) {
        const authority = new web3_js_1.PublicKey(params.authority);
        const creatorPk = new web3_js_1.PublicKey(params.creator);
        const walletToUnlink = new web3_js_1.PublicKey(params.wallet_to_unlink);
        const [profile] = (0, exports.getAgentProfilePda)(creatorPk);
        const [walletLink] = (0, exports.getAgentWalletLinkPda)(walletToUnlink);
        const program = this.getProgram(authority);
        const tx = new web3_js_1.Transaction();
        const ix = await program.methods.unlinkWallet()
            .accounts({
            authority,
            profile,
            walletToUnlink,
            walletLink,
            systemProgram: web3_js_1.SystemProgram.programId,
        })
            .instruction();
        tx.add(ix);
        const versionedTx = await finalizeTransaction(this.connection, tx, authority);
        return {
            transaction: versionedTx,
            message: `Unlink wallet ${walletToUnlink.toBase58()} from agent [${profile.toBase58()}]`,
        };
    }
    async transferAuthority(params) {
        const authority = new web3_js_1.PublicKey(params.authority);
        const creatorPk = new web3_js_1.PublicKey(params.creator);
        const newAuthority = new web3_js_1.PublicKey(params.new_authority);
        const [profile] = (0, exports.getAgentProfilePda)(creatorPk);
        const program = this.getProgram(authority);
        const tx = new web3_js_1.Transaction();
        const ix = await program.methods.transferAuthority()
            .accounts({ authority, profile, newAuthority })
            .instruction();
        tx.add(ix);
        const versionedTx = await finalizeTransaction(this.connection, tx, authority);
        return {
            transaction: versionedTx,
            message: `Transfer agent authority to ${newAuthority.toBase58()}`,
        };
    }
}
exports.RegistryProvider = RegistryProvider;
