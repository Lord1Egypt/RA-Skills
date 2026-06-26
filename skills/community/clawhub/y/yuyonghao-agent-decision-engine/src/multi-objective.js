/**
 * Multi-Objective Optimization Module
 * Supports Pareto optimization, weighted objectives, and constraints
 */

export default class MultiObjectiveOptimizer {
  constructor(options = {}) {
    this.epsilon = options.epsilon || 1e-6;
  }

  /**
   * Normalize objective values to [0, 1] range
   */
  normalize(objectives) {
    const normalized = [];
    const groups = {};
    
    // Group by name for normalization
    for (const obj of objectives) {
      if (!groups[obj.name]) groups[obj.name] = [];
      groups[obj.name].push(obj);
    }
    
    for (const obj of objectives) {
      const group = groups[obj.name];
      const values = group.map(g => g.value);
      const min = Math.min(...values);
      const max = Math.max(...values);
      const range = max - min || 1;
      
      let normValue = (obj.value - min) / range;
      if (obj.minimize) normValue = 1 - normValue;
      
      normalized.push({
        ...obj,
        normalized: Math.max(0, Math.min(1, normValue))
      });
    }
    
    return normalized;
  }

  /**
   * Calculate weighted score for objectives
   */
  weightedScore(objectives) {
    const normalized = this.normalize(objectives);
    const totalWeight = normalized.reduce((sum, o) => sum + (o.weight || 1), 0);
    
    return normalized.reduce((score, o) => {
      return score + (o.normalized * (o.weight || 1) / totalWeight);
    }, 0);
  }

  /**
   * Check if solution dominates another (Pareto dominance)
   */
  dominates(a, b) {
    let betterInAtLeastOne = false;
    
    for (let i = 0; i < a.length; i++) {
      const valA = a[i].minimize ? -a[i].value : a[i].value;
      const valB = b[i].minimize ? -b[i].value : b[i].value;
      
      if (valA < valB - this.epsilon) return false;
      if (valA > valB + this.epsilon) betterInAtLeastOne = true;
    }
    
    return betterInAtLeastOne;
  }

  /**
   * Find Pareto front from set of solutions
   */
  findParetoFront(solutions) {
    const front = [];
    
    for (const sol of solutions) {
      let dominated = false;
      
      for (let i = front.length - 1; i >= 0; i--) {
        if (this.dominates(front[i], sol)) {
          dominated = true;
          break;
        }
        if (this.dominates(sol, front[i])) {
          front.splice(i, 1);
        }
      }
      
      if (!dominated) {
        front.push(sol);
      }
    }
    
    return front;
  }

  /**
   * Check if solution satisfies constraints
   */
  checkConstraints(solution, constraints = []) {
    const violations = [];
    
    for (const c of constraints) {
      let satisfied = true;
      const value = solution[c.objective]?.value ?? solution[c.objective];
      
      switch (c.type) {
        case 'lte':
          satisfied = value <= c.threshold;
          break;
        case 'gte':
          satisfied = value >= c.threshold;
          break;
        case 'eq':
          satisfied = Math.abs(value - c.threshold) < this.epsilon;
          break;
        case 'range':
          satisfied = value >= c.min && value <= c.max;
          break;
      }
      
      if (!satisfied) {
        violations.push({
          constraint: c,
          actual: value,
          severity: c.severity || 1
        });
      }
    }
    
    return {
      satisfied: violations.length === 0,
      violations,
      penalty: violations.reduce((sum, v) => sum + v.severity, 0)
    };
  }

  /**
   * Trade-off analysis between objectives
   */
  analyzeTradeoffs(objectives) {
    const pairs = [];
    
    for (let i = 0; i < objectives.length; i++) {
      for (let j = i + 1; j < objectives.length; j++) {
        const a = objectives[i];
        const b = objectives[j];
        
        // Calculate correlation-like metric
        const tradeoff = {
          pair: [a.name, b.name],
          weights: [a.weight, b.weight],
          conflict: (a.minimize !== b.minimize) || 
                    (a.weight > 0.5 && b.weight > 0.5),
          recommendation: a.weight > b.weight ? a.name : b.name
        };
        
        pairs.push(tradeoff);
      }
    }
    
    return pairs;
  }

  /**
   * Main optimization method
   */
  optimize(solutions, constraints = []) {
    // Filter feasible solutions
    const feasible = solutions.filter(sol => {
      const check = this.checkConstraints(sol, constraints);
      return check.satisfied;
    });
    
    const candidates = feasible.length > 0 ? feasible : solutions;
    
    // Find Pareto front
    const paretoFront = this.findParetoFront(candidates);
    
    // Score all solutions
    const scored = candidates.map(sol => ({
      solution: sol,
      score: this.weightedScore(Array.isArray(sol) ? sol : Object.values(sol)),
      isPareto: paretoFront.includes(sol)
    }));
    
    // Sort by score
    scored.sort((a, b) => b.score - a.score);
    
    return {
      best: scored[0],
      paretoFront: scored.filter(s => s.isPareto),
      all: scored,
      tradeoffs: this.analyzeTradeoffs(
        Array.isArray(solutions[0]) ? solutions[0] : Object.values(solutions[0])
      )
    };
  }
}
