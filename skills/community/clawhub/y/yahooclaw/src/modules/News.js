/**
 * 新闻聚合模块
 * 提供多源新闻查询和情感分析功能
 */

import yahooFinance from 'yahoo-finance2';

export class NewsModule {
  constructor(options = {}) {
    this.options = options;
  }

  /**
   * 获取新闻聚合
   * @param {string} symbol - 股票代码
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 新闻数据
   */
  async getNews(symbol, options = {}) {
    const {
      limit = 10,
      sources = ['yahoo'],
      sentiment = true
    } = options;

    const allNews = [];

    // 获取 Yahoo Finance 新闻
    if (sources.includes('yahoo')) {
      const yahooNews = await this._getYahooNews(symbol, limit);
      allNews.push(...yahooNews);
    }

    // 情感分析
    if (sentiment) {
      for (let news of allNews) {
        news.sentiment = this._analyzeSentiment(news.title + ' ' + (news.summary || ''));
      }
    }

    // 按时间排序
    allNews.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));

    // 限制数量
    const limitedNews = allNews.slice(0, limit);

    // 统计情感分布
    const sentimentStats = this._getSentimentStats(limitedNews);

    return {
      success: true,
      data: {
        symbol: symbol,
        news: limitedNews,
        count: limitedNews.length,
        sources: sources,
        sentimentStats: sentimentStats,
        overallSentiment: this._getOverallSentiment(sentimentStats),
        timestamp: new Date().toISOString()
      },
      message: `成功获取 ${symbol} 新闻，共 ${limitedNews.length} 条`
    };
  }

  /**
   * 获取 Yahoo Finance 新闻
   * @private
   */
  async _getYahooNews(symbol, limit = 10) {
    try {
      const news = await yahooFinance.search(symbol, { newsCount: limit });
      
      return news.news.map(n => ({
        title: n.title,
        summary: n.summary,
        source: 'yahoo',
        publisher: n.publisher,
        link: n.link,
        publishedAt: n.providerPublishTime ? new Date(n.providerPublishTime * 1000).toISOString() : new Date().toISOString(),
        thumbnail: n.thumbnail ? n.thumbnail.resolutions[0]?.url : null,
        type: n.type,
        uuid: n.uuid
      }));
    } catch (error) {
      console.error(`Yahoo News error for ${symbol}:`, error.message);
      return [];
    }
  }

  /**
   * 情感分析（简化版）
   * @private
   */
  _analyzeSentiment(text) {
    const positiveWords = [
      'beat', 'surge', 'soar', 'jump', 'rise', 'gain', 'growth', 'profit', 
      'bullish', 'upgrade', 'outperform', 'buy', 'strong', 'record', 'high',
      'positive', 'optimistic', 'exceed', 'outlook', 'rally', 'boom'
    ];
    
    const negativeWords = [
      'miss', 'drop', 'fall', 'decline', 'loss', 'bearish', 'downgrade',
      'sell', 'weak', 'low', 'negative', 'pessimistic', 'fail', 'crash',
      'plunge', 'slump', 'warning', 'risk', 'concern', 'lawsuit', 'investigation'
    ];

    const textLower = text.toLowerCase();
    
    let positiveCount = 0;
    let negativeCount = 0;

    positiveWords.forEach(word => {
      if (textLower.includes(word)) positiveCount++;
    });

    negativeWords.forEach(word => {
      if (textLower.includes(word)) negativeCount++;
    });

    const total = positiveCount + negativeCount;
    
    if (total === 0) {
      return { label: 'NEUTRAL', score: 0.5, positive: 0, negative: 0 };
    }

    const score = positiveCount / total;
    let label = 'NEUTRAL';
    
    if (score >= 0.6) label = 'POSITIVE';
    else if (score <= 0.4) label = 'NEGATIVE';

    return { label, score: parseFloat(score.toFixed(2)), positive: positiveCount, negative: negativeCount };
  }

  /**
   * 获取情感统计
   * @private
   */
  _getSentimentStats(news) {
    const stats = { positive: 0, negative: 0, neutral: 0, total: news.length };

    news.forEach(n => {
      if (n.sentiment) {
        if (n.sentiment.label === 'POSITIVE') stats.positive++;
        else if (n.sentiment.label === 'NEGATIVE') stats.negative++;
        else stats.neutral++;
      }
    });

    return stats;
  }

  /**
   * 获取整体情感倾向
   * @private
   */
  _getOverallSentiment(stats) {
    if (stats.total === 0) return 'NEUTRAL';
    
    const positiveRatio = stats.positive / stats.total;
    const negativeRatio = stats.negative / stats.total;
    
    if (positiveRatio >= 0.6) return 'BULLISH';
    if (negativeRatio >= 0.6) return 'BEARISH';
    if (positiveRatio >= 0.4) return 'SLIGHTLY_BULLISH';
    if (negativeRatio >= 0.4) return 'SLIGHTLY_BEARISH';
    return 'NEUTRAL';
  }
}
