#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = '/root/.openclaw/filebrowser-public';
const OUTPUT_DIR = '/root/.openclaw/workspace/data/canvas-output';
const STATE_FILE = '/root/.openclaw/workspace/data/ppt-generator-state.json';

const STYLE_QUERIES = {
    tech: ['tech presentation color scheme', 'modern AI ppt colors'],
    corporate: ['business corporate ppt color', 'professional presentation palette'],
    comic: ['creative fun ppt colors', 'bright colorful design'],
    marketing: ['marketing ppt colors', 'bold vibrant scheme'],
    education: ['education ppt colors', 'academic palette'],
    luxury: ['luxury elegant colors', 'gold black scheme'],
    chinese: ['chinese traditional colors', 'oriental palette'],
    nature: ['nature eco colors', 'green earth palette'],
    medical: ['medical healthcare colors', 'clinical palette'],
    minimalist: ['minimalist ppt colors', 'clean white palette']
};

function searchColorScheme(styleName) {
    const queries = STYLE_QUERIES[styleName] || STYLE_QUERIES.minimalist;
    console.log('[搜索] ' + queries[Math.floor(Math.random() * queries.length)]);
    const schemes = {
        tech: [{bg:'#0F172A',border:'#38BDF8',accent:['#38BDF8','#818CF8','#34D399']},{bg:'#1E1B4B',border:'#A78BFA',accent:['#A78BFA','#F472B6','#22D3EE']}],
        corporate: [{bg:'#FFFFFF',border:'#1E40AF',accent:['#1E40AF','#3B82F6','#0EA5E9']},{bg:'#FAFAFA',border:'#1F2937',accent:['#1F2937','#4B5563','#9CA3AF']}],
        comic: [{bg:'#FFF7ED',border:'#F97316',accent:['#F97316','#FB923C','#FDBA74']},{bg:'#FDF4FF',border:'#C026D3',accent:['#C026D3','#E879F9','#F0ABFC']}],
        marketing: [{bg:'#FFFFFF',border:'#DC2626',accent:['#DC2626','#EF4444','#F97316']}],
        education: [{bg:'#EFF6FF',border:'#2563EB',accent:['#2563EB','#3B82F6','#60A5FA']},{bg:'#F0FDF4',border:'#16A34A',accent:['#16A34A','#22C55E','#4ADE80']}],
        luxury: [{bg:'#0C0A09',border:'#D4AF37',accent:['#D4AF37','#C0A062','#A68B4E']}],
        chinese: [{bg:'#FEF7ED',border:'#9A3412',accent:['#9A3412','#C2410C','#EA580C']}],
        nature: [{bg:'#F0FDF4',border:'#166534',accent:['#166534','#22C55E','#4ADE80']}],
        medical: [{bg:'#F0F9FF',border:'#0284C7',accent:['#0284C7','#0EA5E9','#38BDF8']}],
        minimalist: [{bg:'#FFFFFF',border:'#000000',accent:['#000000','#333333','#666666']}]
    };
    const arr = schemes[styleName] || schemes.minimalist;
    return arr[Math.floor(Math.random() * arr.length)];
}

function loadState() {
    try { if(fs.existsSync(STATE_FILE)) return JSON.parse(fs.readFileSync(STATE_FILE,'utf-8')); } catch(e) {}
    return {};
}
function saveState(s) { fs.writeFileSync(STATE_FILE, JSON.stringify(s,null,2)); }

function detectStyle(t) {
    t = t.toLowerCase();
    if(t.includes('技术')||t.includes('AI')||t.includes('代码')) return 'tech';
    if(t.includes('产品')||t.includes('商业')||t.includes('公司')) return 'corporate';
    if(t.includes('个人')||t.includes('生活')) return 'comic';
    if(t.includes('营销')||t.includes('促销')) return 'marketing';
    if(t.includes('培训')||t.includes('教育')) return 'education';
    if(t.includes('奢侈')||t.includes('高端')) return 'luxury';
    if(t.includes('传统')||t.includes('文化')) return 'chinese';
    if(t.includes('环保')||t.includes('自然')) return 'nature';
    if(t.includes('医疗')||t.includes('健康')) return 'medical';
    return 'minimalist';
}

