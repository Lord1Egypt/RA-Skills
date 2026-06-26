---
name: sbti-personality-test
description: "SBTI 恶搞人格测试数据包 - 极简暗黑风格的 MBTI 恶搞测试数据，包含20道搞笑题目、5种人格结果、15个维度定义。纯数据文件，适合自定义前端实现。"
metadata:
  openclaw:
    emoji: "🎭"
    category: "entertainment"
    version: "1.0.2"
    author: "OpenClaw"
    requires:
      bins: []
      env: []
user-invocable: true
disable-model-invocation: false
---

# 🎭 SBTI 恶搞人格测试数据包

## 🎯 核心价值

**MBTI 恶搞人格测试数据包**

- ✅ 20 道搞笑题目（精简格式）
- ✅ 5 种人格结果（DEAD, FUCK, ATM, MALO, SHIT）
- ✅ 15 个维度定义
- ✅ 纯数据文件（JSON 格式）
- ✅ 易于自定义和扩展

---

## 📦 包含内容

### 数据文件

1. **questions.json** - 20 道搞笑题目
2. **results.json** - 5 种人格结果及描述
3. **dimensions.json** - 15 个维度定义

### 示例文件

- **custom_questions.json** - 自定义题目示例

---

## 🎭 5 种人格类型

| 类型 | 英文 | 特点 |
|------|------|------|
| 死者 | DEAD | 人群中最透明的那个 |
| 草者 | FUCK | 情绪不稳定，随时爆炸 |
| ATM-er | ATM | 人肉提款机，永远在付出 |
| 吗喽 | MALO | 职场食物链底端的吉祥物 |
| 狗屎人 | SHIT | 浑身负能量，但很真实 |

---

## 📊 15 个维度

搞笑命名，覆盖职场、社交、心理等场景：

1. 社恐指数
2. 摆烂力
3. 嘴硬程度
4. 表面正常值
5. 内心戏浓度
6. 工具人倾向
7. 整活频率
8. 情绪稳定性（反向）
9. 自我感觉良好度
10. 拖延症等级
11. 社牛残留量
12. 玻璃心厚度
13. 打工人觉悟
14. 网瘾深度
15. 人间清醒度

---

## 🚀 使用方法

### 方式 1：直接使用数据

```javascript
// 读取题目数据
const questions = require('./data/questions.json');

// 读取结果数据
const results = require('./data/results.json');

// 读取维度数据
const dimensions = require('./data/dimensions.json');
```

### 方式 2：自定义前端实现

根据数据文件创建您自己的前端界面：

1. 设计 UI（极简暗黑 + 赛博朋克风格）
2. 实现答题逻辑
3. 计算维度分数
4. 匹配人格类型
5. 显示结果

---

## 📝 数据格式说明

### questions.json 格式

```json
[
  {
    "id": 1,
    "q": "题目内容",
    "o": [
      {
        "t": "选项文本",
        "s": {
          "维度名": 分值
        }
      }
    ]
  }
]
```

### results.json 格式

```json
{
  "DEAD": {
    "n": "死者",
    "en": "DEAD",
    "slogan": "毒舌标语",
    "desc": ["描述段落1", "描述段落2"]
  }
}
```

### dimensions.json 格式

```json
[
  {
    "id": 1,
    "n": "维度名称",
    "d": "描述",
    "low": "低端标签",
    "high": "高端标签",
    "c": "#颜色代码"
  }
]
```

---

## 💡 实现建议

### 前端技术栈

- **框架**: React / Vue / 原生 JavaScript
- **图表**: Chart.js / ECharts
- **样式**: 自定义 CSS（暗黑赛博朋克风格）
- **存储**: LocalStorage API

### 核心功能

1. 题目展示与进度条
2. 选项点击反馈
3. 分数计算逻辑
4. 雷达图/条形图展示
5. 分享功能

---

## 🎯 适用场景

### 场景 1：个人项目

使用数据文件快速搭建测试网站

### 场景 2：学习练习

学习前端开发、数据处理

### 场景 3：定制开发

基于数据创建独特的测试体验

---

## 📝 完整文档

- `README.md` - 详细使用说明
- `data/questions.json` - 20 道题目数据
- `data/results.json` - 5 种人格结果
- `data/dimensions.json` - 15 个维度定义

---

## 🔒 安全与隐私

- ✅ **纯数据文件** - 无可执行代码
- ✅ **无网络请求** - 不需要网络连接
- ✅ **本地使用** - 数据不上传
- ✅ **无敏感信息** - 不包含密码、密钥

---

## 🎯 核心价值

- 🎭 **搞笑无厘头** - 平等冒犯所有人
- 📊 **完整数据** - 20题 + 5人格 + 15维度
- 🔧 **易于定制** - JSON 格式，易于修改
- ⚡ **开箱即用** - 直接使用数据文件
- 💾 **轻量级** - 仅 8KB

---

**让每个人都被平等冒犯！** 🚀
