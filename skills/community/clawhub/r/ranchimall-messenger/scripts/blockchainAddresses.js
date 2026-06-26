/**
 * Blockchain Address Derivation Utilities
 * Derives addresses for multiple blockchains from a single FLO/BTC WIF private key
 *
 * Supported Blockchains:
 * - FLO - via floCrypto (base blockchain)
 * - BTC (Bitcoin) - via btcOperator
 * - ETH (Ethereum) - via floEthereum
 * - AVAX (Avalanche C-Chain) - same as ETH (EVM-compatible)
 * - BSC (Binance Smart Chain) - same as ETH (EVM-compatible)
 * - MATIC (Polygon) - same as ETH (EVM-compatible)
 * - ARB (Arbitrum) - same as ETH (EVM-compatible)
 * - OP (Optimism) - same as ETH (EVM-compatible)
 * - HBAR (Hedera) - same as ETH (EVM-compatible)
 * - XRP (Ripple) - via xrpl library
 * - SUI - via nacl + BLAKE2b
 * - TON - via nacl + TonWeb
 * - TRON - via TronWeb
 * - DOGE - via bitjs with version byte 0x1e
 * - LTC (Litecoin) - via bitjs with version byte 0x30
 * - BCH (Bitcoin Cash) - via bitjs with version byte 0x00 + CashAddr format
 * - DOT (Polkadot) - via @polkadot/util-crypto with SS58 encoding
 * - ALGO (Algorand) - via nacl + SHA-512/256 with Base32 encoding
 * - XLM (Stellar) - via nacl + CRC16-XModem with Base32 encoding
 * - SOL (Solana) - via Ed25519 + Base58 encoding
 * - ADA (Cardano) - via cardanoCrypto library (https://cdn.jsdelivr.net/gh/void-57/cardano-wallet-test@main/cardano-crypto.iife.js)
 *
 * Dependencies :
 * - bitjs (for WIF decoding)
 * - Crypto.util (for hex/bytes conversion)
 * - xrpl (for XRP)
 * - nacl/TweetNaCl (for SUI, TON, ALGO, XLM)
 * - TonWeb (for TON)
 * - TronWeb (for TRON)
 * - @polkadot/util-crypto (for DOT)
 * - @polkadot/util (for DOT)
 * - js-sha512 (for ALGO)
 * - @solana/web3.js (for SOL)
 * - cardanoCrypto (for ADA)
 */

// Base58 encoding/decoding for Solana
var bs58 = (function () {
  const ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
  const BASE = ALPHABET.length;

  // Convert a byte array to a Base58 string
  function encode(buffer) {
    if (buffer.length === 0) return "";

    // Convert byte array to a BigInt
    let intVal = BigInt(0);
    for (let i = 0; i < buffer.length; i++) {
      intVal = intVal * BigInt(256) + BigInt(buffer[i]);
    }

    // Convert BigInt to Base58 string
    let result = "";
    while (intVal > 0) {
      const remainder = intVal % BigInt(BASE);
      intVal = intVal / BigInt(BASE);
      result = ALPHABET[Number(remainder)] + result;
    }

    // Add '1' for each leading 0 byte in the byte array
    for (let i = 0; i < buffer.length && buffer[i] === 0; i++) {
      result = ALPHABET[0] + result;
    }

    return result;
  }

  // Convert a Base58 string to a byte array
  function decode(string) {
    if (string.length === 0) return new Uint8Array();

    // Convert Base58 string to BigInt
    let intVal = BigInt(0);
    for (let i = 0; i < string.length; i++) {
      const charIndex = ALPHABET.indexOf(string[i]);
      if (charIndex < 0) {
        throw new Error("Invalid Base58 character");
      }
      intVal = intVal * BigInt(BASE) + BigInt(charIndex);
    }

    // Convert BigInt to byte array
    const byteArray = [];
    while (intVal > 0) {
      byteArray.push(Number(intVal % BigInt(256)));
      intVal = intVal / BigInt(256);
    }

    // Reverse the byte array and add leading zeros
    byteArray.reverse();
    for (let i = 0; i < string.length && string[i] === ALPHABET[0]; i++) {
      byteArray.unshift(0);
    }

    return Uint8Array.from(byteArray);
  }

  return { encode, decode };
})();

