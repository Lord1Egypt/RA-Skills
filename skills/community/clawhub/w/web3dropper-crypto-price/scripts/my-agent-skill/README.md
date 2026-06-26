# Web3dropper Crypto Price Skill

This OpenClaw skill fetches real-time cryptocurrency prices using the Binance public API.

## Features
- Fetch BTC/USDT price from Binance
- Lightweight Node.js implementation
- Useful for AI agents that need crypto market data

## Example
Run the script to get the current BTC price:

node index.js

Output example:
BTC Price: 67178

## Use Case
AI agents can use this skill to:
- Monitor crypto market prices
- Trigger alerts
- Provide trading data

Built by Web3dropper.

## Technical Details

This skill is implemented in Node.js and uses the Axios HTTP client to fetch cryptocurrency market data from the Binance public API.

The main script (index.js) performs the following steps:

1. Sends an HTTP GET request to the Binance ticker endpoint.
2. Parses the JSON response returned by the API.
3. Extracts the latest BTC/USDT trading price.
4. Prints the value to the console so that OpenClaw agents can consume it.

The code is intentionally lightweight so it can run inside minimal OpenClaw agent environments.

## Architecture

OpenClaw Agent
        |
        v
Crypto Price Skill
        |
        v
Binance REST API

This architecture allows AI agents to retrieve market data without needing direct exchange integration.

## Extending the Skill

Developers can extend this skill by:

- Adding support for multiple trading pairs
- Adding ETH, SOL, or other tokens
- Returning structured JSON responses
- Integrating WebSocket streams for real-time price feeds
- Connecting the data to automated trading strategies

## Security Considerations

This skill only uses the public Binance API endpoint and does not require authentication or API keys.

Therefore it does not expose private user data or trading permissions.

