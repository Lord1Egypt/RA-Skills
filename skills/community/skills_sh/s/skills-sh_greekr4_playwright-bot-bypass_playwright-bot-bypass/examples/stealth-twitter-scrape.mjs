#!/usr/bin/env node
/**
 * Stealth Twitter/X Scraping Example
 * Scrape public Twitter profiles without login
 *
 * Usage: node stealth-twitter-scrape.mjs [username]
 * Requires: npm install rebrowser-playwright
 *
 * Note: X may require login for some profiles since 2023.
 */

import os from 'node:os';
import path from 'node:path';
import { createStealthBrowser, humanDelay, simulateMouseMovement } from '../scripts/stealth-template.mjs';

const username = process.argv[2] || 'elonmusk';

async function scrapeTwitterProfile(username) {
  console.log(`Scraping @${username} profile...\n`);

  const { browser, page } = await createStealthBrowser();

  try {
    await page.goto(`https://x.com/${username}`, { waitUntil: 'domcontentloaded' });

    // Simulate human behavior
    await simulateMouseMovement(page);
    await humanDelay(1000, 2000);

    // Wait for tweets to render
    await page.waitForSelector('article', { timeout: 15000 }).catch(() => {});

    const title = await page.title();
    if (!title.includes('@')) {
      console.log('Profile not loaded. May require login or be restricted.');
      await page.screenshot({ path: path.join(os.tmpdir(), 'twitter-blocked.png') });
      return;
    }

    const data = await page.evaluate(() => {
      const articles = document.querySelectorAll('article');
      const tweets = Array.from(articles).slice(0, 10).map(article => {
        const text = article.innerText.substring(0, 200);
        const time = article.querySelector('time')?.getAttribute('datetime') || '';
        return { text, time };
      });

      return {
        title: document.title,
        url: window.location.href,
        tweetCount: articles.length,
        tweets
      };
    });

    console.log(`Profile loaded: ${data.title}`);
    console.log(`Tweets found: ${data.tweetCount}\n`);

    data.tweets.forEach((tweet, i) => {
      console.log(`--- Tweet ${i + 1} (${tweet.time}) ---`);
      console.log(`${tweet.text.substring(0, 120)}...\n`);
    });

    const out = path.join(os.tmpdir(), `twitter-${username}.png`);
    await page.screenshot({ path: out });
    console.log(`Screenshot saved: ${out}\n`);
  } catch (err) {
    console.error('Error:', err.message);
    await page.screenshot({ path: path.join(os.tmpdir(), 'twitter-error.png') }).catch(() => {});
  } finally {
    await browser.close();
  }
}

scrapeTwitterProfile(username).catch(console.error);
