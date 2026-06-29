# ClawHub 安全审计检查清单

本文档记录了 ClawHub 发布时常见的安全审计问题和修复方法，供后续 Skill 开发参考。

## 审计维度

ClawHub 使用 NVIDIA SkillSpector 进行安全扫描，主要检查以下维度：

| 维度 | 说明 |
|------|------|
| Vulnerability Patterns | 恶意软件、数据泄露 |
| Excessive Agency | 不受限制的工具访问、自主决策 |
| Prompt Injection | 指令覆盖、隐藏指令 |
| Privilege Escalation | 过度权限、凭证访问 |
| Supply Chain | 未固定依赖、外部脚本获取 |
| Context-Inappropriate Capability | 不当能力（歧视、隐私侵犯） |
| Missing User Warnings | 缺少隐私警告、使用声明 |

## 常见问题及修复

### 1. 歧视性评分逻辑

**问题**：基于学校名称（985/211）、性别、年龄等非能力因素进行加分或减分

**示例（错误）**：
```python
top_schools = ['清华', '北大', '浙大', '复旦', '上交', '中科大']
if any(s in school for s in top_schools):
    score += 10
```

**修复**：改为基于客观能力指标
```python
# 仅评估是否有完整教育背景，不基于学校名称
if 'education' in resume and resume['education']:
    edu_count = len(resume['education'])
    if edu_count > 0:
        score += 10
```

**原则**：只评估与岗位要求直接相关的技能和经验

### 2. 主观判断缺乏证据

**问题**：通过简单关键词匹配推断软技能（沟通能力、团队协作等）

**示例（错误）**：
```python
if '沟通' in resume_text:
    strengths.append("具备沟通协调能力")
```

**修复**：提高匹配标准，要求明确证据
```python
# 需要同时出现多个相关关键词
if '沟通' in resume_text and ('客户' in resume_text or '协调' in resume_text or '汇报' in resume_text):
    strengths.append("简历中提到沟通协调相关经验")
```

**附加措施**：添加免责声明
```python
details.append("⚠️ 注意：文化匹配评估仅为参考，需通过面试进一步验证")
```

### 3. 缺少隐私警告

**问题**：处理个人敏感信息（简历、求职数据）但没有隐私声明

**修复**：在 SKILL.md 和 README.md 中添加以下内容：

```markdown
## ⚠️ 重要声明

### 隐私与合规

本技能涉及处理个人敏感信息，使用时请遵守以下原则：

1. **数据最小化**：仅收集与岗位匹配直接相关的必要信息
2. **知情同意**：处理他人简历前，应获得数据主体的明确同意
3. **数据安全**：妥善保管个人信息，处理完成后及时删除
4. **合规使用**：遵守《个人信息保护法》等数据保护法规

### 决策辅助声明

**本工具仅作为决策辅助参考，不应作为自动化决策的唯一依据：**

- 所有决策应由人类审核者最终确认
- 建议结合多种评估方式

### 公平性承诺

本工具已移除基于学校名称、性别、年龄等非能力因素的歧视性评分：
- 不基于毕业院校进行加分或减分
- 不基于性别、年龄等受保护特征进行评估
- 仅评估与岗位要求直接相关的技能和经验
```

### 4. 外部平台引用

**问题**：包含 Twitter、Facebook、Instagram 等境外平台推广内容

**修复**：改为国内技术社区或泛化表述
```markdown
# 错误
- 社媒分享（Twitter、微博、掘金等）

# 正确
- 技术社区分享（掘金、CSDN、知乎等）
- 社媒分享
```

**检查方法**：
```bash
grep -r -i "twitter\|facebook\|instagram\|youtube\|telegram\|reddit" ./
```

### 5. 代码示例导入缺失

**问题**：README 中的示例代码使用了未导入的函数

**示例（错误）**：
```python
from scripts.matcher import TalentMatcher
result = matcher.match(resume_to_dict(resume), jd_to_dict(jd))  # resume_to_dict 未导入
```

**修复**：补齐导入
```python
from scripts.matcher import TalentMatcher, match_to_dict
from scripts.resume_parser import resume_to_dict
from scripts.job_analyzer import jd_to_dict
```

### 6. self 调用模块级函数

**问题**：在类方法中使用 `self.func()` 调用模块级函数

**示例（错误）**：
```python
def some_method(self):
    result = self._helper_function(data)  # _helper_function 是模块级函数
```

**修复**：去掉 self
```python
def some_method(self):
    result = _helper_function(data)
```

## 发布前检查清单

- [ ] 无歧视性评分（学校、性别、年龄）
- [ ] 软技能评估有明确证据支持
- [ ] 包含隐私与合规声明
- [ ] 包含决策辅助声明
- [ ] 无境外平台推广引用
- [ ] 代码示例导入完整
- [ ] 无 self 调用模块级函数
- [ ] 无 __pycache__ 或 .pyc 文件
- [ ] Python 脚本语法检查通过
- [ ] SKILL.md 格式正确（YAML frontmatter）
