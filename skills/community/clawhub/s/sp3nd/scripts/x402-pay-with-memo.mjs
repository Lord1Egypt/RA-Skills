/**
 * SP3ND Agent Payment — lifecycle-safe x402 example
 *
 * Server-priced cart → idempotent order → review/quote gate →
 * shipping selection (when required) → server-issued x402 payment → tracking
 *
 * This example intentionally stops before payment whenever an order is still
 * under review, its quote is stale, or a shipping option still needs selection.
 */

import 'dotenv/config';
import {
  ComputeBudgetProgram,
  Connection,
  Keypair,
  PublicKey,
  TransactionMessage,
  VersionedTransaction,
} from '@solana/web3.js';
import {
  createTransferCheckedInstruction,
  getAssociatedTokenAddress,
} from '@solana/spl-token';
import { createMemoInstruction } from '@solana/spl-memo';
import { readFileSync } from 'fs';

const required = (name) => {
  const value = process.env[name]?.trim();
  if (!value) {
    console.error(`Missing required env var: ${name}`);
    process.exit(1);
  }
  return value;
};

const parsePositiveInteger = (name, fallback) => {
  const value = Number(process.env[name] ?? fallback);
  if (!Number.isInteger(value) || value < 0) {
    throw new Error(`${name} must be a non-negative integer`);
  }
  return value;
};

const parseJson = async (response) => {
  const text = await response.text();
  if (!text) return {};
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text };
  }
};

const requireOk = (response, body, label) => {
  if (!response.ok) {
    throw new Error(
      `${label} failed (${response.status}): ${JSON.stringify(body)}`,
    );
  }
};

const unwrapOrder = (body) => body?.order ?? body?.data?.order ?? body;
const sleep = (milliseconds) =>
  new Promise((resolve) => setTimeout(resolve, milliseconds));

const shippingOptionId = (value) => {
  const candidate =
    value && typeof value === 'object'
      ? value.shipping_option_id ?? value.id
      : value;
  if (candidate === undefined || candidate === null) return null;
  const id = String(candidate).trim();
  return id || null;
};

const shippingSelectionState = (order) => {
  const publicOptions = Array.isArray(order?.shipping_options)
    ? order.shipping_options
    : [];
  const legacyOptions = Array.isArray(order?.manual_quote?.shipping_options)
    ? order.manual_quote.shipping_options
    : [];
  const options = publicOptions.length > 0 ? publicOptions : legacyOptions;
  const selectedId =
    shippingOptionId(order?.selected_shipping_option_id) ||
    shippingOptionId(order?.selected_shipping_option) ||
    shippingOptionId(order?.selected_manual_shipping_option) ||
    shippingOptionId(order?.shipping_option);
  const optionIds = new Set(options.map(shippingOptionId).filter(Boolean));

  return {
    options,
    selectedId,
    selectionRequired:
      optionIds.size > 0 && (!selectedId || !optionIds.has(selectedId)),
  };
};

const printableShippingOptions = (options) =>
  options.map((option) => {
    const id = shippingOptionId(option);
    if (option && typeof option === 'object') {
      return { ...option, shipping_option_id: id };
    }
    return { shipping_option_id: id };
  });

const WALLET_PATH = process.env.AGENT_WALLET_PATH || './.wallet.json';
const API_KEY = required('SP3ND_API_KEY');
const API_SECRET = required('SP3ND_API_SECRET');
const PRODUCT_URL = required('SP3ND_PRODUCT_URL');
const CUSTOMER_EMAIL = required('SP3ND_CUSTOMER_EMAIL');
const IDEMPOTENCY_KEY = required('SP3ND_IDEMPOTENCY_KEY');
const SHIPPING_ADDRESS = JSON.parse(required('SP3ND_SHIPPING_ADDRESS_JSON'));
const QUANTITY = parsePositiveInteger('SP3ND_PRODUCT_QUANTITY', 1);
const MAX_QUOTE_WAIT_SECONDS = parsePositiveInteger(
  'SP3ND_MAX_QUOTE_WAIT_SECONDS',
  0,
);
const POLL_INTERVAL_SECONDS = Math.max(
  5,
  parsePositiveInteger('SP3ND_POLL_INTERVAL_SECONDS', 10),
);
const QUOTE_SAFETY_SECONDS = Math.max(
  15,
  parsePositiveInteger('SP3ND_QUOTE_SAFETY_SECONDS', 30),
);

