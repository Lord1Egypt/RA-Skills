#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const CP = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');
function decrypt() {
  const key = Buffer.from(process.env.ZHIHU_COOKIE_KEY, 'hex');
  const d = readFileSync(CP);
  const iv=d.subarray(0,12),tag=d.subarray(12,28),ct=d.subarray(28);
  const dec=createDecipheriv('aes-256-gcm',key,iv);
  dec.setAuthTag(tag);
  return JSON.parse(Buffer.concat([dec.update(ct),dec.final()]).toString());
}

async function main() {
  const cookies=decrypt();
  const b=await chromium.launch({headless:false,args:['--disable-blink-features=AutomationControlled']});
  const c=await b.newContext({viewport:{width:1280,height:800},locale:'zh-CN'});
  await c.addCookies(cookies);
  const p=await c.newPage();

  await p.goto('https://www.zhihu.com/',{waitUntil:'networkidle',timeout:30000});
  await p.waitForTimeout(2000);
  if(!await p.$('.AppHeader-profileAvatar')){console.log('❌ 未登录');await b.close();return;}
  console.log('✅ 已登录\n');

  const urlToken='liu-bo-94-4';

  // ===== CHECK DATA =====
  console.log('📊 数据检查:\n');

  // 1. Check profile stats (follower/answer count changes)
  const profile=await p.evaluate(async(token)=>{
    const r=await fetch('https://www.zhihu.com/api/v4/members/'+token+'?include=answer_count,article_count,follower_count,voteup_count',{
      headers:{'Accept':'application/json','x-requested-with':'fetch'},credentials:'include'
    });
    return r.json();
  },urlToken);
  
  console.log('👤 账号概况:');
  console.log('  关注者: '+(profile.follower_count||0));
  console.log('  获得赞同: '+(profile.voteup_count||0));
  console.log('  回答数: '+(profile.answer_count||0));
  console.log('  文章数: '+(profile.article_count||0));

  // 2. Check recent answers for vote counts
  console.log('\n📄 最近回答数据:');
  const answers=await p.evaluate(async(token)=>{
    const r=await fetch('https://www.zhihu.com/api/v4/members/'+token+'/answers?limit=10&sort_by=created',{
      headers:{'Accept':'application/json','x-requested-with':'fetch'},credentials:'include'
    });
    const d=await r.json();
    return (d.data||[]).map(a=>({
      id:a.id,
      title:a.question?.title?.substring(0,50)||'',
      votes:a.voteup_count||0,
      comments:a.comment_count||0,
      time:new Date(a.created_time*1000).toLocaleString('zh-CN'),
    }));
  },urlToken);
  answers.forEach((a,i)=>{
    const emoji=a.votes>0?'🔥':(a.comments>0?'💬':'⚪');
    console.log('  '+emoji+' [👍'+a.votes+' 💬'+a.comments+'] '+a.title);
    console.log('     '+a.time);
  });

  // 3. Check专栏 stats
  console.log('\n📰 专栏文章数据:');
  const articles=await p.evaluate(async(token)=>{
    const r=await fetch('https://www.zhihu.com/api/v4/members/'+token+'/articles?limit=5',{
      headers:{'Accept':'application/json','x-requested-with':'fetch'},credentials:'include'
    });
    const d=await r.json();
    return (d.data||[]).map(a=>({
      id:a.id,
      title:a.title?.substring(0,50)||'',
      votes:a.voteup_count||0,
      comments:a.comment_count||0,
      views:a.view_count||a.visit_count||'?',
      time:new Date((a.created_time||a.created)*1000).toLocaleString('zh-CN'),
    }));
  },urlToken);
  articles.forEach((a,i)=>{
    console.log('  📰 [👍'+a.votes+' 💬'+a.comments+' 👁'+a.views+'] '+a.title);
  });

  // ===== FIND INTERACTION TARGETS =====
  console.log('\n🎯 寻找互动目标...');
  
  // Visit hot list
  await p.goto('https://www.zhihu.com/hot',{waitUntil:'networkidle',timeout:30000});
  await p.waitForTimeout(2000);

  const hotItems=await p.evaluate(()=>{
    const items=document.querySelectorAll('.HotList-item,.HotItem,[class*="HotItem"]');
    return Array.from(items).slice(0,20).map(item=>{
      const titleEl=item.querySelector('[class*="title"],h2,.HotItem-title');
      const metaEl=item.querySelector('[class*="metrics"],.HotItem-metrics');
      return{
        title:titleEl?.textContent?.trim()?.substring(0,60)||'',
        meta:metaEl?.textContent?.trim()||'',
        link:item.querySelector('a')?.href||'',
      };
    }).filter(i=>i.title);
  });

  console.log('  热榜中可互动话题:');
  const keywords=['政务','数据','安全','城市','AI','政府','数字','科技','信息'];
  let found=0;
  hotItems.forEach(item=>{
    const matched=keywords.filter(k=>item.title.includes(k));
    if(matched.length>0&&found<5){
      console.log('  🔥 ['+matched.join(',')+'] '+item.title);
      console.log('     '+item.link);
      found++;
    }
  });

  console.log('\n⏳ 浏览器保持打开30秒...');
  await p.waitForTimeout(30000);
  await b.close();
}

main();
