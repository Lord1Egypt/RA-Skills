#!/usr/bin/env node
/**
 * CC Migrator - Claude Code 配置备份脚本
 * 跨平台支持：Mac / Linux / Windows
 *
 * 用法:
 *   node backup.mjs --scan                     # 扫描检测所有配置，输出 JSON 报告
 *   node backup.mjs [output-dir]               # 备份所有配置
 *   node backup.mjs [output-dir] --exclude=a,b # 备份时排除指定项
 */

import { existsSync, mkdirSync, copyFileSync, readFileSync, writeFileSync, readdirSync } from 'fs'
import { join, basename, relative, sep, dirname } from 'path'
import { homedir, hostname, userInfo, platform } from 'os'
import { execSync } from 'child_process'
import { fileURLToPath } from 'url'

const CLAUDE_DIR = join(homedir(), '.claude')
const DATE = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)

/** 日志输出 */
const log = (msg) => console.log(`[backup] ${msg}`)
const info = (msg) => console.log(`[info] ${msg}`)


/** 递归复制目录，排除 .git 和 .DS_Store */
function copyDirSync(src, dest, excludes = ['.git', '.DS_Store']) {
    mkdirSync(dest, { recursive: true })
    const entries = readdirSync(src, { withFileTypes: true })
    for (const entry of entries) {
        if (excludes.includes(entry.name)) continue
        const srcPath = join(src, entry.name)
        const destPath = join(dest, entry.name)
        if (entry.isDirectory()) {
            copyDirSync(srcPath, destPath, excludes)
        } else {
            copyFileSync(srcPath, destPath)
        }
    }
}

/** 递归收集文件列表（相对路径），排除 .git 和 .DS_Store */
function collectFiles(dir, baseDir, excludes = ['.git', '.DS_Store']) {
    const files = []
    if (!existsSync(dir)) return files
    const entries = readdirSync(dir, { withFileTypes: true })
    for (const entry of entries) {
        if (excludes.includes(entry.name)) continue
        const fullPath = join(dir, entry.name)
        if (entry.isDirectory()) {
            files.push(...collectFiles(fullPath, baseDir, excludes))
        } else {
            files.push(relative(baseDir, fullPath).split(sep).join('/'))
        }
    }
    return files
}

/** 安全解析 JSON 文件 */
function readJsonSafe(filePath) {
    try {
        return JSON.parse(readFileSync(filePath, 'utf-8'))
    } catch {
        return null
    }
}

/** 敏感关键词列表 */
const SENSITIVE_KEYWORDS = ['TOKEN', 'SECRET', 'KEY', 'PASSWORD', 'CREDENTIAL', 'AUTH']

/** 检测 settings.json 中的敏感字段 */
function detectSensitiveFields(settingsPath) {
    const settings = readJsonSafe(settingsPath)
    if (!settings) return []
    const sensitiveFields = []
    if (settings.env && typeof settings.env === 'object') {
        for (const [key, value] of Object.entries(settings.env)) {
            const upperKey = key.toUpperCase()
            if (SENSITIVE_KEYWORDS.some(kw => upperKey.includes(kw))) {
                sensitiveFields.push({
                    field: `env.${key}`,
                    has_value: value !== '' && value !== undefined && value !== null
                })
            }
        }
    }
    return sensitiveFields
}

/** 跳过的目录和文件（非用户配置，或运行时生成的） */
const SKIP_ROOT_ENTRIES = new Set([
    '.DS_Store',
    '.session-stats.json',
    '.omc',
    'backups',
    'cache',
    'debug',
    'file-history',
    'history.jsonl',
    'ide',
    'paste-cache',
    'plans',
    'projects',
    'session-env',
    'sessions',
    'shell-snapshots',
    'stats-cache.json',
    'tasks',
    'telemetry',
    'hud'
])

/** 插件目录中需要跳过的子目录 */
const SKIP_PLUGIN_DIRS = new Set(['cache', 'marketplaces', 'data'])



