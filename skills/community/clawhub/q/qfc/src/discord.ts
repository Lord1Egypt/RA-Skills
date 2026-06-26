import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';
import { QFCFaucet } from './faucet.js';
import { QFCChain } from './chain.js';
import { QFCToken } from './token.js';
import { QFCMinerMonitor } from './miner-monitor.js';

export interface BotCommand {
  command: string;
  args: string[];
}

export interface BotResponse {
  success: boolean;
  message: string;
}

/**
 * QFCDiscordBot — command processor for Discord bot integration.
 *
 * Framework-agnostic: parses command strings and returns formatted responses.
 * Does NOT depend on discord.js — can be used with any Discord bot framework.
 */
export class QFCDiscordBot {
  private network: NetworkName;
  private provider;
  private networkConfig;
  private faucet: QFCFaucet | null;
  private chain: QFCChain;
  private token: QFCToken;
  private minerMonitor: QFCMinerMonitor;

  constructor(network: NetworkName = 'testnet') {
    this.network = network;
    this.networkConfig = getNetworkConfig(network);
    this.provider = createProvider(network);
    this.chain = new QFCChain(network);
    this.token = new QFCToken(network);
    this.minerMonitor = new QFCMinerMonitor(network);
    // Faucet is only available on testnet
    this.faucet = network === 'testnet' ? new QFCFaucet(network) : null;
  }

  /** Parse a raw message like "!faucet 0x1234..." into a BotCommand */
  parseCommand(message: string, prefix: string = '!'): BotCommand | null {
    const trimmed = message.trim();
    if (!trimmed.startsWith(prefix)) return null;

    const withoutPrefix = trimmed.slice(prefix.length);
    const parts = withoutPrefix.split(/\s+/).filter((p) => p.length > 0);
    if (parts.length === 0) return null;

    return {
      command: parts[0].toLowerCase(),
      args: parts.slice(1),
    };
  }

