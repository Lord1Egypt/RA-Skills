import { redactObject } from '../redaction.js';
import { ThetaConfig } from '../config.js';
import { thetaVideoClient } from '../clients/thetaVideo.js';

export const video = {
  uploadCreate: (cfg: ThetaConfig, confirm?: boolean) => cfg.dryRun ? { dryRun: true } : thetaVideoClient.createUploadSession(cfg, confirm),
  videoCreate: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : thetaVideoClient.createVideo(cfg, payload, confirm),
  videoGet: (cfg: ThetaConfig, videoId: string) => thetaVideoClient.getVideo(cfg, videoId),
  videoList: (cfg: ThetaConfig, serviceAccountId: string, page = 1, number = 10) => thetaVideoClient.listVideos(cfg, serviceAccountId, page, number),
  streamCreate: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : thetaVideoClient.createStream(cfg, payload, confirm),
  streamGet: (cfg: ThetaConfig, streamId: string) => thetaVideoClient.getStream(cfg, streamId),
  ingestorList: (cfg: ThetaConfig) => thetaVideoClient.listIngestors(cfg),
  ingestorSelect: (cfg: ThetaConfig, ingestorId: string, body: Record<string, unknown>, confirm?: boolean) => cfg.dryRun ? redactObject({ dryRun: true, ingestorId, body }) : thetaVideoClient.selectIngestor(cfg, ingestorId, body, confirm)
};
