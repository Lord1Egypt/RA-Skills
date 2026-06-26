import { loadConfig } from '../config.js';
import { deployments } from '../commands/deployments.js';
import { healthCheck } from '../commands/health.js';
import { inference } from '../commands/inference.js';
import { ondemand } from '../commands/ondemand.js';
import { video } from '../commands/video.js';
import { resolveThetaOnDemandToken } from './secretResolver.js';
function coerceBool(value, fallback) {
    if (value === undefined)
        return fallback;
    const normalized = value.trim().toLowerCase();
    if (['1', 'true', 'yes', 'on'].includes(normalized))
        return true;
    if (['0', 'false', 'no', 'off'].includes(normalized))
        return false;
    return fallback;
}
function coerceInt(value, fallback, min, max) {
    if (!value)
        return fallback;
    const parsed = Number.parseInt(value, 10);
    if (!Number.isFinite(parsed))
        return fallback;
    return Math.min(Math.max(parsed, min), max);
}
async function buildRuntimeConfig(ctx) {
    const base = loadConfig();
    const env = ctx.env ?? {};
    const onDemandApiToken = await resolveThetaOnDemandToken(ctx, base.onDemandApiToken);
    const inferenceAuthUser = env.THETA_INFERENCE_AUTH_USER ?? base.inferenceAuth?.user;
    const inferenceAuthPass = env.THETA_INFERENCE_AUTH_PASS ?? base.inferenceAuth?.pass;
    return {
        ...base,
        dryRun: coerceBool(env.THETA_DRY_RUN, base.dryRun),
        edgecloudApiKey: env.THETA_EC_API_KEY ?? base.edgecloudApiKey,
        edgecloudProjectId: env.THETA_EC_PROJECT_ID ?? base.edgecloudProjectId,
        edgecloudOrgId: env.THETA_ORG_ID ?? base.edgecloudOrgId,
        videoSaId: env.THETA_VIDEO_SA_ID ?? base.videoSaId,
        videoSaSecret: env.THETA_VIDEO_SA_SECRET ?? base.videoSaSecret,
        inferenceEndpoint: env.THETA_INFERENCE_ENDPOINT ?? base.inferenceEndpoint,
        inferenceAuth: inferenceAuthUser && inferenceAuthPass
            ? { user: inferenceAuthUser, pass: inferenceAuthPass }
            : base.inferenceAuth,
        onDemandApiToken,
        onDemandApiBaseUrl: env.THETA_ONDEMAND_API_BASE_URL ?? env.THETA_API_BASE_URL ?? base.onDemandApiBaseUrl,
        edgecloudRpcUrl: env.THETA_EDGECLOUD_RPC_URL ?? base.edgecloudRpcUrl,
        chainRpcUrl: env.THETA_CHAIN_RPC_URL ?? base.chainRpcUrl,
        cliRpcUrl: env.THETA_CLI_RPC_URL ?? base.cliRpcUrl,
        httpTimeoutMs: coerceInt(env.THETA_HTTP_TIMEOUT_MS, base.httpTimeoutMs, 1000, 120000),
        httpMaxRetries: coerceInt(env.THETA_HTTP_MAX_RETRIES, base.httpMaxRetries, 0, 6),
        httpRetryBackoffMs: coerceInt(env.THETA_HTTP_RETRY_BACKOFF_MS, base.httpRetryBackoffMs, 25, 10000)
    };
}
function requireFields(args, fields) {
    for (const field of fields) {
        if (!(field in args) || args[field] === undefined || args[field] === null || args[field] === '') {
            throw new Error(`Missing required field: ${field}`);
        }
    }
}
function requireObject(value, field) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) {
        throw new Error(`${field} must be an object`);
    }
    return value;
}
function requireText(value, field) {
    if (value === undefined || value === null || String(value).trim() === '') {
        throw new Error(`Missing required field: ${field}`);
    }
    return String(value).trim();
}
function resolveInputFields(args) {
    if (Array.isArray(args.input_fields))
        return args.input_fields.map((field) => requireText(field, 'input_fields[]'));
    if (Array.isArray(args.inputFields))
        return args.inputFields.map((field) => requireText(field, 'inputFields[]'));
    const single = args.input_field ?? args.inputField;
    if (single !== undefined && single !== null && String(single).trim() !== '')
        return [requireText(single, 'input_field')];
    return undefined;
}
function resolveProjectId(cfg, args) {
    return requireText(args.projectId ?? cfg.edgecloudProjectId, 'projectId');
}
const commandRegistry = {
    'theta.health': {
        schema: { command: 'theta.health', description: 'EdgeCloud health check via controller VM listing', required: [] },
        handler: (cfg) => healthCheck(cfg)
    },
    'theta.inference.models': {
        schema: { command: 'theta.inference.models', description: 'List models from dedicated inference endpoint', required: [] },
        handler: (cfg, args) => {
            if (args.endpoint !== undefined && String(args.endpoint).trim() !== '') {
                throw new Error('args.endpoint override is disabled for security. Set THETA_INFERENCE_ENDPOINT instead.');
            }
            return inference.models(cfg);
        }
    },
    'theta.inference.chat': {
        schema: { command: 'theta.inference.chat', description: 'Run chat completion on dedicated inference endpoint', required: ['body'] },
        handler: (cfg, args) => {
            if (args.endpoint !== undefined && String(args.endpoint).trim() !== '') {
                throw new Error('args.endpoint override is disabled for security. Set THETA_INFERENCE_ENDPOINT instead.');
            }
            return inference.chat(cfg, args.body);
        }
    },
    'theta.inference.ready': {
        schema: { command: 'theta.inference.ready', description: 'Poll dedicated inference endpoint readiness with openai or gradio probe', required: [] },
        handler: (cfg, args) => inference.ready(cfg, {
            probe: args.probe,
            timeoutMs: args.timeoutMs,
            intervalMs: args.intervalMs
        })
    },
    'theta.ondemand.listServices': {
        schema: { command: 'theta.ondemand.listServices', description: 'List live on-demand services with catalog fallback', required: [] },
        handler: (cfg, args) => ondemand.listLiveServices(cfg, { category: args.category })
    },
    'list_services': {
        schema: { command: 'list_services', description: 'MCP-compatible alias: list available Theta on-demand services', required: [] },
        handler: (cfg, args) => ondemand.listLiveServices(cfg, { category: args.category })
    },
    'theta.ondemand.infer': {
        schema: { command: 'theta.ondemand.infer', description: 'Create on-demand infer request', required: ['service', 'payload'] },
        handler: (cfg, args) => ondemand.infer(cfg, args.service, args.payload, args.options)
    },
    'infer': {
        schema: { command: 'infer', description: 'MCP-compatible alias: create on-demand infer request', required: ['service'] },
        handler: (cfg, args) => ondemand.infer(cfg, requireText(args.service, 'service'), (args.payload ?? {
            input: args.input ?? {},
            ...(args.variant ? { variant: args.variant } : {}),
            ...(args.webhook ? { webhook: args.webhook } : {})
        }), {
            wait: args.wait,
            prediction: args.prediction
        })
    },
    'theta.ondemand.chat': {
        schema: { command: 'theta.ondemand.chat', description: 'Run chat-style on-demand inference; defaults to Qwen3', required: ['messages'] },
        handler: (cfg, args) => ondemand.chat(cfg, args.service ?? 'qwen3', args.messages, {
            maxTokens: args.max_tokens,
            temperature: args.temperature,
            topP: args.top_p,
            stream: args.stream,
            wait: args.wait,
            prediction: args.prediction,
            variant: args.variant,
            webhook: args.webhook,
            reasoningEffort: args.reasoning_effort,
            extraInput: args.extraInput,
            allowUnknownService: args.allowUnknownService
        })
    },
    'theta.ondemand.status': {
        schema: { command: 'theta.ondemand.status', description: 'Get on-demand infer request status', required: ['requestId'] },
        handler: (cfg, args) => ondemand.status(cfg, args.requestId)
    },
    'get_request_status': {
        schema: { command: 'get_request_status', description: 'MCP-compatible alias: get on-demand infer request status', required: [] },
        handler: (cfg, args) => ondemand.status(cfg, requireText(args.request_id ?? args.requestId, 'request_id'))
    },
    'theta.ondemand.inputPresignedUrls': {
        schema: { command: 'theta.ondemand.inputPresignedUrls', description: 'Create presigned URLs for on-demand inputs', required: ['service'] },
        handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, args.service, resolveInputFields(args))
    },
    'get_upload_url': {
        schema: { command: 'get_upload_url', description: 'MCP-compatible alias: create presigned URLs for on-demand inputs', required: ['service'] },
        handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, requireText(args.service, 'service'), resolveInputFields(args))
    },
    'theta.ondemand.pollUntilDone': {
        schema: { command: 'theta.ondemand.pollUntilDone', description: 'Poll on-demand request until terminal state', required: ['requestId'] },
        handler: (cfg, args) => ondemand.pollUntilDone(cfg, args.requestId, args.options)
    },
    'theta.deployments.list': {
        schema: { command: 'theta.deployments.list', description: 'List deployments for project', required: ['projectId'] },
        handler: (cfg, args) => deployments.list(cfg, args.projectId)
    },
    'theta.deployments.routeProbe': {
        schema: { command: 'theta.deployments.routeProbe', description: 'Probe singular/plural deployment list routes for project', required: [] },
        handler: (cfg, args) => deployments.routeProbe(cfg, resolveProjectId(cfg, args))
    },
    'theta.deployments.create': {
        schema: { command: 'theta.deployments.create', description: 'Create deployment from payload', required: ['payload'] },
        handler: (cfg, args) => deployments.create(cfg, { ...requireObject(args.payload, 'payload'), project_id: resolveProjectId(cfg, args) })
    },
    'theta.deployments.start': {
        schema: { command: 'theta.deployments.start', description: 'Start deployment by shard/suffix with route fallback', required: ['shard', 'suffix'] },
        handler: (cfg, args) => deployments.start(cfg, resolveProjectId(cfg, args), requireText(args.shard, 'shard'), requireText(args.suffix, 'suffix'))
    },
    'theta.deployments.stop': {
        schema: { command: 'theta.deployments.stop', description: 'Stop deployment by shard/suffix with route fallback', required: ['shard', 'suffix'] },
        handler: (cfg, args) => deployments.stop(cfg, resolveProjectId(cfg, args), requireText(args.shard, 'shard'), requireText(args.suffix, 'suffix'))
    },
    'theta.deployments.delete': {
        schema: { command: 'theta.deployments.delete', description: 'Delete deployment by shard/suffix with route fallback', required: ['shard', 'suffix'] },
        handler: (cfg, args) => deployments.delete(cfg, resolveProjectId(cfg, args), requireText(args.shard, 'shard'), requireText(args.suffix, 'suffix'))
    },
    'theta.deployments.validateDisposable': {
        schema: { command: 'theta.deployments.validateDisposable', description: 'Create, probe, smoke, delete, and report balance delta for one disposable deployment', required: ['payload'] },
        handler: (cfg, args) => deployments.validateDisposable(cfg, {
            payload: requireObject(args.payload, 'payload'),
            projectId: args.projectId,
            orgId: args.orgId,
            probe: args.probe,
            readyTimeoutMs: args.readyTimeoutMs,
            intervalMs: args.intervalMs,
            smokeMessage: args.smokeMessage,
            model: args.model
        })
    },
    'theta.billing.balance': {
        schema: { command: 'theta.billing.balance', description: 'Read Theta org balance', required: [] },
        handler: (cfg, args) => deployments.balance(cfg, args.orgId)
    },
    'theta.billing.balanceSnapshot': {
        schema: { command: 'theta.billing.balanceSnapshot', description: 'Read Theta org balance and extract numeric value when possible', required: [] },
        handler: (cfg, args) => deployments.balanceSnapshot(cfg, args.orgId)
    },
    'theta.ai.agent.create': {
        schema: { command: 'theta.ai.agent.create', description: 'Create Theta EdgeCloud AI Agent/RAG chatbot', required: ['payload'] },
        handler: (cfg, args) => deployments.chatbotCreate(cfg, { ...requireObject(args.payload, 'payload'), project_id: resolveProjectId(cfg, args) })
    },
    'theta.ai.agent.get': {
        schema: { command: 'theta.ai.agent.get', description: 'Fetch Theta EdgeCloud AI Agent/RAG chatbot details', required: ['chatbotId'] },
        handler: (cfg, args) => deployments.chatbotGet(cfg, requireText(args.chatbotId, 'chatbotId'), resolveProjectId(cfg, args))
    },
    'theta.ai.agent.update': {
        schema: { command: 'theta.ai.agent.update', description: 'Update Theta EdgeCloud AI Agent/RAG chatbot settings', required: ['chatbotId', 'payload'] },
        handler: (cfg, args) => deployments.chatbotUpdate(cfg, requireText(args.chatbotId, 'chatbotId'), { ...requireObject(args.payload, 'payload'), project_id: resolveProjectId(cfg, args) })
    },
    'theta.ai.agent.list': {
        schema: { command: 'theta.ai.agent.list', description: 'List Theta EdgeCloud AI Agent/RAG chatbots', required: [] },
        handler: (cfg, args) => deployments.chatbotList(cfg, resolveProjectId(cfg, args), args.page, args.number)
    },
    'theta.ai.agent.document.create': {
        schema: { command: 'theta.ai.agent.document.create', description: 'Create AI Agent knowledge-base document from provided content', required: ['chatbotId', 'file'] },
        handler: (cfg, args) => deployments.chatbotDocumentCreate(cfg, requireText(args.chatbotId, 'chatbotId'), resolveProjectId(cfg, args), requireObject(args.file, 'file'), args.metadata)
    },
    'theta.ai.agent.document.update': {
        schema: { command: 'theta.ai.agent.document.update', description: 'Update AI Agent knowledge-base document from provided content', required: ['chatbotId', 'documentId', 'file'] },
        handler: (cfg, args) => deployments.chatbotDocumentUpdate(cfg, requireText(args.chatbotId, 'chatbotId'), requireText(args.documentId, 'documentId'), resolveProjectId(cfg, args), requireObject(args.file, 'file'), args.metadata)
    },
    'theta.ai.agent.document.get': {
        schema: { command: 'theta.ai.agent.document.get', description: 'Fetch AI Agent knowledge-base document', required: ['chatbotId', 'documentId'] },
        handler: (cfg, args) => deployments.chatbotDocumentGet(cfg, requireText(args.chatbotId, 'chatbotId'), requireText(args.documentId, 'documentId'))
    },
    'theta.ai.agent.document.list': {
        schema: { command: 'theta.ai.agent.document.list', description: 'List AI Agent knowledge-base documents', required: ['chatbotId'] },
        handler: (cfg, args) => deployments.chatbotDocumentList(cfg, requireText(args.chatbotId, 'chatbotId'), resolveProjectId(cfg, args), args.page, args.number)
    },
    'theta.deployments.listVm': {
        schema: { command: 'theta.deployments.listVm', description: 'List EdgeCloud VM types', required: [] },
        handler: (cfg) => deployments.listVm(cfg)
    },
    'theta.video.list': {
        schema: { command: 'theta.video.list', description: 'List videos for service account', required: ['serviceAccountId'] },
        handler: (cfg, args) => video.videoList(cfg, args.serviceAccountId, args.page ?? 1, args.number ?? 10)
    },
};
const onDemandTokenCommands = new Set([
    'theta.ondemand.infer',
    'theta.ondemand.chat',
    'theta.ondemand.status',
    'theta.ondemand.inputPresignedUrls',
    'theta.ondemand.pollUntilDone',
    'infer',
    'get_request_status',
    'get_upload_url'
]);
export const thetaRuntimeCommandSchemas = Object.fromEntries(Object.entries(commandRegistry).map(([cmd, reg]) => [cmd, reg.schema]));
export function listThetaRuntimeCommands() {
    return Object.keys(commandRegistry).sort();
}
export async function executeThetaRuntimeCommand(args, ctx = {}) {
    const registration = commandRegistry[args.command];
    if (!registration) {
        throw new Error(`Unsupported theta runtime command: ${args.command}`);
    }
    requireFields(args, registration.schema.required);
    const cfg = await buildRuntimeConfig(ctx);
    if (onDemandTokenCommands.has(args.command) && !cfg.dryRun && !cfg.onDemandApiToken) {
        throw new Error('THETA_ONDEMAND_API_TOKEN missing (runtime secret/env resolver)');
    }
    return registration.handler(cfg, args);
}
