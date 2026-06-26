# 微信公众号发布前核对清单 ⭐⭐⭐⭐⭐

**版本：** v1.0  
**创建日期：** 2026-03-13  
**重要性：** ⭐⭐⭐⭐⭐（必须执行）

---

## 🎯 核对原则

**作为机器人技术社区，内容准确性是第一位的！**

每次发布前必须完成以下核对流程，确保：
- ✅ 所有技术信息准确无误
- ✅ 所有数据来自官方文档
- ✅ 所有链接可正常访问
- ✅ 所有代码可正常运行
- ✅ 无拼写错误和格式问题

---

## 📋 核对清单

### 1️⃣ 技术信息核对 ⭐⭐⭐⭐⭐

#### 机器人品牌列表
- [ ] 核对官方后处理器列表（22 个品牌）
- [ ] 区分后处理器 vs eCatalog 组件
- [ ] 核实新增品牌（VC 5.0 新增）
- [ ] 确认连接器名称和版本

**官方 22 个后处理器品牌（必须逐项核对）：**
```
□ ABB                  □ Mitsubishi MELFA
□ CLOOS                □ Nachi
□ Comau                □ OMRON
□ Denso                □ OTC Daihen
□ Doosan               □ Panasonic
□ FANUC                □ Reis Robotics
□ Hyundai Robotics     □ Siasun
□ IGM                  □ Stäubli
□ Kawasaki             □ Techman
□ KUKA                 □ Universal Robots
□ Yamaha               □ Yaskawa
```

**不在后处理器列表的品牌（需标注）：**
```
□ JAKA - eCatalog 有模型，无后处理器
□ Aubo - eCatalog 有模型，无后处理器
□ Epson - eCatalog 有模型，无后处理器
□ 其他协作机器人品牌
```

#### 软件版本信息
- [ ] 核实 VC 版本号（5.0）
- [ ] 核实 Python 版本（3.12.2）
- [ ] 核实发布日期（2026 年 3 月 12 日）
- [ ] 核实系统要求

#### 功能特性
- [ ] 核实新功能（MBE、自动路径求解器等）
- [ ] 核实支持的文件格式
- [ ] 核实支持的协议（OPC UA、MQTT 等）
- [ ] 核实性能数据（仿真速度提升等）

---

### 2️⃣ 官方文档核对 ⭐⭐⭐⭐⭐

#### 必须查阅的官方页面
- [ ] 官方帮助文档首页
  - https://help.visualcomponents.com/5.0/Premium/en/English/Help.htm
- [ ] 新功能列表
  - https://help.visualcomponents.com/5.0/Premium/en/English/WhatsNew.htm
- [ ] 发布说明
  - https://help.visualcomponents.com/5.0/Premium/en/English/Release_Notes/release_notes_5.0.htm
- [ ] Python 3 API 文档
  - https://help.visualcomponents.com/5.0/Premium/en/Python_3_API/Overview.html
- [ ] 机器人连接器文档
  - https://help.visualcomponents.com/5.0/Premium/en/English/Connectivity/
- [ ] 官网产品页面
  - https://www.visualcomponents.com/products/

#### 核对要点
- [ ] 所有技术参数与官方一致
- [ ] 所有功能描述与官方一致
- [ ] 所有链接可正常访问
- [ ] 所有截图来自官方或自己测试

---

### 3️⃣ 代码示例核对 ⭐⭐⭐⭐⭐

#### Python 代码
- [ ] 语法正确（Python 3）
- [ ] 可正常运行（在 VC 中测试）
- [ ] 导入语句正确（`import vcCore as vc`）
- [ ] 异步函数使用 `async/await`
- [ ] 变量命名规范
- [ ] 注释完整

#### 测试流程
```python
# 1. 在 VC 中创建测试组件
# 2. 添加 Python Script 行为
# 3. 粘贴代码
# 4. 运行仿真
# 5. 检查输出面板
# 6. 确认无错误
```

---

### 4️⃣ 链接核对 ⭐⭐⭐⭐

