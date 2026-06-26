import type { ServerConfig } from "../config.js";
import { createRepository } from "../storage/index.js";
import { PlannerAgent } from "../agents/plannerAgent.js";
import { TranscriptionAgent } from "../agents/transcriptionAgent.js";
import { SemanticAgent } from "../agents/semanticAgent.js";
import { KnowledgeAgent } from "../agents/knowledgeAgent.js";
import { EvaluationAgent } from "../agents/evaluationAgent.js";
import { UpstreamTranscriptionClient } from "../services/upstreamClient.js";
import { ModelClient } from "../services/modelClient.js";
import { ExportService } from "../services/exportService.js";
import { VideoToKnowledgePlatform } from "./videoToKnowledgePlatform.js";

export async function createPlatform(config: ServerConfig) {
  const repository = createRepository(config);
  const plannerAgent = new PlannerAgent();
  const transcriptionAgent = new TranscriptionAgent(repository, new UpstreamTranscriptionClient(config));
  const semanticAgent = new SemanticAgent(repository);
  const knowledgeAgent = new KnowledgeAgent(repository, new ModelClient(config));
  const evaluationAgent = new EvaluationAgent();
  const exportService = new ExportService();
  const platform = new VideoToKnowledgePlatform(
    config,
    repository,
    plannerAgent,
    transcriptionAgent,
    semanticAgent,
    knowledgeAgent,
    evaluationAgent,
    exportService,
  );
  await platform.initialize();
  return platform;
}
