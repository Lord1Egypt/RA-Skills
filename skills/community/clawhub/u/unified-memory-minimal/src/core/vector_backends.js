/**
 * Vector Backends - Multiple vector database backends
 */

export const BACKEND_NOTICE = `
🔢 Vector Backend Options for Node.js

1. LanceDB (RECOMMENDED)
   - npm install vectordb

2. sqlite-vec (OpenClaw built-in)
   - Automatic via OpenClaw

3. Qdrant (external service)
   - Requires running Qdrant server

NOT AVAILABLE: FAISS (C++ only)
`;

export class MemoryVectorStore {
  constructor() { this.vectors = new Map(); }
  
  async add(items) { for (const item of items) this.vectors.set(item.id, { vector: item.vector, data: item.data }); }
  
  async search(query, topK = 5) {
    const results = [];
    for (const [id, { vector, data }] of this.vectors) {
      results.push({ id, score: this.cosineSimilarity(query, vector), data });
    }
    return results.sort((a, b) => b.score - a.score).slice(0, topK);
  }
  
  async delete(ids) { for (const id of ids) this.vectors.delete(id); }
  async count() { return this.vectors.size; }
  
  cosineSimilarity(a, b) {
    if (a.length !== b.length) return 0;
    let dotProduct = 0, normA = 0, normB = 0;
    for (let i = 0; i < a.length; i++) { dotProduct += a[i] * b[i]; normA += a[i] * a[i]; normB += b[i] * b[i]; }
    const denominator = Math.sqrt(normA) * Math.sqrt(normB);
    return denominator > 0 ? dotProduct / denominator : 0;
  }
}

if (require.main === module) { console.log(BACKEND_NOTICE); }
