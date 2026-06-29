"use strict";
// ============================================================
// config-loader.ts · .sofagent/config.yml 配置加载器
// v0.95 新增：三级 fallback + 手写极简 YAML 解析器
// v0.97 扩展：环境变量配置（从 lib/config.sh 合并）
// ============================================================
// 配置格式只支持两种语法：
//   key: value          （键值对）
//   - item              （列表项）
// 解析 audit 段下的字段，其余段忽略。
//
// 三级 fallback：
//   1. ${cwd}/.sofagent/config.yml
//   2. ~/.sofagent/config.yml
//   3. DEFAULT_CONFIG
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.ENV_DEFAULTS = exports.DEFAULT_CONFIG = void 0;
exports.loadConfig = loadConfig;
exports.loadEnvConfig = loadEnvConfig;
const fs_1 = require("fs");
const path_1 = require("path");
const os_1 = require("os");
/**
 * 默认配置——当所有 fallback 都找不到配置文件时使用
 */
exports.DEFAULT_CONFIG = {
    lowRiskPatterns: ['package-lock.json', 'yarn.lock', '*.log', 'docs/**'],
    testPatterns: ['npm test', 'npm run test', 'pytest', 'go test'],
    carefulModifyThreshold: 0.2,
    extendedRulesEnabled: false,
};
/**
 * 加载审计配置（三级 fallback）
 * @param cwd 工作目录（默认 process.cwd()）
 * @returns 合并后的 AuditConfig
 */
function loadConfig(cwd) {
    const baseDir = cwd || process.cwd();
    // 1. 尝试 ${cwd}/.sofagent/config.yml
    const projectConfigPath = (0, path_1.join)(baseDir, '.sofagent', 'config.yml');
    const projectConfig = tryLoadYaml(projectConfigPath);
    if (projectConfig) {
        return mergeWithDefaults(projectConfig);
    }
    // 2. 尝试 ~/.sofagent/config.yml
    const homeConfigPath = (0, path_1.join)((0, os_1.homedir)(), '.sofagent', 'config.yml');
    const homeConfig = tryLoadYaml(homeConfigPath);
    if (homeConfig) {
        return mergeWithDefaults(homeConfig);
    }
    // 3. 使用默认配置
    return { ...exports.DEFAULT_CONFIG };
}
// ============================================================
// 内部实现
// ============================================================
/**
 * 尝试从 YAML 文件加载配置，文件不存在或解析失败时返回 null
 */
function tryLoadYaml(filePath) {
    if (!(0, fs_1.existsSync)(filePath)) {
        return null;
    }
    let content;
    try {
        content = (0, fs_1.readFileSync)(filePath, 'utf-8');
    }
    catch {
        return null;
    }
    return parseSimpleYaml(content);
}
/**
 * 极简 YAML 解析器
 * 支持格式：
 *   audit:
 *     lowRiskPatterns:
 *       - package-lock.json
 *       - yarn.lock
 *     testPatterns:
 *       - npm test
 *     carefulModifyThreshold: 0.2
 *     extendedRulesEnabled: false
 *
 * 只解析 audit 段下的字段，其他段忽略。
 * 支持 # 注释（行尾注释和整行注释）。
 */
function parseSimpleYaml(content) {
    const result = {};
    const lines = content.split('\n');
    let inAuditSection = false;
    let inListField = null;
    for (const rawLine of lines) {
        // 去除行尾注释（# 后面的内容），但保留 # 在引号内的情况
        const line = stripComment(rawLine);
        // 空行跳过
        if (line.trim() === '') {
            continue;
        }
        const indent = line.length - line.trimStart().length;
        const trimmed = line.trim();
        // 顶层段（indent === 0）
        if (indent === 0) {
            inAuditSection = false;
            inListField = null;
            if (trimmed === 'audit:') {
                inAuditSection = true;
            }
            continue;
        }
        // 不在 audit 段内，跳过
        if (!inAuditSection) {
            continue;
        }
        // 列表项（以 - 开头）
        if (trimmed.startsWith('- ')) {
            if (inListField) {
                const item = trimmed.substring(2).trim();
                // 去除可能的引号
                const cleanItem = stripQuotes(item);
                if (inListField === 'lowRiskPatterns') {
                    if (!result.lowRiskPatterns)
                        result.lowRiskPatterns = [];
                    result.lowRiskPatterns.push(cleanItem);
                }
                else if (inListField === 'testPatterns') {
                    if (!result.testPatterns)
                        result.testPatterns = [];
                    result.testPatterns.push(cleanItem);
                }
            }
            continue;
        }
        // 键值对
        const colonIdx = trimmed.indexOf(':');
        if (colonIdx === -1) {
            continue;
        }
        const key = trimmed.substring(0, colonIdx).trim();
        const value = trimmed.substring(colonIdx + 1).trim();
        // 值为空——可能是列表段（后续行以 - 开头）
        if (value === '') {
            if (key === 'lowRiskPatterns') {
                inListField = 'lowRiskPatterns';
                if (!result.lowRiskPatterns)
                    result.lowRiskPatterns = [];
            }
            else if (key === 'testPatterns') {
                inListField = 'testPatterns';
                if (!result.testPatterns)
                    result.testPatterns = [];
            }
            else {
                inListField = null;
            }
            continue;
        }
        // 有值——标量字段
        inListField = null;
        if (key === 'carefulModifyThreshold') {
            const num = parseFloat(stripQuotes(value));
            if (!isNaN(num)) {
                result.carefulModifyThreshold = num;
            }
        }
        else if (key === 'extendedRulesEnabled') {
            const cleaned = stripQuotes(value).toLowerCase();
            result.extendedRulesEnabled = cleaned === 'true' || cleaned === 'yes' || cleaned === '1';
        }
    }
    return result;
}
/**
 * 将部分配置与默认配置合并（缺失字段用默认值填充）
 */
