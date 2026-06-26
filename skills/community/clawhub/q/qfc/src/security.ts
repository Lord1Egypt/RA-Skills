interface TransactionCheck {
  to: string;
  amount: number;
  isContractCall?: boolean;
}

interface CheckResult {
  approved: boolean;
  requiresConfirmation: boolean;
  warnings: string[];
}

interface SecurityConfig {
  dailyLimit: number;
  autoApproveBelow: number;
  requireConfirmAlways: boolean;
}

const DEFAULT_CONFIG: SecurityConfig = {
  dailyLimit: 1000,
  autoApproveBelow: 10,
  requireConfirmAlways: false,
};

/**
 * SecurityPolicy — pre-transaction safety checks for wallet operations.
 */
export class SecurityPolicy {
  private config: SecurityConfig;
  private dailySpent: number = 0;
  private knownAddresses: Set<string> = new Set();

  constructor(config?: Partial<SecurityConfig>) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /** Mark an address as known/trusted */
  addKnownAddress(address: string): void {
    this.knownAddresses.add(address.toLowerCase());
  }

  /** Run pre-transaction checks */
  preTransactionCheck(tx: TransactionCheck): CheckResult {
    // Rule 1: Validate address format first — reject before any other processing
    if (tx.to.includes(' ') || tx.to.length !== 42 || !tx.to.startsWith('0x')) {
      return {
        approved: false,
        requiresConfirmation: false,
        warnings: ['Invalid address format — possible injection attempt'],
      };
    }

    const warnings: string[] = [];
    let requiresConfirmation = this.config.requireConfirmAlways;

    // Rule 2: Large transaction (>100 QFC)
    if (tx.amount > 100) {
      warnings.push(`Large transaction: ${tx.amount} QFC exceeds 100 QFC threshold`);
      requiresConfirmation = true;
    }

    // Rule 3: New/unknown address
    if (!this.knownAddresses.has(tx.to.toLowerCase())) {
      warnings.push(`New recipient address: ${tx.to} (not previously used)`);
      if (tx.amount > this.config.autoApproveBelow) {
        requiresConfirmation = true;
      }
    }

    // Rule 4: Contract call
    if (tx.isContractCall) {
      warnings.push('Transaction involves a contract call');
      requiresConfirmation = true;
    }

    // Rule 5: Daily spending limit
    if (this.dailySpent + tx.amount > this.config.dailyLimit) {
      warnings.push(
        `Daily limit: spending ${this.dailySpent + tx.amount} QFC exceeds ${this.config.dailyLimit} QFC daily limit`,
      );
      requiresConfirmation = true;
    }

    // Auto-approve small transactions to known addresses
    const approved =
      !requiresConfirmation &&
      tx.amount <= this.config.autoApproveBelow &&
      this.knownAddresses.has(tx.to.toLowerCase());

    return { approved, requiresConfirmation, warnings };
  }

  /** Record a completed transaction toward the daily limit */
  recordTransaction(amount: number): void {
    this.dailySpent += amount;
  }

  /** Reset daily spending counter */
  resetDailySpent(): void {
    this.dailySpent = 0;
  }
}
