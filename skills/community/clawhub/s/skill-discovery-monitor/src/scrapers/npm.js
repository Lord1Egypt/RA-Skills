const axios = require('axios');

/**
 * npm Registry Scraper
 *
 * Fetches popular CLI tools and packages from npm
 */
class NpmScraper {
  constructor() {
    this.baseURL = 'https://registry.npmjs.org';
    this.searchURL = 'https://api.npms.io/v2';
  }

  /**
   * Get popular CLI tools from npm
   * @param {number} limit - Number of packages to fetch
   * @returns {Promise<Array>}
   */
  async getPopularCLITools(limit = 10) {
    try {
      const response = await axios.get(`${this.searchURL}/search`, {
        params: {
          q: 'keywords:cli,keywords:tool',
          size: limit
        },
        timeout: 10000
      });

      return response.data.results.map(result => this.formatPackage(result.package));
    } catch (error) {
      console.error('npm scraping failed:', error.message);
      return [];
    }
  }

  /**
   * Format npm package data
   */
  formatPackage(pkg) {
    return {
      name: pkg.name,
      platform: 'npm',
      category: 'developer-tools',
      description: pkg.description || 'No description available',
      author: pkg.publisher?.username || pkg.author?.name || 'Unknown',
      stars: pkg.score?.detail?.popularity * 1000 || 0,
      downloads: pkg.score?.detail?.popularity * 10000 || 0,
      version: pkg.version,
      tags: pkg.keywords || [],
      features: this.extractFeatures(pkg),
      url: pkg.links?.npm || `https://www.npmjs.com/package/${pkg.name}`,
      createdAt: pkg.date,
      updatedAt: pkg.date
    };
  }

  /**
   * Extract features
   */
  extractFeatures(pkg) {
    const features = [];
    if (pkg.keywords) {
      features.push(...pkg.keywords.slice(0, 5));
    }
    return features;
  }
}

module.exports = NpmScraper;
