/**
 * Cross-Agent Context Sharing Module v2.0
 * 
 * Enables knowledge extraction and sharing between agents:
 * 1. Extract key information from sessions
 * 2. Publish to shared memory
 * 3. Other agents can read and use it
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

// Paths
const SHARED_DIR = "E:\\zhuazhua\\.openclaw-shared\\memory";
const SHARED_KNOWLEDGE_FILE = path.join(SHARED_DIR, "shared_knowledge.md");
const AGENT_CONTEXT_DIR = path.join(SHARED_DIR, "agent_contexts");
const INBOX_DIR = path.join(SHARED_DIR, "inbox");

// Extraction patterns
const KEY_PATTERNS = {
  // User preferences and instructions
  preferences: [
    /(?:user|用户|prefer|偏好|希望|想要).*?[:：]\s*(.+)/gi,
    /(?:always|一直|始终|总是).*?[:：]\s*(.+)/gi,
    /(?:never|不要|别).*?[:：]\s*(.+)/gi
  ],
  
  // Decisions and conclusions
  decisions: [
    /(?:决定|decision|decided|选择|chose).*?[:：]\s*(.+)/gi,
    /(?:结论|conclusion|综上|因此).*?[:：]\s*(.+)/gi,
    /(?:agreed|agreed|一致同意|共识).*?[:：]\s*(.+)/gi
  ],
  
  // Actions and tasks
  actions: [
    /(?:完成|completed|executed|执行|done).*?[:：]\s*(.+)/gi,
    /(?:task|task|任务).*?[:：]\s*(.+)/gi,
    /(?:will|将会|计划).*?[:：]\s*(.+)/gi
  ],
  
  // Important facts
  facts: [
    /(?:fact|事实|实际上|actually).*?[:：]\s*(.+)/gi,
    /(?:remember|记住|记录).*?[:：]\s*(.+)/gi,
    /(?:important|重要|critical|关键).*?[:：]\s*(.+)/gi
  ],
  
  // Technical knowledge
  technical: [
    /(?:config|配置|设置).*?[:：]\s*(.+)/gi,
    /(?:path|路径|directory|目录).*?[:：]\s*(.+)/gi,
    /(?:command|命令|script|脚本).*?[:：]\s*(.+)/gi
  ]
};

/**
 * Extract key information from a session's messages
 */
function extractKeyInfo(messages) {
  const extracted = {
    preferences: [],
    decisions: [],
    actions: [],
    facts: [],
    technical: []
  };
  
  for (const msg of messages) {
    const content = extractTextContent(msg.content);
    if (!content) continue;
    
    for (const [category, patterns] of Object.entries(KEY_PATTERNS)) {
      for (const pattern of patterns) {
        const matches = content.match(pattern);
        if (matches) {
          for (const match of matches) {
            // Clean up the match
            const cleaned = match.replace(/^(?:user|用户|prefer|偏好|希望|想要|decision|decided|决定|选择|chose|完成|completed|executed|执行|done|task|任务|will|将会|计划|fact|事实|实际上|actually|remember|记住|记录|important|重要|critical|关键|config|配置|设置|path|路径|directory|目录|command|命令|script|脚本|user|用户|prefer|偏好|希望|想要|always|一直|始终|总是|never|不要|别|agreed|一致同意|共识|conclusion|结论|综上|因此).*?[:：]\s*/i, '');
            if (cleaned && cleaned.length > 5 && cleaned.length < 500) {
              extracted[category].push({
                text: cleaned,
                role: msg.role,
                source: "session"
              });
            }
          }
        }
      }
    }
  }
  
  // Deduplicate
  for (const category of Object.keys(extracted)) {
    const seen = new Set();
    extracted[category] = extracted[category].filter(item => {
      const key = item.text.slice(0, 50);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }
  
  return extracted;
}

/**
 * Extract text content from various formats
 */
function extractTextContent(content) {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content.map(block => {
      if (typeof block === "string") return block;
      if (block.text) return block.text;
      if (block.type === "toolCall") return `[tool: ${block.name || 'unknown'}]`;
      if (block.type === "toolResult") return `[result]`;
      return "";
    }).join(" ");
  }
  return "";
}

/**
 * Read session messages
 */
function readSessionMessages(sessionFile) {
  try {
    if (!fs.existsSync(sessionFile)) {
      return { messages: [], error: "Session not found" };
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
    
    for (const line of records) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type === "message" && obj.message?.content) {
          messages.push({
            id: obj.id,
            role: obj.message.role,
            content: obj.message.content,
            timestamp: obj.timestamp
          });
        }
      } catch (e) {}
    }
    
    return { messages, error: null };
  } catch (e) {
    return { messages: [], error: e.message };
  }
}

