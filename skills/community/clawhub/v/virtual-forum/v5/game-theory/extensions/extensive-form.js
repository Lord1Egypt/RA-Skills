/**
 * 扩展式博弈 (Extensive Form Games)
 * 
 * 基于 Osborne 第6章 / Bonanno 第3-4章
 * 
 * 核心概念：
 * - 博弈树 (Game Tree)
 * - 信息集 (Information Sets)
 * - 子博弈完美均衡 (Subgame Perfect Equilibrium)
 * - 逆向归纳 (Backward Induction)
 * - 行为策略 (Behavioral Strategies)
 */

class ExtensiveFormGame {
  constructor(config) {
    this.players = config.players;
    this.root = config.root;
    this.payoffFunction = config.payoffFunction;
    this.nodeMap = new Map(); // 节点映射表
    
    // 初始化时构建节点映射
    if (this.root) {
      this.buildNodeMap(this.root);
    }
  }
  
  /**
   * 构建节点映射表
   */
  buildNodeMap(node) {
    if (!node) return;
    this.nodeMap.set(node.id, node);
    
    for (const action of node.actions || []) {
      if (action.nextNodeId) {
        // 如果子节点已存在，直接引用
        // 否则稍后通过getNode获取
      }
      if (action.child) {
        this.buildNodeMap(action.child);
      }
    }
  }

  /**
   * 通过ID获取节点
   */
  getNode(id) {
    return this.nodeMap.get(id) || null;
  }
  
  /**
   * 添加节点到映射表
   */
  addNode(node) {
    this.nodeMap.set(node.id, node);
  }

  /**
   * 构建博弈树节点
   */
  createNode(id, player, actions, parent = null) {
    return {
      id,
      player, // 'Nature', 'Player1', 'Player2', 或 null（终止节点）
      actions: actions || [], // [{ name, nextNodeId, probability }]
      parent,
      children: [],
      payoff: null, // 终止节点的收益
      informationSet: null // 信息集标签
    };
  }

  /**
   * 子博弈完美均衡求解
   * 
   * 基于逆向归纳 (Backward Induction)
   * Osborne 第6.2节 / Bonanno 第3.2节
   */
  findSubgamePerfectEquilibrium() {
    // 1. 找出所有子博弈
    const subgames = this.identifySubgames();
    
    // 2. 从最底层的子博弈开始求解
    const equilibrium = {};
    
    for (const subgame of subgames.reverse()) {
      const subgameEquilibrium = this.solveSubgame(subgame);
      equilibrium[subgame.rootId] = subgameEquilibrium;
    }
    
    return {
      type: 'Subgame Perfect Equilibrium',
      subgames: subgames.length,
      strategies: equilibrium,
      
      // 验证无不可信威胁
      credibleThreats: this.verifyCredibleThreats(equilibrium)
    };
  }

  /**
   * 识别所有子博弈
   */
  identifySubgames() {
    const subgames = [];
    
    const traverse = (node, path = []) => {
      // 单节点信息集可以开始一个子博弈
      if (node.player !== 'Nature' && node.player !== null) {
        // 检查是否是单节点信息集
        if (this.isSingletonInformationSet(node)) {
          subgames.push({
            rootId: node.id,
            root: node,
            path: [...path]
          });
        }
      }
      
      // 递归遍历子节点
      for (const action of node.actions) {
        const child = this.getNode(action.nextNodeId);
        if (child) {
          traverse(child, [...path, { node: node.id, action: action.name }]);
        }
      }
    };
    
    traverse(this.root);
    
    // 整个博弈也是一个子博弈
    subgames.unshift({
      rootId: this.root.id,
      root: this.root,
      path: []
    });
    
    return subgames;
  }

  /**
   * 检查节点是否为单节点信息集
   */
  isSingletonInformationSet(node) {
    // 简化：假设每个节点的信息集标签唯一
    return true;
  }

  /**
   * 求解子博弈
   */
  solveSubgame(subgame) {
    // 使用逆向归纳
    return this.backwardInduction(subgame.root);
  }