  /** Execute a command and return a formatted response */
  async execute(cmd: BotCommand): Promise<BotResponse> {
    try {
      switch (cmd.command) {
        case 'help':
          return this.cmdHelp();
        case 'faucet':
          return await this.cmdFaucet(cmd.args);
        case 'balance':
          return await this.cmdBalance(cmd.args);
        case 'portfolio':
          return await this.cmdPortfolio(cmd.args);
        case 'tx':
          return await this.cmdTx(cmd.args);
        case 'block':
          return await this.cmdBlock(cmd.args);
        case 'price':
          return await this.cmdPrice();
        case 'miner':
          return await this.cmdMiner(cmd.args);
        case 'info':
          return await this.cmdInfo();
        default:
          return {
            success: false,
            message: `Unknown command \`${cmd.command}\`. Use \`!help\` for available commands.`,
          };
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      return { success: false, message: `**Error:** ${msg}` };
    }
  }

  /** Convenience: parse + execute in one call */
  async handleMessage(message: string, prefix: string = '!'): Promise<BotResponse | null> {
    const cmd = this.parseCommand(message, prefix);
    if (!cmd) return null;
    return this.execute(cmd);
  }

  // ── Command handlers ──────────────────────────────────────────────

  private cmdHelp(): BotResponse {
    const lines = [
      '**QFC Bot Commands**',
      '',
      '`!help` — Show this help message',
      '`!faucet <address>` — Request test QFC (testnet only)',
      '`!balance <address>` — Check QFC balance',
      '`!portfolio <address>` — Show token holdings',
      '`!tx <hash>` — Look up a transaction',
      '`!block [number|latest]` — Get block info',
      '`!price` — Show current gas price',
      '`!miner <address>` — Show miner earnings & status',
      '`!info` — Show network info',
    ];
    return { success: true, message: lines.join('\n') };
  }

  private async cmdFaucet(args: string[]): Promise<BotResponse> {
    if (!this.faucet) {
      return { success: false, message: '**Error:** Faucet is only available on testnet.' };
    }
    if (args.length === 0) {
      return { success: false, message: 'Usage: `!faucet <address>`' };
    }
    const address = args[0];
    if (!ethers.isAddress(address)) {
      return { success: false, message: '**Error:** Invalid address format. Expected `0x` + 40 hex characters.' };
    }

    const result = await this.faucet.requestQFC(address);
    return {
      success: true,
      message: [
        '**Faucet Request Sent**',
        `> **To:** \`${result.to}\``,
        `> **Amount:** ${result.amount} QFC`,
        `> **Tx:** [\`${result.txHash.slice(0, 18)}...\`](${result.explorerUrl})`,
      ].join('\n'),
    };
  }

  private async cmdBalance(args: string[]): Promise<BotResponse> {
    if (args.length === 0) {
      return { success: false, message: 'Usage: `!balance <address>`' };
    }
    const address = args[0];
    if (!ethers.isAddress(address)) {
      return { success: false, message: '**Error:** Invalid address format. Expected `0x` + 40 hex characters.' };
    }

    const balance = await this.provider.getBalance(address);
    const qfc = ethers.formatEther(balance);
    return {
      success: true,
      message: [
        '**QFC Balance**',
        `> **Address:** \`${address}\``,
        `> **Balance:** \`${qfc}\` QFC`,
      ].join('\n'),
    };
  }

  private async cmdPortfolio(args: string[]): Promise<BotResponse> {
    if (args.length === 0) {
      return { success: false, message: 'Usage: `!portfolio <address>`' };
    }
    const address = args[0];
    if (!ethers.isAddress(address)) {
      return { success: false, message: '**Error:** Invalid address format. Expected `0x` + 40 hex characters.' };
    }

    const portfolio = await this.token.getPortfolio(address);
    const lines = [
      `**Portfolio for** \`${address}\``,
      '',
      `**Native QFC:** \`${portfolio.nativeBalance}\` QFC`,
    ];

    if (portfolio.tokens.length > 0) {
      lines.push('', '**ERC-20 Tokens:**');
      for (const t of portfolio.tokens) {
        lines.push(`> **${t.symbol}** (\`${t.name}\`): \`${t.balance}\``);
      }
    } else {
      lines.push('', '*No ERC-20 token holdings found.*');
    }

    return { success: true, message: lines.join('\n') };
  }

  private async cmdTx(args: string[]): Promise<BotResponse> {
    if (args.length === 0) {
      return { success: false, message: 'Usage: `!tx <hash>`' };
    }
    const hash = args[0];

    const tx = await this.chain.getTransaction(hash);
    if (!tx) {
      return { success: false, message: `**Error:** Transaction \`${hash}\` not found.` };
    }

    const explorerUrl = `${this.networkConfig.explorerUrl}/txs/${tx.hash}`;
    return {
      success: true,
      message: [
        '**Transaction Details**',
        `> **Hash:** [\`${tx.hash.slice(0, 18)}...\`](${explorerUrl})`,
        `> **From:** \`${tx.from}\``,
        `> **To:** \`${tx.to ?? 'Contract Creation'}\``,
        `> **Value:** \`${tx.value}\` QFC`,
        `> **Gas Price:** \`${tx.gasPrice}\` gwei`,
        `> **Status:** ${tx.status === 'confirmed' ? '**Confirmed** (block `' + tx.blockNumber + '`)' : '**Pending**'}`,
      ].join('\n'),
    };
  }

  private async cmdBlock(args: string[]): Promise<BotResponse> {
    const blockArg = args.length === 0 ? 'latest' : args[0];
    const blockTag: number | 'latest' =
      blockArg === 'latest' ? 'latest' : parseInt(blockArg, 10);

    if (typeof blockTag === 'number' && isNaN(blockTag)) {
      return { success: false, message: 'Usage: `!block [number|latest]`' };
    }

    const block = await this.chain.getBlock(blockTag);
    const date = new Date(block.timestamp * 1000).toUTCString();
    return {
      success: true,
      message: [
        '**Block Info**',
        `> **Number:** \`${block.number}\``,
        `> **Hash:** \`${block.hash.slice(0, 18)}...\``,
        `> **Time:** ${date}`,
        `> **Miner:** \`${block.miner}\``,
        `> **Transactions:** ${block.transactionCount}`,
        `> **Gas Used:** ${block.gasUsed.toLocaleString()} / ${block.gasLimit.toLocaleString()}`,
      ].join('\n'),
    };
  }

  private async cmdPrice(): Promise<BotResponse> {
    const feeData = await this.provider.getFeeData();
    const gasPrice = feeData.gasPrice
      ? ethers.formatUnits(feeData.gasPrice, 'gwei')
      : 'unknown';
    return {
      success: true,
      message: [
        '**Gas Price**',
        `> **Current:** \`${gasPrice}\` gwei`,
      ].join('\n'),
    };
  }

  private async cmdMiner(args: string[]): Promise<BotResponse> {
    if (args.length === 0) {
      return { success: false, message: 'Usage: `!miner <address>`' };
    }
    const address = args[0];
    if (!ethers.isAddress(address)) {
      return { success: false, message: '**Error:** Invalid address format. Expected `0x` + 40 hex characters.' };
    }

    const status = await this.minerMonitor.getStatus(address);
    const recentEarnings = await this.minerMonitor.getRecentEarnings(address);
    const minerUrl = `${this.networkConfig.explorerUrl}/miner/${address}`;

    const lines = [
      '**⛏️ Miner Status**',
      `> **Address:** [\`${address.slice(0, 10)}...${address.slice(-8)}\`](${minerUrl})`,
      `> **Total Earned:** \`${status.totalEarnedQfc}\` QFC`,
      `> **Available:** \`${ethers.formatEther(BigInt(status.available))}\` QFC`,
      `> **Locked:** \`${ethers.formatEther(BigInt(status.locked))}\` QFC`,
      `> **Score:** ${status.contributionScore}/100`,
      `> **Vesting Tranches:** ${status.activeTranches}`,
    ];

    if (recentEarnings.length > 0) {
      lines.push('', '**Recent Earnings:**');
      for (const e of recentEarnings.slice(0, 5)) {
        lines.push(`> \`${e.rewardQfc}\` QFC — ${e.taskType} (block ${e.blockHeight})`);
      }
      if (recentEarnings.length > 5) {
        lines.push(`> *...and ${recentEarnings.length - 5} more*`);
      }
    }

    return { success: true, message: lines.join('\n') };
  }

  private async cmdInfo(): Promise<BotResponse> {
    const [blockNumber, feeData] = await Promise.all([
      this.provider.getBlockNumber(),
      this.provider.getFeeData(),
    ]);
    const gasPrice = feeData.gasPrice
      ? ethers.formatUnits(feeData.gasPrice, 'gwei')
      : 'unknown';

    return {
      success: true,
      message: [
        '**QFC Network Info**',
        `> **Network:** ${this.networkConfig.name}`,
        `> **Chain ID:** \`${this.networkConfig.chainId}\``,
        `> **Latest Block:** \`${blockNumber}\``,
        `> **Gas Price:** \`${gasPrice}\` gwei`,
        `> **Explorer:** ${this.networkConfig.explorerUrl}`,
        `> **RPC:** \`${this.networkConfig.rpcUrl}\``,
      ].join('\n'),
    };
  }
}
