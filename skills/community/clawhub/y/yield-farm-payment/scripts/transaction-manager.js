#!/usr/bin/env node

/**
 * Professional Transaction Manager for YieldFarmPayment
 * Handles all blockchain interactions with retry, gas optimization, and error recovery
 */

const { createWalletClient, createPublicClient, http, parseGwei } = require('viem');
const { base } = require('viem/chains');

class TransactionManager {
  constructor(config) {
    this.walletClient = config.walletClient;
    this.publicClient = config.publicClient;
    this.account = config.account;
    this.logger = config.logger || console;
    
    // Default settings
    this.settings = {
      maxRetries: 3,
      initialGasPrice: parseGwei('0.05'),
      maxGasPrice: parseGwei('0.5'),
      gasPriceMultiplier: 1.5,
      retryDelayMs: 2000,
      timeoutSeconds: 180,
      ...config.settings
    };
  }

  /**
   * Execute a contract write with retry logic
   */
  async executeContractWrite(contractConfig) {
    const {
      address,
      abi,
      functionName,
      args,
      value = 0n,
      gasPrice = this.settings.initialGasPrice,
      retryCount = 0
    } = contractConfig;

    try {
      this.logger.log(`📝 Executing ${functionName} (attempt ${retryCount + 1})...`);

      const hash = await this.walletClient.writeContract({
        address,
        abi,
        functionName,
        args,
        value,
        account: this.account,
        maxPriorityFeePerGas: gasPrice,
        maxFeePerGas: gasPrice * 2n
      });

      this.logger.log(`✅ Transaction sent: ${hash.substring(0, 16)}...`);

      // Wait for confirmation with timeout
      const receipt = await Promise.race([
        this.publicClient.waitForTransactionReceipt({ hash }),
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Transaction timeout')), this.settings.timeoutSeconds * 1000)
        )
      ]);

      this.logger.log(`✅ Transaction confirmed in block ${receipt.blockNumber}`);
      return { success: true, hash, receipt };

    } catch (error) {
      // Handle specific errors
      const errorMessage = error.message || error.toString();
      
      if (errorMessage.includes('replacement transaction underpriced')) {
        return await this.handleUnderpricedError(contractConfig, error, retryCount);
      }
      
      if (errorMessage.includes('insufficient funds')) {
        this.logger.error('❌ Insufficient funds for transaction');
        return { success: false, error: 'INSUFFICIENT_FUNDS', details: errorMessage };
      }
      
      if (errorMessage.includes('nonce too low')) {
        return await this.handleNonceError(contractConfig, error, retryCount);
      }

      // Generic retry logic
      if (retryCount < this.settings.maxRetries) {
        this.logger.log(`⚠️ Retrying ${functionName} (${retryCount + 1}/${this.settings.maxRetries})...`);
        await this.delay(this.settings.retryDelayMs * (retryCount + 1));
        
        return await this.executeContractWrite({
          ...contractConfig,
          gasPrice: this.increaseGasPrice(gasPrice),
          retryCount: retryCount + 1
        });
      }

      this.logger.error(`❌ Failed after ${this.settings.maxRetries} retries: ${errorMessage}`);
      return { success: false, error: 'MAX_RETRIES_EXCEEDED', details: errorMessage };
    }
  }

  /**
   * Handle 'replacement transaction underpriced' error
   */
  async handleUnderpricedError(contractConfig, originalError, retryCount) {
    this.logger.log('⚠️ Replacement transaction underpriced - increasing gas price...');
    
    if (retryCount < this.settings.maxRetries) {
      const increasedGasPrice = this.increaseGasPrice(contractConfig.gasPrice);
      
      if (increasedGasPrice > this.settings.maxGasPrice) {
        this.logger.error(`❌ Gas price too high (${increasedGasPrice} > ${this.settings.maxGasPrice})`);
        return { success: false, error: 'GAS_PRICE_TOO_HIGH', details: originalError.message };
      }

      await this.delay(this.settings.retryDelayMs);
      
      return await this.executeContractWrite({
        ...contractConfig,
        gasPrice: increasedGasPrice,
        retryCount: retryCount + 1
      });
    }

    this.logger.error('❌ Max retries reached for underpriced transaction');
    return { success: false, error: 'UNDERPRICED_MAX_RETRIES', details: originalError.message };
  }

  /**
   * Handle nonce-related errors
   */
  async handleNonceError(contractConfig, originalError, retryCount) {
    this.logger.log('⚠️ Nonce error - fetching latest nonce...');
    
    try {
      const latestNonce = await this.publicClient.getTransactionCount({
        address: this.account.address,
        blockTag: 'latest'
      });

      this.logger.log(`📊 Latest nonce: ${latestNonce}`);
      
      // We could implement nonce management here
      // For now, just retry with delay
      if (retryCount < this.settings.maxRetries) {
        await this.delay(this.settings.retryDelayMs * 2);
        return await this.executeContractWrite({
          ...contractConfig,
          retryCount: retryCount + 1
        });
      }

    } catch (error) {
      this.logger.error(`❌ Failed to handle nonce error: ${error.message}`);
    }

    return { success: false, error: 'NONCE_ERROR', details: originalError.message };
  }

  /**
   * Increase gas price for retry
   */
  increaseGasPrice(currentGasPrice) {
    const increased = currentGasPrice * BigInt(Math.floor(this.settings.gasPriceMultiplier * 100)) / 100n;
    return increased > this.settings.maxGasPrice ? this.settings.maxGasPrice : increased;
  }

  /**
   * Utility delay function
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Get current gas price from network
   */
  async getCurrentGasPrice() {
    try {
      const gasPrice = await this.publicClient.getGasPrice();
      this.logger.log(`⛽ Current network gas price: ${gasPrice / 1_000_000_000n} Gwei`);
      return gasPrice;
    } catch (error) {
      this.logger.log(`⚠️ Could not fetch gas price, using default: ${error.message}`);
      return this.settings.initialGasPrice;
    }
  }

  /**
   * Check if wallet has sufficient funds for transaction
   */
  async checkBalance(estimatedCost) {
    try {
      const balance = await this.publicClient.getBalance({ address: this.account.address });
      const hasFunds = balance >= estimatedCost;
      
      if (!hasFunds) {
        this.logger.error(`❌ Insufficient balance: ${balance / 1_000_000_000_000_000_000n} ETH < ${estimatedCost / 1_000_000_000_000_000_000n} ETH needed`);
      }
      
      return hasFunds;
    } catch (error) {
      this.logger.error(`❌ Failed to check balance: ${error.message}`);
      return false;
    }
  }
}

module.exports = { TransactionManager };