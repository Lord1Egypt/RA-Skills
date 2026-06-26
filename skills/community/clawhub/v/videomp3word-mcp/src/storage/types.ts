import type { ExecutionMode, KnowledgeResponse, OutputType, WorkflowStepTrace } from "../schemas.js";

export type StorageDriver = "memory" | "mongodb";

export type MediaAssetRecord = {
  id: string;
  sourceUrl: string;
  normalizedSourceUrl: string;
  kind: "audio" | "video" | "unknown";
  createdAt: string;
  updatedAt: string;
  metadata: Record<string, unknown>;
};

export type TranscriptRecord = {
  id: string;
  mediaAssetId: string;
  sourceUrl: string;
  transcriptionFingerprint: string;
  text: string;
  model: string;
  contentHash: string;
  createdAt: string;
  updatedAt: string;
  metadata: Record<string, unknown>;
};

export type SemanticChunkRecord = {
  id: string;
  transcriptId: string;
  mediaAssetId: string;
  index: number;
  text: string;
  chunkConfigHash: string;
  embeddingModel: string;
  embedding: number[];
  keywords: string[];
  entities: Array<{ name: string; type: string }>;
  createdAt: string;
  updatedAt: string;
};

export type KnowledgeUnitRecord = {
  id: string;
  transcriptId: string;
  mediaAssetId: string;
  requestHash: string;
  mode: ExecutionMode;
  requestedOutputs: OutputType[];
  result: Omit<KnowledgeResponse, "request_id" | "trace" | "exports"> & { request_id?: string };
  traceSteps: WorkflowStepTrace[];
  modelsUsed: string[];
  chunkReferences: string[];
  createdAt: string;
  updatedAt: string;
};

export type WorkflowRunRecord = {
  id: string;
  workflowType: string;
  requestHash: string;
  mediaAssetId?: string;
  status: "running" | "completed" | "failed";
  steps: WorkflowStepTrace[];
  createdAt: string;
  updatedAt: string;
  errorMessage?: string;
};

export interface PlatformRepository {
  readonly driver: StorageDriver;
  ensureIndexes(): Promise<void>;
  getMediaAssetBySource(sourceUrl: string): Promise<MediaAssetRecord | null>;
  upsertMediaAsset(record: MediaAssetRecord): Promise<MediaAssetRecord>;
  getTranscriptByFingerprint(mediaAssetId: string, transcriptionFingerprint: string): Promise<TranscriptRecord | null>;
  upsertTranscript(record: TranscriptRecord): Promise<TranscriptRecord>;
  getSemanticChunks(transcriptId: string, chunkConfigHash: string): Promise<SemanticChunkRecord[]>;
  replaceSemanticChunks(records: SemanticChunkRecord[]): Promise<SemanticChunkRecord[]>;
  getKnowledgeUnit(transcriptId: string, requestHash: string): Promise<KnowledgeUnitRecord | null>;
  upsertKnowledgeUnit(record: KnowledgeUnitRecord): Promise<KnowledgeUnitRecord>;
  createWorkflowRun(record: WorkflowRunRecord): Promise<WorkflowRunRecord>;
  updateWorkflowRun(record: WorkflowRunRecord): Promise<void>;
}