/**
 * Generate shared knowledge entry from extracted info
 */
function generateKnowledgeEntry(extracted, sessionFile, agentName) {
  const timestamp = new Date().toISOString();
  const sessionName = path.basename(sessionFile);
  
  let content = `---
type: shared_knowledge
source_session: ${sessionName}
source_agent: ${agentName}
extracted_at: ${timestamp}
tags: [extracted, cross-agent, shared]
---

# Shared Knowledge from ${sessionName}

> Extracted by ${agentName} at ${timestamp}

`;
  
  // Add each category
  for (const [category, items] of Object.entries(extracted)) {
    if (items.length > 0) {
      content += `## ${category.charAt(0).toUpperCase() + category.slice(1)}\n\n`;
      for (const item of items) {
        content += `- **${item.role}**: ${item.text}\n`;
      }
      content += "\n";
    }
  }
  
  return content;
}

/**
 * Publish extracted knowledge to shared memory
 */
function publishKnowledge(extracted, sessionFile, agentName) {
  if (!fs.existsSync(AGENT_CONTEXT_DIR)) {
    fs.mkdirSync(AGENT_CONTEXT_DIR, { recursive: true });
  }
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const sessionName = path.basename(sessionFile).replace(".jsonl", "");
  const filename = `knowledge_${sessionName}_${timestamp}.md`;
  const filePath = path.join(AGENT_CONTEXT_DIR, filename);
  
  const content = generateKnowledgeEntry(extracted, sessionFile, agentName);
  fs.writeFileSync(filePath, content, "utf-8");
  
  // Also append to main shared knowledge file
  if (!fs.existsSync(SHARED_DIR)) {
    fs.mkdirSync(SHARED_DIR, { recursive: true });
  }
  
  const entryMarker = `\n\n<!-- ${timestamp} | ${sessionName} | ${agentName} -->\n`;
  fs.appendFileSync(SHARED_KNOWLEDGE_FILE, entryMarker + content);
  
  return {
    ok: true,
    file: filePath,
    knowledgeCount: Object.values(extracted).reduce((sum, arr) => sum + arr.length, 0)
  };
}

/**
 * Extract and publish from a session
 */
function extractAndPublish(sessionFile, agentName = "unknown") {
  const { messages, error } = readSessionMessages(sessionFile);
  
  if (error || messages.length === 0) {
    return { ok: false, error: error || "No messages found" };
  }
  
  const extracted = extractKeyInfo(messages);
  const totalItems = Object.values(extracted).reduce((sum, arr) => sum + arr.length, 0);
  
  if (totalItems === 0) {
    return { ok: false, error: "No key information extracted" };
  }
  
  const result = publishKnowledge(extracted, sessionFile, agentName);
  return {
    ...result,
    extracted,
    messageCount: messages.length
  };
}

/**
 * Read shared knowledge for an agent
 */
function readSharedKnowledge(agentName = null) {
  if (!fs.existsSync(SHARED_KNOWLEDGE_FILE)) {
    return { knowledge: [], error: "No shared knowledge found" };
  }
  
  const content = fs.readFileSync(SHARED_KNOWLEDGE_FILE, "utf-8");
  
  // Parse knowledge entries (separated by <!-- markers)
  const entries = content.split(/<!-- .*? -->/).filter(e => e.trim());
  const knowledge = [];
  
  for (const entry of entries) {
    if (!entry.trim()) continue;
    
    // Check if entry matches agent filter
    if (agentName && !entry.includes(`source_agent: ${agentName}`)) {
      // Also include entries without agent restriction if no specific agent
      if (!entry.includes("source_agent:")) {
        knowledge.push(entry);
      }
      continue;
    }
    
    knowledge.push(entry);
  }
  
  return { knowledge, error: null };
}