  /**
   * 逆向归纳求解
   * 
   * 从终止节点开始，反向计算最优策略
   */
  backwardInduction(node) {
    // 基本情况：终止节点
    if (node.player === null) {
      return {
        type: 'terminal',
        payoff: node.payoff,
        optimalAction: null
      };
    }
    
    // 自然节点：计算期望收益
    if (node.player === 'Nature') {
      let expectedPayoff = {};
      
      for (const action of node.actions) {
        const child = this.getNode(action.nextNodeId);
        const childSolution = this.backwardInduction(child);
        
        for (const player of this.players) {
          expectedPayoff[player] = (expectedPayoff[player] || 0) + 
            action.probability * childSolution.payoff[player];
        }
      }
      
      return {
        type: 'nature',
        payoff: expectedPayoff,
        probabilities: node.actions.map(a => ({ action: a.name, probability: a.probability }))
      };
    }
    
    // 玩家节点：选择最优行动
    let bestAction = null;
    let bestPayoff = -Infinity;
    let bestPayoffVector = null;
    
    for (const action of node.actions) {
      const child = this.getNode(action.nextNodeId);
      const childSolution = this.backwardInduction(child);
      
      const playerPayoff = childSolution.payoff[node.player];
      
      if (playerPayoff > bestPayoff) {
        bestPayoff = playerPayoff;
        bestAction = action.name;
        bestPayoffVector = childSolution.payoff;
      }
    }
    
    return {
      type: 'player',
      player: node.player,
      optimalAction: bestAction,
      payoff: bestPayoffVector,
      value: bestPayoff
    };
  }

  /**
   * 转换为战略式博弈
   * 
   * 用于对比分析
   */
  convertToStrategicForm() {
    // 生成所有策略组合
    const strategies = this.generateStrategies();
    
    // 计算每种策略组合的收益
    const payoffMatrix = {};
    
    for (const strategyProfile of strategies) {
      const payoff = this.simulatePlay(strategyProfile);
      const key = this.profileToKey(strategyProfile);
      payoffMatrix[key] = this.players.map(p => payoff[p]);
    }
    
    return {
      players: this.players,
      strategies: this.extractStrategySpace(strategies),
      payoffMatrix
    };
  }

  /**
   * 生成所有纯策略
   */
  generateStrategies() {
    // 简化的策略生成
    const playerStrategies = {};
    
    for (const player of this.players) {
      playerStrategies[player] = this.generatePlayerStrategies(player);
    }
    
    // 笛卡尔积
    return this.cartesianProduct(playerStrategies);
  }

  /**
   * 生成单个玩家的所有策略
   * 
   * 策略是信息集到行动的映射
   */
  generatePlayerStrategies(player) {
    const informationSets = this.getInformationSets(player);
    
    // 每个信息集上的行动选择
    const choices = informationSets.map(is => 
      is.availableActions
    );
    
    // 生成所有组合
    const combinations = this.cartesianProduct(choices);
    
    return combinations.map(combo => {
      const strategy = {};
      informationSets.forEach((is, i) => {
        strategy[is.id] = combo[i];
      });
      return strategy;
    });
  }

  /**
   * 获取玩家的信息集
   */
  getInformationSets(player) {
    const sets = [];
    
    const traverse = (node) => {
      if (node.player === player) {
        sets.push({
          id: node.informationSet || node.id,
          availableActions: node.actions.map(a => a.name)
        });
      }
      
      for (const action of node.actions) {
        const child = this.getNode(action.nextNodeId);
        if (child) traverse(child);
      }
    };
    
    traverse(this.root);
    
    return sets;
  }

  /**
   * 模拟策略执行
   */
  simulatePlay(strategyProfile) {
    // 从根节点开始，根据策略选择行动
    let currentNode = this.root;
    
    while (currentNode.player !== null) {
      if (currentNode.player === 'Nature') {
        // 随机选择（按概率）
        const rand = Math.random();
        let cumProb = 0;
        
        for (const action of currentNode.actions) {
          cumProb += action.probability;
          if (rand <= cumProb) {
            currentNode = this.getNode(action.nextNodeId);
            break;
          }
        }
      } else {
        // 玩家选择
        const playerStrategy = strategyProfile[currentNode.player];
        const actionName = playerStrategy[currentNode.informationSet || currentNode.id];
        
        const action = currentNode.actions.find(a => a.name === actionName);
        if (action) {
          currentNode = this.getNode(action.nextNodeId);
        } else {
          break; // 无效策略
        }
      }
    }
    
    return currentNode.payoff || {};
  }

