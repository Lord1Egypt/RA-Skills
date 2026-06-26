/**
 * Local Workflow Store - 保存和检索本地工作流
 *
 * 功能：
 * - 保存成功的工作流到本地文件
 * - 按 intent + url 匹配本地工作流
 * - 优先级：本地 > 云端 > LLM
 */
import type { LobsterWorkflow } from "./types.js";
export interface LocalWorkflow {
    intent: string;
    url: string;
    workflow: LobsterWorkflow;
    createdAt: number;
    updatedAt: number;
    successCount: number;
    failureCount: number;
}
export interface LocalStoreConfig {
    storageDir: string;
    enabled: boolean;
}
/**
 * 初始化本地存储目录
 */
export declare function initLocalStore(config: LocalStoreConfig): void;
/**
 * 保存工作流到本地
 */
export declare function saveLocalWorkflow(config: LocalStoreConfig, intent: string, url: string, workflow: LobsterWorkflow): void;
/**
 * 从本地检索工作流
 */
export declare function findLocalWorkflow(config: LocalStoreConfig, intent: string, url: string): LobsterWorkflow | null;
/**
 * 记录工作流失败
 */
export declare function recordLocalFailure(config: LocalStoreConfig, intent: string, url: string): void;
/**
 * 列出所有本地工作流
 */
export declare function listLocalWorkflows(config: LocalStoreConfig): LocalWorkflow[];
/**
 * 删除本地工作流
 */
export declare function deleteLocalWorkflow(config: LocalStoreConfig, intent: string, url: string): boolean;
