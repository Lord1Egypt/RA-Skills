---
name: ai-exam
description: AI智能出题考试系统 - 基于文档自动生成考试、指派学员并查询结果
version: 1.0.0
author: AI Assistant
tags: [ai, exam, education, openclaw]
---

# AI智能出题考试系统

基于接口文档实现的AI智能出题、考试指派和结果查询系统。支持上传文档、AI自动出题、指派学员/部门、查询考试结果等完整流程。

## 功能特性

- 🤖 AI智能出题 - 上传文档自动生成试题
- 📝 多种题型支持 - 单选、多选、不定项、判断、填空、简答
- 👥 灵活指派 - 支持按用户名和部门名指派
- 📊 结果查询 - 单个和批量查询学员考试结果
- 🔐 自动认证 - 自动管理 access_token，无需手动刷新
- ⚡ 批量操作 - 支持批量指派和批量查询

## 安装

```bash
npm install
```

## 配置

### 环境变量配置

创建 `.env` 文件：

```bash
APP_KEY=your_app_key
APP_SECRET=your_app_secret
CORP_ID=your_corp_id
```

### 代码配置

```javascript
import aiExamSkill from './index.js';

await aiExamSkill.initialize(
  'your_app_key',
  'your_app_secret',
  'your_corp_id'
);
```

## 使用方法

### 1. 完整流程：创建考试并指派

```javascript
import aiExamSkill from './index.js';

// 初始化配置
await aiExamSkill.initialize(appKey, appSecret, corpId);

// 创建考试并指派
const result = await aiExamSkill.createAndAssignExam({
  // 文档路径
  filePath: '/path/to/document.pdf',

  // 考试标题
  examTitle: '2026年春季期末考试',

  // 题型配置
  questionTypes: [
    { type: 'danxuan', count: 10 },      // 单选题 10道
    { type: 'duoxuan', count: 5 },       // 多选题 5道
    { type: 'budingxiang', count: 2 },   // 不定项 2道
    { type: 'panduan', count: 5 },       // 判断题 5道
    { type: 'tiankong', count: 3 },      // 填空题 3道
    { type: 'jianda', count: 2 }         // 简答题 2道
  ],

  // 创建者信息
  creatorUserId: 'A8BD990B-EDE0-4A52-A33B-83EFA574137C',
  creatorUserName: '张老师',
  creatorDeptUserId: '181739082621441031',
  creatorDeptUserName: '张老师',

  // 指派对象（可选）
  assignUserNames: ['李明', '王芳', '张伟'],
  assignDeptNames: ['一年级', '二年级']
});

console.log('考试创建成功！');
console.log('考试ID:', result.examId);
console.log('题目数量:', result.questionCount);
console.log('总分:', result.totalScore);
console.log('及格分:', result.passScore);
```

### 2. 快速创建（使用默认题型）

```javascript
// 使用默认题型配置：10道单选 + 5道多选 + 5道判断
const result = await aiExamSkill.quickCreateExam(
  '/path/to/document.pdf',
  '快速测试考试',
  {
    creatorUserId: 'user_id',
    creatorUserName: '创建者姓名',
    creatorDeptUserId: 'dept_user_id',
    creatorDeptUserName: '创建者部门姓名'
  }
);
```

### 3. 查询单个学员考试结果

```javascript
const examResult = await aiExamSkill.getExamResult(
  'exam_id',
  '学生姓名'
);

console.log('考试名称:', examResult.target_title);
console.log('得分:', examResult.last_score);
console.log('总分:', examResult.total_score);
console.log('通过状态:', examResult.pass_status);
console.log('考试次数:', examResult.attempt_times);
console.log('平均用时:', examResult.avg_used_time, '秒');
console.log('学分:', examResult.credit);
```

### 4. 批量查询考试结果

