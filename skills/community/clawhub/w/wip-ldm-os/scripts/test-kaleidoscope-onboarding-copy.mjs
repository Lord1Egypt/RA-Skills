import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const demo = readFileSync("src/hosted-mcp/demo/index.html", "utf8");
const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");

function functionBody(source, name) {
  const start = source.indexOf("async function " + name + "(");
  assert.notEqual(start, -1, "missing function " + name);
  const open = source.indexOf("{", start);
  let depth = 0;
  for (let i = open; i < source.length; i++) {
    if (source[i] === "{") depth += 1;
    if (source[i] === "}") depth -= 1;
    if (depth === 0) return source.slice(open + 1, i);
  }
  throw new Error("unterminated function " + name);
}

function functionSource(source, name) {
  const start = source.indexOf("function " + name + "(");
  assert.notEqual(start, -1, "missing function " + name);
  const open = source.indexOf("{", start);
  let depth = 0;
  for (let i = open; i < source.length; i++) {
    if (source[i] === "{") depth += 1;
    if (source[i] === "}") depth -= 1;
    if (depth === 0) return source.slice(start, i + 1);
  }
  throw new Error("unterminated function " + name);
}

const noThanks = functionBody(demo, "showNoThanksFlow");
const returningNoThanks = functionBody(demo, "showReturningUserNoThanksFlow");
const startDemo = functionBody(demo, "startDemo");
const authFlow = functionBody(demo, "doFaceIDAuth");
const imageFlow = functionBody(demo, "generateKaleidoscope");
const oldOutro = functionBody(demo, "showOutro");
const approvedOutro = functionBody(demo, "showApprovedOutro");
const returningOutro = functionBody(demo, "showReturningUserOutro");

