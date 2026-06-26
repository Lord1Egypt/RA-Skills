# Word Reader 技能发布指南

## 🚀 发布到 ClawHub

### 1. 准备工作

#### 确保技能完整
- [ ] SKILL.md 文件完整且格式正确
- [ ] 脚本功能正常
- [ ] 安装脚本工作正常
- [ ] README.md 说明清晰
- [ ] 所有依赖已在 SKILL.md 中声明

#### 环境准备
```bash
# 安装 ClawHub CLI
npm install -g clawhub
# 或
pnpm add -g clawhub
```

#### 登录 ClawHub
```bash
# 登录（会打开浏览器进行 OAuth 认证）
clawhub login

# 验证登录状态
clawhub whoami
```

> **注意**：GitHub 账号需要注册满一周才能发布技能

### 2. 发布流程

#### 检查技能
```bash
# 验证技能结构
clawhub validate ./word-reader
```

#### 发布技能
```bash
clawhub publish ./word-reader \
  --slug word-reader \
  --name "Word Reader" \
  --version 1.0.0 \
  --changelog "支持 .docx 和 .doc 格式的 Word 文档读取，提取文本、表格、元数据等" \
  --tags document,word,office,text-extraction,reader,parsing \
  --license MIT \
  --visibility public
```

#### 参数说明
- `--slug`: URL 友好的唯一标识符
- `--name`: 技能显示名称
- `--version`: 遵循语义化版本控制
- `--changelog`: 版本变更说明
- `--tags`: 搜索标签（逗号分隔）
- `--license`: 许可证类型
- `--visibility`: public/private

### 3. 发布后操作

#### 验证发布
```bash
# 查看已发布的技能
clawhub search word-reader

# 安装测试
clawhub install word-reader-test
```

#### 分享技能
- 技能将在 `https://clawhub.com/skills/word-reader` 可见
- 其他用户可通过 `clawhub install word-reader` 安装

### 4. 版本管理

#### 更新技能
```bash
# 修改技能后更新版本号
clawhub publish ./word-reader --version 1.0.1 --changelog "修复了某些文档格式的解析问题"
```

#### 批量操作
```bash
# 同步所有技能
clawhub sync --all

# 发布并标记
clawhub publish ./word-reader --tags latest,stable
```

### 5. 自动化发布

#### GitHub Actions 示例
```yaml
name: Publish Skill
on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install ClawHub CLI
        run: npm install -g clawhub
        
      - name: Login to ClawHub
        run: echo "${{ secrets.CLAWHUB_TOKEN }}" | clawhub login --token
          
      - name: Publish Skill
        run: |
          clawhub publish ./skills/word-reader \
            --slug word-reader \
            --version ${{ github.ref_name }} \
            --changelog "Published from GitHub Actions"
```

### 6. 发布注意事项

#### 必须遵守的规则
- [ ] 技能名称不能与其他技能冲突
- [ ] 版本号遵循 SemVer 规范
- [ ] changelog 清晰描述变更
- [ ] 代码无安全漏洞
- [ ] 许可证声明清晰

#### 最佳实践
- [ ] 发布前充分测试
- [ ] 提供清晰的使用示例
- [ ] 维护更新日志
- [ ] 及时修复问题
- [ ] 关注用户反馈

### 7. 故障排除

#### 常见问题
```bash
# 验证发布权限
clawhub whoami

# 检查技能格式
clawhub validate ./word-reader

# 查看详细错误信息
clawhub publish ./word-reader --verbose
```

#### 重新发布
如果发布失败，可以：
1. 修正问题
2. 增加版本号
3. 重新发布

### 8. 维护指南

#### 监控使用情况
- 定期查看下载统计
- 关注用户反馈
- 及时修复问题

#### 更新策略
- 重要修复：紧急发布补丁版本
- 新功能：发布次版本号
- 重大变更：发布主版本号

现在你的 Word Reader 技能已经准备好发布到 ClawHub 了！