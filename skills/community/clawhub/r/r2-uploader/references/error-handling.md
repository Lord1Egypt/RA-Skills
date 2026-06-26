# 错误处理指南

## 目录

- [诊断流程](#诊断流程)
- [错误码对照表](#错误码对照表)
- [重试机制](#重试机制)
- [特殊路径处理](#特殊路径处理)

---

## 诊断流程

上传失败时按顺序排查：

```bash
# 1. 验证登录状态
wrangler whoami
# 未登录则运行: wrangler login

# 2. 验证 bucket 存在
wrangler r2 bucket list | grep "<bucket>"
# 不存在则创建: wrangler r2 bucket create <bucket>

# 3. 验证文件可读
ls -la "<file-path>"
```

---

## 错误码对照表

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `The file does not exist` | 路径错误或空格问题 | `find` 查找正确路径 → 改用临时文件上传 |
| `Authentication required` | 未登录 | `wrangler login` |
| `Bucket not found` | bucket 不存在 | `wrangler r2 bucket create <name>` |
| `Network error` / `Timeout` | 网络问题 | 检查网络 → 启用重试机制 |
| `Permission denied` | 文件权限不足 | `chmod +r "<file>"` |

---

## 重试机制

```bash
# 最多重试 3 次，每次间隔 2 秒
for i in 1 2 3; do
  wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "<file>" --remote && \
    { echo "✓ 上传成功"; break; }
  echo "⚠ 第 $i 次失败，2秒后重试..."
  sleep 2
done
```

---

## 特殊路径处理

含空格或中文的路径可能导致上传失败，使用临时文件绕过：

```bash
TMP_FILE="/tmp/r2-upload-$(date +%s)"
cp "<source-path>" "$TMP_FILE"
wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "$TMP_FILE" --remote
rm "$TMP_FILE"
```