// BlakeJS - BLAKE2b hashing implementation for SUI
const blakejs = (function () {
  const BLAKE2B_IV32 = new Uint32Array([
    0xf3bcc908, 0x6a09e667, 0x84caa73b, 0xbb67ae85, 0xfe94f82b, 0x3c6ef372,
    0x5f1d36f1, 0xa54ff53a, 0xade682d1, 0x510e527f, 0x2b3e6c1f, 0x9b05688c,
    0xfb41bd6b, 0x1f83d9ab, 0x137e2179, 0x5be0cd19,
  ]);
  const SIGMA8 = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 14, 10, 4, 8, 9, 15,
    13, 6, 1, 12, 0, 2, 11, 7, 5, 3, 11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6,
    7, 1, 9, 4, 7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8, 9, 0, 5,
    7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13, 2, 12, 6, 10, 0, 11, 8, 3, 4,
    13, 7, 5, 15, 14, 1, 9, 12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8,
    11, 13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10, 6, 15, 14, 9, 11,
    3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5, 10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14,
    3, 12, 13, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 14, 10,
    4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3,
  ];
  const SIGMA82 = new Uint8Array(SIGMA8.map((x) => x * 2));
  const v = new Uint32Array(32);
  const m = new Uint32Array(32);
  const parameterBlock = new Uint8Array(64);

  function B2B_GET32(arr, i) {
    return arr[i] ^ (arr[i + 1] << 8) ^ (arr[i + 2] << 16) ^ (arr[i + 3] << 24);
  }
  function ADD64AA(v, a, b) {
    const o0 = v[a] + v[b];
    let o1 = v[a + 1] + v[b + 1];
    if (o0 >= 0x100000000) o1++;
    v[a] = o0;
    v[a + 1] = o1;
  }
  function ADD64AC(v, a, b0, b1) {
    let o0 = v[a] + b0;
    if (b0 < 0) o0 += 0x100000000;
    let o1 = v[a + 1] + b1;
    if (o0 >= 0x100000000) o1++;
    v[a] = o0;
    v[a + 1] = o1;
  }
  function B2B_G(a, b, c, d, ix, iy) {
    const x0 = m[ix],
      x1 = m[ix + 1],
      y0 = m[iy],
      y1 = m[iy + 1];
    ADD64AA(v, a, b);
    ADD64AC(v, a, x0, x1);
    let xor0 = v[d] ^ v[a],
      xor1 = v[d + 1] ^ v[a + 1];
    v[d] = xor1;
    v[d + 1] = xor0;
    ADD64AA(v, c, d);
    xor0 = v[b] ^ v[c];
    xor1 = v[b + 1] ^ v[c + 1];
    v[b] = (xor0 >>> 24) ^ (xor1 << 8);
    v[b + 1] = (xor1 >>> 24) ^ (xor0 << 8);
    ADD64AA(v, a, b);
    ADD64AC(v, a, y0, y1);
    xor0 = v[d] ^ v[a];
    xor1 = v[d + 1] ^ v[a + 1];
    v[d] = (xor0 >>> 16) ^ (xor1 << 16);
    v[d + 1] = (xor1 >>> 16) ^ (xor0 << 16);
    ADD64AA(v, c, d);
    xor0 = v[b] ^ v[c];
    xor1 = v[b + 1] ^ v[c + 1];
    v[b] = (xor1 >>> 31) ^ (xor0 << 1);
    v[b + 1] = (xor0 >>> 31) ^ (xor1 << 1);
  }
  function blake2bCompress(ctx, last) {
    let i;
    for (i = 0; i < 16; i++) {
      v[i] = ctx.h[i];
      v[i + 16] = BLAKE2B_IV32[i];
    }
    v[24] = v[24] ^ ctx.t;
    v[25] = v[25] ^ (ctx.t / 0x100000000);
    if (last) {
      v[28] = ~v[28];
      v[29] = ~v[29];
    }
    for (i = 0; i < 32; i++) m[i] = B2B_GET32(ctx.b, 4 * i);
    for (i = 0; i < 12; i++) {
      B2B_G(0, 8, 16, 24, SIGMA82[i * 16 + 0], SIGMA82[i * 16 + 1]);
      B2B_G(2, 10, 18, 26, SIGMA82[i * 16 + 2], SIGMA82[i * 16 + 3]);
      B2B_G(4, 12, 20, 28, SIGMA82[i * 16 + 4], SIGMA82[i * 16 + 5]);
      B2B_G(6, 14, 22, 30, SIGMA82[i * 16 + 6], SIGMA82[i * 16 + 7]);
      B2B_G(0, 10, 20, 30, SIGMA82[i * 16 + 8], SIGMA82[i * 16 + 9]);
      B2B_G(2, 12, 22, 24, SIGMA82[i * 16 + 10], SIGMA82[i * 16 + 11]);
      B2B_G(4, 14, 16, 26, SIGMA82[i * 16 + 12], SIGMA82[i * 16 + 13]);
      B2B_G(6, 8, 18, 28, SIGMA82[i * 16 + 14], SIGMA82[i * 16 + 15]);
    }
    for (i = 0; i < 16; i++) ctx.h[i] = ctx.h[i] ^ v[i] ^ v[i + 16];
  }
  function blake2bInit(outlen, key) {
    const ctx = {
      b: new Uint8Array(128),
      h: new Uint32Array(16),
      t: 0,
      c: 0,
      outlen: outlen,
    };
    parameterBlock.fill(0);
    parameterBlock[0] = outlen;
    if (key) parameterBlock[1] = key.length;
    parameterBlock[2] = 1;
    parameterBlock[3] = 1;
    for (let i = 0; i < 16; i++)
      ctx.h[i] = BLAKE2B_IV32[i] ^ B2B_GET32(parameterBlock, i * 4);
    if (key) {
      blake2bUpdate(ctx, key);
      ctx.c = 128;
    }
    return ctx;
  }
  function blake2bUpdate(ctx, input) {
    for (let i = 0; i < input.length; i++) {
      if (ctx.c === 128) {
        ctx.t += ctx.c;
        blake2bCompress(ctx, false);
        ctx.c = 0;
      }
      ctx.b[ctx.c++] = input[i];
    }
  }
  function blake2bFinal(ctx) {
    ctx.t += ctx.c;
    while (ctx.c < 128) ctx.b[ctx.c++] = 0;
    blake2bCompress(ctx, true);
    const out = new Uint8Array(ctx.outlen);
    for (let i = 0; i < ctx.outlen; i++)
      out[i] = ctx.h[i >> 2] >> (8 * (i & 3));
    return out;
  }
  function blake2b(input, key, outlen) {
    outlen = outlen || 64;
    if (!(input instanceof Uint8Array)) {
      if (typeof input === "string") {
        const enc = unescape(encodeURIComponent(input));
        input = new Uint8Array(enc.length);
        for (let i = 0; i < enc.length; i++) input[i] = enc.charCodeAt(i);
      } else throw new Error("Input must be string or Uint8Array");
    }
    const ctx = blake2bInit(outlen, key);
    blake2bUpdate(ctx, input);
    return blake2bFinal(ctx);
  }
  return { blake2b: blake2b };
})();

