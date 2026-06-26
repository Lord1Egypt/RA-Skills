/**
 * 战略式博弈 (Strategic Game)
 * 基于 Osborne & Rubinstein 第2章 / Bonanno 第2,6章
 * 
 * 支持：纯策略纳什均衡、混合策略均衡、占优策略求解
 */

class StrategicGame {
  constructor(config) {
    this.players = config.players;
    this.strategies = config.strategies;
    this.payoffMatrix = config.payoffMatrix;
  }

  /**
   * 迭代剔除严格劣策略 (IESDS)
   */
  iteratedEliminationOfStrictlyDominatedStrategies() {
    let remainingStrategies = { ...this.strategies };
    let eliminated = [];
    let changed = true;

    while (changed) {
      changed = false;
      
      for (const player of this.players) {
        const playerStrategies = remainingStrategies[player];
        const otherPlayers = this.players.filter(p => p !== player);
        
        for (let i = 0; i < playerStrategies.length; i++) {
          const si = playerStrategies[i];
          
          for (let j = 0; j < playerStrategies.length; j++) {
            if (i === j) continue;
            const sj = playerStrategies[j];
            
            if (this.isStrictlyDominated(player, si, sj, remainingStrategies)) {
              remainingStrategies[player] = playerStrategies.filter(s => s !== si);
              eliminated.push({ player, strategy: si, dominatedBy: sj });
              changed = true;
              break;
            }
          }
        }
      }
    }

    return { remainingStrategies, eliminated };
  }

  isStrictlyDominated(player, si, sj, remainingStrategies) {
    const otherPlayers = this.players.filter(p => p !== player);
    const otherStrategies = otherPlayers.map(p => remainingStrategies[p]);
    const combinations = this.cartesianProduct(otherStrategies);
    
    let strictlyDominated = true;
    let strictlyBetter = false;
    
    for (const combo of combinations) {
      const strategyProfileSi = this.buildProfile(player, si, otherPlayers, combo);
      const strategyProfileSj = this.buildProfile(player, sj, otherPlayers, combo);
      
      const payoffSi = this.getPayoff(strategyProfileSi, player);
      const payoffSj = this.getPayoff(strategyProfileSj, player);
      
      if (payoffSj <= payoffSi) {
        strictlyDominated = false;
        break;
      }
      if (payoffSj > payoffSi) {
        strictlyBetter = true;
      }
    }
    
    return strictlyDominated && strictlyBetter;
  }

  /**
   * 寻找纯策略纳什均衡
   */
  findPureStrategyNashEquilibrium() {
    const equilibria = [];
    const strategyProfiles = this.generateAllStrategyProfiles();
    
    for (const profile of strategyProfiles) {
      if (this.isNashEquilibrium(profile)) {
        equilibria.push({
          profile,
          payoffs: this.players.map(p => this.getPayoff(profile, p))
        });
      }
    }
    
    return equilibria;
  }

  isNashEquilibrium(profile) {
    for (const player of this.players) {
      const currentStrategy = profile[player];
      const currentPayoff = this.getPayoff(profile, player);
      
      for (const alternativeStrategy of this.strategies[player]) {
        if (alternativeStrategy === currentStrategy) continue;
        
        const deviatedProfile = { ...profile, [player]: alternativeStrategy };
        const deviatedPayoff = this.getPayoff(deviatedProfile, player);
        
        if (deviatedPayoff > currentPayoff + 1e-9) {
          return false;
        }
      }
    }
    return true;
  }

  /**
   * 寻找混合策略纳什均衡 (支撑集枚举法)
   * 修复了原迭代法不收敛的问题
   */
  findMixedStrategyNashEquilibrium() {
    if (this.players.length !== 2) {
      throw new Error('混合策略均衡目前仅支持2人博弈');
    }
    
    const [player1, player2] = this.players;
    const strategies1 = this.strategies[player1];
    const strategies2 = this.strategies[player2];
    
    const equilibria = [];
    
    // 枚举所有可能的支撑集组合
    for (const support1 of this.getAllSubsets(strategies1)) {
      for (const support2 of this.getAllSubsets(strategies2)) {
        if (support1.length === 0 || support2.length === 0) continue;
        
        const equilibrium = this.solveSupportEnumeration(support1, support2, player1, player2);
        if (equilibrium && this.verifyMixedNashEquilibrium(equilibrium)) {
          // 去重
          const alreadyFound = equilibria.some(eq => 
            this.mixedProfilesEqual(eq, equilibrium)
          );
          if (!alreadyFound) {
            equilibria.push(equilibrium);
          }
        }
      }
    }
    
    return equilibria;
  }

