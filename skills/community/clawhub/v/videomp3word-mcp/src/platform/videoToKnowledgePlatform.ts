import type { ServerConfig } from "../config.js";
import type { KnowledgeResponse, VideoToKnowledgeRequest } from "../schemas.js";
import { VideoToKnowledgeRequestSchema } from "../schemas.js";
import { logger } from "../logger.js";
import { createId, sha256 } from "../utils/hash.js";
import type { MediaAssetRecord, PlatformRepository, WorkflowRunRecord } from "../storage/types.js";
import { WorkflowExecutor } from "../workflow/executor.js";
import type { WorkflowNode } from "../workflow/types.js";
import { PlannerAgent } from "../agents/plannerAgent.js";
import { TranscriptionAgent } from "../agents/transcriptionAgent.js";
import { SemanticAgent } from "../agents/semanticAgent.js";
import { KnowledgeAgent } from "../agents/knowledgeAgent.js";
import { EvaluationAgent } from "../agents/evaluationAgent.js";
import { ExportService } from "../services/exportService.js";

type ExecutionContext = {
  requestId: string;
  request: VideoToKnowledgeRequest;
  mediaAsset?: MediaAssetRecord;
};

export class VideoToKnowledgePlatform {
  private readonly workflowExecutor: WorkflowExecutor<ExecutionContext>;

  constructor(
    private readonly config: ServerConfig,
    private readonly repository: PlatformRepository,
    private readonly plannerAgent: PlannerAgent,
    private readonly transcriptionAgent: TranscriptionAgent,
    private readonly semanticAgent: SemanticAgent,
    private readonly knowledgeAgent: KnowledgeAgent,
    private readonly evaluationAgent: EvaluationAgent,
    private readonly exportService: ExportService,
  ) {
    this.workflowExecutor = new WorkflowExecutor<ExecutionContext>(repository);
  }

  async initialize() {
    await this.repository.ensureIndexes();
    logger.info("platform.initialized", { storageDriver: this.repository.driver, baseUrl: this.config.baseUrl });
  }

  getModeProfiles() {
    return this.plannerAgent.getModeProfiles();
  }