if (QUANTITY < 1) throw new Error('SP3ND_PRODUCT_QUANTITY must be at least 1');

const RPC =
  process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com';
const BASE_URL =
  process.env.SP3ND_API_BASE_URL ||
  'https://us-central1-sp3nddotshop-prod.cloudfunctions.net';

const walletData = JSON.parse(readFileSync(WALLET_PATH, 'utf8'));
const keypair = Keypair.fromSecretKey(Uint8Array.from(walletData.secret));
const connection = new Connection(RPC, 'confirmed');
const USER_WALLET =
  process.env.SP3ND_USER_WALLET?.trim() || keypair.publicKey.toBase58();
const SHIPPING_OPTION_ID = process.env.SP3ND_SHIPPING_OPTION_ID?.trim();
const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': API_KEY,
  'X-API-Secret': API_SECRET,
};

console.log('Agent wallet:', keypair.publicKey.toBase58());
console.log('Attributed user wallet:', USER_WALLET);

const getOrder = async (orderId) => {
  const response = await fetch(
    `${BASE_URL}/getPartnerOrder?order_id=${encodeURIComponent(orderId)}`,
    { headers },
  );
  const body = await parseJson(response);
  requireOk(response, body, 'Get order');
  return unwrapOrder(body);
};

const selectShippingOption = async (orderId, shippingOptionId) => {
  const response = await fetch(`${BASE_URL}/selectPartnerOrderShippingOption`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      order_id: orderId,
      shipping_option_id: shippingOptionId,
    }),
  });
  const body = await parseJson(response);
  requireOk(response, body, 'Select shipping option');
  return unwrapOrder(body);
};

const isPaymentReady = (order) =>
  order?.payment_ready === true &&
  ['ready_for_payment', 'quoted'].includes(order?.pricing_status);

const quoteIsCurrent = (order) => {
  if (!order?.quote_expires_at) return true;
  const expiresAt = Date.parse(order.quote_expires_at);
  return (
    Number.isFinite(expiresAt) &&
    expiresAt > Date.now() + QUOTE_SAFETY_SECONDS * 1000
  );
};

const printLifecycle = (order) => {
  console.log(
    [
      `status=${order?.status ?? 'unknown'}`,
      `pricing_status=${order?.pricing_status ?? 'unknown'}`,
      `payment_ready=${order?.payment_ready === true}`,
      `quote_revision=${order?.quote_revision ?? 'none'}`,
      `quote_expires_at=${order?.quote_expires_at ?? 'none'}`,
    ].join(' | '),
  );
};

// 1. Create a server-priced cart. Product URL and quantity are the only
// purchasing inputs; SP3ND resolves all monetary and listing data.
console.log('\nCreating server-priced cart...');
const cartResponse = await fetch(`${BASE_URL}/createPartnerCart`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    items: [{ product_url: PRODUCT_URL, quantity: QUANTITY }],
    user_wallet: USER_WALLET,
  }),
});
const cartBody = await parseJson(cartResponse);
requireOk(cartResponse, cartBody, 'Create cart');
const cart = cartBody.cart ?? cartBody.data?.cart;
if (!cart?.cart_id) throw new Error('Create cart response did not include cart_id');
console.log('Cart:', cart.cart_id);

// 2. Create the order idempotently. Reuse this exact key if any network
// response is lost or this script is run again for the same checkout.
console.log('\nCreating idempotent order...');
const orderResponse = await fetch(`${BASE_URL}/createPartnerOrder`, {
  method: 'POST',
  headers: { ...headers, 'Idempotency-Key': IDEMPOTENCY_KEY },
  body: JSON.stringify({
    cart_id: cart.cart_id,
    idempotency_key: IDEMPOTENCY_KEY,
    user_wallet: USER_WALLET,
    customer_email: CUSTOMER_EMAIL,
    shipping_address: SHIPPING_ADDRESS,
  }),
});
const orderBody = await parseJson(orderResponse);
requireOk(orderResponse, orderBody, 'Create order');
let order = unwrapOrder(orderBody);
if (!order?.order_id) throw new Error('Create order response did not include order_id');
console.log('Order:', order.order_number ?? order.order_id);
printLifecycle(order);

