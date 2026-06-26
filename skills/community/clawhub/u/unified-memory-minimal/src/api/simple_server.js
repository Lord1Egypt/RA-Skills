/**
 * Simple HTTP Server - Agent Collaboration System Web UI
 * 
 * No FastAPI dependency, uses built-in Node.js http module
 * 
 * Usage:
 *   node simple_server.js --port 8080
 * 
 * Access: http://localhost:8080
 */

import http from 'http';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const COLLAB_DIR = path.join(MEMORY_DIR, 'collaboration');

const AGENTS_FILE = path.join(COLLAB_DIR, 'agent_profiles.json');
const TASKS_FILE = path.join(COLLAB_DIR, 'tasks.json');
const EVENTS_FILE = path.join(COLLAB_DIR, 'events.jsonl');

await fs.mkdir(COLLAB_DIR, { recursive: true });

// ========== Data Models ==========

class Agent {
  constructor(data) {
    this.agentId = data.agentId || data.agent_id || '';
    this.name = data.name || '';
    this.role = data.role || '';
    this.skills = data.skills || [];
    this.workload = data.workload || 0.0;
    this.status = data.status || 'online';
  }
  
  toJSON() {
    return {
      agent_id: this.agentId,
      name: this.name,
      role: this.role,
      skills: this.skills,
      workload: this.workload,
      status: this.status
    };
  }
}

class Task {
  constructor(data) {
    this.taskId = data.taskId || data.task_id || '';
    this.taskType = data.taskType || data.task_type || '';
    this.description = data.description || '';
    this.requiredSkills = data.requiredSkills || data.required_skills || [];
    this.priority = data.priority || 'normal';
    this.status = data.status || 'pending';
    this.assignedTo = data.assignedTo || data.assigned_to || null;
  }
  
  toJSON() {
    return {
      task_id: this.taskId,
      task_type: this.taskType,
      description: this.description,
      required_skills: this.requiredSkills,
      priority: this.priority,
      status: this.status,
      assigned_to: this.assignedTo
    };
  }
}

// ========== Storage ==========

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function loadAgents() {
  try {
    if (await fileExists(AGENTS_FILE)) {
      const data = JSON.parse(await fs.readFile(AGENTS_FILE, 'utf-8'));
      return Object.fromEntries(
        Object.entries(data).map(([k, v]) => [k, new Agent(v)])
      );
    }
  } catch {}
  return {};
}

