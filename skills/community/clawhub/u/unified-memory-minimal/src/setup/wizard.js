/**
 * src/setup/wizard.js
 * Auto-Setup 向导 - 交互式配置
 * 用户运行: openclaw skill run unified-memory setup
 */

import { createInterface } from 'readline';
import { writeFileSync, existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { config } from '../config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const MEMORY_DIR = config.memoryDir;

export class SetupWizard {
  constructor() {
    this.rl = null;
  }

  question(query) {
    return new Promise(resolve => {
      this.rl.question(`${query}\n> `, answer => {
        resolve(answer.trim());
      });
    });
  }

  async run() {
    console.log('\n🧠 Unified Memory Phase 3 Setup Wizard\n' + '='.repeat(40) + '\n');

    // 1. 搜索后端选择
    console.log('【1/5】选择搜索后端');
    console.log('  1) BM25+Vector (默认，无需额外依赖)');
    console.log('  2) QMD (推荐，$0 API 成本，本地混合搜索)\n');
    const searchBackend = await this.question('请选择 (1/2)，直接回车默认 1:') || '1';

    // 2. QMD 集合配置（如果选了 QMD）
    let qmdCollections = [];
    if (searchBackend === '2') {
      console.log('\n【可选】QMD 集合（直接回车使用默认集合）:');
      console.log('  workspace, daily-logs, projects, intelligence');
      const cols = await this.question('多个集合用逗号分隔:');
      qmdCollections = cols 
        ? cols.split(',').map(c => c.trim()).filter(Boolean)
        : ['workspace', 'daily-logs', 'projects', 'intelligence'];
    }

    // 3. Git 集成
    console.log('\n【2/5】Git 集成');
    console.log('  启用后记忆自动版本化，可推送/拉取到远程仓库');
    const gitAns = await this.question('是否启用 Git 集成? (y/N):');
    const gitEnabled = gitAns.toLowerCase() === 'y';
    let gitRemote = '';
    if (gitEnabled) {
      gitRemote = await this.question('  远程仓库 URL (可选，直接回车跳过):');
    }

    // 4. 云备份
    console.log('\n【3/5】云备份');
    console.log('  跨设备同步记忆（可选）');
    const cloudAns = await this.question('是否启用云备份? (y/N):');
    const cloudEnabled = cloudAns.toLowerCase() === 'y';
    let cloudProvider = 'supermemory';
    let cloudApiKey = '';

    if (cloudEnabled) {
      console.log('  1) SuperMemory (推荐)');
      console.log('  2) Custom REST API');
      const provAns = await this.question('请选择 (1/2):');
      cloudProvider = provAns === '2' ? 'custom' : 'supermemory';
      cloudApiKey = await this.question(`  API Key (${cloudProvider}):`);
    }

    // 5. Weibull 衰减参数
    console.log('\n【4/5】Weibull 衰减模型参数（高级）');
    console.log('  shape: 形状参数 (1.0-3.0)，越大记忆越持久，默认 1.5');
    console.log('  scale: 尺度参数 (天数)，越大衰减越慢，默认 30');
    const shapeAns = await this.question('shape (直接回车默认 1.5):');
    const scaleAns = await this.question('scale (直接回车默认 30):');

    const shape = parseFloat(shapeAns) || 1.5;
    const scale = parseFloat(scaleAns) || 30;

    // 生成配置
    const newConfig = {
      search: {
        backend: searchBackend === '2' ? 'qmd' : 'bm25',
      },
      qmd: searchBackend === '2' ? {
        enabled: true,
        collections: qmdCollections,
      } : { enabled: false },
      git: {
        enabled: gitEnabled,
        repo_path: gitEnabled ? join(MEMORY_DIR, '.git-repo') : null,
        remote_url: gitRemote || null,
      },
      cloud: {
        enabled: cloudEnabled,
        provider: cloudProvider,
        ...(cloudApiKey ? { api_key: cloudApiKey } : {}),
      },
      weibull_decay: { shape, scale },
    };

    // 保存
    const configPath = join(MEMORY_DIR, 'config.json');
    const existing = existsSync(configPath) 
      ? JSON.parse(readFileSync(configPath, 'utf-8')) 
      : {};

    const merged = { ...existing, ...newConfig };
    writeFileSync(configPath, JSON.stringify(merged, null, 2));

    console.log('\n' + '='.repeat(40));
    console.log('✅ 配置已保存到:', configPath);
    console.log('\n配置预览:');
    console.log(JSON.stringify(merged, null, 2));
    console.log('\n下一步:');
    console.log('  重启 unified-memory 服务使配置生效');
    console.log('  或运行: openclaw skill run unified-memory setup 重新配置\n');
  }

  close() {
    if (this.rl) {
      this.rl.close();
    }
  }
}

// CLI 入口
if (import.meta.url === `file://${process.argv[1]}`) {
  const wizard = new SetupWizard();
  wizard.rl = createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  wizard.run()
    .catch(console.error)
    .finally(() => wizard.close());
}
