#!/usr/bin/env node
/**
 * Fetch a 5-card SAT flashcard deck from the Vocab Voyage MCP server.
 * Run with: node node-flashcards.mjs
 */
const ENDPOINT =
  'https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server';

const headers = {
  'Content-Type': 'application/json',
  Accept: 'application/json',
};
if (process.env.VV_MCP_TOKEN) {
  headers.Authorization = `Bearer ${process.env.VV_MCP_TOKEN}`;
}

const res = await fetch(ENDPOINT, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/call',
    params: {
      name: 'get_flashcards',
      arguments: { test_family: 'sat', count: 5 },
    },
  }),
});

const json = await res.json();
console.log(JSON.stringify(json, null, 2));