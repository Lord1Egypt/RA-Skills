# 案例 1：iOS 开发助手（30 天演化）

## 背景

一个 iOS 开发者使用 Claude Code，希望 Agent 能记住他的编码习惯和项目规范。

## 第 1 天

### 用户纠正
```
用户：这个 block 里忘记加 weakSelf 了
Agent：好的，已修复
```

### Agent 学习
写入 `logs/2026/03/01.md`：
```markdown
## 10:30 - Block 内存泄漏
- 纠正：忘记加 weakSelf
- 教训：block 里访问 self 必须用 weakSelf
- 下次：自动检查所有 block
```

写入 `memory/hot.md`：
```markdown
## 常见错误
- Block 内存泄漏：访问 self 必须用 weakSelf
```

---

## 第 7 天

### 累积规则（hot.md 已有 15 条）
```markdown
## 代码规范
- Block 内存泄漏：访问 self 必须用 weakSelf
- 命名规范：ViewController 后缀，Manager 后缀
- 注释规范：公开方法必须写注释

## 用户偏好
- 喜欢用 MVC+BLL 架构
- 不喜欢用 Storyboard，纯代码布局
```

### 效果
Agent 开始主动应用规则，用户纠正次数减少 30%

---

## 第 30 天

### hot.md（稳定在 85 行）
```markdown
## 代码规范
- 命名：ViewController/Manager/Service 后缀
- Block：必须 weakSelf，strongSelf 判空
- 注释：公开方法 + 复杂逻辑必须注释
- 布局：纯代码，不用 Storyboard

## 项目规范（Tiqmo）
- 网络层：统一用 TQNetworkManager
- 数据库：用 FMDB，不用 CoreData
- 图片加载：用 SDWebImage
```

### 效果
- 用户纠正次数减少 65%
- Token 消耗减少 60%（不需要反复说明规范）
- Agent 能主动发现问题并修复
