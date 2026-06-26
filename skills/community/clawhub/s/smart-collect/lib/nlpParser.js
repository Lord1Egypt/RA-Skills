/**
 * 自然语言解析模块
 * 解析用户指令并执行对应操作
 */

class NLPParser {
  constructor(store, reviewEngine) {
    this.store = store;
    this.reviewEngine = reviewEngine;
  }

  /**
   * 解析并执行指令
   * @param {string} text - 用户输入的自然语言
   * @param {string} id - 收藏ID
   * @returns {Promise<Object>} - 执行结果
   */
  async parse(text, id) {
    const normalized = text.toLowerCase().trim();

    // 推迟X天
    const postponeMatch = normalized.match(/推迟(\d+)天|推迟.*?(\d+)\s*天/);
    if (postponeMatch || normalized.includes('推迟')) {
      const days = postponeMatch ? (parseInt(postponeMatch[1] || postponeMatch[2]) || 1) : 1;
      await this.reviewEngine.postpone(this.store, id, days);
      return { action: 'postpone', days };
    }

    // 已看完归档
    if (normalized.includes('归档') || normalized.includes('看完')) {
      await this.store.updateFrontmatter(id, {
        status: 'archived',
        archivedAt: new Date().toISOString()
      });
      return { action: 'archive' };
    }

    // 添加标签
    const addTagMatch = normalized.match(/添加标签[：:]?\s*(.+)/);
    if (addTagMatch || normalized.includes('添加标签')) {
      const tag = addTagMatch ? addTagMatch[1].trim() : '未命名';
      const item = await this.store.read(id);
      const tags = item?.tags || [];
      if (!tags.includes(tag)) {
        tags.push(tag);
      }
      await this.store.updateFrontmatter(id, { tags });
      return { action: 'addTag', tag };
    }

    // 删除标签
    const removeTagMatch = normalized.match(/删除标签[：:]?\s*(.+)/);
    if (removeTagMatch || normalized.includes('删除标签')) {
      const tag = removeTagMatch ? removeTagMatch[1].trim() : null;
      if (tag) {
        const item = await this.store.read(id);
        const tags = (item?.tags || []).filter(t => t !== tag);
        await this.store.updateFrontmatter(id, { tags });
        return { action: 'removeTag', tag };
      }
      return { action: 'error', message: '未指定要删除的标签' };
    }

    // 标记已回顾
    if (normalized.includes('已回顾') || normalized.includes('回顾')) {
      const item = await this.store.read(id);
      const reviewCount = (item?.reviewCount || 0) + 1;
      const nextReviewAt = this.reviewEngine.calculateNextReviewDate(reviewCount);
      
      await this.store.updateFrontmatter(id, {
        reviewCount,
        nextReviewAt: nextReviewAt.toISOString(),
        lastReviewAt: new Date().toISOString()
      });
      return { action: 'reviewed', reviewCount };
    }

    // 列出所有
    if (normalized.includes('列出') || normalized.includes('列表') || normalized.includes('看看')) {
      const items = await this.store.list();
      return { action: 'list', items };
    }

    // 查看详情
    if (normalized.includes('查看') || normalized.includes('详情')) {
      const item = await this.store.read(id);
      return { action: 'detail', item };
    }

    return { action: 'unknown', message: '无法理解指令' };
  }

  /**
   * 获取支持的指令列表
   * @returns {Array} - 支持的指令
   */
  getSupportedCommands() {
    return [
      { pattern: '推迟X天', example: '推迟3天' },
      { pattern: '已看完归档', example: '已看完归档' },
      { pattern: '添加标签', example: '添加标签 AI' },
      { pattern: '删除标签', example: '删除标签 AI' },
      { pattern: '标记已回顾', example: '已回顾' },
      { pattern: '列出', example: '列出所有收藏' },
      { pattern: '查看', example: '查看详情' }
    ];
  }
}

module.exports = NLPParser;
