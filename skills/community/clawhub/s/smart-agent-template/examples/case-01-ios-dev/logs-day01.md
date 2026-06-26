# 2026-03-01 - Day 1

## 10:30 - Block 内存泄漏
- **纠正**：忘记加 weakSelf
- **教训**：block 里访问 self 必须用 weakSelf
- **下次**：自动检查所有 block

## 14:20 - ViewController 命名
- **纠正**：LoginVC 应该叫 LoginViewController
- **教训**：ViewController 必须写全称，不能缩写
- **下次**：检查所有 VC 命名

## 16:45 - 注释缺失
- **纠正**：公开方法没写注释
- **教训**：所有公开方法必须写注释
- **下次**：自动检查注释完整性
