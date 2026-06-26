import { logger } from "../logger.js";
import type { PlatformRepository, WorkflowRunRecord } from "../storage/types.js";
import type { WorkflowNode, WorkflowState } from "./types.js";

export class WorkflowExecutor<Context> {
  constructor(private readonly repository: PlatformRepository) {}

  async execute(nodes: WorkflowNode<Context>[], context: Context, run: WorkflowRunRecord): Promise<WorkflowState> {
    const state: WorkflowState = {
      results: {},
      steps: [],
      modelsUsed: new Set<string>(),
      chunkReferences: new Set<string>(),
    };

    const pending = new Map(nodes.map((node) => [node.id, node]));

    while (pending.size > 0) {
      const ready = [...pending.values()].filter((node) => node.deps.every((dependency) => dependency in state.results));
      if (ready.length === 0) {
        throw new Error("Workflow graph contains a cycle or unresolved dependency.");
      }

      for (const node of ready) {
        pending.delete(node.id);
        const maxAttempts = Math.max(1, node.retries ?? 1);
        let attempt = 0;
        while (attempt < maxAttempts) {
          attempt += 1;
          const startedAt = Date.now();
          try {
            logger.info("workflow.step.start", { workflowRunId: run.id, step: node.id, attempt });
            const outcome = await node.handler(context, state);
            const trace = {
              step: node.id,
              status: "completed" as const,
              attempt,
              duration_ms: Date.now() - startedAt,
              cached: Boolean(outcome.cached),
              note: outcome.note,
            };
            state.results[node.id] = outcome.data;
            state.steps.push(trace);
            outcome.modelsUsed?.forEach((model) => state.modelsUsed.add(model));
            outcome.chunkReferences?.forEach((chunkId) => state.chunkReferences.add(chunkId));
            run.steps = [...state.steps];
            run.updatedAt = new Date().toISOString();
            await this.repository.updateWorkflowRun(run);
            logger.info("workflow.step.complete", { workflowRunId: run.id, step: node.id, attempt, cached: Boolean(outcome.cached) });
            break;
          } catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            logger.warn("workflow.step.failure", { workflowRunId: run.id, step: node.id, attempt, message });
            if (attempt >= maxAttempts) {
              const trace = {
                step: node.id,
                status: "failed" as const,
                attempt,
                duration_ms: Date.now() - startedAt,
                cached: false,
                note: message,
              };
              state.steps.push(trace);
              run.status = "failed";
              run.errorMessage = message;
              run.steps = [...state.steps];
              run.updatedAt = new Date().toISOString();
              await this.repository.updateWorkflowRun(run);
              throw error;
            }
          }
        }
      }
    }

    return state;
  }
}
