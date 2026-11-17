import { ThetaConfig } from '../config.js';
import { assertApproved } from '../approval.js';
import { edgecloudControllerClient, type ChatbotDocumentFile } from '../clients/edgecloudController.js';
import { edgecloudInferenceClient } from '../clients/edgecloudInference.js';
import { BasicAuth } from '../types.js';
import { redactObject } from '../redaction.js';
import { randomBytes } from 'node:crypto';

type DisposableValidationOptions = {
  confirm?: boolean;
  payload: Record<string, unknown>;
  projectId?: string;
  orgId?: string;
  probe?: 'openai' | 'gradio';
  readyTimeoutMs?: number;
  intervalMs?: number;
  smokeMessage?: string;
  model?: string;
};

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

function requireText(value: unknown, field: string): string {
  if (value === undefined || value === null || String(value).trim() === '') {
    throw new Error(`${field} must be a non-empty string`);
  }
  return String(value).trim();
}

function clampInt(value: number | undefined, fallback: number, min: number, max: number): number {
  if (!Number.isFinite(value)) return fallback;
  return Math.min(Math.max(Math.trunc(value as number), min), max);
}

function generatedPassword(): string {
  return randomBytes(18).toString('base64url');
}

function findKey(obj: unknown, names: Set<string>): unknown {
  if (obj && typeof obj === 'object') {
    if (Array.isArray(obj)) {
      for (const item of obj) {
        const found = findKey(item, names);
        if (found !== undefined && found !== null && found !== '') return found;
      }
      return undefined;
    }
    for (const [key, value] of Object.entries(obj)) {
      if (names.has(key.toLowerCase()) && value !== undefined && value !== null && value !== '') return value;
    }
    for (const value of Object.values(obj)) {
      const found = findKey(value, names);
      if (found !== undefined && found !== null && found !== '') return found;
    }
  }
  return undefined;
}

function extractNumericValue(obj: unknown, names: Set<string>): number | undefined {
  if (obj && typeof obj === 'object') {
    if (Array.isArray(obj)) {
      for (const item of obj) {
        const found = extractNumericValue(item, names);
        if (found !== undefined) return found;
      }
      return undefined;
    }
    for (const [key, value] of Object.entries(obj)) {
      if (!names.has(key.toLowerCase())) continue;
      const parsed = Number(value);
      if (Number.isFinite(parsed)) return parsed;
    }
    for (const value of Object.values(obj)) {
      const found = extractNumericValue(value, names);
      if (found !== undefined) return found;
    }
  }
  return undefined;
}

function balanceValue(response: unknown): number | undefined {
  return extractNumericValue(response, new Set(['balance', 'amount', 'available', 'credit', 'credits', 'remaining', 'total']));
}

async function balanceSnapshot(cfg: ThetaConfig, orgId?: string) {
  const resolvedOrgId = orgId ?? cfg.edgecloudOrgId;
  if (!resolvedOrgId) return { skipped: true, reason: 'missing_org_id' };
  if (!cfg.edgecloudApiKey) return { skipped: true, reason: 'missing_THETA_EC_API_KEY' };
  try {
    const response = await edgecloudControllerClient.balance(cfg, resolvedOrgId);
    return { skipped: false, orgId: resolvedOrgId, value: balanceValue(response), response };
  } catch (error) {
    return {
      skipped: true,
      reason: 'balance_lookup_failed',
      error: (error as { message?: string } | undefined)?.message ?? String(error)
    };
  }
}

function balanceDelta(before: Record<string, unknown>, after: Record<string, unknown>) {
  const beforeValue = typeof before.value === 'number' ? before.value : undefined;
  const afterValue = typeof after.value === 'number' ? after.value : undefined;
  return {
    before,
    after,
    delta: beforeValue !== undefined && afterValue !== undefined ? afterValue - beforeValue : null
  };
}

