# 测试用例输出格式示例

## 格式 1：Markdown 表格（推荐）

```markdown
| 用例 ID | 用例名称 | 前置条件 | 测试步骤 | 预期结果 | 优先级 |
|---------|----------|----------|----------|----------|--------|
| TC-001 | 邮箱登录成功 | 用户已注册 | 1. 输入有效邮箱<br>2. 输入正确密码<br>3. 点击登录 | 登录成功，跳转首页 | P0 |
| TC-002 | 密码错误 | 用户已注册 | 1. 输入邮箱<br>2. 输入错误密码<br>3. 点击登录 | 提示"密码错误" | P1 |
```

**优点**：易读、支持 Markdown 渲染、适合文档

---

## 格式 2：纯文本列表

```
用例 ID: TC-001
用例名称：邮箱登录成功
前置条件：用户已注册
测试步骤:
  1. 输入有效邮箱
  2. 输入正确密码
  3. 点击登录
预期结果：登录成功，跳转首页
优先级：P0

---

用例 ID: TC-002
用例名称：密码错误
前置条件：用户已注册
测试步骤:
  1. 输入邮箱
  2. 输入错误密码
  3. 点击登录
预期结果：提示"密码错误"
优先级：P1
```

**优点**：简单、无格式依赖、适合复制粘贴

---

## 格式 3：JSON 格式

```json
[
  {
    "id": "TC-001",
    "name": "邮箱登录成功",
    "precondition": "用户已注册",
    "steps": ["输入有效邮箱", "输入正确密码", "点击登录"],
    "expected": "登录成功，跳转首页",
    "priority": "P0"
  },
  {
    "id": "TC-002",
    "name": "密码错误",
    "precondition": "用户已注册",
    "steps": ["输入邮箱", "输入错误密码", "点击登录"],
    "expected": "提示\"密码错误\"",
    "priority": "P1"
  }
]
```

**优点**：机器可读、易于导入测试管理系统

---

## 格式 4：XML 格式

```xml
<testcases>
  <testcase id="TC-001" priority="P0">
    <name>邮箱登录成功</name>
    <precondition>用户已注册</precondition>
    <steps>
      <step>输入有效邮箱</step>
      <step>输入正确密码</step>
      <step>点击登录</step>
    </steps>
    <expected>登录成功，跳转首页</expected>
  </testcase>
  <testcase id="TC-002" priority="P1">
    <name>密码错误</name>
    <precondition>用户已注册</precondition>
    <steps>
      <step>输入邮箱</step>
      <step>输入错误密码</step>
      <step>点击登录</step>
    </steps>
    <expected>提示"密码错误"</expected>
  </testcase>
</testcases>
```

**优点**：结构化、支持 Schema 验证

---

## 格式 5：Gherkin（BDD）

```gherkin
Feature: 用户登录

  Scenario: 邮箱登录成功
    Given 用户已注册账号
    When 用户输入有效邮箱和正确密码
    And 用户点击登录按钮
    Then 登录成功
    And 跳转到首页

  Scenario: 密码错误
    Given 用户已注册账号
    When 用户输入有效邮箱和错误密码
    And 用户点击登录按钮
    Then 显示错误提示"密码错误"
    And 停留在登录页
```

**优点**：业务语言、可执行、适合敏捷团队

---

## 格式 6：CSV 格式

```csv
id,name,precondition,steps,expected,priority
TC-001,邮箱登录成功，用户已注册，"1.输入有效邮箱\n2.输入正确密码\n3.点击登录",登录成功跳转首页，P0
TC-002,密码错误，用户已注册，"1.输入邮箱\n2.输入错误密码\n3.点击登录",提示密码错误，P1
```

**优点**：可导入 Excel、测试管理工具

---

## 格式选择建议

| 场景 | 推荐格式 |
|------|----------|
| 文档/报告 | Markdown 表格 |
| 测试管理系统导入 | JSON/XML/CSV |
| 敏捷团队/BDD | Gherkin |
| 快速分享 | 纯文本列表 |
| 自动化集成 | JSON/XML |
