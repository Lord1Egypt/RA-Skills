/**
 * ABTester - A/B 测试框架
 * 提供对照组设计、随机分组、统计显著性检验和结果分析
 */

class ABTester {
  constructor(options = {}) {
    this.options = {
      confidenceLevel: options.confidenceLevel || 0.95,
      minSampleSize: options.minSampleSize || 100,
      maxIterations: options.maxIterations || 1000,
      ...options
    };
    this.experiments = new Map();
    this.results = new Map();
  }

  /**
   * 创建对照实验
   * @param {string} name - 实验名称
   * @param {object} config - 实验配置
   * @param {function} config.control - 对照组函数
   * @param {function} config.treatment - 实验组函数
   * @param {string} config.metric - 评估指标 (duration, success, score)
   */
  createExperiment(name, config) {
    if (!config.control || typeof config.control !== 'function') {
      throw new Error(`Experiment "${name}" must have a control function`);
    }
    if (!config.treatment || typeof config.treatment !== 'function') {
      throw new Error(`Experiment "${name}" must have a treatment function`);
    }

    this.experiments.set(name, {
      name,
      control: config.control,
      treatment: config.treatment,
      metric: config.metric || 'duration',
      higherIsBetter: config.higherIsBetter !== false // 默认越高越好
    });
  }

  /**
   * 移除实验
   */
  removeExperiment(name) {
    this.experiments.delete(name);
    this.results.delete(name);
  }

  /**
   * 运行单个实验
   * @param {string} name - 实验名称
   * @param {object} options - 运行选项
   * @param {number} options.sampleSize - 样本大小
   */
  async run(name, options = {}) {
    const experiment = this.experiments.get(name);
    if (!experiment) {
      throw new Error(`Experiment "${name}" not found`);
    }

    const sampleSize = options.sampleSize || this.options.minSampleSize;
    const controlResults = [];
    const treatmentResults = [];

    // 随机分组并运行测试
    for (let i = 0; i < sampleSize; i++) {
      const isControl = this.randomAssignment();
      
      try {
        const startTime = performance.now();
        let result;
        
        if (isControl) {
          result = await experiment.control();
        } else {
          result = await experiment.treatment();
        }
        
        const endTime = performance.now();
        const duration = endTime - startTime;
        
        const measurement = {
          iteration: i,
          duration,
          success: result !== null && result !== undefined && result !== false,
          value: result,
          timestamp: Date.now()
        };

        if (isControl) {
          controlResults.push(measurement);
        } else {
          treatmentResults.push(measurement);
        }
      } catch (e) {
        // 记录失败但不中断
        const measurement = {
          iteration: i,
          duration: 0,
          success: false,
          error: e.message,
          timestamp: Date.now()
        };
        
        if (isControl) {
          controlResults.push(measurement);
        } else {
          treatmentResults.push(measurement);
        }
      }
    }

    const result = this.analyzeResults(experiment, controlResults, treatmentResults);
    this.results.set(name, result);
    return result;
  }

  /**
   * 运行所有实验
   */
  async runAll(options = {}) {
    const results = {};
    
    for (const name of this.experiments.keys()) {
      results[name] = await this.run(name, options);
    }
    
    return results;
  }

  /**
   * 随机分组
   */
  randomAssignment() {
    return Math.random() < 0.5;
  }

  /**
   * 分析实验结果
   */
  analyzeResults(experiment, controlResults, treatmentResults) {
    const controlMetrics = this.calculateGroupMetrics(controlResults, experiment.metric);
    const treatmentMetrics = this.calculateGroupMetrics(treatmentResults, experiment.metric);

    // 计算统计显著性
    const statisticalTest = this.performTTest(controlMetrics.values, treatmentMetrics.values);
    
    // 确定获胜方
    const winner = this.determineWinner(experiment, controlMetrics, treatmentMetrics, statisticalTest);
    
    // 计算改进幅度
    const improvement = this.calculateImprovement(experiment, controlMetrics, treatmentMetrics);

    return {
      experimentName: experiment.name,
      sampleSize: {
        control: controlResults.length,
        treatment: treatmentResults.length,
        total: controlResults.length + treatmentResults.length
      },
      metrics: {
        control: controlMetrics,
        treatment: treatmentMetrics
      },
      statisticalTest,
      winner,
      improvement,
      confidence: statisticalTest.confidence,
      isSignificant: statisticalTest.isSignificant,
      recommendation: this.generateRecommendation(winner, statisticalTest, improvement)
    };
  }

  /**
   * 计算组内指标
   */
  calculateGroupMetrics(results, metricType) {
    const successfulResults = results.filter(r => r.success);
    const successRate = successfulResults.length / results.length;
    
    let values;
    if (metricType === 'duration') {
      values = successfulResults.map(r => r.duration);
    } else if (metricType === 'score' && successfulResults.length > 0) {
      values = successfulResults.map(r => {
        const val = typeof r.value === 'number' ? r.value : 0;
        return val;
      });
    } else {
      values = successfulResults.map(r => r.duration);
    }

    if (values.length === 0) {
      return {
        mean: 0,
        median: 0,
        stdDev: 0,
        min: 0,
        max: 0,
        successRate: 0,
        values: []
      };
    }

    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const sorted = [...values].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    const min = sorted[0];
    const max = sorted[sorted.length - 1];
    const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);

