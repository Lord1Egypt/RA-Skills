import { thetaChainRpc } from '../clients/thetaChainRpc.js';
import { thetaCliRpc } from '../clients/thetaCliRpc.js';
export const wallet = {
    chainAccountGet: (cfg, address) => thetaChainRpc.getAccount(cfg, address),
    chainTxGet: (cfg, hash) => thetaChainRpc.getTransaction(cfg, hash),
    chainBroadcast: (cfg, txBytes, asyncMode = false) => cfg.dryRun ? { dryRun: true } : thetaChainRpc.broadcastRawTransaction(cfg, txBytes, asyncMode),
    keysList: (cfg) => thetaCliRpc.listKeys(cfg),
    keysNew: (cfg, password) => cfg.dryRun ? { dryRun: true } : thetaCliRpc.newKey(cfg, password),
    keysUnlock: (cfg, address, password) => cfg.dryRun ? { dryRun: true } : thetaCliRpc.unlockKey(cfg, address, password)
};
