import { loadConfig, ThetaConfig } from '../config.js';
import { deployments } from '../commands/deployments.js';
import { healthCheck } from '../commands/health.js';
import { inference } from '../commands/inference.js';
import { ondemand } from '../commands/ondemand.js';
import { video } from '../commands/video.js';
import { billing, gpu } from '../commands/gpu.js';
import { characterRoutes, characterRequest } from '../commands/characters.js';
import { redactObject } from '../redaction.js';
import { sanitizeHttpErrorMessage } from '../errors.js';
import {
  resolveThetaOnDemandToken,
  type ThetaSecretResolverContext
} from './secretResolver.js';

export type ThetaRuntimeContext = ThetaSecretResolverContext;

export type ThetaRuntimeCommandArgs = {
  command: string;
  [key: string]: unknown;
};

export type ThetaCommandSchema = {
  command: string;
  description: string;
  required: string[];
};

type CommandRegistration = {
  schema: ThetaCommandSchema;
  handler: (cfg: ThetaConfig, args: ThetaRuntimeCommandArgs) => Promise<unknown> | unknown;
};

function coerceBool(value: string | undefined, fallback: boolean): boolean {
  if (value === undefined) return fallback;
  const normalized = value.trim().toLowerCase();
  if (['1', 'true', 'yes', 'on'].includes(normalized)) return true;
  if (['0', 'false', 'no', 'off'].includes(normalized)) return false;
  return fallback;
}

function coerceInt(value: string | undefined, fallback: number, min: number, max: number): number {
  if (!value) return fallback;
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed)) return fallback;
  return Math.min(Math.max(parsed, min), max);
}

const CALLER_ENV_KEYS = [
  'THETA_DRY_RUN', 'THETA_EC_API_KEY', 'THETA_EC_PROJECT_ID', 'THETA_ORG_ID', 'THETA_VIDEO_SA_ID',
  'THETA_VIDEO_SA_SECRET', 'THETA_CHARACTERS_API_KEY', 'THETA_INFERENCE_ENDPOINT', 'THETA_INFERENCE_AUTH_USER',
  'THETA_INFERENCE_AUTH_PASS', 'THETA_ONDEMAND_API_TOKEN', 'THETA_ONDEMAND_API_KEY', 'THETA_API_KEY',
  'THETA_ONDEMAND_API_BASE_URL', 'THETA_API_BASE_URL', 'THETA_HTTP_TIMEOUT_MS', 'THETA_HTTP_MAX_RETRIES',
  'THETA_HTTP_RETRY_BACKOFF_MS'
] as const;

// Each caller-supplied field is read exactly once and kept as a plain string, so a getter or proxy
// cannot return one value to the checks below and another to the request.
function snapshotCallerEnv(env: unknown): Record<string, string | undefined> {
  const out: Record<string, string | undefined> = {};
  if (!env || typeof env !== 'object') return out;
  for (const key of CALLER_ENV_KEYS) {
    const value = (env as Record<string, unknown>)[key];
    if (typeof value === 'string') out[key] = value;
  }
  return Object.freeze(out);
}

