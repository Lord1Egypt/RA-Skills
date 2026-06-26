# HOT Memory - Day 30

## 代码规范
- 命名：ViewController/Manager/Service 后缀
- Block：必须 weakSelf，strongSelf 判空
- 注释：公开方法 + 复杂逻辑必须注释
- 布局：纯代码，不用 Storyboard

## 项目规范（Tiqmo）
- 网络层：统一用 TQNetworkManager
- 数据库：用 FMDB，不用 CoreData
- 图片加载：用 SDWebImage

## 用户偏好
- 喜欢用 MVC+BLL 架构
- 不喜欢用 Storyboard，纯代码布局
- 代码风格：6段式注释

## 常见错误
- Block 内存泄漏：访问 self 必须用 weakSelf
- 忘记判空：strongSelf 必须判空
- 命名不规范：ViewController 必须加后缀

## 安全规则
- 密码/token/私钥：永不记录
- 用户隐私：脱敏处理
- 删除操作：二次确认
- 生产环境：明确授权

---
*最后更新: 2026-03-30*
*行数: 85/100*
