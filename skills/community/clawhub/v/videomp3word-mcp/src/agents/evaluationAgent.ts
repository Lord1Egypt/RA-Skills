import type { KnowledgeResponse } from "../schemas.js";
import type { SemanticChunkRecord, TranscriptRecord } from "../storage/types.js";
import type { ExecutionPlan } from "./plannerAgent.js";

export class EvaluationAgent {
  evaluate(
    transcript: TranscriptRecord,
    chunks: SemanticChunkRecord[],
    payload: Omit<KnowledgeResponse, "request_id" | "trace" | "exports">,
    plan: ExecutionPlan,
  ): Record<string, number> {
    const transcriptLength = Math.max(1, transcript.text.length);
    const summaryCoverage = Math.min(1, payload.summary.length / Math.min(400, transcriptLength));
    const topicCoverage = Math.min(1, payload.topics.length / Math.max(1, plan.modeProfile.maxTopics));
    const keyPointCoverage = Math.min(1, payload.key_points.length / Math.max(1, plan.modeProfile.maxKeyPoints));
    const entityCoverage = Math.min(1, payload.entities.length / 6);
    const qaCoverage = plan.requestedOutputs.includes("qa") ? Math.min(1, payload.qa_pairs.length / Math.max(1, plan.modeProfile.qaPairs)) : 1;
    const flashcardCoverage = plan.requestedOutputs.includes("flashcards") ? Math.min(1, payload.flashcards.length / Math.max(1, plan.modeProfile.flashcards)) : 1;
    const taskCoverage = plan.requestedOutputs.includes("tasks") ? Math.min(1, payload.action_items.length / Math.max(1, Math.min(4, plan.modeProfile.maxKeyPoints))) : 1;
    const chunkCoverage = Math.min(1, chunks.length / 3);
    const overall = Number(((summaryCoverage + topicCoverage + keyPointCoverage + entityCoverage + qaCoverage + flashcardCoverage + taskCoverage + chunkCoverage) / 8).toFixed(4));

    return {
      overall,
      summary: Number(summaryCoverage.toFixed(4)),
      topics: Number(topicCoverage.toFixed(4)),
      key_points: Number(keyPointCoverage.toFixed(4)),
      entities: Number(entityCoverage.toFixed(4)),
      qa_pairs: Number(qaCoverage.toFixed(4)),
      flashcards: Number(flashcardCoverage.toFixed(4)),
      action_items: Number(taskCoverage.toFixed(4)),
      chunk_coverage: Number(chunkCoverage.toFixed(4)),
    };
  }
}
