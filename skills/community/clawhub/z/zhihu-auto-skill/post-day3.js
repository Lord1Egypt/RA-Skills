#!/usr/bin/env node
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';
import { createDecipheriv } from 'crypto';
const CP=resolve(homedir(),'.hermes','credentials','zhihu-cookies.enc');
function dk(){const k=Buffer.from(process.env.ZHIHU_COOKIE_KEY,'hex');const d=readFileSync(CP);const iv=d.subarray(0,12),tag=d.subarray(12,28),ct=d.subarray(28);const dec=createDecipheriv('aes-256-gcm',k,iv);dec.setAuthTag(tag);return JSON.parse(Buffer.concat([dec.update(ct),dec.final()]).toString());}
const ck=dk(),b=await chromium.launch({headless:false,args:['--disable-blink-features=AutomationControlled']}),ctx=await b.newContext({viewport:{width:1280,height:800},locale:'zh-CN'});
await ctx.addCookies(ck);const p=await ctx.newPage();
await p.goto('https://www.zhihu.com/',{waitUntil:'networkidle',timeout:30000});await p.waitForTimeout(2000);
if(!await p.$('.AppHeader-profileAvatar')){console.log('❌ 未登录');await b.close();process.exit(1);}
console.log('✅ 已登录');
const content=readFileSync('/Users/liubo/WorkBuddy/2026-05-13-task-11/回答5-体制内技术人职业发展.md','utf-8');
const qid='315426975';
console.log('📝 question/'+qid);
await p.goto('https://www.zhihu.com/question/'+qid,{waitUntil:'networkidle',timeout:30000});await p.waitForTimeout(2000);
await p.evaluate(()=>{for(const b of document.querySelectorAll('button')){if(b.textContent.includes('写回答')){b.click();return;}}});await p.waitForTimeout(2000);
await p.evaluate((text)=>{const ed=document.querySelector('.ProseMirror')||document.querySelector('[contenteditable="true"]');if(ed){ed.focus();const dt=new DataTransfer();dt.setData('text/plain',text);ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true}));}},content);await p.waitForTimeout(2000);
console.log('  ✅ 已填入');
await p.evaluate(()=>{for(const b of document.querySelectorAll('button')){if(b.textContent.includes('发布')||b.textContent.includes('提交回答')){b.click();return;}}});await p.waitForTimeout(3000);
console.log('  ✅ 已发布');
await b.close();
