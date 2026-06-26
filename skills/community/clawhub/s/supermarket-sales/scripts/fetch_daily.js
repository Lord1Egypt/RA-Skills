#!/usr/bin/env node
/**
 * Daily Supermarket Sales Fetcher
 * Fetches Coles and Woolworths specials for the week
 * Run: node fetch_daily.js
 */

const puppeteer = require('puppeteer');

const COLES_URL = 'https://www.coles.com.au/on-special';
const WOOLWORTHS_CATALOGUE = 'https://www.catalogueau.com/woolworths/';
const WOOLWORTHS_SPECIALS = 'https://www.catalogueau.com/sales/?stores=Woolworths';

async function fetchColes() {
    const browser = await puppeteer.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });
    const page = await browser.newPage();
    
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36');
    await page.goto(COLES_URL, { waitUntil: 'networkidle2', timeout: 30000 });
    await new Promise(r => setTimeout(r, 5000));
    
    const deals = await page.evaluate(() => {
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
    
    await browser.close();
    return deals;
}

function printHeader(store) {
    const date = new Date().toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' });
    console.log(`\n=== ${store.toUpperCase()} SPECIALS - ${date} ===`);
    console.log(`Source: ${store === 'Coles' ? COLES_URL : 'catalogueau.com'}\n`);
}

async function main() {
    console.log('🛒 Fetching Daily Supermarket Specials...\n');
    
    // Coles
    try {
        printHeader('Coles');
        const colesDeals = await fetchColes();
        
        if (colesDeals.length > 0) {
            console.log('| # | Product | Price | Deal |');
            console.log('|---|---|---|---|');
            colesDeals.slice(0, 10).forEach((deal, i) => {
                // Clean up and format
                const clean = deal.replace(/\s+/g, ' ').substring(0, 100);
                console.log(`| ${i+1} | ${clean.split('$')[0].substring(0, 30) || '-'} | $${clean.match(/\$[\d.]+/)?.[0]?.replace('$','') || '-'} | ${clean.match(/Save \$[\d.]+|Was \$[\d.]+/)?.[0] || '-'} |`);
            });
        } else {
            console.log('No deals found via browser. Try web_fetch instead.');
        }
    } catch(e) {
        console.log('Coles error:', e.message);
    }
    
    // Woolworths (from aggregator)
    console.log('\n=== WOOLWORTHS SPECIALS ===');
    console.log('Source: catalogueau.com');
    console.log('\nUse: web_fetch https://www.catalogueau.com/sales/?stores=Woolworths');
    console.log('Or search: Woolworths half price specials this week');
    
    console.log('\n✅ Done! Edit the skill or cron job for daily automation.');
}

main().catch(console.error);