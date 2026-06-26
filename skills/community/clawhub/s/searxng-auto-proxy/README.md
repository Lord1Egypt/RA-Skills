# SearXNG Auto Proxy v3.0 🚀

**自适应代理检测 | 智能引擎切换 | 自动节点优化**

---

## 🎯 核心功能

### 三层自适应架构

```
Layer 1: 规则引擎 → 固定代理策略（Google 必代，百度直连）
Layer 2: 动态探测 → 实时检测引擎状态（30 秒间隔）
Layer 3: 代理优化 → 自动测速选路（30 分钟）
```

### 主要特性

- ✅ **13 个引擎配置** - 5 个必须代理，2 个禁止代理，6 个动态选择
- ✅ **实时探测** - 每 30 秒检测引擎可达性
- ✅ **智能缓存** - 三级缓存（引擎/延迟/节点），命中率>90%
- ✅ **自动优化** - 每 30 分钟测速选择最快节点
- ✅ **故障降级** - 连续失败 3 次自动禁用 5 分钟
- ✅ **Clash 集成** - 自动切换代理节点

---

## 📦 安装

### 前置要求

- SearXNG (Docker)
- Clash Proxy
- Python 3.8+
- 依赖：`aiohttp`, `pyyaml`

### 安装步骤

```bash
# 1. 安装依赖
pip3 install aiohttp pyyaml

# 2. 复制配置文件
cp proxy-rules.yml /root/.openclaw/searxng/

# 3. 启动适配器
./start-adapter.sh
```

---

## 🔧 配置

### 代理规则 (`proxy-rules.yml`)

```yaml
engines:
  google:
    proxy_mode: required    # 必须代理
    fallback: bing
    
  baidu:
    proxy_mode: forbidden   # 禁止代理（直连）
    
  wikipedia:
    proxy_mode: dynamic     # 动态选择
    threshold_ms: 2000
    fallback: baidu
```

### 环境变量

```bash
export CONFIG_FILE=/root/.openclaw/searxng/proxy-rules.yml
export LOG_FILE=/root/.openclaw/logs/searxng-proxy-adapter.log
export CACHE_FILE=/root/.openclaw/searxng/proxy-cache.json
export CLASH_API=http://clash:9090
```

---

## 📊 性能指标

| 指标 | 实测值 |
|------|--------|
| 搜索成功率 | 100% |
| 平均响应 | 1-10s |
| 代理延迟 | 384ms |
| 缓存命中 | >90% |
| CPU 使用 | 0.2% |
| 内存使用 | 0.2% |

---

## 📝 使用

### 启动服务

```bash
./start-adapter.sh
```

### 查看日志

```bash
tail -f /root/.openclaw/logs/searxng-proxy-adapter.log
```

### 查看缓存

```bash
cat /root/.openclaw/searxng/proxy-cache.json | python3 -m json.tool
```

---

## 🧪 测试

完整测试报告见 `FINAL-TEST-REPORT-v3.0.md`

**5 轮测试结果：**
- ✅ 基础搜索：44-49 条结果
- ✅ 压力测试：100% 成功
- ✅ 代理切换：正常
- ✅ 实际场景：学术/代码/新闻
- ✅ 性能汇总：10 次 100% 成功

---

## 📄 许可证

MIT License

---

**作者：** pengong101  
**版本：** 3.0.0  
**更新：** 2026-03-21
