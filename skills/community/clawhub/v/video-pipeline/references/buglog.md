# video-pipeline BUG全量记录

更新时间: 2026-05-05 00:49

---

## 架构级BUG

### BUG-004: gen_outline输出10节课而非1节课
- 发现: 05-04 16:11
- 现象: 生成lesson_01~lesson_10共10个子目录
- 根因: 大纲模板定义为"课程系列"而非"单节课slide列表"，数据契约不清晰
- 修复: 重写大纲模板，约束为1节课5-7个slide

### BUG-008: 输出路径不统一
- 发现: 05-04 16:11
- 现象: 各脚本输出路径不一致（Skill目录/项目目录/子目录）
- 根因: 没有统一的--project参数约定
- 修复: 所有脚本统一--project和--lesson参数

### BUG-009: gen_tts生成55个mp3
- 发现: 05-04 16:11
- 现象: 55个audio文件（应5个）
- 根因: 承接BUG-004，10节课×5slide=55
- 修复: 修复outline后自然正确

### BUG-015: 模板医疗内容残留（正则匹配失败）
- 发现: 05-04 22:05
- 现象: 制造业视频TSX中仍有9个医疗词（AI+医疗、上海中山医院等）
- 根因: gen_tsx.py的replace_template_placeholders用正则匹配医疗行业具体文字，对其他行业不匹配→残留
- 修复: 6个模板全部改为占位符（__TITLE__/__BULLET_1__等），替换逻辑改为str.replace

### BUG-016: Composition TSX语法错误（f-string隐式拼接）
- 发现: 05-04 22:51
- 现象: 生成的Composition文件有`}}">`语法错误，Remotion编译失败
- 根因: pipeline.py的content构建用f-string与普通字符串隐式拼接，`}}>` 在某些情况变成 `}}">`
- 修复: 改用列表拼接（content_lines + join）替代隐式字符串拼接

### BUG-017: Root.tsx LESSONS数组注册遗漏
- 发现: 05-04 22:51
- 现象: import了Composition但没加到LESSONS数组→Remotion找不到composition ID
- 根因: register_in_root_tsx只在最后一个import后插入import行，但插入LESSONS entry的逻辑用`\n];`替换，可能匹配不到
- 修复: 修复注册逻辑

### BUG-018: 幽灵Composition（残留slides目录）
- 发现: 05-04 23:29
- 现象: 渲染失败，找不到`using_ai_to_improve_teaching_efficiency/Slide001`
- 根因: 之前测试留下的slides目录（有slide_map.json但无TSX），generate_compositions.py扫描到后生成了Composition
- 修复三处:
  1. generate_compositions.py加TSX文件存在检查
  2. pipeline.py注册前先调用generate_compositions.py同步
  3. 清理脚本同时删slides+Composition+audio+html

---

## 脚本级BUG

### BUG-001: --lesson参数类型写死int
- 发现: 05-04 15:44
- 修复: type=int改为type=str

### BUG-002: :02d格式化不兼容字符串
- 发现: 05-04 15:46
- 修复: 去掉:02d格式化

### BUG-003: HTML输出路径不统一
- 发现: 05-04 15:50
- 修复: 参数传递--project

### BUG-006: gen_compositions未识别自定义课名
- 发现: 05-04 15:20
- 修复: 添加非数字课号支持

### BUG-007: Composition durations变量引用错误
- 发现: 05-04 14:40
- 修复: 从slide_map读取

### BUG-019: --config src/config.ts不存在
- 发现: 05-04 22:55
- 现象: pipeline.py渲染步骤传了`--config src/config.ts`但文件不存在
- 修复: 注释掉该参数

### BUG-020: Windows asyncio事件循环兼容
- 发现: 05-04 22:55
- 现象: TTS在subprocess中可能因事件循环问题导致文件未写入
- 修复: gen_tts.py加`asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())`

---

## 数据/内容级BUG

### BUG-005: narration输出到子目录
- 发现: 05-04 16:11
- 修复: 修复outline后自然归位

### BUG-010: LLM调用是TODO占位
- 发现: 05-04 14:40
- 修复: 接入DashScope qwen-max API

### BUG-013: HTML硬编码行业内容
- 发现: 05-04 21:43
- 现象: 制造业视频显示"智慧医疗新时代"
- 修复: 替换为动态占位符__COURSE_SUBTITLE__/__COURSE_SERIES__

### BUG-014: 缓存残留导致内容串台
- 发现: 05-04 21:45
- 修复: 4个脚本加[CACHE]清除环节

