// EXPERIMENTAL — no build/publish pipeline
TypeScript SDK — Agent Memory Client v8.9

使用示例:

```typescript
import { AgentMemoryClient, MemoryResult } from './agent-memory-client';

const client = new AgentMemoryClient({
  host: 'http://localhost:8988',
  tenantId: 'my-app',
  apiKey: 'sk-xxx',
  protocol: 'http',
});

const result = await client.remember('今天用 LangChain 完成了 RAG 测试');
console.log(`记忆 ID: ${result.memory_id}`);

const matches = await client.recall('RAG 测试的结果怎么样');
matches.forEach(m => console.log(`- ${m.content} (${m.confidence})`));

const trace = await client.trace(result.memory_id);
console.log(`演化链: ${trace.length} 个版本`);

const advice = await client.decide('agent-1', '数据库选型');
console.log(`建议: ${advice.recommendation} (置信度: ${advice.confidence})`);
```
*/

export interface ClientOptions {
  host: string;
  tenantId: string;
  apiKey: string;
  protocol?: 'http' | 'grpc' | 'ws';
  timeout?: number;
}

export interface WriteOptions {
  importance?: 'high' | 'medium' | 'low';
  topics?: string[];
  nature_code?: string;
  visibility?: 'private' | 'team' | 'public';
}

export interface MemoryResult {
  memory_id: string;
  content: string;
  importance: string;
  confidence: number;
  lifecycle_state: string;
  version: number;
  created_at: string;
}

export interface RecallResponse {
  results: MemoryResult[];
  latency_ms: number;
  total_count: number;
  search_mode: string;
}

export interface LifecycleNode {
  memory_id: string;
  version: number;
  lifecycle_state: string;
  importance: string;
  confidence: number;
  content_preview: string;
}

export interface DecisionAdvice {
  recommendation: string;
  confidence: number;
  alternatives: string[];
  risk_factors: Array<{ description: string; severity: string; source_id: string }>;
}

export interface ServerHealth {
  status: string;
  version: string;
  total_memories: number;
  uptime: string;
}

export class AgentMemoryClient {
  private host: string;
  private tenantId: string;
  private apiKey: string;
  private protocol: string;
  private timeout: number;
  private ws: WebSocket | null = null;
  private eventHandlers: Map<string, Array<(data: unknown) => void>> = new Map();

  constructor(options: ClientOptions) {
    this.host = options.host.replace(/\/$/, '');
    this.tenantId = options.tenantId;
    this.apiKey = options.apiKey;
    this.protocol = options.protocol || 'http';
    this.timeout = options.timeout || 30000;
  }

  get authHeaders(): Record<string, string> {
    return {
      'Authorization': `Bearer ${this.apiKey}`,
      'X-Tenant-ID': this.tenantId,
      'Content-Type': 'application/json',
    };
  }

