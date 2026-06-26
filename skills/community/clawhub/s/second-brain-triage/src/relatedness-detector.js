/**
 * Relatedness Detector - 关联性检测器
 * 检测内容之间的关联关系，支持相似度匹配和主题聚类
 */

class RelatednessDetector {
  constructor() {
    // 相似度阈值
    this.thresholds = {
      strong: 0.8,    // 强关联
      medium: 0.5,    // 中等关联
      weak: 0.3,      // 弱关联
    };

    // 停用词
    this.stopWords = new Set([
      '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也',
      '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
      'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
      'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
      'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'and', 'or', 'but',
    ]);

    // 语义相似词映射（简化版）
    this.semanticGroups = {
      '技术': ['编程', '代码', '开发', '软件', '系统', '架构', '算法', '技术', 'tech', 'coding', 'programming'],
      '学习': ['阅读', '研究', '探索', '了解', '掌握', '学习', 'study', 'learn', 'research'],
      '工作': ['项目', '任务', '业务', '产品', '需求', '工作', 'work', 'project', 'task'],
      '生活': ['日常', '家庭', '健康', '饮食', '运动', '生活', 'life', 'daily', 'family'],
      '思考': ['想法', '观点', '反思', '总结', '思考', 'thought', 'idea', 'reflection'],
    };
  }

  /**
   * 检测与现有内容的关联
   * @param {Object} contentAnalysis - 新内容的分析结果
   * @param {Array} existingItems - 现有内容列表
   * @returns {Object} 关联检测结果
   */
  detect(contentAnalysis, existingItems = []) {
    const { metadata, type } = contentAnalysis;
    
    if (!existingItems || existingItems.length === 0) {
      return {
        hasRelated: false,
        relatedItems: [],
        suggestedConnections: [],
        topicClusters: [],
      };
    }

    // 计算与每个现有项的相似度
    const similarities = existingItems.map(item => ({
      item,
      similarity: this._calculateSimilarity(contentAnalysis, item),
    }));

    // 排序并筛选
    similarities.sort((a, b) => b.similarity - a.similarity);

    // 分类关联强度
    const strongRelated = similarities.filter(s => s.similarity >= this.thresholds.strong);
    const mediumRelated = similarities.filter(s => 
      s.similarity >= this.thresholds.medium && s.similarity < this.thresholds.strong
    );
    const weakRelated = similarities.filter(s => 
      s.similarity >= this.thresholds.weak && s.similarity < this.thresholds.medium
    );

    // 生成建议的连接
    const suggestedConnections = this._generateConnectionSuggestions(
      contentAnalysis, 
      strongRelated, 
      mediumRelated
    );

    // 识别主题聚类
    const topicClusters = this._identifyTopicClusters(contentAnalysis, similarities);

    return {
      hasRelated: similarities.some(s => s.similarity >= this.thresholds.weak),
      relatedItems: {
        strong: strongRelated.map(s => ({ ...s.item, similarity: s.similarity })),
        medium: mediumRelated.map(s => ({ ...s.item, similarity: s.similarity })),
        weak: weakRelated.map(s => ({ ...s.item, similarity: s.similarity })),
      },
      topRelated: similarities.slice(0, 5).map(s => ({
        ...s.item,
        similarity: s.similarity,
        relationType: this._determineRelationType(contentAnalysis, s.item),
      })),
      suggestedConnections,
      topicClusters,
      statistics: {
        totalChecked: existingItems.length,
        strongCount: strongRelated.length,
        mediumCount: mediumRelated.length,
        weakCount: weakRelated.length,
      },
    };
  }