### BUG-021: 数据标签全是85%
- 发现: 05-04 23:34
- 现象: 所有数据卡片显示"85%"，三张卡片完全相同
- 根因: gen_tsx.py默认值硬编码`"85%"`，且3个卡片用同一个numbers[0]
- 修复: 默认值改为空，占位符拆分为__DATA_NUMBER_1/2/3__

### BUG-022: LLM编造虚构数字（12核REJECT）
- 发现: 05-04 23:46
- 现象: narration中的"95%"、"2000万"等数字是LLM编造，无数据源支撑
- 根因: gen_narration.py prompt让LLM同时承担"写文案"和"提供数据"，职责错配
- 12核裁定: 5核一致REJECT
- 修复: 
  1. prompt禁止编造具体数字，改为趋势性描述
  2. 数据卡片改为趋势图标（↑↓→）
  3. 后续方案：数据-叙述分离架构

### BUG-023: 趋势图标固化（12核二次审核）
- 发现: 05-05 00:07
- 现象: 每个slide都有相同的3个趋势箭头跳动，不管配音讲什么
- 根因: content_data模板硬编码3个数据卡片，gen_tsx不判断内容类型
- 修复:
  1. 新增3种模板变体（content_text/content_story/content_compare）
  2. gen_tsx加classify_slide_type自动判断
  3. 视觉节奏系统（相邻slide不同模板）
  4. 数据卡片0-3动态

### BUG-024: hook/summary/ending模板空数据卡片
- 发现: 05-05 00:35
- 现象: hook模板有3个空的minWidth:160数据卡片div容器，渲染出空白区域
- 根因: 清TREND占位符时只清了内容文字，没清div容器结构
- 修复: 脚本删除整个minWidth:160数据卡片容器

### BUG-025: summary模板要点内容为空
- 发现: 05-05 00:44
- 现象: 总结页的①②③卡片有结构但内容为空
- 根因: 清TREND占位符时把fontSize:48/26的内容清空了，没用BULLET占位符替代
- 修复: ①②③卡片内容改为__BULLET_1/2/3__

---

## 渲染级BUG

### BUG-011: 视频没更新到桌面
- 发现: 05-04 17:38
- 修复: 脚本加复制步骤

### BUG-012: 50秒黑屏
- 发现: 05-04 17:38
- 根因: Composition duration远大于实际音频总时长
- 修复: calculateMetadata只从slide_map绑定的音频计算

---

### BUG-026: 卡片只有一层文字（完美视频有两层）
- 发现: 05-05 02:40
- 现象: 卡片只有标题一行，完美视频每张卡片有标题(30px)+描述(24px)两层
- 修复: extract_key_points按逗号分割为title+desc，gen_card生成两层div

### BUG-027: 描述行逗号不换行
- 发现: 05-05 02:35
- 现象: 描述文字连成一行，逗号处不换行
- 根因: Python\n在TSX源码里变成实际换行符，React渲染时合并为一行
- 修复: gen_desc_lines函数按逗号拆分为多个独立<div>

### BUG-028: gen_card条件渲染f-string生成无效JSX
- 发现: 05-05 02:49
- 现象: 描述为空时f-string条件渲染缺少闭合</div>
- 修复: 始终输出描述div，空内容显示为空

### BUG-029: 卡片数量固定3，应自适应
- 发现: 05-05 01:44
- 现象: 每页都是3个卡片，视觉重复
- 修复: gen_tsx.py改为动态生成TSX（不用固定模板），卡片数量由narration内容决定

### BUG-030: 完美视频模板固化→gen_tsx v2重做
- 发现: 05-05 01:24
- 现象: 旧模板体系全部删除，从Skill重做
- 修复: gen_tsx.py v2用Python动态生成TSX代码，不再依赖模板文件

## 统计

| 分类 | 数量 | 占比 |
|------|------|------|
| 架构级 | 6 | 24% |
| 脚本级 | 8 | 32% |
| 数据/内容级 | 7 | 28% |
| 渲染级 | 2 | 8% |
| LLM质量 | 2 | 8% |
| 模板/布局级 | 5 | 16% |
| **总计** | **30** | 100% |

## 关键教训

1. **数据契约先行**: 脚本间的输入输出格式必须先定义再编码
2. **不编假数据**: LLM编的数字=虚构，法律+信任双重风险（12核一致REJECT）
3. **模板不能一刀切**: 不同内容类型需要不同视觉布局
4. **清理必须彻底**: 清占位符要连容器结构一起清，否则留空白
5. **根因要挖深**: 表面修3次不如挖到真正根因修1次
6. **全程零干预**: pipeline必须端到端自动，有手动补步骤=不合格
7. **f-string隐式拼接有坑**: 用列表拼接替代，更安全
