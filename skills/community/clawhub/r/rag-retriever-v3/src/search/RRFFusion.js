/**
 * RRF (Reciprocal Rank Fusion) 融合算法
 * 将多个检索结果列表融合为一个排序结果
 */

export class RRFFusion {
  constructor(options = {}) {
    this.k = options.k || 60;  // RRF 常数，通常设为 60
    this.weights = options.weights || {};  // 各检索器的权重
  }

  /**
   * 融合多个检索结果列表
   * @param {Array[]} resultLists - 多个检索结果列表，每个列表包含 {id, score, ...} 的对象
   * @param {Object} options - 配置选项
   * @param {number} options.limit - 返回结果数量限制
   * @returns {Array} - 融合后的排序结果
   */
  fuse(resultLists, options = {}) {
    const limit = options.limit || 10;
    
    if (!resultLists || resultLists.length === 0) {
      return [];
    }

    // 过滤空列表
    const validLists = resultLists.filter(list => list && list.length > 0);
    
    if (validLists.length === 0) {
      return [];
    }

    if (validLists.length === 1) {
      // 只有一个列表，直接返回
      return validLists[0].slice(0, limit).map((item, index) => ({
        ...item,
        rrfScore: 1 / (this.k + index + 1),
        sources: [{ rank: index + 1, score: item.score }]
      }));
    }

    // 收集所有文档 ID 及其在各列表中的排名
    const docRankings = new Map();

    validLists.forEach((list, listIndex) => {
      const weight = this.weights[listIndex] || 1.0;
      
      list.forEach((item, rank) => {
        const id = item.id || item.document_id || JSON.stringify(item);
        
        if (!docRankings.has(id)) {
          docRankings.set(id, {
            item: item,
            rankings: [],
            totalWeight: 0
          });
        }
        
        const entry = docRankings.get(id);
        entry.rankings.push({
          listIndex,
          rank: rank + 1,  // 排名从 1 开始
          score: item.score || 0,
          weight
        });
        entry.totalWeight += weight;
      });
    });

    // 计算 RRF 分数
    const fusedResults = [];
    
    docRankings.forEach((data, id) => {
      // RRF 公式: score = Σ (weight / (k + rank))
      let rrfScore = 0;
      
      data.rankings.forEach(ranking => {
        rrfScore += ranking.weight / (this.k + ranking.rank);
      });

      fusedResults.push({
        ...data.item,
        id,
        rrfScore,
        rankings: data.rankings,
        sourceCount: data.rankings.length
      });
    });

    // 按 RRF 分数降序排序
    fusedResults.sort((a, b) => b.rrfScore - a.rrfScore);

    // 添加融合后的排名
    const finalResults = fusedResults.slice(0, limit).map((item, index) => ({
      ...item,
      fusedRank: index + 1
    }));

    return finalResults;
  }

  /**
   * 带权重的融合
   * 允许为不同的检索器设置不同的权重
   */
  fuseWeighted(resultLists, weights, options = {}) {
    if (weights && weights.length === resultLists.length) {
      this.weights = weights.reduce((acc, w, i) => ({ ...acc, [i]: w }), {});
    }
    return this.fuse(resultLists, options);
  }

  /**
   * 融合两个结果列表（常用场景）
   */
  fuseTwo(vectorResults, keywordResults, options = {}) {
    return this.fuse([vectorResults, keywordResults], options);
  }

  /**
   * 获取融合统计信息
   */
  getFusionStats(fusedResults) {
    if (!fusedResults || fusedResults.length === 0) {
      return null;
    }

    const sourceCounts = fusedResults.map(r => r.sourceCount || 1);
    const rrfScores = fusedResults.map(r => r.rrfScore || 0);

    return {
      totalResults: fusedResults.length,
      avgSourceCount: sourceCounts.reduce((a, b) => a + b, 0) / sourceCounts.length,
      maxSourceCount: Math.max(...sourceCounts),
      minSourceCount: Math.min(...sourceCounts),
      avgRRFScore: rrfScores.reduce((a, b) => a + b, 0) / rrfScores.length,
      maxRRFScore: Math.max(...rrfScores),
      minRRFScore: Math.min(...rrfScores),
      k: this.k
    };
  }

  /**
   * 解释融合结果
   * 返回可读的融合解释
   */
  explainFusion(fusedResult) {
    if (!fusedResult || !fusedResult.rankings) {
      return '无融合信息';
    }

    const explanations = fusedResult.rankings.map(r => 
      `列表 ${r.listIndex + 1}: 排名 ${r.rank} (权重 ${r.weight}, 贡献 ${(r.weight / (this.k + r.rank)).toFixed(4)})`
    );

    return {
      totalScore: fusedResult.rrfScore.toFixed(4),
      sourceCount: fusedResult.sourceCount,
      details: explanations
    };
  }
}

export default RRFFusion;
