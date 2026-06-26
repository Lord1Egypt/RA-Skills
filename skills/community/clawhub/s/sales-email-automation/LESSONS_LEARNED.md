# 📝 邮件发送教训总结

> **位置：** `/Users/wilson/.openclaw/workspace/skills/imap-smtp-email/LESSONS_LEARNED.md`  
> **适用范围：** 所有使用邮件系统发送开发信的 Agent  
> **最后更新：** 2026-03-15 02:50

---

## ⚠️ 四大教训（必读！）

### 教训 1：报价单遗漏

**时间：** 2026-03-15  
**事件：** 给意大利客户 LABEL ITALY 发开发信，只附了产品目录，没有附报价单。

**根本原因：**
- 看到 `output/` 目录不存在，就默认"没有报价单"
- 没有检查 `examples/` 目录里已经有现成报价单

**改进措施：**
- ✅ 发送前检查清单明确要求检查 `output/` **和** `examples/` 两个目录
- ✅ 如报价单不存在，必须调用报价单生成 skill 生成新的

**原则：** 发送前做完整检查，一次性发送完整邮件。

---

### 教训 2：直接照抄模板内容 ⭐

**时间：** 2026-03-15  
**事件：** 给意大利客户 LABEL ITALY 发送开发信时，直接使用了 `development-email.html` 模板，内容中包含：
- "Hi Paul and the QUADNET Team"（澳洲客户名称）
- "West Gladstone, Queensland"（澳洲地点）

**问题严重性：**
- ❌ 客户收到后会发现这是群发模板邮件，缺乏诚意
- ❌ 显得不专业，降低信任度
- ❌ 可能直接被客户标记为垃圾邮件

**根本原因：**
1. 把模板当成了"可以直接发送的成品"
2. 没有理解模板仅作为结构参考
3. 没有根据客户信息生成个性化内容

**改进措施：**
- ✅ 在 SKILL.md 中明确"禁止直接照抄模板"原则
- ✅ 添加发送前检查清单：必须生成个性化正文
- ✅ 提供不同国家客户的寒暄示例

**原则：**
> **模板只参考结构，内容必须定制。**  
> 每次发送前，根据客户信息（公司名、国家、行业）生成个性化正文。  
> 宁可多花 2 分钟定制内容，也不要发送千篇一律的模板邮件。

---

### 教训 3：碎片化发送

**时间：** 2026-03-15  
**事件：** 先发一封只有目录的邮件，后补发带报价单的邮件。

**问题：**
- 客户收到两封独立邮件，体验差
- 显得工作流程混乱
- 增加沟通成本

**原则：** 发送前做完整检查，一次性发送完整邮件。

---

### 教训 4：使用示例报价单而非生成专属报价单 ⭐⭐⭐

**时间：** 2026-03-15  
**事件：** 给美国客户 SPECIALIZED COMPUTER PRODUCTS USA 发送开发信时，直接使用了 `examples/QT-TEST-001-Final.pdf` 这个示例文件，而不是为客户生成专属报价单。

**问题严重性：**
- ❌ 报价单上没有客户公司名称和地址
- ❌ 产品列表不是针对客户需求定制的
- ❌ 显得不专业，像群发垃圾邮件
- ❌ 客户无法用这份报价单做内部采购申请

**根本原因：**
1. **偷懒走捷径** - 看到 `examples/` 目录有现成的 PDF，就直接用了
2. **违反检查清单** - 没有执行"如报价单不存在，调用报价单生成 skill"这一步
3. **没有客户视角** - 为了快速完成任务，跳过定制环节

**正确流程（必须遵守）：**

```markdown
1. 收集客户信息（公司名、地址、行业、联系人）
2. 创建报价单数据文件（JSON 格式，包含客户信息和产品列表）
   位置：/Users/wilson/.openclaw/workspace/skills/quotation-workflow/data/<客户简称>.json
3. 调用报价单生成 skill 生成专属报价单：
   cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow
   bash scripts/generate-all.sh data/<客户数据>.json QT-<日期>-<客户简称>
4. 确认生成的 PDF 文件存在（*-Final.pdf 或 *-HTML.pdf）
5. 发送邮件时附上这份专属报价单
```

