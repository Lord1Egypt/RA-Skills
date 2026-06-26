# 易盾 Android 加固命令说明

## 官方文档
https://support.dun.163.com/documents/15588074449563648?docId=989347548106215424

## 基本命令格式

```bash
java -jar NHPProtect.jar -yunconfig -zipalign -apksign -input E:\yiduntest\test.apk
```

## 命令参数详解

### 必填参数

| 参数 | 说明 |
|------|------|
| `-yunconfig` | 必填项，表示自动从易盾后台获取加固参数 |
| `-input` | 必填项，待加固的APK/AAB文件绝对路径 |

### 可选参数

| 参数 | 说明 |
|------|------|
| `-output` | 指定加固后文件的输出路径和文件名。默认输出在原文件同路径 |
| `-zipalign` | 对加固后的APK包对齐。未对齐的包体可能存在安装失败的情况，**建议使用** |
| `-apksign` | 对加固后的APK包签名。需要配置config.ini文件内的[apksign]字段 |
| `-config` | 指定config文件路径。默认使用同目录下的config.ini |
| `-dex` | 对包体进行dex加密。注意：使用dex加密后如果需要上架Google Play，请确保Google Play自动完整性保护选项是关闭的 |
| `-antirepack` | 搭配dex保护使用，防止二次打包。会对加固时的原包签名和运行时的包签名进行校验 |
| `-u3dastenc` | Unity ab资源加密 |
| `-aabUseApksig` | AAB包签名时使用 |

## config.ini 配置文件

### 必须配置：AppKey

```ini
[appkey]
key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

AppKey 获取地址：https://dun.163.com/dashboard#/login/
在官网登录后进入"安全加固-服务管理"获取

### 可选配置：签名信息

使用 `-apksign` 参数时需要配置：

```ini
[apksign]
keystore=D:\\xxx\\xx.keystore
alias=xxx
pswd=xxx
aliaspswd=xxx
signver=v1+v2
```

**字段说明**：
- `keystore`: 签名文件的绝对路径
- `alias`: 签名别名
- `pswd`: 签名密码
- `aliaspswd`: 签名别名的密码
- `signver`: 签名版本，可选 v1、v2、v1+v2（推荐）

**注意**：
- 若只使用v2签名，仅支持Android 7.0以上系统
- AAB包签名需要加上 `-aabUseApksig` 参数

### 可选配置：SO保护

```ini
[so]
so1=libxxxx.so
so2=libyyyy.so
```

建议配置自研so，第三方so不建议处理

### 可选配置：自动更新

```ini
[update]
u=1
t=30
```

- `u=1`: 启用自动更新，`u=0`: 禁用
- `t=30`: 更新检测频率，单位为天

## 使用示例

### 示例 1：基础加固（推荐）

```bash
java -jar NHPProtect.jar -yunconfig -zipalign -input /path/to/test.apk
```

**说明**：
- 使用云端配置
- 包对齐（建议）
- 默认输出到原文件同目录

### 示例 2：加固+指定输出

```bash
java -jar NHPProtect.jar -yunconfig -zipalign \
  -output /output/test_protected.apk \
  -input /path/to/test.apk
```

### 示例 3：加固+自动签名

```bash
java -jar NHPProtect.jar -yunconfig -zipalign -apksign \
  -input /path/to/test.apk
```

**前置条件**：需要在 config.ini 中配置签名信息

### 示例 4：指定config路径

```bash
java -jar NHPProtect.jar -yunconfig \
  -config /custom/path/config.ini \
  -zipalign \
  -input /path/to/test.apk
```

### 示例 5：dex加密+防二次打包

```bash
java -jar NHPProtect.jar -yunconfig -zipalign -dex -antirepack \
  -input /path/to/test.apk
```

**注意**：
- 使用dex加密后，原包签名建议带上 v1+v2
- 如需上架Google Play，确保关闭自动完整性保护

### 示例 6：Unity ab资源加密

```bash
java -jar NHPProtect.jar -yunconfig -zipalign -apksign -u3dastenc \
  -input /path/to/unity_game.apk
```

需要在 config.ini 中配置：
```ini
[u3dabmode]
mode=4

