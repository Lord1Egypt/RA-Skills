---
name: Meme Rush
description: Fetch real-time meme token lists and topic rush from the Binance Wallet building in BNBTown (Binance Web3 APIs).
building: Binance Wallet
building_id: binanceWallet
---

# Meme Rush Skill

Use this skill when the owner asks about new meme tokens, meme launches, bonding curve statuses, migration statuses, pump.fun tokens, fast meme trading, market hot topics, or trending narratives.

## When to Use

Owner says something like:
- "Are there any new exciting meme tokens on Solana?"
- "What are the hot topics today?"
- "Find me newly migrated tokens on pump.fun"
- "Show me tokens with top 10 holders less than 20%"

## Execution Protocol

To use this skill, the agent must physically walk to the Binance Wallet building (`binanceWallet`) and execute specific APIs.

### Step 1: Submit Task
```http
POST $XTOWN_SERVER_URL/agent/task
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{ "session_token": "<token>", "skill_id": "binanceWallet" }
```
→ Wait for status `awaiting_params`.

### Step 2: Execute Tool
Call `/agent/task/execute` specifying `method` as either `meme-rush` or `topic-rush`.

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "method": "meme-rush", // Switch to "topic-rush" for topics
    "params": {
      "chainId": "CT_501", // "56" for BSC, "CT_501" for Solana
      "rankType": 10       // 10=New, 20=Finalizing, 30=Migrated
    }
  }
}
```

## Supported Endpoints & Arguments

### `meme-rush`
Fetch a ranked list of trending tokens across various launchpads.
- **Required `params` fields:**
  - `chainId` (string) - `56` (BSC), `CT_501` (Solana)
  - `rankType` (integer) - `10` (New), `20` (Finalizing), `30` (Migrated)
- **Optional `params` fields:**
  - `limit` (integer) - Max results
  - `keywords` (string[]) - Ex. ["pepe", "doge"]
  - `progressMin` / `progressMax` (string) - Bonding curve progress
  - `holdersMin` / `holdersMax` (long)
  - `holdersTop10PercentMin` / `holdersTop10PercentMax` (string) - Ex. "25" (meaning 25%)

### `topic-rush`
Fetch AI-driven market topics and narratives, alongside tokens associated with that narrative.
- **Required `params` fields:**
  - `chainId` (string) - `56` (BSC), `CT_501` (Solana)
  - `rankType` (integer) - `10` (Latest), `20` (Rising), `30` (Viral)
  - `sort` (integer) - `10` (create time), `20` (net inflow), `30` (viral time)
- **Optional `params` fields:**
  - `asc` (boolean)
  - `keywords` (string)
  - `topicType` (string)
  - `tokenSizeMin` / `tokenSizeMax` (integer)

---

## Example Prompt Workflow
```
User: "What are the latest hot topics on Solana?"
1. Walk to binanceWallet building
2. Execute tool `topic-rush` with params `{"chainId": "CT_501", "rankType": 10, "sort": 10}`
3. Analyze data returned and report back.
```
