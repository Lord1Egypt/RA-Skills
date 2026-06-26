# QQ邮箱发票下载器 - 完整项目经验与教训总结

**文档用途**: 这份文档记录了从项目开始到 v7.2 的全部经验教训，供未来开发和维护参考，避免重复踩坑。

**最后更新**: 2026-03-09  
**维护者**: momo (记忆管家) 🧠

---

## 目录

1. [项目完整历史](#项目完整历史)
2. [所有踩过的坑](#所有踩过的坑)
3. [核心设计原则](#核心设计原则)
4. [代码规范](#代码规范)
5. [测试 checklist](#测试-checklist)
6. [故障排查指南](#故障排查指南)
7. [版本发布流程](#版本发布流程)

---

## 项目完整历史

### 时间线

```
2026-03-05  项目启动
    ├── v3.2  基础版本 (串行下载)
    └── v4.x  添加MD5去重

2026-03-06  
    ├── v5.0  智能重试机制
    ├── v5.1  浏览器自动化完善
    └── v5.2  终极完整版

2026-03-07
    ├── v6.0  智能自动化版 (auto模式、本地通知)
    ├── v6.1  效率优化版 (并行下载) ⚠️ 缺少浏览器处理！
    └── v6.1.1 修复版 (补回浏览器处理)

2026-03-08
    ├── v6.0.1 目录统一修复
    └── 备份恢复 & Skills配置

2026-03-09  【密集开发日】
    ├── v7.0  终极优化版 (浏览器池3实例) ⚠️ greenlet错误！
    ├── v7.1  稳定优化版 (单浏览器串行) ✅ 修复greenlet
    └── v7.2  增强稳定版 (重试机制、结构化日志) ✅ 当前最新
```

### 版本迭代原因

| 版本 | 为什么创建 | 解决了什么 | 留下了什么问题 |
|------|-----------|-----------|---------------|
| v3.2 | 项目启动 | 基础功能 | 速度慢 |
| v4.x | 需要防重复 | MD5去重 | 还是慢 |
| v5.0 | 网络不稳定 | 重试机制 | 功能单一 |
| v5.1 | 平台支持少 | 更多平台 | 无自动化 |
| v5.2 | 流程不完整 | 自动继续 | 无智能分析 |
| v6.0 | 需要自动化 | auto模式、通知 | 速度一般 |
| v6.1 | 追求速度 | 并行下载 3-5x | **丢失浏览器功能** |
| v6.1.1 | 修复v6.1 | 补回浏览器 | 无 |
| v7.0 | 追求极致性能 | HTTP连接池、浏览器池 | **greenlet错误** |
| v7.1 | 修复v7.0 | 单浏览器串行 | 无重试 |
| v7.2 | 增强稳定性 | 重试机制、日志 | ✅ 当前最佳 |

---

## 所有踩过的坑

### 🔴 严重错误 (导致功能不可用)

#### 1. v6.1 丢失浏览器处理功能
**错误**: 重构时忘记把浏览器处理代码复制到新版本

**现象**: C类发票只记录"待处理"，不会自动下载

**原因**: 
```python
# v6.1 只有A/B类处理
batches = classify_invoices(invoices)
process_batch(batches["attachments"], ...)
process_batch(batches["links"], ...)
# ❌ 忘记处理 batches["browser"]
```

**教训**: 
- 重构时必须逐行对比功能完整性
- 创建功能检查清单
- 每个版本都要有完整测试

---

#### 2. v7.0 greenlet 错误
**错误**: 多线程并行使用 Playwright 浏览器

**现象**: 
```
greenlet.error: cannot switch to a different thread
```

**原因**: Playwright sync_api 不是线程安全的

**错误代码**:
```python
# ❌ 错误: 多线程使用浏览器
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(browser_pool.process, item) 
               for item in items]
```

**正确代码**:
```python
# ✅ 正确: 单浏览器 + Lock 串行
class BrowserPool:
    def __init__(self):
        self._lock = Lock()
    
    def process(self, item):
        with self._lock:  # 保证串行
            # 浏览器操作
```

**教训**:
- **浏览器自动化必须串行！**
- 即使使用多线程，也要通过锁机制保证单线程访问
- 不要为了追求性能牺牲稳定性

---

#### 3. v7.2 开发中的参数传递错误
**错误**: 重构时参数签名不一致

**现象**: `KeyError: 'idx'`

**错误代码**:
```python
# 调用处
result = self.process_browser_with_retry(email_data)

# 定义处
def process_browser_with_retry(self, msg_data, max_retries=3):
    result = self.browser_pool.process_invoice(
        msg_data, msg_data["idx"]  # ❌ msg_data里没有idx！
    )
```

**正确代码**:
```python
# 调用处
result = self.process_browser_with_retry(email_data, idx)

# 定义处  
def process_browser_with_retry(self, email_data, idx, max_retries=3):
    result = self.browser_pool.process_invoice(email_data, idx)
```

**教训**:
- 重构时必须检查所有调用点
- 使用 IDE 的重构工具，不要手动替换
- 参数传递要显式，不要依赖字典内部结构

---

### 🟡 中等错误 (影响性能或体验)

#### 4. 浏览器内存泄漏
**现象**: 长时间运行后浏览器越来越慢，最终崩溃

**原因**: 浏览器实例长期运行不重启，内存不断增长

**解决**:
```python
def _should_restart_browser(self):
    """每50个页面重启一次浏览器"""
    self._page_count += 1
    if self._page_count >= 50:
        self._restart_browser()
        self._page_count = 0
```

**教训**:
- 长期运行的服务必须考虑资源释放
- 定期重启是防止内存泄漏的有效手段
- 监控资源使用情况

---

#### 5. 资源清理不完善
**现象**: 程序退出时浏览器进程残留

**原因**: 资源关闭时没有异常保护

**错误代码**:
```python
# ❌ 错误: 没有异常保护
def close(self):
    self.context.close()  # 如果这里抛出异常...
    self.browser.close()  # ...这行就不会执行
    self.playwright.stop()
```

**正确代码**:
```python
# ✅ 正确: 每个资源都有try-except
def close(self):
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

**教训**:
- 每个资源清理都要有异常保护
- 一个资源清理失败不应影响其他资源
- 使用 debug 级别记录异常，避免污染日志

---

#### 6. 错误信息太短
**现象**: 出错时无法定位问题

**原因**: 错误信息截断太短

**错误代码**:
```python
"备注": str(e)[:50]  # 太短，关键信息丢失
```

**正确代码**:
```python
"备注": str(e)[:100]  # 适当增加长度
```

**教训**:
- 错误信息要足够长以便定位问题
- 但也要避免过长影响显示
- 100字符是较好的平衡点

---

#### 7. 使用 print 而非 logging
**现象**: 日志没有时间戳，难以追踪问题

**原因**: 早期使用 print 输出

**错误代码**:
```python
print(f"✅ 找到 {count} 封发票邮件")
# 输出: ✅ 找到 10 封发票邮件
```

**正确代码**:
```python
logger.info(f"✅ 找到 {count} 封发票邮件")
# 输出: 2026-03-09 22:13:23,862 - INFO - ✅ 找到 10 封发票邮件
```

**教训**:
- 生产环境必须使用 logging
- 日志要有时间戳和级别
- 便于问题追踪和调试

---

### 🟢 小错误 (代码风格问题)

#### 8. 线程安全问题
**现象**: 偶发的重复下载

**原因**: MD5去重没有加锁

**错误代码**:
```python
def is_duplicate(self, content):
    file_hash = hashlib.md5(content).hexdigest()
    # ❌ 没有锁保护
    if file_hash in self.downloaded_hashes:
        return True
    self.downloaded_hashes.add(file_hash)
    return False
```

**正确代码**:
```python
def is_duplicate(self, content):
    file_hash = hashlib.md5(content).hexdigest()
    with self.download_lock:  # ✅ 加锁保护
        if file_hash in self.downloaded_hashes:
            return True
        self.downloaded_hashes.add(file_hash)
        return False
```

**教训**:
- 共享资源必须使用锁保护
- 多线程环境下要考虑线程安全
- 使用 `threading.Lock()`

---

#### 9. 硬编码路径
**现象**: 代码在不同环境无法运行

**原因**: 路径写死在代码中

**错误代码**:
```python
BASE_DIR = r"Z:\OpenClaw\InvoiceOC"  # 硬编码
```

**正确代码**:
```python
BASE_DIR = os.environ.get("INVOICE_DIR", r"Z:\OpenClaw\InvoiceOC")
# 允许通过环境变量覆盖
```

**教训**:
- 配置项要可配置
- 使用环境变量或配置文件
- 提供默认值

---

## 核心设计原则

### 1. 稳定性 > 性能

**正确做法**:
- 先保证稳定运行，再考虑性能优化
- v7.0 为了追求性能导致 greenlet 错误，v7.1 回归稳定

**经验公式**:
```
可用性 = 稳定性 × 性能
如果稳定性 = 0，性能再高也是 0
```

---

### 2. 渐进式优化

**正确做法**:
- 小步快跑，每个版本解决一个核心问题
- 不要一次性改动太多

**版本演进**:
```
v6.0 → 功能完整
v6.1 → 性能优化 (但出错了)
v6.1.1 → 修复错误
v7.0 → 再次性能优化 (又出错了)
v7.1 → 再次修复
v7.2 → 增强稳定性
```

---

### 3. 防御式编程

**正确做法**:
- 假设所有外部输入都可能出错
- 所有操作都可能失败
- 做好异常处理

**代码示例**:
```python
try:
    result = process()
except SpecificError as e:
    # 特定错误处理
    logger.error(f"特定错误: {e}")
except Exception as e:
    # 通用错误处理
    logger.error(f"未知错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    # 清理资源
    cleanup()
```

---

### 4. 智能分类策略

**核心逻辑**:
```
任务按速度分类:
├── 快速任务 (A类) → 高并发
├── 中速任务 (B类) → 中并发
└── 慢速任务 (C类) → 低并发/串行
```

**好处**:
- 快速任务不被慢速任务阻塞
- 资源合理分配
- 用户体验好

---

## 代码规范

### 1. 类设计规范

```python
class ConnectionPool:
    """HTTP连接池 - 复用连接减少开销
    
    使用单例模式确保全局只有一个连接池实例
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        # 线程安全的单例实现
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_session()
        return cls._instance

    def _init_session(self):
        """初始化session (私有方法)"""
        pass

    def get(self, url, **kwargs):
        """获取URL (公共方法)"""
        pass
```

---

### 2. 函数设计规范

```python
def process_with_retry(
    self, 
    data: dict, 
    max_retries: int = 3,
    retry_delay: float = 2.0
) -> dict:
    """处理数据，失败时自动重试
    
    Args:
        data: 要处理的数据
        max_retries: 最大重试次数，默认3次
        retry_delay: 重试延迟基数，默认2秒
        
    Returns:
        处理结果字典，包含status和data字段
        
    Raises:
        不会抛出异常，所有错误都封装在返回值中
    """
    for attempt in range(max_retries):
        try:
            result = self._process(data)
            if result["status"] == "success":
                return result
        except Exception as e:
            logger.warning(f"尝试 {attempt+1} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay ** attempt)
    
    return {"status": "failed", "error": "超过最大重试次数"}
```

---

### 3. 日志规范

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 使用日志
logger.debug("调试信息")      # 开发调试用
logger.info("普通信息")       # 正常流程
logger.warning("警告信息")    # 需要注意
logger.error("错误信息")      # 发生错误
logger.critical("严重错误")   # 系统级错误
```

---

### 4. 异常处理规范

```python
def safe_operation(self):
    """安全操作示例"""
    resource = None
    try:
        resource = open_resource()
        result = process(resource)
        return result
    except SpecificException as e:
        # 特定异常：记录并处理
        logger.error(f"特定错误: {e}")
        return {"status": "error", "type": "specific"}
    except Exception as e:
        # 通用异常：记录完整堆栈
        logger.error(f"未知错误: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return {"status": "error", "type": "unknown"}
    finally:
        # 确保资源释放
        if resource:
            try:
                resource.close()
            except Exception as e:
                logger.debug(f"资源释放失败: {e}")
```

---

## 测试 Checklist

### 功能测试

- [ ] 能正常登录QQ邮箱
- [ ] 能正确搜索发票邮件
- [ ] A类附件能正确下载
- [ ] B类链接能正确下载
- [ ] C类浏览器能正确处理
- [ ] ZIP文件能正确解压
- [ ] 重复文件能正确跳过
- [ ] Excel报告能正确生成

### 异常测试

- [ ] 网络断开时能优雅处理
- [ ] 邮箱登录失败时能提示
- [ ] 下载超时能重试
- [ ] 浏览器崩溃能恢复
- [ ] 文件写入失败能记录

### 性能测试

- [ ] 10封邮件能在3分钟内完成
- [ ] 50封邮件能在10分钟内完成
- [ ] 内存使用不超过500MB
- [ ] CPU使用不超过50%

### 稳定性测试

- [ ] 连续运行1小时不崩溃
- [ ] 处理100+页面后浏览器正常
- [ ] 多次运行结果一致

---

## 故障排查指南

### 问题1: greenlet 错误
**症状**: `greenlet.error: cannot switch to a different thread`

**原因**: 多线程使用Playwright

**解决**: 改为单浏览器串行处理

---

### 问题2: 浏览器下载失败
**症状**: C类发票全部失败

**排查步骤**:
1. 检查 Playwright 是否安装: `playwright install chromium`
2. 检查浏览器能否启动
3. 检查网络连接
4. 查看日志中的具体错误

---

### 问题3: 登录失败
**症状**: `登录失败` 或 `认证错误`

**排查步骤**:
1. 检查邮箱账号密码
2. 检查QQ邮箱授权码是否过期
3. 检查网络连接
4. 检查IMAP服务是否开启

---

### 问题4: 下载速度慢
**症状**: 处理大量邮件时很慢

**优化方法**:
1. 使用 v7.2 版本 (有HTTP连接池)
2. 增加A/B类线程数
3. 检查网络带宽
4. 关闭其他占用网络的程序

---

## 版本发布流程

### 1. 开发阶段

```
1. 从最新稳定版创建分支
2. 实现新功能/修复bug
3. 本地测试通过
4. 代码审查
```

### 2. 测试阶段

```
1. 功能测试 (checklist全部通过)
2. 异常测试 (各种错误场景)
3. 性能测试 (速度、内存)
4. 稳定性测试 (长时间运行)
```

### 3. 文档更新

```
1. 更新 CHANGELOG.md
2. 更新 SKILL.md
3. 更新版本对比表
4. 添加使用示例
```

### 4. 发布阶段

```
1. 创建版本tag
2. 合并到主分支
3. 通知用户
4. 监控反馈
```

---

## 核心经验口诀

```
浏览器必须串行，多线程要加锁
连接池能提速，重试机制保成功
日志记录要详细，错误信息要完整
资源清理要完善，异常处理要全面
渐进优化要稳健，稳定性大于性能
```

---

## 快速参考

### 推荐版本

| 场景 | 版本 | 原因 |
|------|------|------|
| 生产环境 | **v7.2** | 最稳定，成功率最高 |
| 快速测试 | v7.1 | 简单可靠 |
| 避免使用 | v7.0, v6.1 | 有严重bug |

### 常用命令

```bash
# 运行最新版
python invoice_downloader_v72.py 260301 260309

# 运行指定日期范围
python invoice_downloader_v72.py <开始日期YYMMDD> <结束日期YYMMDD>

# 安装依赖
pip install imap-tools pandas openpyxl requests playwright
playwright install chromium
```

### 配置项

```python
EMAIL = "181957682@qq.com"           # 邮箱账号
PASSWORD = "dcdrfqjmoczrbhdj"        # 授权码
BASE_DIR = r"Z:\OpenClaw\InvoiceOC"  # 输出目录
MAX_RETRIES = 3                       # 最大重试次数
BROWSER_RESTART_INTERVAL = 50         # 浏览器重启间隔(页面数)
```

---

**文档结束**

如有新问题，请更新此文档，避免后人重复踩坑。

**维护记录**:
- 2026-03-09: 初始版本，总结 v3.2 → v7.2 全部经验
