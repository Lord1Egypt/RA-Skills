/**
 * 反思能力模块
 * 负责执行后反思、错误分析、成功模式提取和经验积累
 */

const EventEmitter = require('events');

/**
 * 反思记录类
 */
class ReflectionRecord {
  constructor(data) {
    this.id = data.id || `reflection-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    this.taskId = data.taskId;
    this.taskType = data.taskType || 'unknown';
    this.result = data.result;
    this.duration = data.duration || 0;
    this.quality = data.quality || 0;
    this.timestamp = Date.now();
    
    // 反思内容
    this.insights = data.insights || [];
    this.lessons = data.lessons || [];
    this.patterns = data.patterns || [];
    this.improvements = data.improvements || [];
    this.recommendations = data.recommendations || [];
    
    // 元数据
    this.confidence = data.confidence || 0.5;
    this.depth = data.depth || 1;
    this.context = data.context || {};
  }

  addInsight(insight) {
    this.insights.push({
      text: insight,
      timestamp: Date.now()
    });
  }

  addLesson(lesson) {
    this.lessons.push({
      text: lesson,
      timestamp: Date.now()
    });
  }

  addPattern(pattern) {
    this.patterns.push({
      description: pattern.description,
      frequency: pattern.frequency || 1,
      successRate: pattern.successRate || 0,
      timestamp: Date.now()
    });
  }
}

/**
 * 经验库类
 */
class ExperienceStore {
  constructor(options = {}) {
    this.experiences = [];
    this.patterns = new Map();
    this.lessons = new Map();
    this.options = {
      maxExperiences: options.maxExperiences || 1000,
      minPatternFrequency: options.minPatternFrequency || 3,
      ...options
    };
  }

  /**
   * 添加经验
   */
  addExperience(reflection) {
    const experience = {
      id: reflection.id,
      taskType: reflection.taskType,
      result: reflection.result,
      quality: reflection.quality,
      duration: reflection.duration,
      insights: reflection.insights,
      lessons: reflection.lessons,
      timestamp: reflection.timestamp
    };

    // 限制经验数量
    if (this.experiences.length >= this.options.maxExperiences) {
      this.experiences.shift();
    }
    
    this.experiences.push(experience);

    // 更新模式
    this._updatePatterns(reflection);
    
    // 更新教训
    this._updateLessons(reflection);

    return experience;
  }

  /**
   * 更新模式
   */
  _updatePatterns(reflection) {
    reflection.patterns.forEach(pattern => {
      const key = `${reflection.taskType}:${pattern.description}`;
      const existing = this.patterns.get(key);
      
      if (existing) {
        existing.frequency++;
        existing.successRate = (existing.successRate * (existing.frequency - 1) + 
          (reflection.result === 'success' ? 1 : 0)) / existing.frequency;
        existing.lastSeen = Date.now();
      } else {
        this.patterns.set(key, {
          description: pattern.description,
          taskType: reflection.taskType,
          frequency: 1,
          successRate: reflection.result === 'success' ? 1 : 0,
          firstSeen: Date.now(),
          lastSeen: Date.now()
        });
      }
    });
  }

  /**
   * 更新教训
   */
  _updateLessons(reflection) {
    reflection.lessons.forEach(lesson => {
      const key = typeof lesson === 'string' ? lesson : lesson.text;
      const existing = this.lessons.get(key);
      
      if (existing) {
        existing.frequency++;
        existing.lastApplied = Date.now();
      } else {
        this.lessons.set(key, {
          text: key,
          frequency: 1,
          taskTypes: [reflection.taskType],
          firstLearned: Date.now(),
          lastApplied: Date.now()
        });
      }
    });
  }

  /**
   * 获取相关经验
   */
  getRelevantExperiences(taskType, limit = 10) {
    return this.experiences
      .filter(e => e.taskType === taskType)
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, limit);
  }

  /**
   * 获取成功模式
   */
  getSuccessPatterns(taskType, minSuccessRate = 0.7) {
    return Array.from(this.patterns.values())
      .filter(p => p.taskType === taskType && p.successRate >= minSuccessRate)
      .sort((a, b) => b.successRate - a.successRate);
  }

  /**
   * 获取常见错误
   */
  getCommonMistakes(taskType, limit = 5) {
    return this.experiences
      .filter(e => e.taskType === taskType && e.result === 'failure')
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, limit);
  }

  /**
   * 获取统计信息
   */
  getStatistics() {
    const total = this.experiences.length;
    const successes = this.experiences.filter(e => e.result === 'success').length;
    const failures = this.experiences.filter(e => e.result === 'failure').length;
    
    return {
      totalExperiences: total,
      successCount: successes,
      failureCount: failures,
      successRate: total > 0 ? successes / total : 0,
      patternCount: this.patterns.size,
      lessonCount: this.lessons.size
    };
  }

  /**
   * 清理旧经验
   */
  cleanup(maxAge = 30 * 24 * 60 * 60 * 1000) { // 默认30天
    const cutoff = Date.now() - maxAge;
    this.experiences = this.experiences.filter(e => e.timestamp > cutoff);
    
    for (const [key, pattern] of this.patterns) {
      if (pattern.lastSeen < cutoff) {
        this.patterns.delete(key);
      }
    }
  }
}

/**
 * 反思引擎主类
 */
class ReflectionEngine extends EventEmitter {
  constructor(options = {}) {
    super();
    this.experienceStore = new ExperienceStore(options);
    this.reflections = new Map();
    this.options = {
      defaultDepth: options.defaultDepth || 2,
      minQualityThreshold: options.minQualityThreshold || 0.5,
      ...options
    };
  }

  /**
   * 分析执行结果
   */
  async analyze(data) {
    const reflection = new ReflectionRecord({
      taskId: data.taskId || `task-${Date.now()}`,
      taskType: data.task,
      result: data.result,
      duration: data.duration,
      quality: data.quality,
      context: data.context || {},
      depth: this.options.defaultDepth
    });

    // 基于结果类型进行分析
    if (data.result === 'success') {
      await this._analyzeSuccess(reflection, data);
    } else if (data.result === 'failure') {
      await this._analyzeFailure(reflection, data);
    } else {
      await this._analyzePartial(reflection, data);
    }

    // 提取模式
    await this._extractPatterns(reflection, data);

    // 生成建议
    await this._generateRecommendations(reflection, data);

    // 计算置信度
    reflection.confidence = this._calculateConfidence(reflection);

    // 存储反思
    this.reflections.set(reflection.id, reflection);
    
    // 添加到经验库
    this.experienceStore.addExperience(reflection);

    this.emit('reflectionCompleted', { reflection });

    return {
      id: reflection.id,
      taskId: reflection.taskId,
      lessons: reflection.lessons,
      patterns: reflection.patterns,
      recommendations: reflection.recommendations,
      confidence: reflection.confidence,
      insights: reflection.insights
    };
  }

  /**
   * 分析成功
   */
  async _analyzeSuccess(reflection, data) {
    reflection.addInsight(`Task completed successfully in ${data.duration}ms`);
    reflection.addInsight(`Quality score: ${data.quality}`);
    
    // 提取成功因素
    if (data.quality > 0.8) {
      reflection.addLesson('High quality execution achieved');
      reflection.addPattern({
        description: 'high_quality_execution',
        frequency: 1,
        successRate: 1.0
      });
    }
    
    if (data.duration < 1000) {
      reflection.addLesson('Fast execution indicates efficient approach');
    }

    // 获取相关经验进行对比
    const relevant = this.experienceStore.getRelevantExperiences(data.task, 5);
    const avgQuality = relevant.reduce((sum, e) => sum + e.quality, 0) / relevant.length || 0;
    
    if (data.quality > avgQuality) {
      reflection.addInsight('Performance exceeded historical average');
    }
  }

  /**
   * ����ʧ��
   */
  async _analyzeFailure(reflection, data) {
    reflection.addInsight(`Task failed after ${data.duration}ms`);
    
    // ��������ԭ��
    if (data.error) {
      reflection.addLesson(`Error encountered: ${data.error.message || 'Unknown error'}`);
      
      // �������
      if (data.error.message && data.error.message.includes('timeout')) {
        reflection.addPattern({
          description: 'timeout_error',
          frequency: 1,
          successRate: 0
        });
        reflection.improvements.push('Consider increasing timeout or optimizing performance');
      } else if (data.error.message && data.error.message.includes('network')) {
        reflection.addPattern({
          description: 'network_error',
          frequency: 1,
          successRate: 0
        });
        reflection.improvements.push('Implement retry logic for network operations');
      } else {
        reflection.addPattern({
          description: 'general_error',
          frequency: 1,
          successRate: 0
        });
      }
    }
    
    // ����Ƿ����ظ�ʧ��
    const relevant = this.experienceStore.getRelevantExperiences(data.task, 5);
    const recentFailures = relevant.filter(e => e.result === 'failure').length;
    
    if (recentFailures >= 2) {
      reflection.addInsight('Pattern of repeated failures detected');
      reflection.improvements.push('Consider changing approach or seeking alternative solutions');
    }
    
    reflection.addLesson('Failure analysis completed - improvements identified');
  }

  /**
   * �������ֳɹ�
   */
  async _analyzePartial(reflection, data) {
    reflection.addInsight(`Task partially completed in ${data.duration}ms`);
    reflection.addInsight(`Quality score: ${data.quality || 0}`);
    
    if (data.quality < 0.5) {
      reflection.addLesson('Low quality output - review execution steps');
      reflection.improvements.push('Improve quality control measures');
    } else {
      reflection.addLesson('Acceptable quality but room for improvement');
    }
  }

  /**
   * ��ȡģʽ
   */
  async _extractPatterns(reflection, data) {
    // ��������������ȡģʽ
    const taskPatterns = this.experienceStore.getSuccessPatterns(data.task, 0.6);
    
    taskPatterns.forEach(pattern => {
      if (pattern.frequency >= this.experienceStore.options.minPatternFrequency) {
        reflection.addPattern(pattern);
      }
    });
    
    // ʱ��ģʽ
    if (data.duration) {
      const relevant = this.experienceStore.getRelevantExperiences(data.task, 10);
      const avgDuration = relevant.reduce((sum, e) => sum + e.duration, 0) / relevant.length || data.duration;
      
      if (data.duration > avgDuration * 1.5) {
        reflection.addPattern({
          description: 'slower_than_average',
          frequency: 1,
          successRate: data.result === 'success' ? 1 : 0
        });
        reflection.addInsight('Execution was slower than historical average');
      } else if (data.duration < avgDuration * 0.5) {
        reflection.addPattern({
          description: 'faster_than_average',
          frequency: 1,
          successRate: data.result === 'success' ? 1 : 0
        });
        reflection.addInsight('Execution was faster than historical average');
      }
    }
  }

  /**
   * ���ɽ���
   */
  async _generateRecommendations(reflection, data) {
    const recommendations = [];
    
    // ���������Ľ���
    if (data.quality < 0.6) {
      recommendations.push('Focus on improving output quality');
      recommendations.push('Review and refine the execution process');
    }
    
    // �������ܵĽ���
    if (data.duration > 5000) {
      recommendations.push('Consider performance optimization');
    }
    
    // ������ʷģʽ�Ľ���
    const successPatterns = this.experienceStore.getSuccessPatterns(data.task, 0.8);
    if (successPatterns.length > 0) {
      recommendations.push(`Apply successful pattern: ${successPatterns[0].description || 'best practice'}`);
    }
    
    // ���ڳ�������Ľ���
    const mistakes = this.experienceStore.getCommonMistakes(data.task, 3);
    if (mistakes.length > 0) {
      recommendations.push('Review common failure patterns to avoid repetition');
    }
    
    reflection.recommendations = recommendations;
  }

  /**
   * �������Ŷ�
   */
  _calculateConfidence(reflection) {
    let confidence = 0.5;
    
    // ���ڽ��
    if (reflection.result === 'success') {
      confidence += 0.2;
    }
    
    // ��������
    confidence += reflection.quality * 0.2;
    
    // ���ڶ�������
    confidence += Math.min(reflection.insights.length * 0.05, 0.15);
    
    // ����ģʽʶ��
    confidence += Math.min(reflection.patterns.length * 0.05, 0.15);
    
    return Math.min(confidence, 1.0);
  }

  /**
   * ��ȡ��˼��¼
   */
  getReflection(reflectionId) {
    return this.reflections.get(reflectionId);
  }

  /**
   * ��ȡ��������з�˼
   */
  getReflectionsByTask(taskId) {
    return Array.from(this.reflections.values())
      .filter(r => r.taskId === taskId);
  }

  /**
   * ��ȡ�����ͳ��
   */
  getExperienceStatistics() {
    return this.experienceStore.getStatistics();
  }

  /**
   * ��ȡѧϰ����
   */
  getLearningProgress() {
    const stats = this.experienceStore.getStatistics();
    const totalPatterns = this.experienceStore.patterns.size;
    const validatedPatterns = Array.from(this.experienceStore.patterns.values())
      .filter(p => p.frequency >= this.experienceStore.options.minPatternFrequency).length;
    
    return {
      totalExperiences: stats.totalExperiences,
      successRate: stats.successRate,
      patternsIdentified: totalPatterns,
      validatedPatterns,
      lessonsLearned: stats.lessonCount,
      learningStage: this._determineLearningStage(stats)
    };
  }

  /**
   * ȷ��ѧϰ�׶�
   */
  _determineLearningStage(stats) {
    if (stats.totalExperiences < 10) {
      return 'exploration';
    } else if (stats.totalExperiences < 50) {
      return 'pattern_recognition';
    } else if (stats.successRate > 0.8) {
      return 'mastery';
    } else {
      return 'refinement';
    }
  }

  /**
   * ����������
   */
  cleanup(maxAge) {
    this.experienceStore.cleanup(maxAge);
    
    // �����ɷ�˼
    const cutoff = Date.now() - (maxAge || 30 * 24 * 60 * 60 * 1000);
    for (const [id, reflection] of this.reflections) {
      if (reflection.timestamp < cutoff) {
        this.reflections.delete(id);
      }
    }
  }
}

module.exports = {
  ReflectionEngine,
  ReflectionRecord,
  ExperienceStore
};
