import { chunkText, buildHashEmbedding, detectEntities, extractKeywords } from "../utils/text.js";
import { deterministicId } from "../utils/hash.js";
import type { PlatformRepository, SemanticChunkRecord, TranscriptRecord } from "../storage/types.js";
import type { ExecutionPlan } from "./plannerAgent.js";

export class SemanticAgent {
  constructor(private readonly repository: PlatformRepository) {}

  async segmentTranscript(transcript: TranscriptRecord, plan: ExecutionPlan) {
    const existing = await this.repository.getSemanticChunks(transcript.id, plan.chunkConfigHash);
    if (existing.length > 0) return { chunks: existing, cached: true };

    const now = new Date().toISOString();
    const chunks = chunkText(transcript.text, plan.modeProfile.chunkSize).map((text, index) => ({
      id: deterministicId("chunk", `${transcript.id}:${plan.chunkConfigHash}:${index}`),
      transcriptId: transcript.id,
      mediaAssetId: transcript.mediaAssetId,
      index,
      text,
      chunkConfigHash: plan.chunkConfigHash,
      embeddingModel: "hash-embedding:v1",
      embedding: [],
      keywords: [],
      entities: [],
      createdAt: now,
      updatedAt: now,
    } satisfies SemanticChunkRecord));

    await this.repository.replaceSemanticChunks(chunks);
    return { chunks, cached: false };
  }

  async enrichChunks(transcript: TranscriptRecord, plan: ExecutionPlan) {
    const existing = await this.repository.getSemanticChunks(transcript.id, plan.chunkConfigHash);
    if (existing.length === 0) {
      throw new Error("Semantic chunks are missing for transcript enrichment.");
    }
    if (existing.every((chunk) => chunk.embedding.length > 0)) {
      return { chunks: existing, cached: true };
    }

    const now = new Date().toISOString();
    const enriched = existing.map((chunk) => ({
      ...chunk,
      embedding: buildHashEmbedding(chunk.text),
      keywords: extractKeywords(chunk.text, 5),
      entities: detectEntities(chunk.text, 6),
      updatedAt: now,
    }));
    await this.repository.replaceSemanticChunks(enriched);
    return { chunks: enriched, cached: false };
  }
}
