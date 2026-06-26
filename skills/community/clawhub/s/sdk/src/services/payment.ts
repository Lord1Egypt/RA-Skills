import {
  Connection,
  Keypair,
  PublicKey,
  Transaction,
  sendAndConfirmTransaction,
} from '@solana/web3.js';
import {
  createTransferInstruction,
  getAssociatedTokenAddress,
  getAccount,
  TOKEN_PROGRAM_ID,
} from '@solana/spl-token';
import type { ResolvedConfig, WalletAdapter, BalanceResult } from '../types';
import {
  TREASURY_WALLET,
  USDC_MINT,
  USDC_DECIMALS,
  PRICE_USDC,
  PRICE_USDC_RAW,
  X402_VERSION,
  SOLANA_NETWORK,
} from '../constants';
import {
  WalletNotConfiguredError,
  InsufficientBalanceError,
  NetworkError,
} from '../utils/errors';

/**
 * x402 payment proof structure
 */
interface X402PaymentProof {
  x402Version: number;
  network: string;
  payload: {
    signature: string;
    payer: string;
  };
}

/**
 * Payment service for handling USDC transfers via x402
 */
export class PaymentService {
  private connection: Connection;
  private usdcMint: PublicKey;
  private treasuryWallet: PublicKey;

  constructor(private config: ResolvedConfig) {
    this.connection = new Connection(config.rpcEndpoint, 'confirmed');
    this.usdcMint = new PublicKey(USDC_MINT);
    this.treasuryWallet = new PublicKey(TREASURY_WALLET);
  }

  /**
   * Check if a wallet is configured
   */
  hasWallet(): boolean {
    return this.config.wallet !== null;
  }

  /**
   * Get the public key of the configured wallet
   */
  getPublicKey(): PublicKey {
    if (!this.config.wallet) {
      throw new WalletNotConfiguredError();
    }

    if ('publicKey' in this.config.wallet && this.config.wallet.publicKey instanceof PublicKey) {
      return this.config.wallet.publicKey;
    }

    // Keypair
    return (this.config.wallet as Keypair).publicKey;
  }

  /**
   * Check USDC and SOL balance
   */
  async checkBalance(): Promise<BalanceResult> {
    const publicKey = this.getPublicKey();

    try {
      // Get SOL balance
      const solBalance = await this.connection.getBalance(publicKey);
      const sol = solBalance / 1e9; // Convert lamports to SOL

      // Get USDC token account
      const usdcAta = await getAssociatedTokenAddress(this.usdcMint, publicKey);

      let usdc = 0;
      try {
        const tokenAccount = await getAccount(this.connection, usdcAta);
        usdc = Number(tokenAccount.amount) / Math.pow(10, USDC_DECIMALS);
      } catch {
        // Token account doesn't exist, balance is 0
        usdc = 0;
      }

      return {
        usdc,
        sol,
        sufficient: usdc >= PRICE_USDC,
      };
    } catch (error) {
      throw new NetworkError(
        'Failed to check balance',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Send USDC payment to treasury
   * Returns the transaction signature
   */
  async sendPayment(): Promise<string> {
    if (!this.config.wallet) {
      throw new WalletNotConfiguredError();
    }

    const publicKey = this.getPublicKey();

    // Check balance first
    const balance = await this.checkBalance();
    if (!balance.sufficient) {
      throw new InsufficientBalanceError(PRICE_USDC, balance.usdc);
    }

    try {
      // Get token accounts
      const senderAta = await getAssociatedTokenAddress(this.usdcMint, publicKey);
      const recipientAta = await getAssociatedTokenAddress(this.usdcMint, this.treasuryWallet);

      // Create transfer instruction
      const transferInstruction = createTransferInstruction(
        senderAta,
        recipientAta,
        publicKey,
        BigInt(PRICE_USDC_RAW),
        [],
        TOKEN_PROGRAM_ID
      );

      // Build transaction
      const transaction = new Transaction().add(transferInstruction);
      const { blockhash, lastValidBlockHeight } = await this.connection.getLatestBlockhash();
      transaction.recentBlockhash = blockhash;
      transaction.feePayer = publicKey;

      // Sign and send
      let signature: string;

      if (this.config.wallet instanceof Keypair) {
        // Keypair - use sendAndConfirmTransaction
        signature = await sendAndConfirmTransaction(
          this.connection,
          transaction,
          [this.config.wallet]
        );
      } else {
        // Wallet adapter
        const wallet = this.config.wallet as WalletAdapter;
        const signedTx = await wallet.signTransaction(transaction);
        signature = await this.connection.sendRawTransaction(signedTx.serialize());

        // Wait for confirmation
        await this.connection.confirmTransaction({
          signature,
          blockhash,
          lastValidBlockHeight,
        });
      }

      if (this.config.debug) {
        console.log(`[EdgeBets] Payment sent: ${signature}`);
      }

      return signature;
    } catch (error) {
      throw new NetworkError(
        'Failed to send USDC payment',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Build x402 payment proof header value
   */
  buildPaymentProof(signature: string): string {
    const proof: X402PaymentProof = {
      x402Version: X402_VERSION,
      network: SOLANA_NETWORK,
      payload: {
        signature,
        payer: this.getPublicKey().toBase58(),
      },
    };

    return Buffer.from(JSON.stringify(proof)).toString('base64');
  }

  /**
   * Get the treasury wallet address
   */
  getTreasuryWallet(): string {
    return TREASURY_WALLET;
  }

  /**
   * Get the simulation price in USDC
   */
  getPrice(): number {
    return PRICE_USDC;
  }
}
