#!/usr/bin/env node
/**
 * Quick script: Open browser with saved cookies and extract Zhihu profile info
 */
import { chromium } from 'playwright';
import { resolve } from 'path';
import { homedir } from 'os';
import { readFileSync, writeFileSync } from 'fs';
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
  const data = readFileSync(COOKIE_PATH);
  const iv = data.subarray(0, IV_LENGTH);
  const authTag = data.subarray(IV_LENGTH, IV_LENGTH + AUTH_TAG_LENGTH);
  const ciphertext = data.subarray(IV_LENGTH + AUTH_TAG_LENGTH);
  const decipher = createDecipheriv(ALGORITHM, getEncryptionKey(), iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return JSON.parse(decrypted.toString('utf-8'));
}

async function main() {
  console.log('🔍 正在通过浏览器获取你的知乎账号信息...\n');

  const cookies = decryptCookies();
  console.log(`✅ Cookie 解密成功，共 ${cookies.length} 条`);
  
  // Show key cookies
  const keyCookies = cookies.filter(c => ['z_c0', 'd_c0', 'z_login', 'unlock_ticket'].includes(c.name));
  console.log('  关键Cookie:');
  keyCookies.forEach(c => console.log(`    ${c.name}: ${c.value.substring(0, 30)}...`));
  console.log('');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    locale: 'zh-CN',
  });
  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // 1. Go to homepage
    console.log('📡 访问知乎首页...');
    await page.goto('https://www.zhihu.com/', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // Check login status
    const isLoggedIn = await page.$('.AppHeader-profileAvatar');
    console.log(`  登录状态: ${isLoggedIn ? '✅ 已登录' : '❌ 未登录（Cookie 可能已过期）'}`);
    
    if (!isLoggedIn) {
      console.log('  ⚠️ Cookie 似乎已过期，需要重新登录');
      await browser.close();
      return;
    }

    // Try to get profile link
    const profileHref = await page.$eval('a[href*="/people/"]', el => el.getAttribute('href')).catch(() => null);
    console.log(`  个人主页链接: ${profileHref || '未找到'}`);
    
    let urlToken = null;
    if (profileHref) {
      const match = profileHref.match(/\/people\/([^/?]+)/);
      urlToken = match ? match[1] : null;
    }
    
    // If no profile link, try going to notification/settings to get user info
    if (!urlToken) {
      console.log('  尝试从设置页面获取...');
      await page.goto('https://www.zhihu.com/settings/profile', { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000);
      
      urlToken = await page.evaluate(() => {
        // Try to find user info from various sources
        const scripts = document.querySelectorAll('script');
        for (const s of scripts) {
          const t = s.textContent || '';
          if (t.includes('url_token') || t.includes('urlToken')) {
            const m = t.match(/["']url_token["']\s*:\s*["']([^"']+)["']/) || 
                      t.match(/["']urlToken["']\s*:\s*["']([^"']+)["']/);
            if (m) return m[1];
          }
        }
        return null;
      });
    }
    
    if (!urlToken) {
      // Try the /api/v4/me endpoint
      console.log('  尝试 /api/v4/me 端点...');
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
        console.log(`  ✅ 通过 /api/v4/me 获取成功: ${urlToken}`);
      }
    }

    if (!urlToken) {
      console.log('  ❌ 无法获取 url_token');
      await browser.close();
      return;
    }

    console.log(`  url_token: ${urlToken}`);

    // 2. Get full user profile
    console.log('\n📡 获取完整用户资料...');
    const userResult = await page.evaluate(async (token) => {
      try {
        const res = await fetch(`https://www.zhihu.com/api/v4/members/${token}?include=answer_count,article_count,question_count,voteup_count,thanked_count,favorited_count,follower_count,following_count,columns_count,following_topic_count,following_question_count,following_columns_count,favorite_count,shared_count,locations,employments,educations,business,gender,headline,description,avatar_url`, {
          headers: {
            'Accept': 'application/json',
            'x-requested-with': 'fetch',
          },
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
      console.log('\n╔═══════════════════════════════════════════╗');
      console.log('║        📋 你的知乎账号详情               ║');
      console.log('╠═══════════════════════════════════════════╣');
      console.log(`║  用户名:     ${u.name}`);
      console.log(`║  URL Token:  ${u.url_token}`);
      console.log(`║  用户ID:     ${u.id}`);
      console.log(`║  简介:       ${u.headline || '(未设置)'}`);
      if (u.description) console.log(`║  描述:       ${u.description.substring(0, 60)}...`);
      if (u.gender >= 0) console.log(`║  性别:       ${u.gender === 0 ? '女' : u.gender === 1 ? '男' : '未知'}`);
      if (u.business?.name) console.log(`║  行业:       ${u.business.name}`);
      if (u.locations?.length) console.log(`║  所在地:     ${u.locations.map(l => l.name).join(', ')}`);
      if (u.employments?.length) console.log(`║  职业:       ${u.employments.map(e => `${e.company?.name || ''} ${e.job?.name || ''}`).join('; ')}`);
      if (u.educations?.length) console.log(`║  教育:       ${u.educations.map(e => `${e.school?.name || ''} ${e.major?.name || ''}`).join('; ')}`);
      console.log('╠═══════════════════════════════════════════╣');
      console.log('║         📊 数据统计                       ║');
      console.log('╠═══════════════════════════════════════════╣');
      console.log(`║  关注者:     ${(u.follower_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  正在关注:   ${(u.following_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  获得赞同:   ${(u.voteup_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  获得感谢:   ${(u.thanked_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  获得收藏:   ${(u.favorited_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  分享数:     ${(u.shared_count || 0).toLocaleString().padStart(10)}`);
      console.log('╠═══════════════════════════════════════════╣');
      console.log('║         📝 内容产出                       ║');
      console.log('╠═══════════════════════════════════════════╣');
      console.log(`║  回答数:     ${(u.answer_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  文章数:     ${(u.article_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  提问数:     ${(u.question_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  专栏数:     ${(u.columns_count || 0).toLocaleString().padStart(10)}`);
      console.log('╠═══════════════════════════════════════════╣');
      console.log('║         🔖 兴趣关注                       ║');
      console.log('╠═══════════════════════════════════════════╣');
      console.log(`║  关注话题:   ${(u.following_topic_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  关注问题:   ${(u.following_question_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  关注专栏:   ${(u.following_columns_count || 0).toLocaleString().padStart(10)}`);
      console.log(`║  收藏夹数:   ${(u.favorite_count || 0).toLocaleString().padStart(10)}`);
      console.log('╚═══════════════════════════════════════════╝');
      console.log(`\n🔗 个人主页: https://www.zhihu.com/people/${u.url_token}`);

      // 3. Try to get recent answers (if any)
      if (u.answer_count > 0) {
        console.log('\n📡 获取最近回答...');
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
            return { success: false, status: res.status };
          } catch (e) {
            return { success: false, error: e.message };
          }
        }, urlToken);

        if (answersResult.success && answersResult.data.data) {
          const answers = answersResult.data.data;
          console.log(`  最近 ${answers.length} 条回答:`);
          answers.forEach((a, i) => {
            const qTitle = a.question?.title || '(未知问题)';
            const votes = a.voteup_count || 0;
            const comments = a.comment_count || 0;
            const time = new Date(a.created_time * 1000).toLocaleString('zh-CN');
            console.log(`  ${i + 1}. [👍${votes} 💬${comments}] ${qTitle.substring(0, 60)}`);
            console.log(`     时间: ${time}`);
          });
        }
      }

      // 4. Get recent articles
      if (u.article_count > 0) {
        console.log('\n📡 获取最近文章...');
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
            return { success: false, status: res.status };
          } catch (e) {
            return { success: false, error: e.message };
          }
        }, urlToken);

        if (articlesResult.success && articlesResult.data.data) {
          const articles = articlesResult.data.data;
          console.log(`  最近 ${articles.length} 篇文章:`);
          articles.forEach((a, i) => {
            const title = a.title || '(无标题)';
            const votes = a.voteup_count || 0;
            const comments = a.comment_count || 0;
            const time = new Date(a.created_time * 1000 || a.created * 1000).toLocaleString('zh-CN');
            console.log(`  ${i + 1}. [👍${votes} 💬${comments}] ${title.substring(0, 60)}`);
            console.log(`     时间: ${time}`);
          });
        }
      }

      // 5. Get following topics (to understand interests)
      console.log('\n📡 获取关注的话题...');
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
          return { success: false, status: res.status };
        } catch (e) {
          return { success: false, error: e.message };
        }
      }, urlToken);

      if (topicsResult.success && topicsResult.data.data) {
        const topics = topicsResult.data.data;
        console.log(`  关注的话题 (${topics.length}个):`);
        topics.forEach((t, i) => {
          const topic = t.topic || t;
          console.log(`  ${i + 1}. ${topic.name || topic.title || '(未知)'} ${topic.followers_count ? `(${topic.followers_count.toLocaleString()} 关注者)` : ''}`);
        });
      }

      // Save profile data
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

      const profilePath = '/Users/liubo/WorkBuddy/2026-05-13-task-11/zhihu_profile.json';
      writeFileSync(profilePath, JSON.stringify(profileData, null, 2));
      console.log(`\n💾 完整账号数据已保存到: zhihu_profile.json`);

    } else {
      console.log(`❌ 用户API请求失败: ${userResult.status || userResult.error}`);
    }

  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await browser.close();
  }
}

main();
