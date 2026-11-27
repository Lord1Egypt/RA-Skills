# Send OX

*The reads this recipe uses (both MainSafes, the token's `decimals()`) and the simulation of the outer call (it returned true) were checked against the live network on 2026-11-11. The payment itself was not re-run on the production chain.*

**Run it:** `node scripts/send_ox.js <payee account> <amount>` ([scripts/](scripts/README.md)); it finds both Safes, simulates, sends through your BSP and exits non-zero unless the Transfer event is there.

**Money never sits in an account or a key.** Each account's OX is in its **MainSafe**, a Safe wallet created with the account. To pay, your session key asks the `SAFE_AUTH` module to make the payer's MainSafe call the token. The payee is **also a MainSafe**: never send OX to an account address or to a key.

## The recipe

1. **Both Safes**, from `SAFE_MANAGER.getMainSafeAddress(account)`: the payer's (your account) and the payee's.
2. **The inner call**: `PUBLICOS_TOKEN.transfer(payeeSafe, amount)`. OX has 18 decimals; read `decimals()` rather than assuming.
3. **The outer call**, sent by your session key to `SAFE_AUTH`:

```text
executeSafeTransaction(address safe, address to, uint256 value, bytes data, uint8 operation)
  safe      = your MainSafe
  to        = PUBLICOS_TOKEN
  value     = 0            (OX is a token, not the chain's native coin)
  data      = transfer(payeeSafe, amount)
  operation = 0            (Call; DelegateCall is refused)
```

```js
// ethers v6
const ox = new ethers.Interface(['function transfer(address,uint256)']);
const sa = new ethers.Interface(['function executeSafeTransaction(address,address,uint256,bytes,uint8) returns (bool)']);
const data = sa.encodeFunctionData('executeSafeTransaction',
  [mySafe, OX, 0, ox.encodeFunctionData('transfer', [payeeSafe, ethers.parseUnits('5', 18)]), 0]);
await pub.call({ from: key.address, to: SAFE_AUTH, data });          // simulate: returns true, or reverts if the payment would fail
const tx = await keyOnMyBsp.sendTransaction({ to: SAFE_AUTH, data, type: 0, gasPrice: 0n, gasLimit: 1_500_000n });
const receipt = await tx.wait();
```

4. **Check the receipt for a `Transfer` event** from the token, from your Safe to theirs. A failure *inside* the Safe call (not enough OX, a frozen token) reverts the whole transaction with `SafeAuth: Safe execution failed`, and the simulation reverts the same way, so simulating first tells you before you send. The `Transfer` event is still the proof to keep: it says what moved, from which Safe, to which.

## What can stop a payment

| Gate | What you see |
|---|---|
| your key isn't a registered session of the paying account | the network refuses the transaction (`publicos_whyTxRejected` code 1) |
| the paying account's domain has lapsed | refused before it runs (code 2); renew the domain first |
| not enough OX in your MainSafe | reverts: `SafeAuth: Safe execution failed` (the simulation too) |
| `operation` 1 (DelegateCall) | reverts |

## Before you pay for someone

A payment is final. When you act for a person, show them the amount, the payee's name and their Safe address, and wait for a yes every time.
