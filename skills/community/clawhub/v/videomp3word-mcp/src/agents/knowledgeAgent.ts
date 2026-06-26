import type { ActionItem, Entity, Flashcard, KnowledgeResponse, QAPair } from "../schemas.js";
import { clipText, extractActionItems, splitIntoSentences, uniqueStrings } from "../utils/text.js";
import { createId } from "../utils/hash.js";
import type { PlatformRepository, KnowledgeUnitRecord, SemanticChunkRecord, TranscriptRecord } from "../storage/types.js";
import type { ExecutionPlan } from "./plannerAgent.js";
import { ModelClient } from "../services/modelClient.js";

type StructuredKnowledgeDraft = {
  summary?: string;
  topics?: string[];
  key_points?: string[];
  action_items?: ActionItem[];
  qa_pairs?: QAPair[];
  flashcards?: Flashcard[];
  entities?: Entity[];
};

export class KnowledgeAgent {
  constructor(
    private readonly repository: PlatformRepository,
    private readonly modelClient: ModelClient,
  ) {}

  async execute(transcript: TranscriptRecord, chunks: SemanticChunkRecord[], plan: ExecutionPlan) {
    const cached = await this.repository.getKnowledgeUnit(transcript.id, plan.requestHash);
    if (cached) {
      return { knowledgeUnit: cached, cached: true, modelUsed: cached.modelsUsed, chunkReferences: cached.chunkReferences };
    }

    const draft = await this.generateKnowledgeDraft(transcript, chunks, plan);
    const now = new Date().toISOString();
    const knowledgeUnit: KnowledgeUnitRecord = {
      id: createId("knowledge"),
      transcriptId: transcript.id,
      mediaAssetId: transcript.mediaAssetId,
      requestHash: plan.requestHash,
      mode: plan.modeProfile.mode,
      requestedOutputs: plan.requestedOutputs,
      result: {
        mode: plan.modeProfile.mode,
        requested_outputs: plan.requestedOutputs,
        summary: draft.summary || "",
        topics: draft.topics || [],
        key_points: draft.key_points || [],
        action_items: draft.action_items || [],
        qa_pairs: draft.qa_pairs || [],
        flashcards: draft.flashcards || [],
        entities: draft.entities || [],
        confidence_scores: {},
      },
      traceSteps: [],
      modelsUsed: [this.modelClient.isEnabled() ? "knowledge-model" : "heuristic-knowledge"],
      chunkReferences: chunks.map((chunk) => chunk.id),
      createdAt: now,
      updatedAt: now,
    };

    await this.repository.upsertKnowledgeUnit(knowledgeUnit);
    return { knowledgeUnit, cached: false, modelUsed: knowledgeUnit.modelsUsed, chunkReferences: knowledgeUnit.chunkReferences };
  }

  async persistEvaluation(knowledgeUnit: KnowledgeUnitRecord, updatedResult: Omit<KnowledgeResponse, "request_id" | "trace" | "exports">) {
    const updated: KnowledgeUnitRecord = {
      ...knowledgeUnit,
      result: updatedResult,
      updatedAt: new Date().toISOString(),
    };
    await this.repository.upsertKnowledgeUnit(updated);
    return updated;
  }

  private async generateKnowledgeDraft(transcript: TranscriptRecord, chunks: SemanticChunkRecord[], plan: ExecutionPlan): Promise<StructuredKnowledgeDraft> {
    const modelDraft = await this.tryModelDraft(transcript, chunks, plan);
    if (modelDraft) return this.sanitizeDraft(modelDraft, chunks, plan);
    return this.generateHeuristicDraft(transcript, chunks, plan);
  }

  private async tryModelDraft(transcript: TranscriptRecord, chunks: SemanticChunkRecord[], plan: ExecutionPlan): Promise<StructuredKnowledgeDraft | null> {
    if (!this.modelClient.isEnabled()) return null;

    const chunkContext = chunks.map((chunk) => `Chunk ${chunk.index + 1}: ${clipText(chunk.text, 600)}`).join("\n\n");
    const messages = [
      {
        role: "system" as const,
        content: "You are a structured knowledge extraction engine. Return JSON only. Preserve fidelity to the transcript and avoid fabrication. Use empty arrays or empty strings when a requested field has insufficient evidence.",
      },
      {
        role: "user" as const,
        content: [
          `Requested outputs: ${plan.requestedOutputs.join(", ")}`,
          `Execution mode: ${plan.modeProfile.mode}`,
          "Return this JSON shape exactly:",
          JSON.stringify({
            summary: "",
            topics: [],
            key_points: [],
            action_items: [{ task: "", owner: "", deadline: "" }],
            qa_pairs: [{ question: "", answer: "" }],
            flashcards: [{ front: "", back: "" }],
            entities: [{ name: "", type: "" }],
          }),
          "Transcript excerpt:",
          clipText(transcript.text, 8000),
          "Chunk context:",
          chunkContext,
        ].join("\n\n"),
      },
    ];
    return this.modelClient.generateJson<StructuredKnowledgeDraft>(messages, "qwen-plus");
  }

