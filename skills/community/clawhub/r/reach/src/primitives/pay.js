import { ethers } from 'ethers';
import nodeFetch from 'node-fetch';

// Standard ERC20 ABI — just transfer and balanceOf
const ERC20_ABI = [
  'function transfer(address to, uint256 amount) returns (bool)',
  'function balanceOf(address account) view returns (uint256)',
  'function decimals() view returns (uint8)',
  'function symbol() view returns (string)',
  'function approve(address spender, uint256 amount) returns (bool)',
];

// Known token addresses on Base
const KNOWN_TOKENS = {
  USDC: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  WETH: '0x4200000000000000000000000000000000000006',
  DAI: '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb',
  USDbC: '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6Ca',
};

/**
 * Payment primitive. Sends ETH, ERC-20 tokens, or handles x402 payment flows.
 *
 * @param {string} recipient - ETH address or URL (for x402)
 * @param {string|number} amount - Amount to send (in human units, e.g. '0.01' for ETH)
 * @param {object} options
 * @param {string} options.token - Token symbol ('USDC', 'WETH') or contract address
 * @param {string} options.chain - 'base' (default)
 * @param {string} options.rpc - RPC URL
 * @param {string} options.privateKey - Sender private key (falls back to PRIVATE_KEY env)
 * @param {number} options.decimals - Token decimals (auto-detected if not provided)
 * @param {object} options.x402 - x402 payment options { maxAmount, currency }
 * @returns {object} Payment receipt
 */
export async function pay(recipient, amount, options = {}) {
  const {
    token,
    chain = 'base',
    rpc = process.env.RPC_URL || 'https://mainnet.base.org',
    privateKey = process.env.PRIVATE_KEY || process.env.DEPLOYMENT_KEY,
    x402,
  } = options;

  if (!privateKey) {
    throw new Error('No private key. Set PRIVATE_KEY in .env or pass privateKey option.');
  }

  // x402 payment flow — recipient is a URL
  if (recipient.startsWith('http://') || recipient.startsWith('https://')) {
    return await payX402(recipient, { privateKey, rpc, ...options });
  }

  // Validate address
  if (!ethers.isAddress(recipient)) {
    throw new Error(`Invalid recipient address: ${recipient}`);
  }

  const provider = new ethers.JsonRpcProvider(rpc);
  const wallet = new ethers.Wallet(privateKey, provider);

  // ERC-20 token transfer
  if (token) {
    return await sendToken(wallet, provider, recipient, amount, token, options);
  }

  // Native ETH transfer
  return await sendETH(wallet, recipient, amount);
}

/**
 * Send native ETH.
 */
async function sendETH(wallet, recipient, amount) {
  const value = ethers.parseEther(String(amount));

  console.log(`[pay] Sending ${amount} ETH to ${recipient}`);

  const tx = await wallet.sendTransaction({
    to: recipient,
    value,
  });

  console.log(`[pay] TX sent: ${tx.hash}`);
  const receipt = await tx.wait();

  return {
    success: receipt.status === 1,
    type: 'eth',
    from: wallet.address,
    to: recipient,
    amount: String(amount),
    currency: 'ETH',
    hash: tx.hash,
    blockNumber: receipt.blockNumber,
    gasUsed: receipt.gasUsed.toString(),
  };
}

/**
 * Send ERC-20 token.
 */
async function sendToken(wallet, provider, recipient, amount, token, options) {
  // Resolve token address
  let tokenAddress = token;
  if (KNOWN_TOKENS[token.toUpperCase()]) {
    tokenAddress = KNOWN_TOKENS[token.toUpperCase()];
  }

  if (!ethers.isAddress(tokenAddress)) {
    throw new Error(`Unknown token: ${token}. Pass a contract address or use: ${Object.keys(KNOWN_TOKENS).join(', ')}`);
  }

  const contract = new ethers.Contract(tokenAddress, ERC20_ABI, wallet);

  // Get token info
  let decimals = options.decimals;
  let symbol = token;
  try {
    if (!decimals) decimals = await contract.decimals();
    symbol = await contract.symbol();
  } catch {
    decimals = decimals || 18;
  }

  const parsedAmount = ethers.parseUnits(String(amount), decimals);

  console.log(`[pay] Sending ${amount} ${symbol} to ${recipient}`);

  const tx = await contract.transfer(recipient, parsedAmount);
  console.log(`[pay] TX sent: ${tx.hash}`);
  const receipt = await tx.wait();

  return {
    success: receipt.status === 1,
    type: 'erc20',
    from: wallet.address,
    to: recipient,
    amount: String(amount),
    currency: symbol,
    token: tokenAddress,
    hash: tx.hash,
    blockNumber: receipt.blockNumber,
    gasUsed: receipt.gasUsed.toString(),
  };
}

