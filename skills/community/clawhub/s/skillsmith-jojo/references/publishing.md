# 发布到 ClawHub 指南

## 一、发布前准备

### 必须完成的检查

| 步骤 | 通过标准 |
|------|---------|
| 测试验证 | skill-test.py 全部通过 |
| 安全检查 | security-check.py 无高危问题 |
| 性能分析 | token-analyzer.py 评级 A 或 B |

## 二、版本号规范

| 变更类型 | 版本升级 | 示例 |
|---------|---------|------|
| 重大功能 | Major (x.0.0) | 1.0.0 → 2.0.0 |
| 新功能 | Minor (0.x.0) | 1.0.0 → 1.1.0 |
| Bug 修复 | Patch (0.0.x) | 1.0.0 → 1.0.1 |

## 三、发布命令

```bash
# 1. 安装 CLI
npm i -g clawhub

# 2. 登录（需授权）
clawhub login

# 3. 发布
clawhub publish ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 1.0.0 \
  --changelog "初始发布"
```

## 四、署名规范

```
作者: JOJO's Workshop
联系: [授权后填写]
```

---

*JOJO's Workshop · 完美主义标准*
