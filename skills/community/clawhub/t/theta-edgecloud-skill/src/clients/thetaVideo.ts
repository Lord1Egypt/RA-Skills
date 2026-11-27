// Data flow: sends Theta Video service-account credentials (x-tva-sa-id/x-tva-sa-secret) and
// request payloads to https://api.thetavideoapi.com only. Every create/select/unselect call requires
// confirm:true here, in the client, and refuses in dry-run (previews come from commands/video.ts,
// which redacts them). Every object or array response this client returns is name-redacted here
// with redactObject, so livestream keys (stream_key) and other secret-named fields never leave
// the client unredacted. Unlabelled free text is not secret-scanned.
import { ThetaConfig } from '../config.js';
import { redactObject } from '../redaction.js';
import { getJson, postJson, putJson } from './http.js';
import { pathSegment } from '../security.js';
import { assertApproved } from '../approval.js';

const BASE = 'https://api.thetavideoapi.com';

const RESERVED_QUERY = new Set(['page', 'number', 'operator']);
const FILTER_KEY = /^[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}$/;
const MAX_FILTERS = 10;

function boundedInt(value: unknown, label: string, fallback: number, min: number, max: number): number {
  if (value === undefined) return fallback;
  if (typeof value !== 'number' || !Number.isInteger(value) || value < min || value > max) throw new Error(('' + String(label) + ' must be an integer from ' + String(min) + ' to ' + String(max)));
  return value;
}

// Metadata search: every key and value is validated and encoded by URLSearchParams, so a filter
// cannot add or override page/number/operator or inject other query parameters.
export function videoSearchQuery(filters: unknown, operator: unknown, page: unknown, number: unknown): string {
  if (!filters || typeof filters !== 'object' || Array.isArray(filters)) throw new Error('filters must be an object of metadata key -> string value');
  const entries = Object.entries(filters as Record<string, unknown>);
  if (entries.length < 1 || entries.length > MAX_FILTERS) throw new Error(('filters must have 1 to ' + String(MAX_FILTERS) + ' keys'));
  const params = new URLSearchParams();
  for (const [key, value] of entries) {
    if (!FILTER_KEY.test(key) || RESERVED_QUERY.has(key.toLowerCase())) throw new Error(('invalid filter key: ' + String(key.slice(0, 64))));
    if (typeof value !== 'string' || value.length > 256 || /[\x00-\x1f\x7f]/.test(value)) throw new Error(('filter ' + String(key) + ' must be a string of at most 256 printable characters'));
    params.append(key, value);
  }
  if (operator !== undefined && operator !== 'and' && operator !== 'or') throw new Error('operator must be "and" or "or"');
  if (operator) params.set('operator', operator);
  params.set('page', String(boundedInt(page, 'page', 1, 1, 10000)));
  params.set('number', String(boundedInt(number, 'number', 10, 1, 100)));
  return params.toString();
}

// Applied to every client method's result (see thetaVideoClient below).
async function redacted(result: unknown): Promise<unknown> {
  const value = await result;
  return value && typeof value === 'object' ? redactObject(value as Record<string, unknown>) : value;
}

function videoHeaders(cfg: ThetaConfig): HeadersInit {
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
  createUploadSession: (cfg: ThetaConfig, confirm?: boolean) => redacted(assertApproved(cfg, confirm, 'theta.video.uploadCreate') ?? postJson(('' + String(BASE) + '/upload'), {}, net(cfg, videoHeaders(cfg)))),
  createVideo: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => redacted(assertApproved(cfg, confirm, 'theta.video.create') ?? postJson(('' + String(BASE) + '/video'), payload, net(cfg, videoHeaders(cfg)))),
  getVideo: (cfg: ThetaConfig, videoId: string) => redacted(getJson(('' + String(BASE) + '/video/' + String(pathSegment(videoId,'videoId'))), net(cfg, videoHeaders(cfg)))),
  listVideos: (cfg: ThetaConfig, serviceAccountId: string, page = 1, number = 10) =>
    redacted(getJson(('' + String(BASE) + '/video/' + String(pathSegment(serviceAccountId,'serviceAccountId')) + '/list?' + String(new URLSearchParams({page:String(page),number:String(number)}))), net(cfg, videoHeaders(cfg)))),
  // Stream responses carry the livestream key; it is redacted here before returning.
  createStream: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) => redacted(assertApproved(cfg, confirm, 'theta.video.streamCreate') ?? postJson(('' + String(BASE) + '/stream'), payload, net(cfg, videoHeaders(cfg)))),
  getStream: (cfg: ThetaConfig, streamId: string) => redacted(getJson(('' + String(BASE) + '/stream/' + String(pathSegment(streamId,'streamId'))), net(cfg, videoHeaders(cfg)))),
  searchVideos: (cfg: ThetaConfig, serviceAccountId: string, filters: unknown, operator?: unknown, page?: unknown, number?: unknown) => {
    const query = videoSearchQuery(filters, operator, page, number);
    return redacted(getJson(('' + String(BASE) + '/video/' + String(pathSegment(serviceAccountId,'serviceAccountId')) + '/search?' + String(query)), net(cfg, videoHeaders(cfg))));
  },
  listStreams: (cfg: ThetaConfig, serviceAccountId: string, status?: unknown) => {
    if (status !== undefined && status !== 'on' && status !== 'off') throw new Error('status must be "on" or "off"');
    const query = status ? ('?' + String(new URLSearchParams({ status: status as string }))) : '';
    return redacted(getJson(('' + String(BASE) + '/service_account/' + String(pathSegment(serviceAccountId,'serviceAccountId')) + '/streams' + String(query)), net(cfg, videoHeaders(cfg))));
  },
  listIngestors: (cfg: ThetaConfig) => redacted(getJson(('' + String(BASE) + '/ingestor/filter'), net(cfg, videoHeaders(cfg)))),
  selectIngestor: (cfg: ThetaConfig, ingestorId: string, body: Record<string, unknown>, confirm?: boolean) =>
    redacted(assertApproved(cfg, confirm, 'theta.video.ingestorSelect') ?? putJson(('' + String(BASE) + '/ingestor/' + String(pathSegment(ingestorId,'ingestorId')) + '/select'), body, net(cfg, videoHeaders(cfg)))),
  // Frees the ingestor and invalidates the live stream key. Body is always exactly {}.
  unselectIngestor: (cfg: ThetaConfig, ingestorId: string, confirm?: boolean) =>
    redacted(assertApproved(cfg, confirm, 'theta.video.ingestorUnselect') ?? putJson(('' + String(BASE) + '/ingestor/' + String(pathSegment(ingestorId,'ingestorId')) + '/unselect'), {}, net(cfg, videoHeaders(cfg))))
};
