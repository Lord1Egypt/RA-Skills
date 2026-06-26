# 小红书爬虫 Skill

## 功能描述
基于Python的小红书关键词爬取工具，支持搜索和抓取小红书笔记内容，自动推送到飞书群。

## 核心特性
- ✅ **浏览器模拟搜索** - 绕过API限制，搜索成功率更高
- ✅ **Cookie自动管理** - 过期自动触发二维码登录
- ✅ **飞书集成** - 结果自动以卡片形式推送到飞书群
- ✅ **指令识别** - 支持 `run-xhs:关键词` 格式指令

## 命令列表

### run-xhs
执行小红书关键词爬取

**语法：** `run-xhs <关键词>`

**示例：**
- `run-xhs 新燕宝2025` - 搜索"新燕宝2025"相关笔记
- `run-xhs 中间带新燕宝` - 搜索"中间带新燕宝"相关笔记

**说明：**
- 默认返回5条笔记
- 搜索时间约10-30秒
- 结果自动发送到飞书群

### xhs-help
显示帮助信息

**示例：** `xhs-help`

## 环境要求

### Python环境
- Python 3.8+
- 依赖包：
  ```bash
  pip install playwright requests
  playwright install chromium
  ```

### 配置文件
在 `config.py` 中配置以下参数：

```python
# 飞书应用凭证（必填）
FEISHU_APP_ID = "cli_a924d921ce7a9cbd"
FEISHU_APP_SECRET = "5QG92Lp8kvhAkgpPJTd57fIxshnCebEt"

# 群聊ID（在example_openclaw_skill.py中配置）
FEISHU_CHAT_ID = "oc_29fbba0871ab7371a4c1a1ebe0350dac"
```

### OpenClaw配置

#### 方式1：通过配置文件添加（推荐）
在 OpenClaw 的 `config/default.json` 中添加：

```json
{
    "skills": [
        {
            "name": "xhs-crawler",
            "type": "local",
            "path": "D:\\pycharm\\projects\\小红书关键词爬取\\openclaw封装skill",
            "config": {
                "pythonEnv": "python"
            }
        }
    ]
}
```

**注意**：`path` 应该指向 Skill 文件夹，而不是 `index.js` 文件。

#### 方式2：通过 OpenClaw 命令行安装
```bash
# 在 OpenClaw 目录下执行
openclaw skill install D:\pycharm\projects\小红书关键词爬取\openclaw封装skill
```

## 工作流程

```
用户飞书输入: run-xhs 新燕宝2025
    ↓
OpenClaw 接收指令
    ↓
调用 example_openclaw_skill.py "run-xhs：新燕宝2025"
    ↓
解析指令 → 提取关键词
    ↓
检查Cookie有效性
    ↓
├── Cookie有效 → 继续搜索
└── Cookie失效 → 自动二维码登录
        ↓
    截图发送到飞书群
        ↓
    用户手机扫码登录
        ↓
    自动保存Cookie
        ↓
浏览器搜索小红书
    ↓
提取笔记信息（标题、链接、作者、点赞数）
    ↓
发送结果卡片到飞书群
```

## 文件结构

```
openclaw封装skill/
├── index.js                      # OpenClaw Skill入口
├── package.json                  # Node.js项目配置
├── example_openclaw_skill.py     # Python主程序
├── config.py                     # 配置文件
├── feishu_app_bot.py            # 飞书应用机器人
├── cookie_manager.py            # Cookie管理
├── auto_login_with_qrcode.py    # 自动二维码登录
├── xhs_search_with_browser.py   # 浏览器搜索
└── SKILL.md                     # 本文档
```

## 使用示例

### 1. 命令行测试
```bash
cd "D:\pycharm\projects\小红书关键词爬取\openclaw封装skill"
python example_openclaw_skill.py "run-xhs：新燕宝2025"
```

### 2. OpenClaw集成后飞书使用
```
run-xhs 新燕宝2025
```

飞书群将收到：
```
📱 小红书搜索报告

关键词: 新燕宝2025
共找到: 5 条笔记
时间: 2026-03-18 11:09

1. 0岁宝宝疫苗儿保一站式搞定...
   熙熙妈宝藏分享 | 👍 187
   [查看笔记]

2. 新燕宝·开年福利降免赔额...
   中间带新燕宝 | 👍 20
   [查看笔记]

...
```

## 注意事项

1. **首次使用**：需要先运行 `python login.py` 手动登录一次，保存Cookie
2. **Cookie过期**：程序会自动检测并发送二维码到飞书群，扫码后即可继续
3. **IP风控**：如遇"IP存在风险"错误，请切换网络或等待2-4小时
4. **搜索频率**：已设置防风控机制，请求间隔2-5秒

## 故障排查

| 问题 | 解决方法 |
|------|---------|
| 搜索不到结果 | 尝试更换关键词，如"新燕宝2025"代替"新燕宝" |
| Cookie频繁失效 | 正常现象，程序会自动触发重新登录 |
| 飞书收不到消息 | 检查App ID、App Secret、群聊ID是否正确 |
| IP被风控 | 切换手机热点，或等待2-4小时 |

## 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-03-18 | 1.0.0 | 初始版本，完整功能实现 |
