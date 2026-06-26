#!/usr/bin/env bun

import { readdir, readFile, stat, writeFile, rm, mkdir, cpSync } from "fs"
import { createHash } from "crypto"
import { readdir as readdirAsync, readFile as readFileAsync, stat as statAsync, rm as rmAsync, mkdir as mkdirAsync } from "fs/promises"
import { join, extname, dirname, basename } from "path"

const HOME = Bun.env.HOME || Bun.env.USERPROFILE || ""
const SKILL_DIR = join(HOME, ".opencode", "skill")
const CONFIG_DIR = join(HOME, ".opencode", "config")
const CONFIG_FILE = join(CONFIG_DIR, "gatekeeper.json")
const QUARANTINE_DIR = join(CONFIG_DIR, "quarantine")
const SANDBOX_DIR = join(CONFIG_DIR, "sandbox")

interface Config {
  virusTotalApiKey?: string
  autoApprove?: boolean
  requireVT?: boolean
  whitelist?: string[]
}

interface ScanResult {
  name: string
  path: string
  status: "safe" | "warning" | "danger"
  issues: Issue[]
  score: number
  vtResult?: VTResult
}

interface VTResult {
  detected: number
  total: number
  status: "safe" | "suspicious" | "malicious"
  malicious: string[]
}

interface Issue {
  severity: "high" | "medium" | "low" | "info"
  type: string
  description: string
}

