require("dotenv").config();
const fs = require("fs");
const { ethers } = require("ethers");
const axios = require("axios");
const routerAbi = require("./router-abi.json");

// ===== LOAD BRAIN =====
let brain = JSON.parse(fs.readFileSync("brain.json"));
function save() {
  fs.writeFileSync("brain.json", JSON.stringify(brain, null, 2));
}

// ===== CONFIG =====
const RPCS = process.env.RPC_URLS.split(",");
const KEYS = process.env.PRIVATE_KEYS.split(",");
const MAX_TX = parseInt(process.env.MAX_TX_PER_HOUR);

// ===== INIT RPC =====
RPCS.forEach(r => {
  if (!brain.rpcs[r]) {
    brain.rpcs[r] = { success: 1, fail: 1, lastUsed: 0 };
  }
});

// ===== PICK RPC =====
function pickRPC() {
  let best = RPCS[0];
  let score = -1;

  for (let r of RPCS) {
    const d = brain.rpcs[r];
    const rate = d.success / (d.success + d.fail);
    const cooldown = Date.now() - d.lastUsed;

    const s = rate + cooldown / 1e6;

    if (s > score) {
      score = s;
      best = r;
    }
  }

  brain.rpcs[best].lastUsed = Date.now();
  return best;
}

// ===== PROVIDER =====
function getProvider() {
  return new ethers.JsonRpcProvider(pickRPC());
}

// ===== WALLETS =====
const wallets = KEYS.map(k => new ethers.Wallet(k.trim()));

// init wallet brain
wallets.forEach(w => {
  if (!brain.wallets[w.address]) {
    brain.wallets[w.address] = {
      success: 1,
      fail: 1,
      lastUsed: 0
    };
  }
});

// ===== PICK WALLET =====
function pickWallet(provider) {
  let best = null;
  let score = -1;

  for (let w of wallets) {
    const data = brain.wallets[w.address];

    const rate = data.success / (data.success + data.fail);
    const cooldown = Date.now() - data.lastUsed;

    const s = rate + cooldown / 1e6;

    if (s > score) {
      score = s;
      best = w.connect(provider);
    }
  }

  return best;
}

// ===== DECISION =====
function decideAction() {
  const actions = ["tx", "api", "swap", "idle"];

  const weights = [0.2, 0.2, 0.4, 0.2];

  const rand = Math.random();
  let sum = 0;

  for (let i = 0; i < actions.length; i++) {
    sum += weights[i];
    if (rand < sum) return actions[i];
  }
}

// ===== LIMIT =====
let txCount = 0;
setInterval(() => { txCount = 0; }, 60 * 60 * 1000);

// ===== ACTIONS =====
async function doTx(wallet) {
  if (txCount >= MAX_TX) return;

  try {
    const amount = (Math.random() * 0.00002).toFixed(6);

    const tx = await wallet.sendTransaction({
      to: wallet.address,
      value: ethers.parseEther(amount)
    });

    console.log("💸 TX:", tx.hash);

    brain.wallets[wallet.address].success++;
    txCount++;

  } catch {
    console.log("❌ TX FAIL");
    brain.wallets[wallet.address].fail++;
  }

  brain.wallets[wallet.address].lastUsed = Date.now();
}

async function doAPI() {
  try {
    await axios.get("https://api.coingecko.com/api/v3/ping");
    console.log("🌐 API OK");
  } catch {
    console.log("❌ API FAIL");
  }
}

// 🔥 SWAP dApp
async function doSwap(wallet) {
  if (txCount >= MAX_TX) return;

  const decision = await shouldSwap();

  if (!decision) {
    console.log("⛔ Skip swap (strategy)");
    return;
  }

  try {
    const router = new ethers.Contract(
      process.env.DEX_ROUTER,
      routerAbi,
      wallet
    );

    const amountIn = ethers.parseEther("0.00001");

    const tx = await router.swapExactETHForTokens(
      0,
      [process.env.TOKEN_IN, process.env.TOKEN_OUT],
      wallet.address,
      Math.floor(Date.now() / 1000) + 600,
      { value: amountIn }
    );

    console.log("🔄 SMART SWAP:", tx.hash);

    brain.defi.swap_success++;
    brain.wallets[wallet.address].success++;
    txCount++;

  } catch {
    console.log("❌ SWAP FAIL");

    brain.defi.swap_fail++;
    brain.wallets[wallet.address].fail++;
  }

  brain.wallets[wallet.address].lastUsed = Date.now();
}

// ===== DELAY =====
function delay() {
  const min = parseInt(process.env.MIN_DELAY);
  const max = parseInt(process.env.MAX_DELAY);
  return Math.random() * (max - min) + min;
}

// ===== LOOP =====
async function run() {
  const provider = getProvider();
  const wallet = pickWallet(provider);
  const action = decideAction();

  console.log("🧠 Action:", action);

  if (action === "tx") await doTx(wallet);
  if (action === "api") await doAPI();
  if (action === "swap") await doSwap(wallet);
  if (action === "idle") console.log("😴 Idle");

  save();

  setTimeout(run, delay());
}
async function getPrice() {
  try {
    const res = await axios.get(
      "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    );

    return res.data.ethereum.usd;
  } catch {
    return null;
  }
}
async function shouldSwap() {
  const price = await getPrice();

  if (!price) return false;

  // ambil success rate
  const successRate =
    brain.defi.swap_success /
    (brain.defi.swap_success + brain.defi.swap_fail);

  // strategi sederhana:
  // kalau harga rendah ATAU success tinggi → swap
  if (price < 3000 || successRate > 0.6) {
    return true;
  }

  return false;
}
run();