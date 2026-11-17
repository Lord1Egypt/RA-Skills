import { readFileSync } from "node:fs";

const loginFiles = [
  "src/hosted-mcp/app/kaleidoscope-login.html",
  "src/hosted-mcp/demo/login.html",
];

function assertContains(source, needle, label) {
  if (!source.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assertBefore(source, first, second, label) {
  const firstIndex = source.indexOf(first);
  const secondIndex = source.indexOf(second);
  if (firstIndex === -1 || secondIndex === -1 || firstIndex >= secondIndex) {
    throw new Error(`${label} expected "${first}" before "${second}"`);
  }
}

function extractFunction(source, name) {
  const start = source.indexOf(`function ${name}(`);
  if (start === -1) throw new Error(`could not find function ${name}`);
  const bodyStart = source.indexOf("{", start);
  let depth = 0;
  for (let i = bodyStart; i < source.length; i += 1) {
    if (source[i] === "{") depth += 1;
    if (source[i] === "}") depth -= 1;
    if (depth === 0) return source.slice(start, i + 1);
  }
  throw new Error(`could not extract function ${name}`);
}

function assertNotContains(source, needle, label) {
  if (source.includes(needle)) {
    throw new Error(`${label} must not contain: ${needle}`);
  }
}

for (const file of loginFiles) {
  const html = readFileSync(file, "utf8");
  const followFunction = extractFunction(html, "followPairNextIfPresent");
  const backFunction = extractFunction(html, "backToLoginAfterQrScan");

  assertContains(html, 'id="qr-auth-confirm-view"', `${file} confirmation view`);
  assertContains(html, "Your authenticated Kaleidoscope session is available on your other device.", `${file} confirmation headline`);
  assertContains(html, "Back to login", `${file} back button copy`);
  assertNotContains(html, "Open session here", `${file} authenticator completion must not offer local demo open`);
  assertNotContains(html, ">Close</button>", `${file} authenticator completion must not show close action`);
  assertNotContains(html, "Kaleidoscope is ready there.", `${file} removed ready helper copy`);
  assertNotContains(html, "Open Kaleidoscope here", `${file} removed duplicated open copy`);
  assertNotContains(html, "Keep using Kaleidoscope on the other device.", `${file} removed cancel helper copy`);
  assertNotContains(html, "Scan QR Code", `${file} login-page scanner action must be absent`);
  assertNotContains(html, "BarcodeDetector", `${file} login-page scanner detector must be absent`);
  assertNotContains(html, "getUserMedia", `${file} login-page scanner camera code must be absent`);
  assertContains(html, "You can close this page.", `${file} close fallback copy`);

  assertContains(html, "function showQrAuthenticatorConfirmation(identity, isNewAccount)", `${file} confirmation function`);
  assertContains(html, "function backToLoginAfterQrScan()", `${file} back-to-login function`);

  assertContains(
    html,
    "if (DEMO_NEXT_REGEX.test(approveResponse.next)) {\n      return showQrAuthenticatorConfirmation(identity, isNewAccount === true);\n    }",
    `${file} QR authenticator demo next shows confirmation`,
  );
  assertBefore(
    html,
    "return showQrAuthenticatorConfirmation(identity, isNewAccount === true);",
    "next = approveResponse.next;",
    `${file} confirmation intercepts approve next before redirect`,
  );
  assertNotContains(followFunction, "location.replace('/demo');", `${file} QR approve path must not directly enter demo`);
  assertNotContains(followFunction, 'location.href = "/demo";', `${file} QR approve path must not assign demo href`);
  assertNotContains(followFunction, "storeDemoHandoffIfNeeded('/demo'", `${file} QR approve path must not store demo handoff`);

  assertContains(backFunction, "location.replace('/login?next=/demo');", `${file} back returns to login`);
  assertNotContains(backFunction, "storeDemoHandoffIfNeeded", `${file} back must not store demo handoff`);
  assertNotContains(backFunction, "location.replace('/demo')", `${file} back must not open demo`);

  assertContains(html, "if (await followPairNextIfPresent(approveResponse, result, true)) return;", `${file} create caller stops after confirmation`);
  assertContains(html, "if (await followPairNextIfPresent(approveResponse, result, false)) return;", `${file} sign-in caller stops after confirmation`);
  assertContains(html, "storeDemoHandoffIfNeeded(data.next, data, qrLoginMode === 'register');", `${file} requester QR status still stores handoff`);
  assertContains(html, "location.replace(data.next);", `${file} requester QR status still redirects`);
  assertContains(html, "storeDemoHandoffIfNeeded('/demo', result, true);", `${file} same-device create still stores demo handoff`);
  assertContains(html, "storeDemoHandoffIfNeeded('/demo', result, false);", `${file} same-device sign-in still stores demo handoff`);
}

console.log("kaleidoscope QR authenticator confirmation checks passed");
