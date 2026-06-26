---
description: 易盾应用加固 - AI Agent Skill for multi-platform app protection
metadata:
  nanobot:
    always: false
    requires:
      bins: ["java", "curl"]
      env: []
---

# 易盾应用加固 (YiDunAppDefense)

易盾应用加固 Skill 为 AI agent 提供多平台应用加固能力。当前支持 Android、iOS、鸿蒙三大移动平台，H5、SDK、PC 等平台正在开发中，保护应用免受逆向工程和篡改攻击。

## 功能特性

- 🎯 **多平台支持**: Android、iOS、鸿蒙已支持；H5、SDK、PC 计划中
- 🎮 **游戏引擎**: 支持 Unity、Cocos、Unreal Engine、Laya 等主流引擎
- 🔍 **智能识别**: 自动识别文件类型和平台
- 🛡️ **一键加固**: 通过自然语言对话完成应用加固
- 🔧 **自动配置**: 对话式 appkey 配置，无需手动编辑配置文件
- 📦 **自动下载**: 首次使用自动下载易盾加固工具
- 🚀 **简单易用**: 支持默认试用策略，开箱即用
- 🤖 **CI/CD 友好**: 完全自动模式，适合集成到构建流程

## 使用前准备

### 1. 获取 AppKey

访问 [易盾控制台](https://dun.163.com/dashboard#/login/) 注册账号并获取加固服务的 appkey。

### 2. 系统要求

- Java Runtime Environment (JRE) 8+
- curl 或 wget

## 支持的平台

### ✅ 当前支持

**移动平台**：
- **Android**: APK, AAB, Unity, Cocos, UE, Laya
- **iOS**: IPA, xcarchive, Cocos
- **鸿蒙**: HAP, APP, Unity, Cocos

**游戏引擎**（跨平台）：
- **Unity**: Android/iOS/鸿蒙
- **Cocos**: Android/iOS/鸿蒙
- **Unreal Engine**: Android
- **Laya**: Android

### 🔄 计划支持

以下平台正在开发中：

- **H5/小程序**: Unity WebGL, Cocos H5, Laya H5, 通用Web游戏
- **SDK/组件**: JAR/WAR, Android SDK (.aar), iOS SDK (.framework), SO 动态库
- **PC 应用**: Windows (.exe), macOS (.app)

## 使用方法

### 首次使用

在安装 skill 后，第一次使用时会自动下载加固工具并引导配置 appkey：

```
用户: 帮我加固 /path/to/demo.apk

Agent: 检测到首次使用，正在下载易盾加固工具...
       下载完成！请输入您的 appkey。

       如果您还没有 appkey，请访问：
       https://dun.163.com/dashboard#/login/
       注册账号并获取加固服务的 appkey。

用户: [输入 appkey]

Agent: 配置成功！开始加固您的应用...
       ✓ 加固完成！
       输出文件: /path/to/demo_protected.apk
```

### 日常使用

配置完成后，只需简单对话即可加固任意支持的平台：

**Android 加固**:
```
用户: 帮我加固 /Users/demo/app/release.apk

Agent: 正在使用易盾加固工具处理您的应用...
       ✓ 加固完成！
       输出文件: /Users/demo/app/release_protected.apk
```

**iOS 加固**:
```
用户: 加固这个 iOS 应用: /path/to/app.ipa

Agent: 检测到 iOS IPA 文件
       平台: iOS
       文件类型: IPA 应用

       正在加固...
       ✓ 加固完成！
       输出文件: /path/to/app_protected.ipa
```

**鸿蒙加固**:
```
用户: 加固鸿蒙应用 app.hap

Agent: 检测到鸿蒙 HAP 文件
       平台: 鸿蒙
       文件类型: HAP 应用

       正在加固...
       ✓ 加固完成！
```

**Unity 游戏加固**:
```
用户: 加固 Unity 游戏 game.apk

Agent: 检测到 Android APK 文件
       引擎类型: Unity

       正在加固...
       ✓ 加固完成！
```

### 更新 AppKey

如需更新 appkey：

```
用户: 更新易盾加固的 appkey

Agent: 请输入新的 appkey：

用户: [输入新的 appkey]

Agent: AppKey 已更新！
```

## 命令参考

Agent 可以理解以下类型的请求：

**加固操作**:
- "帮我加固这个 APK"
- "使用易盾加固 /path/to/app.apk"
- "加固这个 iOS 应用"
- "保护我的鸿蒙 HAP"
- "加固 Unity 游戏"
- "加固这个 SDK"

**配置操作**:
- "更新易盾 appkey"
- "配置加固工具"

## 技术细节

### 加固工具

使用网易易盾官方 jar 工具（NHPProtect.jar），自动从以下地址下载：
```
https://clienttool.dun.163.com/api/v1/client/jarTool/download
```

### 核心脚本

- **setup.sh**: 初始化和工具下载
- **configure.sh**: AppKey 配置管理
- **defense-smart.sh**: 智能多平台加固脚本（统一入口）

### 配置文件

配置存储在 `~/.yidun-defense/config.ini`：
```ini
[appkey]
key = your_appkey_here

[so]
so1=
so2=

[apksign]
keystore=
alias=
pswd=
signver=v1+v2

[hapsign]
keystoreFile=
keystorePwd=

[update]
u=1
t=30
```

### 智能识别

defense-smart.sh 支持：
- ✅ 自动文件类型识别（基于后缀）
- ✅ 交互式平台选择
- ✅ 自动参数构建
- ✅ 完全自动模式（--auto）
- ✅ 手动平台指定（--platform）

## 故障排查

### 工具下载失败

```bash
# 手动下载工具
curl -o ~/.yidun-defense/yidun-tool.jar \
  "https://clienttool.dun.163.com/api/v1/client/jarTool/download"
```

### AppKey 无效

确保：
1. AppKey 从官方控制台获取
2. 账号已开通加固服务
3. AppKey 未过期

### Java 版本问题

```bash
# 检查 Java 版本
java -version

# 需要 JRE 8 或更高版本
```

### 查看加固日志和成本

每次加固后，工具会在 `~/.yidun-defense/Log/` 目录生成详细日志：

```bash
# 查看最新日志
ls -lt ~/.yidun-defense/Log/ | head -5

# 查看日志内容（包含成本、失败信息等）
cat ~/.yidun-defense/Log/Constants_*.txt
```

日志包含：
- ✅ 加固成本和配额消耗
- ❌ 失败原因和错误详情
- ⚙️ 加固参数和策略配置
- 📊 文件大小和处理时间

## 更多信息

- 官网: https://dun.163.com/
- 文档: https://support.dun.163.com/
- 控制台: https://dun.163.com/dashboard

## License

MIT License

---

**注意**: 本 skill 需要有效的易盾服务账号和 appkey。免费试用策略可在控制台申请。
