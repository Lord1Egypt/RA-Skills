import { loadConfig } from './config.js';
import { redactObject } from './redaction.js';
import { deployments } from './commands/deployments.js';
import { inference } from './commands/inference.js';
import { video } from './commands/video.js';
import { ondemand } from './commands/ondemand.js';
import { healthCheck } from './commands/health.js';
import {
  executeThetaRuntimeCommand,
  listThetaRuntimeCommands,
  thetaRuntimeCommandSchemas,
  thetaCommandRequiresConfirm,
  type ThetaRuntimeCommandArgs,
  type ThetaRuntimeContext
} from './runtime/handlers.js';
import type { ThetaSecretResolverContext } from './runtime/secretResolver.js';

// theta() is a read-only facade: it can list, inspect and poll. It cannot send prompts, spend
// credits or change remote resources, and it never returns credential values.
// executeThetaRuntimeCommand (exported below) runs every command. Approval is not enforced here:
// the network clients require confirm:true for their mutations, high-cost inference and webhook.
// Facade results get the same labelled-secret redaction as runtime results.
async function safe<T>(value: T | Promise<T>): Promise<T> {
  const result = await value;
  return result && typeof result === 'object' ? redactObject(result as Record<string, unknown>) as T : result;
}

export function theta() {
  const cfg = loadConfig();
  return {
    // Which credential families are configured. Never the credential values themselves.
    configured: {
      onDemand: Boolean(cfg.onDemandApiToken),
      controller: Boolean(cfg.edgecloudApiKey),
      project: Boolean(cfg.edgecloudProjectId),
      video: Boolean(cfg.videoSaId && cfg.videoSaSecret),
      characters: Boolean(cfg.charactersApiKey),
      dedicatedEndpoint: Boolean(cfg.inferenceEndpoint),
      dryRun: cfg.dryRun
    },
    deploy: {
      listStandard: (category: 'prototyping' | 'serving' | 'training') => safe(deployments.listStandard(cfg, category)),
      listCustom: (projectId: string) => safe(deployments.listCustom(cfg, projectId)),
      listVm: () => safe(deployments.listVm(cfg)),
      list: (projectId: string) => safe(deployments.list(cfg, projectId)),
      routeProbe: (projectId: string) => safe(deployments.routeProbe(cfg, projectId)),
      balance: (orgId?: string) => safe(deployments.balance(cfg, orgId)),
      chatbotGet: (chatbotId: string, projectId: string) => safe(deployments.chatbotGet(cfg, chatbotId, projectId)),
      chatbotList: (projectId: string, page?: number, number?: number) => safe(deployments.chatbotList(cfg, projectId, page, number)),
      chatbotDocumentGet: (chatbotId: string, documentId: string) => safe(deployments.chatbotDocumentGet(cfg, chatbotId, documentId)),
      chatbotDocumentList: (chatbotId: string, projectId: string, page?: number, number?: number) => safe(deployments.chatbotDocumentList(cfg, chatbotId, projectId, page, number))
    },
    inference: {
      models: () => safe(inference.models(cfg)),
      ready: (opts?: Parameters<typeof inference.ready>[1]) => safe(inference.ready(cfg, opts))
    },
    video: {
      videoGet: (videoId: string) => safe(video.videoGet(cfg, videoId)),
      videoList: (serviceAccountId: string, page?: number, number?: number) => safe(video.videoList(cfg, serviceAccountId, page, number)),
      streamGet: (streamId: string) => safe(video.streamGet(cfg, streamId)),
      ingestorList: () => safe(video.ingestorList(cfg))
    },
    ondemand: {
      catalog: ondemand.catalog,
      listServices: (opts?: Parameters<typeof ondemand.listServices>[0]) => safe(ondemand.listServices(opts)),
      listLiveServices: (opts?: Parameters<typeof ondemand.listLiveServices>[1]) => safe(ondemand.listLiveServices(cfg, opts)),
      status: (requestId: string) => safe(ondemand.status(cfg, requestId)),
      pollUntilDone: (requestId: string, opts?: Parameters<typeof ondemand.pollUntilDone>[2]) => safe(ondemand.pollUntilDone(cfg, requestId, opts))
    },
    healthCheck: () => safe(healthCheck(cfg))
  };
}

export {
  executeThetaRuntimeCommand,
  listThetaRuntimeCommands,
  thetaRuntimeCommandSchemas,
  thetaCommandRequiresConfirm
};

export type {
  ThetaRuntimeCommandArgs,
  ThetaRuntimeContext,
  ThetaSecretResolverContext
};
