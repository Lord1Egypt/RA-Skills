# 易盾加固平台支持类型

## 支持的加固类型

### Android 平台

| 类型 | 文件后缀 | 必需参数 | 描述 |
|------|---------|---------|------|
| **APK 整包** | `.apk` | `-yunconfig -fullapk` | Android 应用整包加固 |
| **AAB 包** | `.aab` | `-yunconfig -fullapk` | Android App Bundle 加固 |
| **Unity** | `.apk` | `-yunconfig` | Unity 引擎游戏加固 |
| **Cocos** | `.apk` | `-yunconfig -cocos` | Cocos 引擎游戏加固 |
| **UE** | `.apk` | `-yunconfig -ue` | Unreal Engine 游戏加固 |
| **Laya** | `.apk` | `-yunconfig -laya` | Laya 引擎游戏加固 |

### iOS 平台

| 类型 | 文件后缀 | 必需参数 | 描述 |
|------|---------|---------|------|
| **IPA 应用** | `.ipa` | `-iOS -nobitcode -yunconfig` | iOS 应用加固 |
| **xcarchive** | `.xcarchive` | `-iOS -nobitcode -yunconfig` | iOS 归档文件加固 |
| **Cocos** | `.ipa` | `-iOS -nobitcode -yunconfig -cocos` | iOS Cocos 游戏 |

### 鸿蒙平台

| 类型 | 文件后缀 | 必需参数 | 描述 |
|------|---------|---------|------|
| **HAP 应用** | `.hap` | `-yunconfig -fullapp -harmony` | 鸿蒙应用加固 |
| **APP 包** | `.app` | `-yunconfig -fullapp -harmony` | 鸿蒙 APP 包加固 |
| **Unity** | `.hap/.app` | `-yunconfig -fullapp -harmony` | 鸿蒙 Unity 游戏 |
| **Cocos** | `.hap/.app` | `-yunconfig -fullapp -harmony -cocos` | 鸿蒙 Cocos 游戏 |

### H5/小程序

| 类型 | 文件后缀 | 必需参数 | 描述 |
|------|---------|---------|------|
| **Unity H5** | `.zip` | `-web -unity` | Unity WebGL 游戏 |
| **Cocos H5** | `.zip` | `-web -cocos` | Cocos H5 游戏 |
| **Laya H5** | `.zip` | `-web -laya` | Laya H5 游戏 |
| **Web 游戏** | `.zip` | `-web` | 通用 Web 游戏 |

### SDK/组件

| 类型 | 文件后缀 | 必需参数 | 描述 |
|------|---------|---------|------|
| **JAR/WAR** | `.zip` | `-sdk` | Java SDK 加固（需打包成 zip） |
| **Android SDK** | `.aar` | `-sdk -android` | Android SDK 加固 |
| **iOS SDK** | `.framework` | `-sdk -iOS` | iOS SDK 加固 |
| **SO 文件** | `.zip` | `-encryptso -yunconfig` | SO 动态库加固（需打包成 zip） |

### PC 平台

| 类型 | 文件后缀 | 必需参数 | 描述 |
|------|---------|---------|------|
| **Windows** | `.exe` | `-pc -windows` | Windows 应用加固 |
| **Mac** | `.app` | `-pc -mac` | macOS 应用加固 |

## 文件类型自动识别规则

### 基于后缀的识别

```
.apk     → Android APK（需进一步判断引擎）
.aab     → Android AAB
.ipa     → iOS IPA
.xcarchive → iOS xcarchive
.hap     → 鸿蒙 HAP
.app     → 鸿蒙 APP 或 macOS APP（需判断）
.aar     → Android SDK
.framework → iOS SDK
.zip     → H5/SDK/SO（需进一步判断）
.exe     → Windows 应用
.jar     → Java JAR（需打包成 zip）
.war     → Java WAR（需打包成 zip）
```

### 引擎类型检测

对于 APK/AAB/IPA 文件，可以通过以下方式检测引擎：