// ============================================================
// 扫描模式：检测所有可迁移的配置，输出 JSON 报告
// ============================================================
function scan() {
    if (!existsSync(CLAUDE_DIR)) {
        console.log(JSON.stringify({ error: `${CLAUDE_DIR} not found` }))
        process.exit(1)
    }

    const detected = []

    // CLAUDE.md
    const claudeMdPath = join(CLAUDE_DIR, 'CLAUDE.md')
    if (existsSync(claudeMdPath)) {
        detected.push({
            id: 'claude_md',
            name: 'CLAUDE.md',
            type: 'direct_copy',
            description: '全局指令文件，定义 Claude Code 的全局行为和规则',
            file_count: 1,
            contains_sensitive: false
        })
    }

    // rules/
    const rulesDir = join(CLAUDE_DIR, 'rules')
    if (existsSync(rulesDir)) {
        const files = collectFiles(rulesDir, CLAUDE_DIR)
        if (files.length > 0) {
            detected.push({
                id: 'rules',
                name: 'rules',
                type: 'direct_copy',
                description: '全局规则文件',
                file_count: files.length,
                files,
                contains_sensitive: false
            })
        }
    }

    // skills/
    const skillsDir = join(CLAUDE_DIR, 'skills')
    if (existsSync(skillsDir)) {
        const skillDirs = readdirSync(skillsDir, { withFileTypes: true })
            .filter(e => e.isDirectory() && e.name !== '.DS_Store')
        if (skillDirs.length > 0) {
            const allFiles = []
            const skillNames = []
            for (const dir of skillDirs) {
                skillNames.push(dir.name)
                allFiles.push(...collectFiles(join(skillsDir, dir.name), CLAUDE_DIR))
            }
            detected.push({
                id: 'skills',
                name: 'skills',
                type: 'direct_copy',
                description: `自定义 skill（${skillNames.join(', ')}）`,
                file_count: allFiles.length,
                sub_items: skillNames,
                contains_sensitive: false
            })
        }
    }

    // commands/
    const commandsDir = join(CLAUDE_DIR, 'commands')
    if (existsSync(commandsDir)) {
        const files = collectFiles(commandsDir, CLAUDE_DIR)
        if (files.length > 0) {
            detected.push({
                id: 'commands',
                name: 'commands',
                type: 'direct_copy',
                description: '自定义命令（slash commands）',
                file_count: files.length,
                contains_sensitive: false
            })
        }
    }

    // agents/
    const agentsDir = join(CLAUDE_DIR, 'agents')
    if (existsSync(agentsDir)) {
        const files = collectFiles(agentsDir, CLAUDE_DIR)
        if (files.length > 0) {
            detected.push({
                id: 'agents',
                name: 'agents',
                type: 'direct_copy',
                description: '自定义 agent 定义文件',
                file_count: files.length,
                contains_sensitive: false
            })
        }
    }

    // 自定义插件
    const pluginsDir = join(CLAUDE_DIR, 'plugins')
    if (existsSync(pluginsDir)) {
        const pluginDirs = readdirSync(pluginsDir, { withFileTypes: true })
            .filter(e => e.isDirectory() && !SKIP_PLUGIN_DIRS.has(e.name) && e.name !== '.DS_Store')
        for (const dir of pluginDirs) {
            const files = collectFiles(join(pluginsDir, dir.name), CLAUDE_DIR)
            if (files.length > 0) {
                detected.push({
                    id: `plugin_${dir.name}`,
                    name: `plugin: ${dir.name}`,
                    type: 'direct_copy',
                    description: `自定义插件 ${dir.name}`,
                    file_count: files.length,
                    contains_sensitive: false
                })
            }
        }
    }

    // settings.json
    const settingsPath = join(CLAUDE_DIR, 'settings.json')
    if (existsSync(settingsPath)) {
        const sensitiveFields = detectSensitiveFields(settingsPath)
        detected.push({
            id: 'settings',
            name: 'settings.json',
            type: 'merge_settings',
            description: '设置文件（环境变量、插件开关、市场配置等）',
            file_count: 1,
            contains_sensitive: sensitiveFields.length > 0,
            sensitive_fields: sensitiveFields
        })
    }

    // 市场插件
    const installedPluginsPath = join(CLAUDE_DIR, 'plugins', 'installed_plugins.json')
    if (existsSync(installedPluginsPath)) {
        const pluginData = readJsonSafe(installedPluginsPath)
        if (pluginData?.plugins) {
            const pluginKeys = Object.keys(pluginData.plugins)
            const commands = pluginKeys.map(key => {
                const [pluginName, marketplace] = key.split('@')
                return `claude plugins install ${marketplace}/${pluginName}`
            })
            if (commands.length > 0) {
                detected.push({
                    id: 'marketplace_plugins',
                    name: '市场插件',
                    type: 'reinstall',
                    description: '通过市场安装的插件（恢复时需重新安装）',
                    file_count: 0,
                    contains_sensitive: false,
                    reinstall_commands: commands,
                    plugin_list: pluginKeys
                })
            }
        }
    }

    // 其他可能的配置文件（动态发现 ~/.claude/ 根目录下未知的 .md .json 等文件）
    if (existsSync(CLAUDE_DIR)) {
        const rootEntries = readdirSync(CLAUDE_DIR, { withFileTypes: true })
        for (const entry of rootEntries) {
            if (SKIP_ROOT_ENTRIES.has(entry.name)) continue
            // 跳过已处理的
            if (['CLAUDE.md', 'rules', 'skills', 'commands', 'agents', 'plugins', 'settings.json'].includes(entry.name)) continue
            if (entry.isFile() && !entry.name.startsWith('.')) {
                detected.push({
                    id: `file_${entry.name.replace(/[^a-zA-Z0-9]/g, '_')}`,
                    name: entry.name,
                    type: 'direct_copy',
                    description: `根目录文件 ${entry.name}`,
                    file_count: 1,
                    contains_sensitive: false
                })
            } else if (entry.isDirectory() && !entry.name.startsWith('.')) {
                const files = collectFiles(join(CLAUDE_DIR, entry.name), CLAUDE_DIR)
                if (files.length > 0) {
                    detected.push({
                        id: `dir_${entry.name}`,
                        name: entry.name,
                        type: 'direct_copy',
                        description: `自定义目录 ${entry.name}`,
                        file_count: files.length,
                        contains_sensitive: false
                    })
                }
            }
        }
    }

    const report = {
        claude_dir: CLAUDE_DIR,
        platform: platform(),
        hostname: hostname(),
        user: userInfo().username,
        scanned_at: new Date().toISOString(),
        detected
    }

    console.log(JSON.stringify(report, null, 2))
}

