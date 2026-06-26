import * as fs from 'node:fs';
import * as path from 'node:path';
import type { ExecutionContract } from '../types/executionContract';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getExecutionContractsPath(): string {
  return path.join(getWorldLoopsDir(), 'execution_contracts.json');
}

export function loadExecutionContracts(): ExecutionContract[] {
  const contractsPath = getExecutionContractsPath();
  if (!fs.existsSync(contractsPath)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(contractsPath, 'utf8')) as ExecutionContract[];
}

export function saveExecutionContract(contract: ExecutionContract): void {
  const contractsPath = getExecutionContractsPath();
  const dir = path.dirname(contractsPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const existing = loadExecutionContracts();
  const upserted = existing.filter((c) => c.id !== contract.id);
  upserted.push(contract);
  fs.writeFileSync(contractsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}

export function findExecutionContractById(id: string): ExecutionContract | null {
  return loadExecutionContracts().find((c) => c.id === id) ?? null;
}

export function listExecutionContracts(): ExecutionContract[] {
  return loadExecutionContracts();
}
