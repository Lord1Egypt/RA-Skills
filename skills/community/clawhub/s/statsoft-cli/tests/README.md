# SPSS 无闪屏调用测试 / SPSS Splash-free Call Test

## 测试目的 / Test Purpose

验证 SPSS 无闪屏调用方式是否正常工作。

Verify that the SPSS splash-free call method works correctly.

## 测试方法 / Test Method

### 首选方式（完全无闪屏）/ Preferred Method (Completely Splash-free)

使用 SPSS 内置 Python 的 `spss` 模块直接运行语法，不调用 `stats.exe`，完全无 GUI。

Use SPSS built-in Python's `spss` module to run syntax directly, without calling `stats.exe`, completely GUI-free.

```bash
# 通过 spss_helper.py 运行
"[SPSS_PYTHON_PATH]" "[SKILL_DIR]/windows-only/SPSS/spss_helper.py" run-internal "[SPS_FILE]"

# 示例
"C:\Program Files\IBM\SPSS\Statistics\26\Python3\python.exe" \
  "[SKILL_DIR]/windows-only/SPSS/spss_helper.py" \
  run-internal \
  "[SKILL_DIR]/tests/test-syntax.sps"
```

### 备用方式（无闪屏）/ Backup Method (No Splash)

通过 `stats.com`（控制台版）调用 .spj 文件，完全无闪屏：

```bash
# 示例
"C:\Program Files\IBM\SPSS\Statistics\26\stats.com" -production silent -nologo "[SKILL_DIR]/tests/test-job.spj"
```

`stats.com` 控制台版纯后台运行，绝无闪屏。

最后备选（可能有闪屏）： `stats.exe -production silent -nologo`。

Call .spj file via `stats.exe -production`. This method may display splash screen.

```bash
# 通过 spss_helper.py 运行
"[STATS_EXE_PATH]" -production "[SPJ_FILE]" silent -nologo

# 示例
"C:\Program Files\IBM\SPSS\Statistics\26\stats.exe" \
  -production \
  "[SKILL_DIR]/tests/test-job.spj"
```

## 测试文件 / Test Files

- `test-syntax.sps` — SPSS 语法文件，生成测试数据并保存
- `test-job.spj` — SPSS 生产作业文件（备用方式使用）

## 预期结果 / Expected Results

1. **无闪屏** — 运行时不显示 SPSS GUI 窗口
2. **输出文件生成** — 生成 `test-data.sav` 文件
3. **数据正确** — `test-data.sav` 包含 5 条记录，id 和 score 两列

## 验证方法 / Verification Method

```bash
# 检查输出文件是否生成
ls -la "[SKILL_DIR]/test-data.sav"

# 读取 .sav 文件内容（需要 pyreadstat）
python -c "
import pyreadstat
df, meta = pyreadstat.read_sav('[SKILL_DIR]/test-data.sav')
print(df)
"
```

## 注意事项 / Notes

1. SPSS 26 内置 Python 3.4，不支持 f-string，所有字符串格式化必须用 `%s` 或 `.format()`
2. 确保输出路径有写权限
3. 如果测试失败，检查 SPSS 安装路径是否正确
