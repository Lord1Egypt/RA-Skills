# 病毒扫描说明

## 检测到的模式

部分杀软检测到代码中包含某些模式。

## 实际情况

### governance.py

包含危险关键词列表，用于内容安全检测：

```python
DANGER_KEYWORDS = [
    'rm -rf', 'delete all', 'drop table',
    'sudo', 'chmod 777',
    'eval', 'exec', 'os.system',
]
```

这些是检测特征库，用于扫描而非执行。

### install_modules.py

安装前扫描脚本是否包含危险模式：

```python
dangerous_patterns = [
    'eval', 'exec', 'compile',
    'subprocess', 'os.system',
    'pickle.load', 'marshal.load',
]
```

这是安全检测功能，在安装前验证脚本安全性。

## 原理说明

杀软的静态分析基于字符串匹配，无法区分：
- 危险代码执行（如 `eval(user_input)`）
- 检测用的字符串列表（如 `pattern = 'eval('`）

这些代码是安全扫描功能，不是危险代码。

## 安全说明

1. 代码不会执行危险操作
2. 安装前会扫描脚本安全性
3. 所有代码本地执行

---

*最后更新：2026-04-12*
