import { ethers } from 'ethers';

/**
 * Crypto signing primitive.
 *
 * @param {string|object} payload - Message string, transaction object, or typed data
 * @param {object} options
 * @param {string} options.type - 'message' | 'transaction' | 'typed' (default: 'message')
 * @param {string} options.privateKey - Private key (falls back to PRIVATE_KEY env var)
 * @param {string} options.rpc - RPC URL (default: Base mainnet)
 * @returns {object} { signature, address, type }
 */
export async function sign(payload, options = {}) {
  const {
    type = 'message',
    privateKey = process.env.PRIVATE_KEY || process.env.DEPLOYMENT_KEY,
    rpc = process.env.RPC_URL || 'https://mainnet.base.org',
  } = options;

  if (!privateKey) {
    throw new Error('No private key provided. Set PRIVATE_KEY env var or pass privateKey option.');
  }

  const provider = new ethers.JsonRpcProvider(rpc);
  const wallet = new ethers.Wallet(privateKey, provider);
  const address = wallet.address;

  switch (type) {
    case 'message': {
      const signature = await wallet.signMessage(
        typeof payload === 'string' ? payload : JSON.stringify(payload)
      );
      return { signature, address, type: 'message' };
    }

    case 'transaction': {
      if (typeof payload !== 'object') {
        throw new Error('Transaction payload must be an object');
      }
      const tx = await wallet.sendTransaction(payload);
      const receipt = await tx.wait();
      return {
        signature: tx.hash,
        address,
        type: 'transaction',
        hash: tx.hash,
        blockNumber: receipt.blockNumber,
        status: receipt.status === 1 ? 'success' : 'failed',
      };
    }

    case 'typed': {
      // EIP-712 typed data signing
      if (!payload.domain || !payload.types || !payload.value) {
        throw new Error('Typed data requires domain, types, and value');
      }
      const signature = await wallet.signTypedData(
        payload.domain,
        payload.types,
        payload.value
      );
      return { signature, address, type: 'typed' };
    }

    default:
      throw new Error(`Unknown sign type: ${type}`);
  }
}

/**
 * Get wallet address without signing anything.
 */
export function getAddress(privateKey) {
  const key = privateKey || process.env.PRIVATE_KEY || process.env.DEPLOYMENT_KEY;
  if (!key) throw new Error('No private key');
  return new ethers.Wallet(key).address;
}