async function buildRuntimeConfig(ctx: ThetaRuntimeContext): Promise<ThetaConfig> {
  const base = loadConfig();
  const callerEnv = snapshotCallerEnv(ctx.env);

  const onDemandApiToken = await resolveThetaOnDemandToken({ env: callerEnv, getSecret: ctx.getSecret }, base.onDemandApiToken);
  if (callerEnv.THETA_INFERENCE_ENDPOINT && base.inferenceEndpoint &&
      new URL(callerEnv.THETA_INFERENCE_ENDPOINT.trim()).origin !== new URL(base.inferenceEndpoint.trim()).origin) {
    throw new Error('Request-level THETA_INFERENCE_ENDPOINT override is disabled; configure the operator endpoint instead');
  }
  const sameInferenceOrigin = !callerEnv.THETA_INFERENCE_ENDPOINT ||
    (base.inferenceEndpoint && new URL(callerEnv.THETA_INFERENCE_ENDPOINT.trim()).origin === new URL(base.inferenceEndpoint.trim()).origin);
  const inferenceAuthUser = callerEnv.THETA_INFERENCE_AUTH_USER ?? (sameInferenceOrigin ? base.inferenceAuth?.user : undefined);
  const inferenceAuthPass = callerEnv.THETA_INFERENCE_AUTH_PASS ?? (sameInferenceOrigin ? base.inferenceAuth?.pass : undefined);

  return {
    ...base,
    // A caller-supplied ctx.env can turn dry-run ON but never OFF an operator-enabled dry-run.
    dryRun: base.dryRun || coerceBool(callerEnv.THETA_DRY_RUN, false),
    edgecloudApiKey: callerEnv.THETA_EC_API_KEY ?? base.edgecloudApiKey,
    edgecloudProjectId: callerEnv.THETA_EC_PROJECT_ID ?? base.edgecloudProjectId,
    edgecloudOrgId: callerEnv.THETA_ORG_ID ?? base.edgecloudOrgId,
    videoSaId: callerEnv.THETA_VIDEO_SA_ID ?? base.videoSaId,
    videoSaSecret: callerEnv.THETA_VIDEO_SA_SECRET ?? base.videoSaSecret,
    charactersApiKey: callerEnv.THETA_CHARACTERS_API_KEY ?? base.charactersApiKey,
    inferenceEndpoint: callerEnv.THETA_INFERENCE_ENDPOINT ?? base.inferenceEndpoint,
    inferenceAuth: inferenceAuthUser && inferenceAuthPass ? { user: inferenceAuthUser, pass: inferenceAuthPass } : undefined,
    onDemandApiToken,
    onDemandApiBaseUrl: callerEnv.THETA_ONDEMAND_API_BASE_URL ?? callerEnv.THETA_API_BASE_URL ?? base.onDemandApiBaseUrl,
    httpTimeoutMs: coerceInt(callerEnv.THETA_HTTP_TIMEOUT_MS, base.httpTimeoutMs, 1000, 120000),
    httpMaxRetries: coerceInt(callerEnv.THETA_HTTP_MAX_RETRIES, base.httpMaxRetries, 0, 6),
    httpRetryBackoffMs: coerceInt(callerEnv.THETA_HTTP_RETRY_BACKOFF_MS, base.httpRetryBackoffMs, 25, 10000)
  };
}

function requireFields(args: ThetaRuntimeCommandArgs, fields: string[]): void {
  for (const field of fields) {
    if (!(field in args) || args[field] === undefined || args[field] === null || args[field] === '') {
      throw new Error(`Missing required field: ${field}`);
    }
  }
}

function requireObject(value: unknown, field: string): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error(`${field} must be an object`);
  }
  return value as Record<string, unknown>;
}

function requireText(value: unknown, field: string): string {
  if (value === undefined || value === null || String(value).trim() === '') {
    throw new Error(`Missing required field: ${field}`);
  }
  return String(value).trim();
}

function resolveInputFields(args: ThetaRuntimeCommandArgs): string[] | undefined {
  if (Array.isArray(args.input_fields)) return args.input_fields.map((field) => requireText(field, 'input_fields[]'));
  if (Array.isArray(args.inputFields)) return args.inputFields.map((field) => requireText(field, 'inputFields[]'));
  const single = args.input_field ?? args.inputField;
  if (single !== undefined && single !== null && String(single).trim() !== '') return [requireText(single, 'input_field')];
  return undefined;
}

function resolveProjectId(cfg: ThetaConfig, args: ThetaRuntimeCommandArgs): string {
  return requireText(args.projectId ?? cfg.edgecloudProjectId, 'projectId');
}

