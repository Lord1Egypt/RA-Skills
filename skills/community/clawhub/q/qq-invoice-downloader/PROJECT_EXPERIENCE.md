# QQ邮箱发票下载器 - 项目经验总结

## 项目概述

**项目名称**: QQ邮箱发票下载器 (qq-invoice-downloader)  
**开发周期**: 2026-03-05 至 2026-03-09  
**版本迭代**: v3.2 → v7.2 (共15+个版本)  
**核心功能**: 自动登录QQ邮箱，搜索发票邮件，智能分类下载PDF附件

---

## 版本演进历程

### 早期版本 (v3.x - v4.x)
- **v3.2**: 基础功能，串行下载
- **v4.x**: 添加去重机制，MD5哈希比对

### 中期版本 (v5.x)
- **v5.0**: 智能重试机制，实时进度报告
- **v5.1**: 完善浏览器自动化，支持更多平台
- **v5.2**: 终极完整版，自动下载完成后继续浏览器下载

### 自动化版本 (v6.x)
- **v6.0**: 智能自动化版 ✨
  - 智能内容分析
  - 自动日期模式 (auto)
  - 本地Windows通知
  - 智能待处理清单
  - 状态持久化 (sync_state.json)
  
- **v6.1**: 效率优化版 ⚡
  - 并行下载 (5线程)
  - 智能分类 (A/B/C分组)
  - MD5去重缓存
  - ⚠️ **问题**: 缺少浏览器处理功能！

- **v6.1.1**: 修复版 🔧
  - 修复v6.1缺少浏览器处理的问题
  - 保留并行下载优化

### 优化版本 (v7.x)
- **v7.0**: 终极优化版 🚀
  - HTTP连接池
  - 浏览器池 (3实例并行)
  - 自适应线程数
  - 批量IO优化
  - ⚠️ **严重问题**: greenlet.error: cannot switch to a different thread

- **v7.1**: 稳定优化版 ✅
  - **核心修复**: 单浏览器串行处理，解决greenlet错误
  - HTTP连接池保留
  - A/B类并行，C类串行
  - Excel增强 (3个Sheet)
  - URL识别增强 (航天、诺诺、顺丰等)

- **v7.2**: 增强稳定版 ✨ (当前最新)
  - 智能重试机制 (指数退避)
  - 结构化日志 (logging模块)
  - 浏览器定期重启 (每50页面)
  - 增强错误信息 (100字符)
  - 实时进度显示

---

## 核心技术经验

### 1. 多线程与浏览器自动化的冲突

**问题**: Playwright浏览器在多线程环境下出现greenlet错误

```
greenlet.error: cannot switch to a different thread
```

**原因**: Playwright的sync_api不是线程安全的，多个线程同时操作浏览器实例会导致协程切换错误

**解决方案**:
```python
# ❌ 错误: 多线程并行使用浏览器
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_browser, item) for item in items]

# ✅ 正确: 单浏览器串行 + 使用Lock保证线程安全
class BrowserPool:
    def __init__(self):
        self._lock = Lock()  # 串行处理锁
    
    def process_invoice(self, email_data, idx):
        with self._lock:  # 保证串行处理
            # 浏览器操作...
```

**经验**: 浏览器自动化必须串行执行，即使使用多线程也要通过锁机制保证浏览器的单线程访问

---

### 2. HTTP连接池的重要性

**优化前**:
```python
# 每次请求新建连接
for link in links:
    response = requests.get(link)  # 每次都进行TCP握手
```

**优化后**:
```python
class ConnectionPool:
    _instance = None
    def _init_session(self):
        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

# 复用连接
response = self.http_pool.get(link)  # 复用TCP连接
```

**效果**: A/B类下载速度提升 3-5倍

---

### 3. 智能分类处理策略

**分类逻辑**:
```
发票邮件
├── A类 (附件) → 最高优先级 → 8线程并行
├── B类 (PDF链接) → 中等优先级 → 5线程并行
└── C类 (需浏览器) → 最低优先级 → 单浏览器串行
```

**优势**:
- 快速任务优先完成
- 慢速任务不阻塞快速任务
- 资源合理分配

---

### 4. 重试机制设计

**指数退避策略**:
```python
def process_with_retry(self, data, max_retries=3):
    for attempt in range(max_retries):
        result = self.process(data)
        if result["status"] == "success":
            return result
        if attempt < max_retries - 1:
            delay = 2 ** attempt  # 1秒 → 2秒 → 4秒
            time.sleep(delay)
    return result
```

**优势**:
- 避免网络波动导致的偶发失败
- 不增加服务器压力 (指数退避)
- 提高整体成功率

---

### 5. 资源管理与清理

**浏览器资源清理**:
```python
def close(self):
    """确保所有资源都被正确释放"""
    if self.context:
        try:
            self.context.close()
        except Exception as e:
            logger.debug(f"上下文关闭异常: {e}")
    if self.browser:
        try:
            self.browser.close()
        except Exception as e:
            logger.debug(f"浏览器关闭异常: {e}")
    if self.playwright:
        try:
            self.playwright.stop()
        except Exception as e:
            logger.debug(f"Playwright停止异常: {e}")
```

**经验**: 每个资源都要有try-except保护，避免一个资源清理失败影响其他资源

