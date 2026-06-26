/**
 * Tests for the 3.3.1 plugin config schema in openclaw.plugin.json.
 *
 * Regression guard: rc.6 rejected `publicUrl` and any `extraction.*` key
 * except `extraction.enabled` + `extraction.model` with `invalid config:
 * must NOT have additional properties`. 3.3.1 widens the surface to
 * include `publicUrl`, `extraction.interval`, `extraction.maxFactsPerExtraction`,
 * and the full `extraction.llm` block.
 *
 * Run with: npx tsx config-schema.test.ts
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

// ---------------------------------------------------------------------------
// Load manifest
// ---------------------------------------------------------------------------

const manifestPath = path.join(__dirname, 'openclaw.plugin.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8')) as {
  configSchema?: {
    properties?: Record<string, unknown>;
    additionalProperties?: boolean;
  };
};

// ---------------------------------------------------------------------------
// Top-level publicUrl is valid
// ---------------------------------------------------------------------------

{
  const props = manifest.configSchema?.properties ?? {};
  assert('publicUrl' in props, 'configSchema.properties includes publicUrl');
  assert(
    (props.publicUrl as { type?: string } | undefined)?.type === 'string',
    'configSchema.properties.publicUrl is type=string',
  );
}

// ---------------------------------------------------------------------------
// extraction.* surface
// ---------------------------------------------------------------------------

{
  const props = manifest.configSchema?.properties ?? {};
  assert('extraction' in props, 'configSchema.properties includes extraction');
  const extraction = props.extraction as {
    properties?: Record<string, unknown>;
    additionalProperties?: boolean;
  } | undefined;
  const extProps = extraction?.properties ?? {};
  assert('enabled' in extProps, 'extraction.properties includes enabled');
  assert('model' in extProps, 'extraction.properties includes model');
  assert('interval' in extProps, 'extraction.properties includes interval (3.3.1)');
  assert(
    'maxFactsPerExtraction' in extProps,
    'extraction.properties includes maxFactsPerExtraction (3.3.1)',
  );
  assert('llm' in extProps, 'extraction.properties includes llm block (3.3.1)');
  assert(extraction?.additionalProperties === false, 'extraction.additionalProperties === false (strict)');
}

// ---------------------------------------------------------------------------
// extraction.llm surface
// ---------------------------------------------------------------------------

{
  const extraction = (manifest.configSchema?.properties?.extraction ?? {}) as {
    properties?: Record<string, unknown>;
  };
  const llm = (extraction.properties?.llm ?? {}) as {
    properties?: Record<string, unknown>;
    additionalProperties?: boolean;
  };
  const llmProps = llm.properties ?? {};
  assert('provider' in llmProps, 'extraction.llm.properties includes provider');
  assert('model' in llmProps, 'extraction.llm.properties includes model');
  assert('apiKey' in llmProps, 'extraction.llm.properties includes apiKey');
  assert('baseUrl' in llmProps, 'extraction.llm.properties includes baseUrl');
  assert(llm.additionalProperties === false, 'extraction.llm.additionalProperties === false (strict)');
}

// ---------------------------------------------------------------------------
// Validate a sample config against the schema using Ajv (a standard JSON-Schema
// validator). If Ajv is not installed we fall back to a lightweight shape check
// that approximates the additionalProperties constraint.
// ---------------------------------------------------------------------------

async function runAjvValidation(): Promise<void> {
  let AjvMod: unknown;
  try {
    AjvMod = await import('ajv');
  } catch {
    console.log('# note: ajv not installed — falling back to structural checks');
    return;
  }
  type AjvCtor = new (opts?: unknown) => { compile: (schema: unknown) => (data: unknown) => boolean };
  const Ajv = (AjvMod as { default?: AjvCtor }).default ?? (AjvMod as { Ajv?: AjvCtor }).Ajv;
  if (!Ajv) {
    console.log('# note: ajv has unexpected shape — skipping strict validation');
    return;
  }
  const ajv = new Ajv({ allErrors: true, strict: false });
  const validate = ajv.compile(manifest.configSchema ?? {});

  const goodConfig = {
    publicUrl: 'https://gateway.example.com:18789',
    extraction: {
      enabled: true,
      interval: 5,
      maxFactsPerExtraction: 10,
      llm: {
        provider: 'zai',
        model: 'glm-4.5-flash',
        apiKey: 'redacted',
      },
    },
  };
  assert(validate(goodConfig) === true, 'schema accepts a config with publicUrl + extraction.* + extraction.llm');

  const badExtraKey = { publicUrl: 'x', somethingElse: true };
  assert(
    validate(badExtraKey) === false,
    'schema rejects unknown top-level key (additionalProperties:false still holds)',
  );

  const badExtraExtractionKey = { extraction: { enabled: true, bogus: 1 } };
  assert(
    validate(badExtraExtractionKey) === false,
    'schema rejects unknown key inside extraction (strict)',
  );

  const badExtraLlmKey = {
    extraction: { llm: { provider: 'zai', apiKey: 'x', bogus: 1 } },
  };
  assert(
    validate(badExtraLlmKey) === false,
    'schema rejects unknown key inside extraction.llm (strict)',
  );
}

await runAjvValidation();

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