// 3. A manual-review order is deliberately not payable. Optionally poll for
// a bounded period; otherwise stop safely and rerun with the same idempotency
// key after SP3ND has supplied a quote.
const waitDeadline = Date.now() + MAX_QUOTE_WAIT_SECONDS * 1000;
while (
  !isPaymentReady(order) &&
  !shippingSelectionState(order).selectionRequired
) {
  if (Date.now() >= waitDeadline) {
    console.log(
      '\nOrder is not payment-ready. No payment was attempted. ' +
        'Refresh this order later or rerun with the same SP3ND_IDEMPOTENCY_KEY.',
    );
    process.exit(0);
  }
  console.log(
    `Waiting for a payable quote; checking again in ${POLL_INTERVAL_SECONDS}s...`,
  );
  await sleep(POLL_INTERVAL_SECONDS * 1000);
  order = await getOrder(order.order_id);
  printLifecycle(order);
}

// 4. Never infer a shipping choice. Select only an opaque option returned by
// the current order quote, or stop and ask the user to choose.
let shipping = shippingSelectionState(order);
if (shipping.selectionRequired) {
  if (!SHIPPING_OPTION_ID) {
    console.log('\nA shipping option must be selected before payment:');
    console.log(
      JSON.stringify(printableShippingOptions(shipping.options), null, 2),
    );
    console.log(
      'Set SP3ND_SHIPPING_OPTION_ID to one of these opaque IDs, then rerun ' +
        'with the same SP3ND_IDEMPOTENCY_KEY. No payment was attempted.',
    );
    process.exit(0);
  }

  const configuredOptionExists = shipping.options.some(
    (option) => shippingOptionId(option) === SHIPPING_OPTION_ID,
  );
  if (!configuredOptionExists) {
    console.error(
      `\nSP3ND_SHIPPING_OPTION_ID "${SHIPPING_OPTION_ID}" is not one of ` +
        'the current order quote options. No payment was attempted.',
    );
    console.log(
      JSON.stringify(printableShippingOptions(shipping.options), null, 2),
    );
    process.exit(1);
  }

  order = await selectShippingOption(order.order_id, SHIPPING_OPTION_ID);
  console.log('\nShipping option selected:', SHIPPING_OPTION_ID);
  printLifecycle(order);
}

// 5. Refresh immediately before payment so quote revision, expiry, selection,
// and readiness all come from the latest server state.
order = await getOrder(order.order_id);
printLifecycle(order);

if (!isPaymentReady(order)) {
  throw new Error('Latest order state is not payment-ready; payment aborted');
}
if (!quoteIsCurrent(order)) {
  throw new Error('Order quote is expired or too close to expiry; payment aborted');
}
shipping = shippingSelectionState(order);
if (shipping.selectionRequired) {
  throw new Error('A required shipping option is not selected; payment aborted');
}

// 6. Request authoritative x402 payment requirements using order_id only.
console.log('\nRequesting server-issued payment requirements...');
const paymentResponse = await fetch(`${BASE_URL}/payAgentOrder`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ order_id: order.order_id }),
});
const paymentBody = await parseJson(paymentResponse);
if (paymentResponse.status !== 402) {
  const latest = await getOrder(order.order_id);
  throw new Error(
    `Expected HTTP 402, received ${paymentResponse.status}. ` +
      `Latest order status: ${latest.status ?? 'unknown'}`,
  );
}

const paymentRequiredHeader =
  paymentResponse.headers.get('PAYMENT-REQUIRED') ||
  paymentResponse.headers.get('payment-required');
const paymentRequired = paymentRequiredHeader
  ? JSON.parse(
      Buffer.from(paymentRequiredHeader, 'base64').toString('utf8'),
    )
  : paymentBody;
const requirement = paymentRequired?.accepts?.[0];
if (!requirement) throw new Error('402 response did not include payment requirements');

const memo =
  paymentBody?.memo ||
  requirement.extra?.memo ||
  (requirement.extra?.order_number
    ? `SP3ND Order: ${requirement.extra.order_number}`
    : null);
if (!memo) throw new Error('402 response did not include an order memo');

