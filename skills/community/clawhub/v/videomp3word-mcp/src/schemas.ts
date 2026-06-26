import { z } from "zod";

export const OutputTypeSchema = z.enum(["summary", "qa", "flashcards", "tasks", "topics"]);
export const ExecutionModeSchema = z.enum(["fast", "balanced", "high_accuracy"]);
export const ExportFormatSchema = z.enum(["json", "markdown", "notion"]);

export const VideoToKnowledgeRequestSchema = z.object({
  media_url: z.string().url(),
  outputs: z.array(OutputTypeSchema).min(1),
  mode: ExecutionModeSchema.default("balanced"),
  export_formats: z.array(ExportFormatSchema).default(["json"]),
  metadata: z.record(z.unknown()).optional(),
});

export const ActionItemSchema = z.object({
  task: z.string(),
  owner: z.string(),
  deadline: z.string(),
});

export const QAPairSchema = z.object({
  question: z.string(),
  answer: z.string(),
});

export const FlashcardSchema = z.object({
  front: z.string(),
  back: z.string(),
});

export const EntitySchema = z.object({
  name: z.string(),
  type: z.string(),
});

export const WorkflowStepTraceSchema = z.object({
  step: z.string(),
  status: z.enum(["completed", "failed"]),
  attempt: z.number().int().min(1),
  duration_ms: z.number().nonnegative(),
  cached: z.boolean(),
  note: z.string().optional(),
});

export const TraceSchema = z.object({
  workflow_run_id: z.string(),
  steps: z.array(WorkflowStepTraceSchema),
  models_used: z.array(z.string()),
  chunk_references: z.array(z.string()),
  resource_ids: z.object({
    media_asset_id: z.string(),
    transcript_id: z.string(),
    knowledge_unit_id: z.string(),
  }),
});

export const KnowledgeResponseSchema = z.object({
  request_id: z.string(),
  mode: ExecutionModeSchema,
  requested_outputs: z.array(OutputTypeSchema),
  summary: z.string(),
  topics: z.array(z.string()),
  key_points: z.array(z.string()),
  action_items: z.array(ActionItemSchema),
  qa_pairs: z.array(QAPairSchema),
  flashcards: z.array(FlashcardSchema),
  entities: z.array(EntitySchema),
  confidence_scores: z.record(z.number()),
  trace: TraceSchema,
  exports: z.record(z.unknown()),
});

export type OutputType = z.infer<typeof OutputTypeSchema>;
export type ExecutionMode = z.infer<typeof ExecutionModeSchema>;
export type ExportFormat = z.infer<typeof ExportFormatSchema>;
export type VideoToKnowledgeRequest = z.infer<typeof VideoToKnowledgeRequestSchema>;
export type ActionItem = z.infer<typeof ActionItemSchema>;
export type QAPair = z.infer<typeof QAPairSchema>;
export type Flashcard = z.infer<typeof FlashcardSchema>;
export type Entity = z.infer<typeof EntitySchema>;
export type WorkflowStepTrace = z.infer<typeof WorkflowStepTraceSchema>;
export type KnowledgeResponse = z.infer<typeof KnowledgeResponseSchema>;
