// Data flow: sends Theta Video service-account credentials (x-tva-sa-id/x-tva-sa-secret) and
// request payloads to https://api.thetavideoapi.com only. Every create/select call requires
// confirm:true here, in the client.
import { ThetaConfig } from '../config.js';
import { getJson, postJson, putJson } from './http.js';
import { pathSegment } from '../security.js';
import { assertApproved } from '../approval.js';

const BASE = 'https://api.thetavideoapi.com';

function h(cfg: ThetaConfig): HeadersInit {
  if (!cfg.videoSaId || !cfg.videoSaSecret) throw new Error('THETA_VIDEO_SA_ID / THETA_VIDEO_SA_SECRET missing');
  return { 'x-tva-sa-id': cfg.videoSaId, 'x-tva-sa-secret': cfg.videoSaSecret };
}

function net(cfg: ThetaConfig, headers: HeadersInit) {
  return {
    headers,
    service: 'theta-video',
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}

export const thetaVideoClient = {
  createUploadSession: (cfg: ThetaConfig, confirm?: boolean) => assertApproved(cfg, confirm, 'theta.video.uploadCreate') ?? postJson(`${BASE}/upload`, {}, net(cfg, h(cfg))),
  createVideo: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => assertApproved(cfg, confirm, 'theta.video.create') ?? postJson(`${BASE}/video`, payload, net(cfg, h(cfg))),
  getVideo: (cfg: ThetaConfig, videoId: string) => getJson(`${BASE}/video/${pathSegment(videoId,'videoId')}`, net(cfg, h(cfg))),
  listVideos: (cfg: ThetaConfig, serviceAccountId: string, page = 1, number = 10) =>
    getJson(`${BASE}/video/${pathSegment(serviceAccountId,'serviceAccountId')}/list?${new URLSearchParams({page:String(page),number:String(number)})}`, net(cfg, h(cfg))),
  createStream: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => assertApproved(cfg, confirm, 'theta.video.streamCreate') ?? postJson(`${BASE}/stream`, payload, net(cfg, h(cfg))),
  getStream: (cfg: ThetaConfig, streamId: string) => getJson(`${BASE}/stream/${pathSegment(streamId,'streamId')}`, net(cfg, h(cfg))),
  listIngestors: (cfg: ThetaConfig) => getJson(`${BASE}/ingestor/filter`, net(cfg, h(cfg))),
  selectIngestor: (cfg: ThetaConfig, ingestorId: string, body: Record<string, unknown>, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.video.ingestorSelect') ?? putJson(`${BASE}/ingestor/${pathSegment(ingestorId,'ingestorId')}/select`, body, net(cfg, h(cfg)))
};
