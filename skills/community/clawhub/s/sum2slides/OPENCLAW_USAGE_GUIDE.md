# Sum2Slides v1.0.1 - OpenClaw Skill 使用说明

## 🎯 概述

Sum2Slides 是专门为 **OpenClaw** 设计的文本转幻灯片技能，深度集成 OpenClaw 生态系统，提供一键式安装、智能工作流和丰富的使用场景支持。

## 📦 OpenClaw 安装方式

### 1. 通过 ClawHub 安装（推荐）
```bash
# 一键安装 Sum2Slides Skill
openclaw skill install sum2slides

# 验证安装
openclaw skill list | grep sum2slides

# 查看 Skill 详情
openclaw skill info sum2slides
```

### 2. 安装后验证
```bash
# 检查 Skill 是否正常工作
openclaw skill test sum2slides

# 查看可用命令
openclaw skill commands sum2slides
```

## 🚀 OpenClaw 使用方式

### 1. 在 OpenClaw 聊天中直接使用

#### 方式 A：@ 提及调用
```bash
# 在 OpenClaw 聊天界面中
@sum2slides 请将今天的会议纪要转为幻灯片

# 或指定模板
@sum2slides 使用商务模板处理项目报告
```

#### 方式 B：命令模式
```bash
# 使用 /open 命令
/open sum2slides --input meeting.txt --output slides.pptx

# 完整参数示例
/open sum2slides --input daily_report.md --template business --theme light --output report.pptx
```

#### 方式 C：快捷指令
```bash
# 预设快捷指令（如果配置了）
/slides 会议纪要内容...
/ppt 项目进度报告...
```

### 2. OpenClaw AI 助手集成

#### 自动触发模式
```bash
# AI 助手自动检测关键词
用户：今天的会议讨论需要转为幻灯片
助手：检测到"幻灯片"关键词，正在使用 sum2slides 处理...
      已生成幻灯片文件：meeting_20260329.pptx
```

#### 主动询问模式
```bash
# 助手主动提供帮助
助手：我注意到您提到了会议纪要，需要我帮您转为幻灯片吗？
用户：好的，谢谢！
助手：正在使用 sum2slides 生成幻灯片...
```

### 3. OpenClaw 配置文件集成

#### 基础配置文件
```yaml
# ~/.openclaw/config.yaml
skills:
  sum2slides:
    # 基础设置
    enabled: true
    auto_trigger: true
    
    # 模板配置
    default_template: "business"
    templates:
      meeting: "business"
      report: "academic"
      creative: "colorful"
    
    # 输出配置
    output:
      dir: "~/OpenClaw/Presentations"
      format: "pptx"
      naming: "{type}_{date}"
    
    # 自动化配置
    automation:
      keywords: ["会议纪要", "报告", "演示", "幻灯片", "PPT"]
      exclude: ["隐私", "机密", "内部"]
      auto_save: true
```

#### 环境变量配置
```bash
# OpenClaw 环境变量
export OPENCLAW_SKILL_SUM2SLIDES_ENABLED=true
export OPENCLAW_SKILL_SUM2SLIDES_TEMPLATE=business
export OPENCLAW_SKILL_SUM2SLIDES_THEME=light
export OPENCLAW_SKILL_SUM2SLIDES_AUTO_CONVERT=true
export OPENCLAW_SKILL_SUM2SLIDES_OUTPUT_DIR=~/OpenClaw/output
```

## 🔧 OpenClaw 工作流集成

### 1. 自动化工作流示例

#### 工作流 1：会议纪要自动化
```yaml
# ~/.openclaw/workflows/meeting_slides.yaml
name: "会议纪要转幻灯片"
description: "自动将会议纪要转为演示文稿"

trigger:
  type: "file_upload"
  pattern: "*meeting*.txt"
  folder: "~/Documents/Meetings"

actions:
  - name: "转换幻灯片"
    skill: "sum2slides"
    params:
      template: "business"
      theme: "light"
      output: "~/Presentations/{filename}.pptx"
  
  - name: "保存到共享"
    skill: "file_manager"
    params:
      action: "copy"
      source: "~/Presentations/{filename}.pptx"
      destination: "~/Shared/TeamPresentations/"
  
  - name: "发送通知"
    skill: "notifier"
    params:
      channel: "slack"
      message: "新的会议幻灯片已生成: {filename}.pptx"
```

#### 工作流 2：日报自动化
```yaml
name: "日报生成自动化"
description: "每天自动生成工作日报幻灯片"

schedule:
  cron: "0 17 * * *"  # 每天17:00

actions:
  - name: "收集日报数据"
    skill: "data_collector"
    params:
      sources: ["jira", "git", "calendar"]
      period: "today"
  
  - name: "生成幻灯片"
    skill: "sum2slides"
    params:
      template: "business"
      output: "~/DailyReports/daily_{date}.pptx"
  
  - name: "邮件发送"
    skill: "email"
    params:
      to: "team@company.com"
      subject: "每日工作汇报 {date}"
      attachment: "~/DailyReports/daily_{date}.pptx"
```

### 2. 与其他 OpenClaw Skill 集成

#### 与 Calendar Skill 集成
```bash
# 获取日历事件并生成幻灯片
openclaw workflow run meeting_to_slides --date today
```

#### 与 Email Skill 集成
```bash
# 处理邮件内容并生成演示文稿
/open email process --skill sum2slides --template business
```

#### 与 Chatbot Skill 集成
```bash
# 聊天记录整理为演示文稿
/open chatbot export --format slides --skill sum2slides
```

## 🎯 OpenClaw 使用场景

### 场景 1：团队协作
```bash
# 团队会议后快速分享
@sum2slides 今天的团队会议讨论要点：
1. 项目进度更新
2. 技术问题讨论
3. 下周工作计划

# 自动生成并分享到团队频道
```

