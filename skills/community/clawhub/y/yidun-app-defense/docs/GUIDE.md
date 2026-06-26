# YiDunAppDefense - 使用指南

## 快速开始

### 1. 安装 Skill

从 ClawHub 安装到本地：

```bash
# 假设安装到 ~/skills/YiDunAppDefense
cd ~/skills/YiDunAppDefense
```

### 2. 初始化

运行安装脚本，自动下载易盾加固工具：

```bash
./scripts/setup.sh
```

该脚本会：
- 检查 Java 环境
- 创建工作目录 `~/.yidun-defense/`
- 下载易盾加固工具（ZIP 包）
- 解压并安装 NHPProtect.jar 和工具目录
- 创建配置文件模板

### 3. 获取 AppKey

访问 [易盾控制台](https://dun.163.com/dashboard#/login/)：

1. 注册或登录账号
2. 进入"应用加固"服务
3. 创建应用并获取 AppKey
4. 记录您的 AppKey

### 4. 配置 AppKey

运行配置脚本：

```bash
./scripts/configure.sh
```

或者直接提供 AppKey：

```bash
./scripts/configure.sh your_appkey_here
```

### 5. 加固应用

```bash
# 自动识别文件类型
./scripts/defense-smart.sh /path/to/your/app.apk

# 完全自动模式（适合 CI/CD）
./scripts/defense-smart.sh /path/to/your/app.ipa --auto

# 手动指定平台
./scripts/defense-smart.sh /path/to/your/app.hap --platform harmony
```

或通过 AI agent 对话：

```
用户: 帮我加固 /Users/demo/app.apk

Agent: 正在使用易盾加固工具处理您的应用...
       ✓ 加固完成！
       输出文件: /Users/demo/app_protected.apk
```

## 支持的平台和文件类型

### 移动平台

#### Android
- **APK 整包**: 普通 Android 应用
- **AAB 包**: Google Play 发布格式
- **Unity 游戏**: Android 平台的 Unity 游戏
- **Cocos 游戏**: Android 平台的 Cocos 游戏
- **UE 游戏**: Android 平台的 Unreal Engine 游戏
- **Laya 游戏**: Android 平台的 Laya 游戏

#### iOS
- **IPA 应用**: 标准 iOS 应用包
- **xcarchive**: Xcode 归档文件
- **Cocos 游戏**: iOS 平台的 Cocos 游戏

#### 鸿蒙
- **HAP 应用**: 鸿蒙应用包
- **APP 包**: 鸿蒙应用包
- **Unity 游戏**: 鸿蒙平台的 Unity 团结引擎
- **Cocos 游戏**: 鸿蒙平台的 Cocos 游戏

### 游戏引擎（跨平台）

- **Unity**: Android/iOS/鸿蒙/H5
- **Cocos**: Android/iOS/鸿蒙/H5
- **Unreal Engine**: Android
- **Laya**: Android/H5

### 其他平台

#### H5/小程序
- Unity WebGL
- Cocos H5
- Laya H5
- 通用 Web 游戏

#### SDK/组件
- JAR/WAR SDK
- Android SDK (.aar)
- iOS SDK (.framework)
- SO 动态库

#### PC 应用
- Windows (.exe)
- macOS (.app)

详细信息请参考：[平台支持详情](PLATFORM_SUPPORT.md)

## 平台选择方法

### 自动识别（推荐）

defense-smart.sh 会自动识别文件类型：

```bash
# 自动识别 APK
./scripts/defense-smart.sh app.apk

# 自动识别 IPA
./scripts/defense-smart.sh app.ipa

# 自动识别 HAP
./scripts/defense-smart.sh app.hap
```

**识别规则**：
- `.apk` → Android APK
- `.aab` → Android AAB
- `.ipa` → iOS IPA
- `.xcarchive` → iOS xcarchive
- `.hap` → 鸿蒙 HAP
- `.app` → 鸿蒙 APP
- `.zip` → 需要进一步询问

### 交互式选择

如果无法自动识别，脚本会询问：

```bash
$ ./scripts/defense-smart.sh game.zip

检测到 ZIP 文件，无法自动识别类型

请选择平台：
1) Android
2) iOS
3) 鸿蒙
4) H5/小程序
5) SDK/组件
6) PC 应用

请选择 [1-6]: 1

请选择应用类型：
1) 普通应用（APK/AAB）
2) Unity 游戏
3) Cocos 游戏
4) Unreal Engine 游戏
5) Laya 游戏

请选择 [1-5]: 2
```

### 手动指定

使用 `--platform` 参数明确指定：

```bash
# 指定为 iOS 平台
./scripts/defense-smart.sh app.zip --platform ios

# 指定为鸿蒙平台
./scripts/defense-smart.sh app.zip --platform harmony

# 指定为 SDK
./scripts/defense-smart.sh lib.zip --platform sdk
```

### 完全自动模式

使用 `--auto` 参数跳过所有交互，使用推荐配置：

```bash
# CI/CD 环境使用
./scripts/defense-smart.sh app.apk --auto
```

**自动模式行为**：
- 使用检测到的平台
- 使用推荐的参数组合
- 自动签名（如果配置）
- 自动对齐（Android）
- 无需任何人工干预

## AI Agent 使用示例

### 首次使用

```
用户: 使用易盾加固这个 APK: /path/to/demo.apk

Agent: 检测到首次使用，正在初始化...
       [自动运行 setup.sh]

       工具下载完成！现在需要配置您的 AppKey。

       如果您还没有 AppKey，请访问：
       https://dun.163.com/dashboard#/login/

       请输入您的 AppKey：

用户: abc123def456...

Agent: AppKey 配置成功！开始加固...
       [执行加固]

       ✓ 加固完成！
       输出文件: /path/to/demo_protected.apk
```

### Android 加固

```
用户: 加固 /Users/work/release.apk

Agent: 检测到 Android APK 文件
       平台: Android
       文件类型: APK 整包

       正在加固...
       ✓ 加固完成！
       输出文件: /Users/work/release_protected.apk

       文件信息:
         原始大小: 25.3 MB
         加固后: 28.1 MB
```

### iOS 加固

```
用户: 加固这个 iOS 应用 app.ipa

Agent: 检测到 iOS IPA 文件
       平台: iOS
       文件类型: IPA 应用

       正在加固...
       ✓ 加固完成！
       输出文件: app_protected.ipa
```

### 鸿蒙加固

```
用户: 加固鸿蒙应用 harmony.hap

Agent: 检测到鸿蒙 HAP 文件
       平台: 鸿蒙
       文件类型: HAP 应用

       是否需要签名？[y/N]: y

       正在加固...
       ✓ 加固完成！
       输出文件: harmony_protected.hap
```

### Unity 游戏加固

```
用户: 加固 Unity 游戏 game.apk

Agent: 检测到 Android APK 文件
       这是 Unity 游戏吗？[y/N]: y

       引擎类型: Unity
       平台: Android

       正在加固...
       ✓ 加固完成！
```

### 更新配置

```
用户: 更新易盾的 appkey

Agent: 请输入新的 AppKey：

用户: new_appkey_here

Agent: AppKey 已更新！
```

## 支持的提示词

Agent 可以理解以下类型的请求：

### 加固相关
- "帮我加固这个 APK"
- "使用易盾加固 /path/to/app.apk"
- "加固这个 iOS 应用"
- "保护我的鸿蒙 HAP"
- "加固 Unity 游戏"
- "对 demo.apk 进行加固"
- "加密这个 SDK"

### 配置相关
- "配置易盾 appkey"
- "更新易盾的密钥"
- "设置加固工具"
- "显示当前配置"

### 帮助相关
- "如何使用易盾加固"
- "易盾加固帮助"
- "加固工具使用说明"
- "支持哪些平台"

## 工作原理

### 1. 目录结构

```
~/.yidun-defense/
├── NHPProtect.jar          # 易盾加固工具（核心）
├── config.ini              # 配置文件
├── tool/                   # 平台工具目录
│   ├── aapt_mac           # Android 资源打包工具（macOS）
│   ├── zipalign_16kb_mac  # APK 对齐工具（macOS）
│   └── ...                # 其他平台工具
└── YiDunPackTool2-xxx/    # 解压的原始包
```

### 2. 加固流程

```
1. 检查工具是否已安装
   └─ 否 → 运行 setup.sh 安装

2. 检查 AppKey 是否已配置
   └─ 否 → 运行 configure.sh 配置

3. 识别文件类型和平台
   ├─ 基于文件后缀自动识别
   ├─ 交互式询问确认
   └─ 或手动指定

4. 构建加固参数
   ├─ 根据平台选择参数
   ├─ 根据引擎类型调整
   └─ 添加签名/对齐等选项

5. 调用 Java 工具执行加固
   └─ cd ~/.yidun-defense && java -jar NHPProtect.jar [参数]

6. 生成加固后的文件
   └─ xxx_protected.*
```

### 3. 配置文件格式

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
aliaspswd=
signver=v1+v2

[hapsign]
keystoreFile=
keystorePwd=
keyAlias=
keyPwd=
appCertFile=
profileFile=
mode=localSign
signAlg=SHA256withECDSA

[update]
u=1
t=30
```

## 高级用法

### 多平台加固示例

#### Android 平台

```bash
# APK 整包加固
./scripts/defense-smart.sh app.apk

# Unity Android 游戏
./scripts/defense-smart.sh unity_game.apk

# AAB 包（Google Play）
./scripts/defense-smart.sh app.aab
```

#### iOS 平台

```bash
# IPA 应用
./scripts/defense-smart.sh app.ipa

# xcarchive 归档
./scripts/defense-smart.sh app.xcarchive

# Cocos iOS 游戏
./scripts/defense-smart.sh cocos_game.ipa
```

#### 鸿蒙平台

```bash
# HAP 应用
./scripts/defense-smart.sh app.hap

# APP 包
./scripts/defense-smart.sh app.app

# Unity 鸿蒙游戏
./scripts/defense-smart.sh unity_harmony.hap
```

#### SDK 加固

```bash
# JAR SDK
zip sdk.zip mylib.jar
./scripts/defense-smart.sh sdk.zip --platform sdk

# Android SDK
./scripts/defense-smart.sh sdk.aar --platform sdk

# iOS SDK
./scripts/defense-smart.sh sdk.framework --platform sdk
```

### 自定义输出目录

编辑配置文件 `~/.yidun-defense/config.ini`：

```ini
[appkey]
key = your_appkey
```

或使用 `-output` 参数（通过修改脚本）。

### 批量加固

```bash
# 批量加固多平台文件
for file in *.{apk,ipa,hap}; do
    [ -f "$file" ] && ./scripts/defense-smart.sh "$file" --auto
done

# 批量加固特定类型
for apk in *.apk; do
    ./scripts/defense-smart.sh "$apk" --auto
done
```

### 查看当前配置

```bash
./scripts/configure.sh --show
```

## 故障排查

### 问题：Java 环境未找到

```
错误: 未检测到 Java 环境！
```

**解决方案**:

```bash
# macOS
brew install openjdk@11

# Ubuntu/Debian
sudo apt install openjdk-11-jre

# 验证安装
java -version
```

### 问题：工具下载失败

```
错误: 下载失败！请检查网络连接
```

**解决方案**:

手动下载工具：

```bash
mkdir -p ~/.yidun-defense
cd ~/.yidun-defense
curl -o yidun-tool.zip \
  "https://clienttool.dun.163.com/api/v1/client/jarTool/download"
unzip yidun-tool.zip
# 复制 NHPProtect.jar 和 tool 目录
```

### 问题：AppKey 无效

```
错误: authentication failed
```

**解决方案**:

1. 检查 AppKey 是否正确
2. 确认账号已开通加固服务
3. 检查服务是否过期
4. 访问控制台查看状态：https://dun.163.com/dashboard

### 问题：加固失败

```
错误: 加固失败！
```

**常见原因**:

1. **APK 格式问题**: 确保是有效的 APK 文件
2. **配额不足**: 检查账户剩余加固次数
3. **网络问题**: 检查网络连接
4. **版本不兼容**: 确保 APK 符合加固要求

**查看详细日志**:

```bash
# 临时日志（每次加固的实时输出）
cat /tmp/yidun-defense.log

# 工具完整日志（推荐）
ls -lt ~/.yidun-defense/Log/ | head -5
cat ~/.yidun-defense/Log/Constants_YYYY-MM-DD_HH_MM_SS_*.txt
```

### 问题：如何查看加固成本和配额

**查询方法**:

1. **通过日志文件查看**（推荐）:
```bash
# 查看最新日志
ls -lt ~/.yidun-defense/Log/ | head -1

# 查看日志内容
cat ~/.yidun-defense/Log/Constants_YYYY-MM-DD_HH_MM_SS_*.txt
```

日志文件包含的关键信息：
- 🔍 **成本信息**: 本次加固消耗的配额或费用
- ❌ **失败原因**: 详细的错误代码和失败原因
- ⚙️ **加固参数**: 使用的策略、选项和配置
- 📦 **文件信息**: 输入/输出文件大小、路径等
- 🌐 **服务器响应**: 易盾服务器的完整响应

2. **通过易盾控制台查看**:
- 访问：https://dun.163.com/dashboard
- 查看加固历史记录
- 查看剩余配额和消费记录

3. **搜索特定信息**:
```bash
# 查看今天的所有加固记录
ls ~/.yidun-defense/Log/Constants_$(date +%Y-%m-%d)*.txt

# 搜索失败的加固
grep -r "error\|failed\|失败" ~/.yidun-defense/Log/

# 搜索成本信息
grep -r "cost\|配额\|消耗" ~/.yidun-defense/Log/
```

## 最佳实践

### 1. 加固前备份

```bash
cp original.apk original.apk.backup
./scripts/defense-smart.sh original.apk
```

### 2. 验证加固结果

加固后应该测试：
- APK 能否正常安装
- 应用功能是否正常
- 性能影响是否可接受

### 3. 版本管理

建议命名规范：
```
app-v1.0-release.apk
app-v1.0-release_protected.apk
```

### 4. 持续集成

可以集成到 CI/CD 流程：

```yaml
# GitHub Actions 示例
- name: Protect APK
  run: |
    ./scripts/configure.sh ${{ secrets.YIDUN_APPKEY }}
    ./scripts/defense-smart.sh app/build/outputs/apk/release/app-release.apk --auto
```

## 更多资源

- **官方文档**: https://support.dun.163.com/
- **控制台**: https://dun.163.com/dashboard
- **技术支持**: 见易盾官网客服

## 常见问题

**Q: 加固会影响应用性能吗？**
A: 加固会有轻微的性能影响，通常在可接受范围内。建议加固后进行性能测试。

**Q: 支持哪些 Android 版本？**
A: 通常支持 Android 4.4+，具体以易盾官方文档为准。

**Q: 加固后还能更新吗？**
A: 可以，每个版本都需要重新加固。

**Q: 试用策略包含哪些功能？**
A: 包括 DEX 加密、SO 保护、资源混淆、反调试等基础功能。

**Q: 收费标准是什么？**
A: 请访问易盾官网查看最新价格：https://dun.163.com/
