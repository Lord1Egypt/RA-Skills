/**
 * Scene & Pipeline Tools Registration
 * Inline tool registration for scene block and pipeline tools
 */
import { inductScenes, listSceneBlocks, getSceneBlock, deleteSceneBlock, searchSceneBlocks, getSceneStats } from '../scene_block.js';
import { scheduler, onConversationEnd, triggerPipeline, getPipelineStatus } from '../pipeline_scheduler.js';

export function registerSceneBlockTools(server, { z }) {
  server.registerTool('memory_scene_induct', {
    description: '从记忆中归纳场景块 (L2 Scene Induction)',
    inputSchema: z.object({
      scope: z.string().optional().default('USER').describe('范围: USER/TEAM/AGENT/GLOBAL'),
      timeRange: z.object({
        start: z.number().optional(),
        end: z.number().optional(),
      }).optional(),
      minMemories: z.number().optional().default(3),
      maxScenes: z.number().optional().default(20),
    })
  }, async ({ scope, timeRange, minMemories, maxScenes }) => {
    const scenes = await inductScenes({ scope, timeRange, minMemories, maxScenes });
    return { content: [{ type: 'text', text: JSON.stringify(scenes, null, 2) }] };
  });

  server.registerTool('memory_scene_list', {
    description: '列出所有场景块',
    inputSchema: z.object({
      scope: z.string().optional().default('USER'),
      limit: z.number().optional().default(20),
    })
  }, async ({ scope, limit }) => {
    const scenes = await listSceneBlocks(scope, limit);
    return { content: [{ type: 'text', text: JSON.stringify(scenes, null, 2) }] };
  });

  server.registerTool('memory_scene_get', {
    description: '获取场景块详情',
    inputSchema: z.object({
      sceneId: z.string().describe('场景块 ID'),
      scope: z.string().optional().default('USER'),
    })
  }, async ({ sceneId, scope }) => {
    const scene = await getSceneBlock(sceneId, scope);
    return { content: [{ type: 'text', text: scene ? JSON.stringify(scene, null, 2) : 'Scene not found' }] };
  });

  server.registerTool('memory_scene_delete', {
    description: '删除场景块',
    inputSchema: z.object({
      sceneId: z.string().describe('场景块 ID'),
      scope: z.string().optional().default('USER'),
    })
  }, async ({ sceneId, scope }) => {
    const result = await deleteSceneBlock(sceneId, scope);
    return { content: [{ type: 'text', text: result ? 'Scene deleted' : 'Scene not found' }] };
  });

  server.registerTool('memory_scene_search', {
    description: '搜索场景块',
    inputSchema: z.object({
      query: z.string().describe('搜索关键词'),
      scope: z.string().optional().default('USER'),
      limit: z.number().optional().default(10),
    })
  }, async ({ query, scope, limit }) => {
    const scenes = await searchSceneBlocks(query, scope, limit);
    return { content: [{ type: 'text', text: JSON.stringify(scenes, null, 2) }] };
  });

  server.registerTool('memory_scene_stats', {
    description: '获取场景统计',
    inputSchema: z.object({ scope: z.string().optional().default('USER') })
  }, async ({ scope }) => {
    const stats = await getSceneStats(scope);
    return { content: [{ type: 'text', text: JSON.stringify(stats, null, 2) }] };
  });
}

export function registerPipelineTools(server, { z }) {
  server.registerTool('memory_pipeline_status', {
    description: '获取四层管线状态 (L0→L1→L2→L3)',
    inputSchema: z.object({})
  }, async () => {
    const status = getPipelineStatus();
    return { content: [{ type: 'text', text: JSON.stringify(status, null, 2) }] };
  });

  server.registerTool('memory_pipeline_trigger', {
    description: '手动触发管线阶段',
    inputSchema: z.object({
      stage: z.enum(['L1', 'L2', 'L3']).describe('管线阶段'),
      sessionId: z.string().optional().describe('会话 ID'),
      scope: z.string().optional().default('USER'),
    })
  }, async ({ stage, sessionId, scope }) => {
    const result = await triggerPipeline(stage, sessionId, scope);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });

  server.registerTool('memory_pipeline_config', {
    description: '更新管线配置',
    inputSchema: z.object({
      enabled: z.boolean().optional(),
      everyNConversations: z.number().optional(),
      enableWarmup: z.boolean().optional(),
      l1IdleTimeoutSeconds: z.number().optional(),
      l2DelayAfterL1Seconds: z.number().optional(),
      l3TriggerEveryN: z.number().optional(),
    })
  }, async (newConfig) => {
    scheduler.updateConfig(newConfig);
    return { content: [{ type: 'text', text: JSON.stringify(scheduler.getStatus(), null, 2) }] };
  });
}
