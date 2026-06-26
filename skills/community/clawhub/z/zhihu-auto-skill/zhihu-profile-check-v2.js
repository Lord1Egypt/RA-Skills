#!/usr/bin/env node
/**
 * Zhihu profile check - combines login + profile extraction in one session
 * Uses non-headless browser to avoid detection
 */
import { chromium } from 'playwright';
import { resolve } from 'path';
import { homedir } from 'os';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { createDecipheriv } from 'crypto';

const COOKIE_PATH = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');
const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 12;
const AUTH_TAG_LENGTH = 16;

function getEncryptionKey() {
  const key = process.env.ZHIHU_COOKIE_KEY;
  if (!key || key.length !== 64) {
    throw new Error('ZHIHU_COOKIE_KEY not set or invalid');
  }
  return Buffer.from(key, 'hex');
}

function decryptCookies() {
  if (!existsSync(COOKIE_PATH)) return null;
  const data = readFileSync(COOKIE_PATH);
  const iv = data.subarray(0, IV_LENGTH);
  const authTag = data.subarray(IV_LENGTH, IV_LENGTH + AUTH_TAG_LENGTH);
  const ciphertext = data.subarray(IV_LENGTH + AUTH_TAG_LENGTH);
  const decipher = createDecipheriv(ALGORITHM, getEncryptionKey(), iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return JSON.parse(decrypted.toString('utf-8'));
}

async function extractProfile(page) {
  // Try multiple approaches to get url_token
  let urlToken = null;
  
  // Method 1: Navigate to profile page via API
  console.log('  📡 方法1: 通过 /api/v4/me 获取...');
  const meResult = await page.evaluate(async () => {
    try {
      const res = await fetch('https://www.zhihu.com/api/v4/me', {
        headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
        credentials: 'include',
      });
      if (res.ok) {
        const data = await res.json();
        return { success: true, data };
      }
      return { success: false, status: res.status };
    } catch (e) {
      return { success: false, error: e.message };
    }
  });
  
  if (meResult.success) {
    urlToken = meResult.data.url_token || meResult.data.id;
    console.log(`  ✅ 通过 /api/v4/me 获取: ${urlToken}`);
  } else {
    console.log(`  ❌ /api/v4/me 失败: ${meResult.status || meResult.error}`);
    
    // Method 2: Try to get profile link from page
    const profileHref = await page.$eval('a[href*="/people/"]', el => el.getAttribute('href')).catch(() => null);
    if (profileHref) {
      const match = profileHref.match(/\/people\/([^/?]+)/);
      urlToken = match ? match[1] : null;
      console.log(`  ✅ 从页面链接获取: ${urlToken}`);
    }
  }
  
  if (!urlToken) {
    console.log('  ❌ 无法获取 url_token');
    return null;
  }
  
  // Get full profile
  console.log('\n📡 获取完整用户资料...');
  const userResult = await page.evaluate(async (token) => {
    try {
      const res = await fetch(`https://www.zhihu.com/api/v4/members/${token}?include=answer_count,article_count,question_count,voteup_count,thanked_count,favorited_count,follower_count,following_count,columns_count,following_topic_count,following_question_count,following_columns_count,favorite_count,shared_count,locations,employments,educations,business,gender,headline,description,avatar_url`, {
        headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
        credentials: 'include',
      });
      if (res.ok) {
        const data = await res.json();
        return { success: true, data };
      }
      return { success: false, status: res.status };
    } catch (e) {
      return { success: false, error: e.message };
    }
  }, urlToken);

  if (userResult.success) {
    const u = userResult.data;
    console.log('\n╔══════════════════════════════════════════════╗');
    console.log('║          📋 你的知乎账号详情                 ║');
    console.log('╠══════════════════════════════════════════════╣');
    console.log(`║  用户名:      ${u.name || 'N/A'}`);
    console.log(`║  URL Token:   ${u.url_token || 'N/A'}`);
    console.log(`║  用户ID:      ${u.id || 'N/A'}`);
    console.log(`║  一句话介绍:   ${u.headline || '(未设置)'}`);
    if (u.description) console.log(`║  个人描述:     ${u.description.substring(0, 55)}...`);
    if (u.gender >= 0) console.log(`║  性别:         ${u.gender === 0 ? '女' : u.gender === 1 ? '男' : '未知'}`);
    if (u.business?.name) console.log(`║  行业:         ${u.business.name}`);
    if (u.locations?.length) console.log(`║  所在地:       ${u.locations.map(l => l.name).join(', ')}`);
    if (u.employments?.length) console.log(`║  职业:         ${u.employments.map(e => `${e.company?.name || ''} ${e.job?.name || ''}`).join('; ')}`);
    if (u.educations?.length) console.log(`║  教育背景:     ${u.educations.map(e => `${e.school?.name || ''} ${e.major?.name || ''}`).join('; ')}`);
    console.log('╠══════════════════════════════════════════════╣');
    console.log('║              📊 社交影响力                    ║');
    console.log('╠══════════════════════════════════════════════╣');
    console.log(`║  关注者:       ${(u.follower_count || 0).toLocaleString()}`);
    console.log(`║  正在关注:     ${(u.following_count || 0).toLocaleString()}`);
    console.log(`║  获得赞同:     ${(u.voteup_count || 0).toLocaleString()}`);
    console.log(`║  获得感谢:     ${(u.thanked_count || 0).toLocaleString()}`);
    console.log(`║  获得收藏:     ${(u.favorited_count || 0).toLocaleString()}`);
    console.log('╠══════════════════════════════════════════════╣');
    console.log('║              📝 内容产出                      ║');
    console.log('╠══════════════════════════════════════════════╣');
    console.log(`║  回答数:       ${(u.answer_count || 0).toLocaleString()}`);
    console.log(`║  文章数:       ${(u.article_count || 0).toLocaleString()}`);
    console.log(`║  提问数:       ${(u.question_count || 0).toLocaleString()}`);
    console.log(`║  专栏数:       ${(u.columns_count || 0).toLocaleString()}`);
    console.log(`║  分享数:       ${(u.shared_count || 0).toLocaleString()}`);
    console.log('╠══════════════════════════════════════════════╣');
    console.log('║              🔖 兴趣关注                      ║');
    console.log('╠══════════════════════════════════════════════╣');
    console.log(`║  关注话题:     ${(u.following_topic_count || 0).toLocaleString()}`);
    console.log(`║  关注问题:     ${(u.following_question_count || 0).toLocaleString()}`);
    console.log(`║  关注专栏:     ${(u.following_columns_count || 0).toLocaleString()}`);
    console.log(`║  收藏夹数:     ${(u.favorite_count || 0).toLocaleString()}`);
    console.log('╚══════════════════════════════════════════════╝');
    console.log(`\n🔗 个人主页: https://www.zhihu.com/people/${u.url_token}`);
    console.log(`🖼️  头像: ${u.avatar_url || 'N/A'}`);

    // Get recent answers
    if (u.answer_count > 0) {
      console.log('\n📡 最近回答 (最多5条):');
      const answersResult = await page.evaluate(async (token) => {
        try {
          const res = await fetch(`https://www.zhihu.com/api/v4/members/${token}/answers?limit=5&sort_by=created`, {
            headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
            credentials: 'include',
          });
          if (res.ok) {
            const data = await res.json();
            return { success: true, data };
          }
          return { success: false };
        } catch (e) { return { success: false }; }
      }, urlToken);
      
      if (answersResult.success && answersResult.data.data) {
        answersResult.data.data.forEach((a, i) => {
          const qTitle = a.question?.title || '(未知问题)';
          const votes = a.voteup_count || 0;
          const time = new Date(a.created_time * 1000).toLocaleString('zh-CN');
          const url = `https://www.zhihu.com/question/${a.question?.id}/answer/${a.id}`;
          console.log(`  ${i+1}. [👍${votes}] ${qTitle.substring(0, 55)}`);
          console.log(`      ${time} | ${url}`);
        });
      }
    }

    // Get recent articles
    if (u.article_count > 0) {
      console.log('\n📡 最近文章 (最多5篇):');
      const articlesResult = await page.evaluate(async (token) => {
        try {
          const res = await fetch(`https://www.zhihu.com/api/v4/members/${token}/articles?limit=5`, {
            headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
            credentials: 'include',
          });
          if (res.ok) {
            const data = await res.json();
            return { success: true, data };
          }
          return { success: false };
        } catch (e) { return { success: false }; }
      }, urlToken);
      
      if (articlesResult.success && articlesResult.data.data) {
        articlesResult.data.data.forEach((a, i) => {
          const title = a.title || '(无标题)';
          const votes = a.voteup_count || 0;
          const time = new Date(a.created_time * 1000 || a.created * 1000).toLocaleString('zh-CN');
          console.log(`  ${i+1}. [👍${votes}] ${title.substring(0, 55)}`);
          console.log(`      ${time}`);
        });
      }
    }

    // Get following topics
    console.log('\n📡 关注的话题 (最多20个):');
    const topicsResult = await page.evaluate(async (token) => {
      try {
        const res = await fetch(`https://www.zhihu.com/api/v4/members/${token}/following-topic-contributions?limit=20`, {
          headers: { 'Accept': 'application/json', 'x-requested-with': 'fetch' },
          credentials: 'include',
        });
        if (res.ok) {
          const data = await res.json();
          return { success: true, data };
        }
        return { success: false };
      } catch (e) { return { success: false }; }
    }, urlToken);
    
    if (topicsResult.success && topicsResult.data.data) {
      topicsResult.data.data.forEach((t, i) => {
        const topic = t.topic || t;
        console.log(`  ${i+1}. ${topic.name || topic.title || '(未知)'}${topic.followers_count ? ` (${topic.followers_count.toLocaleString()}关注)` : ''}`);
      });
    }

    // Save profile
    const profileData = {
      name: u.name,
      url_token: u.url_token,
      id: u.id,
      headline: u.headline || '',
      description: u.description || '',
      avatar_url: u.avatar_url || '',
      gender: u.gender,
      locations: u.locations || [],
      employments: u.employments || [],
      educations: u.educations || [],
      business: u.business || null,
      follower_count: u.follower_count || 0,
      following_count: u.following_count || 0,
      answer_count: u.answer_count || 0,
      article_count: u.article_count || 0,
      question_count: u.question_count || 0,
      voteup_count: u.voteup_count || 0,
      thanked_count: u.thanked_count || 0,
      favorited_count: u.favorited_count || 0,
      shared_count: u.shared_count || 0,
      columns_count: u.columns_count || 0,
      following_topic_count: u.following_topic_count || 0,
      following_question_count: u.following_question_count || 0,
      following_columns_count: u.following_columns_count || 0,
      favorite_count: u.favorite_count || 0,
      profile_url: `https://www.zhihu.com/people/${u.url_token}`,
      fetched_at: new Date().toISOString(),
    };
    
    writeFileSync('/Users/liubo/WorkBuddy/2026-05-13-task-11/zhihu_profile.json', JSON.stringify(profileData, null, 2));
    console.log(`\n💾 完整数据已保存到: zhihu_profile.json`);
    return profileData;
  } else {
    console.log(`❌ 用户API返回: ${userResult.status || userResult.error}`);
    return null;
  }
}

async function tryExistingCookies(cookies) {
  console.log('🔍 尝试使用已有Cookie...\n');
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    locale: 'zh-CN',
  });
  await context.addCookies(cookies);
  const page = await context.newPage();
  
  try {
    await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
    
    const isLoggedIn = await page.$('.AppHeader-profileAvatar');
    if (isLoggedIn) {
      console.log('✅ Cookie有效，已登录');
      const profile = await extractProfile(page);
      await browser.close();
      return profile;
    } else {
      console.log('❌ Cookie已过期，需要重新登录');
      await browser.close();
      return null;
    }
  } catch (e) {
    console.error('错误:', e.message);
    await browser.close();
    return null;
  }
}

