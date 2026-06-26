# QFC Governance Guide

## Overview

QFC uses on-chain governance for protocol upgrades, parameter changes, and AI model approval. Voting power is based on staked QFC tokens (1 QFC = 1 vote).

## Proposal Types

| Type | Deposit | Voting Period | Pass Threshold |
|------|---------|---------------|----------------|
| Parameter adjustment | 1,000 QFC | 7 days | 50% + 1 |
| Protocol upgrade | 10,000 QFC | 14 days | 66.7% (2/3) |
| Treasury spend | 5,000 QFC | 7 days | 50% + 1 |
| Emergency | 50,000 QFC | 3 days | 80% |

Failed proposals lose their deposit (burned).

## Adjustable Parameters

The following can be changed via governance:
- Block gas limit
- Minimum stake requirement
- Slashing penalty percentages
- Fee distribution ratios (producer/voter/burn)
- Maximum validator count

## AI Model Governance

New AI models must be approved by validator vote before miners can use them.

### Proposal Lifecycle

```
Validator proposes new model
    |
    v
Voting period (configurable, default 1 day)
    |
    v
Tally: requires >2/3 supermajority
    |
    +-- Passed: model added to registry, miners can use it
    +-- Rejected: proposal archived
    +-- Expired: no quorum reached
```

### RPC Methods

| Method | Description |
|--------|-------------|
| `qfc_proposeModel` | Submit a new model proposal (validator only) |
| `qfc_voteModel` | Vote on an active proposal (validator only) |
| `qfc_getModelProposals` | List all proposals with status |

### Querying Proposals

```typescript
const staking = new QFCStaking('testnet');

// Get all model governance proposals
// Returns: { id, model, proposer, status, votesFor, votesAgainst, deadline }
```

### Proposal Statuses

| Status | Meaning |
|--------|---------|
| Active | Voting in progress |
| Passed | Approved by >2/3 supermajority |
| Rejected | Failed to reach threshold |
| Expired | Voting period ended without quorum |

## Governor Contract

QFC uses an OpenZeppelin-based Governor contract with Timelock for on-chain governance:

```typescript
const contract = new QFCContract('testnet');

// Create proposal
await contract.send(
  GOVERNOR_ADDRESS,
  GOVERNOR_ABI,
  'propose',
  [targets, values, calldatas, description],
  wallet,
);

// Cast vote (0=Against, 1=For, 2=Abstain)
await contract.send(
  GOVERNOR_ADDRESS,
  GOVERNOR_ABI,
  'castVote',
  [proposalId, 1],
  wallet,
);
```

## Treasury

The Treasury contract holds ecosystem funds with role-based access:
- `DEFAULT_ADMIN_ROLE` — full control
- `SPENDER_ROLE` — can transfer funds (up to approved amount)

Treasury spending requires a governance proposal to pass.
