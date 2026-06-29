export interface EnvReport {
    /** 环境变量 */
    env: Record<string, string>;
    /** 运行环境类型 */
    runtimeEnv: string;
    /** 工具链可用性 */
    tools: Record<string, {
        available: boolean;
        version?: string;
    }>;
    /** 路径信息 */
    paths: string[];
}
/**
 * 探测运行环境类型
 */
export declare function detectRuntimeEnv(): string;
/**
 * 收集关键环境变量
 */
export declare function collectEnvVars(): Record<string, string>;
/**
 * 探测工具链可用性
 */
export declare function detectTools(): Record<string, {
    available: boolean;
    version?: string;
}>;
/**
 * 收集 PATH 中的路径
 */
export declare function collectPaths(separator?: string): string[];
/**
 * 获取系统信息
 */
export declare function getSystemInfo(): {
    hostname: string;
    user: string;
    home: string;
    platform: string;
    cpus: number;
};
/**
 * 完整环境探测
 */
export declare function probeEnvironment(): EnvReport;
//# sourceMappingURL=run-envs.d.ts.map