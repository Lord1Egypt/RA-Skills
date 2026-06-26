/**
 * Vector Memory Skill
 * 
 * Vector-based semantic memory using embeddings for intelligent recall.
 * Stores data in ~/.thepopebot/vector-memory.json
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { OpenAI } = require('openai');

/**
 * Get the path to the vector memory storage file
 */
function getVectorMemoryPath() {
  const homeDir = process.env.HOME || process.env.USERPROFILE || '/tmp';
  const thepopebotDir = path.join(homeDir, '.thepopebot');
  
  if (!fs.existsSync(thepopebotDir)) {
    fs.mkdirSync(thepopebotDir, { recursive: true });
  }
  
  return path.join(thepopebotDir, 'vector-memory.json');
}

/**
 * Load vector memories from disk
 */
function loadVectorMemories() {
  const memoryPath = getVectorMemoryPath();
  
  if (!fs.existsSync(memoryPath)) {
    return { memories: [], meta: { created: new Date().toISOString() } };
  }
  
  try {
    const data = fs.readFileSync(memoryPath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error loading vector memory:', error.message);
    return { memories: [], meta: { created: new Date().toISOString() } };
  }
}

/**
 * Save vector memories to disk
 */
function saveVectorMemories(data) {
  const memoryPath = getVectorMemoryPath();
  
  try {
    fs.writeFileSync(memoryPath, JSON.stringify(data, null, 2), 'utf-8');
  } catch (error) {
    console.error('Error saving vector memory:', error.message);
    throw error;
  }
}

/**
 * Generate embedding using OpenAI
 */
async function generateEmbedding(text) {
  const apiKey = process.env.OPENAI_API_KEY;
  
  if (!apiKey) {
    throw new Error('OPENAI_API_KEY environment variable not set');
  }
  
  const client = new OpenAI({ apiKey });
  
  const response = await client.embeddings.create({
    model: 'text-embedding-ada-002',
    input: text
  });
  
  return response.data[0].embedding;
}

/**
 * Calculate cosine similarity between two vectors
 */
function cosineSimilarity(vecA, vecB) {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  
  if (normA === 0 || normB === 0) return 0;
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Generate a unique memory ID
 */
function generateMemoryId() {
  return 'mem_' + crypto.randomBytes(8).toString('hex');
}

/**
 * Store text with automatic embedding generation
 * @param {string} text - Text to store
 * @param {Object} options - Optional metadata
 * @returns {string} Confirmation with memory ID
 */
async function vstore(text, options = {}) {
  try {
    const embedding = await generateEmbedding(text);
    const data = loadVectorMemories();
    
    const memory = {
      id: generateMemoryId(),
      text,
      embedding,
      tags: options.tags || [],
      metadata: {
        createdAt: new Date().toISOString(),
        ...options.metadata
      }
    };
    
    data.memories.push(memory);
    saveVectorMemories(data);
    
    return `Stored memory with ID: ${memory.id}`;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

/**
 * Search memories by semantic similarity
 * @param {string} query - Search query
 * @param {number} limit - Maximum results (default: 5)
 * @param {number} threshold - Minimum similarity threshold 0-1 (default: 0.3)
 * @returns {string} Search results
 */
async function vsearch(query, limit = 5, threshold = 0.3) {
  try {
    const queryEmbedding = await generateEmbedding(query);
    const data = loadVectorMemories();
    
    if (data.memories.length === 0) {
      return 'No memories stored yet';
    }
    
    // Calculate similarities
    const results = data.memories.map(memory => ({
      id: memory.id,
      text: memory.text,
      tags: memory.tags,
      metadata: memory.metadata,
      similarity: cosineSimilarity(queryEmbedding, memory.embedding)
    }));
    
    // Filter and sort
    const filtered = results
      .filter(r => r.similarity >= threshold)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit);
    
    if (filtered.length === 0) {
      return `No memories found matching: ${query}`;
    }
    
    const formatted = filtered.map((r, i) => 
      `${i + 1}. [Score: ${r.similarity.toFixed(3)}] ${r.text}\n   ID: ${r.id}`
    ).join('\n\n');
    
    return `Found ${filtered.length} relevant memories:\n\n${formatted}`;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

/**
 * Delete a memory by ID
 */
function vdelete(memoryId) {
  try {
    const data = loadVectorMemories();
    const initialLength = data.memories.length;
    data.memories = data.memories.filter(m => m.id !== memoryId);
    
    if (data.memories.length === initialLength) {
      return `Memory not found: ${memoryId}`;
    }
    
    saveVectorMemories(data);
    return `Deleted memory: ${memoryId}`;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

/**
 * List all stored memories
 */
function vlist() {
  try {
    const data = loadVectorMemories();
    
    if (data.memories.length === 0) {
      return 'No vector memories stored yet';
    }
    
    const formatted = data.memories.map((m, i) => {
      const tags = m.tags.length > 0 ? ` [${m.tags.join(', ')}]` : '';
      return `${i + 1}. ${m.id}: ${m.text.substring(0, 100)}${m.text.length > 100 ? '...' : ''}${tags}`;
    }).join('\n');
    
    return `Stored memories (${data.memories.length}):\n\n${formatted}`;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

/**
 * Find memories similar to a given memory ID
 */
async function vsimilar(memoryId, limit = 5) {
  try {
    const data = loadVectorMemories();
    const source = data.memories.find(m => m.id === memoryId);
    
    if (!source) {
      return `Memory not found: ${memoryId}`;
    }
    
    const results = data.memories
      .filter(m => m.id !== memoryId)
      .map(memory => ({
        id: memory.id,
        text: memory.text,
        tags: memory.tags,
        similarity: cosineSimilarity(source.embedding, memory.embedding)
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit);
    
    if (results.length === 0) {
      return 'No similar memories found';
    }
    
    const formatted = results.map((r, i) => 
      `${i + 1}. [Score: ${r.similarity.toFixed(3)}] ${r.text}\n   ID: ${r.id}`
    ).join('\n\n');
    
    return `Memories similar to ${memoryId}:\n\n${formatted}`;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

/**
 * Clear all vector memories
 */
function vclear() {
  try {
    saveVectorMemories({ memories: [], meta: { created: new Date().toISOString() } });
    return 'Cleared all vector memories';
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

module.exports = {
  vstore,
  vsearch,
  vdelete,
  vlist,
  vsimilar,
  vclear,
  cosineSimilarity,
  generateEmbedding
};
