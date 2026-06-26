export type Layer = 'L0' | 'L1' | 'L2' | 'L3';
export type Source = 'text' | 'link' | 'ocr';

export interface Note {
  id: string;
  content: string;
  layer: Layer;
  source: Source;
  url?: string;
  createdAt: number;
  updatedAt: number;
  wordCount: number;
  summary?: string;
  tags?: string[];
  embedding?: number[];
  aiEnhanced?: {
    summary: string;
    tags: string[];
    relatedIds: string[];
  };
}

export interface NoteVersion {
  id: string;
  noteId: string;
  content: string;
  version: number;
  isMarked: boolean;
  markNote?: string;
  createdAt: number;
}

export interface SearchResult {
  note: Note;
  score: number;
  type: 'keyword' | 'semantic' | 'hybrid';
}

export interface SyncResult {
  success: boolean;
  updated: number;
  conflicts: number;
}

export interface AIConfig {
  openaiApiKey?: string;
  embeddingModel?: string;
  chatModel?: string;
}