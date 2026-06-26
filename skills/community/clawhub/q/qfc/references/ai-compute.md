# QFC AI Compute Network Guide

## Overview

QFC's AI Compute Network replaces wasteful PoW hash mining with real AI inference tasks. GPU miners execute AI workloads (text embedding, image classification, LLM inference) and earn QFC rewards. Users can submit inference tasks via RPC and pay with QFC tokens.

## GPU Tiers

Miners are classified into three tiers based on benchmark scores:

| Tier | VRAM | Example GPUs | Task Types |
|------|------|-------------|------------|
| Tier 1 (Cold) | 4-8 GB | RTX 4060 Ti, RTX 3060 | Text embedding, image classification, OCR |
| Tier 2 (Warm) | 12-24 GB | RTX 3090, RTX 4080, RTX 4090 | Image generation, small LLM (<=7B) |
| Tier 3 (Hot) | 40-80 GB | A100, H100 | Medium/large LLM (7B-70B+) |

## Supported Models

Models are approved via on-chain governance (validator vote >2/3). Query the current registry:

```typescript
const inference = new QFCInference('testnet');
const models = await inference.getModels();
```

Current baseline models:
- `qfc-embed-small` — Text embedding (all-MiniLM-L6-v2 style), Tier 1
- `qfc-embed-medium` — Text embedding (larger), Tier 1
- `qfc-classify-small` — Image classification, Tier 1

## Task Lifecycle

```
User submits task (RPC + signature + max_fee)
    |
    v
Fee escrowed (max_fee deducted from user balance)
    |
    v
Task Router assigns to matching miner (by GPU tier)
    |
    v
Miner executes inference, submits proof
    |
    v
Verification:
  - Basic check: epoch, model, FLOPS range
  - 5% spot-check: re-execute and compare output hash
    |
    v
Terminal state:
  - Completed: result returned, fee settled (70% miner, 10% validator, 20% burn)
  - Failed: miner slashed (5% stake, 6h jail)
  - Expired (5min timeout): fee refunded to user
```

## Submitting a Task

```typescript
import { QFCInference } from '@qfc/openclaw-skill';
import { ethers } from 'ethers';

const inference = new QFCInference('testnet');

// 1. Estimate fee
const fee = await inference.estimateFee('qfc-embed-small', 256);
console.log(`Estimated fee: ${fee.baseFee} QFC`);

// 2. Submit task (requires a funded wallet)
const wallet = new ethers.Wallet(privateKey, provider);
const taskId = await inference.submitTask(
  'qfc-embed-small',
  'Hello, QFC compute network!',
  fee.baseFee,
  wallet,
);

// 3. Wait for result
const result = await inference.waitForResult(taskId, 120_000);

// 4. Decode
if (result.status === 'Completed' && result.result) {
  const decoded = inference.decodeResult(result.result);
  console.log('Output:', decoded.output);
  console.log('Execution time:', decoded.executionTimeMs, 'ms');
}
```

## Result Format

Completed tasks return a JSON envelope:

```json
{
  "model": "qfc-embed-small",
  "submitter": "0x1234...abcd",
  "miner": "0x5678...ef01",
  "output_base64": "WzAuMTIzLCAwLjQ1NiwgLi4uXQ==",
  "execution_time_ms": 150,
  "submitted_at": 1709800000,
  "completed_at": 1709800003
}
```

The `output_base64` field contains the base64-encoded inference output. Use `decodeResult()` to parse it automatically.

## Fee Model

Fees are estimated based on:
- **Model complexity** (GFLOPS required)
- **GPU tier** needed
- **Network congestion**

Formula: `base_fee = GFLOPS * tier_multiplier`

| GPU Tier | Multiplier |
|----------|-----------|
| Tier 1 | 1x |
| Tier 2 | 3x |
| Tier 3 | 10x |

Fee settlement: 70% to miner, 10% to block producer, 20% burned.

## Verification

QFC uses a dual verification system:
1. **Basic verification** — Every proof: check epoch, model approval, FLOPS within expected range
2. **Spot-check verification** — 5% probability: re-execute the inference on a validator node, compare output hash (blake3). Mismatch triggers slashing (5% stake, 6h jail)

## RPC Methods

| Method | Description |
|--------|-------------|
| `qfc_getSupportedModels` | List approved models |
| `qfc_getInferenceStats` | Network inference statistics |
| `qfc_submitPublicTask` | Submit inference task (signed) |
| `qfc_getPublicTaskStatus` | Query task status by ID |
| `qfc_estimateInferenceFee` | Estimate task cost |
| `qfc_subscribeTaskStatus` | WebSocket: subscribe to task status changes |

## Network Statistics

```typescript
const stats = await inference.getStats();
console.log(`Tasks completed: ${stats.tasksCompleted}`);
console.log(`Active miners: ${stats.activeMinerCount}`);
console.log(`Pass rate: ${(stats.passRate * 100).toFixed(1)}%`);
```
