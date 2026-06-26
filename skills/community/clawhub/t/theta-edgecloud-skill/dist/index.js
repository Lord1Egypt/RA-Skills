import { loadConfig } from './config.js';
import { deployments } from './commands/deployments.js';
import { inference } from './commands/inference.js';
import { video } from './commands/video.js';
import { ondemand } from './commands/ondemand.js';
import { healthCheck } from './commands/health.js';
import { executeThetaRuntimeCommand, listThetaRuntimeCommands, thetaRuntimeCommandSchemas } from './runtime/handlers.js';
import { resolveThetaOnDemandToken } from './runtime/secretResolver.js';
export function theta() {
    const cfg = loadConfig();
    return {
        cfg,
        deploy: deployments,
        inference,
        video,
        ondemand,
        healthCheck: () => healthCheck(cfg)
    };
}
export { executeThetaRuntimeCommand, listThetaRuntimeCommands, thetaRuntimeCommandSchemas, resolveThetaOnDemandToken };
