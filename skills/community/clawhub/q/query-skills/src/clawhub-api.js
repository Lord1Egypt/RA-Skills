import axios from 'axios';
import { Skill } from './skill.js';

class ClawHubAPI {
  constructor(options = {}) {
    this.baseURL = options.baseURL || 'https://clawhub.ai';
    this.apiKey = options.apiKey || null;
    this.timeout = options.timeout || 10000;

    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: this.timeout,
      headers: this.apiKey ? {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      } : {
        'Content-Type': 'application/json'
      }
    });
  }

  async searchSkills(query, options = {}) {
    const {
      limit = 10,
      minDownloads = 0,
      verified = null,
      qualityScore = 0,
      sort = 'downloads'
    } = options;

    try {
      const params = {
        q: query,
        limit
      };

      // 首先尝试从源站搜索
      let response = await this.client.get('/api/v1/search', { params });
      let results = response.data.results.map(skill => Skill.fromJSON(skill));

      // 如果源站返回空结果，尝试从镜像站获取
      if (results.length === 0) {
        console.log('[ClawHubAPI] 源站返回空结果，尝试从镜像站获取');
        results = await this._searchFromMirror(query, options);
      }

      return results;
    } catch (error) {
      this._handleError(error, '搜索技能失败');
      // 发生错误时，尝试从镜像站获取
      console.log('[ClawHubAPI] 源站搜索失败，尝试从镜像站获取');
      return await this._searchFromMirror(query, options);
    }
  }

  // 从镜像站搜索
  async _searchFromMirror(query, options = {}) {
    try {
      // 使用镜像站的 API 接口
      const mirrorUrl = 'https://skills.volces.com/api/v1/search';
      const params = {
        q: query,
        limit: options.limit || 10
      };

      console.log(`[ClawHubAPI] 从镜像站搜索: ${query}`);
      const response = await axios.get(mirrorUrl, { params });
      
      // 处理返回的数据
      const results = response.data.results || [];
      console.log(`[ClawHubAPI] 镜像站返回 ${results.length} 个结果`);

      // 转换为 Skill 对象
      return results.map(item => {
        // 从 metaContent 中提取信息
        const metaContent = item.metaContent || {};
        const skillMd = metaContent.skillMd || '';
        
        // 解析 skillMd 中的信息
        const nameMatch = skillMd.match(/name: (.*)/);
        const descriptionMatch = skillMd.match(/description: (.*)/);
        
        return Skill.fromJSON({
          name: metaContent.displayName || item.displayName || nameMatch?.[1] || item.slug,
          slug: item.slug,
          description: metaContent.DisplayDescription || descriptionMatch?.[1] || item.summary || '暂无描述',
          tags: metaContent.Keywords || [],
          downloads: 0, // 镜像站 API 没有提供下载量
          verified: true, // 默认为已验证
          qualityScore: item.score || 0,
          repository: '', // 镜像站 API 没有提供仓库链接
          installCommand: '', // 镜像站 API 没有提供安装命令
          version: item.version || '1.0.0',
          author: metaContent.owner || '未知作者',
          createdAt: new Date(item.updatedAt || Date.now()).toISOString(),
          updatedAt: new Date(item.updatedAt || Date.now()).toISOString()
        });
      });
    } catch (error) {
      console.error('[ClawHubAPI] 镜像站搜索失败:', error);
      return [];
    }
  }

  async getSkillDetails(slug) {
    try {
      // 不使用 mock 数据
      const response = await this.client.get(`/api/v1/skills/${slug}`);
      return Skill.fromJSON(response.data);
    } catch (error) {
      this._handleError(error, `获取技能详情失败: ${slug}`);
      return null;
    }
  }

  async getSkills(options = {}) {
    const {
      limit = 20,
      offset = 0,
      sort = 'downloads'
    } = options;

    try {
      // 不使用 mock 数据
      const params = {
        limit,
        offset,
        sort
      };

      const response = await this.client.get('/api/v1/skills', { params });
      return response.data.results.map(skill => Skill.fromJSON(skill));
    } catch (error) {
      this._handleError(error, '获取技能列表失败');
      return [];
    }
  }



  _handleError(error, message) {
    if (error.response) {
      throw new Error(`${message}: ${error.response.status} - ${error.response.data?.message || '未知错误'}`);
    } else if (error.request) {
      throw new Error(`${message}: 网络连接失败`);
    } else {
      throw new Error(`${message}: ${error.message}`);
    }
  }
}

export default ClawHubAPI;
