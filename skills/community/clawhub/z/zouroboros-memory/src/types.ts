export type DecayClass = 'permanent' | 'long' | 'medium' | 'short';

export interface MemoryConfig {
  enabled: boolean;
  dbPath: string;
  vectorEnabled: boolean;
  ollamaUrl: string;
  ollamaModel: string;
  autoCapture: boolean;
  captureIntervalMinutes: number;
  graphBoost: boolean;
  hydeExpansion: boolean;
  decayConfig: { permanent: number; long: number; medium: number; short: number };
  reranker?: { enabled: boolean; model?: string; maxContextChunks?: number };
  cot?: { enabled: boolean; model?: string };
}

export interface MemoryEntry {
  id: string;
  entity: string;
  key: string | null;
  value: string;
  decay: DecayClass;
  createdAt: string;
  updatedAt: string;
  tags?: string[];
}

export interface MemorySearchResult {
  entry: MemoryEntry;
  score: number;
  matchType: 'exact' | 'semantic' | 'hybrid' | 'graph';
}

export interface EpisodicMemory {
  id: string;
  conversationId: string;
  summary: string;
  outcome: 'success' | 'failure' | 'resolved' | 'ongoing';
  entities: string[];
  tags: string[];
  createdAt: string;
  tokenCount?: number;
  daysAgo?: number;
  procedureName?: string;
  procedureVersion?: number | null;
}

export interface TemporalQuery {
  since?: string;
  until?: string;
  outcome?: 'success' | 'failure' | 'resolved' | 'ongoing';
  limit?: number;
}

export interface CognitiveProfile {
  entity: string;
  traits: Record<string, number>;
  preferences: Record<string, string>;
  interactionHistory: InteractionRecord[];
  lastUpdated: string;
}

export interface InteractionRecord {
  timestamp: string;
  type: 'query' | 'store' | 'search';
  success: boolean;
  latencyMs: number;
}

export interface GraphNode {
  id: string;
  type: string;
  label: string;
  properties: Record<string, unknown>;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation: string;
  weight: number;
}

export interface CotAnswerResult {
  answer: string;
  reasoning: string;
  confidence: number;
  sourceFacts: string[];
}

export interface DeepSearchResult {
  results: MemorySearchResult[];
  answer: CotAnswerResult;
}
