/**
 * Boot-time chain-gate predicate for client-side `executeBatch` UserOp
 * submission. Spec #281 §9 Phase 1 (item imp-16).
 *
 * The default behaviour is chain-aware: Pro tier (Gnosis, chain 100) batches
 * via `executeBatch`; Free tier (Base Sepolia, chain 84532) submits one
 * UserOp per fact. The `TOTALRECLAW_GNOSIS_BATCH_ENABLED` env var is a
 * hard kill-switch — setting it to `false` disables batching on every chain
 * regardless of tier, so ops can revert to single-fact submission without a
 * client redeploy if T-7 surfaces a billing regression.
 *
 * Read at boot only (module-load time). Per-write reads would re-parse the
 * env on every submission — too expensive for the auto-extraction hot path
 * and pointless because the env doesn't change mid-process.
 *
 * Sibling work-leaves wire `shouldBatchOnChain` into `submitFactBatchOnChain`
 * (TS) and `agent/lifecycle.py` (Python mirror in `batch_gate.py`); this
 * module ships the primitive only.
 */
const GNOSIS_CHAIN_ID = 100;
const BATCH_ENABLED_AT_BOOT = (process.env.TOTALRECLAW_GNOSIS_BATCH_ENABLED ?? '').toLowerCase() !== 'false';
export function shouldBatchOnChain(chainId) {
    if (!BATCH_ENABLED_AT_BOOT)
        return false;
    return chainId === GNOSIS_CHAIN_ID;
}
export const __testing = {
    readGateForTests(env, chainId) {
        const enabled = (env.TOTALRECLAW_GNOSIS_BATCH_ENABLED ?? '').toLowerCase() !== 'false';
        if (!enabled)
            return false;
        return chainId === GNOSIS_CHAIN_ID;
    },
};