/**
 * Handle x402 HTTP payment protocol.
 *
 * Flow:
 * 1. GET url → expect 402 response with payment details in headers
 * 2. Build and sign payment authorization
 * 3. Retry request with X-PAYMENT header
 * 4. Return content + receipt
 */
async function payX402(url, options = {}) {
  const {
    privateKey = process.env.PRIVATE_KEY,
    rpc = process.env.RPC_URL || 'https://mainnet.base.org',
    maxAmount,
    headers = {},
  } = options;

  console.log(`[pay] x402 payment flow for: ${url}`);

  // Step 1: GET the URL, expect 402
  const initialResponse = await nodeFetch(url, {
    headers: {
      'User-Agent': 'reach-agent/0.1.0',
      ...headers,
    },
  });

  // If not 402, return the content directly (no payment needed)
  if (initialResponse.status !== 402) {
    const content = await initialResponse.text();
    return {
      success: true,
      type: 'x402',
      paid: false,
      status: initialResponse.status,
      content,
      message: 'No payment required',
    };
  }

  // Step 2: Parse payment requirements from 402 response
  const paymentHeader = initialResponse.headers.get('x-payment') ||
                         initialResponse.headers.get('www-authenticate');
  let paymentBody;
  try {
    paymentBody = await initialResponse.json();
  } catch {
    paymentBody = await initialResponse.text().catch(() => '');
  }

  // Extract payment details
  const paymentDetails = parsePaymentDetails(paymentHeader, paymentBody);

  if (!paymentDetails.amount || !paymentDetails.recipient) {
    return {
      success: false,
      type: 'x402',
      error: 'Could not parse payment details from 402 response',
      paymentHeader,
      paymentBody,
    };
  }

  // Check max amount
  if (maxAmount && parseFloat(paymentDetails.amount) > parseFloat(maxAmount)) {
    return {
      success: false,
      type: 'x402',
      error: `Payment amount ${paymentDetails.amount} exceeds max ${maxAmount}`,
      paymentDetails,
    };
  }

  console.log(`[pay] x402 requires: ${paymentDetails.amount} ${paymentDetails.currency || 'USDC'} to ${paymentDetails.recipient}`);

  // Step 3: Sign payment authorization
  const provider = new ethers.JsonRpcProvider(rpc);
  const wallet = new ethers.Wallet(privateKey, provider);

  // For x402, we sign a payment authorization message
  const authMessage = JSON.stringify({
    version: '1',
    url,
    recipient: paymentDetails.recipient,
    amount: paymentDetails.amount,
    currency: paymentDetails.currency || 'USDC',
    timestamp: Date.now(),
    nonce: Math.random().toString(36).substring(2),
  });

  const signature = await wallet.signMessage(authMessage);

  // Step 4: Retry with payment header
  const paymentPayload = Buffer.from(JSON.stringify({
    authorization: authMessage,
    signature,
    payer: wallet.address,
  })).toString('base64');

  const paidResponse = await nodeFetch(url, {
    headers: {
      'User-Agent': 'reach-agent/0.1.0',
      'X-PAYMENT': paymentPayload,
      ...headers,
    },
  });

  const content = await paidResponse.text();

  return {
    success: paidResponse.ok,
    type: 'x402',
    paid: true,
    status: paidResponse.status,
    amount: paymentDetails.amount,
    currency: paymentDetails.currency || 'USDC',
    recipient: paymentDetails.recipient,
    payer: wallet.address,
    content: paidResponse.ok ? content : undefined,
    error: !paidResponse.ok ? content : undefined,
  };
}

/**
 * Parse payment details from a 402 response.
 */
function parsePaymentDetails(header, body) {
  const details = {};

  // Try body first (usually JSON with payment info)
  if (body && typeof body === 'object') {
    details.amount = body.amount || body.price || body.cost;
    details.recipient = body.recipient || body.address || body.payTo;
    details.currency = body.currency || body.token || 'USDC';
    details.network = body.network || body.chain || 'base';
  }

  // Try header
  if (header) {
    // Common formats: "x402 amount=0.01 recipient=0x... currency=USDC"
    const amountMatch = header.match(/amount[=:]?\s*([\d.]+)/i);
    const recipientMatch = header.match(/(?:recipient|address|payto)[=:]?\s*(0x[a-fA-F0-9]{40})/i);
    const currencyMatch = header.match(/(?:currency|token)[=:]?\s*(\w+)/i);

    if (amountMatch) details.amount = details.amount || amountMatch[1];
    if (recipientMatch) details.recipient = details.recipient || recipientMatch[1];
    if (currencyMatch) details.currency = details.currency || currencyMatch[1];
  }

  return details;
}

export { KNOWN_TOKENS, ERC20_ABI };
