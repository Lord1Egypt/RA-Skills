import { MongoClient, type Collection } from "mongodb";
import type {
  KnowledgeUnitRecord,
  MediaAssetRecord,
  PlatformRepository,
  SemanticChunkRecord,
  TranscriptRecord,
  WorkflowRunRecord,
} from "./types.js";

type WithMongoId<T extends { id: string }> = Omit<T, "id"> & { _id: string };

function toMongo<T extends { id: string }>(record: T): WithMongoId<T> {
  const { id, ...rest } = record;
  return { _id: id, ...rest };
}

function fromMongo<T extends { _id: string }>(record: T | null): (Omit<T, "_id"> & { id: string }) | null {
  if (!record) return null;
  const { _id, ...rest } = record;
  return { id: _id, ...rest };
}

export class MongoRepository implements PlatformRepository {
  readonly driver = "mongodb" as const;

  private readonly client: MongoClient;
  private readonly mediaAssets: Collection<WithMongoId<MediaAssetRecord>>;
  private readonly transcripts: Collection<WithMongoId<TranscriptRecord>>;
  private readonly semanticChunks: Collection<WithMongoId<SemanticChunkRecord>>;
  private readonly knowledgeUnits: Collection<WithMongoId<KnowledgeUnitRecord>>;
  private readonly workflowRuns: Collection<WithMongoId<WorkflowRunRecord>>;

  constructor(uri: string, dbName: string) {
    this.client = new MongoClient(uri);
    const db = this.client.db(dbName);
    this.mediaAssets = db.collection("media_assets");
    this.transcripts = db.collection("transcripts");
    this.semanticChunks = db.collection("semantic_chunks");
    this.knowledgeUnits = db.collection("knowledge_units");
    this.workflowRuns = db.collection("workflow_runs");
  }

  async ensureIndexes(): Promise<void> {
    await this.client.connect();
    await Promise.all([
      this.mediaAssets.createIndexes([{ key: { normalizedSourceUrl: 1 }, name: "media_assets_by_source", unique: true }]),
      this.transcripts.createIndexes([{ key: { mediaAssetId: 1, transcriptionFingerprint: 1 }, name: "transcripts_by_fingerprint", unique: true }]),
      this.semanticChunks.createIndexes([{ key: { transcriptId: 1, chunkConfigHash: 1, index: 1 }, name: "semantic_chunks_by_transcript", unique: true }]),
      this.knowledgeUnits.createIndexes([{ key: { transcriptId: 1, requestHash: 1 }, name: "knowledge_units_by_request", unique: true }]),
      this.workflowRuns.createIndexes([{ key: { requestHash: 1, createdAt: -1 }, name: "workflow_runs_by_request" }]),
    ]);
  }

  async getMediaAssetBySource(sourceUrl: string): Promise<MediaAssetRecord | null> {
    return fromMongo(await this.mediaAssets.findOne({ normalizedSourceUrl: sourceUrl })) as MediaAssetRecord | null;
  }

  async upsertMediaAsset(record: MediaAssetRecord): Promise<MediaAssetRecord> {
    await this.mediaAssets.replaceOne({ _id: record.id }, toMongo(record), { upsert: true });
    return record;
  }

  async getTranscriptByFingerprint(mediaAssetId: string, transcriptionFingerprint: string): Promise<TranscriptRecord | null> {
    return fromMongo(await this.transcripts.findOne({ mediaAssetId, transcriptionFingerprint })) as TranscriptRecord | null;
  }

  async upsertTranscript(record: TranscriptRecord): Promise<TranscriptRecord> {
    await this.transcripts.replaceOne({ _id: record.id }, toMongo(record), { upsert: true });
    return record;
  }

  async getSemanticChunks(transcriptId: string, chunkConfigHash: string): Promise<SemanticChunkRecord[]> {
    const records = await this.semanticChunks.find({ transcriptId, chunkConfigHash }).sort({ index: 1 }).toArray();
    return records
      .map((record): SemanticChunkRecord => fromMongo(record as WithMongoId<SemanticChunkRecord>) as SemanticChunkRecord)
      .filter(Boolean);
  }

  async replaceSemanticChunks(records: SemanticChunkRecord[]): Promise<SemanticChunkRecord[]> {
    if (records.length === 0) return [];
    await this.semanticChunks.deleteMany({ transcriptId: records[0].transcriptId, chunkConfigHash: records[0].chunkConfigHash });
    await this.semanticChunks.insertMany(records.map((record) => toMongo(record)));
    return records;
  }

  async getKnowledgeUnit(transcriptId: string, requestHash: string): Promise<KnowledgeUnitRecord | null> {
    return fromMongo(await this.knowledgeUnits.findOne({ transcriptId, requestHash })) as KnowledgeUnitRecord | null;
  }

  async upsertKnowledgeUnit(record: KnowledgeUnitRecord): Promise<KnowledgeUnitRecord> {
    await this.knowledgeUnits.replaceOne({ _id: record.id }, toMongo(record), { upsert: true });
    return record;
  }

  async createWorkflowRun(record: WorkflowRunRecord): Promise<WorkflowRunRecord> {
    await this.workflowRuns.insertOne(toMongo(record));
    return record;
  }

  async updateWorkflowRun(record: WorkflowRunRecord): Promise<void> {
    await this.workflowRuns.replaceOne({ _id: record.id }, toMongo(record), { upsert: true });
  }
}
