# Sci-Hub Mirrors Reference (2026 Updated)

## ✅ 工作状态

**Sci-Hub PDF 链接可以直接提取，无需浏览器！**

### 推荐镜像

| 镜像 | 状态 | 说明 |
|------|------|------|
| `sci-hub.ru` | ✅ **推荐** | 重定向到 sci-net.xyz |
| `sci-net.xyz` | ✅ 工作 | 新域名，PDF 直接嵌入 |
| `sci-hub.st` | ⚠️ 受限 | DDoS-Guard 保护 |

### 使用方法

```bash
# 直接下载
scihub-dl "10.1038/s43017-022-00373-x"

# 指定镜像
scihub-dl "10.1038/s43017-022-00373-x" -m sci-hub.ru
```

---

## 🔧 技术原理

### PDF 链接提取

Sci-Hub/Sci-Net 将 PDF 嵌入在 iframe 中：

```html
<iframe src = "//pdf.sci-net.xyz/{hash}/{title}.pdf#view=FitH">
```

**scihub-dl 自动提取：**
1. 获取 HTML 响应
2. 解析 iframe src 属性
3. 处理协议相对 URL（`//` → `https://`）
4. 移除 URL 锚点参数
5. 直接下载 PDF

### 为什么不需要浏览器？

- PDF URL 在初始 HTML 响应中就有
- 不需要 JavaScript 渲染
- 直接 HTTP 请求即可获取

---

## 🌐 替代资源

### 合法替代
| 服务 | URL | 说明 |
|------|-----|------|
| Unpaywall | unpaywall.org | 浏览器扩展，自动找 OA |
| OA Button | openaccessbutton.org | 免费论文搜索 |
| Core | core.ac.uk | 开放获取仓库 |
| DOAJ | doaj.org | 开放期刊目录 |

### 学术社交网络
- **ResearchGate**: 向作者索取全文
- **Academia.edu**: 作者可能上传预印本
- **Twitter/X**: #ICanHazPDF 标签求助

---

## 📋 故障排除

### 问题：页面显示验证码
**解决**: 手动完成验证，或换一个镜像

### 问题：PDF 不加载
**解决**: 
1. 刷新页面
2. 清除浏览器缓存
3. 尝试其他镜像
4. 使用 VPN

### 问题：404 Not Found
**解决**: 论文可能不在 Sci-Hub 数据库中，尝试：
1. 搜索论文标题 + "pdf"
2. 联系作者索取
3. 通过图书馆获取

---

## 🔄 更新记录

- **2026-03**: sci-hub.st 和 sci-hub.ru 重定向到 sci-net.xyz
- **2026-03**: sci-hub.se 被封锁
- **2025-12**: DDoS-Guard 保护增加

---

## ⚖️ 免责声明

使用 Sci-Hub 可能违反您所在地区的版权法律。请：
- 仅用于学术研究
- 优先使用合法替代方案
- 遵守当地法律法规