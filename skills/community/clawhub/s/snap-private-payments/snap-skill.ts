import {
  estimateWithdrawalFee,
  formatAssetLabel,
  formatWithdrawalEstimate,
  getShieldedBalance,
  parsePoolAddress,
  parseRecipientAddress,
  type SnapIntegrationContext,
} from "../shared/snap-client";
import { listKnownPools } from "../shared/pools";

/**
 * OpenClaw skill wrapper for SNAP.
 *
 * This file can be pointed to by a Moltbot/OpenClaw agent's
 * skill configuration. It exposes deposit, withdraw, and balance
 * check as natural language commands.
 */
export async function handleCommand(
  command: string,
  context: SnapIntegrationContext
): Promise<string> {
  const normalized = command.trim().toLowerCase();
  const pool = parsePoolAddress(context.poolAddress);

  if (isListPoolsCommand(normalized)) {
    return JSON.stringify(
      {
        pools: listKnownPools(context.poolAddress),
      },
      null,
      2
    );
  }

  if (isDepositCommand(normalized)) {
    const amount = extractAmount(command);
    if (amount === null) {
      throw new Error(
        "SNAP OpenClaw deposit requires an amount, for example: deposit 0.1 SOL into SNAP pool"
      );
    }

    const deposit = await context.snapClient.deposit(pool, amount);
    const poolInfo = await context.snapClient.getPoolInfo(pool);
    return `Deposited ${formatAssetLabel(poolInfo)} into SNAP. Deposit index ${
      deposit.depositIndex
    }.`;
  }

  if (isEstimateCommand(normalized)) {
    const poolInfo = await context.snapClient.getPoolInfo(pool);
    const estimate = await estimateWithdrawalFee(
      context.snapClient,
      pool,
      context.relayerUrl
    );
    return formatWithdrawalEstimate(estimate, poolInfo);
  }

  if (isWithdrawCommand(normalized)) {
    if (!context.note) {
      throw new Error(
        "SNAP OpenClaw withdraw requires a note in context.note before funds can be claimed"
      );
    }

    const recipientAddress =
      extractRecipientAddress(command) ?? context.recipientAddress;
    if (!recipientAddress) {
      throw new Error(
        "SNAP OpenClaw withdraw requires a recipient address in the command or context.recipientAddress"
      );
    }

    if (context.relayerUrl) {
      const result = await context.snapClient.withdrawViaRelayer(
        pool,
        context.note,
        parseRecipientAddress(recipientAddress),
        context.relayerUrl
      );
      return `Withdrew from SNAP to ${recipientAddress} through a relayer. Transaction: ${result.txSignature}. Fee ${result.fee}.`;
    }

    const signature = await context.snapClient.withdraw(
      pool,
      context.note,
      parseRecipientAddress(recipientAddress)
    );
    return `Withdrew from SNAP to ${recipientAddress}. Transaction: ${signature}.`;
  }

  if (isBalanceCommand(normalized)) {
    if (!context.viewingKey) {
      throw new Error(
        "SNAP OpenClaw balance check requires context.viewingKey to inspect shielded funds"
      );
    }

    const balance = await getShieldedBalance(
      context.snapClient,
      pool,
      context.viewingKey
    );
    return `Private SNAP balance: ${balance}.`;
  }

  throw new Error(`SNAP OpenClaw skill does not recognize command: ${command}`);
}

function isListPoolsCommand(command: string): boolean {
  return /(?:list|show).*(?:snap )?pools/i.test(command);
}

function extractAmount(command: string): number | null {
  const match = command.match(/(\d+(?:\.\d+)?)/);
  return match ? Number(match[1]) : null;
}

function extractRecipientAddress(command: string): string | null {
  const match = command.match(/\bto\s+([1-9A-HJ-NP-Za-km-z]{32,})\b/i);
  return match?.[1] ?? null;
}

function isDepositCommand(command: string): boolean {
  return /(?:deposit|shield)/i.test(command);
}

function isWithdrawCommand(command: string): boolean {
  return /(?:withdraw|claim)/i.test(command);
}

function isBalanceCommand(command: string): boolean {
  return /(?:balance|what'?s in my snap pool|show my private balance)/i.test(
    command
  );
}

function isEstimateCommand(command: string): boolean {
  return /(?:estimate|fee|cost)/i.test(command);
}
