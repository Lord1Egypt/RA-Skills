/**
 * 审计配置——由 .sofagent/config.yml 加载
 */
export interface AuditConfig {
    /** 低风险文件模式（不计入「不改越界」检查），支持 glob 风格 */
    lowRiskPatterns: string[];
    /** 测试/构建命令模式（用于「不逃验证」规则匹配日志） */
    testPatterns: string[];
    /** 「不改越界」阈值——不相关文件占比超过此比例时 WARN */
    carefulModifyThreshold: number;
    /** 是否启用扩展规则（E1-E4） */
    extendedRulesEnabled: boolean;
}
/**
 * 默认配置——当所有 fallback 都找不到配置文件时使用
 */
export declare const DEFAULT_CONFIG: AuditConfig;
/**
 * 加载审计配置（三级 fallback）
 * @param cwd 工作目录（默认 process.cwd()）
 * @returns 合并后的 AuditConfig
 */
export declare function loadConfig(cwd?: string): AuditConfig;
/**
 * 运行时配置——由环境变量加载（对应 lib/config.sh 导出项）
 */
export interface SofaEnvConfig {
    /** 数据目录路径 */
    dataDir: string;
    /** 日志脱敏开关 */
    sanitizeEnabled: boolean;
    /** 内网 IP 脱敏开关 */
    sanitizeIpsEnabled: boolean;
    /** 日志保留天数 */
    retentionDays: number;
    /** 日志最大条数 */
    retentionMax: number;
    /** 写日志后是否触发清理 */
    cleanupOnRecord: boolean;
    /** 清理触发频率（1/N 概率） */
    cleanupFrequency: number;
    /** 审计日志开关 */
    auditEnabled: boolean;
}
/** 环境变量默认值 */
export declare const ENV_DEFAULTS: Omit<SofaEnvConfig, 'dataDir'>;
/**
 * 从环境变量加载运行时配置
 * 对应 lib/config.sh 的 _parse_conf + export 逻辑
 */
export declare function loadEnvConfig(): SofaEnvConfig;
//# sourceMappingURL=config-loader.d.ts.map