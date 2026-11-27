// Send OX from your account's MainSafe to another account's MainSafe (send_ox.md).
//   node send_ox.js <payee: name or account address> <amount in OX> [--dry]
// The payee is an ACCOUNT (never a Safe, never a key); the script finds both Safes. Simulates first (it returns true,
// or reverts when the payment would fail), sends through your BSP, then looks for the token's Transfer event.
const { ethers, pub, contractAddress, resolveAccount, key, account, sendTx } = require('./chain.js');

(async () => {
  const [payee, amount] = process.argv.slice(2).filter(x => !x.startsWith('--'));
  if (!payee || !amount) { console.log('usage: node send_ox.js <payee: name or account address> <amount in OX> [--dry]'); process.exit(2); }
  const to = await resolveAccount(payee);   // a name, or an account address
  const me = account();
  const safeMgr = new ethers.Contract(await contractAddress('SAFE_MANAGER'), ['function getMainSafeAddress(address) view returns (address)'], pub);
  const [mySafe, theirSafe] = await Promise.all([safeMgr.getMainSafeAddress(me), safeMgr.getMainSafeAddress(to.account)]);
  if (theirSafe === ethers.ZeroAddress) throw new Error('the payee has no MainSafe: is that an account address?');
  const OX = await contractAddress('PUBLICOS_TOKEN');
  const token = new ethers.Contract(OX, ['function decimals() view returns (uint8)', 'function balanceOf(address) view returns (uint256)'], pub);
  const decimals = await token.decimals();
  const units = ethers.parseUnits(amount, decimals);
  const balance = await token.balanceOf(mySafe);
  console.log(`${amount} OX to ${to.name} ${to.account}
  from your MainSafe ${mySafe} (balance ${ethers.formatUnits(balance, decimals)} OX) to theirs ${theirSafe}`);
  if (balance < units) throw new Error('not enough OX in your MainSafe');

  const ox = new ethers.Interface(['function transfer(address,uint256)']);
  const sa = new ethers.Interface(['function executeSafeTransaction(address,address,uint256,bytes,uint8) returns (bool)']);
  const SAFE_AUTH = await contractAddress('SAFE_AUTH');
  const data = sa.encodeFunctionData('executeSafeTransaction', [mySafe, OX, 0, ox.encodeFunctionData('transfer', [theirSafe, units]), 0]);
  if (process.env.PUBLICOS_KEY) { // with a key at hand, check that the Safe call itself would succeed (a failure inside it reverts here too)
    const sim = await pub.call({ from: key().address, to: SAFE_AUTH, data });
    if (!sa.decodeFunctionResult('executeSafeTransaction', sim)[0]) throw new Error('simulation returned false: the Safe call would fail');
  }

  const { hash, receipt, rpc } = await sendTx(SAFE_AUTH, data);
  const transferTopic = ethers.id('Transfer(address,address,uint256)');
  const moved = receipt.logs.find(l => l.address.toLowerCase() === OX.toLowerCase() && l.topics[0] === transferTopic);
  console.log(`sent via ${rpc}: ${hash} block ${receipt.blockNumber} status ${receipt.status} ${moved ? 'Transfer event present: paid' : 'NO Transfer event: nothing moved'}`);
  process.exit(moved ? 0 : 1);
})().catch(e => { console.error('ERR', e.shortMessage || e.message); process.exit(1); });
