"use strict";
/**
 * 错误处理
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaskError = exports.ConfigError = exports.AgentError = exports.ClawCompanyError = void 0;
exports.withErrorHandling = withErrorHandling;
class ClawCompanyError extends Error {
    constructor(message, code, details) {
        super(message);
        this.code = code;
        this.details = details;
        this.name = 'ClawCompanyError';
    }
}
exports.ClawCompanyError = ClawCompanyError;
class AgentError extends ClawCompanyError {
    constructor(agent, message, details) {
        super(`${agent} Agent 失败: ${message}`, 'AGENT_ERROR', { agent, ...details });
        this.name = 'AgentError';
    }
}
exports.AgentError = AgentError;
class ConfigError extends ClawCompanyError {
    constructor(message, details) {
        super(message, 'CONFIG_ERROR', details);
        this.name = 'ConfigError';
    }
}
exports.ConfigError = ConfigError;
class TaskError extends ClawCompanyError {
    constructor(taskId, message, details) {
        super(`任务 ${taskId} 失败: ${message}`, 'TASK_ERROR', { taskId, ...details });
        this.name = 'TaskError';
    }
}
exports.TaskError = TaskError;
/**
 * 错误处理包装器
 */
async function withErrorHandling(operation, fn) {
    try {
        return await fn();
    }
    catch (error) {
        if (error instanceof ClawCompanyError) {
            throw error;
        }
        throw new ClawCompanyError(`${operation} 失败`, 'OPERATION_ERROR', { operation, error: error instanceof Error ? error.message : String(error) });
    }
}
