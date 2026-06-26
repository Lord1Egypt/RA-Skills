#!/usr/bin/env node
/**
 * fetch-secrets.js — OpenClaw exec provider bridge for Supabase Vault
 *
 * Called by OpenClaw at gateway startup via the exec secret provider.
 * Fetches requested secrets from Supabase Vault and outputs the exec protocol.
 *
 * Usage:
 *   node fetch-secrets.js /OPENAI_API_KEY /ANTHROPIC_API_KEY
 *   node fetch-secrets.js          # fetches ALL secrets
 *
 * Output (stdout): { "protocolVersion": 1, "values": { "/KEY": "val" }, "errors": {} }
 *
 * Note: @supabase/supabase-js must be installed alongside this script.
 *   npm install --prefix ~/.openclaw/skills/supabase-vault @supabase/supabase-js
 */

"use strict";

const path = require("node:path");

// Load keychain from same directory
const keychain = require(path.join(__dirname, "keychain.js"));

const TIMEOUT_MS = 8_000;

function output(values, errors) {
  process.stdout.write(
    JSON.stringify({ protocolVersion: 1, values, errors }) + "\n"
  );
}

function stripLeadingSlash(id) {
  return id.startsWith("/") ? id.slice(1) : id;
}

function addLeadingSlash(name) {
  return name.startsWith("/") ? name : `/${name}`;
}

async function main() {
  const requestedIds = process.argv.slice(2); // e.g. ["/OPENAI_API_KEY", "/ANTHROPIC_API_KEY"]

  // Set up timeout
  const timeoutHandle = setTimeout(() => {
    output({}, { _timeout: { message: "fetch-secrets: timed out after 8 seconds" } });
    process.exit(0);
  }, TIMEOUT_MS);
  timeoutHandle.unref();

  let creds;
  try {
    creds = keychain.retrieve();
  } catch (err) {
    output({}, { _auth: { message: `fetch-secrets: credentials not found — ${err.message}` } });
    process.exit(0);
  }

  let createClient;
  try {
    ({ createClient } = require(
      path.join(__dirname, "..", "node_modules", "@supabase", "supabase-js")
    ));
  } catch {
    try {
      ({ createClient } = require("@supabase/supabase-js"));
    } catch (err) {
      output({}, { _deps: { message: `fetch-secrets: @supabase/supabase-js not found — run: npm install --prefix ~/.openclaw/skills/supabase-vault @supabase/supabase-js` } });
      process.exit(0);
    }
  }

  const supabase = createClient(creds.url, creds.serviceRoleKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  const values = {};
  const errors = {};

  try {
    let namesToFetch = requestedIds.map(stripLeadingSlash);

    // If no args, fetch all secrets
    if (namesToFetch.length === 0) {
      const { data, error } = await supabase.rpc("list_secret_names");
      if (error) {
        output({}, { _list: { message: `fetch-secrets: failed to list secrets — ${error.message}` } });
        process.exit(0);
      }
      namesToFetch = (data || []).map((row) => (typeof row === "string" ? row : row.name));
    }

    // Fetch each secret
    await Promise.all(
      namesToFetch.map(async (name) => {
        const refKey = addLeadingSlash(name);
        try {
          const { data, error } = await supabase.rpc("read_secret", { secret_name: name });
          if (error) {
            errors[refKey] = { message: error.message };
          } else if (data === null || data === undefined) {
            errors[refKey] = { message: `Secret "${name}" not found in Vault` };
          } else {
            values[refKey] = String(data);
          }
        } catch (err) {
          errors[refKey] = { message: String(err.message || err) };
        }
      })
    );
  } catch (err) {
    output({}, { _fetch: { message: `fetch-secrets: unexpected error — ${err.message}` } });
    process.exit(0);
  }

  clearTimeout(timeoutHandle);
  output(values, errors);
}

main().catch((err) => {
  output({}, { _fatal: { message: String(err.message || err) } });
  process.exit(0);
});
