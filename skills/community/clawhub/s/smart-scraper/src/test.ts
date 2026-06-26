import { SmartScraper } from './cli.js';

async function test() {
  const scraper = new SmartScraper();
  
  try {
    await scraper.init();
    
    // Test 1: List extraction
    console.log('Test 1: List extraction');
    const listResult = await scraper.scrape({
      url: 'https://news.ycombinator.com',
      type: 'list',
      format: 'json',
      maxItems: 5
    });
    console.log(`Found ${listResult.data.type} with ${(listResult.data as any).items?.length || 0} items\n`);
    
    // Test 2: Article extraction
    console.log('Test 2: Article extraction');
    const articleResult = await scraper.scrape({
      url: 'https://example.com',
      type: 'article',
      format: 'markdown'
    });
    console.log(`Detected: ${articleResult.data.type}\n`);
    
  } catch (error) {
    console.error('Test failed:', error);
  } finally {
    await scraper.close();
  }
}

test();
