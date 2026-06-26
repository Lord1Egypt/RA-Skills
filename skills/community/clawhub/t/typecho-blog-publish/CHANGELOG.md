# Typecho 博客发布技能更新日志

## v1.2.0 (2026-03-27)
### 新增功能
- ✅ **智能配图系统**：新增 `smart_image.py` 脚本，基于主题关键词自动搜索 Unsplash 高质量图片
- ✅ **图片上传优化**：`upload_image.py` 支持直接上传到 Typecho 媒体库
- ✅ **日期修复**：发布脚本自动添加正确的 `dateCreated` 字段，避免 1970-01-01 bug
- ✅ **分类兼容**：强制使用默认分类，避免 "分类不存在" 错误
- ✅ **技能文档更新**：完善使用说明和示例

### 修复问题
- 🐛 **图片显示问题**：修复 Markdown→HTML 转换中的图片标签处理
- 🐛 **URL 生成**：确保文章链接正确生成（配合 Typecho 伪静态配置）
- 🐛 **多图叠加**：识别 Typecho 主题可能的多图片显示特性

### 使用建议
1. **智能配图工作流**：
   ```bash
   # 搜索主题相关图片
   python3 smart_image.py "AI 技术 未来"
   
   # 上传到博客
   python3 upload_image.py /tmp/theme_test.jpg
   
   # 在 Markdown 中使用图片 URL
   ![图片描述](http://yuanblog.tk:9980/usr/uploads/2026/03/xxx.jpg)
   ```

2. **文章发布最佳实践**：
   - 使用 Markdown 头部信息（title、tags、date）
   - 图片放在文章开头或相关位置
   - 使用 `--draft` 参数先保存草稿，确认后再发布

## v1.1.0 (2026-03-26)
### 初始版本
- 基础 XML-RPC 发布功能
- Markdown 文件读取和解析
- 草稿模式支持
- 标签管理
- 批量发布工具

## 已知问题
- Typecho 伪静态配置可能导致 `/archives/{id}.html` URL 404，可通过动态 URL `index.php?action=show&id={id}` 访问
- 部分主题可能在文章页显示多张图片（轮播效果），如需调整可修改主题 CSS

---

*维护者：团子 🌟*  
*博客：渊博（http://yuanblog.tk:9980）*  
*技能ID：typecho-blog-publish*