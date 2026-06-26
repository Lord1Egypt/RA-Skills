#!/usr/bin/env bun

import { readdir, readFile, stat, writeFile, rm, mkdir, cpSync } from "fs"
import { createHash } from "crypto"
import { readdir as readdirAsync, readFile as readFileAsync, stat as statAsync, rm as rmAsync, mkdir as mkdirAsync } from "fs/promises"
import { join, extname, dirname, basename } from "path"

const HOME = Bun.env.HOME || Bun.env.USERPROFILE || ""
const SKILL_DIR = join(HOME, ".opencode", "skill")
const CONFIG_DIR = join(HOME, ".opencode", "config")
const CONFIG_FILE = join(CONFIG_DIR, "security-scan.json")
const QUARANTINE_DIR = join(CONFIG_DIR, "quarantine")
const LOG_FILE = join(CONFIG_DIR, "security-scan.log")

const SAFE_SKILLS = [
  "skill-vet",
  "skill-gatekeeper",
  "skill-security-vet",
  "sandwrap",
  "security-auto",
  "security-shield",
  "healthcheck",
  "ai-debug",
  "ai-memory",
  "self-repair"
]

interface Config {
  autoScanOnStartup?: boolean
  virusTotalApiKey?: string
  autoQuarantine?: boolean
  lastScanTime?: number
  scanInterval?: number
  findings?: Finding[]
}

interface Finding {
  skill: string
  time: number
  status: "safe" | "warning" | "danger"
  score: number
  issues: string[]
  action: "allowed" | "quarantined" | "removed"
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
  { pattern: /socket\.connect.*22|socket\.connect.*3389/g, type: "遠程連接攻擊" },
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
    return { autoScanOnStartup: true, autoQuarantine: true, scanInterval: 86400000, findings: [] }
  }
}

function saveConfig(config: Config) {
  try {
    mkdirSync(dirname(CONFIG_FILE), { recursive: true })
    writeFile(CONFIG_FILE, JSON.stringify(config, null, 2))
  } catch { /* ignore */ }
}

function log(message: string) {
  const timestamp = new Date().toISOString()
  const logLine = `[${timestamp}] ${message}\n`
  try {
    appendFileSync(LOG_FILE, logLine)
  } catch { /* ignore */ }
  console.log(message)
}

async function quarantineSkill(skillName: string, skillPath: string): Promise<boolean> {
  try {
    mkdirSync(QUARANTINE_DIR, { recursive: true })
    const quarantinePath = join(QUARANTINE_DIR, `${skillName}_${Date.now()}`)
    cpSync(skillPath, quarantinePath, { recursive: true })
    rmSync(skillPath, { recursive: true, force: true })
    return true
  } catch {
    return false
  }
}

