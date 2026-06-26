---
name: "trailsnap-cli"
description: "TrailSnap CLI 命令行工具，用于查询照片、相册、标签、位置和人物等信息。当用户需要查看照片、相册数据时调用此技能。"
---

# TrailSnap CLI 技能

此技能允许使用 `trailsnap-cli` Python 脚本与 TrailSnap 后端 API 进行交互。

## 功能
1. 根据指定条件（可选过滤参数）查询照片列表。
2. 查询分类标签、相册、位置和人物（面部）信息。
3. 查询挂载的存储文件夹（目录）列表。

## 初始配置
首次使用该工具前，需要配置 API 地址和 Token：
```bash
python {baseDir}/cli.py config set --url <API_BASE_URL> --token <YOUR_API_TOKEN>
```
配置信息将被保存到同目录下的 `.env` 文件中。

## 使用方法

使用前可以通过 `python {baseDir}/cli.py <command> -h` 或 `python {baseDir}/cli.py <command> <subcommand> -h` 查看每个命令的详细帮助信息。通常情况下，你需要先根据用户的问题逐步筛选出检索条件，然后查询符合条件的照片列表。如果需要访问照片的媒体文件（如 base64 编码或直接下载文件），你可以使用 `medias` 命令。

**你只能通过cli.py脚本运行，不能直接调用API。更不能直接读取.env文件中的配置信息。**

使用 Python 运行脚本：

```bash
python {baseDir}/cli.py <command> <subcommand> [options]
```

详细的命令参考请参考 [reference.md](reference.md) 文件。

### 示例

请参考 [examples/simple.md](examples/simple.md) 文件。