  private async fetch(path: string, body: Record<string, unknown> = {}): Promise<unknown> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);

    try {
      const resp = await fetch(`${this.host}${path}`, {
        method: 'POST',
        headers: this.authHeaders,
        body: JSON.stringify(body),
        signal: controller.signal,
      });
      if (!resp.ok) {
        throw new Error(`AgentMemory API ${resp.status}: ${await resp.text()}`);
      }
      return await resp.json();
    } finally {
      clearTimeout(timer);
    }
  }

  async remember(content: string, options?: WriteOptions): Promise<MemoryResult> {
    const data = await this.fetch('/v1/memories', {
      content,
      importance: options?.importance || 'medium',
      topics: options?.topics || [],
      nature_code: options?.nature_code || 'D05',
      visibility: options?.visibility || 'team',
      owner_agent_id: 'default',
    }) as Record<string, unknown>;

    return {
      memory_id: data.memory_id as string || '',
      content: content,
      importance: options?.importance || 'medium',
      confidence: (data.confidence as number) || 0.5,
      lifecycle_state: (data.lifecycle_state as string) || 'active',
      version: (data.version as number) || 1,
      created_at: new Date().toISOString(),
    };
  }

  async recall(query: string, topK: number = 20): Promise<RecallResponse> {
    const data = await this.fetch('/v1/recall', { query, top_k: topK }) as Record<string, unknown>;
    const results = (data.results || data.primary || []) as Array<Record<string, unknown>>;

    return {
      results: results.map((r) => ({
        memory_id: r.memory_id as string || '',
        content: r.content as string || '',
        importance: r.importance as string || 'medium',
        confidence: r.confidence as number || 0.5,
        lifecycle_state: r.lifecycle_state as string || 'active',
        version: r.version as number || 1,
        created_at: r.created_at as string || '',
      })),
      latency_ms: data.latency_ms as number || 0,
      total_count: (data.total_count as number) || (data.total as number) || results.length,
      search_mode: data.search_mode as string || 'hybrid',
    };
  }

  async get(memoryId: string): Promise<MemoryResult | null> {
    try {
      const data = await this.fetch(`/v1/memories/${memoryId}`) as Record<string, unknown>;
      return {
        memory_id: data.memory_id as string || memoryId,
        content: data.content as string || '',
        importance: data.importance as string || 'medium',
        confidence: data.confidence as number || 0.5,
        lifecycle_state: data.lifecycle_state as string || 'active',
        version: data.version as number || 1,
        created_at: data.created_at as string || '',
      };
    } catch {
      return null;
    }
  }

  async trace(memoryId: string): Promise<LifecycleNode[]> {
    const data = await this.fetch(`/v1/memories/${memoryId}/trace`) as Record<string, unknown>;
    return ((data.nodes || data.chain || []) as Array<Record<string, unknown>>).map((n) => ({
      memory_id: n.memory_id as string || '',
      version: n.version as number || 1,
      lifecycle_state: n.lifecycle_state as string || 'active',
      importance: n.importance as string || 'medium',
      confidence: n.confidence as number || 0.5,
      content_preview: n.content_preview as string || '',
    }));
  }

  async decide(agentId: string, query: string): Promise<DecisionAdvice> {
    const data = await this.fetch('/v1/decide', { agent_id: agentId, query }) as Record<string, unknown>;
    return {
      recommendation: data.recommendation as string || '',
      confidence: data.confidence as number || 0,
      alternatives: (data.alternatives as string[]) || [],
      risk_factors: ((data.risk_factors || []) as Array<Record<string, unknown>>).map((r) => ({
        description: r.description as string || '',
        severity: r.severity as string || 'medium',
        source_id: r.source_id as string || '',
      })),
    };
  }

  async health(): Promise<ServerHealth> {
    const data = await this.fetch('/v1/health') as Record<string, unknown>;
    return {
      status: data.status as string || 'unknown',
      version: data.version as string || '0.0',
      total_memories: data.total_memories as number || 0,
      uptime: data.uptime as string || '',
    };
  }

  async connect(): Promise<void> {
    if (this.protocol !== 'ws') return;
    const url = this.host.replace('http://', 'ws://').replace('https://', 'wss://');
    this.ws = new WebSocket(`${url}/v1/ws/${this.tenantId}`);

    return new Promise((resolve, reject) => {
      if (!this.ws) return reject(new Error('WebSocket not created'));
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const eventType = data.event || data.type || 'unknown';
          const handlers = this.eventHandlers.get(eventType) || [];
          handlers.forEach((fn) => fn(data));
        } catch {
          console.debug('WebSocket 消息解析失败');
        }
      };
      this.ws.onclose = () => {
        this.ws = null;
        setTimeout(() => this.connect(), 3000);
      };
    });
  }

  on(event: string, callback: (data: unknown) => void): void {
    const handlers = this.eventHandlers.get(event) || [];
    handlers.push(callback);
    this.eventHandlers.set(event, handlers);
  }

  off(event: string, callback: (data: unknown) => void): void {
    const handlers = this.eventHandlers.get(event) || [];
    this.eventHandlers.set(event, handlers.filter((h) => h !== callback));
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.eventHandlers.clear();
  }
}

export default AgentMemoryClient;