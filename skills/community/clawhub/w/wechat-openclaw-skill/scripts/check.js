#!/usr/bin/env node

/**
 * 微信集成环境检查脚本
 * 基于B站视频《终于可以在微信中和你的 OpenClaw 聊天了，保姆级一键安装教程》
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

console.log('🔍 微信集成环境检查');
console.log('='.repeat(60));
console.log('基于《终于可以在微信中和你的 OpenClaw 聊天了，保姆级一键安装教程》');
console.log('='.repeat(60));

class WeChatEnvironmentChecker {
  constructor() {
    this.results = [];
    this.issues = [];
    this.recommendations = [];
  }
  
  async runChecks() {
    console.log('\n1. 📱 微信版本检查...');
    await this.checkWeChatVersion();
    
    console.log('\n2. ⚙️  OpenClaw检查...');
    await this.checkOpenClaw();
    
    console.log('\n3. 🖥️  系统环境检查...');
    await this.checkSystemEnvironment();
    
    console.log('\n4. 🌐 网络连接检查...');
    await this.checkNetwork();
    
    console.log('\n5. 📋 生成检查报告...');
    this.generateReport();
  }
  
  async checkWeChatVersion() {
    console.log('   检查微信版本要求...');
    
    // 微信版本要求：8.0.70+
    const requiredVersion = '8.0.70';
    
    this.results.push({
      check: '微信版本',
      required: `>= ${requiredVersion}`,
      status: 'manual',
      message: '请手动检查微信版本：设置 → 关于微信',
      details: '微信8.0.70及以上版本支持OpenClaw插件'
    });
    
    console.log('   ℹ️  需要微信8.0.70或更高版本');
    console.log('   📱 检查方法：微信 → 我 → 设置 → 关于微信');
    
    this.recommendations.push(
      '确保微信已更新到8.0.70或更高版本',
      '在微信设置中启用插件功能'
    );
  }
  
  async checkOpenClaw() {
    const checks = [
      {
        name: 'OpenClaw安装',
        command: 'openclaw --version',
        check: (output) => output.includes('OpenClaw'),
        message: 'OpenClaw已安装',
        error: 'OpenClaw未安装或不在PATH中'
      },
      {
        name: 'OpenClaw版本',
        command: 'openclaw --version',
        check: (output) => {
          const versionMatch = output.match(/OpenClaw\s+(\d+\.\d+\.\d+)/);
          if (versionMatch) {
            const version = versionMatch[1];
            const [major, minor, patch] = version.split('.').map(Number);
            return major >= 2026 && minor >= 4;
          }
          return false;
        },
        message: 'OpenClaw版本符合要求',
        error: '需要OpenClaw 2026.4.0或更高版本'
      },
      {
        name: '网关状态',
        command: 'openclaw gateway status',
        check: (output) => output.includes('running') || output.includes('active'),
        message: 'OpenClaw网关运行中',
        error: 'OpenClaw网关未运行'
      }
    ];
    
    for (const check of checks) {
      try {
        const output = await this.executeCommand(check.command);
        const passed = check.check(output);
        
        this.results.push({
          check: check.name,
          status: passed ? 'passed' : 'failed',
          message: passed ? check.message : check.error,
          details: passed ? output.substring(0, 100) : '请检查OpenClaw安装和配置'
        });
        
        const icon = passed ? '✅' : '❌';
        console.log(`   ${icon} ${check.name}: ${passed ? check.message : check.error}`);
        
        if (!passed) {
          this.issues.push(check.name);
          this.recommendations.push(`解决${check.name}问题: ${check.error}`);
        }
      } catch (error) {
        this.results.push({
          check: check.name,
          status: 'error',
          message: `检查失败: ${error.message}`,
          details: '命令执行错误'
        });
        
        console.log(`   ❌ ${check.name}: 检查失败 - ${error.message}`);
        this.issues.push(check.name);
      }
    }
  }
  
  async checkSystemEnvironment() {
    const checks = [
      {
        name: 'Node.js版本',
        check: () => {
          const version = process.version;
          const major = parseInt(version.replace('v', '').split('.')[0]);
          return major >= 18;
        },
        message: 'Node.js版本符合要求',
        error: '需要Node.js 18.0.0或更高版本'
      },
      {
        name: 'npm可用性',
        check: async () => {
          const output = await this.executeCommand('npm --version');
          return output && !output.includes('command not found');
        },
        message: 'npm可用',
        error: 'npm未安装或不可用'
      },
      {
        name: 'npx可用性',
        check: async () => {
          const output = await this.executeCommand('npx --version');
          return output && !output.includes('command not found');
        },
        message: 'npx可用',
        error: 'npx未安装或不可用'
      }
    ];
    
    for (const check of checks) {
      try {
        let passed;
        if (typeof check.check === 'function') {
          passed = await check.check();
        } else {
          const output = await this.executeCommand(check.command);
          passed = check.check(output);
        }
        
        this.results.push({
          check: check.name,
          status: passed ? 'passed' : 'failed',
          message: passed ? check.message : check.error
        });
        
        const icon = passed ? '✅' : '❌';
        console.log(`   ${icon} ${check.name}: ${passed ? check.message : check.error}`);
        
        if (!passed) {
          this.issues.push(check.name);
        }
      } catch (error) {
        this.results.push({
          check: check.name,
          status: 'error',
          message: `检查失败: ${error.message}`
        });
        
        console.log(`   ❌ ${check.name}: 检查失败`);
        this.issues.push(check.name);
      }
    }
  }
  
  async checkNetwork() {
    console.log('   检查网络连接...');
    
    const networkChecks = [
      {
        name: '微信服务器',
        host: 'weixin.qq.com',
        message: '可访问微信服务器',
        error: '无法访问微信服务器'
      },
      {
        name: 'npm仓库',
        host: 'registry.npmjs.org',
        message: '可访问npm仓库',
        error: '无法访问npm仓库'
      }
    ];
    
    for (const check of networkChecks) {
      try {
        // 简单的ping检查（使用node的dns解析）
        const { promisify } = require('util');
        const dns = require('dns');
        const resolve = promisify(dns.resolve4);
        
        await resolve(check.host);
        
        this.results.push({
          check: `网络-${check.name}`,
          status: 'passed',
          message: check.message
        });
        
        console.log(`   ✅ ${check.name}: ${check.message}`);
      } catch (error) {
        this.results.push({
          check: `网络-${check.name}`,
          status: 'failed',
          message: check.error,
          details: error.message
        });
        
        console.log(`   ❌ ${check.name}: ${check.error}`);
        this.issues.push(`网络-${check.name}`);
        this.recommendations.push(`检查网络连接，确保可以访问${check.host}`);
      }
    }
  }
  
  async executeCommand(command) {
    return new Promise((resolve, reject) => {
      exec(command, { timeout: 10000 }, (error, stdout, stderr) => {
        if (error) {
          reject(new Error(stderr || error.message));
        } else {
          resolve(stdout.toString().trim());
        }
      });
    });
  }
  
  generateReport() {
    console.log('\n' + '='.repeat(60));
    console.log('📊 环境检查报告');
    console.log('='.repeat(60));
    
    const passed = this.results.filter(r => r.status === 'passed').length;
    const failed = this.results.filter(r => r.status === 'failed' || r.status === 'error').length;
    const total = this.results.length;
    
    console.log(`✅ 通过: ${passed}/${total}`);
    console.log(`❌ 失败: ${failed}/${total}`);
    
    if (this.issues.length > 0) {
      console.log('\n🚨 发现的问题:');
      this.issues.forEach((issue, index) => {
        console.log(`   ${index + 1}. ${issue}`);
      });
    } else {
      console.log('\n🎉 所有检查通过！可以开始安装微信集成。');
    }
    
    if (this.recommendations.length > 0) {
      console.log('\n💡 建议操作:');
      this.recommendations.forEach((rec, index) => {
        console.log(`   ${index + 1}. ${rec}`);
      });
    }
    
    // 添加视频中的关键步骤
    console.log('\n📱 微信集成关键步骤（基于视频）:');
    console.log('   1. 确保微信版本 >= 8.0.70');
    console.log('   2. 运行安装命令: npx -y @tencent-weixin/openclaw-weixin-cli@latest install');
    console.log('   3. 扫描生成的二维码');
    console.log('   4. 在微信中开始使用OpenClaw');
    
    console.log('\n🛠️  备用安装方案:');
    console.log('   • Windows用户: openclaw plugins install "@tencent-weixin/openclaw-weixin"');
    console.log('   • 启用插件: openclaw config set plugins.entries.openclaw-weixin.enabled true');
    console.log('   • 扫码登录: openclaw channels login --channel openclaw-weixin');
    
    console.log('\n' + '='.repeat(60));
    console.log('🚀 下一步:');
    
    if (this.issues.length === 0) {
      console.log('   运行安装脚本: node scripts/install.js');
    } else {
      console.log('   先解决上述问题，然后运行安装脚本');
    }
    
    console.log('='.repeat(60));
    
    // 保存详细报告
    const report = {
      timestamp: new Date().toISOString(),
      results: this.results,
      issues: this.issues,
      recommendations: this.recommendations,
      summary: {
        passed,
        failed,
        total
      }
    };
    
    const reportDir = path.join(process.cwd(), 'wechat-openclaw-skill', 'reports');
    if (!fs.existsSync(reportDir)) {
      fs.mkdirSync(reportDir, { recursive: true });
    }
    
    const reportFile = path.join(reportDir, `environment-check-${Date.now()}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    
    console.log(`\n📄 详细报告已保存: ${reportFile}`);
  }
}

// 运行检查
const checker = new WeChatEnvironmentChecker();
checker.runChecks().catch(error => {
  console.error('检查失败:', error);
  process.exit(1);
});