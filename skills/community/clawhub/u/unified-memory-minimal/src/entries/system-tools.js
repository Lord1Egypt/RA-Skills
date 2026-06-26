/**
 * System Tools Registration
 * Inline tool registration for cleaner, local embedding, benchmark, entity, plugin tools
 */
import { getCleaner, initCleaner } from '../memory-cleaner.js';
import { LocalEmbeddingService, EmbeddingNotReadyError, getLocalEmbedding, initLocalEmbedding, isLocalEmbeddingAvailable } from '../local_embedding.js';
import { getPluginStats, getPlugins, enablePlugin, disablePlugin, registerPlugin as registerExternalPlugin } from '../plugin/plugin_manager.js';
import { runRecallBenchmark } from '../benchmark/eval_recall.js';
import { loadEntityConfig, saveEntityConfig, addEntityType, getEntityTypesByPriority } from '../graph/entity_config.js';

export function registerCleanerTools(server, { z }) {
  server.registerTool('memory_cleaner_status', {
    description: '获取数据清理器状态',
    inputSchema: z.object({})
  }, async () => {
    const cleaner = getCleaner();
    return { content: [{ type: 'text', text: JSON.stringify(cleaner.getStatus(), null, 2) }] };
  });

  server.registerTool('memory_cleaner_config', {
    description: '更新数据清理器配置',
    inputSchema: z.object({
      enabled: z.boolean().optional(),
      retentionDays: z.number().optional(),
      cleanTime: z.string().optional(),
      allowAggressiveCleanup: z.boolean().optional(),
    })
  }, async (newConfig) => {
    const cleaner = getCleaner();
    cleaner.updateConfig(newConfig);
    return { content: [{ type: 'text', text: JSON.stringify(cleaner.getStatus(), null, 2) }] };
  });

  server.registerTool('memory_cleaner_run', {
    description: '手动执行一次数据清理',
    inputSchema: z.object({})
  }, async () => {
    const cleaner = getCleaner();
    const results = await cleaner.runOnce();
    return { content: [{ type: 'text', text: JSON.stringify(results, null, 2) }] };
  });
}

export function registerLocalEmbeddingTools(server, { z }) {
  server.registerTool('memory_local_embedding_status', {
    description: '获取本地 Embedding 服务状态',
    inputSchema: z.object({})
  }, async () => {
    const service = getLocalEmbedding({});
    const status = service.getStatus();
    const available = await isLocalEmbeddingAvailable();
    return { content: [{ type: 'text', text: JSON.stringify({ ...status, available }, null, 2) }] };
  });

  server.registerTool('memory_local_embedding_warmup', {
    description: '启动本地 Embedding 模型预热',
    inputSchema: z.object({ waitForReady: z.boolean().optional().default(false) })
  }, async ({ waitForReady }) => {
    const service = getLocalEmbedding({});
    service.startWarmup();
    if (waitForReady) await service.waitForReady();
    return { content: [{ type: 'text', text: JSON.stringify(service.getStatus(), null, 2) }] };
  });

  server.registerTool('memory_local_embedding_embed', {
    description: '使用本地 Embedding 模型获取向量',
    inputSchema: z.object({
      text: z.string().describe('要嵌入的文本'),
      waitForReady: z.boolean().optional().default(true),
    })
  }, async ({ text, waitForReady }) => {
    const service = getLocalEmbedding({});
    if (!service.isReady()) {
      service.startWarmup();
      if (waitForReady) await service.waitForReady();
      else throw new EmbeddingNotReadyError('Local embedding is not ready.');
    }
    const embedding = await service.embed(text);
    return { content: [{ type: 'text', text: JSON.stringify({ dimensions: embedding.length, embedding: Array.from(embedding).slice(0, 10) }, null, 2) }] };
  });
}

export function registerBenchmarkTools(server, { z }) {
  server.registerTool('memory_benchmark_recall', {
    description: '[v4.4] 运行记忆召回基准测试',
    inputSchema: z.object({ limit: z.number().optional().default(10) })
  }, async ({ limit }) => {
    try {
      const report = runRecallBenchmark();
      return { content: [{ type: 'text', text: JSON.stringify(report, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Benchmark error: ${err.message}` }], isError: true };
    }
  });
}

export function registerEntityTools(server, { z }) {
  server.registerTool('memory_entity_types_list', {
    description: '[v4.4] 列出所有可配置的实体类型',
    inputSchema: z.object({})
  }, async () => {
    try {
      const config = loadEntityConfig();
      const byPriority = getEntityTypesByPriority();
      return { content: [{ type: 'text', text: JSON.stringify({ config, byPriority }, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_entity_type_add', {
    description: '[v4.4] 添加或更新一个实体类型配置',
    inputSchema: z.object({
      typeName: z.string().describe('实体类型名称'),
      label: z.string().describe('中文标签'),
      labelEn: z.string().optional(),
      color: z.string().describe('颜色代码'),
      keywords: z.array(z.string()).optional(),
      priority: z.number().optional().default(5),
    })
  }, async ({ typeName, label, labelEn, color, keywords, priority }) => {
    try {
      const newConfig = addEntityType(typeName, { label, labelEn, color, keywords: keywords || [], priority });
      return { content: [{ type: 'text', text: JSON.stringify({ success: true, typeName, config: newConfig[typeName] }, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });
}

export function registerPluginToolsInline(server, { z }) {
  server.registerTool('memory_plugins_list', {
    description: '[v4.4] 列出所有已注册插件及其状态',
    inputSchema: z.object({})
  }, async () => {
    try {
      const stats = await getPluginStats();
      const plugins = await getPlugins();
      const list = Object.entries(plugins).map(([name, p]) => ({
        name, version: p.version, description: p.description, enabled: p.enabled,
        hooks: Object.keys(p.hooks || {}),
      }));
      return { content: [{ type: 'text', text: JSON.stringify({ stats, plugins: list }, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_plugin_enable', {
    description: '[v4.4] 启用指定插件',
    inputSchema: z.object({ name: z.string().describe('插件名称') })
  }, async ({ name }) => {
    try { return { content: [{ type: 'text', text: JSON.stringify(await enablePlugin(name), null, 2) }] }; }
    catch (err) { return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true }; }
  });

  server.registerTool('memory_plugin_disable', {
    description: '[v4.4] 禁用指定插件',
    inputSchema: z.object({ name: z.string().describe('插件名称') })
  }, async ({ name }) => {
    try { return { content: [{ type: 'text', text: JSON.stringify(await disablePlugin(name), null, 2) }] }; }
    catch (err) { return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true }; }
  });

  server.registerTool('memory_plugin_register', {
    description: '[v4.4] 注册一个外部插件',
    inputSchema: z.object({
      name: z.string().describe('插件名称'),
      version: z.string().optional().default('1.0.0'),
      description: z.string().optional(),
      path: z.string().describe('插件文件路径'),
    })
  }, async ({ name, version, description, path }) => {
    try { return { content: [{ type: 'text', text: JSON.stringify(await registerExternalPlugin({ name, version, description, path }), null, 2) }] }; }
    catch (err) { return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true }; }
  });
}
