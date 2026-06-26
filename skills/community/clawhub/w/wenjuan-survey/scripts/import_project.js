#!/usr/bin/env node
/**
 * 问卷网项目导入工具
 * 通过 JSON 导入项目数据
 */

const { resolveAccessToken } = require('./token_store');
const { WENJUAN_HOST } = require('./api_config');
const { importProject, pollImportStatus } = require('./import_project_api');
const { loadProjectFromFile } = require('./project_file_loader');

/** 从本地文件读取 JWT（逻辑见 token_store.js） */
async function getToken() {
  const t = await resolveAccessToken();
  return t || '';
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);

  let filePath = null;
  let outputJson = false;
  /** 默认 true：导入成功后自动发布（与 workflow_create_and_publish 一致）。仅想留在「编辑中」时用 --no-publish */
  let autoPublish = true;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if ((arg === '-f' || arg === '--file') && i + 1 < args.length) {
      filePath = args[++i];
    } else if (arg === '--json') {
      outputJson = true;
    } else if (arg === '--no-publish') {
      autoPublish = false;
    } else if (arg === '-h' || arg === '--help') {
      showHelp();
      process.exit(0);
    }
  }

  if (!filePath) {
    console.error('错误: 必须提供项目文件路径 (-f)');
    process.exit(1);
  }

  const token = await getToken();
  if (!token) {
    console.error('错误: 未找到登录凭证，请先运行 login_auto.js 登录');
    process.exit(1);
  }

  try {
    const projectData = await loadProjectFromFile(filePath);

    console.log('📂 正在导入项目...');
    console.log(`   标题: ${projectData.title || '未命名'}`);
    console.log(`   题目数量: ${(projectData.question_list || projectData.questions || []).length}`);

    // 提交导入请求
    const result = await importProject(projectData, token);

    if (result.error) {
      console.error(`❌ ${result.error}`);
      process.exit(1);
    }

    if (result.status_code !== 1) {
      const errMsg = result.err_msg || result.message || '未知错误';
      console.error(`❌ 导入失败: ${errMsg}`);
      process.exit(1);
    }

    const fingerprint = result.data && result.data.fingerprint;
    if (!fingerprint) {
      console.error('❌ 未获取到 fingerprint');
      process.exit(1);
    }

    // 轮询导入状态
    const statusResult = await pollImportStatus(fingerprint, token);

    if (!statusResult.success) {
      console.error(`❌ ${statusResult.message}`);
      process.exit(1);
    }

    console.log('✅ 项目导入成功！');
    console.log(`   项目ID: ${statusResult.project_id}`);
    if (statusResult.short_id) {
      console.log(`   短链(导入阶段): ${WENJUAN_HOST}/s/${statusResult.short_id}`);
    }

    let publishOutcome = null;
    if (autoPublish) {
      const { publishProjectFullFlow } = require('./workflow_create_and_publish.js');
      publishOutcome = await publishProjectFullFlow(statusResult.project_id);
      if (!publishOutcome.success) {
        console.error(`\n❌ 自动发布失败: ${publishOutcome.error}`);
        if (publishOutcome.reason) {
          console.error(`   原因: ${publishOutcome.reason}`);
        }
        console.error('   项目已导入，可登录问卷网手动发布，或运行: node scripts/publish.js');
        process.exit(1);
      }
    }

    if (outputJson) {
      console.log(JSON.stringify({ import: statusResult, publish: publishOutcome }, null, 2));
    } else if (autoPublish && publishOutcome && publishOutcome.success) {
      console.log('\n✅ 已自动发布（收集中）');
      if (publishOutcome.short_id) {
        console.log(`   答题链接: ${WENJUAN_HOST}/s/${publishOutcome.short_id}`);
      }
    } else if (!autoPublish) {
      console.log('\n💡 已跳过发布（--no-publish），项目处于编辑中，请手动在问卷网点击发布。');
    }
  } catch (error) {
    if (error.code === 'ENOENT') {
      console.error(`❌ 文件不存在: ${filePath}`);
    } else if (error instanceof SyntaxError) {
      console.error(`❌ JSON解析错误: ${error.message}`);
    } else {
      console.error(`❌ 错误: ${error.message}`);
    }
    process.exit(1);
  }
}

function showHelp() {
  console.log(`
问卷网项目导入工具

用法: node import_project.js -f <file-path> [选项]

选项:
  -f, --file <path>       项目JSON文件路径（必填）
  --no-publish            仅导入到「编辑中」，不调用发布接口
  --json                  输出 import + publish 原始 JSON
  -h, --help              显示帮助信息

说明:
  默认会在导入成功后自动发布（与 workflow_create_and_publish.js 相同逻辑，含审核轮询）。
  若只需「创建草稿」，请加 --no-publish。

示例:
  # 导入并自动发布（默认）
  node import_project.js -f project.json

  # 只导入，不发布
  node import_project.js -f project.json --no-publish
`);
}

// 导出模块
module.exports = {
  importProject,
  pollImportStatus,
};

// 如果是直接运行
if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
