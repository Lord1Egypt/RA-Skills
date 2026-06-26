/**
 * Risk Assessment Module
 * Probability evaluation, impact analysis, and risk matrices
 */

export default class RiskAssessor {
  constructor(options = {}) {
    this.probabilityLevels = options.probabilityLevels || [
      { level: 1, label: 'Very Low', min: 0, max: 0.1 },
      { level: 2, label: 'Low', min: 0.1, max: 0.3 },
      { level: 3, label: 'Medium', min: 0.3, max: 0.5 },
      { level: 4, label: 'High', min: 0.5, max: 0.7 },
      { level: 5, label: 'Very High', min: 0.7, max: 1.0 }
    ];
    
    this.impactLevels = options.impactLevels || [
      { level: 1, label: 'Negligible', min: 0, max: 0.1 },
      { level: 2, label: 'Minor', min: 0.1, max: 0.3 },
      { level: 3, label: 'Moderate', min: 0.3, max: 0.5 },
      { level: 4, label: 'Major', min: 0.5, max: 0.7 },
      { level: 5, label: 'Critical', min: 0.7, max: 1.0 }
    ];
  }

  /**
   * Get probability level from value
   */
  getProbabilityLevel(probability) {
    return this.probabilityLevels.find(
      p => probability >= p.min && probability <= p.max
    ) || this.probabilityLevels[2];
  }

  /**
   * Get impact level from value
   */
  getImpactLevel(impact) {
    return this.impactLevels.find(
      i => impact >= i.min && impact <= i.max
    ) || this.impactLevels[2];
  }

  /**
   * Calculate risk score using probability * impact
   */
  calculateRiskScore(probability, impact) {
    return probability * impact;
  }

  /**
   * Get risk rating from score
   */
  getRiskRating(score) {
    if (score < 0.1) return { level: 'Minimal', color: 'green', priority: 1 };
    if (score < 0.25) return { level: 'Low', color: 'lightgreen', priority: 2 };
    if (score < 0.5) return { level: 'Medium', color: 'yellow', priority: 3 };
    if (score < 0.7) return { level: 'High', color: 'orange', priority: 4 };
    return { level: 'Critical', color: 'red', priority: 5 };
  }

  /**
   * Build risk matrix
   */
  buildRiskMatrix() {
    const matrix = [];
    
    for (const prob of this.probabilityLevels) {
      const row = { probability: prob, impacts: [] };
      
      for (const imp of this.impactLevels) {
        const score = this.calculateRiskScore(
          (prob.min + prob.max) / 2,
          (imp.min + imp.max) / 2
        );
        row.impacts.push({
          impact: imp,
          score,
          rating: this.getRiskRating(score)
        });
      }
      
      matrix.push(row);
    }
    
    return matrix;
  }

  /**
   * Assess a single risk
   */
  assessRisk(riskConfig) {
    const {
      id = `risk_${Date.now()}`,
      name = 'Unnamed Risk',
      probability,
      impact,
      category = 'general',
      mitigation = [],
      dependencies = []
    } = riskConfig;

    const probLevel = this.getProbabilityLevel(probability);
    const impLevel = this.getImpactLevel(impact);
    const score = this.calculateRiskScore(probability, impact);
    const rating = this.getRiskRating(score);
    
    // Calculate residual risk after mitigation
    const mitigationEffectiveness = mitigation.reduce((sum, m) => {
      return sum + (m.effectiveness || 0.3);
    }, 0);
    const mitigationFactor = Math.min(0.8, mitigationEffectiveness);
    
    const residualProbability = probability * (1 - mitigationFactor);
    const residualImpact = impact * (1 - mitigationFactor * 0.5);
    const residualScore = this.calculateRiskScore(residualProbability, residualImpact);
    const residualRating = this.getRiskRating(residualScore);

    return {
      id,
      name,
      category,
      probability: {
        value: probability,
        level: probLevel
      },
      impact: {
        value: impact,
        level: impLevel
      },
      score,
      rating,
      mitigation: {
        strategies: mitigation,
        effectiveness: mitigationFactor,
        residualProbability,
        residualImpact,
        residualScore,
        residualRating
      },
      dependencies,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Assess multiple risks
   */
  assessRisks(risks) {
    const assessed = risks.map(r => this.assessRisk(r));
    
    // Calculate aggregate metrics
    const avgScore = assessed.reduce((sum, r) => sum + r.score, 0) / assessed.length;
    const maxRisk = assessed.reduce((max, r) => r.score > max.score ? r : max, assessed[0]);
    const criticalCount = assessed.filter(r => r.rating.level === 'Critical').length;
    
    // Group by category
    const byCategory = {};
    for (const r of assessed) {
      if (!byCategory[r.category]) byCategory[r.category] = [];
      byCategory[r.category].push(r);
    }

    return {
      risks: assessed,
      summary: {
        total: assessed.length,
        averageScore: avgScore,
        highestRisk: maxRisk,
        criticalCount,
        byCategory
      },
      matrix: this.buildRiskMatrix()
    };
  }

  /**
   * Generate mitigation recommendations
   */
  recommendMitigation(risk) {
    const recommendations = [];
    
    if (risk.probability.value > 0.5) {
      recommendations.push({
        type: 'preventive',
        actions: ['Add validation checks', 'Implement monitoring', 'Create alerts'],
        priority: 'high'
      });
    }
    
    if (risk.impact.value > 0.5) {
      recommendations.push({
        type: 'contingency',
        actions: ['Prepare backup plan', 'Allocate reserve resources', 'Define rollback procedure'],
        priority: 'high'
      });
    }
    
    if (risk.rating.level === 'Critical') {
      recommendations.push({
        type: 'immediate',
        actions: ['Escalate to stakeholders', 'Halt dependent activities', 'Form response team'],
        priority: 'urgent'
      });
    }
    
    return recommendations;
  }

  /**
   * Compare risks for prioritization
   */
  prioritizeRisks(risks) {
    return risks
      .map(r => ({
        ...r,
        priorityScore: r.score * 100 + (r.mitigation?.strategies?.length === 0 ? 50 : 0)
      }))
      .sort((a, b) => b.priorityScore - a.priorityScore);
  }
}