async function waitForDedicatedProbe(
  cfg: ThetaConfig,
  endpoint: string,
  auth: BasicAuth,
  probe: 'openai' | 'gradio',
  timeoutMs: number,
  intervalMs: number
) {
  const startedAt = Date.now();
  const attempts: Array<Record<string, unknown>> = [];
  while (Date.now() - startedAt < timeoutMs) {
    const attemptStartedAt = Date.now();
    try {
      const response = probe === 'gradio'
        ? await edgecloudInferenceClient.gradioConfig(cfg, endpoint, auth)
        : await edgecloudInferenceClient.listModels(cfg, endpoint, auth);
      attempts.push({ ok: true, elapsedMs: Date.now() - attemptStartedAt });
      return { ready: true, probe, endpoint, elapsedMs: Date.now() - startedAt, attempts, response };
    } catch (error) {
      attempts.push({
        ok: false,
        elapsedMs: Date.now() - attemptStartedAt,
        status: (error as { status?: number } | undefined)?.status,
        code: (error as { code?: string; name?: string } | undefined)?.code ?? (error as { name?: string } | undefined)?.name,
        message: (error as { message?: string } | undefined)?.message ?? String(error)
      });
    }
    const remainingMs = timeoutMs - (Date.now() - startedAt);
    if (remainingMs <= 0) break;
    await sleep(Math.min(intervalMs, remainingMs));
  }
  return { ready: false, probe, endpoint, elapsedMs: Date.now() - startedAt, attempts };
}

