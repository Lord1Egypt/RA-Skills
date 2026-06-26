#!/usr/bin/env node

/**
 * 微信集成一键安装脚本
 * 基于B站视频《终于可以在微信中和你的 OpenClaw 聊天了，保姆级一键安装教程》
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const readline = require('readline');

console.log('🚀 微信集成一键安装');
console.log('='.repeat(60));
console.log('基于《终于可以在微信中和你的 OpenClaw 聊天了，保姆级一键安装教程》');
console.log('='.repeat(60));

class WeChatInstaller {
  constructor() {
    this.steps = [];
    this.results = [];
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }
  
  async startInstallation() {
    console.log('\n📱 微信集成OpenClaw安装向导');
    console.log('='.repeat(50));
    
    try {
      // 显示安装说明
      await this.showInstructions();
      
      // 确认继续
      const proceed = await this.confirmProceed();
      if (!proceed) {
        console.log('\n安装已取消');
        this.rl.close();
        return;
      }
      
      // 运行安装步骤
      await this.runInstallationSteps();
      
      // 完成安装
      this.completeInstallation();
      
    } catch (error) {
      console.error('\n❌ 安装失败:', error.message);
      this.generateErrorReport(error);
    } finally {
      this.rl.close();
    }
  }
  
  async showInstructions() {
    console.log('\n📖 安装说明:');
    console.log('='.repeat(50));
    
    const instructions = [
      '1. 确保微信已更新到8.0.70或更高版本',
      '2. 确保OpenClaw已安装并运行',
      '3. 准备手机微信用于扫码绑定',
      '4. 安装过程需要网络连接',
      '5. 按照提示完成安装步骤'
    ];
    
    instructions.forEach((instruction, index) => {
      console.log(`   ${index + 1}. ${instruction}`);
    });
    
    console.log('\n🎯 安装目标:');
    console.log('   • 安装微信OpenClaw插件');
    console.log('   • 生成绑定二维码');
    console.log('   • 完成微信授权绑定');
    console.log('   • 在微信中使用OpenClaw');
    
    console.log('\n⏱️  预计时间: 3-5分钟');
    console.log('='.repeat(50));
  }
  
  async confirmProceed() {
    return new Promise((resolve) => {
      this.rl.question('\n是否继续安装？(y/n): ', (answer) => {
        resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
      });
    });
  }
  
  async runInstallationSteps() {
    const steps = [
      {
        name: '检查环境',
        action: async () => {
          console.log('\n1. 🔍 检查系统环境...');
          return await this.checkEnvironment();
        }
      },
      {
        name: '安装微信插件',
        action: async () => {
          console.log('\n2. 📦 安装微信OpenClaw插件...');
          return await this.installWeChatPlugin();
        }
      },
      {
        name: '配置插件',
        action: async () => {
          console.log('\n3. ⚙️  配置微信插件...');
          return await this.configurePlugin();
        }
      },
      {
        name: '生成二维码',
        action: async () => {
          console.log('\n4. 📱 生成微信绑定二维码...');
          return await this.generateQRCode();
        }
      },
      {
        name: '验证安装',
        action: async () => {
          console.log('\n5. ✅ 验证安装结果...');
          return await this.verifyInstallation();
        }
      }
    ];
    
    for (const step of steps) {
      console.log(`\n🔧 步骤: ${step.name}`);
      console.log('-'.repeat(40));
      
      try {
        const result = await step.action();
        this.steps.push({
          step: step.name,
          status: 'completed',
          result
        });
        
        console.log(`   ✅ ${step.name}完成`);
      } catch (error) {
        console.log(`   ❌ ${step.name}失败: ${error.message}`);
        this.steps.push({
          step: step.name,
          status: 'failed',
          error: error.message
        });
        
        // 提供备用方案
        await this.provideFallbackSolution(step.name, error);
      }
    }
  }
  
  async checkEnvironment() {
    const checks = [
      {
        name: 'OpenClaw版本',
        command: 'openclaw --version',
        success: (output) => output.includes('OpenClaw'),
        error: 'OpenClaw未安装'
      },
      {
        name: '网关状态',
        command: 'openclaw gateway status',
        success: (output) => output.includes('running') || output.includes('active'),
        error: 'OpenClaw网关未运行'
      },
      {
        name: 'Node.js版本',
        command: 'node --version',
        success: (output) => {
          const version = output.replace('v', '');
          const major = parseInt(version.split('.')[0]);
          return major >= 18;
        },
        error: '需要Node.js 18或更高版本'
      }
    ];
    
    for (const check of checks) {
      try {
        const output = await this.executeCommand(check.command);
        const passed = check.success(output);
        
        if (!passed) {
          throw new Error(check.error);
        }
        
        console.log(`   ✅ ${check.name}: 通过`);
      } catch (error) {
        throw new Error(`${check.name}检查失败: ${error.message}`);
      }
    }
    
    return '环境检查通过';
  }
  
  async installWeChatPlugin() {
    console.log('   正在安装微信插件...');
    
    // 尝试官方安装命令
    const installCommands = [
      'npx -y @tencent-weixin/openclaw-weixin-cli@latest install',
      'openclaw plugins install "@tencent-weixin/openclaw-weixin"'
    ];
    
    let lastError;
    
    for (const command of installCommands) {
      try {
        console.log(`   尝试命令: ${command}`);
        const output = await this.executeCommand(command, 30000); // 30秒超时
        
        if (output.includes('success') || output.includes('installed') || output.includes('二维码')) {
          console.log(`   ✅ 插件安装成功`);
          return { command, output: output.substring(0, 200) + '...' };
        }
        
        lastError = new Error(`安装命令未返回成功状态: ${command}`);
      } catch (error) {
        lastError = error;
        console.log(`   ⚠️  命令失败: ${command}`);
      }
    }
    
    // 如果所有命令都失败，抛出最后一个错误
    throw lastError || new Error('所有安装命令都失败');
  }
  
  async configurePlugin() {
    console.log('   配置微信插件...');
    
    const configCommands = [
      'openclaw config set plugins.entries.openclaw-weixin.enabled true',
      'openclaw config set channels.weixin.enabled true'
    ];
    
    for (const command of configCommands) {
      try {
        await this.executeCommand(command);
        console.log(`   ✅ 配置命令执行: ${command}`);
      } catch (error) {
        console.log(`   ⚠️  配置命令跳过: ${command} - ${error.message}`);
      }
    }
    
    return '插件配置完成';
  }
  
  async generateQRCode() {
    console.log('   生成微信绑定二维码...');
    
    // 尝试生成二维码
    const qrCommands = [
      'openclaw channels login --channel openclaw-weixin',
      'openclaw pairing create --channel weixin'
    ];
    
    let qrOutput = '';
    
    for (const command of qrCommands) {
      try {
        const output = await this.executeCommand(command, 15000);
        qrOutput = output;
        
        if (output.includes('二维码') || output.includes('QR') || output.includes('scan')) {
          console.log(`   ✅ 二维码生成成功`);
          console.log('\n' + '='.repeat(50));
          console.log('📱 请使用微信扫描二维码完成绑定');
          console.log('='.repeat(50));
          console.log('\n💡 提示:');
          console.log('   1. 打开手机微信');
          console.log('   2. 扫描上方二维码');
          console.log('   3. 确认授权绑定');
          console.log('   4. 等待连接成功');
          console.log('\n' + '='.repeat(50));
          
          // 等待用户扫码
          await this.waitForScan();
          
          return { command, status: '二维码已生成' };
        }
      } catch (error) {
        console.log(`   ⚠️  二维码命令失败: ${command}`);
      }
    }
    
    // 如果无法自动生成二维码，提供手动说明
    console.log('\n📱 手动二维码生成说明:');
    console.log('='.repeat(50));
    console.log('如果未自动生成二维码，请手动执行:');
    console.log('   1. 打开微信 → 我 → 设置 → 插件');
    console.log('   2. 找到「微信 ClawBot」');
    console.log('   3. 点击详情，复制安装命令');
    console.log('   4. 在终端执行: npx -y @tencent-weixin/openclaw-weixin-cli@latest install');
    console.log('   5. 扫描生成的二维码');
    console.log('='.repeat(50));
    
    return { status: '需要手动生成二维码', instructions: '请按照上述说明操作' };
  }
  
  async waitForScan() {
    return new Promise((resolve) => {
      console.log('\n⏳ 等待扫码绑定... (按Enter键继续)');
      this.rl.question('', () => {
        resolve();
      });
    });
  }
  
  async verifyInstallation() {
    console.log('   验证安装结果...');
    
    const verificationCommands = [
      'openclaw plugins list',
      'openclaw channels list'
    ];
    
    const results = {};
    
    for (const command of verificationCommands) {
      try {
        const output = await this.executeCommand(command);
        results[command] = output.substring(0, 150) + '...';
        
        if (output.includes('openclaw-weixin') || output.includes('weixin')) {
          console.log(`   ✅ ${command}: 插件已安装`);
        } else {
          console.log(`   ⚠️  ${command}: 未找到微信插件`);
        }
      } catch (error) {
        console.log(`   ❌ ${command}: 验证失败 - ${error.message}`);
        results[command] = `失败: ${error.message}`;
      }
    }
    
    // 检查网关状态
    try {
      const gatewayStatus = await this.executeCommand('openclaw gateway status');
      if (gatewayStatus.includes('running') || gatewayStatus.includes('active')) {
        console.log('   ✅ OpenClaw网关运行正常');
        results.gateway = '运行中';
      } else {
        console.log('   ⚠️  OpenClaw网关未运行');
        results.gateway = '未运行';
      }
    } catch (error) {
      console.log(`   ❌ 网关状态检查失败: ${error.message}`);
      results.gateway = `检查失败: ${error.message}`;
    }
    
    return results;
  }
  
  async provideFallbackSolution(stepName, error) {
    console.log(`\n🛠️  ${stepName}失败，尝试备用方案...`);
    
    switch (stepName) {
      case '安装微信插件':
        console.log('   备用安装方案:');
        console.log('   1. 手动安装: openclaw plugins install "@tencent-weixin/openclaw-weixin"');
        console.log('   2. 启用插件: openclaw config set plugins.entries.openclaw-weixin.enabled true');
        console.log('   3. 重启网关: openclaw gateway restart');
        break;
        
      case '生成二维码':
        console.log('   手动生成二维码:');
        console.log('   1. 确保微信版本 >= 8.0.70');
        console.log('   2. 微信 → 设置 → 插件 → 微信 ClawBot');
        console.log('   3. 复制安装命令并执行');
        console.log('   4. 扫描生成的二维码');
        break;
        
      default:
        console.log(`   错误详情: ${error.message}`);
        console.log('   请参考文档解决问题');
    }
    
    // 询问是否继续
    const continueInstall = await this.askToContinue();
    if (!continueInstall) {
      throw new Error('用户取消安装');
    }
  }
  
  async askToContinue() {
    return new Promise((resolve) => {
      this.rl.question('\n是否继续安装？(y/n): ', (answer) => {
        resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
      });
    });
  }
  
  async executeCommand(command, timeout = 10000) {
    return new Promise((resolve, reject) => {
      exec(command, { timeout }, (error, stdout, stderr) => {
        if (error) {
          reject(new Error(stderr || error.message));
        } else {
          resolve(stdout.toString().trim());
        }
      });
    });
  }
  
  completeInstallation() {
    console.log('\n' + '='.repeat(60));
    console.log('🎉 微信集成安装完成！');
    console.log('='.repeat(60));
    
    const completedSteps = this.steps.filter(s => s.status === 'completed').length;
    const totalSteps = this.steps.length;
    
    console.log(`📊 安装统计: ${completedSteps}/${totalSteps} 步骤完成`);
    
    console.log('\n🚀 开始使用:');
    console.log('   1. 打开手机微信');
    console.log('   2. 找到「微信 ClawBot」对话');
    console.log('   3. 开始与OpenClaw聊天');
    console.log('   4. 使用所有OpenClaw功能');
    
    console.log('\n💡 使用提示:');
    console.log('   • 在微信中直接发送消息');
    console.log('   • 支持文本、图片、文件');
    console.log('   • 保持OpenClaw所有技能');
    console.log('   • 多会话独立上下文');
    
    console.log('\n🛠️  管理命令:');
    console.log('   • 查看插件: openclaw plugins list');
    console.log('   • 查看频道: openclaw channels list');
    console.log('   • 重启网关: openclaw gateway restart');
    console.log('   • 查看日志: openclaw logs --channel openclaw-weixin');
    
    console.log('\n📚 学习资源:');
    console.log('   • B站视频: 《终于可以在微信中和你的 OpenClaw 聊天了》');
    console.log('   • 官方文档: https://docs.openclaw.ai/channels/weixin');
    console.log('   • 社区支持: https://github.com/openclaw/openclaw/discussions');
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 安装向导结束，享受微信中的OpenClaw体验！');
    console.log('='.repeat(60));
    
    // 保存安装报告
    this.saveInstallationReport();
  }
  
  saveInstallationReport() {
    const report = {
      timestamp: new Date().toISOString(),
      steps: this.steps,
      summary: {
        completed: this.steps.filter(s => s.status === 'completed').length,
        failed: this.steps.filter(s => s.status === 'failed').length,
        total: this.steps.length
      }
    };
    
    const reportDir = path.join(process.cwd(), 'wechat-openclaw-skill', 'reports');
    if (!fs.existsSync(reportDir)) {
      fs.mkdirSync(reportDir, { recursive: true });
    }
    
    const reportFile = path.join(reportDir, `installation-${Date.now()}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    
    console.log(`\n📄 安装报告已保存: ${reportFile}`);
  }
  
  generateErrorReport(error) {
    console.log('\n' + '='.repeat(60));
    console.log('🚨 安装错误报告');
    console.log('='.repeat(60));
    
    console.log(`错误: ${error.message}`);
    console.log(`步骤: ${JSON.stringify(this.steps, null, 2)}`);
    
    console.log('\n🆘 故障排除:');
    console.log('   1. 检查微信版本 >= 8.0.70');
    console.log('   2. 确保OpenClaw网关运行');
    console.log('   3. 检查网络连接');
    console.log('   4. 尝试手动安装命令');
    
    console.log('\n📞 获取帮助:');
    console.log('   • GitHub Issues: https://github.com/tencent-weixin/openclaw-weixin/issues');
    console.log('   • 社区讨论: https://github.com/openclaw/openclaw/discussions');
    console.log('   • B站视频教程评论区');
    
    console.log('\n' + '='.repeat(60));
  }
}

// 启动安装
const installer = new WeChatInstaller();
installer.startInstallation().catch(error => {
  console.error('安装失败:', error);
  process.exit(1);
});