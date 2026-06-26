/**
 * Markdown 存储模块
 * 每条收藏为一个独立 Markdown 文件
 */

const os = require('os');
const fs = require('fs');
const path = require('path');

class MarkdownStore {
  constructor(storagePath) {
    // 支持 ~ 扩展
    if (storagePath.startsWith('~/')) {
      storagePath = path.join(os.homedir(), storagePath.slice(2));
    }
    this.storagePath = storagePath;
    this._ensureDir();
  }

  _ensureDir() {
    if (!fs.existsSync(this.storagePath)) {
      fs.mkdirSync(this.storagePath, { recursive: true });
    }
  }

  /**
   * 生成文件ID
   * @returns {string} - 文件名
   */
  _generateId() {
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
    
    // 查找当天最大序号
    const files = fs.readdirSync(this.storagePath)
      .filter(f => f.startsWith(dateStr) && f.endsWith('.md'));
    
    let maxSeq = 0;
    for (const f of files) {
      const seq = parseInt(f.split('-')[1]?.replace('.md', '') || '0');
      if (seq > maxSeq) maxSeq = seq;
    }
    
    const seq = String(maxSeq + 1).padStart(3, '0');
    return `${dateStr}-${seq}`;
  }

  /**
   * 解析 frontmatter
   * @param {string} content - 文件内容
   * @returns {Object} - 解析后的对象
   */
  _parseFrontmatter(content) {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return { frontmatter: {}, body: content };

    const frontmatterStr = match[1];
    const body = content.slice(match[0].length).trim();

    const frontmatter = {};
    for (const line of frontmatterStr.split('\n')) {
      const colonIdx = line.indexOf(':');
      if (colonIdx === -1) continue;
      
      const key = line.slice(0, colonIdx).trim();
      let value = line.slice(colonIdx + 1).trim();
      
      // 处理数组
      if (value.startsWith('[') && value.endsWith(']')) {
        value = value.slice(1, -1).split(',').map(v => v.trim().replace(/^["']|["']$/g, ''));
      }
      
      frontmatter[key] = value;
    }

    return { frontmatter, body };
  }

  /**
   * 序列化 frontmatter
   * @param {Object} frontmatter - frontmatter 对象
   * @returns {string} - 序列化后的字符串
   */
  _stringifyFrontmatter(frontmatter) {
    const lines = [];
    for (const [key, value] of Object.entries(frontmatter)) {
      if (Array.isArray(value)) {
        lines.push(`${key}: [${value.map(v => `"${v}"`).join(', ')}]`);
      } else if (typeof value === 'string') {
        lines.push(`${key}: ${value}`);
      } else {
        lines.push(`${key}: ${value}`);
      }
    }
    return lines.join('\n');
  }

  /**
   * 创建收藏
   * @param {Object} data - 收藏数据
   * @returns {string} - 收藏ID
   */
  async create(data) {
    const id = this._generateId();
    const now = new Date();
    const nextReview = new Date();
    nextReview.setDate(nextReview.getDate() + 1);
    nextReview.setHours(9, 30, 0, 0);

    const frontmatter = {
      id,
      url: data.url || '',
      title: data.title || '无标题',
      tags: data.tags || [],
      category: data.category || '未分类',
      status: 'inbox',
      createdAt: now.toISOString(),
      nextReviewAt: nextReview.toISOString(),
      reviewCount: 0
    };

    const content = [
      '---',
      this._stringifyFrontmatter(frontmatter),
      '---',
      '',
      '## AI摘要',
      '',
      ...(data.summary || []).map((s, i) => `${i + 1}. ${s}`),
      ''
    ].join('\n');

    const filePath = path.join(this.storagePath, `${id}.md`);
    
    try {
      fs.writeFileSync(filePath, content, 'utf8');
    } catch (err) {
      throw new Error(`Markdown写入失败: ${err.message}`);
    }

    return id;
  }

  /**
   * 读取收藏
   * @param {string} id - 收藏ID
   * @returns {Object|null} - 收藏数据
   */
  async read(id) {
    const filePath = path.join(this.storagePath, `${id}.md`);
    if (!fs.existsSync(filePath)) return null;

    const content = fs.readFileSync(filePath, 'utf8');
    const { frontmatter, body } = this._parseFrontmatter(content);

    return { ...frontmatter, body };
  }

  /**
   * 更新 frontmatter
   * @param {string} id - 收藏ID
   * @param {Object} updates - 更新内容
   */
  async updateFrontmatter(id, updates) {
    const filePath = path.join(this.storagePath, `${id}.md`);
    if (!fs.existsSync(filePath)) {
      throw new Error(`收藏不存在: ${id}`);
    }

    const content = fs.readFileSync(filePath, 'utf8');
    const { frontmatter, body } = this._parseFrontmatter(content);

    const newFrontmatter = { ...frontmatter, ...updates };
    
    const newContent = [
      '---',
      this._stringifyFrontmatter(newFrontmatter),
      '---',
      body
    ].join('\n');

    fs.writeFileSync(filePath, newContent, 'utf8');
  }

  /**
   * 扫描待回顾条目
   * @returns {Promise<Array>} - 待回顾列表
   */
  async scanForReview() {
    const files = fs.readdirSync(this.storagePath)
      .filter(f => f.endsWith('.md'));
    
    const now = new Date();
    const items = [];

    for (const f of files) {
      const content = fs.readFileSync(path.join(this.storagePath, f), 'utf8');
      const { frontmatter } = this._parseFrontmatter(content);

      if (frontmatter.status === 'inbox' || frontmatter.status === 'needs-review') {
        const nextReview = new Date(frontmatter.nextReviewAt || 0);
        if (nextReview <= now) {
          items.push(frontmatter);
        }
      }
    }

    return items;
  }

  /**
   * 列出所有收藏
   * @param {Object} filters - 过滤条件
   * @returns {Promise<Array>} - 收藏列表
   */
  async list(filters = {}) {
    const files = fs.readdirSync(this.storagePath)
      .filter(f => f.endsWith('.md'));
    
    const items = [];

    for (const f of files) {
      const content = fs.readFileSync(path.join(this.storagePath, f), 'utf8');
      const { frontmatter } = this._parseFrontmatter(content);

      let match = true;
      if (filters.status) match = match && frontmatter.status === filters.status;
      if (filters.category) match = match && frontmatter.category === filters.category;
      if (filters.tag) match = match && (frontmatter.tags || []).includes(filters.tag);

      if (match) items.push(frontmatter);
    }

    return items.sort((a, b) => 
      new Date(b.createdAt) - new Date(a.createdAt)
    );
  }

  /**
   * 删除收藏
   * @param {string} id - 收藏ID
   */
  async delete(id) {
    const filePath = path.join(this.storagePath, `${id}.md`);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  }
}

module.exports = MarkdownStore;
