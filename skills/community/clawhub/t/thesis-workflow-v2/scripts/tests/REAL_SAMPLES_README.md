# 真实样本测试使用说明 (REAL_SAMPLES_README)

## ⚠️ 隐私保护

开题报告样本**含学生姓名 / 学号 / 研究方向 / 论文题目**，属于**敏感个人信息**。

**绝对禁止**：
- ❌ 上传任何 docx 开题报告到 GitHub 仓库
- ❌ 在代码中硬编码样本路径或文件名（含学生姓名）
- ❌ 在 CI/CD 公开 runner 上跑真实样本测试

## 🚀 怎么跑真实样本测试

`test_full_workflow.py` Part 2 在**默认情况下跳过**真实样本测试（避免误跑）。

如需本地验证：

### 步骤 1：准备样本目录

把 docx 文件放到**本地**任意目录（不要放在 `mba-thesis-workflow` 仓库目录内）：

```bash
mkdir -p ~/private/mba-proposals
cp /path/to/your/*.docx ~/private/mba-proposals/
```

### 步骤 2：设置环境变量

```bash
export MBA_REAL_SAMPLES_DIR=~/private/mba-proposals
```

### 步骤 3：跑测试

```bash
cd /path/to/mba-thesis-workflow
python3 scripts/tests/test_full_workflow.py
```

输出示例：

```
=== 真实 docx 样本批量测试 ===
   样本目录: /Users/xxx/private/mba-proposals
   待测试样本: 8 个（匿名展示）

   [测试] sample_001 (171 KB)...
      ✅ 全流程通过
         Phase 1.1: 62 真实 + 7 虚拟节点 (0.04s)
         Phase 1.3: 0 hints 写入 (0.07s)
         ch1 摘要: 18 字 (0.0s)
   ...
```

## 🔒 隐私保证

代码层面：

| 保护措施 | 实现 |
|---------|------|
| 不硬编码路径 | `MBA_REAL_SAMPLES_DIR` 环境变量，按需设置 |
| 不硬编码文件名 | 自动发现目录下所有 `*.docx` |
| paper_name 匿名 | `v2_real_sample_001` / `v2_real_sample_002` ... |
| 输出匿名 | 仅显示 `sample_NNN` 索引 + 文件大小 |
| 跳过文档元数据 | 不读取 docx 的作者、标题等元数据字段 |

## 🧹 清理

测试过程中会创建 `v2_real_sample_NNN` 状态的临时文件：

```bash
# 列出所有测试遗留
ls ~/.openclaw/workspace/v2_real_*

# 清理（谨慎操作，会删除本地 state）
rm -rf ~/.openclaw/workspace/v2_real_*
```

## 💡 建议

- 真实样本测试**仅在本地开发时跑**，CI/CD runner 不要设这个环境变量
- 提交 PR 时不要附带任何 docx 文件
- 如果你想把样本提供给项目维护者，**单独发邮件 / 加密压缩包**，不要通过 GitHub Issues
