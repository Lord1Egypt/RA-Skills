import * as fs from 'node:fs';
import * as path from 'node:path';
import type { ExecutionPlan } from '../types/executionPlan';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getExecutionPlansPath(): string {
  return path.join(getWorldLoopsDir(), 'execution_plans.json');
}

export function loadExecutionPlans(): ExecutionPlan[] {
  const plansPath = getExecutionPlansPath();
  if (!fs.existsSync(plansPath)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(plansPath, 'utf8')) as ExecutionPlan[];
}

export function saveExecutionPlan(plan: ExecutionPlan): void {
  const plansPath = getExecutionPlansPath();
  const dir = path.dirname(plansPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const existing = loadExecutionPlans();
  const upserted = existing.filter((p) => p.id !== plan.id);
  upserted.push(plan);
  fs.writeFileSync(plansPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}

export function findExecutionPlanById(id: string): ExecutionPlan | null {
  return loadExecutionPlans().find((p) => p.id === id) ?? null;
}

export function listExecutionPlans(): ExecutionPlan[] {
  return loadExecutionPlans();
}
