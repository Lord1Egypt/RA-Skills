#!/usr/bin/env node
// wip-agent-pay MCP server
// Exposes agent_pay, agent_pay_x402, agent_pay_fund tools via MCP stdio transport.

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { pay, fund, mint } from './providers/index.js';

const server = new Server(
  { name: 'wip-agent-pay', version: '2.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'agent_pay',
      description: 'Authorize a micropayment from the agent wallet. Returns a one-time self-destructing URL.',
      inputSchema: {
        type: 'object',
        properties: {
          amount: { type: 'number', description: 'Payment amount in USD' },
          service: { type: 'string', description: 'Service identifier (e.g. "morning-stew")' },
          note: { type: 'string', description: 'Optional note (e.g. "MS-#8")' },
        },
        required: ['amount', 'service'],
      },
    },
    {
      name: 'agent_pay_x402',
      description: 'Pay for a paywalled URL. The agent wallet handles payment automatically. Returns the content.',
      inputSchema: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'The paywalled URL to pay for' },
          wallet: { type: 'string', enum: ['cdp', 'privy'], description: 'Which wallet to use (default: cdp)' },
        },
        required: ['url'],
      },
    },
    {
      name: 'agent_pay_fund',
      description: 'Fund the agent wallet. Returns a checkout URL the user opens to pay via Apple Pay.',
      inputSchema: {
        type: 'object',
        properties: {
          amount: { type: 'number', description: 'USD amount to fund' },
          wallet: { type: 'string', enum: ['cdp', 'privy'], description: 'Which wallet to fund (default: cdp)' },
        },
        required: ['amount'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === 'agent_pay') {
      if (typeof args.amount !== 'number' || args.amount <= 0) {
        return { content: [{ type: 'text', text: 'amount must be a positive number' }], isError: true };
      }
      if (typeof args.service !== 'string' || args.service.length === 0) {
        return { content: [{ type: 'text', text: 'service is required' }], isError: true };
      }
      const result = await mint(args.amount, args.service, args.note || '');
      if (result.success) {
        const prefix = result.demo ? '[DEMO] ' : '';
        return { content: [{ type: 'text', text: `${prefix}Payment authorized. One-time URL: ${result.url}` }] };
      }
      return { content: [{ type: 'text', text: `Payment failed: ${result.error || 'unknown error'}` }], isError: true };
    }

    if (name === 'agent_pay_x402') {
      if (!args.url) {
        return { content: [{ type: 'text', text: 'url is required' }], isError: true };
      }
      const result = await pay(args.url, { wallet: args.wallet || 'cdp' });
      if (result.success) {
        return { content: [{ type: 'text', text: `Paid ${result.amount} USDC on ${result.network || 'base'}. Service: ${result.service}.` }] };
      }
      return { content: [{ type: 'text', text: `Payment failed: ${result.error || 'unknown error'}` }], isError: true };
    }

    if (name === 'agent_pay_fund') {
      if (typeof args.amount !== 'number' || args.amount <= 0) {
        return { content: [{ type: 'text', text: 'amount must be a positive number' }], isError: true };
      }
      const result = await fund(args.amount, { wallet: args.wallet || 'cdp' });
      if (result.success) {
        return { content: [{ type: 'text', text: `Checkout ready. Have the user open: ${result.checkoutUrl}` }] };
      }
      return { content: [{ type: 'text', text: `Funding failed: ${result.error || 'unknown error'}` }], isError: true };
    }

    return { content: [{ type: 'text', text: `Unknown tool: ${name}` }], isError: true };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