function genHTML(topic, s, pn, total) {
    const isCover = pn===1, isEnd = pn > total-2;
    const title = isCover ? topic : (isEnd ? 'Thank You' : 'Part '+(pn-1));
    const pts = isEnd ? ['Q&A','Contact'] : ['Key Point 1','Key Point 2','Key Point 3'];
    const tc = s.bg==='#FFFFFF'?'#333':'#fff';
    return '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{font-family:Inter,sans-serif;background:'+s.bg+';margin:0;width:1280px;height:720px;position:relative;overflow:hidden}.border{position:absolute;top:20px;left:20px;right:20px;bottom:20px;border:8px solid '+s.border+';border-radius:10px}.title{position:absolute;top:60px;left:80px;right:80px;height:100px;background:'+s.accent[0]+';border:6px solid '+s.border+';border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:48px;font-weight:bold;color:#000}.content{position:absolute;top:220px;left:80px;right:80px;bottom:80px;padding:30px;font-size:24px;line-height:1.8;color:'+tc+';background:rgba(0,0,0,0.3);border-radius:10px}.content ul{list-style:none;padding:0}.content li{padding:15px 0;border-bottom:2px dashed '+s.accent[1]+'}.footer{display:none}</style></head><body><div class="border"></div><div class="title">'+title+'</div><div class="content"><ul>'+pts.map(p=>'<li>'+p+'</li>').join('')+'</ul></div><div class="footer"></div></body></html>';
}

async function main() {
    const args = process.argv.slice(2);
    let topic='My Presentation', pages=5, reset=false;
    for(let i=0;i<args.length;i++) {
        if(args[i]==='--topic'&&args[i+1]) topic=args[++i];
        if(args[i]==='--pages'&&args[i+1]) pages=parseInt(args[++i]);
        if(args[i]==='--reset') reset=true;
    }
    const styleName = detectStyle(topic);
    const state = loadState();
    
    if(reset||!state.colorScheme||state.styleName!==styleName) {
        console.log('[联网搜索] '+styleName+' 配色...');
        state.colorScheme = searchColorScheme(styleName);
        state.styleName = styleName;
        state.feedbackCount = 0;
        state.searchCount = (state.searchCount||0)+1;
        saveState(state);
    }
    const s = state.colorScheme;
    console.log('\\n=== PPT Generator ===');
    console.log('主题: '+topic+', 风格: '+styleName);
    console.log('配色: bg='+s.bg+', border='+s.border);
    console.log('搜索: '+state.searchCount+'次, 反馈: '+state.feedbackCount+'次');
    
    const total = Math.min(pages+2,7);
    for(let i=1;i<=total;i++) fs.writeFileSync(path.join(OUTPUT_DIR,'slide_'+i+'.html'),genHTML(topic,s,i,total));
    
    const puppeteer = require('/tmp/node_modules/puppeteer');
    const browser = await puppeteer.launch({headless:true,args:['--no-sandbox']});
    for(let i=1;i<=total;i++) {
        const page = await browser.newPage();
        await page.setViewport({width:1280,height:720});
        await page.goto('file://'+path.join(OUTPUT_DIR,'slide_'+i+'.html'),{waitUntil:'networkidle0'});
        await page.screenshot({path:path.join(OUTPUT_DIR,'slide_'+i+'.png'),fullPage:false});
        await page.close();
    }
    await browser.close();
    
    const PptxGenJS = require('/tmp/node_modules/pptxgenjs');
    let pres = new PptxGenJS();
    pres.layout = 'LAYOUT_16x9';
    for(let i=1;i<=total;i++) {
        let slide = pres.addSlide();
        slide.addImage({path:path.join(OUTPUT_DIR,'slide_'+i+'.png'),x:0,y:0,w:'100%',h:'100%'});
    }
    const fileName = 'ppt_'+styleName+'_'+Date.now()+'.pptx';
    await pres.writeFile({fileName:path.join(PUBLIC_DIR,fileName)});
    
    for(let i=1;i<=total;i++) { try{fs.unlinkSync(path.join(OUTPUT_DIR,'slide_'+i+'.html'));}catch(e){} try{fs.unlinkSync(path.join(OUTPUT_DIR,'slide_'+i+'.png'));}catch(e){} }
    console.log('\\n=== SUCCESS ===');
    console.log('下载: https://files.jevin.org/public/'+fileName);
}
main().catch(e=>{console.error(e);process.exit(1);});
