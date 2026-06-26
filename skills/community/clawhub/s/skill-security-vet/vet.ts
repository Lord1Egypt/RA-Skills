#!/usr/bin/env bun

import { readdir, readFile, stat, writeFile, rm, mkdir } from "fs"
import { createHash } from "crypto"
import { readdir as readdirAsync, readFile as readFileAsync, stat as statAsync, rm as rmAsync, mkdir as mkdirAsync, readFile as readFileSync } from "fs/promises"
import { join, extname, dirname, basename } from "path"

const HOME = Bun.env.HOME || Bun.env.USERPROFILE || ""
const SKILL_DIR = join(HOME, ".opencode", "skill")
const CONFIG_DIR = join(HOME, ".opencode", "config")
const CONFIG_FILE = join(CONFIG_DIR, "skill-vet.json")
const QUARANTINE_DIR = join(CONFIG_DIR, "quarantine")
const SYSTEM_DRIVES = process.platform === "win32" ? ["C:", "D:", "E:", "F:"] : ["/"]

interface Config {
  virusTotalApiKey?: string
  autoRemove?: boolean
  autoQuarantine?: boolean
  whitelist?: string[]
  excludePaths?: string[]
}

interface ScanResult {
  name: string
  path: string
  status: "safe" | "warning" | "danger"
  issues: Issue[]
  score: number
  vtResult?: VTResult
  removed?: boolean
  quarantined?: boolean
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
  file?: string
  line?: number
  description: string
}

