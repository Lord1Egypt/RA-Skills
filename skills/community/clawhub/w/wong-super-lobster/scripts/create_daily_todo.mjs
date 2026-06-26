import { Client } from '@larksuiteoapi/node-sdk';

const APP_ID = 'cli_a92115f36af9dcd5';
const APP_SECRET = 'iRuP8Jj8LT5iJlFXTRpbiWJr2yRiBx84';
const USER_OPEN_ID = 'ou_3aed530e2f42a906b704bc474609d7ce';

const client = new Client({
  appId: APP_ID,
  appSecret: APP_SECRET
});

async function main() {
  try {
    console.log('Step 1: Creating document...');
    
    const createRes = await client.docx.document.create({
      data: {
        title: `🦞 每日待办 2026.4.6（6 会议 75 项完整版）`
      }
    });
    
    if (createRes.code !== 0) {
      throw new Error(`Failed to create: ${createRes.msg}`);
    }
    
    const docToken = createRes.data.document.document_id;
    console.log(`✓ Document created: ${docToken}`);
    
    const markdownContent = `# 🦞 每日待办 2026.4.6（6 会议 75 项完整版）

**生成时间**: 2026-04-06 19:55
**数据来源**: 6 个会议纪要（含 4/5 新会议）

---

## 🔥 4/5 新会议（商务与科创项目推进会议）

### 明天（4/7）截止 ⚠️🔴

- [ ] 下午 3 点星火盘项目 → 黄桥、刘玉宝、郭春雄
- [ ] 搭建出海 AI 6S 框架给许美盛 → 郭春雄、黄桥
- [ ] 讨论分工规则 → 所有参会人员
- [ ] 列出工作内容 + 排日程表 → 郭春雄、周宇
- [ ] 飞书权限开放给郭哥和卓依 → 刘玉宝、黄桥

### 后天（4/8）截止

- [ ] 评估付余是否能胜任政企方案撰写 → 冯雄

### 下周二（4/14）前

- [ ] 形成新基建和出海 6S 方案初稿 → 许美盛
- [ ] 约焦总/陈博士沟通合作 → 黄桥、刘玉宝
- [ ] 约科创集团沟通 → 黄桥、刘玉宝

### 需尽快

- [ ] 撰写前海 OPC 集群项目方案 → 许美盛

---

## 会议 1: AI 盒子及 NAS 应用 (3/17)

### 逾期 17 天（3/20）

- [ ] 寄送 K1 开发板样机 → 桥哥
- [ ] 销售人员 3 天内学会装机 → 销售团队
- [ ] 徐东配盒子样品寄出 → 徐东
- [ ] 约九龙数据 Lark 团队吃饭 → 桥哥

### 逾期 10 天（3/27）

- [ ] 撰写 LISTFIVE+ 鸿蒙 NAS 报告 → 桥哥
- [ ] 联系洛可可陈希平 → 桥哥
- [ ] 研究工作站是否好用 → 桥哥

### 持续跟进

- [ ] K1/K3 鸿蒙适配
- [ ] 确定 K3 算力分配策略
- [ ] 推进 3C 认证

---

## 会议 2: AI 业务出海及品牌打造 (3/18)

### 逾期 6 天（3/31）

- [ ] 成立前海公司（蒋总入股 10%-20%） → 桥哥
- [ ] 整理会议录音发送 → 桥哥
- [ ] 预留工位给彭迪 → 桥哥

### 4 月 30 日截止

- [ ] 跟进前海 AI 新基建招投标（5000 万） → 桥哥
- [ ] 龙虾耳机海外众筹方案 → 团队
- [ ] 算力合作洽谈 → 团队
- [ ] 马来西亚算力中心评估 → 团队
- [ ] 港中深 AI 学院联合实验室 → 桥哥
- [ ] 组建海外销售团队 → 杨舒平
- [ ] 太原 AI 文旅项目 → 桥哥

---

## 会议 3: 工作规划与项目推进 (3/23)

### 逾期 6 天⚠️ 紧急（3/31）

- [ ] 市公共服务平台 50 万补贴确认 → 桥哥
- [ ] 推动 CSDN 小智申报 → 桥哥

### 今日到期（4/6）⚠️

- [ ] 龙虾盒子 + 耳机完成并投产 → 桥哥

### 4 月 15 日截止

- [ ] 科创局政策登记 → 桥哥

---

## 会议 4: 门店 C 端 AI 会员体系 (3/23)

### 逾期 10 天（3/27）

- [ ] 科普号 + 达人号运营 → 子怡、曼蕾
- [ ] 盒子贴牌完成 → 郭哥带队
- [ ] 2999 元课程完善 → 周泳彤
- [ ] 采购合同签订 → 俊哥
- [ ] 群聊重新分配 → 谢万里
- [ ] 全员拥有龙虾盒子 → 浩林、禹铭

### 5 月 1 日截止

- [ ] 版权工会 AI 院校报名 → 泳彤协助，浩霖主导

---

## 会议 5: 出海业务 KR 拉齐 (3/27)

### 逾期 6 天（3/31）

- [ ] 补充目标节点任务拆解 → 胡万方
- [ ] 确认海外销售资质 → 胡万方
- [ ] 人员招聘测算 → 胡万方、周宇 → 周宇招聘

### 4 月 30 日截止

- [ ] 跑通 1 个社群 +1 个平台 → 杨舒平

---

## NAS 龙虾产品 P0 任务

- [ ] NAS 版龙虾产品深度分析 → 桥哥
- [ ] 联系 ODM 拿 RK3588 开发板 → 桥哥
- [ ] 部署虾技术验证 → 部署虾
- [ ] 10 个开发者需求访谈 → 桥哥

---

## 本周关键节点（4 月第一周）

- [ ] 确定 NAS 龙虾硬件方案 → 桥哥
- [ ] 完成 NAS 龙虾产品定位文档 → 项目虾
- [ ] Skill 市场开发者招募计划 → 创意虾

---

**整理人**: 龙虾仔 🦞
`;

    console.log('\nStep 2: Converting markdown to blocks...');
    
    const convertRes = await client.docx.document.convert({
      data: {
        content_type: 'markdown',
        content: markdownContent
      }
    });
    
    if (convertRes.code !== 0) {
      throw new Error(`Convert failed: ${convertRes.msg}`);
    }
    
    const blocks = convertRes.data?.blocks || [];
    const firstLevelBlockIds = convertRes.data?.first_level_block_ids || [];
    console.log(`✓ Converted to ${blocks.length} blocks`);
    
    console.log('\nStep 3: Cleaning blocks...');
    
    function omitParentId(block) {
      const { parent_id, ...rest } = block;
      return rest;
    }
    
    const descendants = blocks.map(block => {
      const cleanBlock = omitParentId(block);
      return {
        ...(cleanBlock.block_id ? { block_id: cleanBlock.block_id } : {}),
        ...cleanBlock
      };
    });
    
    console.log(`✓ Cleaned ${descendants.length} blocks`);
    
    console.log('\nStep 4: Inserting blocks...');
    
    const insertRes = await client.docx.documentBlockDescendant.create({
      path: {
        document_id: docToken,
        block_id: docToken
      },
      data: {
        children_id: firstLevelBlockIds,
        descendants: descendants,
        index: -1
      }
    });
    
    if (insertRes.code !== 0) {
      throw new Error(`Insert failed: ${insertRes.msg}`);
    }
    
    console.log('✓ Blocks inserted');
    
    console.log('\nStep 5: Setting permission...');
    
    const permRes = await client.drive.permissionMember.create({
      path: { token: docToken },
      params: {
        type: 'docx',
        need_notification: true
      },
      data: {
        member_type: 'openid',
        member_id: USER_OPEN_ID,
        perm: 'edit'
      }
    });
    
    if (permRes.code !== 0) {
      console.warn(`Permission failed: ${permRes.msg}`);
    } else {
      console.log('✓ Permission set');
    }
    
    console.log('\n✅ Success!\n');
    console.log(`📄 https://tcn2fs3elcq2.feishu.cn/docx/${docToken}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.response?.data) {
      console.error('Response:', JSON.stringify(error.response.data, null, 2));
    }
    process.exit(1);
  }
}

main();
