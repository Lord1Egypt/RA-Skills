const args = process.argv.slice(2);

/**
 * Usage: node monitor.js <current_tokens> <max_tokens> <current_model> [quota_remaining_percent]
 */

if (args.length < 3) {
  console.log("Usage: node monitor.js <current_tokens> <max_tokens> <current_model> [quota_remaining_percent]");
  process.exit(1);
}

const current = parseInt(args[0], 10);
const max = parseInt(args[1], 10);
const model = args[2];
const quota = args[3] || "N/A";

const ratio = (current / max);
const percent = Math.round(ratio * 100);

// Generate progress bar
const barLength = 10;
const filledLength = Math.round(ratio * barLength);
const bar = "▓".repeat(Math.min(filledLength, barLength)) + "░".repeat(Math.max(0, barLength - filledLength));

let riskLevel = "正常";
let color = "🟢";

if (ratio >= 0.95) {
  riskLevel = "緊急 (Critical)";
  color = "🔴";
} else if (ratio >= 0.85) {
  riskLevel = "警告 (Warning)";
  color = "🟡";
}

console.log(`
---
### 🛡️ Token Guard 狀態回報
**【風險等級：${riskLevel} ${color}】** 
- **目前模型：** ${model}
- **上下文負載：** \`[${bar}] ${percent}%\`
- **剩餘配額：** ${quota}%

**⚠️ 診測建議：** ${ratio >= 0.85 ? "建議立即執行 /compact 或換模型以免中斷。" : "目前尚在安全範圍，請繼續任務。"}
---
`);