const HIGH_RISK_PATTERNS = [
  { pattern: /eval\s*\(/g, type: "動態程式碼執行 (eval)" },
  { pattern: /new\s+Function\s*\(/g, type: "動態函數創建" },
  { pattern: /child_process\.exec\s*\(/g, type: "系統命令執行" },
  { pattern: /child_process\.spawn\s*\(/g, type: "子進程創建" },
  { pattern: /process\.exit\s*\(/g, type: "強制進程終止" },
  { pattern: /rm\s+-rf\s+\//g, type: "危險刪除命令" },
  { pattern: /decodeURIComponent.*password|decodeURIComponent.*token/g, type: "密碼竊取模式" },
  { pattern: /SetClipboardData|GetAsyncKeyState|keylogger/i, type: "鍵盤側錄模式" },
  { pattern: /socket\.connect.*22|socket\.connect.*3389/g, type: "遠程連接攻擊" },
  { pattern: /WebBrowser\.Navigate|Shell\.Exec|WScript\.Shell/i, type: "惡意腳本模式" },
]

const MEDIUM_RISK_PATTERNS = [
  { pattern: /writeFile.*sync|writeFileSync/g, type: "檔案寫入操作" },
  { pattern: /JSON\.parse.*fetch/g, type: "解析外部 JSON" },
  { pattern: /chmod\s+\d{3,4}/g, type: "修改檔案權限" },
  { pattern: /sudo\s+/g, type: "使用系統管理員權限" },
  { pattern: /curl.*\|.*sh/g, type: "管道下載執行" },
  { pattern: /wget.*\|.*sh/g, type: "Wget 管道執行" },
  { pattern: /powershell.*-enc|powershell.*-encodedcommand/gi, type: "Base64 PowerShell" },
]

const SUSPICIOUS_EXTENSIONS = [".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jse", ".wsf", ".scr", ".pif", ".msi", ".com"]

function loadConfig(): Config {
  try {
    const content = readFileSync(join(CONFIG_FILE), "utf-8")
    return JSON.parse(content)
  } catch {
    return { autoRemove: false, autoQuarantine: true, whitelist: [], excludePaths: ["node_modules", ".git", "Windows", "Program Files"] }
  }
}

function saveConfig(config: Config) {
  try {
    mkdirSync(dirname(CONFIG_FILE), { recursive: true })
    const { writeFileSync } = require("fs")
    writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2))
  } catch {
    // ignore
  }
}

async function quarantineFile(filePath: string): Promise<boolean> {
  try {
    const quarantinePath = join(QUARANTINE_DIR, `${basename(filePath)}_${Date.now()}`)
    mkdirSync(QUARANTINE_DIR, { recursive: true })
    const { cpSync } = require("fs")
    cpSync(filePath, quarantinePath)
    rmSync(filePath, { force: true })
    console.log(`   📦 已隔離至: ${quarantinePath}`)
    return true
  } catch {
    return false
  }
}

async function removeFile(filePath: string): Promise<boolean> {
  try {
    rmSync(filePath, { force: true })
    return true
  } catch {
    return false
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
    const total = detected + suspicious + (lastAnalysisStats.undetected || 0) + (lastAnalysisStats.harmless || 0) + (lastAnalysisStats.unsupported || 0) + (lastAnalysisStats["type-unsupported"] || 0)

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

async function scanFileContent(filePath: string, content: string): Promise<Issue[]> {
  const issues: Issue[] = []

  for (const { pattern, type } of HIGH_RISK_PATTERNS) {
    const matches = content.match(pattern)
    if (matches) {
      for (const match of matches) {
        const lineNum = content.substring(0, content.indexOf(match)).split("\n").length
        issues.push({ severity: "high", type, file: basename(filePath), line: lineNum, description: `${type}` })
      }
    }
  }

  for (const { pattern, type } of MEDIUM_RISK_PATTERNS) {
    const matches = content.match(pattern)
    if (matches) {
      for (const match of matches) {
        const lineNum = content.substring(0, content.indexOf(match)).split("\n").length
        issues.push({ severity: "medium", type, file: basename(filePath), line: lineNum, description: `${type}` })
      }
    }
  }

  return issues
}

async function scanLocalComputer(drive: string, config: Config): Promise<ScanResult[]> {
  const results: ScanResult[] = []
  const scannedFiles = new Set<string>()
  const maxFiles = 10000
  const scanableExtensions = [".js", ".ts", ".tsx", ".jsx", ".bat", ".cmd", ".ps1", ".vbs", ".py", ".rb", ".sh", ".bash"]

  const excludeSet = new Set([
    "node_modules", ".git", "Windows", "Program Files", "Program Files (x86)",
    "AppData/Local/Temp", "AppData/Local/Microsoft/Windows", "$Recycle.Bin",
    "System Volume Information", ".cache", ".npm", ".yarn"
  ])

  async function scanDir(dirPath: string, depth: number = 0) {
    if (depth > 5 || results.filter(r => r.status === "danger").length >= 10) return
    if (scannedFiles.size >= maxFiles) return

    try {
      const entries = await readdirAsync(dirPath, { withFileTypes: true })
      for (const entry of entries) {
        if (scannedFiles.size >= maxFiles) break
        if (excludeSet.has(entry.name)) continue

        const fullPath = join(dirPath, entry.name)

        if (entry.isDirectory()) {
          await scanDir(fullPath, depth + 1)
        } else if (entry.isFile()) {
          const ext = extname(entry.name).toLowerCase()
          
          // 掃描可疑副檔名
          if (SUSPICIOUS_EXTENSIONS.includes(ext)) {
            try {
              const content = await readFileAsync(fullPath, "utf-8")
              const issues = await scanFileContent(fullPath, content)

              if (issues.length > 0) {
                const highCount = issues.filter(i => i.severity === "high").length
                const score = Math.max(0, 100 - highCount * 30)

                results.push({
                  name: entry.name,
                  path: fullPath,
                  status: highCount > 0 ? "danger" : "warning",
                  issues,
                  score
                })
                scannedFiles.add(fullPath)
              }
            } catch {
              // 二進制檔案，跳過
            }
          }
        }
      }
    } catch {
      // 權限不足
    }
  }

  console.log(`\n📂 掃描硬碟: ${drive}`)
  await scanDir(drive)

  return results
}

async function main() {
  const args = process.argv.slice(2)
  let mode: "skill" | "local" | "full" = "skill"
  let targetSkills: string[] | null = null
  let minSeverity: "high" | "medium" | "low" | "info" = "info"
  let showDetails = true
  let enableVT = false
  let autoMode = false
  let configMode = false
  let newApiKey = ""

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "config" && args[i + 1] === "--api-key") {
      configMode = true
      newApiKey = args[i + 2] || ""
      i += 2
    } else if (args[i] === "config" && args[i + 1] === "--auto-remove") {
      configMode = true
      const config = loadConfig()
      config.autoRemove = args[i + 2] !== "false"
      saveConfig(config)
      console.log(`✅ 自動移除: ${config.autoRemove ? "已啟用" : "已停用"}`)
      return
    } else if (args[i] === "scan" && args[i + 1]) {
      targetSkills = args[i + 1].split(",")
      i++
    } else if (args[i] === "local" || args[i] === "--local") {
      mode = "local"
    } else if (args[i] === "full" || args[i] === "--full") {
      mode = "full"
    } else if (args[i] === "--vt" || args[i] === "--virustotal") {
      enableVT = true
    } else if (args[i] === "--auto" || args[i] === "-y") {
      autoMode = true
    } else if (args[i].startsWith("--severity=")) {
      const sev = args[i].split("=")[1]
      if (["high", "medium", "low", "info"].includes(sev)) {
        minSeverity = sev as typeof minSeverity
      }
    } else if (args[i] === "--quiet" || args[i] === "-q") {
      showDetails = false
    }
  }

  const config = loadConfig()

  if (configMode) {
    if (newApiKey) {
      config.virusTotalApiKey = newApiKey
      saveConfig(config)
      console.log("✅ VirusTotal API Key 已儲存")
    } else if (config.virusTotalApiKey) {
      console.log(`☁️ VirusTotal API Key: ${config.virusTotalApiKey.substring(0, 8)}...`)
      console.log(`🔒 自動移除: ${config.autoRemove ? "啟用" : "停用"}`)
    } else {
      console.log("❌ 未設定 VirusTotal API Key")
      console.log("   使用: skill-security-vet config --api-key <YOUR_KEY>")
    }
    return
  }

  console.log(`\n🔍 技能安全審核系統 v4.0`)
  console.log(`📊 模式: ${mode === "skill" ? "技能掃描" : mode === "local" ? "本地電腦掃描" : "完整掃描"}`)
  console.log(`☁️ VirusTotal: ${enableVT && config.virusTotalApiKey ? "已啟用" : "未啟用"}`)
  console.log(`🔒 自動模式: ${autoMode || config.autoRemove ? "已啟用" : "未啟用"}`)
  console.log(`─`.repeat(50))

  if (mode === "skill") {
    if (!targetSkills) {
      try {
        const entries = await readdirAsync(SKILL_DIR, { withFileTypes: true })
        targetSkills = entries.filter((e) => e.isDirectory()).map((e) => e.name).filter((name) => name !== "skill-vet")
      } catch {
        console.error(`❌ 無法讀取技能目錄: ${SKILL_DIR}`)
        process.exit(1)
      }
    }
    console.log(`🎯 目標技能: ${targetSkills.length} 個`)
    console.log(`─`.repeat(50))

    let safeCount = 0, warningCount = 0, dangerCount = 0
    let removedCount = 0, quarantinedCount = 0

    for (const skill of targetSkills) {
      if (config.whitelist?.includes(skill)) {
        console.log(`\n✅ ${skill} - 在白名單中，跳過`)
        safeCount++
        continue
      }

      const skillPath = join(SKILL_DIR, skill)
      const issues: Issue[] = []

      try {
        const skillStat = await statAsync(skillPath)
        if (!skillStat.isDirectory()) continue
      } catch {
        continue
      }

      const scanableExtensions = [".ts", ".tsx", ".js", ".jsx", ".sh", ".bash"]
      const allFiles: string[] = []

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
                allFiles.push(fullPath)
              }
            }
          }
        } catch { /* skip */ }
      }

      await scanDir(skillPath)

      for (const filePath of allFiles) {
        try {
          const content = await readFileAsync(filePath, "utf-8")
          const fileIssues = await scanFileContent(filePath, content)
          issues.push(...fileIssues)
        } catch { /* skip */ }
      }

      const highCount = issues.filter(i => i.severity === "high").length
      const status = highCount > 0 ? "danger" : issues.length > 0 ? "warning" : "safe"
      const score = Math.max(0, 100 - highCount * 30)

      if (status === "danger" && (autoMode || config.autoRemove)) {
        if (config.autoQuarantine) {
          await quarantineFile(skillPath)
          quarantinedCount++
          console.log(`\n🔴 ${skill} - 已自動隔離`)
          continue
        } else {
          await removeFile(skillPath)
          removedCount++
          console.log(`\n🔴 ${skill} - 已自動移除`)
          continue
        }
      }

      const statusIcon = status === "safe" ? "✅" : status === "warning" ? "⚠️" : "🔴"
      console.log(`\n${statusIcon} ${skill} - ${status === "safe" ? "安全" : status === "warning" ? "警告" : "危險"} (${score}/100)`)

      if (showDetails) {
        for (const issue of issues) {
          const icon = issue.severity === "high" ? "🔴" : issue.severity === "medium" ? "🟡" : "🟢"
          console.log(`   ${icon} ${issue.description}`)
        }
      }

      if (status === "safe") safeCount++
      else if (status === "warning") warningCount++
      else dangerCount++
    }

    console.log(`\n${"─".repeat(50)}`)
    console.log(`📊 技能掃描報告`)
    console.log(`   ✅ 安全: ${safeCount} 個`)
    console.log(`   ⚠️ 警告: ${warningCount} 個`)
    console.log(`   🔴 危險: ${dangerCount} 個`)
    if (removedCount > 0) console.log(`   🗑️ 已移除: ${removedCount} 個`)
    if (quarantinedCount > 0) console.log(`   📦 已隔離: ${quarantinedCount} 個`)
  }

  else if (mode === "local" || mode === "full") {
    const allResults: ScanResult[] = []
    
    for (const drive of SYSTEM_DRIVES) {
      try {
        await statAsync(drive)
        const results = await scanLocalComputer(drive, config)
        allResults.push(...results)
      } catch {
        // 硬碟不存在或無法訪問
      }
    }

    let safeCount = 0, warningCount = 0, dangerCount = 0
    let removedCount = 0, quarantinedCount = 0

    for (const result of allResults) {
      if (result.status === "danger" && (autoMode || config.autoRemove)) {
        if (config.autoQuarantine) {
          await quarantineFile(result.path)
          quarantinedCount++
        } else {
          await removeFile(result.path)
          removedCount++
        }
        console.log(`\n🔴 ${result.name} - ${result.path}`)
        console.log(`   📦 已自動處理`)
        dangerCount++
        continue
      }

      const statusIcon = result.status === "safe" ? "✅" : result.status === "warning" ? "⚠️" : "🔴"
      console.log(`\n${statusIcon} ${result.name}`)
      console.log(`   📍 ${result.path}`)
      console.log(`   📊 分數: ${result.score}/100`)

      if (showDetails) {
        for (const issue of result.issues) {
          const icon = issue.severity === "high" ? "🔴" : issue.severity === "medium" ? "🟡" : "🟢"
          console.log(`   ${icon} ${issue.description}`)
        }
      }

      if (result.status === "safe") safeCount++
      else if (result.status === "warning") warningCount++
      else dangerCount++
    }

    console.log(`\n${"─".repeat(50)}`)
    console.log(`📊 本地電腦掃描報告`)
    console.log(`   ✅ 安全: ${safeCount} 個`)
    console.log(`   ⚠️ 警告: ${warningCount} 個`)
    console.log(`   🔴 危險: ${dangerCount} 個`)
    if (removedCount > 0) console.log(`   🗑️ 已移除: ${removedCount} 個`)
    if (quarantinedCount > 0) console.log(`   📦 已隔離: ${quarantinedCount} 個`)
  }

  console.log("")
  process.exit(0)
}

main()
