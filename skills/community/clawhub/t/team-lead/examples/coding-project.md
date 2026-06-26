# 示例：代码功能开发工作流

## 用户请求

```
给我的项目添加用户登录功能，包含邮箱验证和密码加密
```

## Team Lead 执行流程

### Step 1: 任务分析

**识别结果：**
```json
{
  "taskType": "coding",
  "complexity": "medium",
  "requiredCapabilities": ["代码开发", "安全审计", "测试"],
  "estimatedSubtasks": 4
}
```

---

### Step 2: 任务分解

**分解结果：**
```json
{
  "template": "coding",
  "subtasks": [
    {
      "id": "step-0",
      "type": "plan",
      "label": "需求分析",
      "suggestedAgentType": "planning",
      "dependsOn": [],
      "parallel": false,
      "input": {
        "instruction": "分析登录功能需求，列出技术要点和实现步骤"
      },
      "estimatedTime": 45
    },
    {
      "id": "step-1",
      "type": "implement",
      "label": "代码实现",
      "suggestedAgentType": "coding",
      "dependsOn": ["step-0"],
      "parallel": false,
      "input": {
        "instruction": "实现用户登录功能，包含邮箱验证和密码加密"
      },
      "estimatedTime": 180
    },
    {
      "id": "step-2",
      "type": "review",
      "label": "安全审计",
      "suggestedAgentType": "review",
      "dependsOn": ["step-1"],
      "parallel": true,
      "input": {
        "instruction": "审查代码安全性，识别潜在漏洞"
      },
      "estimatedTime": 60
    },
    {
      "id": "step-3",
      "type": "test",
      "label": "测试用例",
      "suggestedAgentType": "testing",
      "dependsOn": ["step-1"],
      "parallel": true,
      "input": {
        "instruction": "生成全面的测试用例并执行"
      },
      "estimatedTime": 90
    }
  ]
}
```

---

### Step 3: 执行过程

```
[14:00:00] 开始任务 task-1710424800000
[14:00:01] 任务分解完成，4 个子任务
[14:00:02] 开始执行 step-0 (需求分析)
[14:00:47] step-0 完成 (45s)
[14:00:48] 开始执行 step-1 (代码实现)
[14:03:48] step-1 完成 (180s)
[14:03:49] 并行执行：step-2 (安全审计), step-3 (测试)
[14:04:49] step-2 完成 (60s)
[14:05:19] step-3 完成 (90s)
[14:05:20] 质量检查通过 (88/100)
[14:05:21] 结果聚合完成
[14:05:22] 任务完成，总耗时 322s
```

---

### Step 4: 各步骤输出示例

#### step-0: 需求分析

```markdown
## 登录功能需求分析

### 功能需求
1. 用户注册（邮箱 + 密码）
2. 邮箱验证（发送验证邮件）
3. 用户登录（邮箱 + 密码）
4. 密码加密存储（bcrypt）
5. 会话管理（JWT）

### 技术栈
- Node.js + Express
- MongoDB + Mongoose
- bcrypt (密码加密)
- jsonwebtoken (JWT)
- nodemailer (邮件发送)

### 实现步骤
1. 创建 User 模型
2. 实现注册接口
3. 实现邮箱验证
4. 实现登录接口
5. 添加中间件验证
```

#### step-1: 代码实现

```javascript
// models/User.js
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true,
    minlength: 8
  },
  emailVerified: {
    type: Boolean,
    default: false
  },
  verificationToken: String
});

// 密码加密
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// 密码验证
userSchema.methods.comparePassword = async function(candidate) {
  return await bcrypt.compare(candidate, this.password);
};

// 生成 JWT
userSchema.methods.generateToken = function() {
  return jwt.sign({ userId: this._id }, process.env.JWT_SECRET, { expiresIn: '7d' });
};
```

#### step-2: 安全审计

