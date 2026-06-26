/**
 * Trace Compiler — converts a recorded OpenClaw session trace
 * into a reusable Lobster workflow.
 *
 * This is the core "one node explores, all nodes benefit" engine.
 * It takes the raw action history from a successful session and
 * compiles it into a parameterized, portable Lobster workflow.
 */
import type { ActionTrace, LobsterWorkflow } from "./types.js";
export interface CompileResult {
    workflow: LobsterWorkflow;
    argCount: number;
}
export declare function compileTrace(intentName: string, actions: ActionTrace[]): CompileResult;
