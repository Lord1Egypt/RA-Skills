#!/usr/bin/env node
/**
 * Velora Chat Helper Script
 * Usage: node velora-chat.js <email> <password> <companion> <message>
 */

const { chromium } = require('playwright');

async function veloraChat(email, password, companion, message) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    console.log('1️⃣ Logging in...');
    await page.goto('https://velora.cloudm8.net/login');
    await page.waitForSelector('input[type="email"]');
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/chat**', { timeout: 20000 });
    await page.waitForTimeout(3000);
    console.log('   ✅ Logged in');
    
    console.log('2️⃣ Starting chat with', companion, '...');
    await page.click('text=Neuer Chat');
    await page.waitForTimeout(2000);
    await page.click(`text=${companion}`);
    await page.waitForTimeout(5000);
    console.log('   ✅ Chat started');
    
    console.log('3️⃣ Sending message...');
    const input = await page.locator('input[type="text"], textarea').first();
    await input.fill(message);
    await input.press('Enter');
    await page.waitForTimeout(15000);
    console.log('   ✅ Message sent');
    
    console.log('4️⃣ Getting images...');
    const images = await page.evaluate(() => {
      const imgs = document.querySelectorAll('img');
      return Array.from(imgs).map(img => img.src).slice(0, 3);
    });
    
    console.log('\n📊 Results:');
    console.log('- Chat URL:', page.url());
    console.log('- Images found:', images.length);
    if (images.length > 0) {
      console.log('- Image URLs:');
      images.forEach((url, i) => console.log(`  ${i+1}. ${url}`));
    }
    
    return { success: true, images, chatUrl: page.url() };
  } catch (e) {
    console.error('❌ Error:', e.message);
    return { success: false, error: e.message };
  } finally {
    await browser.close();
  }
}

// CLI usage
const args = process.argv.slice(2);
if (args.length >= 4) {
  veloraChat(args[0], args[1], args[2], args.slice(3).join(' '))
    .then(r => {
      console.log('\n✅ Done');
      process.exit(r.success ? 0 : 1);
    });
} else {
  console.log('Usage: node velora-chat.js <email> <password> <companion> <message>');
  console.log('Example: node velora-chat.js test@test.com Test1234. Lilith "Hey!"');
}