/**
 * Tool Registry - 工具注册与发现中心
 * 
 * 功能：
 * - 注册/注销工具
 * - 工具元数据管理
 * - 语义匹配工具发现
 * - 工具执行包装（超时、错误处理）
 */

class ToolRegistry {
  constructor() {
    this.tools = new Map(); // name -> {fn, metadata}
  }

  /**
   * 注册工具
   * @param {string} name - 工具名称（唯一标识）
   * @param {Function} fn - 工具执行函数
   * @param {Object} metadata - 工具元数据
   * @param {string} metadata.description - 工具描述
   * @param {Array<string>} metadata.keywords - 关键词（用于匹配）
   * @param {Object} metadata.paramSchema - 参数 schema（JSON Schema 格式）
   * @param {number} metadata.timeout - 超时秒数（默认 30）
   */
  register(name, fn, metadata = {}) {
    if (this.tools.has(name)) {
      console.warn(`⚠️ 工具 ${name} 已存在，将被覆盖`);
    }

    this.tools.set(name, {
      fn: this._wrapExecution(fn, metadata),
      metadata: {
        name,
        description: metadata.description || '无描述',
        keywords: metadata.keywords || [],
        paramSchema: metadata.paramSchema || {},
        timeout: metadata.timeout || 30,
        registeredAt: Date.now(),
      },
    });

    return this;
  }

  /**
   * 批量注册工具
   * @param {Array} tools - [{name, fn, metadata}]
   */
  registerTools(tools) {
    tools.forEach(({ name, fn, metadata }) => {
      this.register(name, fn, metadata);
    });
    return this;
  }

  /**
   * 注销工具
   */
  unregister(name) {
    if (this.tools.has(name)) {
      console.warn(`⚠️ 工具 ${name} 已存在，将被覆盖`);
    }

    this.tools.set(name, {
      fn: this._wrapExecution(fn, metadata),
      metadata: {
        name,
        description: metadata.description || '无描述',
        keywords: metadata.keywords || [],
        paramSchema: metadata.paramSchema || {},
        timeout: metadata.timeout || 30,
        registeredAt: Date.now(),
      },
    });

    return this;
  }

  /**
   * 注销工具
   */
  unregister(name) {
    return this.tools.delete(name);
  }

  /**
   * 获取工具
   */
  get(name) {
    return this.tools.get(name);
  }

  /**
   * 获取工具元数据
   */
  getMetadata(name) {
    const tool = this.tools.get(name);
    return tool ? tool.metadata : null;
  }

  /**
   * 列出所有工具名称
   */
  list() {
    return Array.from(this.tools.keys());
  }

  /**
   * 列出所有工具详情
   */
  listAll() {
    return Array.from(this.tools.entries()).map(([name, { metadata }]) => metadata);
  }

  /**
   * 根据关键词匹配工具
   * @param {string} query - 查询文本
   * @param {number} limit - 最多返回数量
   * @returns {Array<string>} 匹配的工具名称
   */
  match(query, limit = 3) {
    const queryLower = query.toLowerCase();
    const scores = [];

    for (const [name, { metadata }] of this.tools) {
      let score = 0;

      // 关键词匹配
      for (const keyword of metadata.keywords) {
        if (queryLower.includes(keyword.toLowerCase())) {
          score += 2;
        }
      }

      // 描述匹配
      if (metadata.description.toLowerCase().includes(queryLower)) {
        score += 1;
      }

      // 名称匹配
      if (name.toLowerCase().includes(queryLower)) {
        score += 3;
      }

      if (score > 0) {
        scores.push({ name, score });
      }
    }

    // 按分数排序
    scores.sort((a, b) => b.score - a.score);

    return scores.slice(0, limit).map(s => s.name);
  }

  /**
   * 工具执行包装（超时、错误处理）
   */
  _wrapExecution(fn, metadata) {
    const timeout = metadata.timeout || 30;

    return async (...args) => {
      return new Promise((resolve, reject) => {
        const timeoutId = setTimeout(() => {
          reject(new Error(`工具执行超时 (${timeout}s)`));
        }, timeout * 1000);

        Promise.resolve(fn(...args))
          .then(result => {
            clearTimeout(timeoutId);
            resolve(result);
          })
          .catch(error => {
            clearTimeout(timeoutId);
            reject(error);
          });
      });
    };
  }

  /**
   * 导出工具配置（用于序列化/分享）
   */
  export() {
    return {
      tools: this.listAll(),
      exportedAt: Date.now(),
    };
  }

  /**
   * 从配置导入工具（需要配合实际工具实现）
   */
  import(config, toolImplementations) {
    for (const toolConfig of config.tools) {
      const impl = toolImplementations[toolConfig.name];
      if (impl) {
        this.register(toolConfig.name, impl, toolConfig);
      } else {
        console.warn(`⚠️ 工具 ${toolConfig.name} 无实现，跳过`);
      }
    }
    return this;
  }

  /**
   * 清空所有工具
   */
  clear() {
    this.tools.clear();
    return this;
  }

  /**
   * 获取统计信息
   */
  stats() {
    return {
      totalTools: this.tools.size,
      tools: this.list(),
      registeredAt: Array.from(this.tools.values()).map(t => t.metadata.registeredAt),
    };
  }
}

module.exports = { ToolRegistry };