#### 官方链接
- [ ] 所有链接可正常访问
- [ ] 链接文本准确
- [ ] 无死链
- [ ] 使用官方域名

#### 链接格式
```markdown
✅ 正确：https://help.visualcomponents.com/5.0/...
❌ 错误：help.visualcomponents.com/5.0/...（缺少 https）
```

---

### 5️⃣ 文字核对 ⭐⭐⭐⭐

#### 拼写检查
- [ ] 品牌名称拼写正确
  - ABB（不是 ABB 集团）
  - FANUC（不是 Fanuc）
  - KUKA（不是 Kuka）
  - Yaskawa（不是 YASKAWA）
  - Mitsubishi MELFA（不是 Mitsubishi）
  - Stäubli（注意变音符号）
  - OMRON（不是 Omron）

- [ ] 技术术语正确
  - Python 3（不是 Python3）
  - OPC UA（不是 OPCUA）
  - MQTT（不是 Mqtt）
  - CAD（不是 Cad）
  - PLC（不是 Plc）

#### 格式统一
- [ ] 标题层级一致
- [ ] 代码块格式统一
- [ ] 表格格式统一
- [ ] 列表格式统一

---

### 6️⃣ 图片核对 ⭐⭐⭐

#### 封面图
- [ ] 图片来自官方
- [ ] 图片清晰（≥1200px 宽）
- [ ] 图片比例合适（1.8:1 或 16:9）
- [ ] 无版权问题

#### 文章配图
- [ ] 图片清晰
- [ ] 图片与内容相关
- [ ] 图片有说明文字
- [ ] 无版权风险

---

### 7️⃣ 排版核对 ⭐⭐⭐

#### 公众号排版
- [ ] 标题醒目（使用 HTML 样式）
- [ ] 段落间距合适
- [ ] 代码块清晰
- [ ] 表格在手机端显示正常
- [ ] 无 Markdown 语法残留

#### 手机阅读测试
- [ ] 发送到手机预览
- [ ] 检查代码块是否溢出
- [ ] 检查表格是否完整
- [ ] 检查图片是否清晰
- [ ] 检查排版是否美观

---

### 8️⃣ 作者信息核对 ⭐⭐

- [ ] 作者署名正确（Robotqu）
- [ ] 网站链接正确（https://robotqu.com）
- [ ] B 站链接正确（https://space.bilibili.com/505110287）
- [ ] 公众号名称正确（Robotqu 机器人社区）

---

## ✅ 核对流程

### 第一步：自查（作者）
- [ ] 完成所有核对项
- [ ] 标记不确定的内容
- [ ] 记录核对时间

### 第二步：交叉核对（团队成员）
- [ ] 另一位成员独立核对
- [ ] 重点核对技术信息
- [ ] 记录核对结果

### 第三步：官方文档最终确认
- [ ] 再次查阅官方文档
- [ ] 确认所有技术参数
- [ ] 截图保存核对证据

### 第四步：发布前预览
- [ ] 发送到手机预览
- [ ] 检查所有细节
- [ ] 确认无误后发布

---

## 📝 核对记录模板

```markdown
## 核对记录

**文章标题：** [填写]
**核对日期：** 2026-03-XX
**核对人：** [填写]

### 核对结果
- 技术信息：✅ / ❌
- 官方文档：✅ / ❌
- 代码示例：✅ / ❌
- 链接：✅ / ❌
- 文字：✅ / ❌
- 图片：✅ / ❌
- 排版：✅ / ❌
- 作者信息：✅ / ❌

### 问题记录
1. [问题描述] - [已修正/待确认]
2. [问题描述] - [已修正/待确认]

### 最终确认
- [ ] 所有问题已解决
- [ ] 可以发布
- [ ] 核对时间：[填写]
```

---

## ⚠️ 重要提醒

**每次发布前必须完成核对！**

**宁可延迟发布，也要保证准确性！**

**发现错误立即修正并记录！**

---

*版本：v1.0*  
*创建：2026-03-13*  
*维护：Robotqu 机器人社区*
