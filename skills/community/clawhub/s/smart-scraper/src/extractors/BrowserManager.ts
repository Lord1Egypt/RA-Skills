import { chromium, Browser, Page } from 'playwright';
import type { PageStructure, ScrapeOptions } from '../types.js';

export class BrowserManager {
  private browser: Browser | null = null;

  async init(): Promise<void> {
    this.browser = await chromium.launch({ headless: true });
  }

  async newPage(): Promise<Page> {
    if (!this.browser) throw new Error('Browser not initialized');
    return this.browser.newPage();
  }

  async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }

  async scrapePage(url: string, options: ScrapeOptions): Promise<{
    content: string;
    screenshot: Buffer;
    structure: PageStructure;
  }> {
    const page = await this.newPage();
    
    try {
      await page.goto(url, { waitUntil: 'networkidle' });
      
      if (options.waitFor) {
        await page.waitForSelector(options.waitFor, { timeout: 10000 });
      }

      if (options.scroll) {
        await this.autoScroll(page);
      }

      // Analyze page structure
      const structure = await this.analyzeStructure(page);
      
      // Get content based on structure
      const content = await this.extractContent(page, structure);
      
      // Take screenshot for LLM analysis
      const screenshot = await page.screenshot({ fullPage: true });

      return { content, screenshot, structure };
    } finally {
      await page.close();
    }
  }

  private async autoScroll(page: Page): Promise<void> {
    await page.evaluate(async () => {
      await new Promise<void>((resolve) => {
        let totalHeight = 0;
        const distance = 300;
        const timer = setInterval(() => {
          const scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, distance);
          totalHeight += distance;
          
          if (totalHeight >= scrollHeight) {
            clearInterval(timer);
            resolve();
          }
        }, 100);
      });
    });
  }

  private async analyzeStructure(page: Page): Promise<PageStructure> {
    return page.evaluate(() => {
      const structure: PageStructure = {
        type: 'unknown',
        confidence: 0,
        selectors: {}
      };

      // Check for list patterns
      const listSelectors = [
        '[class*="product"]',
        '[class*="item"]',
        '[class*="listing"]',
        '[class*="result"]',
        '.grid > div',
        '.list > div',
        'ul > li'
      ];

      for (const selector of listSelectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length >= 3) {
          structure.type = 'list';
          structure.confidence = Math.min(elements.length / 10, 0.9);
          structure.selectors.container = selector;
          break;
        }
      }

      // Check for article patterns
      if (structure.type === 'unknown') {
        const articleSelectors = [
          'article',
          '[class*="article"]',
          '[class*="post"]',
          '[class*="content"] main'
        ];

        for (const selector of articleSelectors) {
          const element = document.querySelector(selector);
          if (element && element.textContent && element.textContent.length > 500) {
            structure.type = 'article';
            structure.confidence = 0.8;
            structure.selectors.content = selector;
            break;
          }
        }
      }

      // Check for table patterns
      if (structure.type === 'unknown') {
        const tables = document.querySelectorAll('table');
        if (tables.length > 0) {
          const largestTable = Array.from(tables).reduce((largest, table) => {
            return table.rows.length > largest.rows.length ? table : largest;
          });
          
          if (largestTable.rows.length >= 3) {
            structure.type = 'table';
            structure.confidence = 0.85;
            structure.selectors.table = 'table';
          }
        }
      }

      return structure;
    });
  }

  private async extractContent(page: Page, structure: PageStructure): Promise<string> {
    return page.evaluate((struct) => {
      if (struct.type === 'list' && struct.selectors.container) {
        const items = document.querySelectorAll(struct.selectors.container);
        return JSON.stringify(Array.from(items).map(item => item.textContent));
      }
      
      if (struct.type === 'article' && struct.selectors.content) {
        const article = document.querySelector(struct.selectors.content);
        return article?.textContent || document.body.innerText;
      }
      
      if (struct.type === 'table' && struct.selectors.table) {
        const table = document.querySelector(struct.selectors.table);
        return table?.outerHTML || '';
      }
      
      return document.body.innerText;
    }, structure);
  }
}
