/**
 * Decision Tree Module
 * Tree building, path evaluation, pruning, and visualization
 */

export default class DecisionTree {
  constructor(options = {}) {
    this.id = options.id || `tree_${Date.now()}`;
    this.root = null;
    this.nodes = new Map();
    this.pruningThreshold = options.pruningThreshold || 0.05;
  }

  /**
   * Create a new node
   */
  createNode(config) {
    const node = {
      id: config.id || `node_${this.nodes.size}`,
      type: config.type || 'decision', // decision, chance, terminal
      label: config.label || '',
      value: config.value || 0,
      probability: config.probability || 1,
      children: [],
      parent: config.parent || null,
      depth: config.depth || 0,
      metadata: config.metadata || {}
    };
    
    this.nodes.set(node.id, node);
    return node;
  }

  /**
   * Build tree from configuration
   */
  build(config) {
    const { options, outcomes, probabilities, labels, condition, trueBranch, falseBranch } = config;
    
    // Support simple condition-based tree (for test compatibility)
    if (condition !== undefined) {
      this.root = this.createNode({
        id: 'root',
        type: 'decision',
        label: condition,
        depth: 0
      });
      
      // True branch
      if (trueBranch) {
        const trueNode = this.createNode({
          id: 'true_branch',
          type: trueBranch.action ? 'terminal' : 'decision',
          label: trueBranch.action || trueBranch.condition || 'True',
          value: trueBranch.value || 0,
          parent: this.root.id,
          depth: 1
        });
        this.root.children.push(trueNode.id);
      }
      
      // False branch
      if (falseBranch) {
        const falseNode = this.createNode({
          id: 'false_branch',
          type: falseBranch.action ? 'terminal' : 'decision',
          label: falseBranch.action || falseBranch.condition || 'False',
          value: falseBranch.value || 0,
          parent: this.root.id,
          depth: 1
        });
        this.root.children.push(falseNode.id);
      }
      
      return this.root;
    }
    
    // Standard multi-option build
    this.root = this.createNode({
      id: 'root',
      type: 'decision',
      label: 'Root Decision',
      depth: 0
    });
    
    for (let i = 0; i < options.length; i++) {
      const child = this.createNode({
        id: `option_${i}`,
        type: 'chance',
        label: labels?.[i] || `Option ${options[i]}`,
        value: outcomes[i],
        probability: probabilities?.[i] || 1 / options.length,
        parent: this.root.id,
        depth: 1
      });
      
      this.root.children.push(child.id);
    }
    
    return this.root;
  }

  /**
   * Expand a node with children
   */
  expand(nodeId, children) {
    const parent = this.nodes.get(nodeId);
    if (!parent) return null;
    
    for (const childConfig of children) {
      const child = this.createNode({
        ...childConfig,
        parent: nodeId,
        depth: parent.depth + 1
      });
      
      parent.children.push(child.id);
    }
    
    return parent;
  }

  /**
   * Calculate expected value for a node
   */
  calculateExpectedValue(nodeId) {
    const node = this.nodes.get(nodeId);
    if (!node) return 0;
    
    if (node.type === 'terminal' || node.children.length === 0) {
      return node.value;
    }
    
    if (node.type === 'chance') {
      let expectedValue = 0;
      for (const childId of node.children) {
        const child = this.nodes.get(childId);
        const childValue = this.calculateExpectedValue(childId);
        expectedValue += childValue * (child.probability || 1 / node.children.length);
      }
      return expectedValue;
    }
    
    // Decision node - return max child value
    let maxValue = -Infinity;
    for (const childId of node.children) {
      const childValue = this.calculateExpectedValue(childId);
      maxValue = Math.max(maxValue, childValue);
    }
    return maxValue;
  }

  /**
   * Evaluate tree with given data
   */
  evaluate(data) {
    if (!this.root) return null;
    
    // Simple condition evaluation for test compatibility
    const evaluateCondition = (condition, data) => {
      if (!condition) return true;
      // Simple parser for conditions like "x > 5"
      const match = condition.match(/(\w+)\s*([><=!]+)\s*(.+)/);
      if (match) {
        const [, varName, operator, value] = match;
        const varValue = data[varName];
        const compareValue = isNaN(value) ? value : parseFloat(value);
        
        switch (operator.trim()) {
          case '>': return varValue > compareValue;
          case '<': return varValue < compareValue;
          case '>=': return varValue >= compareValue;
          case '<=': return varValue <= compareValue;
          case '==': return varValue == compareValue;
          case '===': return varValue === compareValue;
          default: return true;
        }
      }
      return true;
    };
    
    const result = evaluateCondition(this.root.label, data);
    
    // Return the appropriate branch result
    if (this.root.children.length >= 2) {
      const selectedId = result ? this.root.children[0] : this.root.children[1];
      const selectedNode = this.nodes.get(selectedId);
      return selectedNode ? { action: selectedNode.label, value: selectedNode.value } : null;
    }
    
    return { result };
  }

