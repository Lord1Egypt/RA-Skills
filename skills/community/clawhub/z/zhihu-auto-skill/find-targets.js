#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';

const CP = resolve(homedir(), '.hermes', 'credentials', 'zhihu-cookies.enc');
function decrypt() {
  const key = Buffer.from(process.env.ZHIHU_COOKIE_KEY, 'hex');
  const d = readFileSync(CP);const iv=d.subarray(0,12),tag=d.subarray(12,28),ct=d.subarray(28);
  const dec=createDecipheriv('aes-256-gcm',key,iv);dec.setAuthTag(tag);
  return JSON.parse(Buffer.concat([dec.update(ct),dec.final()]).toString());
}

async function main() {
  const ck=decrypt();
  const b=await chromium.launch({headless:false,args:['--disable-blink-features=AutomationControlled']});
  const ctx=await b.newContext({viewport:{width:1280,height:800},locale:'zh-CN'});
  await ctx.addCookies(ck);
  const p=await ctx.newPage();
  await p.goto('https://www.zhihu.com/',{waitUntil:'networkidle',timeout:30000});
  await p.waitForTimeout(2000);
  console.log('✅ 已登录\n');

  // Search for交互 targets in 数字政府/智慧城市
  const topics=['数字政府建设','智慧城市','政务信息化','等保 网络安全'];
  
  for(const q of topics){
    console.log('🔍 搜索互动目标: '+q);
    const r=await p.evaluate(async(query)=>{
      try{
        const res=await fetch('https://www.zhihu.com/api/v4/search_v3?q='+encodeURIComponent(query)+'&t=general&type=answer&offset=0&limit=5',{
          headers:{'Accept':'application/json','x-requested-with':'fetch'},credentials:'include'
        });
        if(!res.ok) return {error:res.status};
        const d=await res.json();
        return {data:(d.data||[]).slice(0,5).map(item=>{
          const obj=item.object||item;
          return {
            type:obj.type,
            title:obj.question?.title||obj.title||'',
            qid:obj.question?.id||'',
            aid:obj.id||'',
            author:obj.author?.name||'',
            votes:obj.voteup_count||0,
            comments:obj.comment_count||0,
            excerpt:(obj.excerpt||'').substring(0,80),
          };
        })};
      }catch(e){return{error:e.message};}
    },q);
    
    if(r.data){
      r.data.forEach((item,i)=>{
        if(i>=3)return;
        console.log('  '+(i+1)+'. ['+item.author+' 👍'+item.votes+'] '+item.title?.substring(0,60));
        if(item.qid) console.log('     https://www.zhihu.com/question/'+item.qid+'/answer/'+item.aid);
      });
    }else{
      console.log('  搜索失败: '+JSON.stringify(r));
    }
  }

  console.log('\n⏳ 30秒后关闭...');
  await p.waitForTimeout(30000);
  await b.close();
}

main();