  /**
   * 支撑集枚举求解 (正确实现)
   * 
   * 原理：在均衡中，支撑集中的所有策略必须产生相同的期望收益
   * 这给出了线性方程组，可以精确求解混合概率
   */
  solveSupportEnumeration(support1, support2, player1, player2) {
    // 对于2人博弈，解以下方程组：
    // 对于player1：support1中所有策略对player2的混合策略无差异
    // 对于player2：support2中所有策略对player1的混合策略无差异
    
    // 构建收益矩阵子矩阵
    const subMatrix1 = this.buildSubMatrix(player1, support1, support2);
    const subMatrix2 = this.buildSubMatrix(player2, support2, support1);
    
    // 求解player2的混合策略使player1无差异
    const mix2 = this.solveIndifference(player1, support1, support2, subMatrix1);
    if (!mix2) return null;
    
    // 求解player1的混合策略使player2无差异
    const mix1 = this.solveIndifference(player2, support2, support1, subMatrix2);
    if (!mix1) return null;
    
    // 验证概率在[0,1]范围内且和为1
    if (!this.isValidMixture(mix1) || !this.isValidMixture(mix2)) {
      return null;
    }
    
    return {
      [player1]: mix1,
      [player2]: mix2,
      support: { [player1]: support1, [player2]: support2 },
      expectedPayoffs: {
        [player1]: this.expectedPayoff(player1, mix1, mix2),
        [player2]: this.expectedPayoff(player2, mix2, mix1)
      }
    };
  }

  /**
   * 构建子矩阵（指定支撑集的收益矩阵）
   */
  buildSubMatrix(player, rowStrategies, colStrategies) {
    const opponent = this.players.find(p => p !== player);
    const matrix = [];
    
    for (const row of rowStrategies) {
      const rowPayoffs = [];
      for (const col of colStrategies) {
        const profile = { [player]: row, [opponent]: col };
        rowPayoffs.push(this.getPayoff(profile, player));
      }
      matrix.push(rowPayoffs);
    }
    
    return matrix;
  }

  /**
   * 求解无差异方程
   * 
   * 对于支撑集S中的k个策略，需要：
   * U(s_1, σ) = U(s_2, σ) = ... = U(s_k, σ)
   * 
   * 这给出了k-1个独立方程，加上概率和为1的约束
   */
  solveIndifference(player, support, opponentSupport, subMatrix) {
    const k = support.length;
    const m = opponentSupport.length;
    
    if (k === 1) {
      // 纯策略：对面以概率1选择该策略
      const mix = {};
      for (const s of this.strategies[this.players.find(p => p !== player)]) {
        mix[s] = opponentSupport.includes(s) ? 1 : 0;
      }
      return mix;
    }
    
    if (k === 2) {
      // 2个策略的无差异：解一个方程
      // U(s1, σ) = U(s2, σ)
      // p*U(s1,t1) + (1-p)*U(s1,t2) = p*U(s2,t1) + (1-p)*U(s2,t2)
      
      const u11 = subMatrix[0][0];
      const u12 = subMatrix[0][1] || subMatrix[0][0];
      const u21 = subMatrix[1][0];
      const u22 = subMatrix[1][1] || subMatrix[1][0];
      
      // (u11 - u21) * p + (u12 - u22) * (1-p) = 0
      // p = (u22 - u12) / (u11 - u21 + u22 - u12)
      const denominator = u11 - u21 - u12 + u22;
      
      if (Math.abs(denominator) < 1e-10) {
        return null; // 方程无解或无穷解
      }
      
      const p = (u22 - u12) / denominator;
      
      const mix = {};
      for (const s of this.strategies[this.players.find(p => p !== player)]) {
        mix[s] = 0;
      }
      mix[opponentSupport[0]] = p;
      if (opponentSupport[1]) {
        mix[opponentSupport[1]] = 1 - p;
      }
      
      return mix;
    }
    
    // 对于k>2，需要解线性方程组
    // 简化为使用矩阵求解
    return this.solveGeneralIndifference(subMatrix, opponentSupport);
  }

  /**
   * 一般情况的无差异求解 (k>2)
   */
  solveGeneralIndifference(subMatrix, opponentSupport) {
    // 使用高斯消元求解
    const k = subMatrix.length;
    const m = opponentSupport.length;
    
    // 构建增广矩阵: (k-1)个方程，m个未知数
    // 方程形式: Σ_j p_j * (u_{1j} - u_{ij}) = 0 for i = 2..k
    // 约束: Σ_j p_j = 1
    
    const A = [];
    const b = [];
    
    // 无差异方程
    for (let i = 1; i < k; i++) {
      const row = [];
      for (let j = 0; j < m; j++) {
        row.push(subMatrix[0][j] - subMatrix[i][j]);
      }
      A.push(row);
      b.push(0);
    }
    
    // 概率和为1
    const sumRow = Array(m).fill(1);
    A.push(sumRow);
    b.push(1);
    
    // 求解
    const solution = this.solveLinearSystem(A, b);
    if (!solution) return null;
    
    const mix = {};
    for (const s of this.strategies[this.players.find(p => p !== this.players[0])]) {
      mix[s] = 0;
    }
    opponentSupport.forEach((s, i) => {
      mix[s] = solution[i];
    });
    
    return mix;
  }