```javascript
const results = await aiExamSkill.batchGetExamResults(
  'exam_id',
  ['学生A', '学生B', '学生C', '学生D']
);

// 处理结果
results.forEach(result => {
  if (result.success) {
    console.log(`${result.userName}: ${result.data.last_score}分 - ${result.data.pass_status}`);
  } else {
    console.log(`${result.userName}: 查询失败 - ${result.error}`);
  }
});

// 统计通过率
const passedCount = results.filter(r => r.success && r.data.pass_status === 'passed').length;
console.log(`通过率: ${(passedCount / results.length * 100).toFixed(2)}%`);
```

## API 参考

### 题型类型

| 类型 | 说明 |
|------|------|
| `danxuan` | 单选题 |
| `duoxuan` | 多选题 |
| `budingxiang` | 不定项选择题 |
| `panduan` | 判断题 |
| `tiankong` | 填空题 |
| `jianda` | 简答题 |

### 主要方法

#### `initialize(appKey, appSecret, corpId)`

初始化系统配置

**参数:**
- `appKey` (string) - 应用密钥
- `appSecret` (string) - 应用密钥
- `corpId` (string) - 企业ID

**返回:** Promise<void>

---

#### `createAndAssignExam(options)`

创建考试并指派学员/部门

**参数:**
- `options.filePath` (string) - 文档文件路径
- `options.examTitle` (string) - 考试标题
- `options.questionTypes` (Array) - 题型配置数组
- `options.creatorUserId` (string) - 创建者用户ID
- `options.creatorUserName` (string) - 创建者姓名
- `options.creatorDeptUserId` (string) - 创建者部门用户ID
- `options.creatorDeptUserName` (string) - 创建者部门姓名
- `options.assignUserNames` (Array) - 指派用户名列表（可选）
- `options.assignDeptNames` (Array) - 指派部门名列表（可选）

**返回:** Promise<Object>
```javascript
{
  examId: string,           // 考试ID
  examTitle: string,        // 考试标题
  questionCount: number,    // 题目数量
  totalScore: number,       // 总分
  passScore: number,        // 及格分
  assignedUsers: number,    // 已指派用户数
  assignedDepts: number     // 已指派部门数
}
```

---

#### `quickCreateExam(filePath, examTitle, creator)`

快速创建考试（使用默认题型：10道单选 + 5道多选 + 5道判断）

**参数:**
- `filePath` (string) - 文档文件路径
- `examTitle` (string) - 考试标题
- `creator` (Object) - 创建者信息
  - `creatorUserId` (string)
  - `creatorUserName` (string)
  - `creatorDeptUserId` (string)
  - `creatorDeptUserName` (string)

**返回:** Promise<Object> - 同 `createAndAssignExam`

---

#### `getExamResult(examId, userName)`

获取单个学员的考试结果

**参数:**
- `examId` (string) - 考试ID
- `userName` (string) - 学员姓名

**返回:** Promise<Object>
```javascript
{
  target_id: string,        // 考试ID
  target_title: string,     // 考试名称
  category_title: string,   // 分类名称
  dept_user_id: string,     // 用户ID
  total_score: number,      // 总分
  pass_score: number,       // 及格分
  last_score: number,       // 最后得分
  pass_status: string,      // 通过状态 (passed/failed)
  attempt_times: number,    // 考试次数
  avg_used_time: number,    // 平均用时（秒）
  credit: number,           // 学分
  passed_time: string,      // 通过时间
  create_time: string       // 创建时间
}
```

---

#### `batchGetExamResults(examId, userNames)`

批量获取学员考试结果

**参数:**
- `examId` (string) - 考试ID
- `userNames` (Array<string>) - 学员姓名列表

**返回:** Promise<Array<Object>>
```javascript
[
  {
    userName: string,
    success: boolean,
    data: Object,      // 成功时的考试结果
    error: string      // 失败时的错误信息
  }
]
```

## 使用场景

### 场景1: 教师创建期末考试

