# 授客AI智能出题考试系统Skill

基于接口文档实现的AI智能出题、考试指派和结果查询系统。

## 功能特性

- ✅ 自动获取和管理 access_token
- ✅ 上传文档到AI系统
- ✅ AI智能出题（支持多种题型）
- ✅ 考试指派（支持用户和部门）
- ✅ 查询考试结果
- ✅ 批量操作支持

## 安装

```bash
npm install
```

## 配置

### 方式1: 环境变量

```bash
export APP_KEY="your_app_key"
export APP_SECRET="your_app_secret"
export CORP_ID="your_corp_id"
```

### 方式2: 代码初始化

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

// 初始化
await aiExamSkill.initialize(appKey, appSecret, corpId);

// 创建考试并指派
const result = await aiExamSkill.createAndAssignExam({
  filePath: '/path/to/document.pdf',
  examTitle: '期末考试',
  questionTypes: [
    { type: 'danxuan', count: 10 },      // 单选题
    { type: 'duoxuan', count: 5 },       // 多选题
    { type: 'budingxiang', count: 2 },   // 不定项
    { type: 'panduan', count: 5 },       // 判断题
    { type: 'tiankong', count: 3 },      // 填空题
    { type: 'jianda', count: 2 }         // 简答题
  ],
  creatorUserId: 'user_id',
  creatorUserName: '张老师',
  creatorDeptUserId: 'dept_user_id',
  creatorDeptUserName: '张老师',
  assignUserNames: ['学生A', '学生B'],
  assignDeptNames: ['一年级', '二年级']
});

console.log('考试ID:', result.examId);
```

### 2. 快速创建（使用默认题型）

```javascript
const result = await aiExamSkill.quickCreateExam(
  '/path/to/document.pdf',
  '快速测试',
  {
    creatorUserId: 'user_id',
    creatorUserName: '创建者',
    creatorDeptUserId: 'dept_user_id',
    creatorDeptUserName: '创建者'
  }
);
```

### 3. 查询单个学员考试结果

```javascript
const examResult = await aiExamSkill.getExamResult(
  'exam_id',
  '学生姓名'
);

console.log('得分:', examResult.last_score);
console.log('通过状态:', examResult.pass_status);
```

### 4. 批量查询考试结果

```javascript
const results = await aiExamSkill.batchGetExamResults(
  'exam_id',
  ['学生A', '学生B', '学生C']
);

results.forEach(result => {
  if (result.success) {
    console.log(`${result.userName}: ${result.data.last_score}分`);
  } else {
    console.log(`${result.userName}: 查询失败`);
  }
});
```

## API 说明

### 题型类型

- `danxuan` - 单选题
- `duoxuan` - 多选题
- `budingxiang` - 不定项选择题
- `panduan` - 判断题
- `tiankong` - 填空题
- `jianda` - 简答题

### 主要方法

#### `initialize(appKey, appSecret, corpId)`
初始化配置

#### `createAndAssignExam(options)`
创建考试并指派

参数:
- `filePath` - 文档路径
- `examTitle` - 考试标题
- `questionTypes` - 题型配置数组
- `creatorUserId` - 创建者用户ID
- `creatorUserName` - 创建者姓名
- `creatorDeptUserId` - 创建者部门用户ID
- `creatorDeptUserName` - 创建者部门姓名
- `assignUserNames` - 指派用户名列表（可选）
- `assignDeptNames` - 指派部门名列表（可选）

#### `quickCreateExam(filePath, examTitle, creator)`
快速创建考试（使用默认题型）

#### `getExamResult(examId, userName)`
获取学员考试结果

#### `batchGetExamResults(examId, userNames)`
批量获取考试结果

## 项目结构

```
ai_exam/
├── package.json          # 项目配置
├── config.js            # 配置管理
├── api-client.js        # API客户端
├── services.js          # 部门和用户服务
├── exam-service.js      # 考试服务
├── index.js             # 主入口
├── example.js           # 使用示例
└── README.md            # 说明文档
```

## 注意事项

1. access_token 有效期为2小时，系统会自动管理和刷新
2. 文件上传支持 PDF、Word、Excel 等文档格式
3. 题型数量可以根据需要自由配置
4. 指派时会自动查询用户和部门ID，未找到的会跳过

## 错误处理

所有方法都会抛出错误，建议使用 try-catch 捕获：

```javascript
try {
  const result = await aiExamSkill.createAndAssignExam(options);
} catch (error) {
  console.error('操作失败:', error.message);
}
```

## License

MIT
