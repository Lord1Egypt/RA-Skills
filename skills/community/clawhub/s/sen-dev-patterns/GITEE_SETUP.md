# Gitee 发布清单

## 待完成任务

- [ ] 在 Gitee 创建应用获取 Token
  - 地址: https://gitee.com/oauth/applications
  - 权限: projects

- [ ] 运行发布脚本
  ```bash
  cd C:\Users\sen\.codebuddy\skills\sen-dev-patterns
  set GITEE_TOKEN=your_token
  python publish_gitee.py
  ```

- [ ] 验证仓库
  - 访问: https://gitee.com/the13ai/sen-dev-patterns

## 手动发布（无需Token）

1. 访问 https://gitee.com/new
2. 创建新仓库，名称填: `sen-dev-patterns`
3. 创建后运行:
   ```bash
   git remote add gitee https://gitee.com/the13ai/sen-dev-patterns.git
   git push -u gitee master
   ```

## ClawHub 市场

发布到 Gitee 后，可用于国内用户的 Skill 分发。
如需提交到 ClawHub 市场，请访问:
https://clawhub.ai/import?repo=the13ai/sen-dev-patterns
