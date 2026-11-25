# macOS LibreOffice 前置检查

本 skill 不安装任何软件，也不修改系统或 shell 配置。LibreOffice 是外部前置依赖，请由操作员按组织策略准备。

## 检查是否可用

```bash
which soffice
"/Applications/LibreOffice.app/Contents/MacOS/soffice" --version
```

## 如果 `soffice` 不在 PATH

不要修改 `/usr/local/bin`、`~/.zshrc`、`~/.zshenv` 等系统或 shell 配置。
可以在 skill 根目录的可选 `local-env.json` 中指定绝对路径，`parse.py` 会读取：

```json
{
  "renderer": "libreoffice",
  "sofficePath": "/Users/<用户名>/Applications/LibreOffice.app/Contents/MacOS/soffice",
  "notes": "由操作员预先安装 LibreOffice"
}
```

`sofficePath` 不存在时，脚本回落到 `PATH` 中的 `soffice`/`libreoffice`。
若仍不可用，请由操作员安装 LibreOffice，或先把 PPT 导出为 PDF。
