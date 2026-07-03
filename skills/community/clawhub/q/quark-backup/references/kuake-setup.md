# kuake CLI 配置文件参考

## 安装说明

kuake CLI 二进制文件应放在 `tools/kuake/bin/kuake`，包装脚本为 `tools/kuake/use-kuake.sh`。

如需重新下载 kuake CLI：
```bash
# 从 GitHub releases 或官方源获取
```

## Cookie 配置

在 `/home/openclaw/.config/openclaw-quark-backup.env` 中配置：

```bash
KUAKE_COOKIE='完整Cookie串'
```

获取方法：
1. 登录 https://pan.quark.cn
2. 打开浏览器开发者工具（F12）
3. 复制请求头中的 `Cookie` 字段
4. 填入上述文件

## 常用命令

```bash
# 查看用户信息
kuake user

# 列出目录
kuake list "/openclaw"

# 上传文件
kuake upload "本地文件" "/远程路径"

# 创建目录
kuake create "目录名" "/父目录"

# 查看文件信息
kuake info "/文件路径"
```

## 注意事项

- Cookie 会过期，过期后需要重新登录获取
- 敏感信息不要放在备份包里
- 建议定期检查备份是否成功上传