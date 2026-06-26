import type { ScrapedList, ScrapedItem } from '../types.js';

export class ListExtractor {
  extract(content: string, maxItems?: number): ScrapedList {
    // Parse the JSON string from browser
    let items: string[] = [];
    try {
      items = JSON.parse(content);
    } catch {
      // Fallback: split by common delimiters
      items = content.split('\n').filter(line => line.trim().length > 10);
    }

    const scrapedItems: ScrapedItem[] = items
      .slice(0, maxItems || 100)
      .map((text, index) => this.parseItem(text, index));

    return {
      type: 'list',
      items: scrapedItems,
      total: scrapedItems.length,
      pageUrl: ''
    };
  }

  private parseItem(text: string, index: number): ScrapedItem {
    const item: ScrapedItem = {
      id: index + 1,
      rawText: text.trim()
    };

    // Try to extract common patterns
    const lines = text.split('\n').map(l => l.trim()).filter(l => l);
    
    // Look for title (usually first non-empty line)
    if (lines[0]) {
      item.title = lines[0].substring(0, 200);
    }

    // Look for price
    const priceMatch = text.match(/\$[\d,]+\.?\d*|\d+\.\d{2}\s*(USD|EUR|GBP)?/i);
    if (priceMatch) {
      item.price = priceMatch[0];
    }

    // Look for URL
    const urlMatch = text.match(/https?:\/\/[^\s]+/);
    if (urlMatch) {
      item.url = urlMatch[0];
    }

    // Look for description (longest line that's not the title)
    const description = lines.slice(1).find(l => l.length > 20);
    if (description) {
      item.description = description.substring(0, 500);
    }

    return item;
  }
}
