/**
 * Reinforcement Learning Module
 * Q-Learning implementation with customizable rewards
 */

export default class ReinforcementLearner {
  constructor(options = {}) {
    this.learningRate = options.learningRate || 0.1;
    this.discountFactor = options.discountFactor || 0.9;
    this.epsilon = options.epsilon || 0.1; // Exploration rate
    this.epsilonDecay = options.epsilonDecay || 0.995;
    this.minEpsilon = options.minEpsilon || 0.01;
    
    // Store config for selectAction fallback
    this.states = options.states;
    this.actions = options.actions;
    
    // Q-table: state -> action -> value
    this.qTable = new Map();
    
    // State-action history for learning
    this.history = [];
    
    // Reward shaping function
    this.rewardFunction = options.rewardFunction || this.defaultRewardFunction;
    
    // Episode tracking
    this.episodeCount = 0;
    this.totalReward = 0;
  }

  /**
   * Default reward function
   */
  defaultRewardFunction(state, action, nextState, outcome) {
    return outcome?.reward || 0;
  }

  /**
   * Get state key for Q-table
   */
  getStateKey(state) {
    if (Array.isArray(state)) {
      return state.join(',');
    }
    if (typeof state === 'object') {
      return JSON.stringify(state);
    }
    return String(state);
  }

  /**
   * Get Q-value for state-action pair
   */
  getQValue(state, action) {
    const stateKey = this.getStateKey(state);
    
    if (!this.qTable.has(stateKey)) {
      this.qTable.set(stateKey, new Map());
    }
    
    const actionValues = this.qTable.get(stateKey);
    return actionValues.get(action) || 0;
  }

  /**
   * Set Q-value for state-action pair
   */
  setQValue(state, action, value) {
    const stateKey = this.getStateKey(state);
    
    if (!this.qTable.has(stateKey)) {
      this.qTable.set(stateKey, new Map());
    }
    
    this.qTable.get(stateKey).set(action, value);
  }

  /**
   * Choose action using epsilon-greedy policy
   */
  chooseAction(state, availableActions) {
    // Exploration
    if (Math.random() < this.epsilon) {
      const randomIndex = Math.floor(Math.random() * availableActions.length);
      return availableActions[randomIndex];
    }
    
    // Exploitation
    let bestAction = availableActions[0];
    let bestValue = this.getQValue(state, bestAction);
    
    for (const action of availableActions) {
      const value = this.getQValue(state, action);
      if (value > bestValue) {
        bestValue = value;
        bestAction = action;
      }
    }
    
    return bestAction;
  }

  /**
   * Get all Q-values for a state
   */
  getStateValues(state) {
    const stateKey = this.getStateKey(state);
    const actionValues = this.qTable.get(stateKey);
    
    if (!actionValues) return {};
    
    const values = {};
    for (const [action, value] of actionValues) {
      values[action] = value;
    }
    
    return values;
  }

  /**
   * Select action (alias for chooseAction for test compatibility)
   */
  selectAction(state, availableActions) {
    // If availableActions not provided, try to infer from states/actions config
    if (!availableActions && this.states && this.actions) {
      availableActions = Array.from({ length: this.actions }, (_, i) => i);
    }
    if (!availableActions) {
      availableActions = [0, 1]; // Default fallback
    }
    return this.chooseAction(state, availableActions);
  }

  /**
   * Get best action for a state
   */
  getBestAction(state, availableActions) {
    let bestAction = availableActions[0];
    let bestValue = this.getQValue(state, bestAction);
    
    for (const action of availableActions) {
      const value = this.getQValue(state, action);
      if (value > bestValue) {
        bestValue = value;
        bestAction = action;
      }
    }
    
    return { action: bestAction, value: bestValue };
  }

