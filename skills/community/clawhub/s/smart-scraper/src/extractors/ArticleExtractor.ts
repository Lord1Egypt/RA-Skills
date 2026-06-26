import type { ScrapedArticle } from '../types.js';

export class ArticleExtractor {
  extract(content: string, url: string): ScrapedArticle {
    const lines = content.split('\n').map(l => l.trim()).filter(l => l);
    
    // Extract title (first substantial line or h1 pattern)
    let title = lines[0] || 'Untitled';
    if (title.length > 100) {
      title = title.substring(0, 100) + '...';
    }

    // Extract author
    const authorPatterns = [
      /by\s+([^\n]+)/i,
      /author:\s*([^\n]+)/i,
      /written\s+by\s+([^\n]+)/i
    ];
    
    let author: string | undefined;
    for (const pattern of authorPatterns) {
      const match = content.match(pattern);
      if (match) {
        author = match[1].trim().substring(0, 100);
        break;
      }
    }

    // Extract date
    const datePatterns = [
      /\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b/,
      /\b(\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})\b/,
      /(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}/i
    ];

    let publishDate: string | undefined;
    for (const pattern of datePatterns) {
      const match = content.match(pattern);
      if (match) {
        publishDate = match[0];
        break;
      }
    }

    // Clean content (remove title, author, date lines)
    let cleanContent = content
      .replace(title, '')
      .replace(/by\s+[^\n]+/i, '')
      .replace(/author:\s*[^\n]+/i, '')
      .trim();

    return {
      type: 'article',
      title,
      content: cleanContent.substring(0, 10000),
      author,
      publishDate,
      url
    };
  }
}
