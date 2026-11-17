/**
 * Veritier Zero-Quota Integration Test
 * =====================================
 * Extract, verify, validate, attest, informational credentials, reconstruct,
 * JWKS, and revoke. Uses a vt_test_ key so monthly quota is not consumed.
 *
 *   node test_integration.mjs
 *
 * See https://veritier.ai/docs#testing
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_TEST_KEY || process.env.VERITIER_API_KEY || "";
const API_URL = process.env.API_URL || "https://api.veritier.ai";

if (!API_KEY) {
  console.error("Error: VERITIER_TEST_KEY (or VERITIER_API_KEY) is not set.");
  process.exit(1);
}

if (!API_KEY.startsWith("vt_test_")) {
  console.warn("Warning: expected a vt_test_... key. A production key consumes quota.");
}

const HEADERS = {
  Authorization: `Bearer ${API_KEY}`,
  "Content-Type": "application/json",
};

const SAMPLE_TEXT =
  "Python was created by Guido van Rossum. " +
  "The language was first released in 1991. " +
  "Python is named after the British comedy group Monty Python.";

const failures = [];
const TOTAL = 10;

function check(condition, label, detail = "") {
  if (condition) {
    console.log(`  OK ${label}`);
  } else {
    console.log(`  FAIL ${label}` + (detail ? ` - ${detail}` : ""));
    failures.push(label);
  }
}

function runTest(step, name) {
  console.log(`\n[${step}/${TOTAL}] ${name}`);
}

async function fetchWithTimeout(resource, options = {}) {
  const { timeout = 30000, ...rest } = options;
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  try {
    return await fetch(resource, { ...rest, signal: controller.signal });
  } finally {
    clearTimeout(id);
  }
}

async function runAllTests() {
  console.log("========================================");
  console.log("  Veritier Zero-Quota Integration Test");
  console.log("========================================\n");
  console.log(`  API URL: ${API_URL}`);
  console.log(`  Key:     ${API_KEY.slice(0, 12)}... (length: ${API_KEY.length})\n`);

  runTest(1, "API connectivity check");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/health`, { timeout: 10000 });
    check([200, 404].includes(resp.status), "Server reachable", `status=${resp.status}`);
  } catch (err) {
    check(false, "Server reachable", err.message);
  }

  runTest(2, "Extract: mock_claims=3");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/extract`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_claims: 3 }),
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      check((data.claims || []).length === 3, "3 mock claims returned");
      check(data.is_test === true, "is_test=true");
    }
  } catch (err) {
    check(false, "Extract request succeeded", err.message);
  }

  runTest(3, "Extract: mock_claims=0");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/extract`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_claims: 0 }),
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      check(Array.isArray(data.claims) && data.claims.length === 0, "claims=[]");
    }
  } catch (err) {
    check(false, "Extract empty-state request succeeded", err.message);
  }

  runTest(4, "Verify: mock_verdict=true");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/verify`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_verdict: true }),
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      const results = data.results || [];
      check(results.length === 3, "3 ClaimResult objects");
      check(results.every((r) => r.verdict === true), "All verdicts true");
      check(!data.credential, "no credential without action_id");
    }
  } catch (err) {
    check(false, "Verify happy-path request succeeded", err.message);
  }

  runTest(5, "Verify: mock_verdict=false");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/verify`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_verdict: false }),
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      check((data.results || []).every((r) => r.verdict === false), "All verdicts false");
    }
  } catch (err) {
    check(false, "Verify error-path request succeeded", err.message);
  }

  runTest(6, "Validate: mock_validation=true");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/validate`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({
        extracted_text: "Certificate of completion issued to Jane Doe.",
        mock_validation: true,
      }),
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      const result = data.result || {};
      check(result.verdict === "authentic", "result.verdict=authentic", text.slice(0, 120));
      check(data.is_test === true, "is_test=true");
    }
  } catch (err) {
    check(false, "Validate request succeeded", err.message);
  }

  runTest(7, "Verify action_id mints informational credential");
  let informId = null;
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/verify`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({
        text: SAMPLE_TEXT,
        mock_verdict: true,
        action_id: "onboard_inform",
      }),
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      informId = (data.credential || {}).id;
      check(String(informId || "").startsWith("crc_"), "credential.id starts with crc_");
    }
  } catch (err) {
    check(false, "Verify action_id request succeeded", err.message);
  }

  runTest(8, "Attest: mock_decision=allow");
  let credId = null;
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/attest_action`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({
        action_id: "onboard_attest",
        text: "npm install lodash",
        procedure: "package_exists",
        mock_decision: "allow",
      }),
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      check(data.decision === "allow", "decision=allow");
      credId = (data.credential || {}).id;
      check(String(credId || "").startsWith("crc_"), "credential.id starts with crc_");
    }
  } catch (err) {
    check(false, "Attest request succeeded", err.message);
  }

  runTest(9, "Public reconstruct + JWKS");
  try {
    const jwk = await fetchWithTimeout(`${API_URL}/v1/credentials/.well-known/jwk`, {
      timeout: 15000,
    });
    const jwkBody = await jwk.json();
    check(jwk.ok && (jwkBody.keys || []).length > 0, "JWKS returns keys");
    const target = credId || informId;
    if (target) {
      const pub = await fetchWithTimeout(`${API_URL}/v1/credentials/${target}`, {
        timeout: 15000,
      });
      const body = await pub.json();
      check(
        pub.ok && body.id === target && body.signature_valid === true,
        "GET /v1/credentials/:id no auth"
      );
    } else {
      check(false, "GET /v1/credentials/:id no auth", "no credential id");
    }
  } catch (err) {
    check(false, "Reconstruct/JWKS succeeded", err.message);
  }

  runTest(10, "Issuer revoke");
  try {
    const target = informId || credId;
    if (!target) {
      check(false, "revoke target", "no credential id");
    } else {
      const revoked = await fetchWithTimeout(`${API_URL}/v1/credentials/${target}/revoke`, {
        method: "POST",
        headers: HEADERS,
        timeout: 15000,
      });
      const revokedBody = await revoked.json();
      check(revoked.ok && revokedBody.revoked === true, "POST /v1/credentials/:id/revoke");
      const pub = await fetchWithTimeout(`${API_URL}/v1/credentials/${target}`, {
        timeout: 15000,
      });
      const body = await pub.json();
      check(pub.ok && body.revoked === true, "public GET still 200 with revoked=true");
    }
  } catch (err) {
    check(false, "Revoke succeeded", err.message);
  }

  console.log();
  if (failures.length === 0) {
    console.log("All integration checks passed.");
    console.log("  Zero quota was consumed. Switch to a production key for live fact-checking.");
    process.exit(0);
  }
  console.log(`${failures.length} check(s) failed:`);
  failures.forEach((f) => console.log(`  - ${f}`));
  process.exit(1);
}

runAllTests();
