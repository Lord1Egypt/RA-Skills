import type { ExecutionContract } from '../types/executionContract';
export declare function getExecutionContractsPath(): string;
export declare function loadExecutionContracts(): ExecutionContract[];
export declare function saveExecutionContract(contract: ExecutionContract): void;
export declare function findExecutionContractById(id: string): ExecutionContract | null;
export declare function listExecutionContracts(): ExecutionContract[];
