# 「自己」使用说明

> 微信画像分析 + 三层记忆系统 | 零门槛，5分钟上手

---

## 一、「自己」是什么

把你的微信聊天记录，变成一个"更懂你的 AI"。

**功能：**
1. 解密你自己的微信数据库（安全，不盗号）
2. 分析聊天记录，生成 9 个维度的人格画像
3. 画像存入三层记忆系统的冷层，AI 越用越懂你
4. 内置三层记忆系统，节省 99% Token

**适用系统：** Windows 10/11 + 微信 4.x（2025年8月后的版本）

---

## 二、目录结构（严格按三层记忆设计）

```
自己/
├── analyzer/                     ← 微信分析引擎
│   ├── setup.py                 ← 第1步：下载解密工具
│   ├── main.py                 ← 第3步：生成画像
│   ├── sync.py                 ← 第4步：同步到热层
│   └── config.py               ← 过滤规则（自动）
│
├── three-layer-memory/          ← 三层记忆系统（内置完整）
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── micro-sync.sh       ← 每天5次自动同步
│   │   ├── daily-wrapup.sh    ← 每天凌晨摘要
│   │   └── weekly-compound.sh ← 每周减脂
│   └── references/
│
└── storage/cold/另一个我/       ← ⭐ 画像文件存放位置（冷层）
    ├── wechat-profile.md          ← 基础人格画像
    ├── communication-patterns.md ← 沟通模式分析
    ├── emotional-trajectory.md   ← 情绪走势图
    ├── relationship-network.md   ← 关系图谱
    ├── interest-profile.md        ← 兴趣画像
    ├── psychological-profile.md  ← 心理画像
    ├── social-behavior.md        ← 社交行为分析
    ├── linguistic-signature.md   ← 语言印记
    ├── growth-trajectory.md     ← 成长轨迹
    └── timeline/                 ← 按季度归档
        └── 2026-Q2.md
```

---

## 三、安装步骤（首次，只需要做一次）

### Step 1：下载「自己」到你的电脑

把「自己」文件夹保存到任意位置，建议：
```
C:\Users\你的用户名\Desktop\自己\
```

### Step 2：安装解密工具

**重要：用管理员身份打开 PowerShell！**

右键 PowerShell → "以管理员身份运行"，然后运行：

```powershell
python "C:\Users\你的用户名\Desktop\自己\analyzer\setup.py"
```

等待下载完成。

### Step 3：触发密钥提取

解密微信数据库前，必须先让微信把密钥加载到内存：

1. 打开微信电脑版，登录你的账号
2. 在微信里随便打开**几张图片**（让微信缓存图片）
3. **保持微信在运行状态**，不要关闭

### Step 4：解密微信数据库

在 PowerShell（管理员）中运行：

```powershell
python C:\wechat-decrypt\main.py decrypt
```

**成功标志：**
```
21 成功, 0 失败, 共 21 个
解密数据量: 0.7GB
解密文件在: C:\wechat-decrypt\decrypted
```

如果显示"需要管理员权限"，确认 PowerShell 是以管理员身份运行的。

### Step 5：生成画像

```powershell
cd "C:\Users\你的用户名\Desktop\自己"
python analyzer/main.py
```

**成功标志：**
```
✅ 分析完成！
文件保存在: C:\Users\...\storage\cold\另一个我\
```

### Step 6：同步到热层（让 AI 记住你）

```powershell
python analyzer/sync.py
```

**成功标志：**
```
✅ Micro Sync 完成
```

---

## 四、查看生成的画像

画像文件位置：
```
C:\Users\你的用户名\Desktop\自己\storage\cold\另一个我\
```

打开任意 `.md` 文件查看：

| 文件 | 内容 |
|---|---|
| `wechat-profile.md` | 基础信息、群聊列表、联系人 |
| `relationship-network.md` | 好友关系、密切联系人 |
| `interest-profile.md` | 兴趣爱好分布 |
| `social-behavior.md` | 社交行为分析 |
| `linguistic-signature.md` | 你的说话风格 |
| `communication-patterns.md` | 沟通模式 |
| `emotional-trajectory.md` | 情绪变化 |
| `psychological-profile.md` | 心理画像 |
| `growth-trajectory.md` | 成长轨迹 |
| `timeline/2026-Q2.md` | 本季度数据快照 |