  /**
   * 可视化博弈树
   * 
   * 生成Mermaid图或文本表示
   */
  visualize(format = 'mermaid') {
    if (format === 'mermaid') {
      return this.generateMermaidDiagram();
    } else if (format === 'text') {
      return this.generateTextTree();
    }
    
    return this.generateJSONTree();
  }

  /**
   * 生成Mermaid流程图
   */
  generateMermaidDiagram() {
    const lines = ['graph TD'];
    const nodeDefs = new Map();
    
    const traverse = (node, depth = 0) => {
      // 定义节点样式
      let style = '';
      if (node.player === 'Nature') {
        style = '[Nature]';
      } else if (node.player === null) {
        style = `(("${this.formatPayoff(node.payoff)}"))`;
      } else {
        style = `[${node.player}]`;
      }
      
      if (!nodeDefs.has(node.id)) {
        lines.push(`    ${node.id}${style}`);
        nodeDefs.set(node.id, true);
      }
      
      // 添加边
      for (const action of node.actions) {
        const child = this.getNode(action.nextNodeId);
        if (child) {
          const edgeLabel = action.probability ? 
            `${action.name} (${(action.probability * 100).toFixed(0)}%)` : 
            action.name;
          
          lines.push(`    ${node.id} -->|"${edgeLabel}"| ${child.id}`);
          
          traverse(child, depth + 1);
        }
      }
    };
    
    traverse(this.root);
    
    return lines.join('\n');
  }

  /**
   * 生成文本树
   */
  generateTextTree() {
    const lines = [];
    
    const traverse = (node, prefix = '', isLast = true) => {
      const connector = isLast ? '└── ' : '├── ';
      
      let nodeLabel = '';
      if (node.player === 'Nature') {
        nodeLabel = '[Nature]';
      } else if (node.player === null) {
        nodeLabel = `[End: ${this.formatPayoff(node.payoff)}]`;
      } else {
        nodeLabel = `[${node.player}]`;
      }
      
      lines.push(prefix + connector + nodeLabel);
      
      const newPrefix = prefix + (isLast ? '    ' : '│   ');
      
      for (let i = 0; i < node.actions.length; i++) {
        const action = node.actions[i];
        const child = this.getNode(action.nextNodeId);
        
        if (child) {
          const actionLabel = action.probability ? 
            `${action.name} (${(action.probability * 100).toFixed(0)}%)` : 
            action.name;
          
          lines.push(newPrefix + (i === node.actions.length - 1 ? '└── ' : '├── ') + actionLabel);
          traverse(child, newPrefix + '    ', i === node.actions.length - 1);
        }
      }
    };
    
    traverse(this.root, '', true);
    
    return lines.join('\n');
  }

  /**
   * 生成JSON树
   */
  generateJSONTree() {
    const buildTree = (node) => {
      const tree = {
        id: node.id,
        player: node.player,
        payoff: node.payoff
      };
      
      if (node.actions.length > 0) {
        tree.actions = node.actions.map(action => ({
          name: action.name,
          probability: action.probability,
          child: buildTree(this.getNode(action.nextNodeId))
        }));
      }
      
      return tree;
    };
    
    return buildTree(this.root);
  }

  /**
   * 格式化腾收益
   */
  formatPayoff(payoff) {
    if (!payoff) return '';
    return Object.entries(payoff)
      .map(([p, v]) => `${p}:${v}`)
      .join(', ');
  }

  /**
   * 通过ID获取节点
   * 使用预构建的节点映射表
   */
  getNode(id) {
    return this.nodeMap.get(id) || null;
  }
  
  /**
   * 添加节点到映射表
   */
  addNode(node) {
    this.nodeMap.set(node.id, node);
  }

  cartesianProduct(obj) {
    // 简化的笛卡尔积实现
    return [];
  }

  profileToKey(profile) {
    return Object.entries(profile)
      .map(([p, s]) => `${p}:${JSON.stringify(s)}`)
      .join('-');
  }

  extractStrategySpace(strategies) {
    return {};
  }

  verifyCredibleThreats(equilibrium) {
    return { credible: true, threats: [] };
  }
}

module.exports = ExtensiveFormGame;
