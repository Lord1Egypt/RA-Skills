'use strict'

// Preserve integer tokens before JavaScript can round 64-bit IDs. Strings remain opaque.
function parseJson(text) {
  JSON.parse(text) // Reject malformed JSON before token substitution.
  return JSON.parse(text.replace(/"(?:[^"\\]|\\.)*"|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/g, token => {
    if (token[0] === '"' || /[.eE]/.test(token)) return token
    return Number.isSafeInteger(Number(token)) ? token : JSON.stringify(token)
  }))
}

// BigInt is used only for validated integer fields on the wire, never in public output.
function stringifyJson(value) {
  if (typeof value === 'bigint') return value.toString()
  if (Array.isArray(value)) return '[' + value.map(v => stringifyJson(v) ?? 'null').join(',') + ']'
  if (value && typeof value === 'object') return '{' + Object.entries(value)
    .filter(([, v]) => v !== undefined).map(([k, v]) => JSON.stringify(k) + ':' + stringifyJson(v)).join(',') + '}'
  return JSON.stringify(value)
}
module.exports = { parseJson, stringifyJson }