  /**
   * Update Q-value using Q-learning formula
   */
  learn(state, action, reward, nextState, availableNextActions) {
    const currentQ = this.getQValue(state, action);
    
    // Get max Q-value for next state
    let maxNextQ = 0;
    if (availableNextActions && availableNextActions.length > 0) {
      const best = this.getBestAction(nextState, availableNextActions);
      maxNextQ = best.value;
    }
    
    // Q-learning update rule
    const newQ = currentQ + this.learningRate * (
      reward + this.discountFactor * maxNextQ - currentQ
    );
    
    this.setQValue(state, action, newQ);
    
    // Record history
    this.history.push({
      state: this.getStateKey(state),
      action,
      reward,
      nextState: this.getStateKey(nextState),
      qValue: newQ
    });
    
    this.totalReward += reward;
    
    return newQ;
  }

  /**
   * Process a complete step
   */
  step(config) {
    const {
      state,
      actions,
      nextState,
      outcome,
      nextActions
    } = config;
    
    // Choose action
    const action = this.chooseAction(state, actions);
    
    // Calculate reward
    const reward = this.rewardFunction(state, action, nextState, outcome);
    
    // Update Q-value
    this.learn(state, action, reward, nextState, nextActions || actions);
    
    // Decay epsilon
    this.epsilon = Math.max(
      this.minEpsilon,
      this.epsilon * this.epsilonDecay
    );
    
    return {
      action,
      reward,
      epsilon: this.epsilon
    };
  }

  /**
   * End episode and reset tracking
   */
  endEpisode() {
    this.episodeCount++;
    
    const summary = {
      episode: this.episodeCount,
      totalReward: this.totalReward,
      steps: this.history.length,
      epsilon: this.epsilon
    };
    
    this.totalReward = 0;
    
    return summary;
  }

  /**
   * Get policy (best action for each state)
   */
  getPolicy() {
    const policy = {};
    
    for (const [stateKey, actionValues] of this.qTable) {
      let bestAction = null;
      let bestValue = -Infinity;
      
      for (const [action, value] of actionValues) {
        if (value > bestValue) {
          bestValue = value;
          bestAction = action;
        }
      }
      
      policy[stateKey] = { action: bestAction, value: bestValue };
    }
    
    return policy;
  }

  /**
   * Get learning statistics
   */
  getStats() {
    let totalStates = 0;
    let totalActions = 0;
    let maxQ = -Infinity;
    let minQ = Infinity;
    let sumQ = 0;
    
    for (const actionValues of this.qTable.values()) {
      totalStates++;
      for (const value of actionValues.values()) {
        totalActions++;
        maxQ = Math.max(maxQ, value);
        minQ = Math.min(minQ, value);
        sumQ += value;
      }
    }
    
    return {
      states: totalStates,
      actions: totalActions,
      episodes: this.episodeCount,
      epsilon: this.epsilon,
      qValueRange: { min: minQ === Infinity ? 0 : minQ, max: maxQ === -Infinity ? 0 : maxQ },
      avgQ: totalActions > 0 ? sumQ / totalActions : 0,
      historyLength: this.history.length
    };
  }

  /**
   * Reset learner
   */
  reset() {
    this.qTable.clear();
    this.history = [];
    this.episodeCount = 0;
    this.totalReward = 0;
    this.epsilon = 0.1;
  }

  /**
   * Export Q-table
   */
  export() {
    const data = {};
    
    for (const [stateKey, actionValues] of this.qTable) {
      data[stateKey] = {};
      for (const [action, value] of actionValues) {
        data[stateKey][action] = value;
      }
    }
    
    return {
      qTable: data,
      config: {
        learningRate: this.learningRate,
        discountFactor: this.discountFactor,
        epsilon: this.epsilon,
        epsilonDecay: this.epsilonDecay,
        minEpsilon: this.minEpsilon
      },
      stats: this.getStats()
    };
  }

  /**
   * Import Q-table
   */
  import(data) {
    this.qTable.clear();
    
    for (const [stateKey, actionValues] of Object.entries(data.qTable)) {
      const actionMap = new Map();
      for (const [action, value] of Object.entries(actionValues)) {
        actionMap.set(action, value);
      }
      this.qTable.set(stateKey, actionMap);
    }
    
    if (data.config) {
      this.learningRate = data.config.learningRate || this.learningRate;
      this.discountFactor = data.config.discountFactor || this.discountFactor;
      this.epsilon = data.config.epsilon || this.epsilon;
    }
    
    return this;
  }
}