const amountAtomic = BigInt(requirement.maxAmountRequired);
const paymentMint = new PublicKey(requirement.asset);
const payToAddress = new PublicKey(requirement.payTo);
const feePayerAddress = new PublicKey(requirement.extra?.feePayer);
const tokenAccounts = await connection.getParsedTokenAccountsByOwner(
  keypair.publicKey,
  { mint: paymentMint },
);
const tokenAccount = tokenAccounts.value[0];
if (!tokenAccount) throw new Error('Agent wallet has no account for the required asset');
const tokenAmount = tokenAccount.account.data.parsed.info.tokenAmount;
const decimals = Number(tokenAmount.decimals);
if (BigInt(tokenAmount.amount) < amountAtomic) {
  throw new Error('Agent wallet balance is below the server-required amount');
}

console.log(
  '402 amount:',
  Number(amountAtomic) / 10 ** decimals,
  '| asset:',
  requirement.asset,
);
console.log('402 recipient:', requirement.payTo);
console.log('402 memo:', memo);

// 7. Build the transaction exclusively from the server's 402 values.
const sourceAta = await getAssociatedTokenAddress(
  paymentMint,
  keypair.publicKey,
);
const destinationAta = await getAssociatedTokenAddress(
  paymentMint,
  payToAddress,
);
const { blockhash } = await connection.getLatestBlockhash();
const instructions = [
  ComputeBudgetProgram.setComputeUnitLimit({ units: 30000 }),
  ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 1 }),
  createTransferCheckedInstruction(
    sourceAta,
    paymentMint,
    destinationAta,
    keypair.publicKey,
    amountAtomic,
    decimals,
  ),
  createMemoInstruction(memo),
];
const message = new TransactionMessage({
  payerKey: feePayerAddress,
  recentBlockhash: blockhash,
  instructions,
});
const transaction = new VersionedTransaction(message.compileToV0Message());
transaction.sign([keypair]);
const transactionBase64 = Buffer.from(transaction.serialize()).toString(
  'base64',
);

// PayAI currently accepts the v1 payload envelope for this Solana flow. Every
// monetary/resource field below is copied from SP3ND's 402 requirement.
const paymentPayload = {
  x402Version: 1,
  scheme: requirement.scheme,
  network: requirement.network,
  payload: { transaction: transactionBase64 },
};
const paymentSignature = Buffer.from(
  JSON.stringify(paymentPayload),
).toString('base64');

// 8. Send the signed x402 payload to SP3ND. SP3ND is the sole settlement
// authority: it atomically claims the attempt, verifies it with the configured
// facilitator, broadcasts it once, and records the resulting order state.
// Never call the facilitator's /settle endpoint directly.
console.log('\nSubmitting signed payment to SP3ND...');
const paidResponse = await fetch(`${BASE_URL}/payAgentOrder`, {
  method: 'POST',
  headers: { ...headers, 'PAYMENT-SIGNATURE': paymentSignature },
  body: JSON.stringify({ order_id: order.order_id }),
});
const paidBody = await parseJson(paidResponse);
if (!paidResponse.ok) {
  console.error('Exact memo:', memo);
  if (paidBody?.code === 'PAYMENT_SETTLEMENT_UNKNOWN') {
    throw new Error(
      'Settlement outcome is unknown. Do not retry payment. Give SP3ND the ' +
        `order ID ${order.order_id} for manual on-chain reconciliation.`,
    );
  }

  let latest = null;
  try {
    latest = await getOrder(order.order_id);
    console.error('Latest order state:', latest.status ?? 'unknown');
  } catch (refreshError) {
    console.error(
      'Could not refresh the order after the payment response:',
      refreshError instanceof Error ? refreshError.message : refreshError,
    );
  }
  if (latest?.payment_settlement_status === 'unknown') {
    throw new Error(
      'Settlement outcome is unknown. Do not retry payment. Give SP3ND the ' +
        `order ID ${order.order_id} for manual on-chain reconciliation.`,
    );
  }
  throw new Error(
    `SP3ND payment returned ${paidResponse.status}: ` +
      `${JSON.stringify(paidBody)}. Read the order before any retry.`,
  );
}

const paidOrder = unwrapOrder(paidBody);
console.log('\nPayment flow complete.');
console.log('Order:', paidOrder.order_number ?? order.order_number ?? order.order_id);
console.log('Status:', paidOrder.status ?? 'confirmation accepted');
console.log('Transaction:', paidBody.transaction_signature ?? 'recorded by SP3ND');