  async run(input: VideoToKnowledgeRequest): Promise<KnowledgeResponse> {
    const request = VideoToKnowledgeRequestSchema.parse(input);
    const requestId = createId("request");
    const plan = this.plannerAgent.plan(request);
    const workflowRun: WorkflowRunRecord = {
      id: createId("workflow"),
      workflowType: "video_to_knowledge",
      requestHash: plan.requestHash,
      status: "running",
      steps: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    await this.repository.createWorkflowRun(workflowRun);

    const context: ExecutionContext = { requestId, request };

    const nodes: WorkflowNode<ExecutionContext>[] = [
      {
        id: "ingest_media",
        deps: [],
        retries: 1,
        handler: async (ctx) => {
          const normalizedSourceUrl = new URL(request.media_url).toString();
          const existing = await this.repository.getMediaAssetBySource(normalizedSourceUrl);
          if (existing) {
            ctx.mediaAsset = existing;
            workflowRun.mediaAssetId = existing.id;
            return {
              data: existing,
              cached: true,
              note: "Media asset restored from persistence.",
              modelsUsed: [plan.modeProfile.modelLabels.planning],
            };
          }

          const now = new Date().toISOString();
          const pathname = new URL(normalizedSourceUrl).pathname.toLowerCase();
          const kind = /\.(mp3|wav|m4a|aac|flac|ogg|opus|wma)$/.test(pathname)
            ? "audio"
            : /\.(mp4|mov|avi|mkv|webm|mpeg|mpg|wmv)$/.test(pathname)
            ? "video"
            : "unknown";
          const mediaAsset: MediaAssetRecord = {
            id: createId("media"),
            sourceUrl: normalizedSourceUrl,
            normalizedSourceUrl,
            kind,
            createdAt: now,
            updatedAt: now,
            metadata: {
              source_host: new URL(normalizedSourceUrl).hostname,
              request_hash: sha256(normalizedSourceUrl),
            },
          };
          await this.repository.upsertMediaAsset(mediaAsset);
          ctx.mediaAsset = mediaAsset;
          workflowRun.mediaAssetId = mediaAsset.id;
          return {
            data: mediaAsset,
            cached: false,
            note: "Media asset persisted.",
            modelsUsed: [plan.modeProfile.modelLabels.planning],
          };
        },
      },
      {
        id: "transcribe_media",
        deps: ["ingest_media"],
        retries: 2,
        handler: async (ctx) => {
          const mediaAsset = ctx.mediaAsset!;
          const result = await this.transcriptionAgent.execute(mediaAsset.id, mediaAsset.sourceUrl, plan);
          return {
            data: result.transcript,
            cached: result.cached,
            note: result.cached ? "Transcript cache hit." : "Transcript generated from upstream media pipeline.",
            modelsUsed: result.modelUsed,
          };
        },
      },
      {
        id: "segment_transcript",
        deps: ["transcribe_media"],
        retries: 1,
        handler: async (_ctx, state) => {
          const transcript = state.results.transcribe_media as Awaited<ReturnType<TranscriptionAgent["execute"]>>["transcript"];
          const result = await this.semanticAgent.segmentTranscript(transcript, plan);
          return {
            data: result.chunks,
            cached: result.cached,
            note: result.cached ? "Semantic chunks reused from persistence." : "Transcript segmented into semantic chunks.",
            chunkReferences: result.chunks.map((chunk) => chunk.id),
            modelsUsed: [plan.modeProfile.modelLabels.semantic],
          };
        },
      },
      {
        id: "extract_semantics",
        deps: ["segment_transcript"],
        retries: 1,
        handler: async (_ctx, state) => {
          const transcript = state.results.transcribe_media as Awaited<ReturnType<TranscriptionAgent["execute"]>>["transcript"];
          const result = await this.semanticAgent.enrichChunks(transcript, plan);
          return {
            data: result.chunks,
            cached: result.cached,
            note: result.cached ? "Semantic enrichment cache hit." : "Embeddings, keywords, and entities generated.",
            chunkReferences: result.chunks.map((chunk) => chunk.id),
            modelsUsed: [plan.modeProfile.modelLabels.semantic, "hash-embedding:v1"],
          };
        },
      },
      {
        id: "generate_knowledge",
        deps: ["transcribe_media", "extract_semantics"],
        retries: 1,
        handler: async (_ctx, state) => {
          const transcript = state.results.transcribe_media as Awaited<ReturnType<TranscriptionAgent["execute"]>>["transcript"];
          const chunks = state.results.extract_semantics as Awaited<ReturnType<SemanticAgent["enrichChunks"]>>["chunks"];
          const result = await this.knowledgeAgent.execute(transcript, chunks, plan);
          return {
            data: result.knowledgeUnit,
            cached: result.cached,
            note: result.cached ? "Structured knowledge restored from persistence." : "Structured knowledge unit generated.",
            modelsUsed: result.modelUsed,
            chunkReferences: result.chunkReferences,
          };
        },
      },
      {
        id: "evaluate_knowledge",
        deps: ["transcribe_media", "extract_semantics", "generate_knowledge"],
        retries: 1,
        handler: async (_ctx, state) => {
          const transcript = state.results.transcribe_media as Awaited<ReturnType<TranscriptionAgent["execute"]>>["transcript"];
          const chunks = state.results.extract_semantics as Awaited<ReturnType<SemanticAgent["enrichChunks"]>>["chunks"];
          const knowledgeUnit = state.results.generate_knowledge as Awaited<ReturnType<KnowledgeAgent["execute"]>>["knowledgeUnit"];
          const scored = {
            ...knowledgeUnit.result,
            confidence_scores: this.evaluationAgent.evaluate(transcript, chunks, knowledgeUnit.result, plan),
          };
          const updated = await this.knowledgeAgent.persistEvaluation(knowledgeUnit, scored);
          return {
            data: updated,
            cached: false,
            note: "Evaluation scores computed and persisted.",
            modelsUsed: [plan.modeProfile.modelLabels.evaluation],
            chunkReferences: updated.chunkReferences,
          };
        },
      },
    ];

    const workflowState = await this.workflowExecutor.execute(nodes, context, workflowRun);
    workflowRun.status = "completed";
    workflowRun.updatedAt = new Date().toISOString();
    await this.repository.updateWorkflowRun(workflowRun);

    const evaluatedKnowledge = workflowState.results.evaluate_knowledge as Awaited<ReturnType<KnowledgeAgent["persistEvaluation"]>>;
    const responseWithoutExports = {
      request_id: requestId,
      mode: plan.modeProfile.mode,
      requested_outputs: plan.requestedOutputs,
      summary: evaluatedKnowledge.result.summary,
      topics: evaluatedKnowledge.result.topics,
      key_points: evaluatedKnowledge.result.key_points,
      action_items: evaluatedKnowledge.result.action_items,
      qa_pairs: evaluatedKnowledge.result.qa_pairs,
      flashcards: evaluatedKnowledge.result.flashcards,
      entities: evaluatedKnowledge.result.entities,
      confidence_scores: evaluatedKnowledge.result.confidence_scores,
      trace: {
        workflow_run_id: workflowRun.id,
        steps: workflowState.steps,
        models_used: [...workflowState.modelsUsed],
        chunk_references: [...workflowState.chunkReferences],
        resource_ids: {
          media_asset_id: context.mediaAsset!.id,
          transcript_id: evaluatedKnowledge.transcriptId,
          knowledge_unit_id: evaluatedKnowledge.id,
        },
      },
    };

    return {
      ...responseWithoutExports,
      exports: this.exportService.buildExports(responseWithoutExports, request.export_formats),
    };
  }
}
