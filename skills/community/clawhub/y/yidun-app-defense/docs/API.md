# YiDunAppDefense API 文档

## 脚本接口

### setup.sh

初始化易盾加固工具。

**用法**:
```bash
./scripts/setup.sh
```

**功能**:
- 检查 Java 环境
- 创建工作目录 `~/.yidun-defense/`
- 下载易盾加固工具
- 验证工具完整性
- 创建配置文件模板

**返回值**:
- `0`: 成功
- `1`: 失败

**环境要求**:
- Java 8+
- curl 或 wget

---

### configure.sh

配置易盾 AppKey。

**用法**:

```bash
# 交互式配置
./scripts/configure.sh

# 直接设置
./scripts/configure.sh <appkey>

# 显示当前配置
./scripts/configure.sh --show

# 显示帮助
./scripts/configure.sh --help
```

**参数**:
- `<appkey>`: 易盾 AppKey（可选）
- `--show`: 显示当前配置
- `--help`: 显示帮助信息

**返回值**:
- `0`: 成功
- `1`: 失败

**配置文件**:
- 位置: `~/.yidun-defense/config.ini`
- 格式: INI

---

### defense-smart.sh

智能多平台加固脚本（统一入口）。

**用法**:

```bash
./scripts/defense-smart.sh <file> [options]
./scripts/defense-smart.sh --help
```

**参数**:
- `<file>`: 要加固的文件路径（必需）
- `--auto`: 完全自动模式，无需交互
- `--platform <type>`: 指定平台类型（android/ios/harmony/h5/sdk/pc）
- `--help`: 显示帮助信息

**返回值**:
- `0`: 加固成功
- `1`: 加固失败

**输出**:
- 加固后的文件：`<原文件名>_protected.*`
- 日志文件：`/tmp/yidun-defense.log`

**示例**:

```bash
# 自动识别并加固
./scripts/defense-smart.sh demo.apk

# 完全自动模式（CI/CD）
./scripts/defense-smart.sh /path/to/release.apk --auto

# 指定平台
./scripts/defense-smart.sh app.zip --platform android

# 输出将生成在同一目录
# demo.apk -> demo_protected.apk
```

---

## 配置文件格式

### config.ini

```ini
[appkey]
# 易盾 AppKey（必需）
key=your_appkey_here

[so]
# 需要保护的 so 文件名称
so1=
so2=

[apksign]
# Android 签名配置（可选）
keystore=
alias=
pswd=
aliaspswd=
signver=v1+v2

[hapsign]
# 鸿蒙签名配置（可选）
keystoreFile=
keystorePwd=
keyAlias=
keyPwd=
appCertFile=
profileFile=
mode=
signAlg=

[update]
# 自动更新检测
u=1
t=30
```

**配置项说明**:

| 配置节 | 配置项 | 类型 | 必需 | 说明 |
|--------|--------|------|------|------|
| `[appkey]` | `key` | string | 是 | 易盾 AppKey，从控制台获取 |
| `[so]` | `so1`, `so2` | string | 否 | 需要保护的 so 文件名称 |
| `[apksign]` | `keystore` | string | 否 | Android 签名 keystore 路径 |
| `[apksign]` | `alias` | string | 否 | keystore 别名 |
| `[apksign]` | `pswd` | string | 否 | keystore 密码 |
| `[apksign]` | `signver` | string | 否 | 签名版本，默认 v1+v2 |
| `[hapsign]` | `keystoreFile` | string | 否 | 鸿蒙签名 keystore 文件路径 |
| `[hapsign]` | `keystorePwd` | string | 否 | keystore 密码 |
| `[update]` | `u` | int | 否 | 是否检测更新（0=否, 1=是） |
| `[update]` | `t` | int | 否 | 检测间隔（天） |

---

## Java 工具调用

### 命令格式

```bash
java -jar yidun-tool.jar [options]
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-config` | 配置文件路径 | `-config config.ini` |
| `-input` | 输入 APK 路径 | `-input app.apk` |
| `-output` | 输出 APK 路径 | `-output app_protected.apk` |

**注意**: 实际参数可能因易盾工具版本而异，请参考官方文档。

---

## AI Agent 集成

### Skill 元数据

**SKILL.md 配置**:

```yaml
---
description: 易盾应用加固 - AI Agent Skill for Android APK protection
metadata:
  nanobot:
    always: false
    requires:
      bins: ["java", "curl"]
      env: []
---
```

### Agent 调用示例

