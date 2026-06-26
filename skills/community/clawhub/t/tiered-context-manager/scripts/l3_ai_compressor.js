/**
 * L3 AI Compression Module
 * 
 * Uses OpenClaw's own AI capability to generate summaries for session compression.
 * This is NOT calling an external API - it uses our own AI.
 * 
 * How it works:
 * 1. Read session content
 * 2. Generate a summary prompt for our AI
 * 3. The summary is written to inbox as a task
 * 4. The main session processes it using AI capability
 * 5. Compressed content is written back
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

const INBOX_DIR = "E:\\zhuazhua\\.openclaw-shared\\memory\\inbox";
const L3_COMPRESS_FILE = path.join(INBOX_DIR, "l3_ai_compression_tasks.md");
const L3_RESULTS_DIR = path.join(INBOX_DIR, "l3_results");
const LOG_FILE = path.join(INBOX_DIR, "l3_compression_log.md");

// Token estimation
function estimateTokens(text) {
  if (!text || typeof text !== "string") return 0;
  const chinese = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const english = (text.match(/[a-zA-Z]/g) || []).length;
  const other = text.length - chinese - english;
  return Math.ceil(chinese * 1.5) + Math.ceil(english * 0.25) + other;
}

/**
 * Read session file and extract messages
 */
function readSessionMessages(sessionFile) {
  try {
    if (!fs.existsSync(sessionFile)) {
      return { messages: [], totalTokens: 0, error: "Session file not found" };
    }
    
    const content = fs.readFileSync(sessionFile, "utf-8");
    const records = [];
    let start = 0;
    
    for (let i = 0; i < content.length - 1; i++) {
      if (content[i] === '}' && content[i+1] === '\n') {
        records.push(content.slice(start, i + 1));
        start = i + 2;
      }
    }
    const lastRecord = content.slice(start).trim();
    if (lastRecord) records.push(lastRecord);
    
    const messages = [];
    let totalTokens = 0;
    
    for (const line of records) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message" && obj.message?.content) {
          const msg = {
            id: obj.id,
            role: obj.message.role,
            content: obj.message.content,
            timestamp: obj.timestamp
          };
          
          if (Array.isArray(msg.content)) {
            for (const block of msg.content) {
              if (block.text) {
                totalTokens += estimateTokens(block.text);
              }
            }
          } else if (typeof msg.content === "string") {
            totalTokens += estimateTokens(msg.content);
          }
          
          messages.push(msg);
        }
      } catch (e) {}
    }
    
    return { messages, totalTokens, error: null };
  } catch (e) {
    return { messages: [], totalTokens: 0, error: e.message };
  }
}

/**
 * Generate a summary prompt for the AI
 */
function generateSummaryPrompt(sessionFile, messages, totalTokens) {
  const timestamp = new Date().toISOString();
  const sessionName = path.basename(sessionFile);
  
  // Extract first and last few messages for context
  const firstMsgs = messages.slice(0, 3);
  const lastMsgs = messages.slice(-3);
  
  let contextPreview = "=== First messages ===\n";
  for (const msg of firstMsgs) {
    const content = extractTextContent(msg.content);
    contextPreview += `[${msg.role}]: ${content.slice(0, 300)}\n`;
  }
  
  contextPreview += "\n=== Last messages ===\n";
  for (const msg of lastMsgs) {
    const content = extractTextContent(msg.content);
    contextPreview += `[${msg.role}]: ${content.slice(0, 300)}\n`;
  }
  
  const prompt = `## L3 AI压缩任务

**任务ID**: l3_${Date.now()}
**Session文件**: ${sessionFile}
**Session名称**: ${sessionName}
**时间**: ${timestamp}
**消息数**: ${messages.length}
**估算Token**: ${totalTokens.toFixed(0)}

---

### 任务说明

请用你自己的AI能力压缩这个session的内容。

### 压缩方法

1. **读取session文件**: ${sessionFile}
2. **分析对话内容**: 理解主要讨论的主题、决策、行动
3. **生成摘要**: 创建一个压缩摘要，保留关键信息
4. **写回压缩内容**: 用压缩后的内容替换session中的旧内容

### 压缩规则

- **保留**: 角色、关键决策、重要结论、用户偏好、系统配置
- **压缩**: 详细的工具调用结果、长文本、重复内容
- **格式**: toolResult 简化为 "[tool: name ~X tokens]"
- **摘要格式**: 
  \`\`\`
  [COMPRESSED ${messages.length} messages, ~${totalTokens.toFixed(0)} tokens earlier]
  
  Summary:
  - Topics discussed: ...
  - Key decisions: ...
  - Actions taken: ...
  - Important context: ...
  \`\`\`

### Session内容预览

${contextPreview}

---

### 输出要求

1. 处理完成后，更新任务状态为 done
2. 在结果中说明:
   - 压缩前token数
   - 压缩后token数
   - 节省的token数
   - 压缩效果描述

### 执行

请现在开始处理这个压缩任务。`;

  return prompt;
}

/**
 * Extract text content from various content formats
 */
function extractTextContent(content) {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content.map(block => {
      if (typeof block === "string") return block;
      if (block.text) return block.text;
      if (block.type === "toolCall") return `[tool: ${block.name || 'unknown'}]`;
      if (block.type === "toolResult") return `[result: ${(block.text || '').slice(0, 100)}]`;
      return JSON.stringify(block);
    }).join("\n");
  }
  return String(content);
}

