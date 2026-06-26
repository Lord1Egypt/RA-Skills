#!/usr/bin/env node
/**
 * Fetch supermarket specials using Puppeteer browser automation
 * Usage: node fetch_with_puppeteer.js [woolworths|coles|both]
 */
const puppeteer = require('puppeteer');

async function fetchWoolworths() {
    const browser = await puppeteer.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });
    const page = await browser.newPage();
    
    try {
        await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
        await page.goto('https://www.woolworths.com.au/shop/catalogue', { 
            waitUntil: 'networkidle2',
            timeout: 30000 
        });
        
        await new Promise(r => setTimeout(r, 5000));
        
        const products = await page.evaluate(() => {
            const items = [];
            const cards = document.querySelectorAll('article, .product-tile, [data-testid*="product"], .product-card');
            
            cards.forEach(card => {
                const text = card.innerText.replace(/\n/g, ' ').trim();
                if (text.includes('$') && text.length > 10 && text.length < 200) {
                    items.push(text.substring(0, 150));
                }
            });
            return items.slice(0, 20);
        });
        
        return { specials: products, count: products.length };
    } catch (e) {
        return { error: e.message };
    } finally {
        await browser.close();
    }
}

async function fetchColes() {
    const browser = await puppeteer.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });
    const page = await browser.newPage();
    
    try {
        await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
        await page.goto('https://www.coles.com.au/on-special', { 
            waitUntil: 'networkidle2',
            timeout: 30000 
        });
        
        await new Promise(r => setTimeout(r, 5000));
        
        const products = await page.evaluate(() => {
            const items = [];
            const cards = document.querySelectorAll('article, .product-tile, [data-testid*="product"], .product-card');
            
            cards.forEach(card => {
                const text = card.innerText.replace(/\n/g, ' ').trim();
                if (text.includes('$') && text.length > 10 && text.length < 200) {
                    items.push(text.substring(0, 150));
                }
            });
            return items.slice(0, 20);
        });
        
        return { specials: products, count: products.length };
    } catch (e) {
        return { error: e.message };
    } finally {
        await browser.close();
    }
}

async function main() {
    const args = process.argv.slice(2);
    const which = args[0] || 'both';
    
    let woolworths = null;
    let coles = null;
    
    if (which === 'woolworths' || which === 'both') {
        console.log('Fetching Woolworths...');
        woolworths = await fetchWoolworths();
    }
    
    if (which === 'coles' || which === 'both') {
        console.log('Fetching Coles...');
        coles = await fetchColes();
    }
    
    console.log(JSON.stringify({ woolworths, coles }, null, 2));
}

main().catch(console.error);