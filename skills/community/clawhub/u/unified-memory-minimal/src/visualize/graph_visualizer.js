/**
 * Graph Visualizer - Generate interactive knowledge graph HTML
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VISUAL_DIR = MEMORY_DIR;

export function buildGraph(memories) {
  const data = memories || getAllMemories();
  const nodes = [], edges = [];
  const nodeIds = new Set();
  
  for (const mem of data) {
    const memId = mem.id || `mem_${nodes.length}`;
    if (nodeIds.has(memId)) continue;
    nodeIds.add(memId);
    nodes.push({ id: memId, label: (mem.text || '').substring(0, 50), type: mem.category || 'general', size: (mem.importance || 0.5) * 20 + 10 });
    if (Array.isArray(mem.tags)) {
      for (const tag of mem.tags.slice(0, 3)) {
        const tagId = `tag_${tag}`;
        if (!nodeIds.has(tagId)) { nodeIds.add(tagId); nodes.push({ id: tagId, label: tag, type: 'tag', size: 8 }); }
        edges.push({ from: memId, to: tagId, type: 'has_tag', label: 'has' });
      }
    }
  }
  return { nodes, edges };
}

export function generateGraphHtml(graphData) {
  const data = graphData || buildGraph();
  const nodesJson = JSON.stringify(data.nodes);
  const edgesJson = JSON.stringify(data.edges);
  return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>🧠 Knowledge Graph</title>
<script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/standalone/umd/vis-network.min.js"></script>
<style>body{font-family:-apple-system,sans-serif;margin:0;padding:20px;background:#1a1a2e;color:#eee}
h1{color:#4fc3f7;text-align:center}#network{width:100%;height:600px;border:1px solid #333;border-radius:8px;background:#16213e}
.controls{text-align:center;margin:20px 0}.controls button{padding:10px 20px;margin:0 5px;background:#4fc3f7;border:none;border-radius:4px;cursor:pointer}
.stats{text-align:center;color:#888}</style></head>
<body><h1>🧠 Knowledge Graph</h1>
<div class="controls"><button onclick="focusType('preference')">Preference</button>
<button onclick="focusType('decision')">Decision</button><button onclick="resetView()">Reset</button></div>
<div id="network"></div><div class="stats"><span id="nodeCount">0</span> nodes | <span id="edgeCount">0</span> edges</div>
<script>var nodes=new vis.DataSet(${nodesJson});var edges=new vis.DataSet(${edgesJson});
var container=document.getElementById('network');var data={nodes,edges};
var colors={'preference':'#e91e63','decision':'#ff9800','fact':'#2196f3','task':'#4caf50','general':'#9e9e9e','tag':'#00bcd4'};
nodes.forEach(function(n){n.color={background:colors[n.type]||'#9e9e9e',border:colors[n.type]||'#9e9e9e'};nodes.update(n)});
var options={nodes:{shape:'dot',font:{color:'#eee'},borderWidth:2},edges:{width:1,color:{color:'#4fc3f7',opacity:0.6},arrows:{to:{enabled:true,scaleFactor:0.5}}},physics:{forceAtlas2Based:{gravitationalConstant:-50,springLength:100},solver:'forceAtlas2Based',stabilization:{iterations:150}}};
var network=new vis.Network(container,data,options);
document.getElementById('nodeCount').textContent=nodes.length;document.getElementById('edgeCount').textContent=edges.length;
function focusType(t){var sel=nodes.get({filter:function(n){return n.type===t}});if(sel.length>0){network.selectNodes(sel.map(function(n){return n.id}));network.focus(sel[0].id,{scale:1.5,animation:true})}}
function resetView(){network.fit({animation:true})}</script></body></html>`;
}

export function printGraphStats() {
  const graph = buildGraph();
  console.log('\n🕸️  Knowledge Graph Stats\n');
  console.log(`  Nodes: ${graph.nodes.length}`);
  console.log(`  Edges: ${graph.edges.length}`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'save' || args[0] === 'export') {
    mkdirSync(VISUAL_DIR, { recursive: true });
    const file = join(VISUAL_DIR, 'knowledge_graph.html');
    writeFileSync(file, generateGraphHtml(), 'utf-8');
    console.log(`🕸️  Graph saved: ${file}`);
  } else printGraphStats();
}
