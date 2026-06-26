import type {
  KnowledgeUnitRecord,
  MediaAssetRecord,
  PlatformRepository,
  SemanticChunkRecord,
  TranscriptRecord,
  WorkflowRunRecord,
} from "./types.js";

export class MemoryRepository implements PlatformRepository {
  readonly driver = "memory" as const;

  private readonly mediaAssets = new Map<string, MediaAssetRecord>();
  private readonly transcripts = new Map<string, TranscriptRecord>();
  private readonly semanticChunks = new Map<string, SemanticChunkRecord[]>();
  private readonly knowledgeUnits = new Map<string, KnowledgeUnitRecord>();
  private readonly workflowRuns = new Map<string, WorkflowRunRecord>();

  async ensureIndexes(): Promise<void> {
    return;
  }

  async getMediaAssetBySource(sourceUrl: string): Promise<MediaAssetRecord | null> {
    for (const record of this.mediaAssets.values()) {
      if (record.normalizedSourceUrl === sourceUrl) return record;
    }
    return null;
  }

  async upsertMediaAsset(record: MediaAssetRecord): Promise<MediaAssetRecord> {
    this.mediaAssets.set(record.id, record);
    return record;
  }

  async getTranscriptByFingerprint(mediaAssetId: string, transcriptionFingerprint: string): Promise<TranscriptRecord | null> {
    for (const record of this.transcripts.values()) {
      if (record.mediaAssetId === mediaAssetId && record.transcriptionFingerprint === transcriptionFingerprint) {
        return record;
      }
    }
    return null;
  }

  async upsertTranscript(record: TranscriptRecord): Promise<TranscriptRecord> {
    this.transcripts.set(record.id, record);
    return record;
  }

  async getSemanticChunks(transcriptId: string, chunkConfigHash: string): Promise<SemanticChunkRecord[]> {
    return this.semanticChunks.get(`${transcriptId}:${chunkConfigHash}`) || [];
  }

  async replaceSemanticChunks(records: SemanticChunkRecord[]): Promise<SemanticChunkRecord[]> {
    if (records.length === 0) return [];
    this.semanticChunks.set(`${records[0].transcriptId}:${records[0].chunkConfigHash}`, records);
    return records;
  }

  async getKnowledgeUnit(transcriptId: string, requestHash: string): Promise<KnowledgeUnitRecord | null> {
    return this.knowledgeUnits.get(`${transcriptId}:${requestHash}`) || null;
  }

  async upsertKnowledgeUnit(record: KnowledgeUnitRecord): Promise<KnowledgeUnitRecord> {
    this.knowledgeUnits.set(`${record.transcriptId}:${record.requestHash}`, record);
    return record;
  }

  async createWorkflowRun(record: WorkflowRunRecord): Promise<WorkflowRunRecord> {
    this.workflowRuns.set(record.id, record);
    return record;
  }

  async updateWorkflowRun(record: WorkflowRunRecord): Promise<void> {
    this.workflowRuns.set(record.id, record);
  }
}
