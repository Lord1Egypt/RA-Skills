import type { ExecutionPlan } from "./plannerAgent.js";
import { createId, sha256 } from "../utils/hash.js";
import type { PlatformRepository, TranscriptRecord } from "../storage/types.js";
import { UpstreamTranscriptionClient } from "../services/upstreamClient.js";

export class TranscriptionAgent {
  constructor(
    private readonly repository: PlatformRepository,
    private readonly upstreamClient: UpstreamTranscriptionClient,
  ) {}

  async execute(mediaAssetId: string, sourceUrl: string, plan: ExecutionPlan) {
    const cached = await this.repository.getTranscriptByFingerprint(mediaAssetId, plan.transcriptionFingerprint);
    if (cached) {
      return { transcript: cached, cached: true, modelUsed: [cached.model] };
    }

    const result = await this.upstreamClient.transcribe(sourceUrl, plan.modeProfile.mode);
    const now = new Date().toISOString();
    const transcript: TranscriptRecord = {
      id: createId("transcript"),
      mediaAssetId,
      sourceUrl: result.sourceUrl,
      transcriptionFingerprint: plan.transcriptionFingerprint,
      text: result.transcript,
      model: result.modelLabel,
      contentHash: sha256(result.transcript),
      createdAt: now,
      updatedAt: now,
      metadata: {
        route: result.route,
        kind: result.kind,
        execution_mode: plan.modeProfile.mode,
      },
    };

    await this.repository.upsertTranscript(transcript);
    return { transcript, cached: false, modelUsed: [transcript.model] };
  }
}
