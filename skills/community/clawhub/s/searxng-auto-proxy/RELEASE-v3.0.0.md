# SearXNG Auto Proxy v3.0.0 Release

**发布日期：** 2026-03-21  
**作者：** pengong101  
**许可：** MIT

---

## 🎉 重大更新

### v3.0.0 - 三层架构完整实现

**核心变更：**
1. ✅ 完整三层架构（规则 + 动态 + 优化）
2. ✅ 13 个引擎代理规则配置
3. ✅ 动态探测（30 秒间隔）
4. ✅ 自动优化（30 分钟测速）
5. ✅ 三级缓存系统
6. ✅ Clash API 集成
7. ✅ 后台常驻服务

**性能提升：**
- 搜索成功率：100%
- 缓存命中率：>90%
- 资源占用：CPU 0.2%, 内存 0.2%
- 平均响应：1-10 秒

---

## 📦 安装指南

```bash
# 1. 安装依赖
pip3 install aiohttp pyyaml

# 2. 配置
cp proxy-rules.yml /root/.openclaw/searxng/

# 3. 启动
./start-adapter.sh
```

---

## 🧪 测试结果

**5 轮完整测试：**
- 基础搜索：✅
- 压力测试：✅
- 代理切换：✅
- 实际场景：✅
- 性能汇总：✅

详见 `FINAL-TEST-REPORT-v3.0.md`

---

## 📝 升级说明

**从 v2.x 升级：**
1. 备份旧配置
2. 替换 `adapter.py`
3. 添加 `proxy-rules.yml`
4. 重启服务

**破坏性变更：** 无

---

## 🐛 已知问题

1. 部分引擎（qwant）偶尔返回垃圾结果
2. 首次搜索响应较慢（缓存未命中）

---

## 📞 联系方式

- GitHub: pengong101
- Email: pengong101@163.com

---

**完整更新日志：** 见 CHANGELOG.md
