#!/usr/bin/env node
/**
 * wendao-agent CLI
 * 用法: AGENT_PRIVATE_KEY=0x... npx wendao-agent start --token-id 1 --strategy balanced
 *
 * SDK-01: 私钥优先从环境变量 AGENT_PRIVATE_KEY 读取，避免暴露在 shell history 中
 * SDK-05: 合约地址可通过环境变量覆盖
 */
import { Command } from "commander";
import { WenDaoAgent } from "./agent.js";
const BSC_RPC = process.env.BSC_RPC_URL || "https://bsc-dataseed1.bnbchain.org";
// SDK-05: 合约地址支持环境变量覆盖
const CONTRACTS = {
    nfa: process.env.NFA_ADDRESS || "0x3b8d8B6A9Aa1efC474A4eb252048D628569Dd842",
    vault: process.env.VAULT_ADDRESS || "0x5FF4F77213AF077fF82270B32916F62900a1DA61",
    token: process.env.TOKEN_ADDRESS || "0x869f5d274122a91D98f4fbE4f576C351808dDa29",
};
const program = new Command();
program
    .name("wendao-agent")
    .description("🏮 问道 NFA Agent — BAP-578 自主修仙")
    .version("1.0.0");
program
    .command("start")
    .description("启动 Agent 自动修仙")
    .option("--key <privateKey>", "Agent 钱包私钥（推荐使用环境变量 AGENT_PRIVATE_KEY）")
    .requiredOption("--token-id <id>", "NFA tokenId", parseInt)
    .option("--strategy <type>", "策略: aggressive|defensive|balanced", "balanced")
    .option("--interval <seconds>", "行动间隔（秒）", "300")
    .option("--rpc <url>", "BSC RPC URL", BSC_RPC)
    .option("--api <url>", "后端 API URL", "https://wendaobsc.xyz")
    .action(async (opts) => {
    // SDK-01: 优先从环境变量读私钥
    const privateKey = process.env.AGENT_PRIVATE_KEY || opts.key;
    if (!privateKey) {
        console.error("❌ 缺少私钥。请设置环境变量 AGENT_PRIVATE_KEY 或使用 --key 参数");
        console.error("   推荐: export AGENT_PRIVATE_KEY=0x...");
        console.error("   ⚠️ 注意：--key 参数会暴露在 shell history 中，不推荐使用");
        process.exit(1);
    }
    if (opts.key) {
        console.warn("⚠️ 警告：通过 --key 传入私钥会暴露在 shell history 中，推荐使用环境变量 AGENT_PRIVATE_KEY");
    }
    const agent = new WenDaoAgent({
        agentPrivateKey: privateKey,
        rpcUrl: opts.rpc,
        tokenId: opts.tokenId,
        contracts: CONTRACTS,
        apiUrl: opts.api,
        strategy: opts.strategy,
        interval: parseInt(opts.interval),
    });
    agent.on("error", (err) => console.error("❌ Agent 错误:", err.message));
    // 优雅退出
    process.on("SIGINT", () => { agent.stop(); process.exit(0); });
    process.on("SIGTERM", () => { agent.stop(); process.exit(0); });
    await agent.start();
});
program
    .command("status")
    .description("查看 NFA 当前状态")
    .option("--key <privateKey>", "Agent 钱包私钥（推荐使用环境变量 AGENT_PRIVATE_KEY）")
    .requiredOption("--token-id <id>", "NFA tokenId", parseInt)
    .option("--rpc <url>", "BSC RPC URL", BSC_RPC)
    .action(async (opts) => {
    const privateKey = process.env.AGENT_PRIVATE_KEY || opts.key;
    if (!privateKey) {
        console.error("❌ 缺少私钥。请设置环境变量 AGENT_PRIVATE_KEY");
        process.exit(1);
    }
    const agent = new WenDaoAgent({
        agentPrivateKey: privateKey,
        rpcUrl: opts.rpc,
        tokenId: opts.tokenId,
        contracts: CONTRACTS,
        apiUrl: "",
        strategy: "balanced",
    });
    const state = await agent.getState();
    const REALMS = ["炼气", "筑基", "金丹", "元婴", "化神", "炼虚", "合道", "大乘"];
    console.log(`\n🏮 修士 #${state.tokenId} — ${state.warrior.xHandle}`);
    console.log(`   境界: ${REALMS[state.warrior.realm]} Lv.${state.warrior.level}`);
    console.log(`   修为: ${state.warrior.xp} / ${state.xpToNextLevel} XP`);
    console.log(`   未分配SP: ${state.warrior.unspentSP}`);
    console.log(`   五维: STR=${state.warrior.baseStats[0]} AGI=${state.warrior.baseStats[1]} END=${state.warrior.baseStats[2]} INT=${state.warrior.baseStats[3]} CON=${state.warrior.baseStats[4]}`);
    console.log(`   闭关: ${state.isMeditating ? "是" : "否"}`);
    console.log(`   论道: ${state.isInPK ? "是" : "否"}`);
    console.log(`   质押: ${Number(state.staked) / 1e18} $JW`);
    console.log(`   待领: ${Number(state.pendingReward) / 1e18} $JW`);
    console.log(`   Agent $JW: ${Number(state.jwBalance) / 1e18}`);
    console.log(`   Agent BNB: ${Number(state.bnbBalance) / 1e18}`);
});
program.parse();
//# sourceMappingURL=cli.js.map