const commandRegistry: Record<string, CommandRegistration> = {
  'theta.deployments.startByBaseId': {
    schema: {command:'theta.deployments.startByBaseId',description:'Restart stopped GPU node using its base ID',required:['baseId']},
    handler: (cfg,args) => deployments.startByBaseId(cfg,resolveProjectId(cfg,args),requireText(args.baseId,'baseId'),args.confirm===true)
  },
  'theta.templates.listStandard': {
    schema: { command: 'theta.templates.listStandard', description: 'List standard templates including training GPU nodes', required: ['category'] },
    handler: (cfg, args) => {
      if (!['prototyping', 'serving', 'training'].includes(String(args.category))) throw new Error('Invalid template category');
      return deployments.listStandard(cfg, args.category as 'prototyping' | 'serving' | 'training');
    }
  },
  'theta.templates.listCustom': {
    schema: { command: 'theta.templates.listCustom', description: 'List project custom deployment templates', required: [] },
    handler: (cfg, args) => deployments.listCustom(cfg, resolveProjectId(cfg, args))
  },
  'theta.video.uploadCreate': {
    schema: { command: 'theta.video.uploadCreate', description: 'Create video upload session; does not read local files', required: [] },
    handler: (cfg, args) => video.uploadCreate(cfg, args.confirm === true)
  },
  'theta.video.create': {
    schema: { command: 'theta.video.create', description: 'Create video from supplied remote-source payload', required: ['payload'] },
    handler: (cfg, args) => video.videoCreate(cfg, requireObject(args.payload, 'payload'), args.confirm === true)
  },
  'theta.video.get': {
    schema: { command: 'theta.video.get', description: 'Inspect a video', required: ['videoId'] },
    handler: (cfg, args) => video.videoGet(cfg, requireText(args.videoId, 'videoId'))
  },
  'theta.video.streamCreate': {
    schema: { command: 'theta.video.streamCreate', description: 'Create a livestream', required: ['payload'] },
    handler: (cfg, args) => video.streamCreate(cfg, requireObject(args.payload, 'payload'), args.confirm === true)
  },
  'theta.video.streamGet': {
    schema: { command: 'theta.video.streamGet', description: 'Inspect a livestream', required: ['streamId'] },
    handler: (cfg, args) => video.streamGet(cfg, requireText(args.streamId, 'streamId'))
  },
  'theta.video.ingestorList': {
    schema: { command: 'theta.video.ingestorList', description: 'List stream ingestors', required: [] },
    handler: (cfg) => video.ingestorList(cfg)
  },
  'theta.video.ingestorSelect': {
    schema: { command: 'theta.video.ingestorSelect', description: 'Select stream ingestor', required: ['ingestorId', 'body'] },
    handler: (cfg, args) => video.ingestorSelect(cfg, requireText(args.ingestorId, 'ingestorId'), requireObject(args.body, 'body'), args.confirm === true)
  },
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
      return inference.chat(cfg, args.body as { model: string; messages: Array<{ role: string; content: string }>; max_tokens?: number });
    }
  },
  'theta.inference.ready': {
    schema: { command: 'theta.inference.ready', description: 'Poll dedicated inference endpoint readiness with openai or gradio probe', required: [] },
    handler: (cfg, args) => inference.ready(cfg, {
      probe: args.probe as 'openai' | 'gradio' | undefined,
      timeoutMs: args.timeoutMs as number | undefined,
      intervalMs: args.intervalMs as number | undefined
    })
  },
  'theta.ondemand.listServices': {
    schema: { command: 'theta.ondemand.listServices', description: 'List live on-demand services with catalog fallback', required: [] },
    handler: (cfg, args) => ondemand.listLiveServices(cfg, { category: args.category as string | undefined })
  },
  'list_services': {
    schema: { command: 'list_services', description: 'MCP-compatible alias: list available Theta on-demand services', required: [] },
    handler: (cfg, args) => ondemand.listLiveServices(cfg, { category: args.category as string | undefined })
  },
  'theta.ondemand.infer': {
    schema: { command: 'theta.ondemand.infer', description: 'Create on-demand infer request (video, unknown or high-cost services and webhooks require confirm:true)', required: ['service', 'payload'] },
    handler: (cfg, args) => ondemand.infer(
      cfg,
      args.service as string,
      args.payload as Record<string, unknown>,
      { ...(args.options as { wait?: number; prediction?: string } | undefined), confirm: args.confirm === true }
    )
  },
  'infer': {
    schema: { command: 'infer', description: 'MCP-compatible alias: create on-demand infer request (video, unknown or high-cost services and webhooks require confirm:true)', required: ['service'] },
    handler: (cfg, args) => ondemand.infer(
      cfg,
      requireText(args.service, 'service'),
      (args.payload ?? {
        input: args.input ?? {},
        ...(args.variant ? { variant: args.variant } : {}),
        ...(args.webhook ? { webhook: args.webhook } : {})
      }) as Record<string, unknown>,
      {
        wait: args.wait as number | undefined,
        prediction: args.prediction as string | undefined,
        confirm: args.confirm === true
      }
    )
  },
  'theta.ondemand.chat': {
    schema: { command: 'theta.ondemand.chat', description: 'Run chat on-demand inference (GLM-5.3, Qwen3.8, Ling, Qwen3); tools only on GLM-5.3; defaults to Qwen3', required: ['messages'] },
    handler: (cfg, args) => ondemand.chat(
      cfg,
      (args.service as string | undefined) ?? 'qwen3',
      args.messages as Array<{ role: string; content: string }>,
      {
        maxTokens: args.max_tokens as number | undefined,
        temperature: args.temperature as number | undefined,
        topP: args.top_p as number | undefined,
        stream: args.stream as boolean | undefined,
        wait: args.wait as number | undefined,
        prediction: args.prediction as string | undefined,
        variant: args.variant as string | undefined,
        webhook: args.webhook as string | undefined,
        reasoningEffort: args.reasoning_effort as string | undefined,
        enableThinking: args.enable_thinking as boolean | undefined,
        tools: args.tools as Array<Record<string, unknown>> | undefined,
        toolChoice: args.tool_choice,
        parallelToolCalls: args.parallel_tool_calls as boolean | undefined,
        extraInput: args.extraInput as Record<string, unknown> | undefined,
        allowUnknownService: args.allowUnknownService as boolean | undefined,
        allowUnverifiedTools: args.allowUnverifiedTools === true,
        confirm: args.confirm === true
      }
    )
  },
  'theta.ondemand.status': {
    schema: { command: 'theta.ondemand.status', description: 'Get on-demand infer request status', required: ['requestId'] },
    handler: (cfg, args) => ondemand.status(cfg, args.requestId as string)
  },
  'get_request_status': {
    schema: { command: 'get_request_status', description: 'MCP-compatible alias: get on-demand infer request status', required: [] },
    handler: (cfg, args) => ondemand.status(cfg, requireText(args.request_id ?? args.requestId, 'request_id'))
  },
  'theta.ondemand.inputPresignedUrls': {
    schema: { command: 'theta.ondemand.inputPresignedUrls', description: 'Create presigned URLs for on-demand inputs', required: ['service'] },
    handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, args.service as string, resolveInputFields(args))
  },
  'get_upload_url': {
    schema: { command: 'get_upload_url', description: 'MCP-compatible alias: create presigned URLs for on-demand inputs', required: ['service'] },
    handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, requireText(args.service, 'service'), resolveInputFields(args))
  },
  'theta.ondemand.pollUntilDone': {
    schema: { command: 'theta.ondemand.pollUntilDone', description: 'Poll on-demand request until terminal state', required: ['requestId'] },
    handler: (cfg, args) => ondemand.pollUntilDone(cfg, args.requestId as string, args.options as { intervalMs?: number; timeoutMs?: number; maxAttempts?: number } | undefined)
  },
  'theta.deployments.list': {
    schema: { command: 'theta.deployments.list', description: 'List deployments for project', required: [] },
    handler: (cfg, args) => deployments.list(cfg, resolveProjectId(cfg,args))
  },
  'theta.deployments.routeProbe': {
    schema: { command: 'theta.deployments.routeProbe', description: 'Probe singular/plural deployment list routes for project', required: [] },
    handler: (cfg, args) => deployments.routeProbe(cfg, resolveProjectId(cfg, args))
  },
  'theta.deployments.create': {
    schema: { command: 'theta.deployments.create', description: 'Create deployment from payload', required: ['payload'] },
    handler: (cfg, args) => deployments.create(cfg, { ...requireObject(args.payload, 'payload'), project_id: resolveProjectId(cfg, args) }, args.confirm === true)
  },
  'theta.deployments.start': {
    schema: { command: 'theta.deployments.start', description: 'Start deployment by shard/suffix with route fallback', required: ['shard', 'suffix'] },
    handler: (cfg, args) => deployments.start(cfg, resolveProjectId(cfg, args), requireText(args.shard, 'shard'), requireText(args.suffix, 'suffix'), args.confirm === true)
  },
  'theta.deployments.stop': {
    schema: { command: 'theta.deployments.stop', description: 'Stop deployment by shard/suffix with route fallback', required: ['shard', 'suffix'] },
    handler: (cfg, args) => deployments.stop(cfg, resolveProjectId(cfg, args), requireText(args.shard, 'shard'), requireText(args.suffix, 'suffix'), args.confirm === true)
  },
  'theta.deployments.delete': {
    schema: { command: 'theta.deployments.delete', description: 'Delete deployment by shard/suffix with route fallback', required: ['shard', 'suffix'] },
    handler: (cfg, args) => deployments.delete(cfg, resolveProjectId(cfg, args), requireText(args.shard, 'shard'), requireText(args.suffix, 'suffix'), args.confirm === true)
  },
  'theta.deployments.validateDisposable': {
    schema: { command: 'theta.deployments.validateDisposable', description: 'Create, probe, smoke, delete, and report balance delta for one disposable deployment', required: ['payload'] },
    handler: (cfg, args) => deployments.validateDisposable(cfg, {
      payload: requireObject(args.payload, 'payload'),
      confirm: args.confirm === true,
      projectId: args.projectId as string | undefined,
      orgId: args.orgId as string | undefined,
      probe: args.probe as 'openai' | 'gradio' | undefined,
      readyTimeoutMs: args.readyTimeoutMs as number | undefined,
      intervalMs: args.intervalMs as number | undefined,
      smokeMessage: args.smokeMessage as string | undefined,
      model: args.model as string | undefined
    })
  },
  'theta.billing.balance': {
    schema: { command: 'theta.billing.balance', description: 'Read org balance in credits and USD (hosted MCP); falls back to raw controller credits', required: [] },
    handler: async (cfg, args) => {
      try {
        return { source: 'theta-hosted-mcp', ...(await billing.balanceUsd(cfg, resolveProjectId(cfg, args)) as Record<string, unknown>) };
      } catch (error) {
        return {
          source: 'controller-raw',
          warning: `Hosted MCP balance failed (${sanitizeHttpErrorMessage(String((error as Error).message)).slice(0, 300)}); raw value is credits, 1 credit = USD 0.01 on 2026-10-03`,
          response: await deployments.balance(cfg, args.orgId as string | undefined)
        };
      }
    }
  },
  'theta.billing.usage': {
    schema: { command: 'theta.billing.usage', description: 'Project usage by category and day in credits and USD (default last 7 days, max 366)', required: [] },
    handler: (cfg, args) => billing.usage(cfg, resolveProjectId(cfg, args), args.startDate as string | undefined, args.endDate as string | undefined)
  },
  'theta.billing.topUps': {
    schema: { command: 'theta.billing.topUps', description: 'Organization top-up history, newest first', required: [] },
    handler: (cfg, args) => billing.topUps(cfg, resolveProjectId(cfg, args), args.page as number | undefined, args.number as number | undefined)
  },
  'theta.billing.pricing': {
    schema: { command: 'theta.billing.pricing', description: 'Current chatbot, storage and on-demand prices (GPU prices come from theta.gpu.resources.list)', required: [] },
    handler: (cfg, args) => billing.pricing(cfg, resolveProjectId(cfg, args))
  },
  'theta.gpu.resources.list': {
    schema: { command: 'theta.gpu.resources.list', description: 'Hosted and community GPU capacity with region, availability and USD/hour; optional provider/gpuModel/region/maxPricePerHourUsd/availableOnly/limit filters', required: [] },
    handler: (cfg, args) => gpu.listResources(cfg, resolveProjectId(cfg, args), {
      provider: args.provider as string | undefined,
      gpuModel: args.gpuModel as string | undefined,
      region: args.region as string | undefined,
      maxPricePerHourUsd: args.maxPricePerHourUsd as number | undefined,
      availableOnly: args.availableOnly as boolean | undefined,
      limit: args.limit as number | undefined
    })
  },
  'theta.gpu.resources.get': {
    schema: { command: 'theta.gpu.resources.get', description: 'Details and current availability of one GPU resource', required: ['resourceId'] },
    handler: (cfg, args) => gpu.getResource(cfg, resolveProjectId(cfg, args), requireText(args.resourceId, 'resourceId'), args.region as string | undefined)
  },
  'theta.gpu.templates.list': {
    schema: { command: 'theta.gpu.templates.list', description: 'GPU Node deployment templates with allowed container images', required: [] },
    handler: (cfg, args) => gpu.listTemplates(cfg, resolveProjectId(cfg, args))
  },
  'theta.gpu.deployments.list': {
    schema: { command: 'theta.gpu.deployments.list', description: 'GPU Node deployments with state, resource and price', required: [] },
    handler: (cfg, args) => gpu.listDeployments(cfg, resolveProjectId(cfg, args))
  },
  'theta.gpu.deployments.get': {
    schema: { command: 'theta.gpu.deployments.get', description: 'One GPU Node deployment including endpoints and status', required: ['deploymentId'] },
    handler: (cfg, args) => gpu.getDeployment(cfg, resolveProjectId(cfg, args), requireText(args.deploymentId, 'deploymentId'))
  },
  'theta.gpu.deployments.events': {
    schema: { command: 'theta.gpu.deployments.events', description: 'Scheduling and lifecycle events of a GPU Node deployment', required: ['deploymentId'] },
    handler: (cfg, args) => gpu.deploymentEvents(cfg, resolveProjectId(cfg, args), requireText(args.deploymentId, 'deploymentId'))
  },
  'theta.gpu.deployments.logs': {
    schema: { command: 'theta.gpu.deployments.logs', description: 'Recent container logs of a GPU Node deployment', required: ['deploymentId'] },
    handler: (cfg, args) => gpu.deploymentLogs(cfg, resolveProjectId(cfg, args), requireText(args.deploymentId, 'deploymentId'))
  },
  'theta.gpu.deployments.create': {
    schema: { command: 'theta.gpu.deployments.create', description: 'PAID: create a GPU Node with a provider-side max_price_per_hour_usd cap; requires confirm:true after approval', required: ['name', 'deploymentTemplateId', 'resourceId', 'maxPricePerHourUsd'] },
    handler: (cfg, args) => gpu.createDeployment(cfg, resolveProjectId(cfg, args), {
      name: requireText(args.name, 'name'),
      deploymentTemplateId: requireText(args.deploymentTemplateId, 'deploymentTemplateId'),
      resourceId: requireText(args.resourceId, 'resourceId'),
      maxPricePerHourUsd: Number(args.maxPricePerHourUsd),
      confirm: args.confirm as boolean | undefined,
      region: args.region as string | undefined,
      displayName: args.displayName as string | undefined,
      containerImage: args.containerImage as string | undefined,
      sshPublicKey: args.sshPublicKey as string | undefined,
      sshPort: args.sshPort as number | undefined,
      httpPort: args.httpPort as number | undefined
    })
  },
  'theta.gpu.deployments.start': {
    schema: { command: 'theta.gpu.deployments.start', description: 'PAID: start a stopped GPU Node (resumes hourly billing); requires confirm:true', required: ['deploymentId'] },
    handler: (cfg, args) => gpu.lifecycle(cfg, resolveProjectId(cfg, args), 'start', requireText(args.deploymentId, 'deploymentId'), args.confirm as boolean | undefined)
  },
  'theta.gpu.deployments.stop': {
    schema: { command: 'theta.gpu.deployments.stop', description: 'Stop a running GPU Node (billing stops, config kept); requires confirm:true', required: ['deploymentId'] },
    handler: (cfg, args) => gpu.lifecycle(cfg, resolveProjectId(cfg, args), 'stop', requireText(args.deploymentId, 'deploymentId'), args.confirm as boolean | undefined)
  },
  'theta.gpu.deployments.delete': {
    schema: { command: 'theta.gpu.deployments.delete', description: 'PERMANENT: delete a GPU Node and its configuration; requires confirm:true', required: ['deploymentId'] },
    handler: (cfg, args) => gpu.lifecycle(cfg, resolveProjectId(cfg, args), 'delete', requireText(args.deploymentId, 'deploymentId'), args.confirm as boolean | undefined)
  },
  'theta.billing.balanceSnapshot': {
    schema: { command: 'theta.billing.balanceSnapshot', description: 'Read Theta org balance and extract numeric value when possible', required: [] },
    handler: (cfg, args) => deployments.balanceSnapshot(cfg, args.orgId as string | undefined)
  },
  'theta.ai.agent.create': {
    schema: { command: 'theta.ai.agent.create', description: 'Create Theta EdgeCloud AI Agent/RAG chatbot', required: ['payload'] },
    handler: (cfg, args) => deployments.chatbotCreate(cfg, { ...requireObject(args.payload, 'payload'), project_id: resolveProjectId(cfg, args) }, args.confirm === true)
  },
  'theta.ai.agent.get': {
    schema: { command: 'theta.ai.agent.get', description: 'Fetch Theta EdgeCloud AI Agent/RAG chatbot details', required: ['chatbotId'] },
    handler: (cfg, args) => deployments.chatbotGet(cfg, requireText(args.chatbotId, 'chatbotId'), resolveProjectId(cfg, args))
  },
  'theta.ai.agent.update': {
    schema: { command: 'theta.ai.agent.update', description: 'Update Theta EdgeCloud AI Agent/RAG chatbot settings', required: ['chatbotId', 'payload'] },
    handler: (cfg, args) => deployments.chatbotUpdate(cfg, requireText(args.chatbotId, 'chatbotId'), { ...requireObject(args.payload, 'payload'), project_id: resolveProjectId(cfg, args) }, args.confirm === true)
  },
  'theta.ai.agent.list': {
    schema: { command: 'theta.ai.agent.list', description: 'List Theta EdgeCloud AI Agent/RAG chatbots', required: [] },
    handler: (cfg, args) => deployments.chatbotList(cfg, resolveProjectId(cfg, args), args.page as number | undefined, args.number as number | undefined)
  },
  'theta.ai.agent.document.create': {
    schema: { command: 'theta.ai.agent.document.create', description: 'Create AI Agent knowledge-base document from provided content', required: ['chatbotId', 'file'] },
    handler: (cfg, args) => deployments.chatbotDocumentCreate(
      cfg,
      requireText(args.chatbotId, 'chatbotId'),
      resolveProjectId(cfg, args),
      requireObject(args.file, 'file') as { filename: string; content: string; contentType?: string; encoding?: 'utf8' | 'base64' },
      args.metadata as Record<string, unknown> | undefined,
      args.confirm === true
    )
  },
  'theta.ai.agent.document.update': {
    schema: { command: 'theta.ai.agent.document.update', description: 'Update AI Agent knowledge-base document from provided content', required: ['chatbotId', 'documentId', 'file'] },
    handler: (cfg, args) => deployments.chatbotDocumentUpdate(
      cfg,
      requireText(args.chatbotId, 'chatbotId'),
      requireText(args.documentId, 'documentId'),
      resolveProjectId(cfg, args),
      requireObject(args.file, 'file') as { filename: string; content: string; contentType?: string; encoding?: 'utf8' | 'base64' },
      args.metadata as Record<string, unknown> | undefined,
      args.confirm === true
    )
  },
  'theta.ai.agent.document.get': {
    schema: { command: 'theta.ai.agent.document.get', description: 'Fetch AI Agent knowledge-base document', required: ['chatbotId', 'documentId'] },
    handler: (cfg, args) => deployments.chatbotDocumentGet(cfg, requireText(args.chatbotId, 'chatbotId'), requireText(args.documentId, 'documentId'))
  },
  'theta.ai.agent.document.list': {
    schema: { command: 'theta.ai.agent.document.list', description: 'List AI Agent knowledge-base documents', required: ['chatbotId'] },
    handler: (cfg, args) => deployments.chatbotDocumentList(
      cfg,
      requireText(args.chatbotId, 'chatbotId'),
      resolveProjectId(cfg, args),
      args.page as number | undefined,
      args.number as number | undefined
    )
  },
  'theta.deployments.listVm': {
    schema: { command: 'theta.deployments.listVm', description: 'List EdgeCloud VM types', required: [] },
    handler: (cfg) => deployments.listVm(cfg)
  },
  'theta.video.list': {
    schema: { command: 'theta.video.list', description: 'List videos for service account', required: ['serviceAccountId'] },
    handler: (cfg, args) => video.videoList(cfg, args.serviceAccountId as string, (args.page as number | undefined) ?? 1, (args.number as number | undefined) ?? 10)
  },
};

