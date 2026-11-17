const assert = require('node:assert/strict');
const { test } = require('node:test');
const { receive } = require('../scripts/scode_receive');

// The ACP peer is external to this skill. Exercise actual stdio framing and
// process lifecycle here; the ShareOne e2e probe additionally runs real scode.
function peer(permission = false, stopReason = 'end_turn') {
    return `const readline=require('node:readline');
const send=x=>console.log(JSON.stringify(x));
readline.createInterface({input:process.stdin}).on('line',line=>{
 const m=JSON.parse(line); const response=result=>send({jsonrpc:'2.0',id:m.id,result});
 if(m.method==='initialize') response({agentCapabilities:{loadSession:true}});
 if(m.method==='session/load') {response({});send({jsonrpc:'2.0',method:'session/update',params:{sessionId:'canonical-session',update:{sessionUpdate:'available_commands_update'}}});}
 if(m.method==='session/prompt') {
  if(m.params.sessionId!=='canonical-session'||!m.params.prompt[0].text.includes('stable-event')) process.exit(9);
  ${permission ? "send({jsonrpc:'2.0',id:99,method:'session/request_permission',params:{}});" : ''}
  response({stopReason:${JSON.stringify(stopReason)}});
 }
});`;
}

test('ACP loads explicit session and delivers JSON to its canonical session ID', async () => {
    const result = await receive({ events: [{ id: 'stable-event' }] }, 'fixture-session.jsonl', { command: [process.execPath, '-e', peer()] });
    assert.equal(result.stopReason, 'end_turn');
});

test('permission requests and incomplete turns leave the batch unacknowledged', async () => {
    await assert.rejects(receive({ events: [{ id: 'stable-event' }] }, 'fixture-session.jsonl', { command: [process.execPath, '-e', peer(true)] }), /interactive permission/);
    await assert.rejects(receive({ events: [{ id: 'stable-event' }] }, 'fixture-session.jsonl', { command: [process.execPath, '-e', peer(false, 'max_tokens')] }), /did not finish/);
});
