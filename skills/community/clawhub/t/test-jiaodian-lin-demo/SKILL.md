---
name: test-jiaodian-lin-demo
description: 收费技能示例模板 - 带授权验证，演示如何在 ClawHub 发布付费技能
license:
---

# 收费技能示例 (test-jiaodian-lin-demo)

这是一个演示**如何在 ClawHub 发布收费技能**的模板。展示了授权验证的实现方式。

## 商业模式

- **技能本身公开免费，但核心功能需要有效的授权码
- 用户购买后获得授权码，通过环境变量配置即可使用
- 支持单用户授权，验证通过才能使用完整功能

## 配置方式

```bash
# 设置授权码（购买后获得）
export SKILL_LICENSE_KEY=your-purchased-license-key
