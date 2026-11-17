import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { analysisInput, verifiedReport, verifiedDraft, reportFiles, safeJson, requestOpenRouter } from './site-topic-relevance.mjs';
import { crawlSite, isPublicAddress, normalizeSiteUrl, robotsPolicy, siteSourceExcerpts } from './topic-core.mjs';

// Synthetic test evidence, never presented as a real website analysis.
const corpus = () => ({url:'https://example.com',discovered:12,sampled:3,skipped:[],pages:[0,1,2].map(i=>({id:'p'+i,url:'https://example.com/'+i,title:'Synthetic page '+i,description:'Synthetic fixture for deterministic testing.',text:((`Synthetic source ${i}: “Create useful presentations” — exact punctuation, café, 演示文稿 🎬.\n\tKeep internal spacing intact. `).repeat(5)).slice(0,700)}))});
const assessment = () => ({purpose:'Synthetic presentation toolkit.',summary:'Synthetic corpus used only for verification.',topics:[{id:'core',name:'Presentation tools',description:'Create presentations.'},{id:'adjacent',name:'Media utilities',description:'Adjacent tools.'}],findings:[{title:'Connect tasks',description:'Link related tools.',pageIds:['p1']}],pages:[{id:'p0',topicId:'core',relevance:95,reason:'Direct creation workflow.',evidence:'lead'},{id:'p1',topicId:'core',relevance:85,reason:'Supports editing.',evidence:'middle'},{id:'p2',topicId:'adjacent',relevance:55,reason:'Adjacent media workflow.',evidence:'end'}]});
const tempTest = async fn => {const dir=await mkdtemp(path.join(tmpdir(),'site-topic-skill-test-'));try{await fn(dir);}finally{await rm(dir,{recursive:true,force:true});}};
const mockResponse = (text, usage = {input_tokens:1000,output_tokens:100,cost:0.0002}) => new Response(JSON.stringify({id:'synthetic-response',status:'completed',model:'openai/gpt-6-luna',usage,output:[{type:'message',content:[{type:'output_text',text}]}]}),{headers:{'Content-Type':'application/json'}});
const request = {instructions:'Synthetic test.',input:{pages:[]},schema:{type:'object'}};

