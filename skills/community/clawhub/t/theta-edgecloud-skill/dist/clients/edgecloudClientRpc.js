import { postJson } from './http.js';
function rpc(cfg, method, params = {}) {
    if (!cfg.edgecloudRpcUrl)
        throw new Error('THETA_EDGECLOUD_RPC_URL missing');
    return postJson(cfg.edgecloudRpcUrl, { jsonrpc: '2.0', id: Date.now(), method, params }, {
        service: 'edgecloud-client-rpc',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    });
}
export const edgecloudClientRpc = {
    status: (cfg) => rpc(cfg, 'edgecloud.GetStatus'),
    setPrice: (cfg, priceHr) => rpc(cfg, 'edgecloud.SetPrice', { price_hr: priceHr }),
    deployments: (cfg, params) => rpc(cfg, 'edgecloud.GetDeployments', params),
    jobs: (cfg, params) => rpc(cfg, 'edgecloud.GetJobs', params),
    rewards: (cfg, params) => rpc(cfg, 'edgecloud.GetRewards', params)
};