// ============================================================
// 备份模式：执行实际的备份
// ============================================================
function backup(outputDir, excludeIds) {
    if (!existsSync(CLAUDE_DIR)) {
        console.error(`Error: ${CLAUDE_DIR} not found`)
        process.exit(1)
    }

    mkdirSync(outputDir, { recursive: true })

    const items = []
    let totalFiles = 0
    const excluded = new Set(excludeIds)

    const shouldInclude = (id) => !excluded.has(id)

    // CLAUDE.md
    if (shouldInclude('claude_md') && existsSync(join(CLAUDE_DIR, 'CLAUDE.md'))) {
        copyFileSync(join(CLAUDE_DIR, 'CLAUDE.md'), join(outputDir, 'CLAUDE.md'))
        items.push({
            name: 'CLAUDE.md',
            type: 'direct_copy',
            source: 'CLAUDE.md',
            target: '<claude-home>/CLAUDE.md',
            description: '全局指令文件',
            files: ['CLAUDE.md']
        })
        totalFiles++
        log('CLAUDE.md')
    }

    // rules/
    if (shouldInclude('rules') && existsSync(join(CLAUDE_DIR, 'rules'))) {
        copyDirSync(join(CLAUDE_DIR, 'rules'), join(outputDir, 'rules'))
        const files = collectFiles(join(CLAUDE_DIR, 'rules'), CLAUDE_DIR)
        if (files.length > 0) {
            items.push({
                name: 'rules',
                type: 'direct_copy',
                source: 'rules',
                target: '<claude-home>/rules',
                description: '全局规则文件',
                files
            })
            totalFiles += files.length
            log(`rules/ (${files.length} files)`)
        }
    }

    // skills/
    if (shouldInclude('skills') && existsSync(join(CLAUDE_DIR, 'skills'))) {
        const skillDirs = readdirSync(join(CLAUDE_DIR, 'skills'), { withFileTypes: true })
            .filter(e => e.isDirectory() && e.name !== '.DS_Store')
        const allFiles = []
        let skillCount = 0
        for (const dir of skillDirs) {
            copyDirSync(join(CLAUDE_DIR, 'skills', dir.name), join(outputDir, 'skills', dir.name))
            allFiles.push(...collectFiles(join(CLAUDE_DIR, 'skills', dir.name), CLAUDE_DIR))
            skillCount++
        }
        if (skillCount > 0) {
            items.push({
                name: 'skills',
                type: 'direct_copy',
                source: 'skills',
                target: '<claude-home>/skills',
                description: '自定义 skill',
                files: allFiles
            })
            totalFiles += allFiles.length
            log(`skills/ (${skillCount} skills, ${allFiles.length} files)`)
        }
    }

    // commands/
    if (shouldInclude('commands') && existsSync(join(CLAUDE_DIR, 'commands'))) {
        copyDirSync(join(CLAUDE_DIR, 'commands'), join(outputDir, 'commands'))
        const files = collectFiles(join(CLAUDE_DIR, 'commands'), CLAUDE_DIR)
        if (files.length > 0) {
            items.push({
                name: 'commands',
                type: 'direct_copy',
                source: 'commands',
                target: '<claude-home>/commands',
                description: '自定义命令（slash commands）',
                files
            })
            totalFiles += files.length
            log(`commands/ (${files.length} files)`)
        }
    }

    // agents/
    if (shouldInclude('agents') && existsSync(join(CLAUDE_DIR, 'agents'))) {
        copyDirSync(join(CLAUDE_DIR, 'agents'), join(outputDir, 'agents'))
        const files = collectFiles(join(CLAUDE_DIR, 'agents'), CLAUDE_DIR)
        if (files.length > 0) {
            items.push({
                name: 'agents',
                type: 'direct_copy',
                source: 'agents',
                target: '<claude-home>/agents',
                description: '自定义 agent 定义文件',
                files
            })
            totalFiles += files.length
            log(`agents/ (${files.length} files)`)
        }
    }

    // 自定义插件
    const pluginsDir = join(CLAUDE_DIR, 'plugins')
    if (existsSync(pluginsDir)) {
        const pluginDirs = readdirSync(pluginsDir, { withFileTypes: true })
            .filter(e => e.isDirectory() && !SKIP_PLUGIN_DIRS.has(e.name) && e.name !== '.DS_Store')
        for (const dir of pluginDirs) {
            const pluginId = `plugin_${dir.name}`
            if (!shouldInclude(pluginId)) continue
            copyDirSync(join(pluginsDir, dir.name), join(outputDir, 'plugins', dir.name))
            const files = collectFiles(join(pluginsDir, dir.name), CLAUDE_DIR).map(f => f.split(sep).join('/'))
            if (files.length > 0) {
                items.push({
                    name: `plugin: ${dir.name}`,
                    type: 'direct_copy',
                    source: `plugins/${dir.name}`,
                    target: `<claude-home>/plugins/${dir.name}`,
                    description: `自定义插件 ${dir.name}`,
                    files
                })
                totalFiles += files.length
                log(`plugin: ${dir.name}`)
            }
        }
    }

    // settings.json
    if (shouldInclude('settings') && existsSync(join(CLAUDE_DIR, 'settings.json'))) {
        const settingsContent = readJsonSafe(join(CLAUDE_DIR, 'settings.json'))
        const sensitiveFields = detectSensitiveFields(join(CLAUDE_DIR, 'settings.json'))
        const sensitiveFieldNames = sensitiveFields.map(f => f.field)

        // 根据是否排除敏感字段来处理
        if (excluded.has('settings_sensitive') && settingsContent) {
            // 清空敏感字段后再保存
            const cleaned = JSON.parse(JSON.stringify(settingsContent))
            if (cleaned.env) {
                for (const sf of sensitiveFields) {
                    const key = sf.field.replace('env.', '')
                    if (cleaned.env[key] !== undefined) {
                        cleaned.env[key] = ''
                    }
                }
            }
            writeFileSync(join(outputDir, 'settings.json'), JSON.stringify(cleaned, null, 2), 'utf-8')
            log('settings.json (sensitive fields cleared)')
        } else {
            copyFileSync(join(CLAUDE_DIR, 'settings.json'), join(outputDir, 'settings.json'))
            log('settings.json')
        }

        items.push({
            name: 'settings.json',
            type: 'merge_settings',
            source: 'settings.json',
            target: '<claude-home>/settings.json',
            description: '设置文件（环境变量、插件开关、市场配置等）',
            files: ['settings.json'],
            sensitive_fields: sensitiveFieldNames
        })
        totalFiles++
    }

    // 市场插件
    const installedPluginsPath = join(CLAUDE_DIR, 'plugins', 'installed_plugins.json')
    if (shouldInclude('marketplace_plugins') && existsSync(installedPluginsPath)) {
        copyFileSync(installedPluginsPath, join(outputDir, 'installed_plugins.json'))
        const pluginData = readJsonSafe(installedPluginsPath)
        if (pluginData?.plugins) {
            const reinstallCommands = Object.keys(pluginData.plugins).map(key => {
                const [pluginName, marketplace] = key.split('@')
                const cmd = `claude plugins install ${marketplace}/${pluginName}`
                log(`marketplace plugin: ${key} -> ${cmd}`)
                return cmd
            })
            if (reinstallCommands.length > 0) {
                items.push({
                    name: 'marketplace_plugins',
                    type: 'reinstall',
                    source: 'installed_plugins.json',
                    target: '<claude-home>/plugins',
                    description: '通过市场安装的插件（恢复时需重新安装）',
                    files: ['installed_plugins.json'],
                    reinstall_commands: reinstallCommands
                })
            }
        }
    }

    // 动态发现的其他配置
    if (existsSync(CLAUDE_DIR)) {
        const rootEntries = readdirSync(CLAUDE_DIR, { withFileTypes: true })
        for (const entry of rootEntries) {
            if (SKIP_ROOT_ENTRIES.has(entry.name)) continue
            if (['CLAUDE.md', 'rules', 'skills', 'commands', 'agents', 'plugins', 'settings.json'].includes(entry.name)) continue
            const entryId = entry.isFile()
                ? `file_${entry.name.replace(/[^a-zA-Z0-9]/g, '_')}`
                : `dir_${entry.name}`
            if (!shouldInclude(entryId)) continue

            if (entry.isFile() && !entry.name.startsWith('.')) {
                copyFileSync(join(CLAUDE_DIR, entry.name), join(outputDir, entry.name))
                items.push({
                    name: entry.name,
                    type: 'direct_copy',
                    source: entry.name,
                    target: `<claude-home>/${entry.name}`,
                    description: `根目录文件 ${entry.name}`,
                    files: [entry.name]
                })
                totalFiles++
                log(entry.name)
            } else if (entry.isDirectory() && !entry.name.startsWith('.')) {
                copyDirSync(join(CLAUDE_DIR, entry.name), join(outputDir, entry.name))
                const files = collectFiles(join(CLAUDE_DIR, entry.name), CLAUDE_DIR)
                if (files.length > 0) {
                    items.push({
                        name: entry.name,
                        type: 'direct_copy',
                        source: entry.name,
                        target: `<claude-home>/${entry.name}`,
                        description: `自定义目录 ${entry.name}`,
                        files
                    })
                    totalFiles += files.length
                    log(`${entry.name}/ (${files.length} files)`)
                }
            }
        }
    }

    // 复制 RESTORE_GUIDE.md
    const __filename = fileURLToPath(import.meta.url)
    const __dirname = dirname(__filename)
    const restoreGuideSrc = join(__dirname, '..', 'RESTORE_GUIDE.md')
    if (existsSync(restoreGuideSrc)) {
        copyFileSync(restoreGuideSrc, join(outputDir, 'RESTORE_GUIDE.md'))
        log('RESTORE_GUIDE.md')
    } else {
        info('RESTORE_GUIDE.md 未找到，跳过')
    }

    // 生成 manifest.json
    const manifest = {
        version: '1.0',
        created_at: new Date().toISOString(),
        source_machine: hostname(),
        source_user: userInfo().username,
        source_platform: platform(),
        claude_home_note: '<claude-home> 表示 ~/.claude（Unix）或 %USERPROFILE%\\.claude（Windows），恢复时根据当前平台解析',
        summary: {
            total_files: totalFiles,
            total_items: items.length
        },
        items
    }

    writeFileSync(join(outputDir, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf-8')

    console.log('')
    info('备份完成！')
    info(`输出目录: ${outputDir}`)
    info(`总文件数: ${totalFiles}`)
    info(`配置项数: ${items.length}`)
    console.log('')

    // 打包
    try {
        const parentDir = join(outputDir, '..')
        const dirName = basename(outputDir)

        if (platform() === 'win32') {
            const zipName = `${dirName}.zip`
            execSync(
                `powershell -Command "Compress-Archive -Path '${outputDir}' -DestinationPath '${join(parentDir, zipName)}'"`,
                { stdio: 'pipe' }
            )
            info(`备份包: ${join(parentDir, zipName)}`)
        } else {
            const archiveName = `${dirName}.tar.gz`
            execSync(`tar -czf "${join(parentDir, archiveName)}" -C "${parentDir}" "${dirName}"`, { stdio: 'pipe' })
            info(`备份包: ${join(parentDir, archiveName)}`)
        }
    } catch {
        info('打包跳过（可手动压缩备份目录）')
    }

    console.log('')
    log('完成! 将备份包复制到新机器，然后让 Claude 读取 RESTORE_GUIDE.md 来恢复配置。')
}

// ============================================================
// 入口：解析命令行参数
// ============================================================
const args = process.argv.slice(2)

if (args.includes('--scan')) {
    scan()
} else {
    const excludeArg = args.find(a => a.startsWith('--exclude='))
    const excludeIds = excludeArg ? excludeArg.replace('--exclude=', '').split(',') : []
    const outputDir = args.find(a => !a.startsWith('--')) || join(homedir(), 'Desktop', `cc-backup-${DATE}`)
    backup(outputDir, excludeIds)
}
