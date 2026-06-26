const { chromium } = require('playwright');
const { JSDOM } = require('jsdom');

async function extractArticles(html) {
    const dom = new JSDOM(html);
    const document = dom.window.document;
    const articles = [];

    // 根据我们在上一轮抓取的 DOM 结构选择文章容器
    const articleElements = document.querySelectorAll('a[href^="/preprints"]');

    articleElements.forEach(el => {
        const title = el.querySelector('h4')?.textContent.trim();
        const abstract = el.querySelector('p')?.textContent.trim();
        const doi = el.querySelector('span:last-child')?.textContent.trim();
        
        if (title && abstract) {
            articles.push({ title, abstract, doi });
        }
    });

    return articles;
}

async function run() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    try {
        await page.goto('https://shitjournal.org/', { waitUntil: 'networkidle' });
        const content = await page.content();
        const articles = await extractArticles(content);
        
        console.log(`Found ${articles.length} articles:`);
        articles.forEach(art => {
            console.log(`- ${art.title} [${art.doi}]`);
        });
        
        // 此处后续可集成 LLM 分析与公众号发布
    } catch (error) {
        console.error('Error scraping:', error);
    } finally {
        await browser.close();
    }
}

run();