assert.match(startDemo, /Hi, I'm L\\u0113sa\. Welcome to Kaleidoscope\./);
assert.match(startDemo, /You just created an account with a passkey\. The passkey lives on your phone\./);
assert.match(startDemo, /Going forward, you can use your phone to log into any Work in Progress Computer service\./);
assert.match(startDemo, /Anytime I need your permission to do something, I'll ask, and you authorize with your fingerprint or face\. No passwords\. Ever\./);
assert.match(startDemo, /Hi, " \+ currentAccountLabel\(\) \+ "\. Welcome back to Kaleidoscope\./);
assert.match(startDemo, /Do you want to try giving me permission with your device to create something that costs money\?/);
assert.doesNotMatch(startDemo, /getWalletSummary\(\)/);
assert.doesNotMatch(startDemo, /Your balance is " \+ wallet\.balance/);
assert.doesNotMatch(startDemo, /Your account is a key on your device, not an email\./);
assert.doesNotMatch(startDemo, /You just logged in with your passkey/);
assert.doesNotMatch(startDemo, /And I can use it too/);

assert.match(demo, /I have a wallet with " \+ wallet\.balance \+ "\. Do I have your permission to spend " \+ wallet\.cost/);
assert.match(demo, /addMessage\('Authorizing', 'user'\)/);
assert.doesNotMatch(demo, /addMessage\('Authorized', 'user'\)/);
assert.doesNotMatch(demo, /This is the end of the demo\. Tap the icon to start over\./);
assert.doesNotMatch(demo, /open wip\.computer\/demo/);

assert.match(noThanks, /No problem\. Let me show you something beautiful\./);
assert.match(noThanks, /IS_RETURNING_USER_FLOW/);
assert.match(noThanks, /showReturningUserNoThanksFlow\(\)/);
assert.match(noThanks, /generateKaleidoscope\(false, \{ showWalletReceipt: false, showOutro: false \}\)/);
assert.match(noThanks, /showApprovedOutro\(\)/);
assert.doesNotMatch(noThanks, /\/demo\/api\/imagine/);
assert.doesNotMatch(noThanks, /fallback\.jpg/);
assert.doesNotMatch(noThanks, /Cost:/);
assert.doesNotMatch(noThanks, /Balance:/);

assert.match(returningNoThanks, /No problem\. You can come back anytime\./);
assert.match(returningNoThanks, /At Work in Progress Computer, we are building the future of AI and human interaction\./);
assert.match(returningNoThanks, /https:\/\/x\.com\/wipcomputer/);
assert.match(returningNoThanks, /Made in California by WIP Computer, Inc\. Learning Dreaming Machines\./);
assert.doesNotMatch(returningNoThanks, /generateKaleidoscope/);
assert.doesNotMatch(returningNoThanks, /\/demo\/api\/imagine/);
assert.doesNotMatch(returningNoThanks, /Cost:/);
assert.doesNotMatch(returningNoThanks, /Balance:/);
assert.doesNotMatch(returningNoThanks, /passkey/i);

assert.match(imageFlow, /var showWalletReceipt = options\.showWalletReceipt !== false;/);
assert.match(imageFlow, /if \(showWalletReceipt\) \{/);
assert.match(imageFlow, /body: JSON\.stringify\(\{ prompt: prompt \}\)/);
assert.doesNotMatch(imageFlow, /mode:/);
assert.doesNotMatch(server, /no_thanks/i);
assert.doesNotMatch(server, /Free onboarding generation/);

assert.match(oldOutro, /IS_RETURNING_USER_FLOW/);
assert.match(oldOutro, /showReturningUserOutro\(\)/);
assert.match(oldOutro, /showApprovedOutro\(\)/);
assert.match(approvedOutro, /At Work in Progress Computer, we are building the future of AI and human interaction\./);
assert.match(approvedOutro, /https:\/\/wip\.computer\/demo/);
assert.match(approvedOutro, /https:\/\/x\.com\/wipcomputer/);
assert.match(approvedOutro, /Your passkey will keep working after you leave\./);
assert.doesNotMatch(approvedOutro, /Your account stays active/);
assert.doesNotMatch(approvedOutro, /When you come back/);

assert.match(returningOutro, /At Work in Progress Computer, we are building the future of AI and human interaction\./);
assert.match(returningOutro, /We believe permission is a conversation\. Your AI asks\. You decide\. One glance, one tap\./);
assert.match(returningOutro, /https:\/\/x\.com\/wipcomputer/);
assert.match(returningOutro, /Made in California by WIP Computer, Inc\. Learning Dreaming Machines\./);
assert.doesNotMatch(returningOutro, /https:\/\/wip\.computer\/demo/);
assert.doesNotMatch(returningOutro, /log out/);
assert.doesNotMatch(returningOutro, /Your passkey will keep working after you leave\./);
assert.doesNotMatch(returningOutro, /Your account stays active/);
assert.doesNotMatch(returningOutro, /When you come back/);

assert.match(authFlow, /That passkey belongs to a different account/);
assert.match(authFlow, /isSameAccountAuthorization\(result, activeToken, activeTenant\)/);
assert.doesNotMatch(authFlow, /result\.tenantId !== activeTenant/);

const { canonicalAccountId, isSameAccountAuthorization } = Function(
  functionSource(demo, "canonicalAccountId") + "\n"
  + functionSource(demo, "isSameAccountAuthorization") + "\n"
  + "return { canonicalAccountId, isSameAccountAuthorization };"
)();

assert.equal(canonicalAccountId("acct:parker-smoke-test"), "parker-smoke-test");
assert.equal(canonicalAccountId("parker-smoke-test"), "parker-smoke-test");
assert.equal(canonicalAccountId(" key:abc "), "key:abc");
assert.equal(canonicalAccountId(""), null);
assert.equal(canonicalAccountId(null), null);

assert.equal(
  isSameAccountAuthorization({ tenantId: "parker-smoke-test", apiKey: "different-token" }, "active-token", "acct:parker-smoke-test"),
  true,
);
assert.equal(
  isSameAccountAuthorization({ tenantId: "acct:parker-smoke-test", apiKey: "different-token" }, "active-token", "parker-smoke-test"),
  true,
);
assert.equal(
  isSameAccountAuthorization({ tenantId: "acct:other-account", apiKey: "active-token" }, "active-token", "acct:parker-smoke-test"),
  false,
);
assert.equal(
  isSameAccountAuthorization({ apiKey: "active-token" }, "active-token", null),
  true,
);
assert.equal(
  isSameAccountAuthorization({ apiKey: "other-token" }, "active-token", null),
  false,
);

assert.match(demo, /id="kscopeIcon" type="button" onclick="logoutAndSignBackIn\(\)"/);
assert.match(demo, /sessionStorage\.removeItem\('lesa-token'\)/);
assert.match(demo, /window\.location\.href = '\/login\?next=\/demo'/);

assert.match(server, /const IMAGE_COST_CENTS = 1;/);
assert.match(server, /const INITIAL_BALANCE_CENTS = 1000;/);
assert.match(server, /const DEMO_WALLET_RESET_MARKER_FILE = join/);
assert.match(server, /\.demo-wallet-reset-v0-4-87\.json/);
assert.match(server, /function walletUserIdForAgent\(agentId\)/);
assert.match(server, /agentId\.startsWith\("acct:"\) \? agentId\.slice\("acct:"\.length\) : agentId/);
assert.match(server, /function resetAndNormalizeWalletFileEntries\(wallets\)/);
assert.match(server, /normalizedWallets\[walletUserIdForAgent\(agentId\)\] = INITIAL_BALANCE_CENTS/);
assert.match(server, /async function resetExistingDemoWalletsToStarterBalanceOnce\(\)/);
assert.match(server, /await prisma\.wallet\.updateMany\(\{ data: \{ balance: INITIAL_BALANCE_CENTS \} \}\)/);
assert.match(server, /saveWalletsToFile\(normalizedWalletFile\.wallets\)/);
assert.match(server, /prismaCount: prismaResetCount/);
assert.match(server, /jsonCount: jsonResetCount/);
assert.match(server, /const walletUserId = walletUserIdForAgent\(agentId\);/);
assert.match(server, /where: \{ userId: walletUserId \}/);
assert.match(server, /data: \{ userId: walletUserId, balance: INITIAL_BALANCE_CENTS \}/);
assert.match(server, /return w\[walletUserId\] !== undefined \? w\[walletUserId\] : INITIAL_BALANCE_CENTS/);
assert.match(server, /if \(w\[walletUserId\] === undefined\) w\[walletUserId\] = INITIAL_BALANCE_CENTS/);
assert.match(server, /w\[walletUserId\] = Math\.max\(0, w\[walletUserId\] - cents\)/);
assert.match(server, /return w\[walletUserId\]/);
assert.match(server, /await resetExistingDemoWalletsToStarterBalanceOnce\(\);/);

console.log("Kaleidoscope onboarding copy checks passed");