  /**
   * Evaluate all paths from root to leaves
   */
  evaluatePaths() {
    const paths = [];
    
    const traverse = (nodeId, currentPath, probability) => {
      const node = this.nodes.get(nodeId);
      if (!node) return;
      
      const path = [...currentPath, node];
      
      if (node.type === 'terminal' || node.children.length === 0) {
        const value = this.calculateExpectedValue(nodeId);
        paths.push({
          nodes: path,
          probability,
          value,
          decisionSequence: path.filter(n => n.type === 'decision').map(n => n.label)
        });
        return;
      }
      
      for (const childId of node.children) {
        const child = this.nodes.get(childId);
        traverse(childId, path, probability * (child.probability || 1));
      }
    };
    
    traverse(this.root.id, [], 1);
    
    // Sort by value descending
    paths.sort((a, b) => b.value - a.value);
    
    return paths;
  }

  /**
   * Find optimal path
   */
  findOptimalPath() {
    const paths = this.evaluatePaths();
    return paths[0] || null;
  }

  /**
   * Prune low-value branches
   */
  prune(threshold = this.pruningThreshold) {
    const optimalValue = this.calculateExpectedValue(this.root.id);
    const minAcceptable = optimalValue * (1 - threshold);
    
    const pruned = [];
    
    const shouldPrune = (nodeId) => {
      const value = this.calculateExpectedValue(nodeId);
      return value < minAcceptable;
    };
    
    const pruneNode = (nodeId) => {
      const node = this.nodes.get(nodeId);
      if (!node) return;
      
      // Check children first
      for (let i = node.children.length - 1; i >= 0; i--) {
        const childId = node.children[i];
        if (shouldPrune(childId)) {
          pruned.push(childId);
          node.children.splice(i, 1);
          this.nodes.delete(childId);
        } else {
          pruneNode(childId);
        }
      }
    };
    
    pruneNode(this.root.id);
    
    return {
      prunedNodes: pruned,
      remainingNodes: this.nodes.size,
      optimalValue: this.calculateExpectedValue(this.root.id)
    };
  }

  /**
   * Get tree statistics
   */
  getStats() {
    let maxDepth = 0;
    let decisionCount = 0;
    let chanceCount = 0;
    let terminalCount = 0;
    
    for (const node of this.nodes.values()) {
      maxDepth = Math.max(maxDepth, node.depth);
      
      switch (node.type) {
        case 'decision': decisionCount++; break;
        case 'chance': chanceCount++; break;
        case 'terminal': terminalCount++; break;
      }
    }
    
    return {
      totalNodes: this.nodes.size,
      maxDepth,
      decisionCount,
      chanceCount,
      terminalCount,
      branchingFactor: this.root ? this.root.children.length : 0
    };
  }

  /**
   * Generate ASCII visualization
   */
  visualize() {
    const lines = [];
    
    const visualizeNode = (nodeId, prefix = '', isLast = true) => {
      const node = this.nodes.get(nodeId);
      if (!node) return;
      
      const connector = isLast ? '└── ' : '├── ';
      const value = node.value !== undefined ? ` (${node.value.toFixed(2)})` : '';
      const prob = node.probability !== 1 ? ` [p=${node.probability.toFixed(2)}]` : '';
      
      lines.push(`${prefix}${connector}${node.label}${value}${prob}`);
      
      const newPrefix = prefix + (isLast ? '    ' : '│   ');
      
      for (let i = 0; i < node.children.length; i++) {
        const childId = node.children[i];
        visualizeNode(childId, newPrefix, i === node.children.length - 1);
      }
    };
    
    if (this.root) {
      lines.push(this.root.label);
      for (let i = 0; i < this.root.children.length; i++) {
        visualizeNode(this.root.children[i], '', i === this.root.children.length - 1);
      }
    }
    
    return lines.join('\n');
  }

  /**
   * Export to JSON
   */
  toJSON() {
    return {
      id: this.id,
      root: this.root,
      nodes: Array.from(this.nodes.entries()),
      stats: this.getStats()
    };
  }

  /**
   * Import from JSON
   */
  fromJSON(data) {
    this.id = data.id;
    this.nodes = new Map(data.nodes);
    this.root = data.root;
    return this;
  }
}
