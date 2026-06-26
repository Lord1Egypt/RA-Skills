# Windows终端下查找Markdown文件内容技巧汇总

以下整理一些在Windows终端（如 PowerShell、CMD 或 Windows Terminal）下，针对 Markdown 文件内容查找的常用方法和技巧：

## 1. 使用 findstr 查找内容

`findstr` 是 Windows 下常用的命令行查找工具，支持正则表达式。

### 查找包含关键词的行

```bash
grep -n "关键词" *.md
```

### 支持递归查找

```bash
grep -R -n "关键词" --include="*.md" .
```
- `/S`：递归子目录查找

### 查找多个关键词（包含任一）

```bash
grep -R -n -i -E "关键字1|关键字2" --include="*.md" .
```
- `/I`：忽略大小写

### 查找不包含某关键词的行

```bash
grep -n -v "不包含的词" *.md
```
- `/V`：查找不包含指定内容的行

### 使用正则表达式查找（部分支持）

```bash
grep -n -E "^# " *.md
```
- `/R`：使用正则表达式
- `/C:"表达式"`：指定搜索字符串或表达式

## 2. 利用 PowerShell 强大字符串处理能力

### 获取包含关键词的行及文件名

```bash
grep -R "关键词" --include="*.md"
```

### 查找包含多关键词的行

```bash
grep -R -E "关键字1|关键字2" --include="*.md"
```

### 查找并统计匹配数量

```bash
grep -R "关键词" --include="*.md" | wc -l
```

### 只显示文件名

```bash
grep -R -l "关键词" --include="*.md"
```

## 3. 模糊/复杂模式查找建议

- 使用正则表达式时，建议采用 PowerShell 的 `Select-String`。
- 例如查找代码块开头：

```bash
grep -R "^```" --include="*.md"
```

- 查找所有标题（以 # 开头）：

```bash
grep -R "^#" --include="*.md"
```

## 4. 其他技巧

- 查看与标记相关内容（如 TODO、FIXME）：

```bash
grep -R -n -i "TODO|FIXME" --include="*.md"
```

- 结合管道进行更复杂的过滤处理：

```bash
grep -R "关键词" --include="*.md" | grep -v "排除词"
```

## 5. 扩展工具推荐

- **grep for Windows**：可安装 [GnuWin32 grep](http://gnuwin32.sourceforge.net/packages/grep.htm) 或 [Git Bash (含grep)](https://gitforwindows.org/) 获得和 Linux 一样的强大 grep 查找能力。

  示例：

  ```bash
  grep -rn "关键词" *.md
  ```


