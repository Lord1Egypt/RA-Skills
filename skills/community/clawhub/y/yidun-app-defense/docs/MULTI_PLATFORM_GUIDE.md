# 易盾多平台加固使用指南

## 概述

易盾加固工具现已支持**所有主流平台**的应用加固，包括：
- ✅ Android（APK/AAB）
- ✅ iOS（IPA/xcarchive）
- ✅ 鸿蒙（HAP/APP）
- ✅ H5/小程序
- ✅ SDK/组件
- ✅ PC 应用

## 快速开始

### 方式 1：智能模式（推荐）

自动识别文件类型并加固：

```bash
./scripts/defense-smart.sh /path/to/your/file
```

### 方式 2：完全自动模式

不询问，使用推荐配置：

```bash
./scripts/defense-smart.sh /path/to/your/file --auto
```

### 方式 3：指定平台

手动指定平台类型：

```bash
./scripts/defense-smart.sh /path/to/your/file --platform android
```


## 平台使用示例

### Android 平台

#### APK 整包加固

```bash
# 交互式
./scripts/defense-smart.sh /path/to/app.apk

# 自动模式
./scripts/defense-smart.sh /path/to/app.apk --auto
```

**交互式选择**：
1. 选择应用类型（普通/Unity/Cocos/UE/Laya）
2. 是否需要 zipalign 对齐？（建议选 Y）
3. 是否需要自动签名？（需要配置签名信息）
4. 是否需要 DEX 加密？（仅普通应用）

#### AAB 包加固

```bash
./scripts/defense-smart.sh /path/to/app.aab
```

#### Unity 游戏

```bash
./scripts/defense-smart.sh /path/to/unity_game.apk
# 选择类型: 2) Unity 引擎
```

**注意**：Unity 加固需要配置符号表：
```ini
[SymbolPath]
path=E:\TEST\Symbols
```

### iOS 平台

#### IPA 应用加固

```bash
./scripts/defense-smart.sh /path/to/app.ipa
```

#### xcarchive 加固

```bash
./scripts/defense-smart.sh /path/to/app.xcarchive
```

**注意**：iOS 加固需要配置符号表（.ipa 文件）：
```ini
[SymbolPath]
path=/Users/test/Symbols
```

### 鸿蒙平台

#### HAP 应用加固

```bash
./scripts/defense-smart.sh /path/to/app.hap
```

#### APP 包加固

```bash
./scripts/defense-smart.sh /path/to/app.app --platform harmony
```

**注意**：`.app` 文件需要指定平台，否则可能被误识别为 macOS 应用。

#### 鸿蒙签名配置

```ini
[hapsign]
keystoreFile=C:\test\haptest.p12
keystorePwd=xxxxx
keyAlias=xxxxx
keyPwd=xxxxxx
appCertFile=C:\test\haptest.cer
profileFile=C:\test\test.p7b
mode=localSign
signAlg=SHA256withECDSA
```

### H5/小程序

#### Unity WebGL 游戏

```bash
./scripts/defense-smart.sh /path/to/unity_h5.zip --platform h5
# 在交互中选择 Unity 引擎
```

#### Cocos H5 游戏

```bash
./scripts/defense-smart.sh /path/to/cocos_h5.zip --platform h5
# 在交互中选择 Cocos 引擎
```

### SDK/组件

#### Android SDK（.aar）

```bash
./scripts/defense-smart.sh /path/to/sdk.aar --platform sdk
```

#### JAR/WAR 加固

**注意**：JAR/WAR 必须先打包成 ZIP：

```bash
# 1. 打包成 zip
zip sdk.zip mylib.jar

# 2. 加固
./scripts/defense-smart.sh sdk.zip --platform sdk
```

**使用加固后的 JAR**：
```bash
java -javaagent:yourpaoject-encrypted.jar -jar yourpaoject-encrypted.jar
```

#### SO 文件加固

```bash
# 1. 打包 SO 文件
zip libtest.zip libtest.so

# 2. 配置 config.ini
[so]
so1=libtest.so

# 3. 加固
java -jar NHPProtect.jar -yunconfig -encryptso -input libtest.zip
```

### PC 应用

#### Windows EXE

```bash
./scripts/defense-smart.sh /path/to/app.exe --platform pc
```

#### macOS APP

```bash
./scripts/defense-smart.sh /path/to/app.app --platform pc
```

## 配置文件说明

### 通用配置

```ini
[appkey]
key=你的AppKey
# 从 https://dun.163.com/dashboard 获取

[update]
u=1
t=30
```

### Android 签名配置

```ini
[apksign]
keystore=D:\xxx\xx.keystore
alias=your_alias
pswd=keystore_password
aliaspswd=alias_password
signver=v1+v2
```

### SO 文件配置

```ini
[so]
so1=libtest.so
so2=libtest2.so
# 建议只配置自研 SO，第三方 SO 不建议处理
```

### Unity 配置

```ini
[SymbolPath]
path=E:\TEST\Symbols

[u3dabmode]
mode=4

[u3dabPath]
path1=assets/balling.ab
path2=assets/GameAbs
```

### 渠道包配置

```ini
[Channel]
path=E:\Desktop\Channel.txt
```

