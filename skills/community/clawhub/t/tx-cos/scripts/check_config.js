#!/usr/bin/env node
const required = ["COS_SECRET_ID", "COS_SECRET_KEY", "COS_REGION", "COS_BUCKET"];
const optional = ["COS_DOMAIN"];

const result = {
  ok: true,
  required: {},
  optional: {},
  missing: [],
};

for (const key of required) {
  const set = Boolean(process.env[key]);
  result.required[key] = set ? "set" : "missing";
  if (!set) result.missing.push(key);
}

for (const key of optional) {
  result.optional[key] = process.env[key] ? "set" : "missing";
}

result.ok = result.missing.length === 0;
console.log(JSON.stringify(result, null, 2));
process.exit(result.ok ? 0 : 1);
