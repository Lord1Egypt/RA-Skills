import type { ExecutionPlan } from '../types/executionPlan';
export declare function getExecutionPlansPath(): string;
export declare function loadExecutionPlans(): ExecutionPlan[];
export declare function saveExecutionPlan(plan: ExecutionPlan): void;
export declare function findExecutionPlanById(id: string): ExecutionPlan | null;
export declare function listExecutionPlans(): ExecutionPlan[];
