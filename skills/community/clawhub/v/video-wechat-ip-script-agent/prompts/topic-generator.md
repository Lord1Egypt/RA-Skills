任务：生成视频号选题

输入变量：
- 行业：{{industry}}
- 内容方向：{{direction}}
- 目标人群：{{targetAudience}}
- 数量：{{count}}
- 偏好风格：{{style}}
- 输出包配置：{{outputProfile}}
- 输出字段：{{outputFields}}

要求：
1. 选题必须贴近真实内容场景
2. 标题可拍、可讲、可口播
3. 避免假大空和鸡汤化表达
4. 优先使用痛点、反差、观点、方法、案例五类切入
5. 每个选题必须包含：
   - title
   - category（痛点/反差/观点/方法/案例）
   - angle
   - targetAudience
6. 输出字段优先按 `topicOutputProfilesConfig[outputProfile]` 执行

{{outputRequirement}}
