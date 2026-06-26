# 发布注意事项

## 发布前检查

确认 skill 目录中不包含：

- 私钥 / 公钥文件
- 写死的 KID / Project ID / API Host / 私钥绝对路径
- `local/` 下的所有文件（配置、缓存、CSV 数据）

确认 `local/` 目录不在版本控制中。

## 安装后

详见 `references/setup.md`。配置完成后运行：

```bash
bash ./scripts/init.sh
bash ./scripts/test.sh
```
