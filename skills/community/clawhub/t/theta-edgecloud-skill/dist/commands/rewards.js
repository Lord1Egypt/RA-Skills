import { edgecloudClientRpc } from '../clients/edgecloudClientRpc.js';
export const rewards = {
    edgeStatus: (cfg) => edgecloudClientRpc.status(cfg),
    setPrice: (cfg, priceHr) => cfg.dryRun ? { dryRun: true, priceHr } : edgecloudClientRpc.setPrice(cfg, priceHr),
    deployments: (cfg, params) => edgecloudClientRpc.deployments(cfg, params),
    jobs: (cfg, params) => edgecloudClientRpc.jobs(cfg, params),
    rewards: (cfg, params) => edgecloudClientRpc.rewards(cfg, params)
};