/**
 * Create an L3 compression task in inbox
 */
function createL3Task(sessionFile, tokenBudget, currentTokens, reason) {
  const { messages, totalTokens, error } = readSessionMessages(sessionFile);
  
  if (error) {
    return { ok: false, error };
  }
  
  if (messages.length < 6) {
    return { ok: false, error: "Too few messages for L3 compression" };
  }
  
  const taskId = `l3_${Date.now()}`;
  const timestamp = new Date().toISOString();
  const sessionName = path.basename(sessionFile);
  
  // Generate the prompt
  const prompt = generateSummaryPrompt(sessionFile, messages, totalTokens);
  
  // Ensure directories exist
  if (!fs.existsSync(INBOX_DIR)) {
    fs.mkdirSync(INBOX_DIR, { recursive: true });
  }
  if (!fs.existsSync(L3_RESULTS_DIR)) {
    fs.mkdirSync(L3_RESULTS_DIR, { recursive: true });
  }
  
  // Write task file
  const taskContent = `---\ntype: l3_ai_compression\nstatus: pending\ntask_id: ${taskId}\nfrom: tiered_engine_v2\ntime: ${timestamp}\n---\n\n${prompt}\n`;
  
  fs.appendFileSync(L3_COMPRESS_FILE, taskContent);
  
  // Also create individual task file for easier processing
  const individualTaskFile = path.join(L3_RESULTS_DIR, `${taskId}.md`);
  fs.writeFileSync(individualTaskFile, taskContent);
  
  // Log the task
  const logEntry = `\n- **${timestamp}** | ${sessionName} | ${messages.length} msgs | ~${totalTokens.toFixed(0)} tokens | reason: ${reason}`;
  fs.appendFileSync(LOG_FILE, logEntry);
  
  return {
    ok: true,
    taskId,
    sessionFile,
    sessionName,
    messageCount: messages.length,
    totalTokens: totalTokens.toFixed(0),
    taskFile: individualTaskFile
  };
}

/**
 * Check for completed L3 tasks and apply compression
 */
function processCompletedL3Tasks() {
  if (!fs.existsSync(L3_RESULTS_DIR)) {
    return [];
  }
  
  const results = [];
  const files = fs.readdirSync(L3_RESULTS_DIR);
  
  for (const file of files) {
    if (!file.endsWith('.md')) continue;
    
    const filePath = path.join(L3_RESULTS_DIR, file);
    const content = fs.readFileSync(filePath, "utf-8");
    
    // Check if task is done
    const statusMatch = content.match(/status:\s*(\w+)/);
    if (!statusMatch || statusMatch[1] !== 'done') continue;
    
    // Extract results
    const result = parseL3Result(content, filePath);
    if (result) {
      results.push(result);
    }
  }
  
  return results;
}

/**
 * Parse L3 compression result
 */
function parseL3Result(content, filePath) {
  const lines = content.split('\n');
  const result = {
    taskId: null,
    sessionFile: null,
    status: null,
    tokensBefore: 0,
    tokensAfter: 0,
    summary: null,
    raw: content
  };
  
  for (const line of lines) {
    if (line.startsWith('task_id:')) {
      result.taskId = line.replace('task_id:', '').trim();
    } else if (line.startsWith('session_file:')) {
      result.sessionFile = line.replace('session_file:', '').trim();
    } else if (line.startsWith('status:')) {
      result.status = line.replace('status:', '').trim();
    } else if (line.startsWith('tokens_before:')) {
      result.tokensBefore = parseInt(line.replace('tokens_before:', '').trim()) || 0;
    } else if (line.startsWith('tokens_after:')) {
      result.tokensAfter = parseInt(line.replace('tokens_after:', '').trim()) || 0;
    }
  }
  
  // Extract summary from content
  const summaryMatch = content.match(/Summary:?\s*\n([\s\S]*?)(?=\n---|\n$)/i);
  if (summaryMatch) {
    result.summary = summaryMatch[1].trim();
  }
  
  return result.taskId ? result : null;
}

/**
 * Get L3 compression statistics
 */
function getL3Stats() {
  const stats = {
    totalTasks: 0,
    pendingTasks: 0,
    completedTasks: 0,
    totalTokensSaved: 0,
    recentTasks: []
  };
  
  if (!fs.existsSync(LOG_FILE)) {
    return stats;
  }
  
  const content = fs.readFileSync(LOG_FILE, "utf-8");
  const lines = content.split('\n').filter(l => l.trim());
  
  stats.totalTasks = lines.length;
  
  // Parse each line
  for (const line of lines) {
    if (line.includes('|')) {
      const parts = line.split('|').map(p => p.trim());
      if (parts.length >= 4) {
        const task = {
          time: parts[0].replace('- **', '').replace('**', ''),
          session: parts[1],
          messages: parseInt(parts[2]) || 0,
          tokens: parseInt(parts[3]) || 0,
          reason: parts[4] || ''
        };
        stats.recentTasks.push(task);
      }
    }
  }
  
  return stats;
}

module.exports = {
  estimateTokens,
  readSessionMessages,
  generateSummaryPrompt,
  createL3Task,
  processCompletedL3Tasks,
  parseL3Result,
  getL3Stats,
  L3_COMPRESS_FILE,
  L3_RESULTS_DIR,
  LOG_FILE
};
