"use strict";
/**
 * Pyre Kit Actions
 *
 * Thin wrappers that call torchsdk functions and map params/results
 * into game-semantic Pyre types. No new on-chain logic.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.startVaultPnlTracker = exports.createEphemeralAgent = void 0;
exports.blacklistMints = blacklistMints;
exports.isBlacklistedMint = isBlacklistedMint;
exports.getBlacklistedMints = getBlacklistedMints;
exports.getDexPool = getDexPool;
exports.getDexVaults = getDexVaults;
const web3_js_1 = require("@solana/web3.js");
const program_1 = require("torchsdk/dist/program");
// ─── Blacklist ──────────────────────────────────────────────────────
// Mints from previous swarm runs. Agents should skip these and only
// interact with freshly launched factions.
const DEFAULT_BLACKLIST = [
    // wave 8 (devnet cleanup — all pw suffix factions)
    '3YVQpChWJ9T5CzainxwMNLzKsHy8u8wd7MgjKeeVLRpw',
    '6wnFRhhuU6XeEf8SwtmKy2QUZWYGD7EVwh65pgvDf2pw',
    'DNBgxep1kCnCoqdxKtakfAJ3Mo8guCFCtPHD4Ced5pw',
    'FGdfU9idC5hSBViV3qLTc7k5T2E7kJNWoMW1rwjaZ2pw',
    '9TTsdARLybGb7TZVas35i2wvHUHeLQrYtWnJPWnFwFpw',
    '5XosaZCiDv8YQXAzJo1ubhBFqtM3ZekyDdTAxKazYzpw',
    'CAe4w6FQ7AhrvpMQ6ycaEwGtUxwgaQb35EDktBy4ZGpw',
    '3iJ1verR1yrGFnRMoKoVYhdQ1kMHqfGNKogxxPMpxXpw',
    'c6NHDuVPTjPZPeTof8BdV5sNJxVHyuJyh7dcSa66rpw',
    '2pfU4sDg2f7eGgtPNXh6HG3xEAkB9BoGmME38RWuEMpw',
    '1c4znhcmuLrdKcFUZcJ8J53ZsJvfPcDMyGDisu5gCpw',
    '8SSeiQnTJ9KQgpm7Jq2BGmg2Bn4ArNe6BJuNqKY73bpw',
    'JEStmbXsvpQdS1VjHwKNVqeS3eLFEEC1VuEyg25papw',
    'AumckZMavdsKDZrFPctY5Voe2Cv6A8GQNxZWuxnko2pw',
    'H64NipdSfmvh4CM8pF14qzqTZJbGsgojBVF28XWZ8Upw',
    'J82LYUU4qPCPU1HsWUrtVdyCigg1L5RrDFERQnHHeBpw',
    'HMLtAzEHbmX9gvyLihfaqRJYCG7qq4EHQUGsbS7s6qpw',
    'EtP7XYSRoUJz4ofEARUEn54kSZpubX2G5KhfEZ7rNqpw',
    'EFNHBpgjr4Juu9Z9xfzYVfba9g3P1NQFLkDnZpATPrpw',
    '4nSXyJq1C9U9qNcHYDm4JThs2GHDkmnDqm3jPtGdh2pw',
    'GGBX5tnuA7MNUUtMJTnj7ZTpSkZzeY2UsPikVaF938pw',
    '3givRfqqrHehbBRwwoMSKV3fneN6yG9BJMni5Zr5YBpw',
    'GwtQPPjfkco7ntq3dWZ5VsU29ReusPbNWCE4DGyxzmpw',
    '2XRBi9djXc9xaU86UCfoecLdJdut15SfdBxtc4WMmXpw',
    '5BkD7zSf2WkHBnR1V88Pc5e3DT7NyYgtpVtGWjdKewpw',
    '6LFeAtJ4WF3e4FKu7Ea5iQ8wfNTfbAsfeZdDixySwNpw',
    '4RvArVVtXyMGkT7j97ZiDDkVRvgw3vKt83DfLhsL36pw',
    'AkRQw4cxuZQtsfv8Jc7tt7Nrw15vyCgpaUH6gaYgxopw',
    '9uvnuxJekM7Zww5FBpP2upXiSwWUGSGmnKxHTaTUSpw',
    'FZrKLrjfXKrnCf6qZZAj6zE3nYJrkkrT4hJWghp63gpw',
    'ow7MTQHqbQvvZ5yv1keZH15YqyfwuSaUCojT7khP8pw',
    '7XuCFJ8ZfqNKTN8LWx3s7RKTQD8Xxh4oPySmRjShDApw',
    '5TDDYeLDveD2WGLCtVZ9BmK7f1QYdbmVjVvUjg36Sdpw',
    'Awzh9iPMYyfqqQtFeAmscpFrVwGrx2QZ8JZVYbPtREpw',
    '4FRnFhWy4SCrPDzRRtZpwGQZxGVEcDXD5tYw6Dbmqfpw',
    '9YyLmA4FMuHqR93f3teFxHoWGhRjePLgf43WQ81nbvpw',
    '5JgumB3eim8uEoj17a6i19RPebmYvafJ8vebUVofyDpw',
    '5SjXpXXnqcbaN676ze6kkqk6bvWqZGRdWoP6sufBcRpw',
    'J7cwzF2AZJhmt9WQdnmRqn7qNy3qZx1NuHpuD9TgBWpw',
    '8DfQuT4sevw3jiicWB3voaNfpHvQhaC1xE3qTdTZZGpw',
    'CTNADfuQHJqf5Kovitgv3nrbUhgcK934dLXhT23t1Rpw',
    '6sAhh4FHNpXwW3tcNsQV3ZQ5Fj8SrRReGSS53Pf6SGpw',
    'JBFd9UFY75oXfugxyZUzVr84FLCBVEejUx1BaYBSyQpw',
    'CEs9kGhotgHjxfLL43M9mssPvfzzqdpoECUxqyKfYVpw',
    '3p1Tsiy6kGpXZpKZeJN8EMy7wRfUyMTdwPZdNtRoMepw',
    '9hjHtoKsyP2CrAyrcUdMppy7KgEaJAFNEqbB37JykPpw',
    'CrvcE77chpeBFhFbJPqkaEgRLpZnvGSECqcVLH2h89pw',
    'jbnmVvRnWv9WtfMs7tFfZC3graUyp12zmuac9y4ebpw',
    '2pCKo6SZ35Jpy2WcLCxeF6oijKcvVc5DdsMfZacwUBpw',
    'DzDPetohbp9b8eUK8VhyCwELVMqjRyDtpgxt7vqNSMpw',
    '8uCTJ6mbQa1Bz3GC1i89VJfLUxT6UJqonhHbFhAmz7pw',
    '6NLyzNy9nGshzgZSbF64djH89npZScXpYzNcTMLQ5fpw',
    '2pZsR4ahhkyq2o5pE6CMMA9WmukBabLz3S23pWVMqmpw',
    '7cwpzKf3E6EXoWEVcbTEUUd3DBKc4Zy8nJ19HSZGn4pw',
    '9huQ2WzyshJbFXAYXoXCgFWqNp2hKgvmcUq6VZVRijpw',
    'B9g48Ljaz8gLxZgzTe724xt1moFku2v5CQ8seTH4hApw',
    '3daJ9z51pkbS1Adc93rrFf64WxkDNAxnVaR75GY2ZMpw',
    '3p4G3Ymx1b7n3NSPtfG78ZR1EtNAD92hfsBGknJoRqpw',
    'CmdsKMxes4fvPNx6pN4KuCnJQ55u76muxqNRBQYkEgpw',
    'ArqV3HfakFJ6tBZRfAGtyvGPhosW11rwnrJG8tKFWgpw',
    'HBhiSv1VwfCeqzLiNtiAhQq1LprNUx5aseoMFyP7AWpw',
    '6GwtU2Li5fXjsXkNmBNN5qqNURrvNmfuwLm3VFHx7wpw',
    '5wxmiCWMX3vSA9mKgT4DicqsMs2FmkA1SC4y7P43DVpw',
    '4mwCa28z2PYnWkcQtqbNAek67QbTM9hjUFRXjDZmXopw',
    '2ZSwLE9Hz34oN9nKnwiN51AU4oTFvY3yh91TXjKMqApw',
    '9VhbVcLcGDdiTCq1Kqxy5E2nkFoHGrNUeHB8S1ndCTpw',
    'AvhBaBG944UBqkS5CV4qyb3mPYq95skERiHZVNRwU5pw',
    'C3ZGJjBX9GaY1oXJDHaqeDVPLAzQ8UmANAEybfZrnppw',
    'Ber8fuf1qsKGYJJ44kmnmwF4NmAGHW4bew8A8UpETVpw',
    '8WEk9VbfgsfNb3yHWsvh1sK75qMUejVnZT2rsxXEcqpw',
    'Cdn1zQVeyFLddkcFcCBft1jh6nC149egzNWor45LKipw',
    'y6B1hcduenHtwe5jTWWddkQo45utjszCHsWYjiquvpw',
    '396VE4JMcTM2ERGGhRkMM5YYmZXLkebpyJ51JdPNpDpw',
    'GGp44js46952XQodd2GE3uLi6HpjRY4xaqxkpAvYwtpw',
    'F29SmsUvHYPiEgKJsFmahaKDMAJdkZ2KoDiBiYDZuGpw',
    'CDyXd1yxUNXRwUMBMytKQsH3xadvgBSvnQk9cKETwCpw',
    '3Z4jQxFFJ4a8wR6CFgRG8KCqEhBWPVFQN2fz2KvrzWpw',
    'xrgQK5D5iyyjfLnMWtCQL6rcr61bou9B6q52mpVXipw',
    'Cz4DNBhzUVp3nqe9PgwEQB1qdydkhKu9kE7cBP3S1epw',
    'DKGTjiVXMRCA61eqPGRkSAdThxv1J8EjZmFUpgwbqGpw',
    'CXYcmdbarV8mSHbpAiwZ1EN1hCze6cPTf8RyHW1xx6pw',
    '5CC76QppJqxRWq78hbt6pnkqotfvShEcM79nzAc4VDpw',
];
const BLACKLISTED_MINTS = new Set(DEFAULT_BLACKLIST);
/** Add mints to the blacklist (call at startup with old mints) */
function blacklistMints(mints) {
    for (const m of mints)
        BLACKLISTED_MINTS.add(m);
}
/** Check if a mint is blacklisted */
function isBlacklistedMint(mint) {
    return BLACKLISTED_MINTS.has(mint);
}
/** Get all blacklisted mints */
function getBlacklistedMints() {
    return Array.from(BLACKLISTED_MINTS);
}
/** Create an ephemeral agent keypair (memory-only, zero key management) */
var torchsdk_1 = require("torchsdk");
Object.defineProperty(exports, "createEphemeralAgent", { enumerable: true, get: function () { return torchsdk_1.createEphemeralAgent; } });
/** Get the Raydium pool state PDA for an ascended faction's DEX pool */
function getDexPool(mint) {
    const { poolState } = (0, program_1.getRaydiumMigrationAccounts)(new web3_js_1.PublicKey(mint));
    return poolState;
}
/** Get Raydium pool vault addresses for an ascended faction */
function getDexVaults(mint) {
    const accts = (0, program_1.getRaydiumMigrationAccounts)(new web3_js_1.PublicKey(mint));
    return {
        solVault: (accts.isWsolToken0 ? accts.token0Vault : accts.token1Vault).toString(),
        tokenVault: (accts.isWsolToken0 ? accts.token1Vault : accts.token0Vault).toString(),
    };
}
const startVaultPnlTracker = async (intel, wallet) => {
    const before = await intel.getAgentSolLamports(wallet);
    return {
        async finish() {
            const after = await intel.getAgentSolLamports(wallet);
            const diff = after - before;
            return {
                spent: diff < 0 ? Math.abs(diff) : 0,
                received: diff > 0 ? diff : 0,
            };
        },
    };
};
exports.startVaultPnlTracker = startVaultPnlTracker;
