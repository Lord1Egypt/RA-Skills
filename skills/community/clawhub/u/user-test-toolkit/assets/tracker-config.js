/**
 * tracker-config.js — global Tracker 全局配置
 * 
 * 使用前必读：
 * 1. 在引入 tracker.js 之前引入本文件
 * 2. 至少设置 TRACKER_ENDPOINT（数据上报地址）
 * 3. 可选覆盖其他配置项
 * 
 * 示例（在你的页面 <head> 中）：
 * <script src="tracker-config.js"></script>
 * <script>
 *   // 修改 endpoint（必须）
 *   window.TRACKER_CONFIG.endpoint = 'https://your-server.com/track';
 *   // 可选：自定义 milestone 名称
 *   window.TRACKER_CONFIG.milestones = { TASK_DONE: 'task_done', STEP2: 'step2' };
 *   // 可选：自定义 action 映射
 *   window.TRACKER_CONFIG.actionMap = { '.my-btn': 'my_action' };
 * </script>
 * <script src="tracker.js"></script>
 */

window.TRACKER_CONFIG = window.TRACKER_CONFIG || {};

/**
 * endpoint — 埋点数据上报地址（必需）
 * 格式：完整的 URL，tracker 会 POST JSON body 到此地址
 * 
 * 示例：'https://your-api.com/track'
 *        'https://analytics.your-product.com/collect'
 */
window.TRACKER_CONFIG.endpoint = window.TRACKER_CONFIG.endpoint || '';

/**
 * milestones — milestone 名称映射表（可选）
 * 
 * 用于将业务 milestone 名称映射为通用名称，
 * 让 survey.js 的跨项目复用成为可能。
 * 
 * 格式：{ 业务名称: 通用名称 }
 * 
 * 示例：
 *   { 'mps_complete': 'task_done', 'finetune_edit': 'step2' }
 * 
 * 不设置时使用默认映射（见 tracker.js 内部 DEFAULT_MILESTONE_MAP）
 */
window.TRACKER_CONFIG.milestones = window.TRACKER_CONFIG.milestones || null;

/**
 * 默认 milestone 映射（global → 通用名称）
 * 当 TRACKER_CONFIG.milestones 未设置时使用此表
 */
window.TRACKER_CONFIG.DEFAULT_MILESTONE_MAP = {
  'mps_complete':   'task_done',
  'view_result':    'result_viewed',
  'finetune_edit':  'step_edited',
  'export':         'exported',
  'upload_done':    'upload_done',
  'page_translate': 'page_entered'
};

/**
 * actionMap — action 自动分类映射表（可选）
 * 
 * 格式：{ 'selector': 'actionName', ... }
 * 
 * tracker.js 的 identifyAction() 函数会优先检查此映射表，
 * 再回退到默认的 action 识别逻辑。
 * 
 * 示例：
 *   { '.signup-btn': 'signup', '#checkout': 'purchase' }
 */
window.TRACKER_CONFIG.actionMap = window.TRACKER_CONFIG.actionMap || null;

/**
 * flushInterval — 上报批量发送间隔（ms，默认 8000）
 */
window.TRACKER_CONFIG.flushInterval = window.TRACKER_CONFIG.flushInterval || 8000;

/**
 * maxQueue — 缓存队列最大条数，达到后立即上报（默认 30）
 */
window.TRACKER_CONFIG.maxQueue = window.TRACKER_CONFIG.maxQueue || 30;

/**
 * disabled — 设置为 true 可临时禁用埋点（保留记录但不上报）
 */
window.TRACKER_CONFIG.disabled = window.TRACKER_CONFIG.disabled || false;

/**
 * getMilestone(name) — 将业务 milestone 名称映射为通用名称
 * 供 tracker.js 内部使用
 */
window.TRACKER_CONFIG.getMilestone = function(name) {
  if (this.milestones && this.milestones[name]) {
    return this.milestones[name];
  }
  return this.DEFAULT_MILESTONE_MAP[name] || name;
};
