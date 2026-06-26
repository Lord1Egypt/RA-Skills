# Signal-Track 检查清单

- [ ] 扫描项目文件夹，确认不存在明文敏感信息：
  - `apikey` / `api key`
  - `token` / `Authorization`
  - `user_id` / `userId`
  - `pid`
  - IP 地址（IPv4 / IPv6）
  - 绝对目录路径（如 `/Users/...`, `C:\...`）
  - 若发现命中，需记录文件路径和行号，并立即处理或脱敏。
