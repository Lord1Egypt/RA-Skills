/**
 * Session Password - Document Generator
 * Generates DOCX files for Feature Spec and User Manual
 * 
 * Version: 1.0.0
 * Author: squallsol
 */

const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, AlignmentType } = require('docx');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace'), 'session password');

// Create output directory
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Helper: Create a simple table
function createTable(headers, rows) {
  const tableRows = [];
  
  // Header row
  tableRows.push(new TableRow({
    children: headers.map(h => new TableCell({
      children: [new Paragraph({ 
        children: [new TextRun({ text: h, bold: true })],
        alignment: AlignmentType.CENTER
      })],
      width: { size: 100 / headers.length, type: WidthType.PERCENTAGE }
    }))
  }));
  
  // Data rows
  rows.forEach(row => {
    tableRows.push(new TableRow({
      children: row.map(cell => new TableCell({
        children: [new Paragraph({ children: [new TextRun(cell)] })],
        width: { size: 100 / row.length, type: WidthType.PERCENTAGE }
      }))
    }));
  });
  
  return new Table({
    rows: tableRows,
    width: { size: 100, type: WidthType.PERCENTAGE }
  });
}

// Feature Spec Document
async function createFeatureSpecDoc() {
  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        // Title
        new Paragraph({
          children: [new TextRun({ text: 'Session Password 功能说明书', bold: true, size: 36 })],
          heading: HeadingLevel.TITLE,
          alignment: AlignmentType.CENTER
        }),
        new Paragraph({
          children: [new TextRun({ text: 'Feature Specification', size: 28 })],
          alignment: AlignmentType.CENTER
        }),
        new Paragraph({ children: [] }),
        
        // Version info
        new Paragraph({ children: [new TextRun({ text: '版本 / Version: 1.0.0', bold: true })] }),
        new Paragraph({ children: [new TextRun({ text: '作者 / Author: squallsol', bold: true })] }),
        new Paragraph({ children: [new TextRun({ text: '日期 / Date: 2026-03-16', bold: true })] }),
        new Paragraph({ children: [] }),
        
        // Overview
        new Paragraph({ children: [new TextRun({ text: '概述 / Overview', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({
          children: [new TextRun('Session Password 是一个为 OpenClaw 会话提供安全口令认证的技能模块。它使用行业标准的 bcrypt 哈希算法保护用户口令，并提供多层次的安全恢复机制。')]
        }),
        new Paragraph({
          children: [new TextRun('Session Password is a skill module that provides secure passphrase authentication for OpenClaw sessions. It uses industry-standard bcrypt hashing to protect user passwords and offers multi-layered security recovery mechanisms.')]
        }),
        new Paragraph({ children: [] }),
        
        // Core Features
        new Paragraph({ children: [new TextRun({ text: '核心功能 / Core Features', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        
        new Paragraph({ children: [new TextRun({ text: '1. 口令认证 / Password Authentication', bold: true })], heading: HeadingLevel.HEADING_2 }),
        createTable(
          ['功能 / Feature', '描述 / Description'],
          [
            ['bcrypt 哈希', '使用成本因子 12 的 bcrypt 算法加密口令，抗彩虹表攻击'],
            ['会话超时', '可配置的闲置超时（默认 60 分钟）'],
            ['失败锁定', '连续 5 次失败后锁定账户 15 分钟'],
            ['审计日志', '记录所有认证事件，便于安全审计']
          ]
        ),
        new Paragraph({ children: [] }),
        
        new Paragraph({ children: [new TextRun({ text: '2. 恢复机制 / Recovery Mechanisms', bold: true })], heading: HeadingLevel.HEADING_2 }),
        createTable(
          ['机制 / Mechanism', '说明 / Description'],
          [
            ['安全邮箱', '必填，用于接收恢复码'],
            ['恢复码', '6 位数字验证码，有效期 10 分钟'],
            ['安全问题', '可选的备用验证方式']
          ]
        ),
        new Paragraph({ children: [] }),
        
        new Paragraph({ children: [new TextRun({ text: '3. 双语支持 / Bilingual Support', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('• 中文 (zh-CN)')] }),
        new Paragraph({ children: [new TextRun('• English (en)')] }),
        new Paragraph({ children: [] }),
        
        // Security Features
        new Paragraph({ children: [new TextRun({ text: '安全特性 / Security Features', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        
        new Paragraph({ children: [new TextRun({ text: '口令复杂度要求 / Password Requirements', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('✅ 最小长度：12 个字符')] }),
        new Paragraph({ children: [new TextRun('✅ 必须包含大写字母 (A-Z)')] }),
        new Paragraph({ children: [new TextRun('✅ 必须包含小写字母 (a-z)')] }),
        new Paragraph({ children: [new TextRun('✅ 必须包含数字 (0-9)')] }),
        new Paragraph({ children: [new TextRun('✅ 必须包含特殊符号 (@$!%*?&)')] }),
        new Paragraph({ children: [new TextRun('❌ 禁止使用常见弱口令')] }),
        new Paragraph({ children: [] }),
        
        new Paragraph({ children: [new TextRun({ text: '安全措施 / Security Measures', bold: true })], heading: HeadingLevel.HEADING_2 }),
        createTable(
          ['措施 / Measure', '实现 / Implementation'],
          [
            ['哈希存储', 'bcrypt ($2b$)，非明文存储'],
            ['文件权限', '配置文件权限 600（仅所有者可读写）'],
            ['防暴力破解', '失败锁定 + 超时机制'],
            ['防绕过', '检测哈希值输入，拒绝疑似攻击']
          ]
        ),
        new Paragraph({ children: [] }),
        
        // Config Files
        new Paragraph({ children: [new TextRun({ text: '配置文件 / Configuration Files', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        createTable(
          ['文件 / File', '路径 / Path', '用途 / Purpose'],
          [
            ['auth-config.json', 'memory/', '主配置文件'],
            ['auth-users.json', 'memory/', '用户凭据（bcrypt 哈希）'],
            ['auth-state.json', 'memory/', '会话状态'],
            ['auth-audit.log', 'memory/', '审计日志']
          ]
        ),
        new Paragraph({ children: [] }),
        
        // Voice Commands
        new Paragraph({ children: [new TextRun({ text: '语音指令 / Voice Commands', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        createTable(
          ['中文', 'English', '动作 / Action'],
          [
            ['忘记口令', 'forgot password', '触发邮箱恢复'],
            ['修改口令', 'change password', '修改当前口令'],
            ['退出认证', 'logout', '清除认证状态'],
            ['卸载口令skill', 'uninstall auth skill', '完全移除认证']
          ]
        ),
        new Paragraph({ children: [] }),
        
        // Tech Specs
        new Paragraph({ children: [new TextRun({ text: '技术规格 / Technical Specifications', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({ children: [new TextRun('• Node.js: >= 18.0.0')] }),
        new Paragraph({ children: [new TextRun('• 依赖: bcrypt ^5.1.1')] }),
        new Paragraph({ children: [new TextRun('• 哈希算法: bcrypt (成本因子 12)')] }),
        new Paragraph({ children: [new TextRun('• 备份哈希: SHA-256 (向后兼容)')] }),
        new Paragraph({ children: [] }),
        
        // Version History
        new Paragraph({ children: [new TextRun({ text: '版本历史 / Version History', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        createTable(
          ['版本 / Version', '日期 / Date', '更新内容 / Changes'],
          [['1.0.0', '2026-03-16', '初始版本，完整功能实现']]
        ),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: 'Document generated by Session Password v1.0.0', italics: true })] }),
      ]
    }]
  });
  
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(path.join(OUTPUT_DIR, 'Session_Password_Feature_Specification_v1.0.0.docx'), buffer);
  console.log('✅ Created: Session_Password_Feature_Specification_v1.0.0.docx');
}

// User Manual Document
async function createUserManualDoc() {
  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        // Title
        new Paragraph({
          children: [new TextRun({ text: 'Session Password 用户手册', bold: true, size: 36 })],
          heading: HeadingLevel.TITLE,
          alignment: AlignmentType.CENTER
        }),
        new Paragraph({
          children: [new TextRun({ text: 'User Manual', size: 28 })],
          alignment: AlignmentType.CENTER
        }),
        new Paragraph({ children: [] }),
        
        // Version info
        new Paragraph({ children: [new TextRun({ text: '版本 / Version: 1.0.0', bold: true })] }),
        new Paragraph({ children: [new TextRun({ text: '作者 / Author: squallsol', bold: true })] }),
        new Paragraph({ children: [new TextRun({ text: '日期 / Date: 2026-03-16', bold: true })] }),
        new Paragraph({ children: [] }),
        
        // Table of Contents
        new Paragraph({ children: [new TextRun({ text: '目录 / Table of Contents', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({ children: [new TextRun('1. 安装设置 / Installation')] }),
        new Paragraph({ children: [new TextRun('2. 首次配置 / First-time Setup')] }),
        new Paragraph({ children: [new TextRun('3. 日常使用 / Daily Usage')] }),
        new Paragraph({ children: [new TextRun('4. 口令恢复 / Password Recovery')] }),
        new Paragraph({ children: [new TextRun('5. 修改口令 / Change Password')] }),
        new Paragraph({ children: [new TextRun('6. 卸载 / Uninstall')] }),
        new Paragraph({ children: [new TextRun('7. 常见问题 / FAQ')] }),
        new Paragraph({ children: [] }),
        
        // Section 1
        new Paragraph({ children: [new TextRun({ text: '1. 安装设置 / Installation', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({ children: [new TextRun({ text: '前提条件 / Prerequisites', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('• OpenClaw 已安装并运行')] }),
        new Paragraph({ children: [new TextRun('• Node.js >= 18.0.0')] }),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: '安装步骤 / Installation Steps', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun({ text: 'cd ~/.openclaw/workspace/skills/session-password', font: 'Courier New' })] }),
        new Paragraph({ children: [new TextRun({ text: 'npm install', font: 'Courier New' })] }),
        new Paragraph({ children: [new TextRun({ text: 'node scripts/setup.js', font: 'Courier New' })] }),
        new Paragraph({ children: [] }),
        
        // Section 2
        new Paragraph({ children: [new TextRun({ text: '2. 首次配置 / First-time Setup', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({ children: [new TextRun({ text: '步骤 1：选择语言', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('选择中文或英文作为界面语言。')] }),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: '步骤 2：创建管理员用户', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('输入用户名（默认：admin）和口令。')] }),
        new Paragraph({ children: [new TextRun({ text: '口令要求 / Password Requirements:', bold: true })] }),
        new Paragraph({ children: [new TextRun('• 至少 12 个字符')] }),
        new Paragraph({ children: [new TextRun('• 包含大写字母 (A-Z)')] }),
        new Paragraph({ children: [new TextRun('• 包含小写字母 (a-z)')] }),
        new Paragraph({ children: [new TextRun('• 包含数字 (0-9)')] }),
        new Paragraph({ children: [new TextRun('• 包含特殊符号 (@$!%*?&)')] }),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: '步骤 3：安全邮箱', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun({ text: '必填项', bold: true }), new TextRun(' - 用于账户恢复。忘记口令时，恢复码将发送到此邮箱。')] }),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: '步骤 4：安全问题（可选）', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('设置一个安全问题作为备用验证方式。')] }),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: '步骤 5：设置', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('• 超时时间：闲置多久后需要重新认证（默认 60 分钟）')] }),
        new Paragraph({ children: [new TextRun('• 自动重置：认证后是否自动执行 /new 或 /reset')] }),
        new Paragraph({ children: [] }),
        
        // Section 3
        new Paragraph({ children: [new TextRun({ text: '3. 日常使用 / Daily Usage', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({ children: [new TextRun({ text: '认证流程 / Authentication Flow', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('1. 启动会话时，系统提示输入口令')] }),
        new Paragraph({ children: [new TextRun('2. 输入正确口令后，获得访问权限')] }),
        new Paragraph({ children: [new TextRun('3. 闲置超过设定时间后，需要重新认证')] }),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: '自动超时 / Auto Timeout', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('• 默认 60 分钟闲置后超时')] }),
        new Paragraph({ children: [new TextRun('• 超时后需要重新输入口令')] }),
        new Paragraph({ children: [] }),
        
        // Section 4
        new Paragraph({ children: [new TextRun({ text: '4. 口令恢复 / Password Recovery', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({ children: [new TextRun({ text: '方法一：邮箱恢复', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('1. 输入："忘记口令" 或 "forgot password"')] }),
        new Paragraph({ children: [new TextRun('2. 系统发送 6 位恢复码到安全邮箱')] }),
        new Paragraph({ children: [new TextRun('3. 输入收到的恢复码')] }),
        new Paragraph({ children: [new TextRun('4. 设置新口令')] }),
        new Paragraph({ children: [] }),
        new Paragraph({ children: [new TextRun({ text: '方法二：安全问题', bold: true })], heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [new TextRun('1. 输入："忘记口令"')] }),
        new Paragraph({ children: [new TextRun('2. 选择安全问题验证')] }),
        new Paragraph({ children: [new TextRun('3. 正确回答问题后设置新口令')] }),
        new Paragraph({ children: [] }),
        
        // Section 5
        new Paragraph({ children: [new TextRun({ text: '5. 修改口令 / Change Password', bold: true, size: 28 })], heading: HeadingLevel.HEADING_1 }),
        new Paragraph({ children: [new TextRun('在已认证状态下：')] }),
        new Paragraph({ children: [