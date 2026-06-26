# AgentCard agent.txt Analysis

**Source:** agentcard.sh/agent.txt
**Retrieved:** 2026-03-25

## Structure

Pure operational instructions. No marketing. Clear sections:

1. **One-line description**: "Virtual debit cards you can use to pay for things online."
2. **When to Use**: 4 bullet points (buy something, need spending limit, x402 payment, human asked)
3. **When NOT to Use**: 4 bullet points (physical purchase, recurring billing, send money, 3DS)
4. **Install**: `npm install -g agent-cards`
5. **Authenticate**: `agent-cards signup`
6. **Commands**: create, list, details, balance (each with exact syntax)
7. **MCP Integration**: how to connect, then each tool with exact params
8. **Typical flow**: 8 numbered steps from signup to purchase
9. **Links**: website + npm

## Key Patterns

- **No pitch**: doesn't explain what AgentCard "is" or why it matters. Just what it does.
- **When / When NOT**: explicitly scopes the skill. AI knows when to use it AND when not to.
- **Exact params**: every MCP tool lists its params with types.
- **Typical flow**: end-to-end walkthrough so the AI can follow the happy path.
- **Short**: fits in one screen. AI reads it all and follows it.

## What We Can Learn

1. Start with "what" not "why". The AI doesn't need to be sold.
2. "When NOT to Use" is as valuable as "When to Use". Prevents misuse.
3. Exact params and syntax. No ambiguity.
4. Typical flow = the AI's script. If it exists, the AI follows it.
5. Brevity works. Short files get fully read. Long files get skimmed.
