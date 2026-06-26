# 高级用法

## 目录

- [批量上传](#批量上传)
- [并发上传](#并发上传)

---

## 批量上传

### 上传当前目录所有图片

```bash
for file in *.jpg *.png *.gif *.webp; do
  [ -f "$file" ] || continue
  wrangler r2 object put "$R2_BUCKET/agent/$(date +%Y%m%d)/$file" --file "$file" --remote && \
    echo "✓ $file"
done
```

### 上传指定目录所有文件

```bash
DIR="/path/to/dir"
for file in "$DIR"/*; do
  [ -f "$file" ] || continue
  wrangler r2 object put "$R2_BUCKET/agent/$(date +%Y%m%d)/$(basename "$file")" --file "$file" --remote && \
    echo "✓ $(basename "$file")"
done
```

---

## 并发上传

使用 `xargs` 并发上传（4 个进程）：

```bash
find . -name "*.jpg" -print0 | xargs -0 -P 4 -I FILE \
  sh -c 'wrangler r2 object put "$R2_BUCKET/agent/$(date +%Y%m%d)/$(basename FILE)" --file FILE --remote'
```

参数说明：
- `-P 4`: 同时运行 4 个进程
- `-print0` / `-0`: 正确处理含空格的文件名
- `sh -c`: 避免 `{}` 在复杂命令中的展开问题