```python
# 伪代码示例：Agent 如何调用 skill

def handle_defense_request(user_message, apk_path):
    """
    处理用户的加固请求

    Args:
        user_message: 用户消息，如 "帮我加固这个APK"
        apk_path: APK 文件路径

    Returns:
        加固结果消息
    """

    # 1. 检查工具是否已安装
    if not tool_installed():
        run_command("./scripts/setup.sh")

    # 2. 检查 AppKey 是否已配置
    if not appkey_configured():
        appkey = prompt_user("请输入您的 AppKey：")
        run_command(f"./scripts/configure.sh {appkey}")

    # 3. 执行加固
    result = run_command(f"./scripts/defense-smart.sh {apk_path}")

    # 4. 返回结果
    if result.success:
        return f"加固完成！输出文件: {result.output_file}"
    else:
        return f"加固失败: {result.error}"
```

### 提示词识别

Agent 应能识别以下模式：

```python
DEFENSE_PATTERNS = [
    r"加固.*\.apk",
    r"使用易盾.*\.apk",
    r"保护.*APK",
    r"加密.*应用",
    r"defense.*apk",
]

CONFIG_PATTERNS = [
    r"配置.*appkey",
    r"更新.*密钥",
    r"设置.*易盾",
]
```

---

## 错误码

### 通用错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `E001` | Java 环境未找到 | 安装 JRE 8+ |
| `E002` | 工具下载失败 | 检查网络或手动下载 |
| `E003` | 配置文件不存在 | 运行 setup.sh |
| `E004` | AppKey 未配置 | 运行 configure.sh |
| `E005` | APK 文件不存在 | 检查文件路径 |

### 加固错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `D001` | AppKey 无效 | 检查 AppKey 是否正确 |
| `D002` | APK 格式错误 | 确保是有效的 APK 文件 |
| `D003` | 配额不足 | 充值或联系客服 |
| `D004` | 网络超时 | 检查网络连接 |
| `D005` | 服务异常 | 稍后重试或联系技术支持 |

---

## 日志格式

### 标准输出

```
[INFO] 检查 Java 环境...
[SUCCESS] Java 环境检查通过 (version: 11.0.12)
[INFO] 开始加固 APK 文件...
[INFO] 输入文件: /path/to/demo.apk
[INFO] 输出文件: /path/to/demo_protected.apk
[SUCCESS] 加固完成！
```

### 日志文件

位置: `/tmp/yidun-defense.log`

```
2026-02-27 10:30:15 [INFO] Starting defense process
2026-02-27 10:30:16 [INFO] Input: /path/to/demo.apk
2026-02-27 10:30:16 [INFO] AppKey: abc***def (masked)
2026-02-27 10:30:20 [INFO] Tool execution started
2026-02-27 10:32:45 [SUCCESS] Defense completed
2026-02-27 10:32:45 [INFO] Output: /path/to/demo_protected.apk
```

---

## 性能指标

### 典型加固时间

| APK 大小 | 加固时间 | 内存使用 |
|----------|----------|----------|
| < 10 MB | 30-60s | ~500 MB |
| 10-50 MB | 1-3 min | ~800 MB |
| 50-100 MB | 3-5 min | ~1.2 GB |
| > 100 MB | 5-10 min | ~2 GB |

### 文件大小变化

通常加固后文件大小增加 **10-20%**。

---

## 安全性

### AppKey 存储

- AppKey 存储在 `~/.yidun-defense/config.ini`
- 文件权限应设置为 `600`（仅所有者可读写）
- 不要将 AppKey 提交到版本控制系统

### 临时文件

- 加固过程中可能产生临时文件
- 临时文件会在加固完成后自动清理
- 位置: `/tmp/yidun-*`

### 网络通信

- 工具下载使用 HTTPS
- 加固服务使用加密通信
- AppKey 通过安全通道传输

---

## 版本兼容性

### 支持的平台

- macOS 10.14+
- Ubuntu 18.04+
- Debian 10+
- CentOS 7+

### Java 版本

- 最低要求: JRE 8
- 推荐版本: JRE 11+

### Android 版本

- 支持: Android 4.4 (API 19) 及以上
- 推荐: Android 5.0 (API 21) 及以上

---

## 更新记录

### v1.0.0 (2026-02-27)

- ✨ 初始版本发布
- 🎯 支持 APK 加固功能
- ⚙️ 对话式 AppKey 配置
- 📦 自动工具下载
- 📝 完整文档

---

## 技术支持

- **官方文档**: https://support.dun.163.com/
- **控制台**: https://dun.163.com/dashboard
- **GitHub Issues**: (如果开源)
- **ClawHub**: https://clawhub.ai/
