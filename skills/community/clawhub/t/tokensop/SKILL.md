# TOKEN SOP - 本地工作流缓存技能

**调用全网智能体经验，大幅节省你的 Token 消耗**

---

## 🎯 核心优势

| 优势 | 说明 |
|------|------|
| 💰 节省 Token | 重复任务直接复用，0 消耗 |
| ⚡ 极速响应 | 本地调用，秒级执行 |
| 🌐 全网经验 | 云端工作流共享 |
| 🔒 隐私安全 | 本地存储，不上传敏感数据 |

---

## 工作原理

```
第一次执行 → 消耗 Token → 保存到本地
          ↓
后续执行 → 本地命中 → 0 Token 消耗！
```

---

## 功能特点

1. **本地缓存** - 自动保存成功的工作流到本地
2. **智能匹配** - 优先使用本地缓存，节省 Token
3. **云端备份** - 可贡献到云端，供全网使用
4. **离线可用** - 断网也能正常运行

---

## 配置

| 配置 | 默认值 | 说明 |
|------|--------|------|
| enabled | true | 启用技能 |
| local_store_enabled | true | 启用本地缓存 |
| local_store_dir | ~/.openclaw/workflows | 本地存储目录 |
| auto_contribute | true | 自动贡献到云端 |
| cloud_endpoint | https://api.ainclaw.com | 云端 API |

---

## 安装

```bash
npm install
npm run build
```
