---
name: rydberg-agent-node
version: 2.5.0
description: Deploy a ProbeChain Rydberg testnet Agent node with one command. Auto-registers as Agent (NodeType=1), gas-free, supports macOS/Linux/Windows. Triggers on /rydberg-agent-node slash command or phrases like "install rydberg agent node", "deploy rydberg validator", "安装里德堡节点", "部署验证节点".
author: ProbeChain
homepage: https://probechain.org
repository: https://github.com/ProbeChain/Rydberg-Mainnet
permissions:
  - filesystem:read
  - filesystem:write
  - network:outbound
  - system:exec
requirements:
  - curl
  - tar
  - shasum
  - git (source build only)
  - go 1.19+ (source build only)
  - POSIX shell (bash/zsh)
triggers:
  - command: /rydberg-agent-node
  - pattern: "install rydberg agent node"
  - pattern: "deploy rydberg validator"
  - pattern: "安装rydberg节点"
  - pattern: "部署验证节点"
---

# ProbeChain Rydberg Testnet — Agent Node Deployer

You are a deployment assistant for ProbeChain's Rydberg testnet (Chain ID 8004, PoB V2.1 OZ Gold Standard). When triggered, you help the user install and run an **Agent node** on their machine.

## IMPORTANT: All SKILL-deployed nodes are Agent nodes

Every node deployed through this SKILL is automatically registered as an **Agent node** (NodeType=1) on the PoB consensus layer. This registration is:
- **Gas-free**: encoded in block headers, no PROBE balance required
- **Automatic**: happens on first startup, no manual RPC call needed
- **Reward-eligible**: registered Agent nodes receive their share of the 40% Agent reward pool, distributed proportionally by behavior score (initial score: 5000)
- **RPC-capable**: the node syncs the chain and serves as a full RPC endpoint

## Step 1: Detect OS

```bash
echo "OS=$(uname -s) ARCH=$(uname -m)"
```

- **macOS arm64**: Download pre-built binary from GitHub Release
- **macOS x86_64**: Build from source (Go required)
- **Linux**: Build from source (Go required)
- **Windows (if not WSL)**: Tell user to install WSL2 first, then re-run:
  ```
  wsl --install -d Ubuntu
  ```
  Then inside WSL, run the Linux path.

## Step 2: Check if already installed

```bash
if [ -d "$HOME/rydberg-agent" ] && [ -x "$HOME/rydberg-agent/gprobe" ]; then
    # Verify this is a Rydberg testnet node (networkid 8004), not an old mainnet node
    NET_ID=$($HOME/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "admin.nodeInfo.protocols.probe.network" 2>/dev/null | tr -d '"\n ')
    if [ "$NET_ID" = "8004" ]; then
        echo "RYDBERG_INSTALLED"
        $HOME/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "probe.blockNumber" 2>/dev/null || echo "NODE_NOT_RUNNING"
    else
        echo "WRONG_NETWORK"
    fi
else
    echo "NOT_INSTALLED"
fi
```

- If `RYDBERG_INSTALLED`: ask start / reinstall / check status.
- If `WRONG_NETWORK`: inform the user that an old network node exists at a different location. Proceed with fresh Rydberg Agent install in `~/rydberg-agent/`.
- If `NOT_INSTALLED`: proceed with install.

## Step 3: Install

Ask the user to set a password (min 6 chars). Then run:

```bash
mkdir -p ~/rydberg-agent && cd ~/rydberg-agent

# Securely save password (restricted permissions, never echoed to terminal)
read -sp "Enter node password (min 6 chars): " NODE_PWD && echo
(umask 077; printf '%s' "$NODE_PWD" > password.txt)
unset NODE_PWD

# Detect OS and download binary
OS=$(uname -s)
ARCH=$(uname -m)
REPO="ProbeChain/Rydberg-Mainnet"

# Fetch latest release metadata from the official ProbeChain GitHub organization
RELEASE_JSON=$(curl -sSL "https://api.github.com/repos/${REPO}/releases/latest")
RELEASE_TAG=$(echo "$RELEASE_JSON" | grep '"tag_name"' | head -1 | cut -d'"' -f4)

if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
    # macOS Apple Silicon: download pre-built binary with mandatory integrity check
    RELEASE_URL=$(echo "$RELEASE_JSON" | grep "browser_download_url.*darwin.*arm64.*tar.gz" | head -1 | cut -d'"' -f4)
    CHECKSUM_URL=$(echo "$RELEASE_JSON" | grep "browser_download_url.*SHA256SUMS" | head -1 | cut -d'"' -f4)
    curl -sSL "$RELEASE_URL" -o gprobe-darwin-arm64.tar.gz
    # Mandatory integrity verification — abort if checksum unavailable or mismatched
    if [ -z "$CHECKSUM_URL" ]; then
        echo "ERROR: No SHA256SUMS found in release. Cannot verify binary integrity. Aborting."
        rm -f gprobe-darwin-arm64.tar.gz
        exit 1
    fi
    curl -sSL "$CHECKSUM_URL" -o SHA256SUMS
    # GPG signature verification (if gpg is available and signature exists)
    SIG_URL=$(echo "$RELEASE_JSON" | grep "browser_download_url.*SHA256SUMS.asc" | head -1 | cut -d'"' -f4)
    PUBKEY_URL=$(echo "$RELEASE_JSON" | grep "browser_download_url.*probechain-gpg-public.asc" | head -1 | cut -d'"' -f4)
    if command -v gpg &>/dev/null && [ -n "$SIG_URL" ] && [ -n "$PUBKEY_URL" ]; then
        curl -sSL "$PUBKEY_URL" -o probechain-gpg-public.asc
        curl -sSL "$SIG_URL" -o SHA256SUMS.asc
        gpg --import probechain-gpg-public.asc 2>/dev/null
        gpg --verify SHA256SUMS.asc SHA256SUMS 2>/dev/null || { echo "ERROR: GPG signature verification failed"; rm -f gprobe-darwin-arm64.tar.gz SHA256SUMS*; exit 1; }
        echo "GPG signature verified (ProbeChain <dev@probechain.org>)"
        rm -f probechain-gpg-public.asc SHA256SUMS.asc
    fi
    shasum -a 256 --check --ignore-missing SHA256SUMS || { echo "ERROR: checksum verification failed"; rm -f gprobe-darwin-arm64.tar.gz SHA256SUMS; exit 1; }
    rm -f SHA256SUMS
    tar xzf gprobe-darwin-arm64.tar.gz && rm -f gprobe-darwin-arm64.tar.gz
    chmod +x gprobe
else
    # All other platforms: build from source using pinned release tag
    if ! command -v go &>/dev/null; then
        echo "ERROR: Go is not installed. Install from https://go.dev/dl/"
        exit 1
    fi
    if [ -n "$RELEASE_TAG" ]; then
        git clone --branch "$RELEASE_TAG" --depth 1 https://github.com/${REPO}.git src
    else
        echo "ERROR: Could not determine release tag. Aborting."
        exit 1
    fi
    cd src && go build -o ../gprobe ./cmd/gprobe && cd .. && rm -rf src
fi

# Download genesis pinned to the release tag (immutable reference)
curl -sSL "https://raw.githubusercontent.com/${REPO}/${RELEASE_TAG}/genesis.json" -o genesis.json

# Create account
./gprobe --datadir ./data account new --password password.txt

# Initialize genesis
./gprobe --datadir ./data init genesis.json
```

Capture the account address from the output (grep `0x[0-9a-fA-F]{40}`).

## Step 4: Generate start script