async function loginAndExtract() {
  console.log('🔐 打开浏览器登录知乎...\n');
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    locale: 'zh-CN',
  });
  const page = await context.newPage();
  
  try {
    await page.goto('https://www.zhihu.com/signin', { waitUntil: 'networkidle', timeout: 60000 });
    console.log('✅ 登录页面已打开，请扫码或账号登录...');
    console.log('⏳ 等待登录完成（超时5分钟）...\n');
    
    await page.waitForFunction(() => {
      return !!document.querySelector('.AppHeader-profileAvatar');
    }, { timeout: 5 * 60 * 1000 });
    
    await page.waitForTimeout(3000);
    console.log('✅ 登录成功！\n');
    
    // Save cookies
    const cookies = await context.cookies();
    const { encryptAndSaveCookies } = await import('./scripts/zhihu-core.js');
    encryptAndSaveCookies(cookies);
    console.log('✅ Cookie已保存\n');
    
    // Navigate to home
    await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    const profile = await extractProfile(page);
    await browser.close();
    return profile;
  } catch (e) {
    console.error('❌ 错误:', e.message);
    await browser.close();
    return null;
  }
}

async function main() {
  // Try existing cookies first
  const cookies = decryptCookies();
  if (cookies) {
    const profile = await tryExistingCookies(cookies);
    if (profile) return;
  }
  
  // Login fresh
  await loginAndExtract();
}

main();
