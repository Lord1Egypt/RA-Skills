import { BrowserManager } from './extractors/BrowserManager.js';
import { DataFormatter } from './utils/DataFormatter.js';
import type { ScrapeOptions, ScrapedData } from './types.js';

export class SmartScraper {
  private browser: BrowserManager;
  private formatter: DataFormatter;

  constructor() {
    this.browser = new BrowserManager();
    this.formatter = new DataFormatter();
  }

  async init(): Promise<void> {
    await this.browser.init();
  }

  async close(): Promise<void> {
    await this.browser.close();
  }

  async scrape(options: ScrapeOptions): Promise<{
    data: ScrapedData;
    raw: string;
    format: string;
  }> {
    // Scrape page
    const { content, structure } = await this.browser.scrapePage(options.url, options);
    
    // Format data
    const data = this.formatter.format(content, structure, options);
    
    // Output in requested format
    const format = options.format || 'json';
    let raw: string;
    
    switch (format) {
      case 'csv':
        raw = this.formatter.toCSV(data);
        break;
      case 'markdown':
        raw = this.formatter.toMarkdown(data);
        break;
      case 'json':
      default:
        raw = this.formatter.toJSON(data);
    }

    return { data, raw, format };
  }
}

// CLI usage
async function main() {
  const args = process.argv.slice(2);
  const options: ScrapeOptions = {
    url: '',
    type: 'auto',
    format: 'json'
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--url':
      case '-u':
        options.url = args[++i];
        break;
      case '--type':
      case '-t':
        options.type = args[++i] as any;
        break;
      case '--format':
      case '-f':
        options.format = args[++i] as any;
        break;
      case '--max':
      case '-m':
        options.maxItems = parseInt(args[++i]);
        break;
      case '--scroll':
        options.scroll = true;
        break;
    }
  }

  if (!options.url) {
    console.error('Usage: npm run scrape -- --url <url> [--type list|article|table] [--format json|csv|markdown]');
    process.exit(1);
  }

  const scraper = new SmartScraper();
  
  try {
    await scraper.init();
    console.log(`🔍 Scraping: ${options.url}`);
    
    const result = await scraper.scrape(options);
    
    console.log(`\n✅ Detected type: ${result.data.type}`);
    console.log(`📊 Format: ${result.format}\n`);
    console.log(result.raw);
    
  } catch (error) {
    console.error('❌ Error:', error);
    process.exit(1);
  } finally {
    await scraper.close();
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { main };
