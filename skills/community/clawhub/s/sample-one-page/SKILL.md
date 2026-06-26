---
name: elegant-one-pager-architect
description: >-
  当用户要求整理沟通记录、会议纪要，或需要生成“一页纸汇报”、“高管总结”、“排版卡片”、“导出PDF/图片”时触发。
  该技能将杂乱文本清洗为客观结论，并直接渲染为具备现代感、色彩丰富、使用渐变色区分板块且视觉舒适的HTML瀑布流代码。
---

# 核心动作
按照以下3个步骤处理用户的输入内容。直接输出最终的HTML代码，**禁止输出任何解释性或过渡性文本**。

## Step 1: 事实抽取 (Information Extraction)
从输入文本中提取以下5类信息。若某类信息完全缺失，直接跳过，**严禁自行编造或使用空白占位符**：
1. 核心主题与涉及方（干系人、系统）
2. 最终定论/当前确切状态
3. 核心推导逻辑/技术过程
4. 量化数据/指标
5. 进度节点/风险/下一步动作

## Step 2: 语言清洗 (Language Sanitization)
- **去口语化**：将聊天记录转换为书面业务语言，保持**客观、折中**的语气。
- **高信噪比**：精准提炼，去除废话。

## Step 3: 动态渲染 (Dynamic Rendering)
将抽取并清洗后的内容代入下方的 HTML 模板中。

**DOM 删减规则：**
- 如果 [核心数据] 与 [进度节点] **同时缺失**，彻底删除包含这两个模块的外部 `<div style="display: flex;">` 容器。
- 如果仅缺失其中一个，删除缺失项对应的子 `<div>`，并保持保留项的 `flex: 1` 属性以占满整行。

**HTML 输出模板（现代色彩渐变版）：**
```html
<div style="background: linear-gradient(145deg, #F8FAFC 0%, #FFFFFF 100%); padding: 40px; border-radius: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #334155; max-width: 850px; margin: 20px auto; box-shadow: 0 10px 40px rgba(0,0,0,0.06); border: 1px solid rgba(255,255,255,0.8); overflow: hidden;">

  <div style="background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%); padding: 20px 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 20px rgba(99,102,241,0.25);">
    <h1 style="font-size: 26px; margin: 0 0 8px 0; color: #FFFFFF; font-weight: 600; letter-spacing: -0.3px;">[提取的核心主题]</h1>
    <p style="font-size: 14px; color: rgba(255,255,255,0.85); margin: 0; font-weight: 400;"><strong>相关方：</strong>[提取的干系人/系统] | <strong>时间：</strong>[当前日期或事件日期]</p>
  </div>

  <div style="background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); border-left: 4px solid #0EA5E9; padding: 18px 25px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 12px rgba(14,165,233,0.08);">
    <h2 style="font-size: 17px; margin: 0 0 12px 0; color: #0369A1; display: flex; align-items: center;">
      <span style="margin-right: 8px;">📍</span>核心结论 / Executive Summary
    </h2>
    <p style="font-size: 15px; line-height: 1.7; margin: 0; color: #475569; font-weight: 500;">[用 2-3 句话客观总结沟通的最终定论或当前状态]</p>
  </div>

  <div style="display: flex; gap: 20px; margin-bottom: 25px;">
    <div style="flex: 1; background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); padding: 20px; border-radius: 10px; border: 1px solid rgba(16,185,129,0.15); box-shadow: 0 2px 12px rgba(16,185,129,0.06);">
      <h3 style="font-size: 15px; margin: 0 0 15px 0; color: #047857; border-bottom: 1px solid rgba(16,185,129,0.2); padding-bottom: 8px; display: flex; align-items: center;">
        <span style="margin-right: 8px;">📊</span>核心数据/量化指标
      </h3>
      <ul style="font-size: 14px; margin: 0; padding-left: 18px; color: #475569; line-height: 1.8;">
        <li>[量化点 1]</li>
        </ul>
    </div>
    <div style="flex: 1; background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); padding: 20px; border-radius: 10px; border: 1px solid rgba(245,158,11,0.15); box-shadow: 0 2px 12px rgba(245,158,11,0.06);">
      <h3 style="font-size: 15px; margin: 0 0 15px 0; color: #B45309; border-bottom: 1px solid rgba(245,158,11,0.2); padding-bottom: 8px; display: flex; align-items: center;">
        <span style="margin-right: 8px;">⏱️</span>进度节点
      </h3>
      <ul style="font-size: 14px; margin: 0; padding-left: 18px; color: #475569; line-height: 1.8;">
        <li>[节点 1及状态]</li>
        </ul>
    </div>
  </div>

  <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); padding: 25px; border-radius: 10px; margin-bottom: 25px; border: 1px solid rgba(203,213,225,0.3); box-shadow: 0 2px 12px rgba(0,0,0,0.02);">
    <h2 style="font-size: 17px; margin: 0 0 18px 0; color: #475569; display: flex; align-items: center;">
      <span style="margin-right: 8px;">🧠</span>核心推导逻辑与过程
    </h2>
    <div style="font-size: 14px; line-height: 1.8; color: #64748B;">
      [使用无序列表或带序号的列表，客观描述决策过程、技术方案或业务链路]
    </div>
  </div>

  <div style="background: linear-gradient(135deg, #FEFCE8 0%, #FEF9C3 100%); padding: 20px 25px; border-radius: 10px; border: 1px solid rgba(234,179,8,0.15); box-shadow: 0 2px 12px rgba(234,179,8,0.06);">
    <h2 style="font-size: 17px; margin: 0 0 15px 0; color: #A16207; display: flex; align-items: center;">
      <span style="margin-right: 8px;">🎯</span>下一步动作 / 风险关注点
    </h2>
    <ul style="font-size: 14px; margin: 0; padding-left: 18px; line-height: 1.8; color: #57534E;">
      <li><strong>[动作/风险1]：</strong>[具体描述与责任边界]</li>
      </ul>
  </div>

</div>
