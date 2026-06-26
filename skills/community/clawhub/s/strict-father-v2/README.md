# 严厉的父亲 · Strict Father — 安装包

> 紫微斗数12宫框架下的残酷真相诊断器
> 联系作者 @yongzhuan_bot

---

## 文件结构

```
strict-father/
├── SKILL.md              ← 核心技能文件（主文件）
├── README.md             ← 本说明
├── install.sh            ← 一键安装脚本
└── scripts/
    └── calculate.js      ← 紫微斗数排盘脚本（基于iztro）
```

## 安装

### 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/0xcii/strict-father/main/install.sh | bash
```

### 手动安装（Hermes）

```bash
# 安装技能
mkdir -p ~/.hermes/skills/strict-father
cp SKILL.md ~/.hermes/skills/strict-father/

# 安装排盘脚本（可选）
mkdir -p ~/.hermes/skills/strict-father/scripts
cp scripts/calculate.js ~/.hermes/skills/strict-father/scripts/
cd ~/.hermes/skills/strict-father && npm init -y && npm install iztro
```

### 手动安装（Open Claw）

```bash
mkdir -p ~/.claude/skills
cp SKILL.md ~/.claude/skills/strict-father.md
```

## 使用

### Hermes

```
/skill strict-father
```

技能加载后，AI会**首先要求你提供出生时间**（年月日+时辰+性别）。没有命盘不做分析。

收到出生信息后，AI自动调用排盘脚本计算命盘，然后基于命盘12宫输出你的真实盲区。

### Open Claw

```
/strict-father
```

---

## 排盘脚本

技能的核心是**AI自动调用排盘脚本**，不需要用户手动操作。

但如果你只是想测试排盘，可以手动运行：

```bash
cd ~/.hermes/skills/strict-father
node scripts/calculate.js 1956-09-12 16:00 男
```

输出结构化JSON，包含12宫星曜、四化、三方四正。

AI根据命盘数据，能给出更精准的个人分析。

---

## 框架说明

"严厉的父亲"不是命理软件。它是一个**基于紫微斗数12宫的结构化自我审视框架**。

核心逻辑：

```
你没有意识到的盲区 = 
  你的行为模式（从历史记录提取）
  × 你的命盘结构（从出生时间计算）
  × 人类社会的基本规律（从逻辑推演）
  ÷ 你给自己讲的自我安慰的故事（需要你主动识别）
```

---

## 关注获取更多

关注 [@yongzhuan_bot](https://t.me/yongzhuan_bot) 获取更多深度个人成长与web3内容。
