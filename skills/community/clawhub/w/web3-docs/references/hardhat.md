# Hardhat Reference

Hardhat is the most popular Ethereum development framework for TypeScript-first teams. Use it when you want mature plugin ecosystem, built-in TypeScript support, and Hardhat Ignition for deployment management.

## Installation

```bash
mkdir my-project && cd my-project
npm init -y
npm install --save-dev hardhat
npx hardhat init
# Choose: Create a TypeScript project
```

This installs `hardhat-toolbox` (ethers.js v6, chai, waffle/viem, gas reporter, coverage).

## Project Structure

```
my-project/
├── contracts/
│   └── MyToken.sol
├── ignition/
│   └── modules/
│       └── MyToken.ts      ← deployment modules (recommended)
├── scripts/
│   └── deploy.ts           ← manual deploy scripts (optional)
├── test/
│   └── MyToken.ts
├── hardhat.config.ts       ← main config
├── package.json
└── .env                    ← RPC URLs, private keys (never commit)
```

## hardhat.config.ts

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";
dotenv.config();

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: { enabled: true, runs: 200 },
    },
  },
  networks: {
    // Local fork
    hardhat: {
      forking: {
        url: process.env.OPTIMISM_RPC_URL || "https://mainnet.optimism.io",
        // blockNumber: 12345678,  // pin for deterministic tests
      },
    },
    // Live networks — set RPC + private key in .env
    optimism: {
      url: process.env.OPTIMISM_RPC_URL || "https://mainnet.optimism.io",
      accounts: process.env.DEPLOYER_PRIVATE_KEY ? [process.env.DEPLOYER_PRIVATE_KEY] : [],
      chainId: 10,
    },
    base: {
      url: process.env.BASE_RPC_URL || "https://mainnet.base.org",
      accounts: process.env.DEPLOYER_PRIVATE_KEY ? [process.env.DEPLOYER_PRIVATE_KEY] : [],
      chainId: 8453,
    },
  },
  etherscan: {
    apiKey: {
      optimisticEthereum: process.env.OPTIMISM_ETHERSCAN_API_KEY || "",
      base: process.env.BASE_ETHERSCAN_API_KEY || "",
    },
    customChains: [
      {
        network: "base",
        chainId: 8453,
        urls: {
          apiURL: "https://api.basescan.org/api",
          browserURL: "https://basescan.org",
        },
      },
    ],
  },
  gasReporter: {
    enabled: process.env.REPORT_GAS === "true",
    currency: "USD",
  },
};

export default config;
```

## Core Commands

```bash
npx hardhat compile                   # Compile contracts
npx hardhat test                      # Run all tests
npx hardhat test --grep "transfer"   # Run specific tests
npx hardhat coverage                  # Coverage report (requires solidity-coverage)
npx hardhat node                      # Start local Hardhat Network (port 8545)
npx hardhat console --network localhost  # Interactive console

# Deploy with Ignition
npx hardhat ignition deploy ignition/modules/MyToken.ts --network optimism

# Deploy with script
npx hardhat run scripts/deploy.ts --network base

# Verify on Etherscan/Basescan
npx hardhat verify --network optimism 0xYOUR_CONTRACT_ADDRESS "Constructor" "Args"
npx hardhat verify --network base 0xYOUR_CONTRACT_ADDRESS
```

## Writing Tests (ethers.js v6 + chai)

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { MyToken } from "../typechain-types";

describe("MyToken", function () {
  let token: MyToken;
  let owner: any;
  let addr1: any;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();

    const MyTokenFactory = await ethers.getContractFactory("MyToken");
    token = await MyTokenFactory.deploy(ethers.parseEther("1000000")) as MyToken;
    await token.waitForDeployment();
  });

  it("should assign total supply to owner", async function () {
    const ownerBalance = await token.balanceOf(owner.address);
    expect(await token.totalSupply()).to.equal(ownerBalance);
  });

  it("should transfer tokens between accounts", async function () {
    await token.transfer(addr1.address, ethers.parseEther("50"));
    expect(await token.balanceOf(addr1.address)).to.equal(ethers.parseEther("50"));
  });

  it("should revert with insufficient balance", async function () {
    await expect(
      token.connect(addr1).transfer(owner.address, ethers.parseEther("1"))
    ).to.be.revertedWith("ERC20InsufficientBalance");
  });

  it("should emit Transfer event", async function () {
    await expect(token.transfer(addr1.address, ethers.parseEther("10")))
      .to.emit(token, "Transfer")
      .withArgs(owner.address, addr1.address, ethers.parseEther("10"));
  });
});
```

## Hardhat Ignition Deployment

Ignition is the recommended deployment system (replaces scripts/ for complex deployments):

```typescript
// ignition/modules/MyToken.ts
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";
import { parseEther } from "viem";

const MyTokenModule = buildModule("MyTokenModule", (m) => {
  const initialSupply = m.getParameter("initialSupply", parseEther("1000000").toString());
  const token = m.contract("MyToken", [initialSupply]);
  return { token };
});

export default MyTokenModule;
```

```bash
npx hardhat ignition deploy ignition/modules/MyToken.ts \
  --network optimism \
  --parameters '{"MyTokenModule": {"initialSupply": "1000000000000000000000000"}}'
```

## Manual Deploy Script

```typescript
// scripts/deploy.ts
import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  console.log("Balance:", ethers.formatEther(await deployer.provider.getBalance(deployer.address)));

  const MyToken = await ethers.getContractFactory("MyToken");
  const token = await MyToken.deploy(ethers.parseEther("1000000"));
  await token.waitForDeployment();

  console.log("MyToken deployed to:", await token.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

## Common Plugins

```bash
# Included in hardhat-toolbox:
# - ethers.js v6
# - chai assertions
# - TypeChain (generates TypeScript types from ABIs)
# - hardhat-gas-reporter
# - solidity-coverage
# - hardhat-etherscan

# Additional useful plugins:
npm install --save-dev @openzeppelin/hardhat-upgrades   # Upgradeable contracts
npm install --save-dev hardhat-deploy                   # Deployment management
npm install --save-dev @nomicfoundation/hardhat-foundry # Use Foundry alongside Hardhat
```

## TypeChain (Auto-generated Types)

After `npx hardhat compile`, TypeChain generates type-safe contract interfaces in `typechain-types/`:

```typescript
import { MyToken, MyToken__factory } from "../typechain-types";

const token: MyToken = await ethers.getContractAt("MyToken", "0x...");
// token.transfer() is now fully typed — args and return values
```

## .env Setup

```bash
DEPLOYER_PRIVATE_KEY=0x...
OPTIMISM_RPC_URL=https://opt-mainnet.g.alchemy.com/v2/YOUR_KEY
BASE_RPC_URL=https://base-mainnet.g.alchemy.com/v2/YOUR_KEY
OPTIMISM_ETHERSCAN_API_KEY=...
BASE_ETHERSCAN_API_KEY=...
REPORT_GAS=true
```

## Gotchas

- `waitForDeployment()` replaces the old `deployed()` — use for ethers.js v6
- `getAddress()` replaces `.address` for contract instances in ethers.js v6
- Hardhat Network always mines a block per transaction by default — set `mining.auto: false` for interval mining
- Use `loadFixture` from `@nomicfoundation/hardhat-toolbox/network-helpers` for fast test isolation
- `forking` on mainnet: set `HARDHAT_FORK_URL` or `forking.url` in config — uses Alchemy/Infura