test('public URL and DNS boundaries remain enforced in the standalone bundle',()=>{
  for(const url of ['http://localhost/','https://127.0.0.1/','https://192.168.1.2/','https://private.internal/','https://user:secret@example.com/','file:///tmp/sample.html','https://example.com:8080/'])assert.throws(()=>normalizeSiteUrl(url));
  for(const address of ['127.0.0.1','10.0.0.1','169.254.1.10','100.64.0.1','::1','fc00::1','::ffff:127.0.0.1'])assert.equal(isPublicAddress(address),false,address);
  assert.equal(isPublicAddress('1.1.1.1'),true);
  assert.equal(normalizeSiteUrl('example.com').href,'https://example.com/');
});
test('bundled robots matcher honors terminal anchors, literal punctuation, and rule precedence', () => {
  const policy = robotsPolicy([
    'User-agent: *',
    'Disallow: /docs/*/notes.txt$',
    'Allow: /docs/public/notes.txt$',
    'Disallow: /search?sort=popular$',
  ].join('\n'));
  const allows = (path) => policy.allows(new URL(path, 'https://example.com'));
  assert.equal(allows('/docs/private/notes.txt'), false);
  assert.equal(allows('/docs/private/notesXtxt'), true);
  assert.equal(allows('/docs/public/notes.txt'), true);
  assert.equal(allows('/docs/private/notes.txt/intro'), true);
  assert.equal(allows('/search?sort=popular'), false);
});
test('rebuilt crawler observes the standalone sampling limit even with more eligible pages', async () => {
  const origin = 'https://example.com';
  const paths = ['/articles/one', '/articles/two', '/docs/one', '/products/one', '/help', '/about'];
  const read = async (url) => {
    let text;
    if (url.pathname === '/robots.txt') text = 'User-agent: *\nDisallow:';
    else if (url.pathname === '/sitemap.xml') {
      const entries = paths.map(pathname => `<url><loc>${origin}${pathname}</loc></url>`);
      text = `<urlset>${entries.join('')}</urlset>`;
    } else {
      const paragraph = `Public documentation for the page at ${url.pathname}. `;
      text = `<title>${url.pathname}</title><main><p>${paragraph.repeat(5)}</p></main>`;
    }
    return { url, status: 200, headers: new Headers(), text };
  };
  for (const limit of [3, 5]) {
    const report = await crawlSite(origin, AbortSignal.timeout(5000), read, undefined, {
      pageLimit: limit,
    });
    assert.equal(report.discovered, paths.length + 1);
    assert.equal(report.sampled, limit);
    assert.equal(report.pages.length, limit);
  }
});
test('source-selected evidence preserves Unicode and exact source substrings',()=>{
  const c=corpus(),r=verifiedReport(c,assessment());
  assert.equal(r.model,'current-assistant');assert.equal(r.usage,null);
  for(const p of r.pages){const source=c.pages.find(x=>x.id===p.id);assert.ok(source.text.includes(p.quote));assert.ok(p.quote.length<=220);assert.ok(p.quote.isWellFormed());}
  assert.deepEqual(Object.keys(analysisInput(c).pages[0].excerpts),['lead','middle','end']);
  assert.ok(Object.values(siteSourceExcerpts(c.pages[0].text)).every(x=>c.pages[0].text.includes(x)));
  assert.ok(Math.abs(r.radius-(.05+.15+.45)/3)<1e-12);
  assert.deepEqual(r.pages.map(p=>p.outside),[false,false,true]);
});
test('sitemap-only discovery follows the selected index and filters non-HTML even at extensionless URLs', async () => {
  const origin = 'https://example.com';
  const visited = [];
  const read = async (url) => {
    visited.push(url.pathname);
    const headers = new Headers({ 'Content-Type': 'text/html; charset=utf-8' });
    let text = `<main><p>${('Page-specific editorial content for ' + url.pathname + '. ').repeat(6)}</p></main>`;
    if (url.pathname === '/robots.txt') text = `User-agent: *\nSitemap: ${origin}/sitemap.xml`;
    if (url.pathname === '/selected.xml') {
      text = `<?xml version="1.0"?><s:sitemapindex xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"><s:sitemap><s:loc>${origin}/child.xml</s:loc></s:sitemap></s:sitemapindex>`;
    }
    if (url.pathname === '/child.xml') {
      text = `<urlset>${['one', 'two', 'three', 'output', 'broken', 'redirect'].map((part) =>
        `<url><loc>${origin}/${part}</loc><image:image><image:loc>${origin}/image-endpoint</image:loc></image:image></url>`
      ).join('')}</urlset>`;
    }
    if (url.pathname === '/output') headers.set('Content-Type', 'image/jpeg');
    if (url.pathname === '/broken') text = '\u0000JFIF\u0001' + 'bytes'.repeat(70);
    if (url.pathname === '/redirect') url = new URL('/unlisted', origin);
    return {url, status:200, headers, text};
  };
  const result = await crawlSite(origin + '/selected.xml', AbortSignal.timeout(5000), read, undefined, {
    sitemapOnly: true, pageLimit: 6,
  });
  assert.equal(result.discovered, 6);
  assert.equal(result.sampled, 6);
  assert.deepEqual(result.sitemaps, [origin + '/selected.xml', origin + '/child.xml']);
  assert.deepEqual(result.pages.map(p => p.url), ['one', 'two', 'three'].map(part => origin + '/' + part));
  assert.deepEqual(new Set(result.skipped.map(p=>p.url)), new Set(['output', 'broken', 'redirect'].map(part=>origin+'/'+part)));
  assert.ok(!visited.some(path=>['/', '/sitemap.xml', '/image-endpoint'].includes(path)));
});
test('missing sitemap stops discovery without fetching the homepage, and old binary corpus is rejected', async () => {
  const visited = [];
  const missing = async (url) => {
    visited.push(url.pathname);
    return {url, status:404, headers:new Headers(), text:''};
  };
  await assert.rejects(crawlSite('https://example.com', AbortSignal.timeout(5000), missing, undefined, {
    sitemapOnly:true,
  }), /No eligible page URLs were found in a readable sitemap/);
  assert.deepEqual(visited, ['/robots.txt', '/sitemap.xml']);
  const old = corpus();
  old.pages[0].text = '\u0000JFIF\u0001' + old.pages[0].text;
  assert.throws(() => verifiedReport(old, assessment()), /Corpus contains binary content/);
});
test('missing, duplicated, invented and cross-page evidence cannot produce a report',()=>{
  for(const mutate of [a=>a.pages.pop(),a=>a.pages[1].id='p0',a=>a.pages[0].id='invented',a=>a.pages[0].topicId='invented',a=>a.pages[0].evidence='invented',a=>a.pages[0].evidence='__proto__',a=>a.findings[0].pageIds=['invented'],a=>a.pages[0].relevance=101]){const a=assessment();mutate(a);assert.throws(()=>verifiedReport(corpus(),a));}
  const c=corpus();c.pages[0].url='https://different.example.org/a';assert.throws(()=>verifiedReport(c,assessment()));
});
test('unknown model-written quotation is discarded instead of trusted',()=>{
  const a=assessment();a.pages[0].quote='Invented quotation should not appear';
  assert.ok(!verifiedReport(corpus(),a).pages[0].quote.includes('Invented quotation'));
});
test('unassigned topics do not appear as misleading zero-page groups',()=>{
  const a=assessment();a.topics.push({id:'unused',name:'Unused grouping',description:'No supporting pages.'});
  assert.equal(verifiedReport(corpus(),a).topics.length,2);
});
test('HTML is self-contained, escapes hostile page strings, and excludes private costs',()=>tempTest(async dir=>{
  const c=corpus();c.pages[0].title='</script><img src=x onerror=alert(1)>';
  const r=verifiedReport(c,assessment());r.cost={totalNanoUsd:123456789};r.responseId='secret-response';r.pages[0].cost='private-cost';
  await reportFiles(dir,r);const html=await readFile(path.join(dir,'report.html'),'utf8');const saved=JSON.parse(await readFile(path.join(dir,'report.json'),'utf8'));
  assert.ok(!html.includes('</script><img src=x onerror'));
  assert.ok(html.includes('\\u003c/script>'));
  assert.ok(!html.includes('secret-response'));assert.ok(!html.includes('private-cost'));assert.ok(!html.includes('123456789'));
  assert.ok(!/<script\b[^>]*src=/i.test(html));assert.ok(!/https:\/\/(?:cdn|fonts\.)/.test(html));
  assert.equal(saved.cost,undefined);assert.equal(saved.pages[0].cost,undefined);assert.equal(saved.responseId,undefined);
  assert.equal(JSON.parse(safeJson({text:'</script>\u2028'})).text,'</script>\u2028');
}));
test('actual provider counters are saved before malformed output fails, with no retry',()=>tempTest(async dir=>{
  let calls=0;
  await assert.rejects(requestOpenRouter(request,{dir,key:'synthetic-test-key',fetcher:async()=>{calls++;return mockResponse('not-json');}}));
  const [name]=await readdir(path.join(dir,'private'));const run=JSON.parse(await readFile(path.join(dir,'private',name),'utf8'));
  assert.equal(calls,1);assert.equal(run.status,'failed');assert.equal(run.tokens.inputTokens,1000);assert.equal(run.cost.totalNanoUsd,200000);
}));
test('re-render archives previous artifacts without changing evidence or calling a provider',()=>tempTest(async dir=>{
  const first=verifiedReport(corpus(),assessment());await reportFiles(dir,first);
  const oldHtml=await readFile(path.join(dir,'report.html'),'utf8');
  const second={...first,summary:'Revised assessment summary.'};
  await assert.rejects(reportFiles(dir,second),/--replace/);
  assert.equal(await readFile(path.join(dir,'report.html'),'utf8'),oldHtml);
  await reportFiles(dir,second,{replace:true});
  const [revision]=await readdir(path.join(dir,'revisions'));
  assert.equal(await readFile(path.join(dir,'revisions',revision,'report.html'),'utf8'),oldHtml);
  assert.equal(JSON.parse(await readFile(path.join(dir,'report.json'),'utf8')).summary,second.summary);
  assert.ok(!(await readdir(dir)).some(name=>name.startsWith('.render-')));
}));
test('missing provider usage remains unknown and zero cost remains zero',()=>tempTest(async dir=>{
  const first=await requestOpenRouter(request,{dir,key:'synthetic-test-key',fetcher:async()=>mockResponse('{}',{})});assert.equal(first.usage,null);await first.finish('completed');
  const second=await requestOpenRouter(request,{dir,key:'synthetic-test-key',fetcher:async()=>mockResponse('{}',{input_tokens:1,output_tokens:1,cost:0})});await second.finish('completed');
  const records=await Promise.all((await readdir(path.join(dir,'private'))).map(async n=>JSON.parse(await readFile(path.join(dir,'private',n),'utf8'))));
  assert.ok(records.some(r=>r.cost===null));assert.ok(records.some(r=>r.cost?.totalNanoUsd===0));
}));
test('provider errors redact keys and never follow redirects or retry',()=>tempTest(async dir=>{
  let calls=0;await assert.rejects(requestOpenRouter(request,{dir,key:'synthetic-test-key',fetcher:async(_url,options)=>{calls++;assert.equal(options.redirect,'manual');throw Error('Transport: synthetic-test-key');}}),/\[redacted\]/);
  assert.equal(calls,1);const [name]=await readdir(path.join(dir,'private'));assert.ok(!(await readFile(path.join(dir,'private',name),'utf8')).includes('synthetic-test-key'));
}));
test('draft assessment only links supplied topics and pages',()=>{
  const r=verifiedReport(corpus(),assessment());const d={topicId:'core',relevance:88,reason:'Supports a presentation workflow.',suggestion:'Link the creation tool.',relatedPageIds:['p0']};assert.equal(verifiedDraft(r,d).relevance,88);
  assert.throws(()=>verifiedDraft(r,{...d,topicId:'invented'}));assert.throws(()=>verifiedDraft(r,{...d,relatedPageIds:['invented']}));
});
test('CLI renders from another working directory without npm or the source repository',()=>tempTest(async dir=>{
  await writeFile(path.join(dir,'corpus.json'),JSON.stringify(corpus()));await writeFile(path.join(dir,'assessment.json'),JSON.stringify(assessment()));
  const cli=path.join(path.dirname(fileURLToPath(import.meta.url)),'site-topic-relevance.mjs');
  const result=spawnSync(process.execPath,[cli,'render','--dir',dir,'--assessment',path.join(dir,'assessment.json'),'--lang','en'],{cwd:tmpdir(),encoding:'utf8',env:{PATH:process.env.PATH}});
  assert.equal(result.status,0,result.stderr);assert.ok((await readFile(path.join(dir,'report.html'),'utf8')).includes('report-data'));
}));
