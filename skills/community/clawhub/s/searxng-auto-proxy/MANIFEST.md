# SearXNG Auto Proxy v3.0.0 - 发布清单

**发布日期：** 2026-03-21  
**版本：** v3.0.0  
**作者：** pengong101

---

## 📦 文件清单

| 文件 | 大小 | 说明 |
|------|------|------|
| adapter.py | ~20KB | 核心适配器 |
| proxy-rules.yml | ~3KB | 代理规则配置 |
| clawhub.json | ~1KB | ClawHub 配置 |
| README.md | ~2.5KB | 使用说明 |
| RELEASE-v3.0.0.md | ~1.4KB | 发布说明 |
| SKILL.md | ~12KB | 技能文档 |
| LICENSE | ~1KB | MIT 许可 |
| requirements.txt | ~170B | Python 依赖 |
| FINAL-TEST-REPORT-v3.0.md | ~11KB | 测试报告 |
| start-adapter.sh | ~200B | 启动脚本 |

---

## 📊 测试状态

- ✅ 5 轮完整测试通过
- ✅ 搜索成功率 100%
- ✅ 缓存命中率>90%
- ✅ 资源占用<0.5%

---

## 🚀 安装方式

```bash
# 1. 安装依赖
pip3 install aiohttp pyyaml

# 2. 复制配置
cp proxy-rules.yml /root/.openclaw/searxng/

# 3. 启动服务
./start-adapter.sh
```

---

**打包时间：** 2026-03-21
