# 安装指南 - 微信公众号运营技能

## 前提条件

1. **WorkBuddy** 已安装
2. **Python 3.8+** 已安装（用于运行自动化发布脚本）
3. 已认证的**微信公众号**（订阅号或服务号均可）

---

## 快速安装

### 方法一：解压到 skills 目录

1. 将 `wechat-official-account.zip` 解压
2. 将解压后的 `wechat-official-account` 文件夹放入：
   - **Windows**：`C:\Users\你的用户名\.workbuddy\skills\`
   - **macOS/Linux**：`~/.workbuddy/skills/`
3. 重启 WorkBuddy，技能自动加载

### 方法二：使用 WorkBuddy 技能市场安装（如有）

直接在技能市场搜索 "wechat-official-account" 安装。

---

## 配置公众号凭证

### 1. 获取 AppID 和 AppSecret

- 登录 [微信公众平台](https://mp.weixin.qq.com)
- 路径：「设置与开发」→「基本配置」

### 2. 查询你的出口 IP 并加入白名单

```powershell
# Windows PowerShell
(Invoke-WebRequest -Uri "https://api.ipify.org").Content
```

```bash
# Linux / macOS
curl ifconfig.me
```

将查到的 IP 填入公众平台「IP白名单」。

### 3. 创建凭证文件

在你的工作目录创建 `wechat_credentials.json`：

```json
{
  "appid": "wx你的AppID",
  "appsecret": "你的AppSecret"
}
```

---

## 安装 Python 依赖

```bash
pip install requests Pillow
```

---

## 验证安装

在 WorkBuddy 中输入：

```
写推文 帮我写一篇关于[主题]的公众号文章
```

或者直接测试脚本：

```bash
python scripts/publish.py 你的文章.md 封面图.png
```

---

## 依赖的其他技能（可选）

以下技能配合使用效果更好：

| 技能 | 用途 | 是否必须 |
|------|------|---------|
| `humanizer` | 去除 AI 写作痕迹 | 可选 |
| `baidu-search` | 选题研究 | 可选 |
| `多模态内容生成` | 生成封面图/配图 | 可选 |
| `agent-browser` | 浏览器自动化 | 可选 |

---

## 常见问题

**Q: 提示 IP 不在白名单 (40164)?**
A: 重新查询出口 IP，更新白名单，IP 可能因网络变动而改变。

**Q: 提示无效 media_id (40007)?**
A: 确保封面图使用了永久素材接口 (`add_material`)，而非临时素材接口。

**Q: Python 脚本找不到 requests 模块?**
A: 运行 `pip install requests Pillow` 安装依赖。

---

更多详情参见 `references/` 目录中的文档。
