# 🎭 SBTI 恶搞人格测试数据包

> 极简暗黑风格的 MBTI 恶搞测试数据包，搞笑无厘头，平等冒犯所有人

---

## ✨ 特性

- 🎭 **5 种搞笑人格** - DEAD, FUCK, ATM, MALO, SHIT
- 📊 **15 个维度** - 社恐指数、摆烂力、嘴硬程度...
- 🎯 **20 道题目** - 搞笑无厘头风格
- 📦 **纯数据文件** - JSON 格式，易于使用
- 🔧 **高度可定制** - 支持自定义前端实现

---

## 📦 文件结构

```
sbti-personality-test/
├── SKILL.md                    # 技能主文档
├── README.md                   # 使用说明（本文件）
├── LICENSE                     # MIT 许可证
├── data/
│   ├── questions.json         # 20 道题目
│   ├── results.json           # 5 种人格结果
│   └── dimensions.json        # 15 个维度定义
└── examples/
    └── custom_questions.json  # 自定义题目示例
```

---

## 🚀 快速开始

### 1. 使用数据文件

```javascript
// 在 Node.js 中
const questions = require('./data/questions.json');
const results = require('./data/results.json');
const dimensions = require('./data/dimensions.json');

// 在浏览器中
fetch('./data/questions.json')
  .then(res => res.json())
  .then(questions => console.log(questions));
```

### 2. 创建前端界面

根据数据文件设计您自己的测试界面：

- 极简暗黑风格
- 赛博朋克元素
- 响应式设计
- 流畅动效

---

## 🎭 5 种人格类型

### 1. 死者 (DEAD)

- **特点**: 人群中最透明的那个
- **Slogan**: 恭喜你，你是人群中最透明的那个。

### 2. 草者 (FUCK)

- **特点**: 情绪不稳定，随时爆炸
- **Slogan**: 你的情绪就像过山车，但只有你在车上。

### 3. ATM-er (ATM)

- **特点**: 人肉提款机，永远在付出
- **Slogan**: 你的存在意义就是让别人占便宜。

### 4. 吗喽 (MALO)

- **特点**: 职场食物链底端的吉祥物
- **Slogan**: 你是职场食物链底端的吉祥物。

### 5. 狗屎人 (SHIT)

- **特点**: 浑身负能量，但很真实
- **Slogan**: 你是行走的负能量发射器。

---

## 📊 15 个维度

| 维度 | 说明 | 极端表现 |
|------|------|---------|
| 社恐指数 | 害怕社交的程度 | 低=社牛，高=社恐 |
| 摆烂力 | 躺平放弃的程度 | 低=上进，高=摆烂 |
| 嘴硬程度 | 死不认错的程度 | 低=真诚，高=嘴硬 |
| 表面正常值 | 看起来正常的程度 | 低=怪异，高=伪装 |
| 内心戏浓度 | 内心戏的丰富程度 | 低=直率，高=戏精 |
| 工具人倾向 | 被人利用的程度 | 低=自主，高=工具人 |
| 整活频率 | 整活的频率 | 低=正常，高=整活怪 |
| 情绪稳定性（反向） | 情绪波动程度 | 低=稳定，高=不稳定 |
| 自我感觉良好度 | 自信程度 | 低=自卑，高=自恋 |
| 拖延症等级 | 拖延的严重程度 | 低=高效，高=拖延 |
| 社牛残留量 | 社交能力 | 低=社恐，高=社牛 |
| 玻璃心厚度 | 抗打击能力 | 低=坚强，高=玻璃心 |
| 打工人觉悟 | 工作态度 | 低=摸鱼，高=拼命 |
| 网瘾深度 | 网络依赖程度 | 低=现充，高=网瘾 |
| 人间清醒度 | 理性程度 | 低=糊涂，高=清醒 |

---

## 🎨 自定义题目

### 创建自定义题目

```json
[
  {
    "id": 1,
    "q": "你的题目内容",
    "o": [
      {
        "t": "选项 A",
        "s": {
          "社恐指数": 3,
          "摆烂力": 2
        }
      },
      {
        "t": "选项 B",
        "s": {
          "社恐指数": 1,
          "表面正常值": 3
        }
      }
    ]
  }
]
```

### 字段说明

- `id`: 题目唯一标识
- `q`: 题目内容（question）
- `o`: 选项数组（options）
  - `t`: 选项文本（text）
  - `s`: 维度分数映射（scores）

---

## 💡 实现建议

### 前端技术栈

- **框架**: React / Vue / 原生 JavaScript
- **图表**: Chart.js / ECharts（雷达图、条形图）
- **样式**: CSS（暗黑赛博朋克风格）
- **存储**: LocalStorage API（保存进度）

### 核心功能

1. ✅ 题目展示与进度条
2. ✅ 选项点击反馈（动画）
3. ✅ 分数计算逻辑
4. ✅ 雷达图/条形图展示
5. ✅ 分享功能（复制链接/生成图片）

### 设计风格

- **配色**: 黑色背景 + 荧光绿/紫/蓝
- **字体**: 现代无衬线粗体
- **动效**: 发光、滑入、缩放
- **布局**: 居中、卡片式

---

## 🛠️ 技术栈示例

### React 实现

```jsx
import questions from './data/questions.json';
import results from './data/results.json';

function Quiz() {
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  
  // 实现答题逻辑
}
```

### Vue 实现

```vue
<script setup>
import { ref } from 'vue';
import questions from './data/questions.json';

const current = ref(0);
const answers = ref({});
</script>
```

---

## 📱 移动端适配

### 响应式断点

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### 触摸交互

- 选项点击区域 ≥ 44px
- 支持左右滑动切换题目
- 进度条自适应宽度

---

## 🎯 验收标准

- [ ] 正确读取并解析所有数据文件
- [ ] 实现 20 道题目的答题流程
- [ ] 正确计算 15 个维度的分数
- [ ] 正确匹配 5 种人格类型
- [ ] 显示人格称号、标语、描述
- [ ] 实现雷达图或条形图展示
- [ ] 移动端布局正常
- [ ] 答题进度本地存储

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🤝 贡献

欢迎贡献！可以：

1. 添加新的搞笑题目
2. 创建新的人格类型
3. 改进维度设计
4. 分享前端实现案例

---

## 📞 使用示例

### 示例 1：纯数据使用

```bash
# 解压数据文件
tar -xzf sbti-personality-test.tar.gz

# 使用数据文件
cd sbti-personality-test/data
# questions.json - 题目数据
# results.json - 结果数据
# dimensions.json - 维度数据
```

### 示例 2：前端集成

```html
<!DOCTYPE html>
<html>
<head>
  <title>SBTI 测试</title>
</head>
<body>
  <div id="app"></div>
  <script>
    // 加载数据
    fetch('./data/questions.json')
      .then(res => res.json())
      .then(questions => {
        // 实现答题逻辑
      });
  </script>
</body>
</html>
```

---

**让每个人都被平等冒犯！** 🚀
