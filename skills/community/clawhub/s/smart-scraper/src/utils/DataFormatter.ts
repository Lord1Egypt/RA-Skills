import type { ScrapedData, ScrapeOptions } from '../types.js';
import { ListExtractor } from './ListExtractor.js';
import { ArticleExtractor } from './ArticleExtractor.js';
import { TableExtractor } from './TableExtractor.js';

export class DataFormatter {
  private listExtractor = new ListExtractor();
  private articleExtractor = new ArticleExtractor();
  private tableExtractor = new TableExtractor();

  format(
    content: string,
    structure: { type: string; selectors: Record<string, string | undefined> },
    options: ScrapeOptions
  ): ScrapedData {
    const { type, url = '' } = options;

    switch (structure.type) {
      case 'list':
        return this.listExtractor.extract(content, options.maxItems);
      
      case 'article':
        return this.articleExtractor.extract(content, url);
      
      case 'table':
        return this.tableExtractor.extract(content, url);
      
      default:
        // Auto-detect based on content
        if (content.includes('<table')) {
          return this.tableExtractor.extract(content, url);
        }
        if (content.length > 1000) {
          return this.articleExtractor.extract(content, url);
        }
        return this.listExtractor.extract(content, options.maxItems);
    }
  }

  toJSON(data: ScrapedData): string {
    return JSON.stringify(data, null, 2);
  }

  toCSV(data: ScrapedData): string {
    if (data.type === 'table') {
      const headers = data.headers.join(',');
      const rows = data.rows.map(row => 
        data.headers.map(h => {
          const val = row[h];
          const str = String(val ?? '');
          return str.includes(',') ? `"${str}"` : str;
        }).join(',')
      );
      return [headers, ...rows].join('\n');
    }

    if (data.type === 'list') {
      if (data.items.length === 0) return '';
      const headers = Object.keys(data.items[0]).join(',');
      const rows = data.items.map(item =>
        Object.values(item).map(v => {
          const str = String(v ?? '');
          return str.includes(',') ? `"${str}"` : str;
        }).join(',')
      );
      return [headers, ...rows].join('\n');
    }

    // Article to CSV (single row)
    return `title,content,author,date\n"${data.title}","${data.content.substring(0, 200)}...",${data.author || ''},${data.publishDate || ''}`;
  }

  toMarkdown(data: ScrapedData): string {
    if (data.type === 'article') {
      return `# ${data.title}\n\n` +
        (data.author ? `**Author:** ${data.author}\n` : '') +
        (data.publishDate ? `**Date:** ${data.publishDate}\n` : '') +
        `**URL:** ${data.url}\n\n---\n\n${data.content}`;
    }

    if (data.type === 'list') {
      return data.items.map((item, i) => {
        const title = item.title || item.rawText || `Item ${i + 1}`;
        const details = Object.entries(item)
          .filter(([k]) => !['id', 'rawText', 'title'].includes(k))
          .map(([k, v]) => `- ${k}: ${v}`)
          .join('\n');
        return `## ${title}\n${details ? details + '\n' : ''}`;
      }).join('\n');
    }

    if (data.type === 'table') {
      const headerRow = '| ' + data.headers.join(' | ') + ' |';
      const separator = '| ' + data.headers.map(() => '---').join(' | ') + ' |';
      const rows = data.rows.map(row => 
        '| ' + data.headers.map(h => row[h] ?? '').join(' | ') + ' |'
      );
      return [headerRow, separator, ...rows].join('\n');
    }

    return '';
  }
}
