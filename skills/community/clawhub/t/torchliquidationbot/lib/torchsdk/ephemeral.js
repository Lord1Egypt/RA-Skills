"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createEphemeralAgent = void 0;
/*
 * Ephemeral Agent Keypair
 *
 * generates an in-process keypair that lives only in memory.
 * the authority links this wallet to their vault, and the SDK uses it to sign transactions.
 * when the process stops, the private key is lost — zero key management, zero risk.
 * flow:
 *   1. const agent = createEphemeralAgent()
 *   2. Authority calls buildLinkWalletTransaction({ wallet_to_link: agent.publicKey })
 *   3. SDK uses agent.sign(tx) for all vault operations
 *   4. On shutdown, keys are GC'd. Authority unlinks the wallet.
 */
const web3_js_1 = require("@solana/web3.js");
// create an ephemeral agent keypair.
// the keypair exists only in memory. No file is written to disk.
// when the process exits, the private key is permanently lost.
const createEphemeralAgent = () => {
    const keypair = web3_js_1.Keypair.generate();
    return {
        publicKey: keypair.publicKey.toBase58(),
        keypair,
        sign: (tx) => {
            if (tx instanceof web3_js_1.VersionedTransaction) {
                tx.sign([keypair]);
            }
            else {
                tx.partialSign(keypair);
            }
            return tx;
        },
    };
};
exports.createEphemeralAgent = createEphemeralAgent;
//# sourceMappingURL=ephemeral.js.map