function mergeWithDefaults(partial) {
    return {
        lowRiskPatterns: partial.lowRiskPatterns ?? exports.DEFAULT_CONFIG.lowRiskPatterns,
        testPatterns: partial.testPatterns ?? exports.DEFAULT_CONFIG.testPatterns,
        carefulModifyThreshold: partial.carefulModifyThreshold ?? exports.DEFAULT_CONFIG.carefulModifyThreshold,
        extendedRulesEnabled: partial.extendedRulesEnabled ?? exports.DEFAULT_CONFIG.extendedRulesEnabled,
    };
}
/**
 * 去除行尾注释（# 后面的内容）
 * 不处理引号内的 # ——极简解析器，配置文件中的 # 通常不需要出现在值中
 */
function stripComment(line) {
    const hashIdx = line.indexOf('#');
    if (hashIdx === -1)
        return line;
    // 如果 # 在行首（缩进后），整行是注释
    if (line.trim().startsWith('#'))
        return '';
    return line.substring(0, hashIdx);
}
/**
 * 去除字符串两端的引号（单引号或双引号）
 */
function stripQuotes(s) {
    if (s.length >= 2) {
        if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
            return s.substring(1, s.length - 1);
        }
    }
    return s;
}
/** 环境变量默认值 */
exports.ENV_DEFAULTS = {
    sanitizeEnabled: false,
    sanitizeIpsEnabled: false,
    retentionDays: 90,
    retentionMax: 500,
    cleanupOnRecord: false,
    cleanupFrequency: 10,
    auditEnabled: false,
};
/**
 * 从环境变量加载运行时配置
 * 对应 lib/config.sh 的 _parse_conf + export 逻辑
 */
function loadEnvConfig() {
    const homeDir = (0, os_1.homedir)();
    const dataDir = resolveDataDir(homeDir);
    return {
        dataDir,
        sanitizeEnabled: resolveBoolEnv('SOFA_SANITIZE', exports.ENV_DEFAULTS.sanitizeEnabled),
        sanitizeIpsEnabled: resolveBoolEnv('SOFA_SANITIZE_IPS', exports.ENV_DEFAULTS.sanitizeIpsEnabled),
        retentionDays: resolveNumberEnv('SOFA_RETENTION_DAYS', exports.ENV_DEFAULTS.retentionDays),
        retentionMax: resolveNumberEnv('SOFA_RETENTION_MAX', exports.ENV_DEFAULTS.retentionMax),
        cleanupOnRecord: resolveBoolEnv('SOFA_CLEANUP_ON_RECORD', exports.ENV_DEFAULTS.cleanupOnRecord),
        cleanupFrequency: resolveNumberEnv('SOFA_CLEANUP_FREQUENCY', exports.ENV_DEFAULTS.cleanupFrequency),
        auditEnabled: resolveBoolEnv('SOFA_AUDIT_ENABLED', exports.ENV_DEFAULTS.auditEnabled),
    };
}
/**
 * 解析数据目录（对应 _sofa_find_data_dir 函数）
 * 优先级：环境变量 > 当前目录 > 标记文件 > fallback
 */
function resolveDataDir(home) {
    // 1. 环境变量显式指定
    if (process.env.SOFAGENT_DATA && (0, fs_1.existsSync)(process.env.SOFAGENT_DATA)) {
        return process.env.SOFAGENT_DATA;
    }
    // 2. 当前目录有 .sofagent/
    const cwdData = (0, path_1.join)(process.cwd(), '.sofagent');
    if ((0, fs_1.existsSync)(cwdData)) {
        return cwdData;
    }
    // 3. 标记文件
    const markers = [
        (0, path_1.join)(home, '.openclaw', 'skills', 'sofagent', '.sofagent-data-path'),
        (0, path_1.join)(home, '.workbuddy', 'skills', 'sofagent', '.sofagent-data-path'),
    ];
    for (const marker of markers) {
        if ((0, fs_1.existsSync)(marker)) {
            try {
                const path = (0, fs_1.readFileSync)(marker, 'utf-8').trim();
                if (path && (0, fs_1.existsSync)(path))
                    return path;
            }
            catch { /* */ }
        }
    }
    // 4. fallback
    return (0, path_1.join)(process.cwd(), '.sofagent');
}
function resolveBoolEnv(key, defaultValue) {
    const val = process.env[key];
    if (val === undefined || val === '')
        return defaultValue;
    return val.toLowerCase() === 'true' || val === '1' || val.toLowerCase() === 'yes';
}
function resolveNumberEnv(key, defaultValue) {
    const val = process.env[key];
    if (val === undefined || val === '')
        return defaultValue;
    const num = parseInt(val, 10);
    return isNaN(num) ? defaultValue : num;
}
//# sourceMappingURL=config-loader.js.map