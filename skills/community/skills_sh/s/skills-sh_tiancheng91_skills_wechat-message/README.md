# 微信消息发送 - 使用说明

在 macOS 上通过命令行或剪切板，自动向微信联系人或群组发送消息。

---

## 环境要求

- **系统**：macOS 或 Windows
- **应用**：
  - macOS：已安装并登录 [微信 for Mac](https://mac.weixin.qq.com/)
  - Windows：已安装并登录 [微信 for Windows](https://windows.weixin.qq.com/)
- **权限**：
  - macOS：终端（或运行脚本的应用）需已授予 **辅助功能** 权限
  - Windows：以当前登录用户运行即可，无需额外权限

---

## 快速开始

在项目根目录执行：

**macOS：**
```bash
osascript scripts/wechat_automation_script.applescript "联系人名称" "消息内容" "图片路径"
```

**Windows（PowerShell）：**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/wechat_automation_script.ps1 "联系人名称" "消息内容" "图片路径"
```

例如给好友「张三」发一条消息：

**macOS：**
```bash
osascript scripts/wechat_automation_script.applescript "张三" "你好，今天有空吗？"
```

**Windows：**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/wechat_automation_script.ps1 "张三" "你好，今天有空吗？"
```

执行成功后终端会输出：`微信消息发送完成`，全程约 15 秒。

---

## 命令格式

**macOS：**
```bash
osascript scripts/wechat_automation_script.applescript [联系人名称] [消息内容]
```

**Windows：**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/wechat_automation_script.ps1 [联系人名称] [消息内容]
```

| 参数           | 必填 | 说明 |
|----------------|------|------|
| 联系人名称     | 否*  | 微信好友备注名或群名称，需与微信里显示一致；不传则从 **剪切板** 读取 |
| 消息内容       | 否** | 要发送的文本；不传则从 **剪切板** 读取（仅文本模式） |
| 图片路径/URL   | 否** | 本地图片路径或 `http(s)://` 图片地址；与消息至少提供一项 |

\* 两个参数都不传时，会依次从剪切板取「联系人名称」和「消息内容」并发送。若只传一个参数，另一个仍从剪切板获取。

\** 使用第三个参数发送图片时，消息内容可传空字符串 `""`；若同时提供消息与图片，先发送文本再发送图片。

**使用剪切板方式**：先把「联系人名称」或「消息内容」复制到剪切板，再在项目根目录执行：

**macOS：**
```bash
# 不传参数：从剪切板读取联系人 + 消息（需事先复制好对应内容）
osascript scripts/wechat_automation_script.applescript
```

**Windows：**  
剪切板内容为两行：第一行为联系人名称，第二行起为消息内容。然后执行：
```powershell
powershell -ExecutionPolicy Bypass -File scripts/wechat_automation_script.ps1
```

---

## 使用示例

### 1. 给好友发消息

```bash
osascript scripts/wechat_automation_script.applescript "张三" "你好，今天有空吗？"
```

### 2. 给群组发消息

```bash
osascript scripts/wechat_automation_script.applescript "工作群" "今天下午 3 点开会，请准时参加。"
```

### 3. 多行消息

多行内容直接写在第二个参数里即可（保持引号内换行）：

```bash
osascript scripts/wechat_automation_script.applescript "张三" "会议通知：

时间：下午 3 点
地点：会议室 A
主题：项目进度讨论"
```

### 4. 消息中含引号

引号需转义，例如：

```bash
osascript scripts/wechat_automation_script.applescript "张三" "他说\"好的\"，明天见"
```

### 5. 群内 @ 某人

```bash
osascript scripts/wechat_automation_script.applescript "项目组" "@张三 请查收最新文档"
```

### 6. 中英文混合

```bash
osascript scripts/wechat_automation_script.applescript "Yatocala" "hello，这是测试消息"
```

### 7. 发送本地图片

仅发图片（消息参数传空字符串）：

```bash
osascript scripts/wechat_automation_script.applescript "张三" "" "/Users/me/Desktop/screenshot.png"
```

先发文字再发图片：

```bash
osascript scripts/wechat_automation_script.applescript "张三" "请看截图" "/Users/me/Desktop/screenshot.png"
osascript scripts/wechat_automation_script.applescript "张三" "" "https://example.com/image.png"
```

**Windows：**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/wechat_automation_script.ps1 "张三" "" "C:\Users\me\Desktop\screenshot.png"
```

---

## 权限配置

若脚本报错或无法控制微信窗口，请检查辅助功能权限：

1. 打开 **系统设置** → **隐私与安全性** → **辅助功能**
2. 将 **终端**（或你用来执行命令的 App，如 iTerm、Cursor 等）加入列表并勾选
3. 如有 **System Events**，也建议勾选

修改后若仍无效，可重启终端再试。

---

## 注意事项

- **微信需已登录**：执行前请确认微信 for Mac/Windows 已登录且未被退出
- **联系人名称要一致**：名称需与微信中显示的备注/群名完全一致，脚本会选「搜索到的第一个结果」
- **执行期间勿操作微信**：约 15 秒内请勿切换窗口或键盘操作，以免打断流程
- **编码**：终端建议使用 UTF-8，避免中文乱码
- **Windows**：首次运行若提示无法执行脚本，请使用 `-ExecutionPolicy Bypass`；若微信内修改过「搜索」快捷键，需在 `wechat_automation_script.ps1` 中将 `^f` 改为对应快捷键（如 `^k`）

---

## 常见问题

| 现象           | 可能原因           | 建议 |
|----------------|--------------------|------|
| 消息没发出去   | 焦点不在输入框     | 不要在此期间点击其他窗口，可重试一次 |
| 搜不到联系人   | 名称不一致         | 在微信里确认备注名/群名，再原样填写 |
| 脚本报错/无反应 | 未给辅助功能权限   | 按上文「权限配置」检查并勾选终端等 App |
| 不能获得 window 1 | 微信被隐藏/最小化  | 脚本会 `open -a WeChat` 尝试恢复一次；仍失败时手动打开微信 |
| 中文乱码       | 终端编码非 UTF-8   | 在终端设置里改为 UTF-8 后重试 |

---

## 项目结构

```
wechat-message/
├── README.md               # 本使用说明
├── SKILL.md                # 技能/集成说明
├── scripts/
│   ├── wechat_automation_script.applescript   # macOS 发送脚本
│   └── wechat_automation_script.ps1          # Windows 发送脚本（PowerShell）
└── examples/
    └── sample.md           # 更多示例
```

更多示例见 `examples/sample.md`。
