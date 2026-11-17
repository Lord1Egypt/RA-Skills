# 前端静态应用边界判定

以**最终构建产物和部署时运行要求**判断，不用框架名称、目录名或“是否调用 API”作单独结论。

## 可接受

- 本地构建产生可直接由 CDN/Nginx 提供的 `index.html` 与静态资源。
- React、Vue、Svelte、Solid、Astro 或 Angular 的静态产物。
- 浏览器直接访问公开 HTTPS 的 API、CDN、BaaS 或图床，例如天气/地图 API、Supabase、Firebase。
- `server/`、`api/`、`services/` 之类目录仅作为审计线索；只有构建脚本、启动脚本或实际代码证明它是上线必需服务端，才应拒绝。

## 必须拒绝

- 必须运行自建服务端（Express、FastAPI、Django、Nest 等）、SSR/BFF/Server Actions，或服务端数据库/队列/迁移。
- 项目自身承载的 WebSocket/SSE、cron、worker、后台任务。
- 部署时需要 PM2、Docker、systemd、服务器环境变量、远端安装依赖或运行 ZIP 内脚本。
- 浏览器产物包含 API key、私钥、Cookie 或其他秘密，或要求部署端充当密钥代理。

## 最小判定顺序

1. 先确认私有上传与部署端点门禁。
2. 本地运行项目声明的构建命令。
3. 确认最终发布目录含 `index.html`，并只包含静态资源。
4. 审计是否存在上线必需的服务端运行时和秘密泄露。
5. 仅在上述条件全部成立时制作并提交静态 ZIP。