```markdown
## 安全审计报告

### ✅ 安全措施到位
- [x] 密码使用 bcrypt 加密（12 轮）
- [x] JWT 设置合理过期时间
- [x] 邮箱唯一性约束
- [x] 密码长度要求

### ⚠️ 建议改进
1. **速率限制**: 添加登录尝试限制，防止暴力破解
   ```javascript
   // 建议使用 express-rate-limit
   const limiter = rateLimit({
     windowMs: 15 * 60 * 1000,
     max: 5
   });
   ```

2. **密码复杂度**: 增加密码复杂度要求
   ```javascript
   // 建议添加正则验证
   const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
   ```

3. **HTTPS**: 确保生产环境使用 HTTPS

4. **环境变量**: 确保 JWT_SECRET 不在代码中硬编码
```

#### step-3: 测试用例

```javascript
// tests/auth.test.js
describe('Authentication', () => {
  describe('POST /api/auth/register', () => {
    it('应该成功注册新用户', async () => {
      const res = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'test@example.com',
          password: 'Password123'
        });
      
      expect(res.status).toBe(201);
      expect(res.body).toHaveProperty('token');
    });

    it('应该拒绝重复邮箱', async () => {
      // ...
    });

    it('应该拒绝弱密码', async () => {
      // ...
    });
  });

  describe('POST /api/auth/login', () => {
    it('应该成功登录', async () => {
      // ...
    });

    it('应该拒绝错误密码', async () => {
      // ...
    });
  });
});
```

---

### Step 5: 结果聚合

**聚合策略：** `chain`（链式结果）

**最终输出：**
```markdown
# 用户登录功能实现

## 📋 需求分析
[step-0 输出]

## 💻 代码实现
[step-1 输出]

### 文件结构
```
src/
├── models/
│   └── User.js
├── controllers/
│   └── auth.controller.js
├── middleware/
│   └── auth.middleware.js
└── routes/
    └── auth.routes.js
```

### 核心代码
[关键代码片段]

## 🔒 安全审计
[step-2 输出]

### 安全评分：85/100
- 密码加密：✅
- JWT 认证：✅
- 速率限制：⚠️ 建议添加
- 密码复杂度：⚠️ 建议加强

### 待改进项
1. 添加登录速率限制
2. 增强密码复杂度要求
3. 添加双因素认证（可选）

## ✅ 测试用例
[step-3 输出]

### 测试覆盖
- 注册流程：✅
- 登录流程：✅
- 邮箱验证：✅
- 错误处理：✅

### 运行测试
```bash
npm test
# 通过率：100% (12/12)
```

## 🚀 部署检查清单
- [ ] 设置环境变量 JWT_SECRET
- [ ] 配置邮件服务
- [ ] 启用 HTTPS
- [ ] 配置速率限制
- [ ] 设置监控告警
```

---

### Step 6: 质量检查

**质量报告：**
```json
{
  "summary": {
    "total": 4,
    "passed": 4,
    "avgScore": 0.88
  },
  "details": [
    {
      "subtaskId": "step-0",
      "overallScore": 0.92,
      "feedback": ["需求分析全面", "技术选型合理"]
    },
    {
      "subtaskId": "step-1",
      "overallScore": 0.90,
      "feedback": ["代码规范", "遵循最佳实践"]
    },
    {
      "subtaskId": "step-2",
      "overallScore": 0.85,
      "feedback": ["安全审查详细", "建议具体可行"]
    },
    {
      "subtaskId": "step-3",
      "overallScore": 0.85,
      "feedback": ["测试覆盖全面", "用例设计合理"]
    }
  ]
}
```

---

## 关键指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 总耗时 | 322s | 包含完整开发流程 |
| 质量评分 | 88/100 | 良好 |
| Agent 使用数 | 4 | planning, coding, review, testing |
| 代码行数 | ~300 | 完整实现 |
| 测试覆盖 | 100% | 12/12 通过 |
| 安全问题 | 3 个 | 已识别并给出建议 |

---

## 经验教训

### ✅ 做得好的
1. 需求分析清晰，指导后续实现
2. 安全审计及时发现潜在问题
3. 测试覆盖全面

### ⚠️ 可改进的
1. 可以在实现前添加数据库设计审查
2. 可以添加性能测试
3. 可以考虑添加 API 文档生成

---

## 复用建议

同样的工作流可以应用于：
- 其他用户功能开发（注册、找回密码等）
- API 接口开发
- 数据管理功能
- 第三方集成
