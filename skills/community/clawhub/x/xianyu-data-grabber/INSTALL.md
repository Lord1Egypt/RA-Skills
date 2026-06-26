# 🐾 闲鱼数据抓取技能 - 一键安装

## 快速安装（推荐）

**复制以下命令，发送给 OpenClaw 执行：**

```bash
curl -sL https://raw.githubusercontent.com/your-username/xianyu-data-grabber/main/install.sh | bash
```

**或者本地安装：**

```bash
cd /root/.openclaw/workspace
bash skills/xianyu-data-grabber/install.sh
```

---

## 安装过程

脚本会自动完成以下步骤：

1. ✅ 检查 Python3 和 Node.js
2. ✅ 安装 Tesseract OCR（系统依赖）
3. ✅ 安装 Python 依赖（pillow, pytesseract, opencv）
4. ✅ 安装 Node 依赖（playwright）
5. ✅ 下载 Chromium 浏览器（约 100MB）
6. ✅ 创建配置文件
7. ✅ 设置文件权限
8. ✅ 配置定时任务
9. ✅ 测试验证

**预计时间**: 5-10 分钟（主要耗时在浏览器下载）

---

## 安装后配置（可选）

### 1. 配置 Gitee（自动上传）

编辑 `~/.openclaw/workspace/.xianyu-grabber-config.json`:

```json
{
  "gitee": {
    "token": "你的 Gitee 个人访问令牌",
    "owner": "你的 Gitee 用户名",
    "repo": "xianyu-data"
  }
}
```

**获取 Gitee Token**:
1. 登录 https://gitee.com
2. 设置 → 个人访问令牌
3. 创建令牌（勾选 `projects` 权限）

### 2. 配置闲鱼 Cookie（提高成功率）

编辑同一配置文件:

```json
{
  "xianyu": {
    "cookie": "你的闲鱼 Cookie"
  }
}
```

**获取 Cookie**:
1. 浏览器登录闲鱼
2. F12 → Network → 刷新
3. 复制 Cookie 字段

---

## 验证安装

```bash
# 查看技能状态
cd /root/.openclaw/workspace
./skills/xianyu-data-grabber/run.sh status

# 测试抓取
./skills/xianyu-data-grabber/run.sh grab "Magisk"

# 测试可视化
./skills/xianyu-data-grabber/run.sh visualize

# 查看帮助
./skills/xianyu-data-grabber/run.sh help
```

---

## 常见问题

### Q1: Tesseract 安装失败

**解决**:
```bash
# Ubuntu/Debian
apt-get install tesseract-ocr tesseract-ocr-chi-sim

# CentOS/RHEL
yum install tesseract tesseract-langpack-chi_sim
```

### Q2: Playwright 浏览器下载失败

**解决**:
```bash
# 手动下载
npx playwright install chromium

# 或使用国内镜像
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
npx playwright install chromium
```

### Q3: Python 依赖安装失败

**解决**:
```bash
# 使用国内镜像
pip3 install pillow pytesseract opencv-python-headless \
  -i https://pypi.tuna.tsinghua.edu.cn/simple \
  --break-system-packages
```

### Q4: 权限不足

**解决**:
```bash
# 使用 sudo
sudo bash skills/xianyu-data-grabber/install.sh

# 或修改目录权限
chmod -R 755 ~/.openclaw/workspace
```

---

## 卸载

```bash
# 删除技能目录
rm -rf ~/.openclaw/workspace/skills/xianyu-data-grabber

# 删除配置文件
rm ~/.openclaw/workspace/.xianyu-grabber-config.json

# 删除定时任务
crontab -l | grep -v xianyu | crontab -

# 删除数据（可选）
rm -rf ~/.openclaw/workspace/legion/data/xianyu-*
rm -rf ~/.openclaw/workspace/legion/screenshots/xianyu-*
```

---

## 更新

```bash
# 拉取最新代码
cd ~/.openclaw/workspace/skills/xianyu-data-grabber
git pull origin main

# 重新安装依赖
bash install.sh
```

---

## 技术支持

- 技能文档：`skills/xianyu-data-grabber/SKILL.md`
- 使用说明：`skills/xianyu-data-grabber/USAGE.md`
- 功能清单：`skills/xianyu-data-grabber/FEATURES.md`

---

**作者**: 爪爪 🐾  
**版本**: 3.0  
**日期**: 2026-03-20
