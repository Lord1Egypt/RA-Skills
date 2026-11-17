// wip-agent-pay OpenClaw plugin
// Registers agent_pay, agent_pay_x402, agent_pay_fund as tools in the agent context.

import { pay, fund, mint } from './providers/index.js';

export default {
  register(api) {
    // --- Mint one-time URL (Mode B) ---
    api.registerTool({
      name: 'agent_pay',
      label: 'Authorize Agent Payment',
      description: 'Authorize a micropayment from the agent wallet. Returns a one-time self-destructing URL.',
      parameters: {
        type: 'object',
        properties: {
          amount: { type: 'number', description: 'Payment amount in USD' },
          service: { type: 'string', description: 'Service identifier (e.g. "morning-stew")' },
          note: { type: 'string', description: 'Optional note (e.g. "MS-#8")' },
        },
        required: ['amount', 'service'],
      },
      async execute(_id, params) {
        try {
          const result = await mint(params.amount, params.service, params.note || '');
          if (result.success) {
            const prefix = result.demo ? '[DEMO] ' : '';
            return { content: [{ type: 'text', text: `${prefix}Payment authorized. One-time URL: ${result.url}` }] };
          }
          return { content: [{ type: 'text', text: `Payment failed: ${result.error || 'unknown error'}` }], isError: true };
        } catch (err) {
          return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
        }
      },
    }, { optional: true });

    // --- Pay paywalled URL (x402) ---
    api.registerTool({
      name: 'agent_pay_x402',
      label: 'Pay Paywalled URL',
      description: 'Pay for a paywalled URL. The agent wallet handles payment automatically. Returns the content.',
      parameters: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'The paywalled URL to pay for' },
          wallet: { type: 'string', enum: ['cdp', 'privy'], description: 'Which wallet to use (default: cdp)' },
        },
        required: ['url'],
      },
      async execute(_id, params) {
        try {
          const result = await pay(params.url, { wallet: params.wallet || 'cdp' });
          if (result.success) {
            return { content: [{ type: 'text', text: `Paid ${result.amount} USDC on ${result.network || 'base'}. Service: ${result.service}.` }] };
          }
          return { content: [{ type: 'text', text: `Payment failed: ${result.error || 'unknown error'}` }], isError: true };
        } catch (err) {
          return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
        }
      },
    }, { optional: true });

    // --- Fund wallet (Apple Pay) ---
    api.registerTool({
      name: 'agent_pay_fund',
      label: 'Fund Agent Wallet',
      description: 'Fund the agent wallet. Returns a checkout URL the user opens to pay via Apple Pay.',
      parameters: {
        type: 'object',
        properties: {
          amount: { type: 'number', description: 'USD amount to fund' },
          wallet: { type: 'string', enum: ['cdp', 'privy'], description: 'Which wallet to fund (default: cdp)' },
        },
        required: ['amount'],
      },
      async execute(_id, params) {
        try {
          const result = await fund(params.amount, { wallet: params.wallet || 'cdp' });
          if (result.success) {
            return { content: [{ type: 'text', text: `Checkout ready. Have the user open: ${result.checkoutUrl}` }] };
          }
          return { content: [{ type: 'text', text: `Funding failed: ${result.error || 'unknown error'}` }], isError: true };
        } catch (err) {
          return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
        }
      },
    }, { optional: true });
  }
};
