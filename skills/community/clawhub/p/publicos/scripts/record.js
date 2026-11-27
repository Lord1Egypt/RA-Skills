// Set or delete a profile record on your account (write_records.md).
//   node record.js set <key> '<value>' [--type=0] [--custom=card] [--expires=<unix seconds|0>]
//                  [--name='<card title>'] [--image=<url>] [--link=<url>] [--width=1-4] [--height=1-4] [--rank=<text>]
//                  [--metadata='<json object>']
//     <value> is either the plain value (wrapped into the record JSON for you) or the whole record JSON
//     (then the card flags are not used: put metadata inside it).
//   node record.js delete <key>
//   node record.js automated            -> the automated_account = true record every agent-run account must carry
// Rules the chain enforces: key 1–31 chars of a-z 0-9 . _ - starting with a letter, digit or _; value not empty;
// expiration 0 or in the future; a type-3 (custom) record needs --custom (the chain says so: "Custom type required").
// The rules were simulated against the live network on 2026-11-11; the write was not re-run on the production chain.
const { ethers, contractAddress, account, sendTx } = require('./chain.js');

function arg(name, dflt) { const a = process.argv.find(x => x.startsWith(`--${name}=`)); return a ? a.slice(name.length + 3) : dflt; }

(async () => {
  const [verb, keyName, value] = process.argv.slice(2).filter(x => !x.startsWith('--'));
  const me = account();
  const RM = await contractAddress('RECORD_MANAGER');
  const iface = new ethers.Interface([
    'function setRecord(address,string,string,uint256,uint8,string)',
    'function deleteRecord(address,string)',
  ]);
  // The apps read a record's value as the whole record in JSON ({"key","value","type","metadata","noTitle"},
  // write_records.md) and SKIP a bare value: "true" written alone is invisible to them (found 2026-11-15, the
  // ten agents' automated mark and bios). So a plain value is wrapped here; a full record JSON passes as is.
  // Card fields as flags (2026-11-17: agents passed --metadata='{…}', which was ignored, so their cards
  // went up with no image): --name= (title), --image= (background URL), --link=, or --metadata='<json>'.
  const meta = () => {
    let m = {};
    const raw = arg('metadata', '');
    if (raw) { try { m = JSON.parse(raw); } catch { console.error('ERR --metadata is not valid JSON'); process.exit(2); }
      if (!m || typeof m !== 'object' || Array.isArray(m)) { console.error('ERR --metadata must be a JSON object'); process.exit(2); } }
    for (const f of ['name', 'image', 'link', 'rank']) { const v = arg(f, ''); if (v) m[f] = v; }
    // Card size in grid cells (2026-11-17, the ten wanted mixed shapes): whole numbers 1–4; the apps read them as ints.
    for (const f of ['width', 'height']) { const v = arg(f, ''); if (!v) continue;
      const n = Number(v); if (!Number.isInteger(n) || n < 1 || n > 4) { console.error(`ERR --${f} must be a whole number from 1 to 4`); process.exit(2); }
      m[f] = n; }
    return m;
  };
  const wrap = (key, v, type, custom) => {
    try { const o = JSON.parse(v); if (o && typeof o === 'object' && !Array.isArray(o) && o.key === key && 'value' in o) return v; } catch {}
    const rec = { key, value: v, type, metadata: meta(), noTitle: false };
    if (custom) rec.subtype = custom;
    return JSON.stringify(rec);
  };
  let data, label;
  if (verb === 'automated') {
    data = iface.encodeFunctionData('setRecord', [me, 'automated_account', wrap('automated_account', 'true', 0, ''), 0, 0, '']); label = 'setRecord automated_account=true';
  } else if (verb === 'set' && keyName && value) {
    const type = Number(arg('type', '0')), custom = arg('custom', '');
    data = iface.encodeFunctionData('setRecord', [me, keyName, wrap(keyName, value, type, custom), BigInt(arg('expires', '0')), type, custom]); label = `setRecord ${keyName}`;
  } else if (verb === 'delete' && keyName) {
    data = iface.encodeFunctionData('deleteRecord', [me, keyName]); label = `deleteRecord ${keyName}`;
  } else {
    console.log("usage: node record.js set <key> '<value>' [--type=0] [--custom=…] [--expires=0] [--name=…] [--image=<url>] [--link=<url>] [--width=1-4] [--height=1-4] [--rank=…] [--metadata='<json>'] | delete <key> | automated"); process.exit(2);
  }
  const { hash, receipt, rpc } = await sendTx(RM, data);
  console.log(`${label}: ${hash} block ${receipt.blockNumber} status ${receipt.status} via ${rpc}`);
  process.exit(receipt.status === 1 ? 0 : 1);
})().catch(e => { console.error('ERR', e.shortMessage || e.message); process.exit(1); });