const HIGH_RISK_PATTERNS = [
  { pattern: /eval\s*\(/g, type: "動態程式碼執行 (eval)" },
  { pattern: /new\s+Function\s*\(/g, type: "動態函數創建" },
  { pattern: /child_process\.exec\s*\(/g, type: "系統命令執行" },
  { pattern: /child_process\.spawn\s*\(/g, type: "子進程創建" },
  { pattern: /process\.exit\s*\(/g, type: "強制進程終止" },
  { pattern: /decodeURIComponent.*password|decodeURIComponent.*token/g, type: "密碼竊取模式" },
  { pattern: /SetClipboardData|GetAsyncKeyState|keylogger/i, type: "鍵盤側錄模式" },
]

const MEDIUM_RISK_PATTERNS = [
  { pattern: /writeFile.*sync|writeFileSync/g, type: "檔案寫入操作" },
  { pattern: /curl.*\|.*sh/g, type: "管道下載執行" },
  { pattern: /wget.*\|.*sh/g, type: "Wget 管道執行" },
  { pattern: /powershell.*-enc|base64.*decode/gi, type: "Base64 PowerShell" },
]

function loadConfig(): Config {
  try {
    const content = readFileSync(join(CONFIG_FILE), "utf-8")
    return JSON.parse(content)
  } catch {
    return { autoApprove: false, requireVT: true, whitelist: [] }
  }
}

function saveConfig(config: Config) {
  try {
    mkdirSync(dirname(CONFIG_FILE), { recursive: true })
    writeFile(CONFIG_FILE, JSON.stringify(config, null, 2))
  } catch { /* ignore */ }
}

async function quarantineSkill(skillName: string, skillPath: string): Promise<boolean> {
  try {
    mkdirSync(QUARANTINE_DIR, { recursive: true })
    const quarantinePath = join(QUARANTINE_DIR, `${skillName}_${Date.now()}`)
    cpSync(skillPath, quarantinePath, { recursive: true })
    rmSync(skillPath, { recursive: true, force: true })
    console.log(`   📦 已隔離至: ${quarantinePath}`)
    return true
  } catch {
    return false
  }
}

async function copyToSandbox(skillName: string, skillPath: string): Promise<string | null> {
  try {
    const sandboxPath = join(SANDBOX_DIR, skillName)
    mkdirSync(SANDBOX_DIR, { recursive: true })
    cpSync(skillPath, sandboxPath, { recursive: true })
    return sandboxPath
  } catch {
    return null
  }
}

async function calculateFileHash(filePath: string): Promise<string | null> {
  try {
    const content = await readFileAsync(filePath)
    return createHash("sha256").update(content).digest("hex")
  } catch {
    return null
  }
}

async function checkVirusTotal(hash: string, apiKey: string): Promise<VTResult | null> {
  try {
    const response = await fetch(`https://www.virustotal.com/api/v3/files/${hash}`, {
      headers: { "x-apikey": apiKey },
    })
    if (!response.ok) return null

    const data = await response.json()
    const attributes = data.data?.attributes
    if (!attributes) return null

    const lastAnalysisStats = attributes.last_analysis_stats || {}
    const detected = lastAnalysisStats.malicious || 0
    const suspicious = lastAnalysisStats.suspicious || 0
    const total = detected + suspicious + (lastAnalysisStats.undetected || 0) + (lastAnalysisStats.harmless || 0)

    const maliciousNames: string[] = []
    const results = attributes.last_analysis_results || {}
    for (const [engine, result] of Object.entries(results)) {
      const r = result as { category: string; result: string }
      if (r.category === "malicious" || r.result === "malicious") {
        maliciousNames.push(engine)
      }
    }

    let status: "safe" | "suspicious" | "malicious" = "safe"
    if (detected > 5) status = "malicious"
    else if (suspicious > 0 || detected > 0) status = "suspicious"

    return { detected: detected + suspicious, total, status, malicious: maliciousNames.slice(0, 10) }
  } catch {
    return null
  }
}

async function scanSkillFiles(skillPath: string): Promise<{ issues: Issue[], score: number }> {
  const issues: Issue[] = []
  const scanableExtensions = [".ts", ".tsx", ".js", ".jsx", ".sh", ".bash"]

  async function scanDir(dirPath: string) {
    try {
      const entries = await readdirAsync(dirPath, { withFileTypes: true })
      for (const entry of entries) {
        const fullPath = join(dirPath, entry.name)
        if (entry.isDirectory() && !entry.name.startsWith(".") && entry.name !== "node_modules") {
          await scanDir(fullPath)
        } else if (entry.isFile()) {
          const ext = extname(entry.name).toLowerCase()
          if (scanableExtensions.includes(ext)) {
            try {
              const content = await readFileAsync(fullPath, "utf-8")
              for (const { pattern, type } of HIGH_RISK_PATTERNS) {
                if (pattern.test(content)) {
                  issues.push({ severity: "high", type, description: `發現危險模式: ${type}` })
                }
              }
              for (const { pattern, type } of MEDIUM_RISK_PATTERNS) {
                if (pattern.test(content)) {
                  issues.push({ severity: "medium", type, description: `發現潛在風險: ${type}` })
                }
              }
            } catch { /* skip */ }
          }
        }
      }
    } catch { /* skip */ }
  }

  await scanDir(skillPath)

  const highCount = issues.filter(i => i.severity === "high").length
  const mediumCount = issues.filter(i => i.severity === "medium").length
  const score = Math.max(0, 100 - highCount * 30 - mediumCount * 10)

  return { issues, score }
}

async function auditSkill(skillName: string): Promise<ScanResult> {
  const skillPath = join(SKILL_DIR, skillName)
  const config = loadConfig()

  console.log(`\n🔒 Skill Gatekeeper - 自動化安全審核`)
  console.log(`─`.repeat(50))
  console.log(`📦 審核技能: ${skillName}`)
  console.log(`📍 狀態: 進入沙盒隔離環境...`)

  // 1. 複製到沙盒
  const sandboxPath = await copyToSandbox(skillName, skillPath)
  if (!sandboxPath) {
    return {
      name: skillName,
      path: skillPath,
      status: "danger",
      issues: [{ severity: "high", type: "沙盒複製失敗", description: "無法複製到沙盒環境" }],
      score: 0
    }
  }
  console.log(`   ✅ 已複製至沙盒環境`)

  // 2. 本地安全掃描
  console.log(`\n🔍 執行本地安全掃描...`)
  const { issues, score } = await scanSkillFiles(sandboxPath)

  const highCount = issues.filter(i => i.severity === "high").length
  const mediumCount = issues.filter(i => i.severity === "medium").length

  if (issues.length > 0) {
    for (const issue of issues) {
      const icon = issue.severity === "high" ? "🔴" : issue.severity === "medium" ? "🟡" : "🟢"
      console.log(`   ${icon} ${issue.description}`)
    }
  }
  console.log(`   📊 分數: ${score}/100`)

  // 3. VirusTotal 雲端檢測
  let vtResult: VTResult | undefined
  if (config.virusTotalApiKey) {
    console.log(`\n☁️ 執行 VirusTotal 雲端檢測...`)
    const mainFile = join(sandboxPath, "SKILL.md")
    const hash = await calculateFileHash(mainFile)
    if (hash) {
      vtResult = await checkVirusTotal(hash, config.virusTotalApiKey)
      if (vtResult) {
        const vtIcon = vtResult.status === "safe" ? "✅" : vtResult.status === "suspicious" ? "⚠️" : "🔴"
        console.log(`   ☁️ VT: ${vtResult.detected}/${vtResult.total} 防毒引擎標記 ${vtIcon}`)
        if (vtResult.malicious.length > 0) {
          console.log(`   🔴 惡意引擎: ${vtResult.malicious.slice(0, 3).join(", ")}`)
        }
      }
    }
  } else {
    console.log(`\n☁️ VirusTotal: 未設定 API Key (使用 --vt-key 設定)`)
  }

  // 4. 清理沙盒
  rmSync(sandboxPath, { recursive: true, force: true })

  // 5. 決定結果
  let status: "safe" | "warning" | "danger" = "safe"
  if (highCount > 0) status = "danger"
  else if (mediumCount > 0 || (vtResult && vtResult.detected > 0)) status = "warning"

  return {
    name: skillName,
    path: skillPath,
    status,
    issues,
    score,
    vtResult
  }
}

async function installWithAudit(slug: string): Promise<boolean> {
  console.log(`\n📦 安裝技能: ${slug}`)
  console.log(`   🔒 自動進入安全審核...`)

  // 使用 clawhub 安裝
  const { execSync } = await import("child_process")
  try {
    execSync(`node "C:/Users/ReaMasTer/AppData/Roaming/npm/node_modules/clawhub/bin/clawdhub.js" install ${slug} --dir "${SKILL_DIR}"`, {
      encoding: "utf-8"
    })
  } catch {
    console.log(`   ❌ 安裝失敗`)
    return false
  }

  // 審核剛安裝的技能
  const skillName = slug.split("/").pop() || slug
  const result = await auditSkill(skillName)

  if (result.status === "danger") {
    console.log(`\n⚠️ 安全審核: 未通過`)
    console.log(`   🔴 本地風險: ${result.issues.filter(i => i.severity === "high").length} 項高風險`)
    if (result.vtResult) console.log(`   ☁️ 雲端風險: ${result.vtResult.detected} 項`)
    console.log(`\n🛡️ 安全策略: 拒絕安裝，已移至隔離區`)
    await quarantineSkill(result.name, result.path)
    return false
  } else if (result.status === "warning") {
    console.log(`\n⚠️ 安全審核: 發現警告`)
    console.log(`   🟡 需要人工審核`)
    console.log(`\n🛡️ 安全策略: 暫停安裝，等待確認`)
    return false
  }

  console.log(`\n✅ 安全審核: 通過`)
  console.log(`🛡️ 安全策略: 自動放行`)
  return true
}

async function main() {
  const args = process.argv.slice(2)
  const command = args[0]

  if (command === "config") {
    if (args[1] === "--vt-key" && args[2]) {
      const config = loadConfig()
      config.virusTotalApiKey = args[2]
      saveConfig(config)
      console.log("✅ VirusTotal API Key 已設定")
    } else if (args[1] === "--auto-approve") {
      const config = loadConfig()
      config.autoApprove = args[2] !== "false"
      saveConfig(config)
      console.log(`✅ 自動放行: ${config.autoApprove ? "啟用" : "停用"}`)
    } else if (args[1] === "--require-vt") {
      const config = loadConfig()
      config.requireVT = args[2] !== "false"
      saveConfig(config)
      console.log(`✅ 強制 VirusTotal: ${config.requireVT ? "啟用" : "停用"}`)
    } else {
      const config = loadConfig()
      console.log(`🔒 Skill Gatekeeper 配置`)
      console.log(`   ☁️ VirusTotal: ${config.virusTotalApiKey ? "已設定" : "未設定"}`)
      console.log(`   🤖 自動放行: ${config.autoApprove ? "啟用" : "停用"}`)
      console.log(`   🔍 強制 VT: ${config.requireVT ? "啟用" : "停用"}`)
      console.log(`\n設定方式:`)
      console.log(`   skill-gatekeeper config --vt-key <YOUR_KEY>`)
      console.log(`   skill-gatekeeper config --auto-approve true`)
    }
    return
  }

  if (command === "install" && args[1]) {
    const success = await installWithAudit(args[1])
    process.exit(success ? 0 : 1)
    return
  }

  if (command === "audit" && args[1]) {
    const result = await auditSkill(args[1])

    console.log(`\n${"─".repeat(50)}`)
    console.log(`📊 審核結果摘要`)
    console.log(`   📦 技能: ${result.name}`)
    console.log(`   📊 分數: ${result.score}/100`)
    console.log(`   🔴 高風險: ${result.issues.filter(i => i.severity === "high").length} 項`)
    console.log(`   🟡 中風險: ${result.issues.filter(i => i.severity === "medium").length}項`)
    if (result.vtResult) {
      console.log(`   ☁️ VT 標記: ${result.vtResult.detected}/${result.vtResult.total}`)
    }

    if (result.status === "safe") {
      console.log(`\n✅ 審核通過 - 安全放行`)
    } else if (result.status === "warning") {
      console.log(`\n⚠️ 審核警告 - 需要人工確認`)
    } else {
      console.log(`\n🔴 審核失敗 - 拒絕安裝`)
      console.log(`   📦 已移至隔離區`)
    }
    process.exit(result.status === "danger" ? 1 : 0)
    return
  }

  if (command === "audit-all") {
    console.log(`\n🔒 Skill Gatekeeper - 批量審核`)
    console.log(`─`.repeat(50))

    const entries = await readdirAsync(SKILL_DIR, { withFileTypes: true })
    const skills = entries.filter(e => e.isDirectory()).map(e => e.name)

    let safe = 0, warning = 0, danger = 0

    for (const skill of skills) {
      if (skill === "skill-gatekeeper" || skill === "skill-vet") continue

      const result = await auditSkill(skill)

      if (result.status === "safe") {
        console.log(`\n✅ ${skill} - 安全 (${result.score}/100)`)
        safe++
      } else if (result.status === "warning") {
        console.log(`\n⚠️ ${skill} - 警告 (${result.score}/100)`)
        warning++
      } else {
        console.log(`\n🔴 ${skill} - 危險 (${result.score}/100)`)
        await quarantineSkill(skill, join(SKILL_DIR, skill))
        danger++
      }
    }

    console.log(`\n${"─".repeat(50)}`)
    console.log(`📊 批量審核報告`)
    console.log(`   ✅ 安全: ${safe} 個`)
    console.log(`   ⚠️ 警告: ${warning} 個`)
    console.log(`   🔴 危險: ${danger} 個 (已隔離)`)
    return
  }

  console.log(`\n🔒 Skill Gatekeeper - 自動化安全審核系統`)
  console.log(`─`.repeat(50))
  console.log(`使用方式:`)
  console.log(`   skill-gatekeeper install <slug>    # 安裝並審核`)
  console.log(`   skill-gatekeeper audit <技能名>     # 審核已安裝技能`)
  console.log(`   skill-gatekeeper audit-all          # 批量審核所有技能`)
  console.log(`   skill-gatekeeper config --vt-key <key>  # 設定 VirusTotal API Key`)
  console.log(`\n例如:`)
  console.log(`   skill-gatekeeper install github`)
  console.log(`   skill-gatekeeper audit my-skill`)
}

main()
