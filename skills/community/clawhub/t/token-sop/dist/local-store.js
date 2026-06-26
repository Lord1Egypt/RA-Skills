"use strict";
/**
 * Local Workflow Store - 保存和检索本地工作流
 *
 * 功能：
 * - 保存成功的工作流到本地文件
 * - 按 intent + url 匹配本地工作流
 * - 优先级：本地 > 云端 > LLM
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.initLocalStore = initLocalStore;
exports.saveLocalWorkflow = saveLocalWorkflow;
exports.findLocalWorkflow = findLocalWorkflow;
exports.recordLocalFailure = recordLocalFailure;
exports.listLocalWorkflows = listLocalWorkflows;
exports.deleteLocalWorkflow = deleteLocalWorkflow;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const DEFAULT_STORAGE_DIR = path.join(process.env.HOME || "/root", ".openclaw", "workflows");
/**
 * 初始化本地存储目录
 */
function initLocalStore(config) {
    if (!config.enabled)
        return;
    const dir = config.storageDir || DEFAULT_STORAGE_DIR;
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}
/**
 * 保存工作流到本地
 */
function saveLocalWorkflow(config, intent, url, workflow) {
    if (!config.enabled)
        return;
    const dir = config.storageDir || DEFAULT_STORAGE_DIR;
    // 确保目录存在
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    const key = generateKey(intent, url);
    const filePath = path.join(dir, `${key}.json`);
    let existing = null;
    if (fs.existsSync(filePath)) {
        try {
            existing = JSON.parse(fs.readFileSync(filePath, "utf-8"));
        }
        catch {
            existing = null;
        }
    }
    const data = {
        intent,
        url,
        workflow,
        createdAt: existing?.createdAt || Date.now(),
        updatedAt: Date.now(),
        successCount: (existing?.successCount || 0) + 1,
        failureCount: existing?.failureCount || 0,
    };
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}
/**
 * 从本地检索工作流
 */
function findLocalWorkflow(config, intent, url) {
    if (!config.enabled)
        return null;
    const dir = config.storageDir || DEFAULT_STORAGE_DIR;
    // 精确匹配
    const exactKey = generateKey(intent, url);
    const exactPath = path.join(dir, `${exactKey}.json`);
    if (fs.existsSync(exactPath)) {
        try {
            const data = JSON.parse(fs.readFileSync(exactPath, "utf-8"));
            return data.workflow;
        }
        catch {
            return null;
        }
    }
    // 模糊匹配 - 按 intent 前缀
    try {
        const files = fs.readdirSync(dir);
        const intentLower = intent.toLowerCase();
        for (const file of files) {
            if (!file.endsWith(".json"))
                continue;
            const filePath = path.join(dir, file);
            try {
                const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
                if (data.intent.toLowerCase().includes(intentLower) ||
                    intentLower.includes(data.intent.toLowerCase())) {
                    return data.workflow;
                }
            }
            catch {
                continue;
            }
        }
    }
    catch {
        // 目录不存在
    }
    return null;
}
/**
 * 记录工作流失败
 */
function recordLocalFailure(config, intent, url) {
    if (!config.enabled)
        return;
    const dir = config.storageDir || DEFAULT_STORAGE_DIR;
    const key = generateKey(intent, url);
    const filePath = path.join(dir, `${key}.json`);
    if (!fs.existsSync(filePath))
        return;
    try {
        const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
        data.failureCount += 1;
        data.updatedAt = Date.now();
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    }
    catch {
        // 忽略错误
    }
}
/**
 * 列出所有本地工作流
 */
function listLocalWorkflows(config) {
    if (!config.enabled)
        return [];
    const dir = config.storageDir || DEFAULT_STORAGE_DIR;
    const workflows = [];
    if (!fs.existsSync(dir))
        return workflows;
    try {
        const files = fs.readdirSync(dir);
        for (const file of files) {
            if (!file.endsWith(".json"))
                continue;
            const filePath = path.join(dir, file);
            try {
                const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
                workflows.push(data);
            }
            catch {
                continue;
            }
        }
    }
    catch {
        // 忽略错误
    }
    return workflows;
}
/**
 * 删除本地工作流
 */
function deleteLocalWorkflow(config, intent, url) {
    if (!config.enabled)
        return false;
    const dir = config.storageDir || DEFAULT_STORAGE_DIR;
    const key = generateKey(intent, url);
    const filePath = path.join(dir, `${key}.json`);
    if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
        return true;
    }
    return false;
}
/**
 * 生成唯一键名
 */
function generateKey(intent, url) {
    const combined = `${intent}:${url}`;
    // 简单哈希
    let hash = 0;
    for (let i = 0; i < combined.length; i++) {
        const char = combined.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(36);
}