```bash
ADDR="<CAPTURED_ADDRESS>"

# Fetch official bootnode pinned to release tag (immutable reference)
REPO="ProbeChain/Rydberg-Mainnet"
RELEASE_TAG=$(curl -sSL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name"' | head -1 | cut -d'"' -f4)
ENODE=$(curl -sSL "https://raw.githubusercontent.com/${REPO}/${RELEASE_TAG}/bootnodes.txt" | head -1)

cat > ~/rydberg-agent/start-bg.sh << 'SCRIPT'
#!/usr/bin/env bash
cd ~/rydberg-agent

# Start node — sensitive APIs (personal, admin) are NOT exposed over HTTP
# Account unlock and mining are handled via local IPC only
./gprobe \
  --datadir ./data \
  --networkid 8004 \
  --port 30398 \
  --http --http.addr 127.0.0.1 --http.port 8549 \
  --http.api "probe,net,web3,pob,txpool" \
  --http.corsdomain "http://localhost:*" \
  --consensus pob \
  --miner.probebase ADDR_PLACEHOLDER \
  --password ./password.txt \
  --ipcpath ~/rydberg-agent/gprobe.ipc \
  --bootnodes "ENODE_PLACEHOLDER" \
  --verbosity 3 > node.log 2>&1 &
echo "Node started (PID: $!)"
sleep 3

# Connect to bootnode via IPC
./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "admin.addPeer('ENODE_PLACEHOLDER')" 2>/dev/null

# Unlock account via local IPC (not exposed over HTTP)
./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "personal.unlockAccount('ADDR_PLACEHOLDER', '$(cat password.txt)', 0)" 2>/dev/null

# Start mining via IPC
./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "miner.start(1)" 2>/dev/null

# Auto-register as Agent node (gas-free, consensus-layer registration)
sleep 5
RESULT=$(./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "pob.registerNode('ADDR_PLACEHOLDER', 1)" 2>/dev/null)
echo "Agent registration: $RESULT"
SCRIPT

sed -i.bak "s|ADDR_PLACEHOLDER|$ADDR|g; s|ENODE_PLACEHOLDER|$ENODE|g" ~/rydberg-agent/start-bg.sh
rm -f ~/rydberg-agent/start-bg.sh.bak
chmod +x ~/rydberg-agent/start-bg.sh
```

## Step 5: Start and verify

```bash
cd ~/rydberg-agent && ./start-bg.sh
sleep 8
./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "probe.blockNumber"
./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "admin.peers.length"
./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "pob.getNodeRegistrationStatus('$ADDR')"
./gprobe attach ~/rydberg-agent/gprobe.ipc --exec "web3.fromWei(probe.getBalance('$ADDR'), 'probeer')"
```

Verify that `getNodeRegistrationStatus` shows `isAgent: true`. If not (registration not yet included in a block), wait a few more blocks and check again.

## Response Format

Always reply in the user's language (Chinese if Chinese).

Success:
```
Rydberg Agent 节点部署完成

地址: 0x...
类型: Agent (PoB NodeType=1)
区块: #1234
节点: 1 peers
余额: xxx PROBE
Agent注册: isAgent=true, score=5000

节点已自动注册为 Agent，可参与区块同步和 RPC 服务。
Agent 奖励池（每块 40%）将按行为评分比例分配。

查日志: tail -f ~/rydberg-agent/node.log
停节点: kill $(pgrep -f "gprobe.*8004")
```

Failure — report the exact error and suggest fixes:
- "Go not installed" → link to https://go.dev/dl/
- "Port in use" → change --port
- "Permission denied" → chmod +x gprobe

## Sub-Commands

- `/rydberg-agent-node status`:
  ```bash
  ~/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "JSON.stringify({block:probe.blockNumber,peers:admin.peers.length})"
  ```
- `/rydberg-agent-node stop`:
  ```bash
  kill $(pgrep -f "gprobe.*networkid 8004")
  ```
- `/rydberg-agent-node start`:
  ```bash
  cd ~/rydberg-agent && ./start-bg.sh
  ```
- `/rydberg-agent-node logs`:
  ```bash
  tail -30 ~/rydberg-agent/node.log
  ```
- `/rydberg-agent-node balance`:
  ```bash
  ADDR=$(ls ~/rydberg-agent/data/keystore/ | head -1 | grep -oE '[0-9a-f]{40}')
  ~/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "web3.fromWei(probe.getBalance('0x$ADDR'), 'probeer')"
  ```
- `/rydberg-agent-node agent-status`:
  ```bash
  ADDR=$(ls ~/rydberg-agent/data/keystore/ | head -1 | grep -oE '[0-9a-f]{40}')
  ~/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "pob.getNodeRegistrationStatus('0x$ADDR')"
  ~/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "pob.getAgentScores()"
  ~/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "pob.getAgentCount()"
  ```
- `/rydberg-agent-node re-register` (if registration was missed):
  ```bash
  ADDR=$(ls ~/rydberg-agent/data/keystore/ | head -1 | grep -oE '[0-9a-f]{40}')
  ~/rydberg-agent/gprobe attach ~/rydberg-agent/gprobe.ipc --exec "pob.registerNode('0x$ADDR', 1)"
  ```
