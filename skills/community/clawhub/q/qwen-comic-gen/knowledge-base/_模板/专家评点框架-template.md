# 专家评点框架模板

**用途**: 用于豆包会话后的知识内化与深度分析  
**适用场景**: 任何需要从专家角度评点的知识领域  
**输出格式**: HTML 专业版（Mermaid 图表 + 深度分析）

---

## 📋 标准结构

### 1. 专家总评（必填）
- 总体评分（0-100 分）
- 4 维度分析：
  - ✅ 做得好的地方
  - ❌ 严重错误
  - ⚠️ 关键欠缺
  - ⚠️ 模糊地带

### 2. 错误纠正（必填）
- 原文引用
- 纠正内容
- 专家分析（为什么错、影响是什么）

### 3. 关键欠缺（必填）
- 缺失模块 1 + 风险 + 建议
- 缺失模块 2 + 风险 + 建议
- 缺失模块 3 + 风险 + 建议

### 4. 知识架构图（必填）
- Mermaid 思维导图
- 展示知识点之间的逻辑关系

### 5. 完整对比表（推荐）
- 多维度对比表格
- 帮助快速区分相似概念

### 6. 专家建议框架（推荐）
- 6 大模块完整方案
- 可落地的行动建议

### 7. 决策树（可选）
- 判断流程图
- 帮助快速决策

### 8. 专家总结（必填）
- 总体评价
- 优点总结
- 缺点总结
- 行动建议

---

## 🎨 HTML 模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>[主题] - 专家深度评点</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        /* 渐变色背景 + 专业卡片式设计 */
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 [主题] - 专家深度评点</h1>
        
        <!-- 1. 专家总评 -->
        <div class="section">
            <h2>📊 专家总评</h2>
            <div class="expert-verdict">
                <h3>阿福专家 verdict：[分数] 分 - [一句话评价]</h3>
                <div class="verdict-grid">
                    <div class="verdict-item verdict-good">✅ 做得好的地方</div>
                    <div class="verdict-item verdict-bad">❌ 严重错误</div>
                    <div class="verdict-item verdict-warning">⚠️ 关键欠缺</div>
                    <div class="verdict-item verdict-warning">⚠️ 模糊地带</div>
                </div>
            </div>
        </div>
        
        <!-- 2. 错误纠正 -->
        <div class="section">
            <h2>🔧 错误纠正</h2>
            <div class="correction-box">
                <h4>错误 1：[错误名称]</h4>
                <div class="original">❌ 原文：[引用]</div>
                <div class="corrected">✅ 纠正：[正确内容]</div>
                <div class="analysis">📖 专家分析：[详细分析]</div>
            </div>
        </div>
        
        <!-- 3. 关键欠缺 -->
        <div class="section">
            <h2>⚠️ 关键欠缺</h2>
            <div class="insight-box">
                <h4>欠缺 1：[欠缺名称]</h4>
                <ul>
                    <li><strong>问题</strong>：[描述]</li>
                    <li><strong>风险</strong>：[影响]</li>
                    <li><strong>建议</strong>：[解决方案]</li>
                </ul>
            </div>
        </div>
        
        <!-- 4. 知识架构图 -->
        <div class="section">
            <h2>🗺️ 知识架构图</h2>
            <div class="framework-box">
                <h4>[主题] 完整知识体系</h4>
                <div class="mermaid">
graph TB
    [ Mermaid 思维导图]
                </div>
            </div>
        </div>
        
        <!-- 5. 完整对比表 -->
        <div class="section">
            <h2>📋 完整对比表</h2>
            <table class="comparison-table">
                [对比表格]
            </table>
        </div>
        
        <!-- 6. 专家建议框架 -->
        <div class="section">
            <h2>🎯 专家建议框架</h2>
            <div class="action-framework">
                <h4>[主题] 完整框架（建议版）</h4>
                <div class="action-grid">
                    [6 大模块建议]
                </div>
            </div>
        </div>
        
        <!-- 7. 决策树 -->
        <div class="section">
            <h2>🌳 决策树</h2>
            <div class="mermaid">
                [判断流程图]
            </div>
        </div>
        
        <!-- 8. 专家总结 -->
        <div class="section">
            <h2>📝 专家总结</h2>
            <div class="expert-verdict">
                <h3>🎯 总体评价</h3>
                <p>优点、缺点、建议</p>
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({ startOnLoad: true });
    </script>
</body>
</html>
```

---

## 💡 使用示例

### 示例 1：供应链管理
```
主题：委外 BOM 物料管理
评分：70 分
错误：C 件定义错误、毛需求规则缺失
欠缺：质量责任、交付风险、成本核算、变更管理
架构图：物料分类→需求计算→释放规则→缺失模块
```

### 示例 2：AI 工具使用
```
主题：提示词工程
评分：85 分
错误：无
欠缺：缺少评估标准、缺少迭代流程
架构图：角色设定→任务描述→约束条件→输出格式
```

### 示例 3：技术技能
```
主题：PowerShell 脚本编写
评分：60 分
错误：编码处理不当
欠缺：错误处理、日志记录、参数验证
架构图：参数解析→主逻辑→错误处理→日志输出
```

---

## 🎨 设计规范

### 颜色方案
- **主色**: #667eea → #764ba2（紫色渐变）
- **成功**: #28a745（绿色）
- **警告**: #ffc107（黄色）
- **错误**: #dc3545（红色）
- **信息**: #17a2b8（蓝色）

### 字体
- **标题**: Microsoft YaHei, 36px
- **正文**: Microsoft YaHei, 15px
- **代码**: Consolas, 14px

### 布局
- **容器**: 最大宽度 1800px，居中
- **卡片**: 圆角 15px，阴影 0 20px 60px
- **间距**: 50px（section）、25px（内部）

---

## 📋 检查清单

创建专家评点前，确认：

- [ ] 已阅读完整原文
- [ ] 已识别所有错误
- [ ] 已列出关键欠缺
- [ ] 已绘制知识架构图
- [ ] 已提供行动建议
- [ ] 已给出总体评分
- [ ] HTML 格式正确
- [ ] Mermaid 图表可渲染
- [ ] 文件命名规范
- [ ] 保存到正确领域目录

---

## 🔄 更新记录

| 日期 | 版本 | 变更内容 | 负责人 |
|------|------|----------|--------|
| 2026-03-05 | v1.0 | 初始版本，基于 BOM 评点案例 | 阿福 |

---

_本模板由阿福创建，用于标准化专家评点输出_