---

## 五、定期更新（数据有更新时）

微信每天都有新消息，想更新画像：

### 方式 A：完整更新

```powershell
# 1. 重新解密（确保微信在运行）
python C:\wechat-decrypt\main.py decrypt

# 2. 重新分析
cd "C:\Users\你的用户名\Desktop\自己"
python analyzer/main.py

# 3. 同步到热层
python analyzer/sync.py
```

### 方式 B：只更新分析（数据未变化时）

```powershell
cd "C:\Users\你的用户名\Desktop\自己"
python analyzer/main.py
python analyzer/sync.py
```

---

## 六、三层记忆系统说明

### 数据流向

```
微信记录导出
     ↓
分析引擎（main.py）
     ↓
结构化报告（9个.md文件）
     ↓
写入 cold layer（storage/cold/另一个我/）
     ↓
定期 Micro Sync（sync.py）
     ↓
更新到热层 MEMORY.md（AI 直接读取）
```

### 三层职责

| 层级 | 内容 | 更新频率 |
|---|---|---|
| **热层** | MEMORY.md | 每次 sync 更新 |
| **暖层** | Micro Sync 扫描 session 记录 | 每天 5 次 |
| **冷层** | storage/cold/另一个我/ | 每次 main.py 运行 |

### Token 节省

- **无三层记忆**：每次对话重载全部上下文 → 消耗大
- **有三层记忆**：热层 ≤8KB，AI 每次只读关键信息 → **节省 99% Token**

---

## 七、过滤规则（自动，无需手动）

以下内容会自动过滤，**不会**出现在画像里：

- ❌ 营销/福利群（奶茶、咖啡、外卖、优惠券等）
- ❌ 公众号推送（gh_ 开头的服务号）
- ❌ 商业账号（论文辅导、考证推销等）
- ❌ 机器人消息

**只会分析你的真实社交数据。**

---

## 八、隐私说明

- ✅ **本地运行**：所有数据存在你自己的电脑，不上传任何服务器
- ✅ **不盗账号**：wechat-decrypt 从进程内存读取密钥，不需要微信账号密码
- ✅ **仅分析自己**：只分析你自己的微信数据，不涉及第三方隐私
- ✅ **可删除**：随时可以删除 `C:\wechat-decrypt` 文件夹

---

## 九、常见问题

### Q1: 解密失败，显示"权限不足"
确认 PowerShell 是**以管理员身份运行**的。右键 PowerShell 图标 → "以管理员身份运行"。

### Q2: 解密失败，显示"微信未运行"
确保微信电脑版已经**登录并保持运行**，不要最小化或锁屏。

### Q3: 解密成功但分析报错
可能是路径有中文，先把「自己」文件夹放到纯英文路径下，比如：
```
C:\Users\你的用户名\Desktop\自己\
```

### Q4: 想换一台电脑使用
重新走一遍 Step 1~6 即可，画像文件可以复制带走。

### Q5: 微信版本低于 4.x
微信 4.x 是 2025年8月后的版本，旧版本不支持。更新微信即可。

---

## 十、文件清单

```
自己/
├── README.md                      ← 你现在看的（用户版）
├── SKILL.md                       ← 技术文档
├── analyzer/
│   ├── setup.py                  ← Step 2：安装解密工具
│   ├── main.py                   ← Step 5：生成画像
│   ├── sync.py                   ← Step 6：同步到热层
│   ├── config.py                 ← 过滤规则（自动）
│   └── models.py                 ← 数据模型（自动）
├── three-layer-memory/            ← 三层记忆系统（内置）
│   ├── SKILL.md                 ← 详细文档
│   ├── scripts/                  ← 定时脚本
│   └── references/               ← 规则参考
└── storage/                      ← 画像存储（运行后生成）
    └── cold/
        └── 另一个我/              ← 9个画像文件 + timeline/
```

---

## 十一、一句话总结

> 下载 → 安装解密工具 → 解密微信 → 运行分析 → 同步到热层 → AI 越用越懂你
