# taobao-image-search-skill

淘宝以图搜同款与加购技能（脚本优先，browser 兜底）。现已支持自动登录检测与任务自动续行。

## 功能

- **以图搜同款**: 基于图片在淘宝搜索同款/相似商品
- **自动化流程**: 自动进入候选商品详情页并尝试加入购物车
- **自动登录检测**: 自动校验登录状态。若未登录，会弹出登录窗口并等待登录后再自动继续执行任务。
- **结构化结果**: 产出结构化结果与截图，便于回归验证

## 快速开始

### 安装与环境

1. 克隆或复制这些脚本到您的本地环境。
2. 安装 Playwright 及其浏览器依赖：
   ```bash
   npm install playwright
   npx playwright install chromium
   ```

### 2. 准备测试图片

默认使用仓库内 `test.png`。也可以在执行时传入任意本地图片路径：

## 安全与隐私提醒

> [!CAUTION]
> **本技能会在本地持久化浏览器会话令牌。**
> - 存储位置：`verification-artifacts/taobao-storage-state.json` 与 `.pw-user-data-taobao/`。
> - 这些文件包含您的淘宝登录 Cookies。**严禁分享或上传这些文件。**
> - 请仅在受信的个人机器上使用本技能。
> - 若需彻底注销并清除令牌，请手动删除上述目录。

```bash
node run-taobao-task.js --image /absolute/path/to/your-image.png
```

### 3. 执行完整链路（支持自动登录）

你不再需要手动运行 `save-taobao-cookie.js`。直接运行主入口即可：

```bash
node run-taobao-task.js --image ./test.png --headed
```

**执行逻辑：**
1. 脚本会检查淘宝登录状态。
2. 若 **未登录**，会自动打开有界面浏览器窗口。
3. 请在窗口内完成登录。
4. 脚本 **自动检测** 登录成功后，会 **立即续行** 原有的搜索任务。

### 4. 进阶参数

可以直接通过主入口传递参数给底层脚本：

```bash
node run-taobao-task.js --image ./test.png --headed --delay-ms 5000
```

可选参数：
- `--image, -i`：图片路径（默认 `test.png`）
- `--headless` / `--headed`：是否无头运行（默认 `--headed`）
- `--out-dir`：输出目录（默认 `verification-artifacts`）
- `--delay-ms`：为关键等待步骤增加额外延迟（默认 `5000`）

## 输出结果

- `verification-artifacts/result.json`：结构化执行结果
- `verification-artifacts/run-log.txt`：详细执行日志
- `verification-artifacts/*.png`：关键步骤截图

关键字段：
- `success`：流程是否整体执行成功
- `loginCheck.isLoggedIn`：登录状态
- `addToCart.success`：是否检测到加购成功提示

## 目录结构

- `SKILL.md`：OpenClaw/Codex 技能说明（脚本优先）
- `run-taobao-task.js`：支持自动登录的主入口脚本
- `auto-login-taobao.js`：自动登录监测脚本
- `verify-taobao-runner.js`：底层自动化验证脚本

## 常见问题

- **登录超时**：10 分钟内未完成登录，脚本将中止
- **页面变更**：若淘宝结构调整，请参考 `SKILL.md` 的 browser 工具回退流程手动验证
- **加购失败**：通常是规格选择、风控或登录态过期导致
