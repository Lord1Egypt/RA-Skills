export interface CompactConfig {
  max_tokens: number;
  preserve_recent: number;
  auto_compact: boolean;
  model: string;
}

// 默认配置：模型留空，将在运行时动态读取 OpenClaw 配置
const DEFAULT_CONFIG: CompactConfig = {
  max_tokens: 10000, // 恢复默认阈值
  preserve_recent: 4,
  auto_compact: true,
  model: '' // 空字符串表示使用 OpenClaw 全局默认模型
};

export function loadConfig(overrides: Partial<CompactConfig> = {}): CompactConfig {
  return {
    ...DEFAULT_CONFIG,
    ...overrides
  };
}

/**
 * 从 OpenClaw 配置系统加载配置
 * OpenClaw 插件配置应该位于 plugins.entries.<plugin-id>.config 下
 */
export function loadFromOpenClawConfig(pluginConfig: Record<string, any> | null = {}): CompactConfig {
  // OpenClaw 插件配置结构：
  // {
  //   plugins: {
  //     entries: {
  //       "openclaw-session-compact": {
  //         enabled: true,
  //         config: {
  //           max_tokens: 10000,
  //           preserve_recent: 4,
  //           auto_compact: true,
  //           model: ""
  //         }
  //       }
  //     }
  //   }
  // }
  
  // api.getConfig() 可能返回整个配置对象或插件特定配置
  // 我们需要从不同的可能路径中提取配置
  const config = pluginConfig?.config || pluginConfig || {};
  
  return {
    max_tokens: config.max_tokens ?? DEFAULT_CONFIG.max_tokens,
    preserve_recent: config.preserve_recent ?? DEFAULT_CONFIG.preserve_recent,
    auto_compact: config.auto_compact ?? DEFAULT_CONFIG.auto_compact,
    model: config.model ?? DEFAULT_CONFIG.model,
  };
}

export function mergeConfigs(base: Partial<CompactConfig>, override: Partial<CompactConfig>): CompactConfig {
  return {
    ...DEFAULT_CONFIG,
    ...base,
    ...override
  };
}
