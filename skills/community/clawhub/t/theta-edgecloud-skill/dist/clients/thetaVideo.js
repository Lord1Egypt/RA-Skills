import { getJson, postJson, putJson } from './http.js';
const BASE = 'https://api.thetavideoapi.com';
function h(cfg) {
    if (!cfg.videoSaId || !cfg.videoSaSecret)
        throw new Error('THETA_VIDEO_SA_ID / THETA_VIDEO_SA_SECRET missing');
    return { 'x-tva-sa-id': cfg.videoSaId, 'x-tva-sa-secret': cfg.videoSaSecret };
}
function net(cfg, headers) {
    return {
        headers,
        service: 'theta-video',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
export const thetaVideoClient = {
    createUploadSession: (cfg) => postJson(`${BASE}/upload`, {}, net(cfg, h(cfg))),
    createVideo: (cfg, payload) => postJson(`${BASE}/video`, payload, net(cfg, h(cfg))),
    getVideo: (cfg, videoId) => getJson(`${BASE}/video/${videoId}`, net(cfg, h(cfg))),
    listVideos: (cfg, serviceAccountId, page = 1, number = 10) => getJson(`${BASE}/video/${serviceAccountId}/list?page=${page}&number=${number}`, net(cfg, h(cfg))),
    createStream: (cfg, payload) => postJson(`${BASE}/stream`, payload, net(cfg, h(cfg))),
    getStream: (cfg, streamId) => getJson(`${BASE}/stream/${streamId}`, net(cfg, h(cfg))),
    listIngestors: (cfg) => getJson(`${BASE}/ingestor/filter`, net(cfg, h(cfg))),
    selectIngestor: (cfg, ingestorId, body) => putJson(`${BASE}/ingestor/${ingestorId}/select`, body, net(cfg, h(cfg)))
};