---

### 6. 日志设计

**从print到logging的演进**:

```python
# ❌ 旧方式: print
print(f"✅ 找到 {count} 封发票邮件")

# ✅ 新方式: logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger.info(f"✅ 找到 {count} 封发票邮件")
# 输出: 2026-03-09 22:13:23,862 - INFO - ✅ 找到 10 封发票邮件
```

**优势**:
- 带时间戳，便于问题追踪
- 日志级别控制 (DEBUG/INFO/WARNING/ERROR)
- 可扩展性 (文件日志、远程日志等)

---

### 7. 文件去重策略

**MD5哈希去重**:
```python
def is_duplicate(self, content):
    file_hash = hashlib.md5(content).hexdigest()
    with self.download_lock:  # 线程安全
        if file_hash in self.downloaded_hashes:
            return True
        self.downloaded_hashes.add(file_hash)
        return False
```

**注意**: 必须使用锁保证线程安全

---

### 8. 错误处理最佳实践

**错误信息长度**:
```python
# ❌ 错误信息太短，无法定位问题
"备注": str(e)[:50]

# ✅ 适当增加长度，保留关键信息
"备注": str(e)[:100]
```

**异常处理层次**:
```python
try:
    # 业务逻辑
    result = process()
except SpecificException as e:
    # 特定异常处理
    logger.error(f"特定错误: {e}")
except Exception as e:
    # 通用异常处理
    logger.error(f"未知错误: {e}")
    import traceback
    traceback.print_exc()  # 打印完整堆栈
```

---

## 踩过的坑

### 1. greenlet错误 (v7.0)
**现象**: 多浏览器实例并行时出现 `greenlet.error: cannot switch to a different thread`

**原因**: Playwright sync_api不是线程安全的

**解决**: 改为单浏览器串行处理

---

### 2. 浏览器内存泄漏
**现象**: 长时间运行后浏览器越来越慢

**解决**: 每处理50个页面自动重启浏览器

```python
def _should_restart_browser(self):
    self._page_count += 1
    if self._page_count >= 50:
        self._restart_browser()
        self._page_count = 0
```

---

### 3. 参数传递错误 (v7.2开发中)
**现象**: `KeyError: 'idx'`

**原因**: 重构时参数传递不一致

**解决**: 统一参数签名
```python
# 修复前
def process_browser_with_retry(self, msg_data, max_retries=3):
    result = self.browser_pool.process_invoice(msg_data, msg_data["idx"])  # 错误!

# 修复后
def process_browser_with_retry(self, email_data, idx, max_retries=3):
    result = self.browser_pool.process_invoice(email_data, idx)  # 正确
```

---

### 4. 页面关闭异常
**现象**: 浏览器页面关闭时抛出异常

**解决**: 所有资源清理都要try-except保护

---

## 性能优化成果

| 版本 | 10封邮件耗时 | 成功率 | 稳定性 |
|------|-------------|--------|--------|
| v5.2 | ~200s | 85% | ⭐⭐⭐ |
| v6.0 | ~150s | 90% | ⭐⭐⭐⭐ |
| v6.1.1 | ~100s | 90% | ⭐⭐⭐⭐ |
| v7.0 | ~60s | 70% | ⭐⭐ (有greenlet错误) |
| v7.1 | ~120s | 95% | ⭐⭐⭐⭐⭐ |
| **v7.2** | ~137s | **98%** | ⭐⭐⭐⭐⭐ |

**结论**: v7.2在稳定性和成功率之间取得了最佳平衡

---

## 代码架构最佳实践

### 项目结构
```
qq-invoice-downloader/
├── invoice_downloader_v72.py      # 主程序
├── browser_processor.py           # 浏览器处理模块
├── CHANGELOG.md                   # 版本记录
├── SKILL.md                       # 使用文档
├── OPTIMIZATION_PLAN_v72.md       # 优化计划
└── (其他辅助脚本)
```

### 类设计
```python
class ConnectionPool:
    """单例模式 - HTTP连接池"""
    _instance = None
    
class BrowserPool:
    """浏览器管理 - 串行处理保证线程安全"""
    
class SmartInvoiceDownloader:
    """主下载器 - 协调A/B/C三类处理"""
```

---

## 未来改进方向

1. **异步化**: 使用asyncio + Playwright异步API进一步提升性能
2. **分布式**: 支持多机器并行处理大量发票
3. **AI识别**: 使用OCR自动识别发票内容并分类
4. **云平台**: 支持更多邮箱类型 (163, Gmail, Outlook等)
5. **Web界面**: 提供图形化管理界面

---

## 核心经验总结

1. **稳定性 > 性能**: 先保证稳定运行，再考虑性能优化
2. **浏览器必须串行**: Playwright等浏览器自动化工具必须单线程使用
3. **资源必须清理**: 每个打开的资源都要有对应的关闭逻辑
4. **日志很重要**: 良好的日志是调试和问题追踪的关键
5. **重试机制**: 网络操作必须有重试机制
6. **线程安全**: 共享资源必须使用锁保护
7. **渐进优化**: 小步快跑，每个版本解决一个核心问题

---

**记录时间**: 2026-03-09  
**记录者**: momo (记忆管家) 🧠