/**
 * Convert WIF private key to BSC (Binance Smart Chain) address
 * BSC uses the same address format as Ethereum (EVM-compatible)
 * @param {string} publicKey - Compressed public key in hex
 * @returns {string} BSC address (same as ETH address)
 */
function convertPublicKeyToBscAddress(publicKey) {
  // BSC addresses are identical to Ethereum addresses
  // Both use the same EVM-compatible format
  if (
    typeof floEthereum === "undefined" ||
    !floEthereum.ethAddressFromCompressedPublicKey
  ) {
    throw new Error("floEthereum library not loaded");
  }
  return floEthereum.ethAddressFromCompressedPublicKey(publicKey);
}

/**
 * Convert WIF private key to XRP (Ripple) address
 * Uses xrpl library with Ed25519 derivation
 * @param {string} wif - WIF format private key
 * @returns {string|null} XRP address or null on error
 */
function convertWIFtoXrpAddress(wif) {
  try {
    if (typeof window.xrpl === "undefined") {
      throw new Error("xrpl library not loaded");
    }
    if (typeof bitjs === "undefined") {
      throw new Error("bitjs library not loaded");
    }
    // Use bitjs.wif2privkey to decode WIF and get the raw private key hex
    const decoded = bitjs.wif2privkey(wif);
    if (!decoded || !decoded.privkey) {
      throw new Error("Failed to decode WIF private key");
    }
    // Convert hex string to byte array for xrpl
    const keyBytes = Crypto.util.hexToBytes(decoded.privkey);
    // Create XRP wallet from entropy (raw private key bytes)
    const wallet = xrpl.Wallet.fromEntropy(keyBytes);
    return wallet.address;
  } catch (error) {
    console.error("WIF to XRP conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to SUI address
 * Uses Ed25519 keypair + BLAKE2b-256 hashing
 * @param {string} wif - WIF format private key
 * @returns {string|null} SUI address (0x prefixed) or null on error
 */
function convertWIFtoSuiAddress(wif) {
  try {
    if (typeof nacl === "undefined") {
      throw new Error("nacl (TweetNaCl) library not loaded");
    }
    if (typeof bitjs === "undefined") {
      throw new Error("bitjs library not loaded");
    }
    // Use bitjs.wif2privkey to decode WIF and get the raw private key hex
    const decoded = bitjs.wif2privkey(wif);
    if (!decoded || !decoded.privkey) {
      throw new Error("Failed to decode WIF private key");
    }
    // Get first 32 bytes (64 hex chars) for Ed25519 seed
    const privKeyHex = decoded.privkey.substring(0, 64);
    const privBytes = Crypto.util.hexToBytes(privKeyHex);
    const seed = new Uint8Array(privBytes.slice(0, 32));
    // Generate Ed25519 keypair from seed
    const keyPair = nacl.sign.keyPair.fromSeed(seed);
    const pubKey = keyPair.publicKey;
    // Prefix public key with 0x00 (Ed25519 scheme flag)
    const prefixedPubKey = new Uint8Array([0x00, ...pubKey]);
    // Hash with BLAKE2b-256
    const hash = blakejs.blake2b(prefixedPubKey, null, 32);
    // Convert to hex address with 0x prefix
    const suiAddress = "0x" + Crypto.util.bytesToHex(hash);
    return suiAddress;
  } catch (error) {
    console.error("WIF to SUI conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to TON address
 * Uses Ed25519 keypair + TonWeb v4R2 wallet
 * @param {string} wif - WIF format private key
 * @returns {Promise<string|null>} TON address (bounceable format) or null on error
 */
async function convertWIFtoTonAddress(wif) {
  try {
    if (typeof nacl === "undefined") {
      throw new Error("nacl (TweetNaCl) library not loaded");
    }
    if (typeof TonWeb === "undefined") {
      throw new Error("TonWeb library not loaded");
    }
    if (typeof bitjs === "undefined") {
      throw new Error("bitjs library not loaded");
    }
    // Use bitjs.wif2privkey to decode WIF and get the raw private key hex
    const decoded = bitjs.wif2privkey(wif);
    if (!decoded || !decoded.privkey) {
      throw new Error("Failed to decode WIF private key");
    }
    // Get first 32 bytes (64 hex chars) for Ed25519 seed
    const privKeyHex = decoded.privkey.substring(0, 64);
    const seed = Crypto.util.hexToBytes(privKeyHex);
    // Generate Ed25519 keypair from seed
    const keyPair = nacl.sign.keyPair.fromSeed(new Uint8Array(seed));
    // Create TON wallet using TonWeb v4R2 wallet
    const tonweb = new TonWeb();
    const WalletClass = TonWeb.Wallets.all.v4R2;
    if (!WalletClass) {
      throw new Error("TonWeb v4R2 wallet not available");
    }
    const wallet = new WalletClass(tonweb.provider, {
      publicKey: keyPair.publicKey,
    });
    const address = await wallet.getAddress();
    // Return user-friendly bounceable address
    return address.toString(true, true, false);
  } catch (error) {
    console.error("WIF to TON conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to TRON address
 * Uses TronWeb library for address derivation
 * @param {string} wif - WIF format private key
 * @returns {string|null} TRON address (Base58 format) or null on error
 */
function convertWIFtoTronAddress(wif) {
  try {
    if (typeof TronWeb === "undefined") {
      throw new Error("TronWeb library not loaded");
    }
    if (typeof bitjs === "undefined") {
      throw new Error("bitjs library not loaded");
    }
    // Use bitjs.wif2privkey to decode WIF and get the raw private key hex
    const decoded = bitjs.wif2privkey(wif);
    if (!decoded || !decoded.privkey) {
      throw new Error("Failed to decode WIF private key");
    }
    // Get the hex private key (64 chars)
    const privKeyHex = decoded.privkey.substring(0, 64);
    // Use TronWeb to derive address from private key
    const tronAddress = TronWeb.address.fromPrivateKey(privKeyHex);
    return tronAddress;
  } catch (error) {
    console.error("WIF to TRON conversion error:", error);
    return null;
  }
}

/**
 * Derive all blockchain addresses from a WIF private key
 * @param {string} wif - WIF format private key
 * @returns {Promise<Object>} Object containing all derived addresses
 */
async function deriveAllBlockchainAddresses(wif) {
  const addresses = {
    bsc: null,
    matic: null,
    hbar: null,
    arb: null,
    op: null,
    xrp: null,
    sui: null,
    ton: null,
    tron: null,
    doge: null,
    ltc: null,
    bch: null,
    dot: null,
    algo: null,
    xlm: null,
    sol: null,
    ada: null,
  };

  try {
    // BSC, MATIC, HBAR, ARB, and OP use same address as ETH (requires public key, not WIF)
    // These will be set from floGlobals.myEthID in the main code
    addresses.bsc = null; // Set in main code as same as ETH
    addresses.matic = null; // Set in main code as same as ETH
    addresses.hbar = null; // Set in main code as same as ETH
    addresses.arb = null; // Set in main code as same as ETH
    addresses.op = null; // Set in main code as same as ETH
  } catch (e) {
    console.warn("BSC/MATIC/HBAR/ARB/OP derivation failed:", e);
  }
  try {
    addresses.xrp = convertWIFtoXrpAddress(wif);
  } catch (e) {
    console.warn("XRP derivation failed:", e);
  }
  try {
    addresses.sui = convertWIFtoSuiAddress(wif);
  } catch (e) {
    console.warn("SUI derivation failed:", e);
  }
  try {
    addresses.ton = await convertWIFtoTonAddress(wif);
  } catch (e) {
    console.warn("TON derivation failed:", e);
  }
  try {
    addresses.tron = convertWIFtoTronAddress(wif);
  } catch (e) {
    console.warn("TRON derivation failed:", e);
  }
  try {
    addresses.doge = convertWIFtoDogeAddress(wif);
  } catch (e) {
    console.warn("DOGE derivation failed:", e);
  }
  try {
    addresses.dot = await convertWIFtoPolkadotAddress(wif);
  } catch (e) {
    console.warn("DOT derivation failed:", e);
  }
  try {
    addresses.algo = convertWIFtoAlgorandAddress(wif);
  } catch (e) {
    console.warn("ALGO derivation failed:", e);
  }
  try {
    addresses.xlm = convertWIFtoStellarAddress(wif);
  } catch (e) {
    console.warn("XLM derivation failed:", e);
  }
  try {
    addresses.ltc = convertWIFtoLitecoinAddress(wif);
  } catch (e) {
    console.warn("LTC derivation failed:", e);
  }
  try {
    addresses.bch = convertWIFtoBitcoinCashAddress(wif);
  } catch (e) {
    console.warn("BCH derivation failed:", e);
  }
  try {
    addresses.sol = convertWIFtoSolanaAddress(wif);
  } catch (e) {
    console.warn("SOL derivation failed:", e);
  }
  try {
    addresses.ada = await convertWIFtoCardanoAddress(wif);
  } catch (e) {
    console.warn("ADA derivation failed:", e);
  }

  return addresses;
}

/**
 * Convert WIF private key to DOGE (Dogecoin) address
 * Uses secp256k1 with version byte 0x1e (30)
 * @param {string} wif - WIF format private key
 * @returns {string|null} DOGE address (Base58 format starting with 'D') or null on error
 */
function convertWIFtoDogeAddress(wif) {
  try {
    // Store original settings
    const origPub = bitjs.pub;
    const origPriv = bitjs.priv;
    const origBitjsCompressed = bitjs.compressed;

    // Decode WIF to get raw private key and determine if compressed
    const decode = Bitcoin.Base58.decode(wif);
    const keyWithVersion = decode.slice(0, decode.length - 4);
    let key = keyWithVersion.slice(1);

    let compressed = true;
    if (key.length >= 33 && key[key.length - 1] === 0x01) {
      // Compressed WIF has 0x01 suffix
      key = key.slice(0, key.length - 1);
      compressed = true;
    } else {
      compressed = false;
    }

    const privKeyHex = Crypto.util.bytesToHex(key);

    // Set DOGE version bytes and compression
    bitjs.pub = 0x1e;
    bitjs.priv = 0x9e;
    bitjs.compressed = compressed;

    // Generate public key from private key
    const pubKey = bitjs.newPubkey(privKeyHex);
    // Generate DOGE address from public key
    const dogeAddress = bitjs.pubkey2address(pubKey);

    // Restore original settings
    bitjs.pub = origPub;
    bitjs.priv = origPriv;
    bitjs.compressed = origBitjsCompressed;

    return dogeAddress;
  } catch (error) {
    console.error("WIF to DOGE conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to LTC (Litecoin) address
 * Uses secp256k1 with version byte 0x30 (48)
 * @param {string} wif - WIF format private key
 * @returns {string|null} LTC address (Base58 format starting with 'L') or null on error
 */
function convertWIFtoLitecoinAddress(wif) {
  try {
    // Store original settings
    const origPub = bitjs.pub;
    const origPriv = bitjs.priv;
    const origBitjsCompressed = bitjs.compressed;

    // Decode WIF to get raw private key and determine if compressed
    const decode = Bitcoin.Base58.decode(wif);
    const keyWithVersion = decode.slice(0, decode.length - 4);
    let key = keyWithVersion.slice(1);

    let compressed = true;
    if (key.length >= 33 && key[key.length - 1] === 0x01) {
      // Compressed WIF has 0x01 suffix
      key = key.slice(0, key.length - 1);
      compressed = true;
    } else {
      compressed = false;
    }

    const privKeyHex = Crypto.util.bytesToHex(key);

    // Set LTC version bytes and compression
    bitjs.pub = 0x30; // Litecoin mainnet pubkey version
    bitjs.priv = 0xb0; // Litecoin mainnet private key version
    bitjs.compressed = compressed;

    // Generate public key from private key
    const pubKey = bitjs.newPubkey(privKeyHex);
    // Generate LTC address from public key
    const ltcAddress = bitjs.pubkey2address(pubKey);

    // Restore original settings
    bitjs.pub = origPub;
    bitjs.priv = origPriv;
    bitjs.compressed = origBitjsCompressed;

    return ltcAddress;
  } catch (error) {
    console.error("WIF to LTC conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to BCH (Bitcoin Cash) address in CashAddr format
 * Uses secp256k1 with version byte 0x00 (same as BTC) but returns CashAddr format
 * @param {string} wif - WIF format private key
 * @returns {string|null} BCH address (CashAddr format without prefix) or null on error
 */
function convertWIFtoBitcoinCashAddress(wif) {
  try {
    // Helper function to convert legacy address to CashAddr
    function toCashAddr(legacyAddr) {
      if (!legacyAddr || typeof legacyAddr !== "string") return legacyAddr;
      if (legacyAddr.includes(":")) return legacyAddr; // Already cashaddr

      try {
        const ALPHABET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";

        function polymod(values) {
          let c = 1n;
          for (let v of values) {
            let b = c >> 35n;
            c = ((c & 0x07ffffffffn) << 5n) ^ BigInt(v);
            if (b & 1n) c ^= 0x98f2bc8e61n;
            if (b & 2n) c ^= 0x79b76d99e2n;
            if (b & 4n) c ^= 0xf33e5fb3c4n;
            if (b & 8n) c ^= 0xae2eabe2a8n;
            if (b & 16n) c ^= 0x1e4f43e470n;
          }
          return c ^ 1n;
        }

        function expandPrefix(prefix) {
          let ret = [];
          for (let i = 0; i < prefix.length; i++) {
            ret.push(prefix.charCodeAt(i) & 0x1f);
          }
          ret.push(0);
          return ret;
        }

        function convertBits(data, from, to, pad = true) {
          let acc = 0;
          let bits = 0;
          const ret = [];
          const maxv = (1 << to) - 1;
          for (let i = 0; i < data.length; ++i) {
            const value = data[i] & 0xff;
            acc = (acc << from) | value;
            bits += from;
            while (bits >= to) {
              bits -= to;
              ret.push((acc >> bits) & maxv);
            }
            acc &= (1 << bits) - 1;
          }
          if (pad && bits > 0) {
            ret.push((acc << (to - bits)) & maxv);
          }
          return ret;
        }

        // Decode legacy address
        const decoded = Bitcoin.Base58.decode(legacyAddr);
        if (!decoded || decoded.length < 25) return legacyAddr;

        const version = decoded[0];
        const hash = decoded.slice(1, -4);

        // Version byte 0x00 is P2PKH (type 0), 0x05 is P2SH (type 1)
        const type = version === 0x00 ? 0 : version === 0x05 ? 1 : null;
        if (type === null) return legacyAddr;

        const prefix = "bitcoincash";
        const versionByte = type << 3;
        const payload = [versionByte].concat(Array.from(hash));
        const payload5bit = convertBits(payload, 8, 5, true);

        const checksumData = expandPrefix(prefix)
          .concat(payload5bit)
          .concat([0, 0, 0, 0, 0, 0, 0, 0]);
        const checksum = polymod(checksumData);
        const checksum5bit = [];
        for (let i = 0; i < 8; i++) {
          checksum5bit.push(Number((checksum >> (5n * BigInt(7 - i))) & 0x1fn));
        }

        const combined = payload5bit.concat(checksum5bit);
        let ret = "";
        for (let v of combined) {
          ret += ALPHABET[v];
        }
        return ret;
      } catch (e) {
        console.error("CashAddr conversion error:", e);
        return legacyAddr;
      }
    }

    // Store original settings
    const origPub = bitjs.pub;
    const origPriv = bitjs.priv;
    const origBitjsCompressed = bitjs.compressed;

    // Decode WIF to get raw private key and determine if compressed
    const decode = Bitcoin.Base58.decode(wif);
    const keyWithVersion = decode.slice(0, decode.length - 4);
    let key = keyWithVersion.slice(1);

    let compressed = true;
    if (key.length >= 33 && key[key.length - 1] === 0x01) {
      key = key.slice(0, key.length - 1);
      compressed = true;
    } else {
      compressed = false;
    }

    const privKeyHex = Crypto.util.bytesToHex(key);

    // Set BCH version bytes (same as BTC mainnet)
    bitjs.pub = 0x00; // Bitcoin Cash mainnet pubkey version
    bitjs.priv = 0x80; // Bitcoin Cash mainnet private key version
    bitjs.compressed = compressed;

    // Generate public key from private key
    const pubKey = bitjs.newPubkey(privKeyHex);
    // Generate legacy BCH address from public key
    const legacyAddress = bitjs.pubkey2address(pubKey);

    // Convert to CashAddr format
    const cashAddr = toCashAddr(legacyAddress);

    // Restore original settings
    bitjs.pub = origPub;
    bitjs.priv = origPriv;
    bitjs.compressed = origBitjsCompressed;

    return cashAddr;
  } catch (error) {
    console.error("WIF to BCH conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to Polkadot (DOT) address
 * Uses Sr25519 (Schnorrkel) keypair with SS58 address encoding (prefix 0 for Polkadot mainnet)
 * @param {string} wif - WIF format private key
 * @returns {Promise<string|null>} DOT address (SS58 format) or null on error
 */
async function convertWIFtoPolkadotAddress(wif) {
  try {
    if (typeof bitjs === "undefined") {
      throw new Error("bitjs library not loaded");
    }

    // Access Polkadot library from window object
    const polkadotAPI = window.polkadotUtilCrypto;

    if (!polkadotAPI) {
      throw new Error("@polkadot/util-crypto library not loaded");
    }

    // Wait for WASM crypto to be ready
    if (typeof polkadotAPI.cryptoWaitReady === "function") {
      await polkadotAPI.cryptoWaitReady();
    }

    // Use bitjs.wif2privkey to decode WIF and get the raw private key hex
    const decoded = bitjs.wif2privkey(wif);
    if (!decoded || !decoded.privkey) {
      throw new Error("Failed to decode WIF private key");
    }

    // Get first 32 bytes (64 hex chars) for Sr25519 seed
    const privKeyHex = decoded.privkey.substring(0, 64);
    const privBytes = Crypto.util.hexToBytes(privKeyHex);
    const seed = new Uint8Array(privBytes.slice(0, 32));

    // Create Sr25519 keypair from seed (Polkadot uses Schnorrkel/Sr25519, not Ed25519)
    const keyPair = polkadotAPI.sr25519PairFromSeed(seed);

    // Encode address in SS58 format with Polkadot prefix (0)
    const dotAddress = polkadotAPI.encodeAddress(keyPair.publicKey, 0);

    return dotAddress;
  } catch (error) {
    console.error("WIF to Polkadot conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to Algorand (ALGO) address
 * Uses Ed25519 keypair with Base32 encoding and SHA-512/256 checksum
 * @param {string} wif - WIF format private key
 * @returns {string|null} ALGO address (Base32 format) or null on error
 */
function convertWIFtoAlgorandAddress(wif) {
  try {
    if (typeof bitjs === "undefined") {
      throw new Error("bitjs library not loaded");
    }
    if (typeof nacl === "undefined") {
      throw new Error("nacl (TweetNaCl) library not loaded");
    }
    if (typeof sha512 === "undefined") {
      throw new Error("js-sha512 library not loaded");
    }

    // Use bitjs.wif2privkey to decode WIF and get the raw private key hex
    const decoded = bitjs.wif2privkey(wif);
    if (!decoded || !decoded.privkey) {
      throw new Error("Failed to decode WIF private key");
    }

    // Get first 32 bytes (64 hex chars) for Ed25519 seed
    const privKeyHex = decoded.privkey.substring(0, 64);
    const privBytes = Crypto.util.hexToBytes(privKeyHex);
    const seed = new Uint8Array(privBytes.slice(0, 32));

    // Generate Ed25519 keypair from seed
    const keyPair = nacl.sign.keyPair.fromSeed(seed);
    const pubKey = keyPair.publicKey;

    // Algorand uses SHA-512/256 (32 bytes output) for checksum
    const hashResult = new Uint8Array(sha512.sha512_256.array(pubKey));
    const checksum = hashResult.slice(28, 32);
    const addressBytes = new Uint8Array([...pubKey, ...checksum]);

    // Base32 encode the address
    const BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    let bits = 0;
    let value = 0;
    let output = "";

    for (let i = 0; i < addressBytes.length; i++) {
      value = (value << 8) | addressBytes[i];
      bits += 8;

      while (bits >= 5) {
        output += BASE32_ALPHABET[(value >>> (bits - 5)) & 31];
        bits -= 5;
      }
    }

    if (bits > 0) {
      output += BASE32_ALPHABET[(value << (5 - bits)) & 31];
    }

    return output;
  } catch (error) {
    console.error("WIF to Algorand conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to Stellar (XLM) address
 * Uses Ed25519 keypair generation with Stellar-specific encoding
 * @param {string} wif - The WIF private key
 * @returns {string} - The Stellar address (starting with 'G')
 */
function convertWIFtoStellarAddress(wif) {
  try {
    // Helper function to convert hex to bytes
    function hexToBytes(hex) {
      const bytes = [];
      for (let i = 0; i < hex.length; i += 2) {
        bytes.push(parseInt(hex.substr(i, 2), 16));
      }
      return bytes;
    }

    // Calculate CRC16-XModem checksum (Stellar uses this)
    function crc16XModem(data) {
      let crc = 0x0000;
      for (let i = 0; i < data.length; i++) {
        crc ^= data[i] << 8;
        for (let j = 0; j < 8; j++) {
          if (crc & 0x8000) {
            crc = (crc << 1) ^ 0x1021;
          } else {
            crc = crc << 1;
          }
        }
      }
      return crc & 0xffff;
    }

    // Decode WIF to get private key (32 bytes)
    const privKeyHex = bitjs.wif2privkey(wif).privkey;
    const privBytes = hexToBytes(privKeyHex);
    const seed = new Uint8Array(privBytes.slice(0, 32));

    // Generate Ed25519 keypair from seed using TweetNaCl
    const keyPair = nacl.sign.keyPair.fromSeed(seed);
    const pubKey = keyPair.publicKey;

    // Stellar address encoding: version byte (0x30 for public key 'G') + public key + CRC16-XModem checksum
    const versionByte = 0x30; // Results in 'G' prefix for public keys
    const payload = new Uint8Array([versionByte, ...pubKey]);

    const checksum = crc16XModem(payload);
    // Checksum is stored in little-endian format
    const checksumBytes = new Uint8Array([
      checksum & 0xff,
      (checksum >> 8) & 0xff,
    ]);
    const addressBytes = new Uint8Array([...payload, ...checksumBytes]);

    // Base32 encode the address (RFC 4648)
    const BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    let bits = 0;
    let value = 0;
    let output = "";

    for (let i = 0; i < addressBytes.length; i++) {
      value = (value << 8) | addressBytes[i];
      bits += 8;

      while (bits >= 5) {
        output += BASE32_ALPHABET[(value >>> (bits - 5)) & 31];
        bits -= 5;
      }
    }

    if (bits > 0) {
      output += BASE32_ALPHABET[(value << (5 - bits)) & 31];
    }

    return output;
  } catch (error) {
    console.error("WIF to Stellar conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to Solana (SOL) address
 * Uses Ed25519 keypair generation with Base58 encoding
 * @param {string} wif - The WIF private key
 * @returns {string} - The Solana address (Base58 encoded public key)
 */
function convertWIFtoSolanaAddress(wif) {
  try {
    // Helper function to convert hex to bytes
    function hexToBytes(hex) {
      const bytes = [];
      for (let i = 0; i < hex.length; i += 2) {
        bytes.push(parseInt(hex.substr(i, 2), 16));
      }
      return bytes;
    }

    // Decode WIF to get private key (32 bytes)
    const privKeyHex = bitjs.wif2privkey(wif).privkey;
    const privBytes = hexToBytes(privKeyHex);
    const seed = new Uint8Array(privBytes.slice(0, 32));

    // Generate Ed25519 keypair from seed
    // Use Solana Web3.js Keypair.fromSeed()
    if (typeof solanaWeb3 === "undefined") {
      throw new Error("Solana Web3.js library not loaded");
    }

    const keypair = solanaWeb3.Keypair.fromSeed(seed);
    const solanaAddress = keypair.publicKey.toString();

    return solanaAddress;
  } catch (error) {
    console.error("WIF to Solana conversion error:", error);
    return null;
  }
}

/**
 * Convert WIF private key to Cardano (ADA) address
 * Uses cardanoCrypto library for address derivation
 * @param {string} wif - WIF format private key
 * @returns {Promise<string|null>} Cardano address or null on error
 */
async function convertWIFtoCardanoAddress(wif) {
  try {
    if (typeof window.cardanoCrypto === "undefined") {
      throw new Error("cardanoCrypto library not loaded");
    }

    // Use cardanoCrypto.importFromKey to derive all addresses from WIF
    const wallet = await window.cardanoCrypto.importFromKey(wif);

    if (!wallet || !wallet.Cardano || !wallet.Cardano.address) {
      throw new Error("Failed to derive Cardano address");
    }

    return wallet.Cardano.address;
  } catch (error) {
    console.error("WIF to Cardano conversion error:", error);
    return null;
  }
}
