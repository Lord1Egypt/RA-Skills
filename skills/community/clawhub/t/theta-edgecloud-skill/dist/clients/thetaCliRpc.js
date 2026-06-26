import { postJson } from './http.js';
function rpc(cfg, method, params = {}) {
    if (!cfg.cliRpcUrl)
        throw new Error('THETA_CLI_RPC_URL missing');
    return postJson(cfg.cliRpcUrl, { jsonrpc: '2.0', id: Date.now(), method, params }, {
        service: 'theta-cli-rpc',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    });
}
export const thetaCliRpc = {
    listKeys: (cfg) => rpc(cfg, 'thetacli.ListKeys'),
    newKey: (cfg, password) => rpc(cfg, 'thetacli.NewKey', { password }),
    unlockKey: (cfg, address, password) => rpc(cfg, 'thetacli.UnlockKey', { address, password })
};
