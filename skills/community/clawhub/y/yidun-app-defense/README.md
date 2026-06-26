# YiDunAppDefense

<div align="center">

**🛡️ 易盾应用加固 - AI Agent Skill**

为 AI agent 提供多平台应用一键加固能力

**当前支持**: Android、iOS、鸿蒙
**计划支持**: H5、SDK、PC

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)](https://github.com)

[快速开始](#快速开始) • [使用指南](docs/GUIDE.md) • [API 文档](docs/API.md) • [ClawHub](https://clawhub.ai/)

</div>

---

## 📖 简介

YiDunAppDefense 是一个面向 AI agent 的多平台应用加固 skill，封装了网易易盾的应用加固能力。通过自然语言对话，即可完成 Android、iOS、鸿蒙等多平台应用的安全加固，保护应用免受逆向工程、代码篡改和恶意攻击。

### ✨ 核心特性

- 🤖 **AI 驱动**: 通过自然语言对话完成加固操作
- 🎯 **多平台支持**: Android、iOS、鸿蒙已支持；H5、SDK、PC 计划中
- 🎮 **游戏引擎**: 支持 Unity、Cocos、Unreal Engine、Laya 等主流引擎
- 🔍 **智能识别**: 自动识别文件类型和平台
- 🔧 **零配置**: 对话式 AppKey 配置，无需手动编辑文件
- 📦 **自动化**: 首次使用自动下载工具和引导配置
- 🚀 **开箱即用**: 默认使用试用策略，立即可用
- 🛡️ **专业加固**: 基于网易易盾企业级加固技术
- 🌐 **跨平台**: 支持 macOS、Linux 等主流操作系统

---

## 🚀 快速开始

### 环境要求

- **Java**: JRE 8+ (推荐 JRE 11+)
- **网络工具**: curl 或 wget
- **操作系统**: macOS 10.14+ / Ubuntu 18.04+ / Debian 10+ / CentOS 7+

### 安装

#### 方法一：从 ClawHub 安装（推荐）

```bash
# 访问 ClawHub 并安装到本地
# https://clawhub.ai/skills/yidun-app-defense

# 安装到指定目录
cd ~/skills/YiDunAppDefense
```

#### 方法二：手动克隆

```bash
# 克隆仓库
git clone <repository-url> ~/yidun/YiDunAppDefense
cd ~/yidun/YiDunAppDefense

# 运行初始化
./scripts/setup.sh
```

### 首次使用

1. **初始化工具**

```bash
./scripts/setup.sh
```

这会自动：
- 检查 Java 环境
- 下载易盾加固工具
- 创建配置文件模板

2. **获取 AppKey**

访问 [易盾控制台](https://dun.163.com/dashboard#/login/)：
- 注册/登录账号
- 开通应用加固服务
- 创建应用并获取 AppKey

3. **配置 AppKey**

```bash
./scripts/configure.sh
```

按提示输入您的 AppKey。

4. **加固应用**

```bash
# 自动识别文件类型
./scripts/defense-smart.sh /path/to/your/app.apk

# 完全自动模式（适合 CI/CD）
./scripts/defense-smart.sh /path/to/your/app.ipa --auto

# 手动指定平台
./scripts/defense-smart.sh /path/to/your/app.hap --platform harmony
```

加固后的文件：`/path/to/your_protected.*`

---

## 💬 AI Agent 使用

### 首次对话示例

```
用户: 帮我加固这个 APK: /Users/demo/app.apk

Agent: 检测到首次使用，正在初始化易盾加固工具...
       ✓ Java 环境检查通过
       ✓ 工具下载完成

       现在需要配置您的 AppKey。
       如果您还没有 AppKey，请访问：
       https://dun.163.com/dashboard#/login/

       请输入您的 AppKey：

用户: abc123def456ghi789...

Agent: ✓ AppKey 配置成功！

       开始加固您的应用...
       [进度] 正在调用易盾加固工具...
       [进度] 处理中...

       ✓ 加固完成！

       输出文件: /Users/demo/app_protected.apk

       文件信息:
         原始大小: 25.3 MB
         加固后: 28.1 MB
         增加: 2.8 MB (11%)
```

### 日常使用示例

```
用户: 加固 release.apk

Agent: 正在使用易盾加固工具处理...
       ✓ 加固完成！
       输出文件: release_protected.apk
```

### 更新配置

```
用户: 更新易盾 appkey

Agent: 请输入新的 AppKey：

用户: new_appkey_123

Agent: ✓ AppKey 已更新！
```

---

## 📚 使用指南

### 支持的平台和文件类型

#### ✅ 当前支持的平台

**移动平台**：
- **Android**: APK, AAB, Unity, Cocos, UE, Laya
- **iOS**: IPA, xcarchive, Cocos
- **鸿蒙**: HAP, APP, Unity, Cocos

**游戏引擎**（跨平台）：
- **Unity**: Android/iOS/鸿蒙
- **Cocos**: Android/iOS/鸿蒙
- **Unreal Engine**: Android
- **Laya**: Android

#### 🔄 计划支持的平台

以下平台正在开发中，敬请期待：

- **H5/小程序**: Unity WebGL, Cocos H5, Laya H5, Web游戏
- **SDK/组件**: JAR/WAR, Android SDK (.aar), iOS SDK (.framework), SO 动态库
- **PC应用**: Windows (.exe), macOS (.app)

详细文档：[平台支持详情](docs/PLATFORM_SUPPORT.md) | [多平台使用指南](docs/MULTI_PLATFORM_GUIDE.md)

### 支持的提示词

Agent 可以理解多种表达方式：

**加固操作**:
- "帮我加固这个 APK"
- "使用易盾加固 /path/to/app.apk"
- "加固这个 iOS 应用"
- "保护我的鸿蒙 HAP 文件"
- "加固 Unity 游戏"
- "加密这个 SDK"

**配置管理**:
- "配置易盾 appkey"
- "更新加固工具的密钥"
- "设置易盾加固"

**帮助信息**:
- "如何使用易盾加固"
- "易盾加固帮助"

### 目录结构

```
YiDunAppDefense/
├── CLAUDE.md                 # AI 工作流规则
├── SKILL.md                  # Skill 描述（ClawHub）
├── README.md                 # 本文档
├── scripts/                  # 核心脚本
│   ├── setup.sh             # 初始化和工具下载
│   ├── configure.sh         # AppKey 配置
│   └── defense-smart.sh     # 智能多平台加固脚本 ⭐
├── config/                   # 配置文件
│   └── config.ini.template  # 配置模板
├── docs/                     # 文档
│   ├── GUIDE.md             # 详细使用指南
│   ├── PLATFORM_SUPPORT.md  # 平台支持详情 ⭐
│   ├── MULTI_PLATFORM_GUIDE.md  # 多平台使用指南 ⭐
│   ├── YIDUN_COMMAND.md     # 易盾命令说明
│   └── API.md               # API 文档
└── tasks/                    # 任务管理
    ├── todo.md              # 任务清单
    ├── lessons.md           # 经验总结
    └── multi-platform-upgrade.md  # 多平台升级报告 ⭐
```

---

## 🛠️ 高级用法

### 多平台加固示例

#### Android 加固
```bash
# APK 整包
./scripts/defense-smart.sh app.apk

# Unity 游戏
./scripts/defense-smart.sh unity_game.apk

# AAB 包
./scripts/defense-smart.sh app.aab
```

#### iOS 加固
```bash
# IPA 应用
./scripts/defense-smart.sh app.ipa

# xcarchive 归档
./scripts/defense-smart.sh app.xcarchive
```

#### 鸿蒙加固
```bash
# HAP 应用
./scripts/defense-smart.sh app.hap

# APP 包
./scripts/defense-smart.sh app.app
```

#### SDK 加固
```bash
# Android SDK
./scripts/defense-smart.sh sdk.aar --platform sdk

# iOS SDK
./scripts/defense-smart.sh sdk.framework --platform sdk
```

### 批量加固

```bash
#!/bin/bash
# 批量加固多个文件
for file in /path/to/apps/*; do
    echo "Processing: $file"
    ./scripts/defense-smart.sh "$file" --auto
done
```

### 自定义输出目录

编辑 `~/.yidun-defense/config.ini`:

```ini
[yidun]
appkey = your_appkey
output_dir = /custom/output/path
```

### 集成到 CI/CD

```yaml
# GitHub Actions 示例 - 多平台构建和加固
name: Multi-Platform Build and Protect

on: [push]

jobs:
  protect-android:
    runs-on: ubuntu-latest
    steps:
      - name: Setup YiDun Defense
        run: |
          ./scripts/setup.sh
          ./scripts/configure.sh ${{ secrets.YIDUN_APPKEY }}

      - name: Protect Android APK
        run: |
          ./scripts/defense-smart.sh \
            app/build/outputs/apk/release/app-release.apk \
            --auto

      - name: Upload Protected APK
        uses: actions/upload-artifact@v3
        with:
          name: protected-apk
          path: app/build/outputs/apk/release/app-release_protected.apk

  protect-ios:
    runs-on: macos-latest
    steps:
      - name: Setup YiDun Defense
        run: |
          ./scripts/setup.sh
          ./scripts/configure.sh ${{ secrets.YIDUN_APPKEY }}

      - name: Protect iOS IPA
        run: |
          ./scripts/defense-smart.sh \
            build/ios/app.ipa \
            --auto

      - name: Upload Protected IPA
        uses: actions/upload-artifact@v3
        with:
          name: protected-ipa
          path: build/ios/app_protected.ipa
```

---

## 🔧 故障排查

### Java 环境问题

```bash
# 检查 Java 版本
java -version

# macOS 安装
brew install openjdk@11

# Ubuntu 安装
sudo apt install openjdk-11-jre
```

### 工具下载失败

```bash
# 手动下载
mkdir -p ~/.yidun-defense
curl -L -o ~/.yidun-defense/yidun-tool.jar \
  "https://clienttool.dun.163.com/api/v1/client/jarTool/download"
```

### AppKey 无效

检查：
1. AppKey 是否正确复制
2. 账号是否已开通加固服务
3. 服务是否在有效期内
4. 访问控制台查看状态

### 加固日志和成本查询

每次加固后，工具会在 `~/.yidun-defense/Log/` 目录下生成详细的日志文件：

```bash
# 查看最新的加固日志
ls -lt ~/.yidun-defense/Log/ | head -5

# 查看具体日志内容
cat ~/.yidun-defense/Log/Constants_YYYY-MM-DD_HH_MM_SS_*.txt
```

日志文件包含的关键信息：
- **成本信息**: 本次加固消耗的配额或费用
- **失败原因**: 如果加固失败，会显示详细的错误信息
- **加固参数**: 使用的加固策略和参数配置
- **文件信息**: 输入文件和输出文件的详细信息
- **服务器响应**: 易盾服务器返回的完整响应

查看日志示例：
```bash
# 查看今天的所有加固日志
ls ~/.yidun-defense/Log/Constants_$(date +%Y-%m-%d)*.txt

# 搜索失败的加固记录
grep -r "error\|failed\|失败" ~/.yidun-defense/Log/
```

### 更多问题

查看 [详细故障排查指南](docs/GUIDE.md#故障排查)

---

## 📖 文档

- [详细使用指南](docs/GUIDE.md) - 完整的使用说明和最佳实践
- [平台支持详情](docs/PLATFORM_SUPPORT.md) - 所有支持平台的详细信息
- [多平台使用指南](docs/MULTI_PLATFORM_GUIDE.md) - 多平台加固使用指南
- [易盾命令说明](docs/YIDUN_COMMAND.md) - 加固命令详解
- [API 文档](docs/API.md) - 脚本接口和技术细节
- [易盾官方文档](https://support.dun.163.com/) - 官方技术文档

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 开发指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

请遵循 [CLAUDE.md](CLAUDE.md) 中定义的工作流规范。

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- [网易易盾](https://dun.163.com/) - 提供企业级加固服务
- [ClawHub](https://clawhub.ai/) - AI Skill 分发平台

---

## 📮 联系方式

- **官网**: https://dun.163.com/
- **控制台**: https://dun.163.com/dashboard
- **技术支持**: 见易盾官网客服
- **ClawHub**: https://clawhub.ai/

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个星标！**

Made with ❤️ for AI Agent Community

</div>
