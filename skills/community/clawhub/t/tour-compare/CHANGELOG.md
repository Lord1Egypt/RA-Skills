# 🦐 tour-compare 扩展功能更新日志

## v0.2.0 (2026-04-01) - 扩展功能版本

### ✨ 新增功能

#### 1. 🔗 URL 链接抓取

**功能描述**: 支持直接输入携程/飞猪/同程的商品 URL，自动抓取商品信息并进行对比。

**使用方法**:
```bash
# 纯 URL 对比
./scripts/compare.sh compare https://ctrip.com/p/123 https://fliggy.com/p/456

# 混合输入（JSON + URL）
./scripts/compare.sh compare \
  '{"platform":"携程","title":"云南 6 日游","price":3299}' \
  https://fliggy.com/p/789012
```

**支持平台**:
- ✅ 携程 (ctrip.com)
- ✅ 飞猪 (fliggy.com)
- ✅ 同程 (ly.com)
- 🔲 马蜂窝 (计划中)
- 🔲 穷游 (计划中)

**技术实现**:
- 使用 Puppeteer 进行网页抓取
- Cheerio 解析 HTML
- 自动识别平台并提取关键字段（价格、评分、购物店数量等）

**依赖安装**:
```bash
npm install puppeteer cheerio
```

---

#### 2. 🖼️ 导出图片功能

**功能描述**: 将对比报告导出为 PNG 图片，方便分享和保存。

**使用方法**:
```bash
# 导出对比报告
./scripts/compare.sh compare <商品 1> <商品 2> --export report.png

# 带人群参数 + 导出
./scripts/compare.sh compare <商品 1> <商品 2> --group 老人 --export report.png
```

**输出示例**:
- 白色简洁背景
- 标题 + 对比表格
- 推荐标记（🥇🥈🥉）
- 各维度最佳标注
- 生成时间和免责声明

**依赖安装**:
```bash
npm install canvas

# macOS 还需要：
brew install pkg-config cairo pango libpng jpeg giflib librsvg
```

---

#### 3. 📝 改进的 CLI 体验

**新增选项**:
- `--export <path>`: 导出图片
- `--no-fetch`: 禁用自动抓取，强制使用 JSON 模式

**改进的错误提示**:
- 链接抓取失败时提供降级建议
- 缺少依赖时提示安装命令
- 输入格式错误时显示示例

---

### 🔧 技术改进

#### 项目结构
```
skills/tour-compare/
├── src/
│   ├── crawler/           # 新增：爬虫模块
│   │   └── ota-crawler.js
│   ├── export/            # 新增：导出模块
│   │   └── image-exporter.js
│   ├── analyzer/          # 分析引擎
│   ├── ui/                # 输出界面
│   └── config/            # 配置
├── scripts/
│   ├── compare.sh         # CLI 入口
│   └── demo.sh            # 新增：演示脚本
└── examples/
    └── usage.md           # 更新：使用示例
```

#### 依赖管理
- 将 puppeteer/cheerio/canvas 移至 optionalDependencies
- 基础功能无需这些依赖也可使用
- 按需安装高级功能

---

### 📊 功能对比

| 功能 | v0.1.0 | v0.2.0 |
|------|--------|--------|
| JSON 输入对比 | ✅ | ✅ |
| URL 链接对比 | ❌ | ✅ |
| 智能推荐 | ✅ | ✅ |
| 深度分析 | ✅ | ✅ |
| 导出图片 | ❌ | ✅ |
| 人群适配 | ✅ | ✅ |
| 避坑提醒 | ✅ | ✅ |

---

### 🧪 测试脚本

运行完整功能演示：
```bash
cd skills/tour-compare
./scripts/demo.sh
```

演示内容包括：
1. JSON 商品对比（带老人参数）
2. 智能推荐（云南，老人，5000 预算）
3. 深度分析单个商品
4. 帮助信息展示

---

### 📖 文档更新

- ✅ README.md - 添加新功能说明
- ✅ examples/usage.md - 完整使用指南
- ✅ SKILL.md - 更新迭代状态

---

### 🐛 已知问题

1. **图片导出依赖复杂**
   - canvas 在部分系统安装困难
   - 解决方案：考虑使用纯文本报告或简化版导出

2. **链接抓取稳定性**
   - OTA 平台可能反爬虫
   - 解决方案：添加重试机制、User-Agent 轮换

3. **数据准确性**
   - 抓取的数据可能有延迟
   - 解决方案：添加时间戳，提示用户以官网为准

---

### 🎯 下一步计划

#### 短期 (v0.3.0)
- [ ] 添加重试机制和错误处理
- [ ] 支持马蜂窝平台
- [ ] 优化图片导出（无需 canvas 依赖）
- [ ] 添加单元测试

#### 中期 (v0.4.0)
- [ ] 历史价格追踪
- [ ] 行程地图可视化
- [ ] 用户评价情感分析
- [ ] 批量对比（10+ 商品）

#### 长期 (v1.0.0)
- [ ] Web 界面
- [ ] API 服务
- [ ] 浏览器插件
- [ ] 多语言支持

---

### 💡 使用建议

#### 开发者
```bash
# 完整安装（所有功能）
npm install
npm install puppeteer cheerio canvas

# 运行测试
./scripts/demo.sh

# 查看代码结构
tree src/
```

#### 普通用户
```bash
# 基础安装（仅 JSON 模式）
npm install

# 使用示例
./scripts/compare.sh compare \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8}' \
  '{"platform":"飞猪","title":"云南 6 日游","price":2899,"rating":4.6}'
```

---

### 📝 变更日志

**2026-04-01**
- ✅ 添加 URL 链接抓取功能
- ✅ 添加图片导出功能
- ✅ 改进 CLI 错误提示
- ✅ 更新文档和示例

**2026-03-31**
- ✅ 初始版本发布 (v0.1.0)
- ✅ 支持 JSON 输入对比
- ✅ 智能推荐引擎
- ✅ 深度分析功能

---

_Made with 🦐 by 小虾_