### 场景 2：客户汇报
```bash
# 准备客户汇报材料
/open sum2slides --input client_report.md --template business --theme professional --output client_presentation.pptx

# 自动添加公司Logo和水印
```

### 场景 3：教育培训
```bash
# 创建培训材料
@sum2slides 使用学术模板
# 培训大纲
## 第一章：基础概念
## 第二章：高级技巧
## 第三章：实战案例
```

### 场景 4：个人学习
```bash
# 学习笔记整理
/open sum2slides --input study_notes.md --template academic --output learning_summary.pptx
```

## 📊 OpenClaw Skill 管理

### 1. Skill 管理命令
```bash
# 查看所有已安装 Skill
openclaw skill list

# 查看 sum2slides 详情
openclaw skill info sum2slides

# 更新 sum2slides
openclaw skill update sum2slides

# 禁用/启用 sum2slides
openclaw skill disable sum2slides
openclaw skill enable sum2slides

# 卸载 sum2slides
openclaw skill uninstall sum2slides

# 查看使用统计
openclaw skill stats sum2slides
```

### 2. Skill 配置管理
```bash
# 导出当前配置
openclaw skill config export sum2slides > sum2slides_config.yaml

# 导入配置
openclaw skill config import sum2slides --file sum2slides_config.yaml

# 重置配置
openclaw skill config reset sum2slides
```

### 3. Skill 调试和日志
```bash
# 查看 Skill 日志
openclaw skill logs sum2slides

# 调试模式运行
openclaw skill debug sum2slides --input test.txt

# 性能测试
openclaw skill benchmark sum2slides
```

## 💡 OpenClaw 最佳实践

### 1. 配置建议
- **自动触发关键词**: 根据团队习惯设置（如"幻灯片"、"PPT"、"演示"）
- **默认模板**: 根据主要使用场景设置默认模板
- **输出目录**: 设置统一的输出目录便于管理
- **权限控制**: 配置适当的文件访问权限

### 2. 工作流优化
- **预设工作流**: 为常用场景创建预设工作流
- **定时任务**: 利用定时任务自动化重复工作
- **错误处理**: 配置工作流失败时的处理机制
- **通知机制**: 设置生成完成后的通知方式

### 3. 性能优化
- **批量处理**: 一次性处理多个文件
- **缓存机制**: 启用模板缓存提高性能
- **并发控制**: 配置适当的并发处理数量
- **资源监控**: 监控 Skill 的资源使用情况

### 4. 安全考虑
- **输入验证**: 确保输入内容的安全性
- **权限控制**: 控制文件访问权限
- **日志审计**: 记录所有操作日志
- **备份策略**: 定期备份配置和生成的文件

## 🔗 资源和支持

### OpenClaw 相关资源
- **官方文档**: https://docs.openclaw.ai
- **Skill 开发指南**: https://docs.openclaw.ai/skills
- **API 参考**: https://docs.openclaw.ai/api
- **社区论坛**: https://community.openclaw.ai

### Sum2Slides 资源
- **GitHub 仓库**: 本地化技能版本
- **问题反馈**: 本地化技能版本/issues
- **使用示例**: 本地化技能版本/examples
- **更新日志**: 本地化技能版本/CHANGELOG.md

### 社区支持
- **Discord 社区**: https://discord.gg/clawd
- **Slack 频道**: #openclaw-skills
- **Stack Overflow**: openclaw 标签
- **邮件列表**: skills@openclaw.ai

## 🚀 快速开始 Checklist

### 安装配置
- [ ] 安装 Sum2Slides Skill: `openclaw skill install sum2slides`
- [ ] 验证安装: `openclaw skill list | grep sum2slides`
- [ ] 基础配置: 编辑 `~/.openclaw/config.yaml`
- [ ] 测试运行: `@sum2slides 测试内容`

### 日常使用
- [ ] 在聊天中使用: `@sum2slides 会议纪要...`
- [ ] 使用命令模式: `/open sum2slides --input file.txt`
- [ ] 配置自动化: 设置关键词自动触发
- [ ] 创建工作流: 为重复任务创建工作流

### 高级功能
- [ ] 集成其他 Skill: 与 calendar、email 等 Skill 集成
- [ ] 配置工作流: 创建自动化工作流
- [ ] 性能优化: 根据使用情况优化配置
- [ ] 监控管理: 设置监控和告警

---

## 📝 故障排除

### 常见问题

#### Q1: Skill 安装失败
```bash
# 检查网络连接
ping github.com

# 检查 ClawHub 状态
openclaw status

# 尝试手动安装
cd /tmp && 通过 OpenClaw 安装技能
cd sum2slides && openclaw skill install .
```

#### Q2: Skill 无法调用
```bash
# 检查 Skill 状态
openclaw skill info sum2slides

# 检查配置文件
cat ~/.openclaw/config.yaml | grep sum2slides

# 重启 OpenClaw
openclaw restart
```

#### Q3: 生成失败
```bash
# 查看详细日志
openclaw skill logs sum2slides --level debug

# 测试简单输入
@sum2slides 测试文本

# 检查依赖
pip list | grep python-pptx
```

#### Q4: 性能问题
```bash
# 查看资源使用
openclaw skill stats sum2slides

# 调整配置
# 在配置文件中调整并发数、缓存大小等
```

### 获取帮助
```bash
# 查看帮助文档
openclaw help skill
openclaw help sum2slides

# 社区求助
# 在 Discord 或 GitHub Issues 描述问题
```

---

**生成时间**: 2026年3月29日 16:45  
**版本**: Sum2Slides v1.0.1  
**适用平台**: OpenClaw 1.0+  

**现在您已经掌握了 Sum2Slides 在 OpenClaw 中的所有使用方法！** 🚀