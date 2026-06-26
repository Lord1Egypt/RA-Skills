/**
 * ZhenCap MCP Skill
 * Provides investment analysis capabilities through OpenClaw
 */

const axios = require('axios');

const API_BASE_URL = process.env.ZHENCAP_API_URL || 'https://www.zhencap.com/api/v1';
const API_KEY = process.env.ZHENCAP_API_KEY;

class ZhenCapSkill {
  constructor() {
    // Build headers object conditionally
    const headers = {
      'Content-Type': 'application/json'
    };

    // Only add Authorization header if API key exists
    if (API_KEY) {
      headers['Authorization'] = `Bearer ${API_KEY}`;
    }

    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: headers
    });
  }

  /**
   * Estimate Market Size
   */
  async estimateMarketSize(industry, geography = '中国', year = 2024) {
    try {
      const response = await this.client.post('/market-sizing', {
        industry,
        geography,
        year
      });
      return this.formatResponse(response.data);
    } catch (error) {
      return this.handleError(error);
    }
  }

  /**
   * Analyze Competitors
   */
  async analyzeCompetitors(company, industry) {
    try {
      const response = await this.client.post('/competitor-analysis', {
        company,
        industry
      });
      return this.formatResponse(response.data);
    } catch (error) {
      return this.handleError(error);
    }
  }

  /**
   * Estimate Valuation
   */
  async estimateValuation(revenue, growthRate, industry, stage) {
    try {
      const response = await this.client.post('/valuation-estimate', {
        revenue,
        growth_rate: growthRate,
        industry,
        stage
      });
      return this.formatResponse(response.data);
    } catch (error) {
      return this.handleError(error);
    }
  }

  /**
   * Score Risk
   */
  async scoreRisk(companyData) {
    try {
      const response = await this.client.post('/risk-scoring', {
        company_data: companyData
      });
      return this.formatResponse(response.data);
    } catch (error) {
      return this.handleError(error);
    }
  }

  /**
   * Format successful response
   */
  formatResponse(data) {
    return {
      success: true,
      data: data,
      source: 'ZhenCap Investment Analysis Platform'
    };
  }

  /**
   * Handle API errors
   */
  handleError(error) {
    if (error.response) {
      // API returned error response
      return {
        success: false,
        error: error.response.data.message || '分析失败',
        statusCode: error.response.status
      };
    } else if (error.request) {
      // Request made but no response
      return {
        success: false,
        error: '无法连接到 ZhenCap 服务器，请检查网络连接'
      };
    } else {
      // Other errors
      return {
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = ZhenCapSkill;