```javascript
// 1. 上传教材PDF，AI自动生成试题
// 2. 指派给整个班级
const result = await aiExamSkill.createAndAssignExam({
  filePath: '/documents/math_textbook.pdf',
  examTitle: '数学期末考试',
  questionTypes: [
    { type: 'danxuan', count: 20 },
    { type: 'duoxuan', count: 10 },
    { type: 'jianda', count: 5 }
  ],
  creatorUserId: 'teacher_001',
  creatorUserName: '李老师',
  creatorDeptUserId: 'dept_teacher_001',
  creatorDeptUserName: '李老师',
  assignDeptNames: ['三年级一班', '三年级二班']
});
```

### 场景2: 企业培训考核

```javascript
// 1. 上传培训资料
// 2. 指派给新员工
const result = await aiExamSkill.createAndAssignExam({
  filePath: '/training/company_policy.pdf',
  examTitle: '新员工入职培训考核',
  questionTypes: [
    { type: 'danxuan', count: 15 },
    { type: 'panduan', count: 10 }
  ],
  creatorUserId: 'hr_001',
  creatorUserName: 'HR张经理',
  creatorDeptUserId: 'dept_hr_001',
  creatorDeptUserName: 'HR张经理',
  assignDeptNames: ['2026届新员工']
});
```

### 场景3: 批量查询考试结果并生成报告

```javascript
// 查询所有学员成绩
const students = ['张三', '李四', '王五', '赵六', '钱七'];
const results = await aiExamSkill.batchGetExamResults(examId, students);

// 生成统计报告
const passed = results.filter(r => r.success && r.data.pass_status === 'passed');
const failed = results.filter(r => r.success && r.data.pass_status !== 'passed');
const avgScore = results
  .filter(r => r.success)
  .reduce((sum, r) => sum + r.data.last_score, 0) / results.length;

console.log('考试统计报告:');
console.log(`总人数: ${results.length}`);
console.log(`通过人数: ${passed.length}`);
console.log(`未通过人数: ${failed.length}`);
console.log(`通过率: ${(passed.length / results.length * 100).toFixed(2)}%`);
console.log(`平均分: ${avgScore.toFixed(2)}`);
```

## 错误处理

所有方法都会抛出错误，建议使用 try-catch 捕获：

```javascript
try {
  const result = await aiExamSkill.createAndAssignExam(options);
  console.log('操作成功:', result);
} catch (error) {
  console.error('操作失败:', error.message);

  // 根据错误类型进行处理
  if (error.message.includes('access_token')) {
    console.error('认证失败，请检查配置');
  } else if (error.message.includes('文件不存在')) {
    console.error('文件路径错误');
  } else {
    console.error('未知错误');
  }
}
```

## 注意事项

1. **Token管理**: access_token 有效期为2小时，系统会自动管理和刷新，无需手动处理
2. **文件格式**: 支持 PDF、Word、Excel 等常见文档格式
3. **题型配置**: 题型数量可以根据需要自由配置，建议总题数在 15-50 道之间
4. **指派逻辑**:
   - 系统会自动查询用户名和部门名对应的ID
   - 未找到的用户或部门会跳过，不影响其他指派
   - 可以只指派用户、只指派部门，或两者都指派
5. **并发限制**: 批量操作时建议控制并发数量，避免API限流

## 项目结构

```
ai_exam/
├── config.js          # 配置管理（token缓存、默认配置）
├── api-client.js      # API客户端（统一请求处理）
├── services.js        # 部门和用户服务
├── exam-service.js    # 考试核心服务
├── index.js           # 主入口（Skill类）
├── example.js         # 使用示例
├── package.json       # 项目配置
├── README.md          # 说明文档
├── skill.md           # Skill文档
├── .env.example       # 环境变量示例
└── .gitignore         # Git忽略配置
```

## 依赖项

- `axios` - HTTP客户端
- `form-data` - 文件上传支持

## 版本历史

### v1.0.0 (2026-03-15)
- ✨ 初始版本发布
- ✅ 支持AI智能出题
- ✅ 支持考试指派
- ✅ 支持结果查询
- ✅ 自动Token管理

## 许可证

MIT

## 支持

如有问题或建议，请提交 Issue 或 Pull Request。
