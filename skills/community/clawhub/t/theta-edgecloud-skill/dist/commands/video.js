import { thetaVideoClient } from '../clients/thetaVideo.js';
export const video = {
    uploadCreate: (cfg) => cfg.dryRun ? { dryRun: true } : thetaVideoClient.createUploadSession(cfg),
    videoCreate: (cfg, payload) => cfg.dryRun ? { dryRun: true, payload } : thetaVideoClient.createVideo(cfg, payload),
    videoGet: (cfg, videoId) => thetaVideoClient.getVideo(cfg, videoId),
    videoList: (cfg, serviceAccountId, page = 1, number = 10) => thetaVideoClient.listVideos(cfg, serviceAccountId, page, number),
    streamCreate: (cfg, payload) => cfg.dryRun ? { dryRun: true, payload } : thetaVideoClient.createStream(cfg, payload),
    streamGet: (cfg, streamId) => thetaVideoClient.getStream(cfg, streamId),
    ingestorList: (cfg) => thetaVideoClient.listIngestors(cfg),
    ingestorSelect: (cfg, ingestorId, body) => cfg.dryRun ? { dryRun: true, ingestorId, body } : thetaVideoClient.selectIngestor(cfg, ingestorId, body)
};
