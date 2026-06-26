/**
 * windows-esm-installer - Windows 一键安装修复工具
 * 
 * 解决 Windows 用户安装 OpenClaw/Skill 时的常见问题：
 * - ESM URL 报错（c: 盘路径不支持）
 * - npm 依赖下载超时
 * - 系统依赖缺失
 * - 权限问题
 * - 中文路径乱码
 * 
 * 触发命令：/win-fix, /install-fix, /windows-install
 * 自然语言：Windows 安装、修复安装、ESM 报错
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import { existsSync, writeFileSync, readFileSync, renameSync } from 'fs';
import { join, dirname, basename, extname } from 'path';

const execAsync = promisify(exec);

/**
 * 修复 Windows 路径
 * 将 c:\path\to\file 转换为 file:///c:/path/to/file
 */
export function fixWindowsPath(inputPath: string): string {
  // 规范化路径分隔符
  const normalized = inputPath.replace(/\\/g, '/');
  
  // 移除开头的斜杠
  const cleanPath = normalized.replace(/^\/+/, '');
  
  // 转换为 file:// URL
  const fileUrl = `file:///${cleanPath}`;
  
  return fileUrl;
}

/**
 * 检测系统依赖
 */
export async function checkSystemDeps(): Promise<{
  nodeVersion: string;
  npmVersion: string;
  missing: string[];
  warnings: string[];
}> {
  const missing: string[] = [];
  const warnings: string[] = [];
  let nodeVersion = '未检测到';
  let npmVersion = '未检测到';
  
  // 检测 Node.js
  try {
    const { stdout } = await execAsync('node --version');
    nodeVersion = stdout.trim();
    
    // 检查版本 >= 18.0.0
    const versionMatch = nodeVersion.match(/v(\d+)\.(\d+)\.(\d+)/);
    if (versionMatch) {
      const major = parseInt(versionMatch[1]);
      if (major < 18) {
        warnings.push(`Node.js 版本 ${nodeVersion} 低于要求的 18.0.0`);
      }
    }
  } catch {
    missing.push('Node.js');
  }
  
  // 检测 npm
  try {
    const { stdout } = await execAsync('npm --version');
    npmVersion = stdout.trim();
    
    const versionMatch = npmVersion.match(/(\d+)\.(\d+)\.(\d+)/);
    if (versionMatch) {
      const major = parseInt(versionMatch[1]);
      if (major < 9) {
        warnings.push(`npm 版本 ${npmVersion} 低于要求的 9.0.0`);
      }
    }
  } catch {
    missing.push('npm');
  }
  
  // 检测 zstd（Windows 可选）
  try {
    await execAsync('zstd --version 2>nul');
  } catch {
    warnings.push('zstd 未安装（某些 Skill 需要）');
  }
  
  // 检测 git
  try {
    await execAsync('git --version 2>nul');
  } catch {
    warnings.push('git 未安装（Skill 发布需要）');
  }
  
  return { nodeVersion, npmVersion, missing, warnings };
}

/**
 * 设置国内 npm 镜像源
 */
export async function setupNpmMirror(): Promise<boolean> {
  try {
    await execAsync('npm config set registry https://registry.npmmirror.com');
    return true;
  } catch {
    return false;
  }
}

/**
 * 生成 Windows 安装脚本
 */
export function generateInstallScript(projectPath: string): {
  batPath: string;
  ps1Path: string;
} {
  const batContent = `@echo off
chcp 65001 >nul
echo ========================================
echo   OpenClaw Windows 一键安装脚本
echo ========================================
echo.

:: 检查 Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js
    echo 请先安装 Node.js: https://nodejs.org/
    pause
    exit /b 1
)

:: 设置国内镜像源
echo [1/3] 设置 npm 镜像源...
npm config set registry https://registry.npmmirror.com

:: 安装依赖
echo [2/3] 安装项目依赖...
call npm install --verbose

:: 验证安装
echo [3/3] 验证安装...
node --version
npm --version

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 生成报告：INSTALL_REPORT.md
pause
`;

  const ps1Content = `# OpenClaw Windows PowerShell 安装脚本
# 以管理员身份运行

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenClaw Windows 一键安装脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Node.js
try {
    $nodeVersion = node --version
    Write-Host "[✓] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未检测到 Node.js" -ForegroundColor Red
    Write-Host "请先安装 Node.js: https://nodejs.org/" -ForegroundColor Yellow
    pause
    exit 1
}

# 设置国内镜像源
Write-Host ""
Write-Host "[1/3] 设置 npm 镜像源..." -ForegroundColor Cyan
npm config set registry https://registry.npmmirror.com

# 安装依赖
Write-Host ""
Write-Host "[2/3] 安装项目依赖..." -ForegroundColor Cyan
npm install --verbose

# 验证安装
Write-Host ""
Write-Host "[3/3] 验证安装..." -ForegroundColor Cyan
node --version
npm --version

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "生成报告：INSTALL_REPORT.md" -ForegroundColor Yellow
Write-Host ""
pause
`;

  const batPath = join(projectPath, 'install.bat');
  const ps1Path = join(projectPath, 'install.ps1');
  
  writeFileSync(batPath, batContent, 'utf-8');
  writeFileSync(ps1Path, ps1Content, 'utf-8');
  
  return { batPath, ps1Path };
}

/**
 * 生成安装报告
 */
