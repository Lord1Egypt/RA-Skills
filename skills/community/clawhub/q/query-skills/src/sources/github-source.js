import BaseSource from './base-source.js';

class GitHubSource extends BaseSource {
  constructor(options = {}) {
    super(options);
    this.name = 'github';
    this.description = 'GitHub 社区技能源';
    this.apiUrl = 'https://api.github.com';
    this.token = options.token;
  }

  async searchSkills(query, options = {}) {
    try {
      // 模拟 GitHub 搜索结果
      // 实际实现时可以使用 GitHub API
      const mockResults = this.getMockResults(query);
      return mockResults.map(skill => this.formatSkill(skill));
    } catch (error) {
      console.error(`[GitHubSource] 搜索错误:`, error);
      return [];
    }
  }

  async getSkillDetails(slug) {
    try {
      // 模拟获取技能详情
      const mockSkill = this.getMockSkill(slug);
      if (mockSkill) {
        return this.formatSkill(mockSkill);
      }
      return null;
    } catch (error) {
      console.error(`[GitHubSource] 获取技能详情错误:`, error);
      return null;
    }
  }

  async getSkills(options = {}) {
    try {
      // 模拟获取技能列表
      const mockResults = this.getMockResults('');
      return mockResults.map(skill => this.formatSkill(skill));
    } catch (error) {
      console.error(`[GitHubSource] 获取技能列表错误:`, error);
      return [];
    }
  }

  // 模拟 GitHub 搜索结果
  getMockResults(query) {
    const allSkills = [
      {
        name: 'GitHub Actions Skill',
        slug: 'github-actions-skill',
        description: 'GitHub Actions 工作流自动化技能',
        tags: ['github', 'actions', 'automation'],
        downloads: 1200,
        verified: false,
        qualityScore: 75,
        author: 'github-user',
        repository: 'https://github.com/github-user/github-actions-skill'
      },
      {
        name: 'GitHub Issues Skill',
        slug: 'github-issues-skill',
        description: 'GitHub Issues 管理技能',
        tags: ['github', 'issues', 'management'],
        downloads: 850,
        verified: false,
        qualityScore: 70,
        author: 'github-user',
        repository: 'https://github.com/github-user/github-issues-skill'
      },
      {
        name: 'GitHub Repository Skill',
        slug: 'github-repository-skill',
        description: 'GitHub 仓库管理技能',
        tags: ['github', 'repository', 'management'],
        downloads: 920,
        verified: false,
        qualityScore: 68,
        author: 'github-user',
        repository: 'https://github.com/github-user/github-repository-skill'
      }
    ];

    if (!query) {
      return allSkills;
    }

    // 简单的关键词匹配
    return allSkills.filter(skill => 
      skill.name.toLowerCase().includes(query.toLowerCase()) ||
      skill.description.toLowerCase().includes(query.toLowerCase()) ||
      skill.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
    );
  }

  // 模拟获取单个技能
  getMockSkill(slug) {
    const allSkills = this.getMockResults('');
    return allSkills.find(skill => skill.slug === slug);
  }

  // 重写格式化方法
  formatSkill(skill) {
    const formatted = super.formatSkill(skill);
    return {
      ...formatted,
      source: 'github',
      sourceUrl: formatted.repository
    };
  }
}

export default GitHubSource;