# edgebets-sdk

TypeScript SDK for the EdgeBets sports simulation API. Run professional-grade Monte Carlo simulations for NBA, NFL, MLB, and MLS with x402 USDC payments on Solana.

## Features

- **10,000 Monte Carlo simulations** per request
- **Full TypeScript support** with comprehensive types
- **Automatic payment handling** via x402 protocol
- **Auto-polling** for simulation results
- **4 major sports leagues** (NBA, NFL, MLB, MLS)
- **Edge detection** vs market odds
- **OpenClaw compatible** for AI agent integration

## Installation

```bash
npm install edgebets-sdk
```

## Quick Start

```typescript
import { EdgeBetsClient } from 'edgebets-sdk';
import { Keypair } from '@solana/web3.js';
import fs from 'fs';

// Load your Solana wallet
const secretKey = JSON.parse(fs.readFileSync('~/.config/solana/id.json', 'utf-8'));
const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));

// Create client
const client = new EdgeBetsClient({
  wallet: keypair,
  debug: true,
});

// Get today's NBA games (FREE)
const games = await client.getGames('nba');
console.log(`Found ${games.length} NBA games today`);

// Run simulation on first game ($0.50 USDC)
const result = await client.simulate('nba', games[0].id, {
  onStatus: (status) => console.log(`Status: ${status}`),
});

// Display results
console.log(`${result.homeTeamName} vs ${result.awayTeamName}`);
console.log(`Home win: ${(result.homeWinProbability * 100).toFixed(1)}%`);
console.log(`Away win: ${(result.awayWinProbability * 100).toFixed(1)}%`);
console.log(`Projected total: ${result.averageTotalPoints.toFixed(1)}`);

if (result.edgeAnalysis?.homeIsValue) {
  console.log('VALUE: Home team has positive edge vs market!');
}
```

## API Reference

### EdgeBetsClient

#### Constructor

```typescript
const client = new EdgeBetsClient({
  wallet: keypair,              // Solana Keypair or WalletAdapter
  rpcEndpoint: '...',           // Custom RPC (default: mainnet-beta)
  apiBaseUrl: '...',            // Custom API URL
  pollingInterval: 3000,        // Poll interval in ms
  pollingTimeout: 120000,       // Max poll time in ms
  debug: false,                 // Enable debug logging
});
```

### Games (FREE)

```typescript
// Get today's games
const games = await client.getGames('nba');     // 'nba' | 'nfl' | 'mlb' | 'mls'

// Get tomorrow's games
const tomorrow = await client.getTomorrowGames('nfl');

// Get specific game
const game = await client.getGameDetails('mlb', 'mlb-2026-03-28-nyy-bos');
```

### Simulations ($0.50 USDC)

```typescript
// Full simulation with auto-polling
const result = await client.simulate('nba', gameId, {
  count: 10000,                               // Simulation count
  onStatus: (status, job) => { ... },         // Status callback
  pollingInterval: 3000,                      // Override poll interval
  pollingTimeout: 120000,                     // Override timeout
});

// Manual flow (advanced)
const job = await client.startSimulation('nba', gameId);
const status = await client.pollResult(job.jobId);
```

### Wallet & Balance

```typescript
// Check balance
const balance = await client.checkBalance();
// { usdc: 5.25, sol: 0.05, sufficient: true }

// Get price quote
const quote = await client.getQuote();
// { price: 0.5, currency: 'USDC', network: 'solana-mainnet', recipient: '...' }

// Check if wallet configured
client.hasWallet();  // boolean

// Get treasury address
client.getTreasuryWallet();  // 'DuDL...'

// Get simulation price
client.getPrice();  // 0.5
```

## Types

### SimulationResult

```typescript
interface SimulationResult {
  gameId: string;
  simulationCount: number;

  // Teams
  homeTeamName: string;
  awayTeamName: string;
  homeTeamAbbr: string;
  awayTeamAbbr: string;

  // Win Probabilities (0-1)
  homeWinProbability: number;
  awayWinProbability: number;

  // Score Projections
  averageHomeScore: number;
  averageAwayScore: number;
  averageTotalPoints: number;
  predictedSpread: number;

  // Advanced Analytics
  elo?: EloRatings;
  fourFactors?: FourFactors;          // NBA only
  edgeAnalysis?: EdgeAnalysis;         // Value vs market
  bettingInsights?: BettingInsights;   // Fair odds
  scoreDistribution?: ScoreDistribution;
  factorBreakdown?: FactorBreakdown[];
}
```

### EdgeAnalysis

```typescript
interface EdgeAnalysis {
  hasOdds: boolean;
  homeEdge: number;         // Positive = value
  awayEdge: number;
  homeIsValue: boolean;
  awayIsValue: boolean;
  spreadEdge: number;
  homeKelly?: number;       // Kelly bet fraction
  awayKelly?: number;
}
```

## Error Handling

```typescript
import {
  EdgeBetsError,
  PaymentRequiredError,
  InsufficientBalanceError,
  WalletNotConfiguredError,
  PollingTimeoutError,
  SimulationFailedError,
} from 'edgebets-sdk';

try {
  const result = await client.simulate('nba', gameId);
} catch (error) {
  if (error instanceof InsufficientBalanceError) {
    console.log(`Need ${error.required} USDC, have ${error.available}`);
  } else if (error instanceof PollingTimeoutError) {
    console.log('Simulation took too long, try again');
  } else if (error instanceof WalletNotConfiguredError) {
    console.log('Please configure a wallet');
  }
}
```

## Helper Function

```typescript
import { createClient } from 'edgebets-sdk';
import fs from 'fs';

// Quick setup from secret key file
const secretKey = JSON.parse(fs.readFileSync('wallet.json', 'utf-8'));
const client = createClient(secretKey, { debug: true });
```

## OpenClaw Integration

This package includes a `SKILL.md` for OpenClaw agents. Install via ClawHub:

```bash
clawhub install edgebets
```

Or give your agent this URL:
```
https://api.edgebets.fun/api/v1/x402/openapi.json
```

## Pricing

| Action | Cost |
|--------|------|
| Get games | FREE |
| Run simulation | $0.50 USDC |

Payments are processed via x402 protocol on Solana mainnet.

## Requirements

- Node.js 18+
- Solana wallet with USDC (mainnet)
- Small amount of SOL for transaction fees

## Links

- [Website](https://edgebets.fun)
- [API Documentation](https://api.edgebets.fun/api/v1/x402)
- [OpenAPI Spec](https://api.edgebets.fun/api/v1/x402/openapi.json)
- [x402 Protocol](https://x402.org)

## License

MIT
