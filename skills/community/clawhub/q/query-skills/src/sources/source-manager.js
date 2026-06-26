import ClawHubSource from './clawhub-source.js';
import GitHubSource from './github-source.js';
import FilterSort from '../filter-sort.js';

class SourceManager {
  constructor(options = {}) {
    this.options = options;
    this.sources = [];
    this.initSources();
  }

  // 初始化所有来源
  initSources() {
    // 添加 ClawHub 来源
    this.sources.push(new ClawHubSource({
      apiOptions: this.options.clawhubOptions || { baseURL: 'https://clawhub.ai' }
    }));

    // 添加 GitHub 来源
    this.sources.push(new GitHubSource({
      token: this.options.githubToken
    }));

    // 可以在此添加更多来源
  }

  // 获取所有可用来源
  getSources() {
    return this.sources;
  }

  // 搜索所有来源
  async searchAll(query, options = {}) {
    try {
      const results = await Promise.all(
        this.sources.map(source => source.searchSkills(query, options))
      );

      // 合并结果并去重
      const mergedResults = this.mergeAndDeduplicate(results.flat());
      
      // 应用过滤
      let filteredResults = mergedResults;
      if (options.filters) {
        filteredResults = FilterSort.filterSkills(mergedResults, options.filters);
      }
      
      // 应用排序
      const sortedResults = FilterSort.sortSkills(
        filteredResults,
        options.sort || 'relevance',
        options.sortOrder || 'desc'
      );
      
      // 应用分页
      if (options.pagination) {
        return FilterSort.paginateSkills(
          sortedResults,
          options.pagination.page || 1,
          options.pagination.pageSize || 20
        );
      }
      
      return sortedResults;
    } catch (error) {
      console.error('[SourceManager] 搜索错误:', error);
      return [];
    }
  }

  // 从特定来源搜索
  async searchFrom(sourceName, query, options = {}) {
    try {
      const source = this.sources.find(s => s.name === sourceName);
      if (!source) {
        throw new Error(`来源 ${sourceName} 不存在`);
      }
      
      let results = await source.searchSkills(query, options);
      
      // 应用过滤
      if (options.filters) {
        results = FilterSort.filterSkills(results, options.filters);
      }
      
      // 应用排序
      results = FilterSort.sortSkills(
        results,
        options.sort || 'relevance',
        options.sortOrder || 'desc'
      );
      
      // 应用分页
      if (options.pagination) {
        return FilterSort.paginateSkills(
          results,
          options.pagination.page || 1,
          options.pagination.pageSize || 20
        );
      }
      
      return results;
    } catch (error) {
      console.error(`[SourceManager] 从 ${sourceName} 搜索错误:`, error);
      return [];
    }
  }

  // 获取技能详情（从所有来源）
  async getSkillDetails(slug) {
    try {
      for (const source of this.sources) {
        const skill = await source.getSkillDetails(slug);
        if (skill) {
          return skill;
        }
      }
      return null;
    } catch (error) {
      console.error('[SourceManager] 获取技能详情错误:', error);
      return null;
    }
  }

  // 合并结果并去重
  mergeAndDeduplicate(results) {
    const seen = new Set();
    return results.filter(skill => {
      const key = `${skill.slug}-${skill.source}`;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }

  // 检查所有来源的可用性
  async checkSourcesAvailability() {
    const availability = [];
    for (const source of this.sources) {
      const isAvailable = await source.isAvailable();
      availability.push({
        name: source.name,
        description: source.description,
        available: isAvailable
      });
    }
    return availability;
  }

  // 高级搜索
  async advancedSearch(criteria = {}) {
    try {
      const results = await Promise.all(
        this.sources.map(source => source.searchSkills(criteria.query || '', criteria))
      );

      // 合并结果并去重
      const mergedResults = this.mergeAndDeduplicate(results.flat());
      
      // 应用高级搜索
      return FilterSort.advancedSearch(mergedResults, criteria);
    } catch (error) {
      console.error('[SourceManager] 高级搜索错误:', error);
      return [];
    }
  }
}

export default SourceManager;