const onDemandTokenCommands = new Set<string>([
  'theta.ondemand.infer',
  'theta.ondemand.chat',
  'theta.ondemand.status',
  'theta.ondemand.inputPresignedUrls',
  'theta.ondemand.pollUntilDone',
  'infer',
  'get_request_status',
  'get_upload_url'
]);

// Billable, persistent or destructive remote mutations. Code-enforced: outside dry-run they
// require confirm:true, which an agent passes only after the user approves the specific action.
// Router-level copy of the approval rule (the network clients enforce the same rule themselves):
// every PUT/DELETE and every resource-creating or persistent POST requires confirm:true. Ungated by
// design: chat on listed models and inference on the listed low-cost services (max_tokens <= 5000
// per call), dedicated-endpoint chat, upload-URL creation, and read-only queries.
const confirmRequiredCommands = new Set<string>([
  'theta.deployments.create', 'theta.deployments.start', 'theta.deployments.stop', 'theta.deployments.delete',
  'theta.deployments.startByBaseId', 'theta.deployments.validateDisposable',
  'theta.ai.agent.create', 'theta.ai.agent.update', 'theta.ai.agent.document.create', 'theta.ai.agent.document.update',
  'theta.video.uploadCreate', 'theta.video.create', 'theta.video.streamCreate', 'theta.video.ingestorSelect',
  'theta.characters.create', 'theta.characters.update', 'theta.characters.delete',
  'theta.characters.session.create', 'theta.characters.session.delete', 'theta.characters.session.context',
  'theta.characters.session.message',
  'theta.gpu.deployments.create', 'theta.gpu.deployments.start', 'theta.gpu.deployments.stop', 'theta.gpu.deployments.delete'
]);