export const deployments = {
  startByBaseId: (cfg: ThetaConfig, projectId: string, baseId: string, confirm?: boolean) => cfg.dryRun ? {dryRun:true,action:'startByBaseId',projectId,baseId} : edgecloudControllerClient.startDeploymentByBaseId(cfg,projectId,baseId,confirm),
  listStandard: (cfg: ThetaConfig, category: 'prototyping' | 'serving' | 'training') => edgecloudControllerClient.listStandardTemplates(cfg, category),
  listCustom: (cfg: ThetaConfig, projectId: string) => edgecloudControllerClient.listCustomTemplates(cfg, projectId),
  listVm: (cfg: ThetaConfig) => edgecloudControllerClient.listVmTypes(cfg),
  balance: (cfg: ThetaConfig, orgId?: string) => edgecloudControllerClient.balance(cfg, requireText(orgId ?? cfg.edgecloudOrgId, 'orgId')),
  balanceSnapshot,
  routeProbe: (cfg: ThetaConfig, projectId: string) => edgecloudControllerClient.routeProbeDeploymentsList(cfg, projectId),
  create: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : edgecloudControllerClient.createDeployment(cfg, payload, confirm),
  list: (cfg: ThetaConfig, projectId: string) => edgecloudControllerClient.listDeployments(cfg, projectId),
  start: (cfg: ThetaConfig, projectId: string, shard: string, suffix: string, confirm?: boolean) => cfg.dryRun ? { dryRun: true, action: 'start', projectId, shard, suffix } : edgecloudControllerClient.startDeployment(cfg, projectId, shard, suffix, confirm),
  stop: (cfg: ThetaConfig, projectId: string, shard: string, suffix: string, confirm?: boolean) => cfg.dryRun ? { dryRun: true, action: 'stop', projectId, shard, suffix } : edgecloudControllerClient.stopDeployment(cfg, projectId, shard, suffix, confirm),
  delete: (cfg: ThetaConfig, projectId: string, shard: string, suffix: string, confirm?: boolean) => cfg.dryRun ? { dryRun: true, action: 'delete', projectId, shard, suffix } : edgecloudControllerClient.deleteDeployment(cfg, projectId, shard, suffix, confirm),
  validateDisposable: async (cfg: ThetaConfig, opts: DisposableValidationOptions) => {
    const payload = { ...opts.payload };
    const projectId = String(opts.projectId ?? payload.project_id ?? cfg.edgecloudProjectId ?? '').trim();
    if (!projectId) throw new Error('projectId or payload.project_id is required');
    payload.project_id = projectId;

    const authUser = String(payload.auth_username ?? `openclaw_${randomBytes(4).toString('hex')}`);
    const authPass = String(payload.auth_password ?? generatedPassword());
    payload.auth_username = authUser;
    payload.auth_password = authPass;
    const auth = { user: authUser, pass: authPass };
    const probe = opts.probe ?? 'openai';
    const readyTimeoutMs = clampInt(opts.readyTimeoutMs, 120000, 1000, 1800000);
    const intervalMs = clampInt(opts.intervalMs, 10000, 500, 60000);

    if (cfg.dryRun) {
      return redactObject({
        dryRun: true,
        would: [
          'read org balance before if orgId is configured',
          'create deployment with generated Basic Auth',
          `poll ${probe} readiness`,
          'run one minimal smoke call for OpenAI-compatible probes',
          'delete deployment in cleanup',
          'verify cleanup from deployment list',
          'read org balance after and report delta'
        ],
        payload,
        probe,
        readyTimeoutMs,
        intervalMs,
        orgIdConfigured: Boolean(opts.orgId ?? cfg.edgecloudOrgId)
      });
    }

    // PAID create + delete: refuse before any request (including the balance read) without approval.
    assertApproved(cfg, opts.confirm, 'theta.deployments.validateDisposable');
    let created: unknown;
    let readiness: unknown;
    let smoke: unknown;
    let deleteResult: unknown;
    let cleanupVerification: unknown;
    let operationFailure: string | undefined;
    const before = await balanceSnapshot(cfg, opts.orgId);
    try {
      created = await edgecloudControllerClient.createDeployment(cfg, payload, opts.confirm);
      const endpoint = String(findKey(created, new Set(['endpoint', 'endpointurl', 'url'])) ?? '').trim();
      if (!endpoint) throw new Error('Deployment create response did not include an endpoint');

      readiness = await waitForDedicatedProbe(cfg, endpoint, auth, probe, readyTimeoutMs, intervalMs);
      if (probe === 'openai' && (readiness as { ready?: boolean }).ready && opts.smokeMessage) {
        const readinessModel = findKey((readiness as { response?: unknown }).response, new Set(['id', 'model']));
        smoke = await edgecloudInferenceClient.chat(
          cfg,
          {
            model: opts.model ?? String(readinessModel ?? 'default'),
            messages: [{ role: 'user', content: opts.smokeMessage }],
            max_tokens: 32
          },
          endpoint,
          auth
        );
      }
    } catch (error) {
      operationFailure = (error as Error)?.message ?? String(error);
    } finally {
      const baseId = created ? findKey(created, new Set(['baseid', 'base_id', 'deployment_id', 'id'])) : undefined;
      const shard = created ? findKey(created, new Set(['shard'])) : undefined;
      const suffix = created ? findKey(created, new Set(['suffix'])) : undefined;
      if (created && shard !== undefined && shard !== null && String(shard) !== '' && suffix !== undefined && suffix !== null && String(suffix) !== '') {
        try {
          await edgecloudControllerClient.deleteDeployment(cfg, projectId, String(shard), String(suffix), opts.confirm);
          deleteResult = { ok: true, shard, suffix };
        } catch (error) {
          deleteResult = { ok: false, error: (error as { message?: string } | undefined)?.message ?? String(error) };
        }
      } else {
        deleteResult = { ok: false, warning: 'could_not_determine_delete_handle', baseId, shard, suffix };
      }

      try {
        const listed = await edgecloudControllerClient.listDeployments(cfg, projectId);
        const needleValues = [baseId, suffix].filter((value) => value !== undefined && value !== null && value !== '').map(String);
        const response = listed as {body?: unknown; deployments?: unknown};
        const body = response?.body ?? listed;
        const rows = Array.isArray(body) ? body : (body as {deployments?: unknown})?.deployments;
        const identifiable = (entry: unknown): boolean => !!entry && typeof entry === 'object' && Object.entries(entry).some(([key,value]) =>
          (['baseid','base_id','deployment_id','id','suffix'].includes(key.toLowerCase()) && ['string','number'].includes(typeof value) && String(value).length > 0) ||
          (typeof value === 'object' && identifiable(value)));
        const knownList = Array.isArray(rows) && rows.every(identifiable);
        const containsHandle = (entry: unknown): boolean => {
          if (!entry || typeof entry !== 'object') return false;
          return Object.entries(entry).some(([key,value]) =>
            (['baseid','base_id','deployment_id','id','suffix'].includes(key.toLowerCase()) && needleValues.includes(String(value))) ||
            (typeof value === 'object' && containsHandle(value)));
        };
        cleanupVerification = {
          checked: knownList && needleValues.length > 0,
          projectId,
          deletedHandlesAbsent: knownList && needleValues.length > 0 && !rows.some(containsHandle),
          handlesChecked: needleValues
        };
      } catch (error) {
        cleanupVerification = { checked: false, error: (error as { message?: string } | undefined)?.message ?? String(error) };
      }
    }
    const after = await balanceSnapshot(cfg, opts.orgId);

    return redactObject({
      // ok = create, readiness and verified cleanup all succeeded, plus (for the default openai
      // probe) a successful inference smoke call, which needs smokeMessage. smokeTested says
      // whether inference was exercised.
      ok: !operationFailure && (readiness as {ready?: boolean})?.ready === true && (deleteResult as {ok?: boolean})?.ok === true && (cleanupVerification as {deletedHandlesAbsent?: boolean})?.deletedHandlesAbsent === true
        && ((opts.probe ?? 'openai') !== 'openai' || smoke !== undefined),
      smokeTested: smoke !== undefined,
      operationFailure,
      createResponse: created,
      readiness,
      smokeResponse: smoke,
      deleteResult,
      cleanupVerification,
      balance: balanceDelta(before, after)
    });
  },
  chatbotCreate: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : edgecloudControllerClient.createChatbot(cfg, payload, confirm),
  chatbotGet: (cfg: ThetaConfig, chatbotId: string, projectId: string) => edgecloudControllerClient.getChatbot(cfg, chatbotId, projectId),
  chatbotUpdate: (cfg: ThetaConfig, chatbotId: string, payload: Record<string, unknown>, confirm?: boolean) => cfg.dryRun ? redactObject({ dryRun: true, chatbotId, payload }) : edgecloudControllerClient.updateChatbot(cfg, chatbotId, payload, confirm),
  chatbotList: (cfg: ThetaConfig, projectId: string, page = 0, number = 100) => edgecloudControllerClient.listChatbots(cfg, projectId, page, number),
  chatbotDocumentCreate: (cfg: ThetaConfig, chatbotId: string, projectId: string, file: ChatbotDocumentFile, metadata?: Record<string, unknown>, confirm?: boolean) =>
    cfg.dryRun ? { dryRun: true, chatbotId, projectId, file: { ...file, content: '[redacted]' }, metadata } : edgecloudControllerClient.createChatbotDocument(cfg, chatbotId, projectId, file, metadata, confirm),
  chatbotDocumentUpdate: (cfg: ThetaConfig, chatbotId: string, documentId: string, projectId: string, file: ChatbotDocumentFile, metadata?: Record<string, unknown>, confirm?: boolean) =>
    cfg.dryRun ? { dryRun: true, chatbotId, documentId, projectId, file: { ...file, content: '[redacted]' }, metadata } : edgecloudControllerClient.updateChatbotDocument(cfg, chatbotId, documentId, projectId, file, metadata, confirm),
  chatbotDocumentGet: (cfg: ThetaConfig, chatbotId: string, documentId: string) => edgecloudControllerClient.getChatbotDocument(cfg, chatbotId, documentId),
  chatbotDocumentList: (cfg: ThetaConfig, chatbotId: string, projectId: string, page = 0, number = 30) => edgecloudControllerClient.listChatbotDocuments(cfg, chatbotId, projectId, page, number),
};
