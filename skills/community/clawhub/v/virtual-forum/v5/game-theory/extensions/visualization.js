/**
 * 博弈论可视化模块
 * Game Theory Visualization
 */

class GameTheoryVisualizer {
  constructor() {
    this.colors = {
      player1: '#FF6B6B',
      player2: '#4ECDC4',
      nature: '#95E1D3',
      equilibrium: '#F38181'
    };
  }

  /**
   * 可视化收益矩阵
   */
  visualizePayoffMatrix(matrix, players) {
    const strategies = [...new Set(Object.keys(matrix).map(k => k.split('-')[0]))];
    
    let html = '<table style="border-collapse: collapse;">';
    html += '<tr><th></th>' + strategies.map(s => `<th>${s}</th>`).join('') + '</tr>';
    
    for (const s1 of strategies) {
      html += `<tr><th>${s1}</th>`;
      for (const s2 of strategies) {
        const key = `${s1}-${s2}`;
        const payoff = matrix[key];
        html += `<td style="padding: 10px; border: 1px solid #ccc;">${payoff[0]}, ${payoff[1]}</td>`;
      }
      html += '</tr>';
    }
    
    html += '</table>';
    return html;
  }

  /**
   * 生成Mermaid博弈树
   */
  generateGameTreeMermaid(gameTree) {
    const lines = ['graph TD'];
    let nodeId = 0;
    
    const traverse = (node, parent = null, label = '') => {
      const id = `N${nodeId++}`;
      const name = node.player || `End(${JSON.stringify(node.payoff)})`;
      lines.push(`  ${id}["${name}"]`);
      
      if (parent) {
        lines.push(`  ${parent} -->|"${label}"| ${id}`);
      }
      
      for (const action of node.actions || []) {
        traverse(action.child, id, action.name);
      }
      
      return id;
    };
    
    traverse(gameTree);
    return lines.join('\n');
  }
}

module.exports = GameTheoryVisualizer;