export function thetaCommandRequiresConfirm(command: string): boolean {
  return confirmRequiredCommands.has(command);
}

for (const [name, route] of Object.entries(characterRoutes)) {
  const command = `theta.characters.${name}`;
  commandRegistry[command] = {
    schema: {command, description: `AI Characters ${name}; game-scoped key required`, required: [...route.fields, ...(['POST','PUT'].includes(route.method) ? ['payload'] : [])]},
    handler: (cfg, args) => characterRequest(cfg, name, args)
  };
}

export const thetaRuntimeCommandSchemas: Record<string, ThetaCommandSchema> = Object.fromEntries(
  Object.entries(commandRegistry).map(([cmd, reg]) => [cmd, confirmRequiredCommands.has(cmd)
    ? { ...reg.schema, description: `${reg.schema.description} [requires confirm:true outside dry-run]` }
    : reg.schema])
);

export function listThetaRuntimeCommands(): string[] {
  return Object.keys(commandRegistry).sort();
}

export async function executeThetaRuntimeCommand(
  args: ThetaRuntimeCommandArgs,
  ctx: ThetaRuntimeContext = {}
): Promise<unknown> {
  const registration = Object.hasOwn(commandRegistry, args.command) ? commandRegistry[args.command] : undefined;
  if (!registration) {
    throw new Error(`Unsupported theta runtime command: ${args.command}`);
  }

  requireFields(args, registration.schema.required);
  const cfg = await buildRuntimeConfig(ctx);

  if (onDemandTokenCommands.has(args.command) && !cfg.dryRun && !cfg.onDemandApiToken) {
    throw new Error('THETA_ONDEMAND_API_TOKEN missing (runtime secret/env resolver)');
  }

  if (confirmRequiredCommands.has(args.command) && !cfg.dryRun && args.confirm !== true) {
    throw new Error(`${args.command} creates, changes, bills or deletes remote resources. Preview with THETA_DRY_RUN=1, get explicit user approval for this exact action, then pass confirm:true.`);
  }

  const result = await registration.handler(cfg, args);
  // Live results and previews: fields whose names mark secrets (password, token, secret, api key,
  // authorization, credential) are replaced with [redacted]. Usage counts (*_tokens) are kept.
  return result && typeof result === 'object' ? redactObject(result as Record<string, unknown>) : result;
}
