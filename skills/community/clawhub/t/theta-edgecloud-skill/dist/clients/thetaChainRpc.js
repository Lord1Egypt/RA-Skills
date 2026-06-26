import { postJson } from './http.js';
function rpc(cfg, method, params = {}) {
    if (!cfg.chainRpcUrl)
        throw new Error('THETA_CHAIN_RPC_URL missing');
    return postJson(cfg.chainRpcUrl, { jsonrpc: '2.0', id: Date.now(), method, params }, {
        service: 'theta-chain-rpc',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    });
}
export const thetaChainRpc = {
    getVersion: (cfg) => rpc(cfg, 'theta.GetVersion'),
    getAccount: (cfg, address) => rpc(cfg, 'theta.GetAccount', { address }),
    getTransaction: (cfg, hash) => rpc(cfg, 'theta.GetTransaction', { hash }),
    broadcastRawTransaction: (cfg, tx_bytes, asyncMode = false) => rpc(cfg, asyncMode ? 'theta.BroadcastRawTransactionAsync' : 'theta.BroadcastRawTransaction', { tx_bytes })
};
