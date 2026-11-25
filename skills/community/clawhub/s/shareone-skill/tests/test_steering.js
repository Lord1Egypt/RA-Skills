const {test} = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const https = require('node:https');
const {EventEmitter} = require('node:events');
const fs = require('node:fs');
const path = require('node:path');
const {fixture, json, error} = require('./http_fixture');
const {requestBuffer} = require('../scripts/shareone_client');

const SOURCE = 'https://gitlab.com/team/review/-/raw/' + 'a'.repeat(40) + '/dist/review.html';

test('share links cannot override deployment configuration or send a key to another origin', async t => {
    const intended = await fixture(t, (_, res) => json(res, {ok:true}));
    const foreign = await fixture(t, (_, res) => json(res, {ok:true}));
    for (const [script, args] of [['update_share_settings', ['--watermark','review']], ['manage_collaborators', ['--action','list']]]) {
        for (const ref of [foreign.base + '/s/review', 'https://untrusted.shareone.vip/s/review', 'http://shareone.vip/s/review']) {
            const result = await intended.run(script, [ref,...args]);
            assert.equal(result.status, 2, result.stderr);
            assert.equal(error(result).error_code, 'UNTRUSTED_SHARE_ORIGIN');
            assert.match(error(result).hint, /SHAREONE_BASE_URL/);
        }
        for (const ref of [intended.base + '/s/review', 'https://s.shareone.vip/s/review', 'https://shareone.app/md/review']) {
            const result = await intended.run(script, [ref,...args]);
            assert.equal(result.status, 0, result.stderr);
            assert.equal(intended.requests.at(-1).headers['x-api-key'], 'isolated-owner-key');
        }
        const result = await intended.run(script, [foreign.base + '/s/review',...args,'--base-url',foreign.base]);
        assert.equal(result.status, 0, result.stderr);
    }
    assert.equal(foreign.requests.length, 2, 'Only explicitly configured deployment calls may reach the foreign origin');
});

test('settings preserve omitted fields and empty clears, while dry-run needs no credentials or proxy calls', async t => {
    const f = await fixture(t, (_, res) => json(res, {settings:{watermark:null}}));
    const result = await f.run('update_share_settings', ['https://shareone.vip/s/review','--watermark','','--allow-comments','false']);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(f.requests[0].path, '/api/v1/pages/review');
    assert.deepEqual(JSON.parse(f.requests[0].body), {watermark:'',allow_comments:false});
    const before = f.requests.length;
    const dry = await f.run('update_share_settings', ['review','--watermark','','--dry-run'], {
        SHAREONE_API_KEY:'',SUDOWORK_AUTH_PROXY_URL:f.base+'/proxy',SUDOWORK_AUTH_PROXY_TOKEN:'synthetic-proxy-token',
    });
    assert.equal(dry.status,0,dry.stderr);
    assert.equal(JSON.parse(dry.stdout).base_url,f.base);
    assert.equal(f.requests.length,before);
});

test('redirects reject HTTPS downgrades and strip all credential headers when the origin changes', async t => {
    for (const name of Object.keys(process.env)) if (/^(http|https|all)_proxy$/i.test(name)) {
        const value=process.env[name];delete process.env[name];t.after(()=>{process.env[name]=value;});
    }
    const calls=[];
    let redirect='http://fixture.invalid/final';
    const fake=(url,options,callback)=>{
        calls.push({url:String(url),headers:options.headers});
        const req=new EventEmitter();req.write=()=>{};
        req.end=()=>queueMicrotask(()=>{
            const res=new EventEmitter();res.statusCode=String(url).endsWith('/start')?302:204;
            res.headers=res.statusCode===302?{location:redirect}:{};res.resume=()=>{};
            callback(res);if(res.statusCode!==302)res.emit('end');
        });return req;
    };
    t.mock.method(http,'request',fake);t.mock.method(https,'request',fake);
    const options={headers:{'X-API-Key':'synthetic-key',Authorization:'synthetic-bearer',Cookie:'synthetic-cookie'}};
    await assert.rejects(requestBuffer('https://fixture.invalid/start',options),{code:'UNSAFE_REDIRECT'});
    assert.equal(calls.length,1,'No plaintext request may be sent');
    redirect='https://fixture.invalid/final';calls.length=0;
    await requestBuffer('https://fixture.invalid/start',options);
    assert.equal(calls.at(-1).headers['X-API-Key'],'synthetic-key');
    redirect='https://other.invalid/final';calls.length=0;
    await requestBuffer('https://fixture.invalid/start',options);
    assert.deepEqual(calls.at(-1).headers,{});
    calls.length=0;
    await assert.rejects(requestBuffer('https://fixture.invalid/start',{...options,method:'POST'},'private-content'),{code:'UNSAFE_REDIRECT'});
    assert.equal(calls.length,1,'A private body cannot be forwarded to another origin');
    redirect='https://fixture.invalid/final';calls.length=0;
    await requestBuffer('http://fixture.invalid/start',options);
    assert.deepEqual(calls.at(-1).headers,{},'An HTTPS upgrade is still a different origin');
});

