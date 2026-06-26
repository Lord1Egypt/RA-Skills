/**
 * Deployment Kit - 部署管理器
 * Docker + CI/CD + 健康检查
 */

import { EventEmitter } from 'events';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * 部署管理器
 */
export class DeployManager extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = {
      imageName: config.imageName || 'openclaw',
      containerName: config.containerName || 'openclaw',
      port: config.port || 18789,
      registry: config.registry || null,
      ...config
    };
    this.status = 'idle';
  }

  /**
   * 构建 Docker 镜像
   */
  async buildImage() {
    this.emit('build-started');
    this.status = 'building';
    
    try {
      const { stdout, stderr } = await execAsync(
        `docker build -t ${this.config.imageName}:latest .`
      );
      
      this.status = 'built';
      this.emit('build-completed', { stdout, stderr });
      return { success: true, stdout };
    } catch (error) {
      this.status = 'failed';
      this.emit('build-failed', error);
      throw error;
    }
  }

  /**
   * 运行容器
   */
  async runContainer() {
    this.emit('run-started');
    this.status = 'running';
    
    try {
      // 停止旧容器
      await execAsync(`docker stop ${this.config.containerName} 2>nul || true`);
      await execAsync(`docker rm ${this.config.containerName} 2>nul || true`);
      
      // 启动新容器
      const { stdout } = await execAsync(
        `docker run -d -p ${this.config.port}:${this.config.port} ` +
        `--name ${this.config.containerName} ${this.config.imageName}:latest`
      );
      
      this.status = 'deployed';
      this.emit('run-completed', { containerId: stdout.trim() });
      return { success: true, containerId: stdout.trim() };
    } catch (error) {
      this.status = 'failed';
      this.emit('run-failed', error);
      throw error;
    }
  }

  /**
   * 健康检查
   */
  async healthCheck() {
    const checks = {
      docker: await this.checkDocker(),
      container: await this.checkContainer(),
      port: await this.checkPort(),
      timestamp: new Date().toISOString()
    };
    
    const healthy = checks.docker && checks.container && checks.port;
    
    this.emit('health-checked', { healthy, checks });
    return { healthy, checks };
  }

  /**
   * 检查 Docker 状态
   */
  async checkDocker() {
    try {
      await execAsync('docker version');
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 检查容器状态
   */
  async checkContainer() {
    try {
      const { stdout } = await execAsync(
        `docker ps -q -f name=${this.config.containerName}`
      );
      return stdout.trim().length > 0;
    } catch {
      return false;
    }
  }

  /**
   * 检查端口
   */
  async checkPort() {
    try {
      const { stdout } = await execAsync(
        `netstat -an | findstr :${this.config.port}`
      );
      return stdout.includes('LISTENING');
    } catch {
      return false;
    }
  }

  /**
   * 获取容器日志
   */
  async getLogs(lines = 100) {
    try {
      const { stdout } = await execAsync(
        `docker logs --tail ${lines} ${this.config.containerName}`
      );
      return stdout;
    } catch (error) {
      return `Error getting logs: ${error.message}`;
    }
  }

  /**
   * 停止容器
   */
  async stop() {
    try {
      await execAsync(`docker stop ${this.config.containerName}`);
      this.status = 'stopped';
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * 一键部署
   */
  async deploy() {
    this.emit('deploy-started');
    
    try {
      await this.buildImage();
      await this.runContainer();
      const health = await this.healthCheck();
      
      this.emit('deploy-completed', { health });
      return { success: true, health };
    } catch (error) {
      this.emit('deploy-failed', error);
      throw error;
    }
  }
}

export default DeployManager;