  private sanitizeDraft(draft: StructuredKnowledgeDraft, chunks: SemanticChunkRecord[], plan: ExecutionPlan): StructuredKnowledgeDraft {
    const entities = uniqueEntityList([...(draft.entities || []), ...chunks.flatMap((chunk) => chunk.entities)], 12);
    return {
      summary: typeof draft.summary === "string" ? draft.summary.trim() : "",
      topics: uniqueStrings(draft.topics || [], plan.modeProfile.maxTopics),
      key_points: uniqueStrings(draft.key_points || [], plan.modeProfile.maxKeyPoints),
      action_items: sanitizeActionItems(draft.action_items || []).slice(0, plan.modeProfile.maxKeyPoints),
      qa_pairs: sanitizeQaPairs(draft.qa_pairs || []).slice(0, plan.modeProfile.qaPairs),
      flashcards: sanitizeFlashcards(draft.flashcards || []).slice(0, plan.modeProfile.flashcards),
      entities,
    };
  }

  private generateHeuristicDraft(transcript: TranscriptRecord, chunks: SemanticChunkRecord[], plan: ExecutionPlan): StructuredKnowledgeDraft {
    const sentences = splitIntoSentences(transcript.text);
    const keywords = uniqueStrings(chunks.flatMap((chunk) => chunk.keywords), plan.modeProfile.maxTopics);
    const keyPoints = uniqueStrings(
      [
        ...chunks.slice(0, plan.modeProfile.maxKeyPoints).map((chunk) => clipText(chunk.text, 180)),
        ...sentences.filter((sentence) => /\b(decide|plan|important|because|need|will|must|should)\b/i.test(sentence)).map((sentence) => clipText(sentence, 180)),
      ],
      plan.modeProfile.maxKeyPoints,
    );
    const summary = keyPoints.slice(0, Math.max(3, Math.min(5, keyPoints.length))).join(" ") || clipText(transcript.text, 320);
    const actionItems = extractActionItems(sentences, plan.modeProfile.maxKeyPoints);
    const qaPairs = buildQaPairs(keywords, keyPoints, plan.modeProfile.qaPairs);
    const flashcards = buildFlashcards(keywords, keyPoints, plan.modeProfile.flashcards);
    const entities = uniqueEntityList(chunks.flatMap((chunk) => chunk.entities), 12);

    return {
      summary,
      topics: keywords,
      key_points: keyPoints,
      action_items: plan.requestedOutputs.includes("tasks") ? actionItems : [],
      qa_pairs: plan.requestedOutputs.includes("qa") ? qaPairs : [],
      flashcards: plan.requestedOutputs.includes("flashcards") ? flashcards : [],
      entities,
    };
  }
}

function uniqueEntityList(values: Entity[], limit: number): Entity[] {
  const seen = new Set<string>();
  const output: Entity[] = [];
  for (const entity of values) {
    const key = `${entity.name.toLowerCase()}:${entity.type.toLowerCase()}`;
    if (seen.has(key)) continue;
    seen.add(key);
    output.push(entity);
    if (output.length >= limit) break;
  }
  return output;
}

function sanitizeActionItems(values: ActionItem[]): ActionItem[] {
  return values
    .filter((value) => value && typeof value.task === "string")
    .map((value) => ({
      task: value.task.trim(),
      owner: (value.owner || "unassigned").trim() || "unassigned",
      deadline: (value.deadline || "unspecified").trim() || "unspecified",
    }))
    .filter((value) => Boolean(value.task));
}

function sanitizeQaPairs(values: QAPair[]): QAPair[] {
  return values
    .filter((value) => value && typeof value.question === "string" && typeof value.answer === "string")
    .map((value) => ({ question: value.question.trim(), answer: value.answer.trim() }))
    .filter((value) => Boolean(value.question) && Boolean(value.answer));
}

function sanitizeFlashcards(values: Flashcard[]): Flashcard[] {
  return values
    .filter((value) => value && typeof value.front === "string" && typeof value.back === "string")
    .map((value) => ({ front: value.front.trim(), back: value.back.trim() }))
    .filter((value) => Boolean(value.front) && Boolean(value.back));
}

function buildQaPairs(topics: string[], keyPoints: string[], limit: number): QAPair[] {
  const outputs: QAPair[] = [];
  for (let index = 0; index < Math.min(limit, topics.length); index += 1) {
    outputs.push({
      question: `What does the transcript say about ${topics[index]}?`,
      answer: keyPoints[index] || `The transcript treats ${topics[index]} as a core topic.`,
    });
  }
  return outputs;
}

function buildFlashcards(topics: string[], keyPoints: string[], limit: number): Flashcard[] {
  const outputs: Flashcard[] = [];
  for (let index = 0; index < Math.min(limit, Math.max(topics.length, keyPoints.length)); index += 1) {
    outputs.push({
      front: topics[index] ? `Explain ${topics[index]}` : `Key point ${index + 1}`,
      back: keyPoints[index] || `Review the transcript discussion for item ${index + 1}.`,
    });
  }
  return outputs;
}