async function scanSkill(skillName: string): Promise<{ issues: Issue[], score: number, status: "safe" | "warning" | "danger" }> {
  const skillPath = join(SKILL_DIR, skillName)
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
                  issues.push({ severity: "high", type, description: type })
                }
              }
              for (const { pattern, type } of MEDIUM_RISK_PATTERNS) {
                if (pattern.test(content)) {
                  issues.push({ severity: "medium", type, description: type })
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
  const status = highCount > 0 ? "danger" : mediumCount > 0 ? "warning" : "safe"

  return { issues, score, status }
}

async function runSecurityScan(autoAction: boolean = true) {
  const config = loadConfig()
  const timestamp = Date.now()

  log(`
╔══════════════════════════════════════════════════════════════╗
║     🔒 OpenCode 技能安全掃描 - 啟動時自動檢查              ║
╚══════════════════════════════════════════════════════════════╝`)

  const entries = await readdirAsync(SKILL_DIR, { withFileTypes: true })
  const skills = entries.filter(e => e.isDirectory()).map(e => e.name)

  log(`📁 掃描目錄: ${SKILL_DIR}`)
  log(`🎯 技能數量: ${skills.length} 個`)
  log(`🤖 自動處理: ${autoAction && config.autoQuarantine ? "啟用" : "停用"}`)
  log(`─`.repeat(60))

  let safe = 0, warning = 0, danger = 0
  const newFindings: Finding[] = []

  for (const skill of skills) {
    if (SAFE_SKILLS.includes(skill)) {
      log(`🛡️ ${skill}: 安全工具，跳過掃描`)
      safe++
      newFindings.push({ skill, time: timestamp, status: "safe", score: 100, issues: [], action: "allowed" })
      continue
    }

    const result = await scanSkill(skill)
    const icon = result.status === "safe" ? "✅" : result.status === "warning" ? "⚠️" : "🔴"
    const statusText = result.status === "safe" ? "安全" : result.status === "warning" ? "警告" : "危險"

    log(`${icon} ${skill}: ${statusText} (${result.score}/100)`)

    if (result.issues.length > 0) {
      for (const issue of result.issues.slice(0, 3)) {
        const issueIcon = issue.severity === "high" ? "🔴" : issue.severity === "medium" ? "🟡" : "🟢"
        log(`   ${issueIcon} ${issue.description}`)
      }
    }

    if (result.status === "safe") safe++
    else if (result.status === "warning") warning++
    else danger++

    const finding: Finding = {
      skill,
      time: timestamp,
      status: result.status,
      score: result.score,
      issues: result.issues.map(i => i.description),
      action: result.status === "danger" && autoAction && config.autoQuarantine ? "quarantined" : "allowed"
    }

    if (result.status === "danger" && autoAction && config.autoQuarantine) {
      const skillPath = join(SKILL_DIR, skill)
      const success = await quarantineSkill(skill, skillPath)
      if (success) {
        log(`   📦 已自動隔離危險技能`)
        finding.action = "quarantined"
      }
    }

    newFindings.push(finding)
  }

  log(`─`.repeat(60))
  log(`📊 掃描報告`)
  log(`   ✅ 安全: ${safe} 個`)
  log(`   ⚠️ 警告: ${warning} 個`)
  log(`   🔴 危險: ${danger} 個`)

  config.findings = newFindings
  config.lastScanTime = timestamp
  saveConfig(config)

  if (danger > 0 && autoAction && config.autoQuarantine) {
    log(`
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  安全警告: 發現 ${danger} 個危險技能，已自動隔離！        ║
╚══════════════════════════════════════════════════════════════╝`)
  } else if (danger === 0 && warning === 0) {
    log(`
╔══════════════════════════════════════════════════════════════╗
║  ✅  安全狀態: 所有技能掃描通過，系統安全                   ║
╚══════════════════════════════════════════════════════════════╝`)
  }

  log("")
}

async function main() {
  const args = process.argv.slice(2)

  if (args[0] === "enable") {
    const config = loadConfig()
    config.autoScanOnStartup = true
    saveConfig(config)
    log("✅ 啟動時自動掃描已啟用")
    return
  }

  if (args[0] === "disable") {
    const config = loadConfig()
    config.autoScanOnStartup = false
    saveConfig(config)
    log("✅ 啟動時自動掃描已停用")
    return
  }

  if (args[0] === "status") {
    const config = loadConfig()
    log("🔒 OpenCode 安全掃描設定")
    log(`   啟動時掃描: ${config.autoScanOnStartup ? "啟用" : "停用"}`)
    log(`   自動隔離: ${config.autoQuarantine ? "啟用" : "停用"}`)
    log(`   上次掃描: ${config.lastScanTime ? new Date(config.lastScanTime).toLocaleString() : "從未掃描"}`)
    log(`   發現問題: ${config.findings?.filter(f => f.status !== "safe").length || 0} 個`)
    return
  }

  if (args[0] === "log") {
    try {
      const log = readFileSync(LOG_FILE, "utf-8")
      console.log(log)
    } catch {
      console.log("無掃描日誌")
    }
    return
  }

  await runSecurityScan(true)
}

main()
