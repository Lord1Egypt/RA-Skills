import { ethers } from 'ethers';
import { NetworkName, createProvider } from './provider.js';

export interface EventSubscription {
  stop: () => void;
}

export interface TransferEvent {
  blockNumber: number;
  txHash: string;
  from: string;
  to: string;
  value: string;
}

export interface SwapEvent {
  blockNumber: number;
  txHash: string;
  user: string;
  tokenIn: string;
  amountIn: string;
  tokenOut: string;
  amountOut: string;
}

export interface BlockEvent {
  number: number;
  hash: string;
  timestamp: number;
  transactions: number;
}

/**
 * QFCEvents — Watch for on-chain events via polling.
 * QFC doesn't support WebSocket subscriptions, so we poll for new blocks/logs.
 */
export class QFCEvents {
  private provider: ethers.JsonRpcProvider;

  constructor(network: NetworkName = 'testnet') {
    this.provider = createProvider(network);
  }

  /**
   * Watch ERC-20 Transfer events for a token.
   * @param tokenAddress - ERC-20 token contract
   * @param callback - called for each new Transfer event
   * @param intervalMs - polling interval (default 5000ms)
   */
  watchTransfers(
    tokenAddress: string,
    callback: (event: TransferEvent) => void,
    intervalMs: number = 5000,
  ): EventSubscription {
    const transferTopic = ethers.id('Transfer(address,address,uint256)');
    let lastBlock = 0;
    let stopped = false;

    const poll = async () => {
      while (!stopped) {
        try {
          const currentBlock = await this.provider.getBlockNumber();
          if (lastBlock === 0) {
            lastBlock = currentBlock;
            await new Promise((r) => setTimeout(r, intervalMs));
            continue;
          }

          if (currentBlock > lastBlock) {
            const logs = await this.provider.send('eth_getLogs', [{
              address: tokenAddress,
              topics: [transferTopic],
              fromBlock: `0x${(lastBlock + 1).toString(16)}`,
              toBlock: `0x${currentBlock.toString(16)}`,
            }]);

            for (const log of logs) {
              const from = '0x' + log.topics[1].slice(26);
              const to = '0x' + log.topics[2].slice(26);
              const value = BigInt(log.data).toString();
              callback({
                blockNumber: parseInt(log.blockNumber, 16),
                txHash: log.transactionHash,
                from,
                to,
                value,
              });
            }
            lastBlock = currentBlock;
          }
        } catch {
          // Ignore polling errors, retry next interval
        }
        await new Promise((r) => setTimeout(r, intervalMs));
      }
    };

    poll();
    return { stop: () => { stopped = true; } };
  }

  /**
   * Watch Swap events on an AMM pool.
   * @param poolAddress - SimpleSwap pool contract
   * @param callback - called for each new Swap event
   * @param intervalMs - polling interval (default 5000ms)
   */
  watchSwaps(
    poolAddress: string,
    callback: (event: SwapEvent) => void,
    intervalMs: number = 5000,
  ): EventSubscription {
    const swapTopic = ethers.id('Swap(address,address,uint256,address,uint256)');
    let lastBlock = 0;
    let stopped = false;

    const poll = async () => {
      while (!stopped) {
        try {
          const currentBlock = await this.provider.getBlockNumber();
          if (lastBlock === 0) {
            lastBlock = currentBlock;
            await new Promise((r) => setTimeout(r, intervalMs));
            continue;
          }

          if (currentBlock > lastBlock) {
            const logs = await this.provider.send('eth_getLogs', [{
              address: poolAddress,
              topics: [swapTopic],
              fromBlock: `0x${(lastBlock + 1).toString(16)}`,
              toBlock: `0x${currentBlock.toString(16)}`,
            }]);

            for (const log of logs) {
              const user = '0x' + log.topics[1].slice(26);
              const iface = new ethers.Interface([
                'event Swap(address indexed user, address tokenIn, uint256 amountIn, address tokenOut, uint256 amountOut)',
              ]);
              const decoded = iface.decodeEventLog('Swap', log.data, log.topics);
              callback({
                blockNumber: parseInt(log.blockNumber, 16),
                txHash: log.transactionHash,
                user,
                tokenIn: decoded.tokenIn,
                amountIn: decoded.amountIn.toString(),
                tokenOut: decoded.tokenOut,
                amountOut: decoded.amountOut.toString(),
              });
            }
            lastBlock = currentBlock;
          }
        } catch {
          // Ignore polling errors
        }
        await new Promise((r) => setTimeout(r, intervalMs));
      }
    };

    poll();
    return { stop: () => { stopped = true; } };
  }

  /**
   * Watch for new blocks.
   * @param callback - called for each new block
   * @param intervalMs - polling interval (default 5000ms)
   */
  watchBlocks(
    callback: (event: BlockEvent) => void,
    intervalMs: number = 5000,
  ): EventSubscription {
    let lastBlock = 0;
    let stopped = false;

    const poll = async () => {
      while (!stopped) {
        try {
          const currentBlock = await this.provider.getBlockNumber();
          if (lastBlock === 0) {
            lastBlock = currentBlock - 1;
          }

          for (let i = lastBlock + 1; i <= currentBlock; i++) {
            const block = await this.provider.send('eth_getBlockByNumber', [
              `0x${i.toString(16)}`,
              false,
            ]);
            if (block) {
              callback({
                number: i,
                hash: block.hash,
                timestamp: parseInt(block.timestamp, 16),
                transactions: block.transactions?.length ?? 0,
              });
            }
          }
          lastBlock = currentBlock;
        } catch {
          // Ignore polling errors
        }
        await new Promise((r) => setTimeout(r, intervalMs));
      }
    };

    poll();
    return { stop: () => { stopped = true; } };
  }

  /**
   * Watch NFT marketplace sale events.
   * @param marketplaceAddress - NFTMarketplace contract
   * @param callback - called for each Sold event
   * @param intervalMs - polling interval (default 5000ms)
   */
  watchNFTSales(
    marketplaceAddress: string,
    callback: (event: { listingId: number; buyer: string; seller: string; price: string; blockNumber: number; txHash: string }) => void,
    intervalMs: number = 5000,
  ): EventSubscription {
    const soldTopic = ethers.id('Sold(uint256,address,address,uint256)');
    let lastBlock = 0;
    let stopped = false;

    const poll = async () => {
      while (!stopped) {
        try {
          const currentBlock = await this.provider.getBlockNumber();
          if (lastBlock === 0) {
            lastBlock = currentBlock;
            await new Promise((r) => setTimeout(r, intervalMs));
            continue;
          }

          if (currentBlock > lastBlock) {
            const logs = await this.provider.send('eth_getLogs', [{
              address: marketplaceAddress,
              topics: [soldTopic],
              fromBlock: `0x${(lastBlock + 1).toString(16)}`,
              toBlock: `0x${currentBlock.toString(16)}`,
            }]);

            for (const log of logs) {
              const listingId = Number(BigInt(log.topics[1]));
              const buyer = '0x' + log.topics[2].slice(26);
              const seller = '0x' + log.topics[3].slice(26);
              const price = ethers.formatEther(BigInt(log.data));
              callback({
                listingId,
                buyer,
                seller,
                price,
                blockNumber: parseInt(log.blockNumber, 16),
                txHash: log.transactionHash,
              });
            }
            lastBlock = currentBlock;
          }
        } catch {
          // Ignore polling errors
        }
        await new Promise((r) => setTimeout(r, intervalMs));
      }
    };

    poll();
    return { stop: () => { stopped = true; } };
  }
}