test('Sudowork preserves server domain errors before considering proxy missing-secret messages', async t => {
    let body={error_code:'REMOTE_SOURCE_UNAVAILABLE',detail:'Registered GitLab read credential is unavailable',
        hint:'Restore the repository credential; preserve this ShareOne identity.',retryable:true};
    const f=await fixture(t,(req,res)=>{
        if(req.path.startsWith('/secrets'))json(res,{data:[{namespace:'service:shareone',key:'X-API-Key'}]});
        else json(res,body,502);
    });
    const proxy={SUDOWORK_AUTH_PROXY_URL:f.base+'/proxy',SUDOWORK_AUTH_PROXY_BASE_URL:f.base,SUDOWORK_AUTH_PROXY_TOKEN:'synthetic-proxy-token'};
    const result=await f.run('shareone_api_request',['/api/v1/pages','--method','POST','--data','{}','--idempotency-key','source-intent'],proxy);
    assert.equal(result.status,9,result.stderr);
    assert.equal(error(result).error_code,'REMOTE_SOURCE_UNAVAILABLE');
    assert.equal(error(result).hint,body.hint);
    assert.equal(error(result).retryable,true);
    assert.doesNotMatch(result.stderr,/create_guest|SUDOWORK_ENV_OK_KEY_NOT_FOUND/);
    body={detail:'Secret X-API-Key not found'};
    const missing=await f.run('shareone_api_request',['/api/v1/me'],proxy);
    assert.equal(missing.status,7);
    assert.equal(error(missing).error_code,'SUDOWORK_ENV_OK_KEY_NOT_FOUND');
});

test('invalid publication responses remain unconfirmed with operation-specific replay safety and no history write', async t => {
    let response='';
    const f=await fixture(t,(_,res)=>{res.writeHead(201,{'Content-Type':'application/json'});res.end(response);});
    const file=path.join(f.dir,'review.html');fs.writeFileSync(file,'<p>Review</p>');
    for(const value of ['', '<html>proxy error</html>', 'null', '{}', '[]', '{"share_id":"missing-url"}']) {
        response=value;
        for(const key of [null,'same-intent']) {
            const before=f.requests.length;
            const result=await f.run('upload_page',[file,...(key?['--idempotency-key',key]:[])]);
            assert.equal(result.status,9,result.stderr);
            assert.equal(error(result).error_code,'INVALID_RESPONSE');
            assert.equal(error(result).retryable,Boolean(key));
            assert.match(error(result).hint,/same intent key/);
            assert.equal(f.requests.length,before+1,'The helper must not replay an ambiguous creation');
            assert.equal(fs.existsSync(path.join(f.dir,'.shareone_history.json')),false);
        }
    }
    response='{"share_id":"review","share_url":"https://shareone.vip/s/review"}';
    const result=await f.run('upload_page',[file,'--idempotency-key','same-intent']);
    assert.equal(result.status,0,result.stderr);
    assert.equal(JSON.parse(result.stdout).share_id,'review');
    assert.equal(JSON.parse(fs.readFileSync(path.join(f.dir,'.shareone_history.json'),'utf8'))[file].idempotency_key,'same-intent');
});

test('a pending review remains an explicit pending record without a fabricated share or publication history', async t => {
    const pending={status:'automatic_pending',review_id:'review-id',filename:'review.html',estimated_seconds:10};
    const f=await fixture(t,(_,res)=>json(res,pending,202));
    const file=path.join(f.dir,'review.html');fs.writeFileSync(file,'<p>Review</p>');
    const result=await f.run('upload_page',[file,'--allow-data','true']);
    assert.equal(result.status,0,result.stderr);
    assert.deepEqual(JSON.parse(result.stdout),pending);
    assert.doesNotMatch(result.stderr,/PAGE_DATA_ENABLED/);
    assert.equal(fs.existsSync(path.join(f.dir,'.shareone_history.json')),false);
});

test('explicit source detachment retains the local update contract and verifies submitted bytes', async t => {
    const content='<p>Owner-selected replacement</p>';
    const f=await fixture(t,(req,res)=>{
        if(req.method==='GET'){res.writeHead(200);res.end(content);}
        else json(res,{share_id:'review',share_url:'https://shareone.vip/s/review'});
    });
    const file=path.join(f.dir,'review.html');fs.writeFileSync(file,content);
    const result=await f.run('upload_page',[file,'--share-id','review','--remote-url','']);
    assert.equal(result.status,0,result.stderr);
    assert.equal(f.requests[0].method,'PUT');
    assert.deepEqual(JSON.parse(f.requests[0].body),{filename:'review.html',html_content:content,remote_url:''});
    assert.equal(f.requests[1].path,'/api/v1/shares/review/download');
    const before=f.requests.length;
    const invalid=await f.run('upload_page',[file,'--remote-url','']);
    assert.equal(invalid.status,2);
    assert.equal(f.requests.length,before);
});

test('command help and malformed arguments are handled without authentication, network calls or content reads', async t => {
    const f=await fixture(t,(_,res)=>json(res,{}));
    const proxy={SHAREONE_API_KEY:'',SUDOWORK_AUTH_PROXY_URL:f.base+'/proxy',SUDOWORK_AUTH_PROXY_TOKEN:'synthetic-proxy-token'};
    for(const script of ['shareone_api_request','upload_page','refresh_share','update_share_settings','manage_collaborators','publish']) {
        for(const help of ['--help','-h']) {
            const result=await f.run(script,[help],proxy);
            assert.equal(result.status,0,result.stderr);
            assert.match(result.stdout,/Use when:/);assert.match(result.stdout,/Returns:/);assert.match(result.stdout,/Usage:/);
        }
        const missing=await f.run(script,['--api-key','--help']);
        assert.equal(missing.status,2);
        assert.equal(error(missing).error_code,'MISSING_VALUE');
        const empty=await f.run(script,[''],proxy);
        assert.equal(empty.status,2,empty.stderr);
        assert.equal(error(empty).error_code,'BAD_ARGS');
    }
    const scope=await f.run('upload_page',['--remote-url',SOURCE,'--viewer-scope','unknown']);
    assert.equal(scope.status,2);
    const both=await f.run('upload_page',['does-not-exist.html','--remote-url',SOURCE]);
    assert.equal(both.status,2);
    assert.equal(f.requests.length,0);
});