Channel.txt 示例：
```
360|CHANNEL|奇虎
baidu|CHANNEL_BAIDU
```

## 智能识别规则

### 文件后缀识别

| 后缀 | 自动识别为 | 需要进一步确认 |
|------|-----------|---------------|
| `.apk` | Android APK | 引擎类型 |
| `.aab` | Android AAB | - |
| `.ipa` | iOS IPA | - |
| `.xcarchive` | iOS xcarchive | - |
| `.hap` | 鸿蒙 HAP | - |
| `.app` | 鸿蒙/macOS | 平台类型 |
| `.zip` | H5/SDK/SO | 具体类型 |
| `.exe` | Windows | - |

### 引擎检测（未来功能）

通过分析文件内容自动检测引擎类型：
- Unity：检测 `libunity.so`、`libil2cpp.so`
- Cocos：检测 `libcocos2d.so`
- UE：检测 `libUE4.so`

## 常见问题

### Q1: 如何选择正确的平台？

**A**:
- 如果文件后缀明确（.apk、.ipa、.hap），工具会自动识别
- `.app` 文件：鸿蒙使用 `--platform harmony`，macOS 使用 `--platform pc`
- `.zip` 文件：根据内容选择 h5/sdk

### Q2: 什么时候需要配置符号表？

**A**:
- Unity 游戏（Android/iOS）
- iOS IPA 文件
- Unity H5 游戏

符号表路径配置：
```ini
[SymbolPath]
path=/path/to/Symbols
```

### Q3: 签名失败怎么办？

**A**: 检查 config.ini 中的签名配置：
1. 文件路径是否正确（使用绝对路径）
2. 密码是否正确
3. 签名版本是否匹配（v1/v2/v1+v2）

### Q4: 加固后 Google Play 上架失败？

**A**: 关闭 Google Play 自动完整性保护：
1. 进入 Google Play Console
2. 版本 > 设置 > 应用完整性
3. 关闭"自动完整性保护"

### Q5: JAR/WAR 加固后如何使用？

**A**: 使用 javaagent 启动：
```bash
java -javaagent:encrypted.jar -jar encrypted.jar
```

### Q6: SO 文件必须打包成 ZIP 吗？

**A**: 是的，SO 加固要求：
1. 将 SO 文件打包成 ZIP
2. 在 config.ini 中配置 SO 名称
3. 使用 `-encryptso` 参数

## 最佳实践

### 1. Android 应用

```bash
# 推荐配置：对齐 + 签名
./scripts/defense-smart.sh app.apk
# 选择：
# - 对齐: Y
# - 签名: Y (需配置签名信息)
# - DEX 加密: N (普通应用可选 Y)
```

### 2. iOS 应用

```bash
# 必须配置符号表（.ipa 文件）
# 1. 编辑 config.ini
[SymbolPath]
path=/Users/project/Symbols

# 2. 加固
./scripts/defense-smart.sh app.ipa
```

### 3. Unity 游戏

```bash
# 1. 配置符号表
[SymbolPath]
path=/path/to/Unity/Symbols

# 2. （可选）配置 AB 资源加密
[u3dabmode]
mode=4

# 3. 加固
./scripts/defense-smart.sh unity_game.apk
# 选择: 2) Unity 引擎
```

### 4. 批量加固

```bash
# Android APK 批量
for apk in *.apk; do
    ./scripts/defense-smart.sh "$apk" --auto
done

# 多平台混合
for file in *.{apk,ipa,hap}; do
    ./scripts/defense-smart.sh "$file" --auto
done
```

### 5. CI/CD 集成

```yaml
# GitHub Actions 示例
- name: Install YiDun Tool
  run: |
    cd YiDunAppDefense
    ./scripts/setup.sh

- name: Configure AppKey
  run: |
    ./scripts/configure.sh ${{ secrets.YIDUN_APPKEY }}

- name: Protect APK
  run: |
    ./scripts/defense-smart.sh app/release/app.apk --auto
```

## 参数参考

### defense-smart.sh 参数

```bash
./scripts/defense-smart.sh <file> [options]

Options:
  --auto               完全自动模式，不询问
  --platform <type>    指定平台：android/ios/harmony/h5/sdk/pc
  --help              显示帮助
```

### NHPProtect.jar 参数（高级）

详见各平台文档：
- [Android 加固参数](YIDUN_COMMAND.md)
- [iOS 加固参数](~/Download/Jar/iOS_APP加固_网易易盾.md)
- [鸿蒙加固参数](~/Download/Jar/鸿蒙_APP加固_网易易盾.md)

## 文档索引

- [平台支持详情](PLATFORM_SUPPORT.md) - 所有平台的详细说明
- [Android 加固命令](YIDUN_COMMAND.md) - Android 完整命令参考
- [使用指南](GUIDE.md) - 基础使用说明
- [测试文档](TESTING.md) - 测试说明

## 技术支持

- 官方文档：https://support.dun.163.com/
- 控制台：https://dun.163.com/dashboard
- 原始文档：~/Download/Jar/（各平台 MD 文件）

---

**文档版本**: v2.0.0
**最后更新**: 2026-02-27
**支持平台**: Android, iOS, 鸿蒙, H5, SDK, PC
