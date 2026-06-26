export interface ScrapedItem {
  [key: string]: string | number | boolean | null;
}

export interface ScrapedList {
  type: 'list';
  items: ScrapedItem[];
  total: number;
  pageUrl: string;
}

export interface ScrapedArticle {
  type: 'article';
  title: string;
  content: string;
  author?: string;
  publishDate?: string;
  url: string;
}

export interface ScrapedTable {
  type: 'table';
  headers: string[];
  rows: Record<string, string | number>[];
  url: string;
}

export type ScrapedData = ScrapedList | ScrapedArticle | ScrapedTable;

export interface ScrapeOptions {
  url: string;
  type?: 'list' | 'article' | 'table' | 'auto';
  format?: 'json' | 'csv' | 'markdown';
  waitFor?: string;
  scroll?: boolean;
  maxItems?: number;
}

export interface PageStructure {
  type: 'list' | 'article' | 'table' | 'unknown';
  confidence: number;
  selectors: {
    container?: string;
    items?: string;
    title?: string;
    content?: string;
    table?: string;
  };
}
