/**
 * Connectors - 连接器模块入口
 * 
 * 提供外部数据源连接器的统一导出和管理
 * 
 * 支持的连接器（未来扩展）：
 * - GitHubConnector: GitHub issues, PRs, commits
 * - NotionConnector: Notion pages, databases
 * - FeishuConnector: 飞书文档、多维表格
 * - SlackConnector: Slack messages, channels
 */

import BaseConnector from './base.js';

// ─── 连接器注册表 ───────────────────────────────────────────────────────────────
const connectorRegistry = new Map();

/**
 * 注册连接器
 */
export function registerConnector(name, ConnectorClass) {
  connectorRegistry.set(name, ConnectorClass);
}

/**
 * 创建连接器实例
 */
export function createConnector(name, options = {}) {
  const ConnectorClass = connectorRegistry.get(name);
  
  if (!ConnectorClass) {
    throw new Error(`Unknown connector: ${name}`);
  }
  
  return new ConnectorClass(options);
}

/**
 * 获取所有已注册的连接器
 */
export function listConnectors() {
  return [...connectorRegistry.keys()];
}

/**
 * 批量创建连接器
 */
export function createConnectors(configs = []) {
  const connectors = [];
  
  for (const cfg of configs) {
    try {
      const connector = createConnector(cfg.type, cfg);
      connectors.push(connector);
    } catch (e) {
      console.error(`Failed to create connector ${cfg.type}: ${e.message}`);
    }
  }
  
  return connectors;
}

// ─── 导出 ────────────────────────────────────────────────────────────────────

export { BaseConnector } from './base.js';

export default {
  BaseConnector,
  registerConnector,
  createConnector,
  listConnectors,
  createConnectors,
};