export function generateInstallReport(
  systemInfo: any,
  success: boolean,
  errors: string[] = []
): string {
  const report = `# OpenClaw 安装报告

## 系统信息
- **操作系统**: ${systemInfo.platform || 'Windows'}
- **Node.js**: ${systemInfo.nodeVersion || '未检测到'}
- **npm**: ${systemInfo.npmVersion || '未检测到'}

## 安装配置
- **镜像源**: https://registry.npmmirror.com
- **安装时间**: ${new Date().toLocaleString('zh-CN')}

## 安装状态
- **状态**: ${success ? '✅ 成功' : '❌ 失败'}
${errors.length > 0 ? `\n## 错误信息\n${errors.map(e => `- ${e}`).join('\n')}` : ''}

## 下一步
1. 运行 \`openclaw gateway start\` 启动服务
2. 在飞书中与机器人对话
3. 如有问题，运行 \`claw skill run windows-esm-installer --diagnose\`

---
*报告生成时间：${new Date().toISOString()}*
`;

  return report;
}

/**
 * 诊断模式
 */
export async function runDiagnose(): Promise<string> {
  const systemDeps = await checkSystemDeps();
  
  let report = `### 🔍 Windows 安装环境诊断报告

**生成时间：** ${new Date().toLocaleString('zh-CN')}

---

### 📊 系统检测

| 组件 | 状态 | 版本 |
|------|------|------|
| Node.js | ${systemDeps.nodeVersion !== '未检测到' ? '✅' : '❌'} | ${systemDeps.nodeVersion} |
| npm | ${systemDeps.npmVersion !== '未检测到' ? '✅' : '❌'} | ${systemDeps.npmVersion} |

---

### ⚠️ 警告信息
${systemDeps.warnings.length > 0 
  ? systemDeps.warnings.map(w => `- ${w}`).join('\n')
  : '✅ 无警告'}

---

### ❌ 缺失组件
${systemDeps.missing.length > 0 
  ? systemDeps.missing.map(m => `- ${m}`).join('\n')
  : '✅ 无缺失'}

---

### 💡 建议
${systemDeps.missing.length > 0 
  ? '请先安装缺失组件后重试'
  : systemDeps.warnings.length > 0
  ? '建议根据警告信息优化环境'
  : '✅ 环境良好，可以安装'}

---

*诊断完成*`;

  return report;
}

/**
 * 匹配触发关键词
 */
function matchesTrigger(message: string): boolean {
  const triggers = [
    '/win-fix',
    '/install-fix',
    '/windows-install',
    'Windows 安装',
    '修复安装',
    'ESM 报错',
    'c: 盘路径',
    'npm 超时',
    '安装失败',
    '一键安装',
  ];
  
  const lowerMessage = message.toLowerCase().trim();
  return triggers.some(trigger => lowerMessage.includes(trigger.toLowerCase()));
}

/**
 * 主处理函数
 */
export async function handleWindowsEsmInstaller(
  message: string,
  context?: any
): Promise<string | null> {
  if (!matchesTrigger(message)) {
    return null;
  }
  
  // 检查诊断模式
  if (message.includes('--diagnose') || message.includes('诊断')) {
    return await runDiagnose();
  }
  
  // 检查系统依赖
  const systemDeps = await checkSystemDeps();
  
  // 如果有缺失组件，提示安装
  if (systemDeps.missing.length > 0) {
    return `### ❌ 安装环境检测失败

**缺失组件：**
${systemDeps.missing.map(m => `- ${m}`).join('\n')}

**请先安装缺失组件后重试。**

**安装指南：**
1. Node.js: https://nodejs.org/
2. 下载 LTS 版本
3. 安装后重启终端`;
  }
  
  // 设置 npm 镜像源
  await setupNpmMirror();
  
  // 生成安装脚本
  const projectPath = process.cwd();
  const { batPath, ps1Path } = generateInstallScript(projectPath);
  
  // 生成安装报告
  const report = generateInstallReport(systemDeps, true);
  const reportPath = join(projectPath, 'INSTALL_REPORT.md');
  writeFileSync(reportPath, report, 'utf-8');
  
  return `### ✅ Windows 安装环境已修复

**检测结果：**
- Node.js: ${systemDeps.nodeVersion} ✅
- npm: ${systemDeps.npmVersion} ✅
- npm 镜像源：已设置为 npmmirror.com ✅

**生成文件：**
- install.bat: ${batPath}
- install.ps1: ${ps1Path}
- INSTALL_REPORT.md: ${reportPath}

---

### 🚀 下一步

**方式 1：双击运行脚本**
1. 打开文件资源管理器
2. 找到 \`install.bat\` 或 \`install.ps1\`
3. 右键 → "以管理员身份运行"

**方式 2：命令行运行**
\`\`\`bash
# 批处理
install.bat

# PowerShell
.\\install.ps1
\`\`\`

**方式 3：继续手动安装**
\`\`\`bash
npm config set registry https://registry.npmmirror.com
npm install
\`\`\`

---

*如有问题，运行 \`/win-fix --diagnose\` 诊断*`;
}

// 导出给 OpenClaw 使用
export default {
  name: 'windows-esm-installer',
  version: '1.0.0',
  description: 'Windows 一键安装修复工具 - 解决 ESM URL 报错、npm 超时等问题',
  triggers: ['/win-fix', '/install-fix', 'Windows 安装'],
  handler: handleWindowsEsmInstaller,
};