    return {
      mean: Math.round(mean * 100) / 100,
      median: Math.round(median * 100) / 100,
      stdDev: Math.round(stdDev * 100) / 100,
      min: Math.round(min * 100) / 100,
      max: Math.round(max * 100) / 100,
      successRate: Math.round(successRate * 100) / 100,
      values
    };
  }

  /**
   * 执行 t 检验
   */
  performTTest(controlValues, treatmentValues) {
    if (controlValues.length < 2 || treatmentValues.length < 2) {
      return {
        tStatistic: 0,
        pValue: 1,
        confidence: 0,
        isSignificant: false,
        degreesOfFreedom: 0
      };
    }

    const controlMean = controlValues.reduce((a, b) => a + b, 0) / controlValues.length;
    const treatmentMean = treatmentValues.reduce((a, b) => a + b, 0) / treatmentValues.length;
    
    const controlVar = this.calculateVariance(controlValues, controlMean);
    const treatmentVar = this.calculateVariance(treatmentValues, treatmentMean);
    
    const pooledStd = Math.sqrt((controlVar + treatmentVar) / 2);
    
    if (pooledStd === 0) {
      return {
        tStatistic: 0,
        pValue: 1,
        confidence: 0,
        isSignificant: false,
        degreesOfFreedom: controlValues.length + treatmentValues.length - 2
      };
    }

    const standardError = pooledStd * Math.sqrt(1 / controlValues.length + 1 / treatmentValues.length);
    const tStatistic = (treatmentMean - controlMean) / standardError;
    const degreesOfFreedom = controlValues.length + treatmentValues.length - 2;
    
    // 简化的 p-value 计算 (使用正态分布近似)
    const pValue = this.calculatePValue(Math.abs(tStatistic), degreesOfFreedom);
    const confidence = 1 - pValue;
    const isSignificant = pValue < (1 - this.options.confidenceLevel);

    return {
      tStatistic: Math.round(tStatistic * 1000) / 1000,
      pValue: Math.round(pValue * 10000) / 10000,
      confidence: Math.round(confidence * 10000) / 10000,
      isSignificant,
      degreesOfFreedom
    };
  }

  /**
   * 计算方差
   */
  calculateVariance(values, mean) {
    return values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length;
  }

  /**
   * 计算 p-value (简化版)
   */
  calculatePValue(tStat, df) {
    // 使用简化的正态分布近似
    // 对于大样本，t 分布接近正态分布
    const z = tStat;
    // 简化的累积分布函数近似
    const p = Math.exp(-0.5 * z * z) / (z * Math.sqrt(2 * Math.PI) + 0.5);
    return Math.min(1, Math.max(0, p * 2)); // 双尾检验
  }

  /**
   * 确定获胜方
   */
  determineWinner(experiment, controlMetrics, treatmentMetrics, statisticalTest) {
    if (!statisticalTest.isSignificant) {
      return 'none'; // 没有显著差异
    }

    const controlBetter = experiment.higherIsBetter 
      ? controlMetrics.mean > treatmentMetrics.mean
      : controlMetrics.mean < treatmentMetrics.mean;

    return controlBetter ? 'control' : 'treatment';
  }

  /**
   * 计算改进幅度
   */
  calculateImprovement(experiment, controlMetrics, treatmentMetrics) {
    if (controlMetrics.mean === 0) {
      return treatmentMetrics.mean === 0 ? 0 : Infinity;
    }

    const rawImprovement = (treatmentMetrics.mean - controlMetrics.mean) / controlMetrics.mean;
    
    // 如果越低越好，反转符号
    const improvement = experiment.higherIsBetter ? rawImprovement : -rawImprovement;
    
    return Math.round(improvement * 10000) / 10000;
  }

  /**
   * 生成建议
   */
  generateRecommendation(winner, statisticalTest, improvement) {
    if (!statisticalTest.isSignificant) {
      return 'No significant difference detected. Consider increasing sample size or running longer.';
    }

    if (winner === 'treatment') {
      const percent = Math.abs(improvement * 100).toFixed(2);
      return `Treatment shows ${percent}% improvement with ${(statisticalTest.confidence * 100).toFixed(1)}% confidence. Consider deploying treatment.`;
    } else {
      const percent = Math.abs(improvement * 100).toFixed(2);
      return `Control performs ${percent}% better. Keep current implementation.`;
    }
  }

  /**
   * 获取实验结果
   */
  getResults(experimentName) {
    if (experimentName) {
      return this.results.get(experimentName);
    }
    return Object.fromEntries(this.results);
  }

  /**
   * 清空结果
   */
  clearResults() {
    this.results.clear();
  }

  /**
   * 获取实验列表
   */
  getExperimentList() {
    return Array.from(this.experiments.keys());
  }
}

module.exports = { ABTester };
