#!/usr/bin/env node
/**
 * @zouroboros/autoloop — Autonomous single-metric optimization loop
 *
 * Reads a program.md, creates a git branch, and loops:
 *   propose change → commit → run experiment → measure metric → keep or revert
 *
 * Inspired by karpathy/autoresearch. Generalized for any single-metric task.
 *
 * @license MIT
 */
interface ProgramConfig {
    name: string;
    objective: string;
    metric: {
        name: string;
        direction: "lower_is_better" | "higher_is_better";
        extract: string;
    };
    setup: string;
    targetFile: string;
    runCommand: string;
    readOnlyFiles: string[];
    constraints: {
        timeBudgetSeconds: number;
        maxExperiments: number;
        maxDurationHours: number;
        maxCostUSD: number;
    };
    stagnation: {
        threshold: number;
        doubleThreshold: number;
        tripleThreshold: number;
    };
    notes: string;
}
interface ExperimentRecord {
    commit: string;
    metric: number;
    status: "keep" | "discard" | "crash";
    description: string;
    timestamp: string;
    durationMs: number;
}
declare function parseProgram(path: string): ProgramConfig;

export { type ExperimentRecord, type ProgramConfig, parseProgram };
