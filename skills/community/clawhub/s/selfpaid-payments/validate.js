/**
 * SelfPaid Pre-Signing Validation Layer
 * 
 * Enforces strict local validation on all remotely constructed transactions
 * before they can be forwarded to any wallet signer.
 * 
 * Complies with OpenClaw Security Standard T09 (Safe Transaction Construction).
 */

const ALLOWLIST = {
  chainId: 8453,
  usdc: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913',
  aavePool: '0xa238dd80c259a72e81d7e4664a9801593f98d1c5',
  morphoVault: '0xc1256ae5ff1cf2719d4937adb3bbccab2e00a2ca',
  developerWallet: '0x785cf69ced4e20a7e975a3391d51321b1528fdfe',
  selectors: {
    erc20Transfer: '0xa9059cbb',
    erc20Approve: '0x095ea7b3',
    aaveSupply: '0x617ba037'
  }
};

/**
 * Validates a buildPayment API response against expected parameters.
 * Throws an Error if ANY validation check fails.
 * 
 * @param {Object} buildResponse - Response from POST /api/v1/payment/build
 * @param {Object} expected - { amount, recipient, sender }
 * @returns {Object} { valid: true, summary: Object }
 */
function validatePaymentBatch(buildResponse, expected) {
  if (!buildResponse || !buildResponse.success) {
    throw new Error('Validation failed: response marked as unsuccessful');
  }

  // 1. Enforce Chain ID 8453 (Base Mainnet)
  if (buildResponse.chainId !== ALLOWLIST.chainId) {
    throw new Error(`Validation failed: chainId ${buildResponse.chainId} is not Base (${ALLOWLIST.chainId})`);
  }

  const calls = buildResponse.batchCalls || [];
  if (calls.length !== 4) {
    throw new Error(`Validation failed: expected exactly 4 batch calls, received ${calls.length}`);
  }

  // 2. Enforce zero native-token value on all calls
  for (let i = 0; i < calls.length; i++) {
    if (calls[i].value && calls[i].value !== '0x0' && calls[i].value !== '0') {
      throw new Error(`Validation failed: call ${i + 1} attempts non-zero native ETH transfer: ${calls[i].value}`);
    }
  }

  const norm = addr => (addr || '').toLowerCase();
  const expectedRecipient = norm(expected.recipient);
  const expectedSender = norm(expected.sender);
  const expectedAmountWei = BigInt(Math.round(Number(expected.amount) * 1e6));

  // 3. Recalculate and enforce Developer Fee limits (0.5%, min 0.1 USDC, max 50 USDC)
  let expectedFee = Number(expected.amount) * 0.005;
  if (expectedFee < 0.1) expectedFee = 0.1;
  if (expectedFee > 50.0) expectedFee = 50.0;
  const expectedFeeWei = BigInt(Math.round(expectedFee * 1e6));

  // --- Call 1: Developer Fee Transfer ---
  const call1 = calls[0];
  if (norm(call1.to) !== ALLOWLIST.usdc) {
    throw new Error(`Validation failed: Call 1 target is not USDC contract (${call1.to})`);
  }
  if (!call1.data.startsWith(ALLOWLIST.selectors.erc20Transfer)) {
    throw new Error(`Validation failed: Call 1 selector is not ERC20 transfer`);
  }
  const call1To = '0x' + call1.data.slice(34, 74).toLowerCase();
  const call1Amount = BigInt('0x' + call1.data.slice(74, 138));
  if (call1To !== ALLOWLIST.developerWallet) {
    throw new Error(`Validation failed: Call 1 recipient (${call1To}) does not match developer wallet (${ALLOWLIST.developerWallet})`);
  }
  if (call1Amount !== expectedFeeWei) {
    throw new Error(`Validation failed: Call 1 fee (${call1Amount}) does not match recalculated fee (${expectedFeeWei})`);
  }

  // --- Call 2: Principal Payment Transfer ---
  const call2 = calls[1];
  if (norm(call2.to) !== ALLOWLIST.usdc) {
    throw new Error(`Validation failed: Call 2 target is not USDC contract (${call2.to})`);
  }
  if (!call2.data.startsWith(ALLOWLIST.selectors.erc20Transfer)) {
    throw new Error(`Validation failed: Call 2 selector is not ERC20 transfer`);
  }
  const call2To = '0x' + call2.data.slice(34, 74).toLowerCase();
  const call2Amount = BigInt('0x' + call2.data.slice(74, 138));
  if (call2To !== expectedRecipient) {
    throw new Error(`Validation failed: Call 2 recipient (${call2To}) does not match expected (${expectedRecipient})`);
  }
  if (call2Amount !== expectedAmountWei) {
    throw new Error(`Validation failed: Call 2 amount (${call2Amount}) does not match expected (${expectedAmountWei})`);
  }

  // --- Call 3: Token Approval ---
  const call3 = calls[2];
  if (norm(call3.to) !== ALLOWLIST.usdc) {
    throw new Error(`Validation failed: Call 3 target is not USDC contract (${call3.to})`);
  }
  if (!call3.data.startsWith(ALLOWLIST.selectors.erc20Approve)) {
    throw new Error(`Validation failed: Call 3 selector is not ERC20 approve`);
  }
  const call3Spender = '0x' + call3.data.slice(34, 74).toLowerCase();
  const call3Amount = BigInt('0x' + call3.data.slice(74, 138));
  if (call3Spender !== ALLOWLIST.aavePool && call3Spender !== ALLOWLIST.morphoVault) {
    throw new Error(`Validation failed: Call 3 spender (${call3Spender}) is not an approved yield pool`);
  }
  // Reject infinite / unlimited approvals
  const maxUint = BigInt('0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff');
  if (call3Amount === maxUint) {
    throw new Error(`Validation failed: Unlimited approval is strictly rejected`);
  }

  // --- Call 4: Supply Collateral to Yield Pool ---
  const call4 = calls[3];
  const poolTarget = norm(call4.to);
  if (poolTarget !== ALLOWLIST.aavePool && poolTarget !== ALLOWLIST.morphoVault) {
    throw new Error(`Validation failed: Call 4 target (${poolTarget}) is not an approved yield pool`);
  }
  // Enforce Call 3 approved spender strictly equals Call 4 destination
  if (call3Spender !== poolTarget) {
    throw new Error(`Validation failed: Call 3 spender (${call3Spender}) does not match Call 4 target (${poolTarget})`);
  }

  // Validate Call 4 calldata based on protocol
  if (poolTarget === ALLOWLIST.aavePool) {
    if (!call4.data.startsWith(ALLOWLIST.selectors.aaveSupply)) {
      throw new Error(`Validation failed: Call 4 does not use Aave V3 supply selector (${ALLOWLIST.selectors.aaveSupply})`);
    }
    const asset = '0x' + call4.data.slice(34, 74).toLowerCase();
    const supplyAmount = BigInt('0x' + call4.data.slice(74, 138));
    const onBehalfOf = '0x' + call4.data.slice(162, 202).toLowerCase();

    if (asset !== ALLOWLIST.usdc) {
      throw new Error(`Validation failed: Aave supply asset is not USDC (${asset})`);
    }
    if (supplyAmount !== call3Amount) {
      throw new Error(`Validation failed: Aave supply amount (${supplyAmount}) does not match approved amount (${call3Amount})`);
    }
    if (onBehalfOf !== expectedSender) {
      throw new Error(`Validation failed: Aave supply onBehalfOf (${onBehalfOf}) does not match sender (${expectedSender})`);
    }
  } else if (poolTarget === ALLOWLIST.morphoVault) {
    if (!call4.data.startsWith(ALLOWLIST.selectors.morphoDeposit || '0x6e553f65')) {
      throw new Error(`Validation failed: Call 4 does not use Morpho deposit selector (0x6e553f65)`);
    }
    const depositAmount = BigInt('0x' + call4.data.slice(10, 74));
    const receiver = '0x' + call4.data.slice(98, 138).toLowerCase();

    if (depositAmount !== call3Amount) {
      throw new Error(`Validation failed: Morpho deposit amount (${depositAmount}) does not match approved amount (${call3Amount})`);
    }
    if (receiver !== expectedSender) {
      throw new Error(`Validation failed: Morpho deposit receiver (${receiver}) does not match sender (${expectedSender})`);
    }
  }

  return {
    valid: true,
    summary: {
      chainId: ALLOWLIST.chainId,
      recipient: expectedRecipient,
      paymentAmountUSDC: Number(expected.amount),
      developerFeeUSDC: expectedFee,
      collateralDepositUSDC: Number(buildResponse.summary.yieldDepositAmount),
      estimatedRecoveryDays: buildResponse.summary.estimatedRecoveryDays,
      protocol: buildResponse.summary.protocol
    }
  };
}

module.exports = { validatePaymentBatch, ALLOWLIST };