  /**
   * 解线性方程组 (高斯消元)
   */
  solveLinearSystem(A, b) {
    const n = A.length;
    const m = A[0].length;
    
    if (n !== m) {
      // 使用最小二乘或检查是否有唯一解
      return null;
    }
    
    // 前向消元
    const augmented = A.map((row, i) => [...row, b[i]]);
    
    for (let i = 0; i < n; i++) {
      // 找主元
      let maxRow = i;
      for (let k = i + 1; k < n; k++) {
        if (Math.abs(augmented[k][i]) > Math.abs(augmented[maxRow][i])) {
          maxRow = k;
        }
      }
      
      // 交换
      [augmented[i], augmented[maxRow]] = [augmented[maxRow], augmented[i]];
      
      // 如果主元为0，矩阵奇异
      if (Math.abs(augmented[i][i]) < 1e-10) {
        return null;
      }
      
      // 消元
      for (let k = i + 1; k < n; k++) {
        const factor = augmented[k][i] / augmented[i][i];
        for (let j = i; j <= n; j++) {
          augmented[k][j] -= factor * augmented[i][j];
        }
      }
    }
    
    // 回代
    const solution = Array(n).fill(0);
    for (let i = n - 1; i >= 0; i--) {
      solution[i] = augmented[i][n];
      for (let j = i + 1; j < n; j++) {
        solution[i] -= augmented[i][j] * solution[j];
      }
      solution[i] /= augmented[i][i];
    }
    
    return solution;
  }

  /**
   * 验证混合策略是否为有效纳什均衡
   */
  verifyMixedNashEquilibrium(equilibrium) {
    const [player1, player2] = this.players;
    const mix1 = equilibrium[player1];
    const mix2 = equilibrium[player2];
    
    // 检查支撑集外是否有更高收益的策略
    for (const player of this.players) {
      const myMix = player === player1 ? mix1 : mix2;
      const oppMix = player === player1 ? mix2 : mix1;
      const currentPayoff = this.expectedPayoff(player, myMix, oppMix);
      
      for (const strategy of this.strategies[player]) {
        const strategyMix = { [strategy]: 1 };
        const strategyPayoff = this.expectedPayoff(
          player, 
          Object.fromEntries(this.strategies[player].map(s => [s, s === strategy ? 1 : 0])),
          oppMix
        );
        
        if (strategyPayoff > currentPayoff + 1e-6) {
          return false; // 存在有利偏离
        }
      }
    }
    
    return true;
  }

  /**
   * 检查混合策略是否有效
   */
  isValidMixture(mixture) {
    let sum = 0;
    for (const prob of Object.values(mixture)) {
      if (prob < -1e-6 || prob > 1 + 1e-6) {
        return false;
      }
      sum += prob;
    }
    return Math.abs(sum - 1) < 1e-6;
  }

  /**
   * 比较两个混合策略配置是否相等
   */
  mixedProfilesEqual(eq1, eq2) {
    for (const player of this.players) {
      if (!this.mixturesEqual(eq1[player], eq2[player])) {
        return false;
      }
    }
    return true;
  }

  // ... 其他方法保持不变 ...

  expectedPayoff(player, myMixture, opponentMixture) {
    let expected = 0;
    const opponent = this.players.find(p => p !== player);
    
    for (const [myStrategy, myProb] of Object.entries(myMixture)) {
      if (myProb === 0) continue;
      
      for (const [oppStrategy, oppProb] of Object.entries(opponentMixture)) {
        if (oppProb === 0) continue;
        
        const profile = { [player]: myStrategy, [opponent]: oppStrategy };
        expected += myProb * oppProb * this.getPayoff(profile, player);
      }
    }
    
    return expected;
  }

  cartesianProduct(arrays) {
    if (arrays.length === 0) return [[]];
    if (arrays.length === 1) return arrays[0].map(a => [a]);
    
    const result = [];
    const [first, ...rest] = arrays;
    const restProduct = this.cartesianProduct(rest);
    
    for (const item of first) {
      for (const combo of restProduct) {
        result.push([item, ...combo]);
      }
    }
    return result;
  }

  buildProfile(player, strategy, otherPlayers, otherStrategies) {
    const profile = { [player]: strategy };
    otherPlayers.forEach((p, i) => profile[p] = otherStrategies[i]);
    return profile;
  }

  getAllSubsets(array) {
    const subsets = [[]];
    for (const item of array) {
      const newSubsets = subsets.map(s => [...s, item]);
      subsets.push(...newSubsets);
    }
    return subsets;
  }

  mixturesEqual(m1, m2, epsilon = 1e-6) {
    const keys = new Set([...Object.keys(m1), ...Object.keys(m2)]);
    for (const k of keys) {
      if (Math.abs((m1[k] || 0) - (m2[k] || 0)) > epsilon) return false;
    }
    return true;
  }

  getPayoff(profile, player) {
    const key = this.players.map(p => profile[p]).join('-');
    const payoffs = this.payoffMatrix[key];
    const playerIndex = this.players.indexOf(player);
    return payoffs[playerIndex];
  }

  generateAllStrategyProfiles() {
    const strategyArrays = this.players.map(p => this.strategies[p]);
    const combinations = this.cartesianProduct(strategyArrays);
    
    return combinations.map(combo => {
      const profile = {};
      this.players.forEach((p, i) => profile[p] = combo[i]);
      return profile;
    });
  }
}

module.exports = StrategicGame;