**示例数据文件模板：**
```json
{
  "quotationNo": "QT-20260315-002",
  "date": "2026-03-15",
  "validUntil": "2026-04-14",
  "customer": {
    "name": "客户公司名",
    "address": "客户地址",
    "country": "国家",
    "email": "客户邮箱"
  },
  "products": [
    {
      "description": "HDMI 2.1 Cable 8K@60Hz 48Gbps",
      "specification": "1.5m, Black",
      "quantity": 1000,
      "unitPrice": 3.50
    }
  ],
  "terms": {
    "moq": "500 pcs (negotiable)",
    "delivery": "7-15 days for standard products",
    "payment": "T/T, L/C, PayPal",
    "packaging": "Gift box, kraft box, PE bag"
  }
}
```

**✅ 脚本已兼容多种字段格式：**
- `customer.name` / `customer.company_name` 都支持
- `product.unitPrice` / `product.unit_price` 都支持
- `terms` 字典格式 / 列表格式 都支持
- `quotationNo` / `quotation.quotation_no` 都支持

**模板文件：** `/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/template-standard.json`

**改进措施：**
- ✅ 在 SKILL.md 中明确"禁止使用示例报价单"原则
- ✅ 在发送前检查清单中强调"必须生成专属报价单"
- ✅ 提供报价单数据文件模板和生成命令
- ✅ 将此教训记录到 MEMORY.md

**原则：**
> **每次开发信必须生成新的专属报价单，禁止使用示例文件。**  
> 报价单是正式商务文件，必须包含：客户公司名、地址、定制产品列表、有效报价。  
> 示例文件仅用于测试和演示，绝对不能发送给真实客户。

**记忆口诀：**
```
开发信三件套：个性化正文 + 产品目录 + 专属报价单 ⭐
示例文件 = 测试用，禁止发给客户 ❌
```

---

## ✅ 发送前检查清单（最终版）

**必须按顺序执行，确保一次性发送完整邮件：**

```markdown
1. [ ] **收集客户信息**（从 OKKI 或其他来源）
   - 公司名称
   - 国家/地区
   - 行业/业务类型
   - 联系人姓名（如有）
   - 邮箱地址

2. [ ] **生成个性化邮件正文** ⭐
   - 根据客户信息定制寒暄内容（提及客户所在地/行业）
   - 调整语气和重点（不同市场关注点不同）
   - 生成 HTML 文件或准备 `--body` 内容
   - **禁止直接照抄模板中的特定客户信息**

3. [ ] 确认产品目录存在
   - 检查：`/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf`
   - 路径包含空格，命令中需要用引号包裹

4. [ ] **生成专属报价单** ⭐⭐⭐（禁止使用示例文件）
   - **原则：** 每次开发信必须生成新的专属报价单，禁止使用示例文件
   - **步骤：**
     ```bash
     # 1. 创建客户专属数据文件
     # 位置：/Users/wilson/.openclaw/workspace/skills/quotation-workflow/data/<客户简称>.json
     
     # 2. 调用报价单生成 skill
     cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow
     bash scripts/generate-all.sh data/<客户数据>.json QT-<日期>-<客户简称>
     
     # 3. 确认生成的 PDF 文件
     ls data/QT-*.pdf
     ```
   - **重要：** 邮件附件必须使用 HTML 转换的 PDF（`*-HTML.pdf` 或 `*-Final.pdf`）
     - ✅ HTML 转换的 PDF = 邮件附件（现代设计，专业美观）
     - ⚠️ Excel 转换的 PDF = 内部存档（仅用于内部，不发送客户）
   - **禁止：** ❌ 不要使用 `examples/` 目录的示例报价单发送给客户

5. [ ] 确认所有附件路径正确且文件可读
   ```bash
   ls -la "/path/to/catalogue.pdf"
   ls -la "/path/to/quotation.pdf"
   ```

6. [ ] 一次性发送完整邮件（正文 + 目录 + 报价单）
```

---

## 📚 相关文档

- **SKILL.md** - 邮件系统技能文档（含完整工作流）
- **INTEGRATION.md** - 集成配置文档
- **TOOLS.md** - 全员共享工具集
- **MEMORY.md** - 长期记忆（教训已记录）

---

**创建者：** WILSON  
**创建时间：** 2026-03-15 02:50  
**目的：** 确保所有 Agent 遵守正确流程，避免重复犯错