[SymbolPath]
path=E:\TEST\Symbols
```

### 示例 7：AAB包加固

```bash
java -jar NHPProtect.jar -yunconfig -zipalign -apksign -aabUseApksig \
  -input /path/to/app.aab
```

## 输出文件

### 默认命名规则

- 原文件：`test.apk`
- 加固后：`test_protected.apk`（默认在原文件同目录）

### 指定输出路径

使用 `-output` 参数可以指定完整的输出路径和文件名：

```bash
java -jar NHPProtect.jar -yunconfig -zipalign \
  -output /custom/path/my_app_hardened.apk \
  -input /path/to/test.apk
```

## 注意事项

### 1. 包名报备
加固会强校验包名。如有新包名需要加固，**请提前向易盾运营报备**。

### 2. 签名和对齐
加固后的包**必须进行对齐和重签**才可以正常安装。建议：
- 使用 `-zipalign` 参数对齐
- 使用 `-apksign` 参数自动签名，或手动重签

### 3. 母包和渠道包
- 母包加固后可以分包
- 若母包加固后渠道包需要反编译，则母包加固时**不建议加上 `-dex`**

### 4. Unity版本兼容性
Unity 2019及以上版本，原包覆盖安装加固包时需要注意：
- 两个包体 `assets\bin\Data\boot.config` 内的 `buildDate` 需要不一样
- 否则由于Unity缓存机制会导致安装问题

### 5. 热更机制
使用防动态内存dump global-metadata.dat加固选项时：
- 需要确保 `libil2cpp.so` 和 `libunity.so` 均支持热更

### 6. 网络要求
`-yunconfig` 参数需要从易盾后台获取配置，确保网络连接正常。

## 工具更新

### 自动更新

工具会定期检测新版本，网络正常时自动升级。可通过 config.ini 配置：

```ini
[update]
u=1    # 启用自动更新
t=1    # 每1天检测一次
```

### 手动更新

```bash
java -jar NHPProtect.jar -update
```

## 故障排查

### 问题1：加固失败 - AppKey无效

**原因**：
- AppKey未配置或配置错误
- AppKey已过期
- 网络无法连接易盾服务器

**解决方案**：
1. 检查 config.ini 中的 AppKey 是否正确
2. 访问 https://dun.163.com/dashboard 验证AppKey状态
3. 检查网络连接

### 问题2：加固失败 - 包名未报备

**错误信息**：包名校验失败

**解决方案**：
联系易盾运营，报备新的包名

### 问题3：加固后无法安装

**原因**：包未对齐或未签名

**解决方案**：
1. 使用 `-zipalign` 参数对齐
2. 使用 `-apksign` 参数签名，或手动重签

### 问题4：Google Play上架失败

**原因**：使用了 `-dex` 加密且Google Play自动完整性保护冲突

**解决方案**：
在Google Play Console中关闭自动完整性保护：
版本 > 设置 > 应用完整性 > 自动完整性保护

## 最佳实践

### 推荐配置

```bash
# 基础加固（推荐新手使用）
java -jar NHPProtect.jar -yunconfig -zipalign -input app.apk

# 完整加固（推荐生产使用）
java -jar NHPProtect.jar -yunconfig -zipalign -apksign -dex -input app.apk
```

### 配置文件示例

```ini
[appkey]
key=your_32_char_appkey_here

[apksign]
keystore=/path/to/your.keystore
alias=your_alias
pswd=keystore_password
aliaspswd=alias_password
signver=v1+v2

[update]
u=1
t=7
```

### 工作流程

1. **首次配置**：
   ```bash
   # 配置 AppKey
   vi config.ini
   ```

2. **测试加固**：
   ```bash
   # 基础测试
   java -jar NHPProtect.jar -yunconfig -zipalign -input test.apk
   ```

3. **生产加固**：
   ```bash
   # 完整加固+签名
   java -jar NHPProtect.jar -yunconfig -zipalign -apksign -dex \
     -input release.apk
   ```

4. **验证结果**：
   - 检查输出文件是否生成
   - 安装测试加固后的APK
   - 功能完整性测试
   - 性能测试

## 相关文档

- 易盾控制台：https://dun.163.com/dashboard
- 官方文档：https://support.dun.163.com/documents/15588074449563648?docId=989347548106215424
- 客服支持：见易盾官网

---

**文档版本**：v1.0
**最后更新**：2026-02-27
