#!/usr/bin/env node
/**
 * wecom-deep-op 使用示例
 *
 * 运行前请确保已配置环境变量或 mcporter.json
 *
 * 环境变量示例：
 *   export WECOM_DOC_BASE_URL="https://...?uaKey=YOUR_KEY"
 *   export WECOM_SCHEDULE_BASE_URL="https://...?uaKey=YOUR_KEY"
 *   ...
 */

import {
  doc_create,
  doc_get,
  doc_edit,
  schedule_create,
  schedule_list,
  meeting_create,
  todo_create,
  contact_search
} from '../src/index.ts';

async function main() {
  console.log('=== wecom-deep-op 使用示例 ===\n');

  // 1. 健康检查
  console.log('1. 检查服务状态...');
  const ping = await (await import('../src/index.ts')).ping();
  console.log(JSON.stringify(ping, null, 2));

  // 2. 创建文档
  console.log('\n2. 创建文档...');
  const doc = await doc_create(3, 'AI战略规划会议纪要');
  console.log('创建成功:', doc);
  if (doc.errcode === 0 && doc.docid) {
    const docid = doc.docid;

    // 3. 编辑文档
    console.log('\n3. 编辑文档...');
    const editResult = await doc_edit(docid, '# 会议纪要\n\n## 参会人员\n- 张三\n- 李四\n\n## 决议\n1. 推进AI项目\n2. 下周再会');
    console.log('编辑结果:', editResult);

    // 4. 读取文档
    console.log('\n4. 读取文档（首次调用）...');
    const getInit = await doc_get(docid);
    console.log('任务ID:', getInit.task_id, '完成?', getInit.task_done);

    if (!getInit.task_done && getInit.task_id) {
      console.log('等待导出完成...');
      await new Promise(resolve => setTimeout(resolve, 3000));

      const getResult = await doc_get(docid, undefined, getInit.task_id);
      console.log('导出完成:', !!getResult.content);
      console.log('内容预览:', getResult.content?.substring(0, 200) + '...');
    }
  }

  // 5. 搜索联系人
  console.log('\n5. 搜索联系人 "张三"...');
  const searchResult = await contact_search('张三');
  console.log(`找到 ${searchResult.matched_count} 个结果:`);
  searchResult.userlist.forEach(u => console.log(`  - ${u.name} (${u.userid})`));

  // 6. 创建日程（示例）
  console.log('\n6. 创建日程（示例，实际执行需取消注释）...');
  /*
  const schedule = await schedule_create({
    summary: '项目评审会',
    start_time: '2026-03-25 14:00:00',
    end_time: '2026-03-25 16:00:00',
    location: '线上会议',
    description: '讨论Q1项目进展',
    attendees: ['zhangsan']
  });
  console.log('日程创建:', schedule);
  */

  console.log('\n=== 示例执行完毕 ===');
}

main().catch(console.error);