async function saveAgents(agents) {
  const data = Object.fromEntries(
    Object.entries(agents).map(([k, v]) => [k, v.toJSON()])
  );
  await fs.writeFile(AGENTS_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

async function loadTasks() {
  try {
    if (await fileExists(TASKS_FILE)) {
      const data = JSON.parse(await fs.readFile(TASKS_FILE, 'utf-8'));
      return Object.fromEntries(
        Object.entries(data).map(([k, v]) => [k, new Task(v)])
      );
    }
  } catch {}
  return {};
}

async function saveTasks(tasks) {
  const data = Object.fromEntries(
    Object.entries(tasks).map(([k, v]) => [k, v.toJSON()])
  );
  await fs.writeFile(TASKS_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

async function logEvent(eventType, data) {
  const event = {
    timestamp: new Date().toISOString(),
    event_type: eventType,
    ...data
  };
  await fs.appendFile(EVENTS_FILE, JSON.stringify(event) + '\n', 'utf-8');
}

// ========== Dashboard HTML ==========

function getDashboardHtml() {
  return `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Agent Collaboration System</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; margin-bottom: 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { color: #666; font-size: 16px; margin-bottom: 15px; }
        .agent { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; }
        .agent:last-child { border-bottom: none; }
        .agent-name { font-weight: bold; }
        .status-online { color: #4caf50; }
        .status-offline { color: #999; }
        .status-busy { color: #ff9800; }
        .task { padding: 10px; border-bottom: 1px solid #eee; }
        .task-status { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
        .status-pending { background: #e3f2fd; color: #1976d2; }
        .status-assigned { background: #fff3e0; color: #f57c00; }
        .status-completed { background: #e8f5e9; color: #388e3c; }
        .btn { background: #1976d2; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #1565c0; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .refresh { color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Agent Collaboration System</h1>
        <p class="refresh">自动刷新于 <span id="time"></span></p>
        
        <div class="grid">
            <div class="card">
                <h2>📝 注册 Agent</h2>
                <form id="registerForm">
                    <div class="form-group">
                        <label>Agent ID</label>
                        <input type="text" name="agent_id" required placeholder="agent_001">
                    </div>
                    <div class="form-group">
                        <label>名称</label>
                        <input type="text" name="name" required placeholder="产品经理">
                    </div>
                    <div class="form-group">
                        <label>角色</label>
                        <select name="role">
                            <option value="pm">PM</option>
                            <option value="architect">架构师</option>
                            <option value="engineer">工程师</option>
                            <option value="qa">QA</option>
                            <option value="devops">DevOps</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>技能 (逗号分隔)</label>
                        <input type="text" name="skills" placeholder="Python, JavaScript">
                    </div>
                    <button type="submit" class="btn">注册</button>
                </form>
            </div>
            
            <div class="card">
                <h2>📋 创建任务</h2>
                <form id="taskForm">
                    <div class="form-group">
                        <label>任务 ID</label>
                        <input type="text" name="task_id" required placeholder="task_001">
                    </div>
                    <div class="form-group">
                        <label>类型</label>
                        <select name="task_type">
                            <option value="development">开发</option>
                            <option value="design">设计</option>
                            <option value="testing">测试</option>
                            <option value="deployment">部署</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>描述</label>
                        <textarea name="description" rows="3" placeholder="任务描述..."></textarea>
                    </div>
                    <button type="submit" class="btn">创建</button>
                </form>
            </div>
        </div>
        
        <div class="card">
            <h2>👥 Agents</h2>
            <div id="agentsList">加载中...</div>
        </div>
        
        <div class="card">
            <h2>📌 Tasks</h2>
            <div id="tasksList">加载中...</div>
        </div>
    </div>
    
    <script>
        const API = '/api';
        
        function updateTime() {
            document.getElementById('time').textContent = new Date().toLocaleTimeString();
        }
        
        async function loadAgents() {
            try {
                const res = await fetch(API + '/agents');
                const data = await res.json();
                const html = data.agents && data.agents.length > 0 
                    ? data.agents.map(a => \`
                        <div class="agent">
                            <span class="agent-name">\${a.name}</span>
                            <span class="status-\${a.status}">\${a.status} (\${(a.workload * 100).toFixed(0)}%)</span>
                        </div>
                    \`).join('')
                    : '<p>暂无 Agent</p>';
                document.getElementById('agentsList').innerHTML = html;
            } catch (e) {
                document.getElementById('agentsList').innerHTML = '<p>加载失败</p>';
            }
        }
        
        async function loadTasks() {
            try {
                const res = await fetch(API + '/tasks');
                const data = await res.json();
                const html = data.tasks && data.tasks.length > 0
                    ? data.tasks.map(t => \`
                        <div class="task">
                            <strong>\${t.task_id}</strong> - \${t.description || '(无描述)'}
                            <span class="task-status status-\${t.status}">\${t.status}</span>
                        </div>
                    \`).join('')
                    : '<p>暂无任务</p>';
                document.getElementById('tasksList').innerHTML = html;
            } catch (e) {
                document.getElementById('tasksList').innerHTML = '<p>加载失败</p>';
            }
        }
        
        document.getElementById('registerForm').onsubmit = async (e) => {
            e.preventDefault();
            const fd = new FormData(e.target);
            await fetch(API + '/agents/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    agent_id: fd.get('agent_id'),
                    name: fd.get('name'),
                    role: fd.get('role'),
                    skills: fd.get('skills').split(',').map(s => s.trim()).filter(Boolean)
                })
            });
            e.target.reset();
            loadAgents();
        };
        
        document.getElementById('taskForm').onsubmit = async (e) => {
            e.preventDefault();
            const fd = new FormData(e.target);
            await fetch(API + '/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    task_id: fd.get('task_id'),
                    task_type: fd.get('task_type'),
                    description: fd.get('description')
                })
            });
            e.target.reset();
            loadTasks();
        };
        
        loadAgents();
        loadTasks();
        updateTime();
        setInterval(() => { loadAgents(); loadTasks(); updateTime(); }, 5000);
    </script>
</body>
</html>`;
}

// ========== URL Parser (Simple) ==========

function parseUrl(urlStr) {
  const url = new URL(urlStr, 'http://localhost');
  return {
    pathname: url.pathname,
    searchParams: url.searchParams
  };
}

// ========== Request Handlers ==========

async function handleListAgents() {
  const agents = await loadAgents();
  return {
    count: Object.keys(agents).length,
    agents: Object.values(agents).map(a => a.toJSON())
  };
}

async function handleGetAgent(agentId) {
  const agents = await loadAgents();
  const agent = agents[agentId];
  return agent ? agent.toJSON() : { error: 'Not found' };
}

async function handleRegisterAgent(data) {
  const agents = await loadAgents();
  const now = new Date().toISOString();
  const agent = new Agent({
    agentId: data.agent_id,
    name: data.name,
    role: data.role,
    skills: data.skills || [],
    status: 'online'
  });
  agents[agent.agentId] = agent;
  await saveAgents(agents);
  await logEvent('agent_registered', { agent_id: agent.agentId, name: agent.name });
  return { status: 'success', agent: agent.toJSON() };
}

async function handleListTasks(status = null) {
  const tasks = await loadTasks();
  let taskList = Object.values(tasks).map(t => t.toJSON());
  if (status) {
    taskList = taskList.filter(t => t.status === status);
  }
  return { count: taskList.length, tasks: taskList };
}

async function handleCreateTask(data) {
  const tasks = await loadTasks();
  const now = new Date().toISOString();
  const task = new Task({
    taskId: data.task_id,
    taskType: data.task_type || 'general',
    description: data.description || '',
    status: 'pending'
  });
  tasks[task.taskId] = task;
  await saveTasks(tasks);
  await logEvent('task_created', { task_id: task.taskId, task_type: task.taskType });
  return { status: 'success', task: task.toJSON() };
}

async function handleAssignTask(data) {
  const tasks = await loadTasks();
  const task = tasks[data.task_id];
  if (!task) return { error: 'Task not found' };
  
  task.status = 'assigned';
  task.assignedTo = data.agent_id;
  await saveTasks(tasks);
  await logEvent('task_assigned', { task_id: task.taskId, agent_id: data.agent_id });
  return { status: 'success' };
}

async function handleCompleteTask(data) {
  const tasks = await loadTasks();
  const task = tasks[data.task_id];
  if (!task) return { error: 'Task not found' };
  
  task.status = 'completed';
  task.result = data.result || {};
  await saveTasks(tasks);
  await logEvent('task_completed', { task_id: task.taskId });
  return { status: 'success' };
}

async function handleStats() {
  const agents = await loadAgents();
  const tasks = await loadTasks();
  const taskList = Object.values(tasks).map(t => t.toJSON());
  
  return {
    agents: { total: Object.keys(agents).length },
    tasks: {
      total: taskList.length,
      pending: taskList.filter(t => t.status === 'pending').length,
      completed: taskList.filter(t => t.status === 'completed').length
    }
  };
}

// ========== HTTP Server ==========

const PORT = parseInt(process.argv.find(a => a.startsWith('--port='))?.split('=')[1]) || 8080;

const server = http.createServer(async (req, res) => {
  const parsed = parseUrl(req.url);
  const path = parsed.pathname;
  const method = req.method;
  
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  res.setHeader('Content-Type', 'application/json');
  
  try {
    let body = '';
    if (['POST', 'PUT', 'PATCH'].includes(method)) {
      body = await new Promise((resolve, reject) => {
        let data = '';
        req.on('data', chunk => data += chunk);
        req.on('end', () => resolve(data));
        req.on('error', reject);
      });
    }
    
    const data = body ? JSON.parse(body) : {};
    const query = parsed.searchParams;
    
    // Routes
    if (path === '/' || path === '/ui') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(getDashboardHtml());
      return;
    }
    
    if (path === '/api/agents' && method === 'GET') {
      res.end(JSON.stringify(await handleListAgents()));
      return;
    }
    
    if (path === '/api/agents' && method === 'POST') {
      res.end(JSON.stringify(await handleRegisterAgent(data)));
      return;
    }
    
    if (path.startsWith('/api/agents/')) {
      const agentId = path.split('/')[3];
      if (method === 'GET') {
        res.end(JSON.stringify(await handleGetAgent(agentId)));
        return;
      }
    }
    
    if (path === '/api/tasks' && method === 'GET') {
      const status = query.get('status');
      res.end(JSON.stringify(await handleListTasks(status)));
      return;
    }
    
    if (path === '/api/tasks' && method === 'POST') {
      res.end(JSON.stringify(await handleCreateTask(data)));
      return;
    }
    
    if (path === '/api/tasks/assign' && method === 'POST') {
      const result = await handleAssignTask(data);
      res.end(JSON.stringify(result));
      return;
    }
    
    if (path === '/api/tasks/complete' && method === 'POST') {
      res.end(JSON.stringify(await handleCompleteTask(data)));
      return;
    }
    
    if (path === '/api/stats' && method === 'GET') {
      res.end(JSON.stringify(await handleStats()));
      return;
    }
    
    if (path === '/api/health' && method === 'GET') {
      res.end(JSON.stringify({ status: 'healthy', timestamp: new Date().toISOString() }));
      return;
    }
    
    // 404
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
    
  } catch (error) {
    console.error('Request error:', error);
    res.writeHead(500);
    res.end(JSON.stringify({ error: error.message }));
  }
});

server.listen(PORT, () => {
  console.log(`
🚀 Simple HTTP Server started
   Port: ${PORT}
   URL:  http://localhost:${PORT}
   UI:   http://localhost:${PORT}/ui
`);
});

export default server;