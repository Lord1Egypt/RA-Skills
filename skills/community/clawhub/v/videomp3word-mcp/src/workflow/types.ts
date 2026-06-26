import type { WorkflowStepTrace } from "../schemas.js";

export type StepOutcome<T = unknown> = {
  data: T;
  cached?: boolean;
  note?: string;
  modelsUsed?: string[];
  chunkReferences?: string[];
};

export type WorkflowState = {
  results: Record<string, unknown>;
  steps: WorkflowStepTrace[];
  modelsUsed: Set<string>;
  chunkReferences: Set<string>;
};

export type WorkflowNode<Context> = {
  id: string;
  deps: string[];
  retries?: number;
  handler: (context: Context, state: WorkflowState) => Promise<StepOutcome>;
};