/**
 * Get latest shared knowledge entries
 */
function getRecentKnowledge(count = 5) {
  if (!fs.existsSync(AGENT_CONTEXT_DIR)) {
    return [];
  }
  
  const files = fs.readdirSync(AGENT_CONTEXT_DIR)
    .filter(f => f.endsWith(".md"))
    .map(f => ({
      name: f,
      path: path.join(AGENT_CONTEXT_DIR, f),
      mtime: fs.statSync(path.join(AGENT_CONTEXT_DIR, f)).mtime.getTime()
    }))
    .sort((a, b) => b.mtime - a.mtime)
    .slice(0, count);
  
  const recent = [];
  for (const file of files) {
    try {
      const content = fs.readFileSync(file.path, "utf-8");
      recent.push({
        file: file.name,
        mtime: new Date(file.mtime).toISOString(),
        content: content.slice(0, 500)
      });
    } catch (e) {}
  }
  
  return recent;
}

/**
 * Create context package for agent handoff
 */
function createContextPackage(sessionFile, targetAgent, purpose = "continuation") {
  const { messages, error } = readSessionMessages(sessionFile);
  
  if (error) {
    return { ok: false, error };
  }
  
  const extracted = extractKeyInfo(messages);
  
  // Create context package
  const pkg = {
    purpose,
    sourceSession: path.basename(sessionFile),
    targetAgent,
    createdAt: new Date().toISOString(),
    summary: {
      messageCount: messages.length,
      roleCounts: messages.reduce((acc, m) => {
        acc[m.role] = (acc[m.role] || 0) + 1;
        return acc;
      }, {})
    },
    extractedKnowledge: extracted,
    recentMessages: messages.slice(-5).map(m => ({
      role: m.role,
      preview: extractTextContent(m.content).slice(0, 200)
    }))
  };
  
  // Write to inbox for target agent
  const inboxFile = path.join(INBOX_DIR, `for_${targetAgent}.md`);
  const timestamp = new Date().toISOString();
  
  let content = `---
type: agent_handoff
from_session: ${path.basename(sessionFile)}
purpose: ${purpose}
created: ${timestamp}
target: ${targetAgent}
---

# Context Handoff to ${targetAgent}

## Purpose
${purpose}

## Summary
- Source session: ${path.basename(sessionFile)}
- Message count: ${pkg.summary.messageCount}
- Created: ${timestamp}

## Role Distribution
${JSON.stringify(pkg.summary.roleCounts, null, 2)}

## Extracted Knowledge

`;
  
  for (const [category, items] of Object.entries(extracted)) {
    if (items.length > 0) {
      content += `### ${category}\n`;
      for (const item of items.slice(0, 5)) {
        content += `- ${item.text}\n`;
      }
      content += "\n";
    }
  }
  
  content += `## Recent Messages\n\n`;
  for (const msg of pkg.recentMessages) {
    content += `**${msg.role}**: ${msg.preview}\n\n`;
  }
  
  if (!fs.existsSync(INBOX_DIR)) {
    fs.mkdirSync(INBOX_DIR, { recursive: true });
  }
  
  fs.writeFileSync(inboxFile, content, "utf-8");
  
  return {
    ok: true,
    package: pkg,
    file: inboxFile
  };
}

module.exports = {
  KEY_PATTERNS,
  extractKeyInfo,
  extractTextContent,
  readSessionMessages,
  generateKnowledgeEntry,
  publishKnowledge,
  extractAndPublish,
  readSharedKnowledge,
  getRecentKnowledge,
  createContextPackage,
  SHARED_KNOWLEDGE_FILE,
  AGENT_CONTEXT_DIR
};