  /**
   * 计算两个内容的相似度
   */
  _calculateSimilarity(analysis1, analysis2) {
    const scores = [];

    // 1. 标签相似度
    const tagSimilarity = this._calculateTagSimilarity(
      analysis1.metadata.tags || [],
      analysis2.metadata.tags || []
    );
    scores.push({ weight: 0.3, value: tagSimilarity });

    // 2. 标题相似度
    const titleSimilarity = this._calculateTextSimilarity(
      analysis1.metadata.title || '',
      analysis2.metadata.title || ''
    );
    scores.push({ weight: 0.25, value: titleSimilarity });

    // 3. 内容类型相似度
    const typeSimilarity = analysis1.type === analysis2.type ? 1 : 0;
    scores.push({ weight: 0.15, value: typeSimilarity });

    // 4. 描述相似度
    const descSimilarity = this._calculateTextSimilarity(
      analysis1.metadata.description || '',
      analysis2.metadata.description || ''
    );
    scores.push({ weight: 0.2, value: descSimilarity });

    // 5. 语义相似度（基于关键词）
    const semanticSimilarity = this._calculateSemanticSimilarity(
      `${analysis1.metadata.title} ${analysis1.metadata.description}`,
      `${analysis2.metadata.title} ${analysis2.metadata.description}`
    );
    scores.push({ weight: 0.1, value: semanticSimilarity });

    // 加权计算
    let totalWeight = 0;
    let weightedSum = 0;
    for (const score of scores) {
      weightedSum += score.value * score.weight;
      totalWeight += score.weight;
    }

    return weightedSum / totalWeight;
  }

  /**
   * 计算标签相似度（Jaccard系数）
   */
  _calculateTagSimilarity(tags1, tags2) {
    if (tags1.length === 0 || tags2.length === 0) return 0;
    
    const set1 = new Set(tags1.map(t => t.toLowerCase()));
    const set2 = new Set(tags2.map(t => t.toLowerCase()));
    
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    const union = new Set([...set1, ...set2]);
    
    return intersection.size / union.size;
  }

  /**
   * 计算文本相似度（基于词频）
   */
  _calculateTextSimilarity(text1, text2) {
    if (!text1 || !text2) return 0;
    
    const words1 = this._extractKeywords(text1);
    const words2 = this._extractKeywords(text2);
    
    if (words1.length === 0 || words2.length === 0) return 0;
    
    // 计算词频向量
    const allWords = new Set([...words1, ...words2]);
    const freq1 = this._getWordFrequency(words1);
    const freq2 = this._getWordFrequency(words2);
    
    // 计算余弦相似度
    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;
    
    for (const word of allWords) {
      const f1 = freq1[word] || 0;
      const f2 = freq2[word] || 0;
      dotProduct += f1 * f2;
      norm1 += f1 * f1;
      norm2 += f2 * f2;
    }
    
    if (norm1 === 0 || norm2 === 0) return 0;
    
    return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
  }

  /**
   * 计算语义相似度
   */
  _calculateSemanticSimilarity(text1, text2) {
    const words1 = this._extractKeywords(text1);
    const words2 = this._extractKeywords(text2);
    
    let matches = 0;
    
    for (const word1 of words1) {
      for (const word2 of words2) {
        if (this._areSemanticallyRelated(word1, word2)) {
          matches++;
          break;
        }
      }
    }
    
    return Math.min(1, matches / Math.min(words1.length, words2.length));
  }

  /**
   * 检查两个词是否语义相关
   */
  _areSemanticallyRelated(word1, word2) {
    if (word1 === word2) return true;
    
    for (const group of Object.values(this.semanticGroups)) {
      const inGroup1 = group.some(g => word1.toLowerCase().includes(g.toLowerCase()));
      const inGroup2 = group.some(g => word2.toLowerCase().includes(g.toLowerCase()));
      if (inGroup1 && inGroup2) return true;
    }
    
    return false;
  }

  /**
   * 提取关键词
   */
  _extractKeywords(text) {
    // 分词（简化版）
    const words = text
      .toLowerCase()
      .replace(/[^\w\u4e00-\u9fa5]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length >= 2 && !this.stopWords.has(w));
    
    return words;
  }

  /**
   * 获取词频
   */
  _getWordFrequency(words) {
    const freq = {};
    for (const word of words) {
      freq[word] = (freq[word] || 0) + 1;
    }
    return freq;
  }