1. **Unity**：
   - 存在 `libunity.so`
   - 存在 `libil2cpp.so` 或 `libmono.so`
   - 存在 `Data/` 目录

2. **Cocos**：
   - 存在 `libcocos2d.so`
   - 存在 `cocos2d-x` 相关文件

3. **UE**：
   - 存在 `libUE4.so`
   - 存在 Unreal Engine 特征文件

4. **Laya**：
   - 存在 `LayaAir` 相关文件

### ZIP 文件类型判断

对于 `.zip` 文件，需要检查内容：

1. **SO 加固**：包含 `.so` 文件
2. **JAR/WAR SDK**：包含 `.jar` 或 `.war` 文件
3. **H5 游戏**：包含 `index.html`、`Build/` 等 Web 资源

## 交互式选择流程

当无法自动识别时，按以下顺序询问：

1. **平台选择**：
   - Android
   - iOS
   - 鸿蒙
   - H5/小程序
   - SDK/组件
   - PC

2. **应用类型**（针对选定平台）：
   - 普通应用
   - Unity 游戏
   - Cocos 游戏
   - UE 游戏
   - Laya 游戏

3. **特殊选项**：
   - 是否需要 DEX 加密？（Android）
   - 是否需要防二次打包？（Android）
   - 是否需要签名？
   - 是否需要对齐？（Android）

## 参数组合示例

### Android APK 整包 + 签名 + 对齐
```bash
java -jar NHPProtect.jar -yunconfig -fullapk -zipalign -apksign -input test.apk
```

### Android Unity APK + DEX 加密
```bash
java -jar NHPProtect.jar -yunconfig -zipalign -apksign -dex -input unity.apk
```

### iOS IPA 应用
```bash
java -jar NHPProtect.jar -iOS -nobitcode -yunconfig -input app.ipa
```

### 鸿蒙 HAP + 签名
```bash
java -jar NHPProtect.jar -yunconfig -fullapp -harmony -hapsign -input test.hap
```

### SO 文件加固
```bash
java -jar NHPProtect.jar -yunconfig -encryptso -input libtest.zip
```

### JAR SDK 加固
```bash
java -jar NHPProtect.jar -sdk -input sdk.zip
```

## config.ini 配置示例

### Android 签名配置
```ini
[apksign]
keystore=D:\xxx\xx.keystore
alias=xxx
pswd=xxx
aliaspswd=xxx
signver=v1+v2
```

### 鸿蒙签名配置
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

### SO 文件配置
```ini
[so]
so1=libtest.so
so2=libtest2.so
```

### Unity 符号表配置
```ini
[SymbolPath]
path=E:\TEST\Symbols
```

### iOS 符号表配置
```ini
[SymbolPath]
path=/Users/test/Symbols
```

### Unity AB 资源加密
```ini
[u3dabmode]
mode=4

[u3dabPath]
path1=assets/balling.ab
path2=assets/GameAbs
```

## 注意事项

### Android
- APK 整包加固需要 `-fullapk` 参数
- Google Play 上架需要关闭自动完整性保护
- 建议使用 `-zipalign` 进行对齐
- 防二次打包需要 `-antirepack` 参数

### iOS
- `.ipa` 文件需要配置符号表路径
- 必须使用 `-nobitcode` 参数
- xcarchive 文件可以直接加固

### 鸿蒙
- 必须包含 `-harmony` 参数
- `.app` 文件需要 `-fullapp` 参数
- 签名需要配置多个证书文件

### Unity
- 需要配置符号表路径
- AB 资源加密需要额外配置
- 支持 il2cpp 和 mono 引擎

### SO 文件
- 必须打包成 `.zip` 格式
- 需要在 config.ini 中指定 SO 名称
- 建议只保护自研 SO

### JAR/WAR
- 必须打包成 `.zip` 格式
- 加固后需要用 `-javaagent` 启动
- 需要联系技术支持配置加密包名

---

**文档版本**: v1.0.0
**最后更新**: 2026-02-27
