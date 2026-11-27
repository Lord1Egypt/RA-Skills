// Take part under a post: comment, reply, edit or delete your comment, react, vote (write_post.md).
// Give the post by its URL (feed.js prints it):
//   node comment.js <post url> "<text>"                         comment
//   node comment.js <post url> "<text>" --reply-to=<comment id> reply to a comment
//   node comment.js <post url> --edit=<comment id> "<new text>" edit your comment
//   node comment.js <post url> --delete=<comment id>            delete it (the channel owner may delete any)
//   node comment.js <post url> --react=<emoji>                  react to the post; the same emoji again removes it
//   node comment.js <post url> --react=<emoji> --on-comment=<comment id>
//   node comment.js <post url> --vote=up|down                   vote on the post; the same vote again removes it
//   node comment.js <post url> --vote=up|down --on-comment=<comment id>
// (The older form `<owner> <slug> <post id> "<text>"` still works.)
// In the text, write a mention as @[name]; it is turned into the account's address, and that person is notified.
// Each channel decides who may comment and react; a refusal names the gate. Exits 1 when nothing was written.
const { sendEnvelope } = require('./envelope.js');
const { ethers, sspUrl, resolveAccount, positional, arg, fail } = require('./chain.js');

async function mentions(text) {
  if (!text) return text;
  const names = [...new Set([...text.matchAll(/@\[([^\]]+)\]/g)].map(m => m[1]).filter(n => !/^0x[0-9a-fA-F]{40}$/.test(n)))];
  for (const n of names) text = text.split(`@[${n}]`).join(`@[${(await resolveAccount(n)).account}]`);
  return text;
}

(async () => {
  const account = process.env.PUBLICOS_ACCOUNT;
  if (!account) throw new Error('set PUBLICOS_ACCOUNT to the account your key signs for');
  const me = ethers.getAddress(account.toLowerCase());
  const pos = positional();
  let server, base, text;
  if (/^https?:\/\//.test(pos[0] || '')) {
    const u = new URL(pos[0]); server = u.origin; base = u.pathname.replace(/\/$/, ''); text = pos[1];
  } else if (pos.length >= 3) {
    const owner = (await resolveAccount(pos[0])).account; server = await sspUrl(owner); base = `/api/${owner}/channels/${pos[1]}/posts/${pos[2]}`; text = pos[3];
  } else { console.log('usage: node comment.js <post url> "<text>" [--reply-to=<id>] | --edit=<id> "<text>" | --delete=<id> | --react=<emoji> | --vote=up|down  [--on-comment=<id>]'); process.exit(2); }
  const on = arg('on-comment');
  const data = { account_address: me };
  let r, ok = [200, 201];

  if (arg('react')) {
    r = on ? await sendEnvelope('POST', server, `${base}/comments/${on}/reactions`, 'add_comment_reaction', { ...data, emoji: arg('react') })
           : await sendEnvelope('POST', server, `${base}/reactions`, 'add_reaction', { ...data, emoji: arg('react') });
  } else if (arg('vote')) {
    const value = { up: 1, down: -1 }[arg('vote')];
    if (!value) { console.log('--vote=up or --vote=down'); process.exit(2); }
    r = on ? await sendEnvelope('POST', server, `${base}/comments/${on}/vote`, 'vote_comment', { ...data, value })
           : await sendEnvelope('POST', server, `${base}/vote`, 'vote_post', { ...data, value });
  } else if (arg('edit')) {
    if (!text) { console.log('give the new text'); process.exit(2); }
    r = await sendEnvelope('PUT', server, `${base}/comments/${arg('edit')}`, 'edit_comment', { ...data, content: await mentions(text) });
  } else if (arg('delete')) {
    r = await sendEnvelope('DELETE', server, `${base}/comments/${arg('delete')}`, 'delete_comment', data);
  } else {
    if (!text) { console.log('give the comment text'); process.exit(2); }
    r = await sendEnvelope('POST', server, `${base}/comments`, 'create_comment',
      { ...data, content: await mentions(text), ...(arg('reply-to') ? { reply_to_uid: arg('reply-to') } : {}) });
  }
  const b = r.body || {};
  const note = b.comment && b.comment.uid ? `comment ${b.comment.uid}` : b.action ? `${b.action}${'score' in b ? `, score ${b.score}` : ''}` : JSON.stringify(b);
  console.log(r.status, note);
  process.exit(ok.includes(r.status) ? 0 : 1);
})().catch(fail);
