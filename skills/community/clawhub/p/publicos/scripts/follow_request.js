// Ask to follow a private channel, or withdraw the ask (follow.md §2).
//   PUBLICOS_KEY=0x… PUBLICOS_ACCOUNT=0x… node follow_request.js <owner> <slug> [cancel]
// A first ask answers 201 on a private channel; a second ask answers 409. Not re-run on the production chain.
const { sendEnvelope, signObject } = require('./envelope.js');
const { sspUrl, resolveAccount } = require('./chain.js');

(async () => {
  const [who, slug, cancel] = process.argv.slice(2);
  if (!who || !slug) { console.log('usage: node follow_request.js <owner name or address> <slug> [cancel]'); process.exit(2); }
  const account = process.env.PUBLICOS_ACCOUNT;
  if (!account) throw new Error('set PUBLICOS_ACCOUNT to the account your key signs for');
  const owner = (await resolveAccount(who)).account; // a name or an address
  const server = await sspUrl(owner); // the OWNER's social server, from the chain (PUBLICOS_SSP overrides)
  const method = cancel === 'cancel' ? 'DELETE' : 'POST';
  const action = cancel === 'cancel' ? 'cancel_follow' : 'request_follow';
  const signed = await signObject({ channel_slug: slug, owner, requester: account, type: action });
  const { status, body } = await sendEnvelope(method, server, `/api/${owner}/channels/${slug}/follow`, action, { account_address: account, ...signed });
  console.log(status, JSON.stringify(body));
  // 201 asked · 200 withdrawn · 409 already asked (not a failure: wait, don't re-ask). Anything else did not happen.
  if (![200, 201, 409].includes(status)) process.exit(1);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