  /**
   * 确定关系类型
   */
  _determineRelationType(analysis1, analysis2) {
    const relations = [];
    
    // 父子关系
    if (analysis2.metadata.title && 
        analysis1.metadata.title &&
        analysis2.metadata.title.includes(analysis1.metadata.title)) {
      relations.push('parent');
    }
    
    // 相同主题
    const tagOverlap = (analysis1.metadata.tags || []).filter(t => 
      (analysis2.metadata.tags || []).includes(t)
    );
    if (tagOverlap.length > 0) {
      relations.push('same-topic');
    }
    
    // 相同类型
    if (analysis1.type === analysis2.type) {
      relations.push('same-type');
    }
    
    // 时间相关
    if (analysis1.metadata.dates && analysis2.metadata.dates) {
      relations.push('time-related');
    }
    
    return relations.length > 0 ? relations : ['related'];
  }

  /**
   * 生成连接建议
   */
  _generateConnectionSuggestions(newAnalysis, strongRelated, mediumRelated) {
    const suggestions = [];
    
    // 强关联建议合并
    if (strongRelated.length > 0) {
      suggestions.push({
        type: 'merge',
        description: `与"${strongRelated[0].item.metadata.title}"高度相关，建议合并或建立父子关系`,
        target: strongRelated[0].item,
      });
    }
    
    // 中等关联建议链接
    if (mediumRelated.length > 0) {
      const topMedium = mediumRelated.slice(0, 2);
      suggestions.push({
        type: 'link',
        description: `建议与以下内容建立链接: ${topMedium.map(r => r.item.metadata.title).join(', ')}`,
        targets: topMedium.map(r => r.item),
      });
    }
    
    // 建议标签
    const suggestedTags = this._suggestTags(newAnalysis, [...strongRelated, ...mediumRelated]);
    if (suggestedTags.length > 0) {
      suggestions.push({
        type: 'tag',
        description: '建议添加标签',
        tags: suggestedTags,
      });
    }
    
    return suggestions;
  }

  /**
   * 建议标签
   */
  _suggestTags(newAnalysis, relatedItems) {
    const tagFrequency = {};
    
    // 统计关联项的标签
    for (const { item } of relatedItems) {
      for (const tag of (item.metadata.tags || [])) {
        tagFrequency[tag] = (tagFrequency[tag] || 0) + 1;
      }
    }
    
    // 筛选高频标签
    const existingTags = new Set(newAnalysis.metadata.tags || []);
    const suggested = Object.entries(tagFrequency)
      .filter(([tag, count]) => count >= 2 && !existingTags.has(tag))
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([tag]) => tag);
    
    return suggested;
  }

  /**
   * 识别主题聚类
   */
  _identifyTopicClusters(newAnalysis, similarities) {
    const clusters = [];
    
    // 基于标签聚类
    const tagClusters = {};
    for (const { item } of similarities.filter(s => s.similarity >= 0.4)) {
      for (const tag of (item.metadata.tags || [])) {
        if (!tagClusters[tag]) {
          tagClusters[tag] = [];
        }
        tagClusters[tag].push(item);
      }
    }
    
    // 找出主要聚类
    for (const [tag, items] of Object.entries(tagClusters)) {
      if (items.length >= 2) {
        clusters.push({
          topic: tag,
          itemCount: items.length,
          items: items.slice(0, 5),
          coherence: Math.min(1, items.length / 10),
        });
      }
    }
    
    // 按大小排序
    clusters.sort((a, b) => b.itemCount - a.itemCount);
    
    return clusters.slice(0, 3);
  }

  /**
   * 批量检测关联性
   */
  batchDetect(items, options = {}) {
    const results = [];
    
    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      const otherItems = items.filter((_, idx) => idx !== i);
      
      const relatedness = this.detect(item.analysis, otherItems.map(it => it.analysis));
      
      results.push({
        ...item,
        relatedness,
      });
    }
    
    return results;
  }

  /**
   * 查找重复或高度相似的内容
   */
  findDuplicates(items, threshold = 0.85) {
    const duplicates = [];
    
    for (let i = 0; i < items.length; i++) {
      for (let j = i + 1; j < items.length; j++) {
        const similarity = this._calculateSimilarity(
          items[i].analysis,
          items[j].analysis
        );
        
        if (similarity >= threshold) {
          duplicates.push({
            item1: items[i],
            item2: items[j],
            similarity,
            isDuplicate: similarity >= 0.95,
          });
        }
      }
    }
    
    return duplicates;
  }
}

module.exports = RelatednessDetector;