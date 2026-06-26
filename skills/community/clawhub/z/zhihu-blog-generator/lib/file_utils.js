/**
 * 知乎技术博客生成器 - 文件操作工具
 */

const fs = require('fs');
const path = require('path');
const config = require('./config');

class FileUtils {
  constructor(sessionId) {
    this.sessionId = sessionId;
    this.sessionDir = config.output.getSessionDir(sessionId);
  }

  /**
   * 创建会话目录结构
   */
  createSessionDirectories() {
    const dirs = [
      this.sessionDir,
      path.join(this.sessionDir, config.directories.topic),
      path.join(this.sessionDir, config.directories.collected),
      path.join(this.sessionDir, config.directories.collected, 'web_pages'),
      path.join(this.sessionDir, config.directories.collected, 'papers'),
      path.join(this.sessionDir, config.directories.collected, 'code_snippets'),
      path.join(this.sessionDir, config.directories.draft),
      path.join(this.sessionDir, config.directories.refined),
      path.join(this.sessionDir, config.directories.output),
      path.join(this.sessionDir, config.directories.images),
    ];

    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });

    return this.sessionDir;
  }

  /**
   * 获取目录路径
   */
  getDir(dirName) {
    return path.join(this.sessionDir, config.directories[dirName] || dirName);
  }

  /**
   * 保存 JSON 文件
   */
  saveJSON(filename, data, dir = '') {
    const dirPath = dir ? this.getDir(dir) : this.sessionDir;
    const filePath = path.join(dirPath, filename);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return filePath;
  }

  /**
   * 读取 JSON 文件
   */
  readJSON(filename, dir = '') {
    const dirPath = dir ? this.getDir(dir) : this.sessionDir;
    const filePath = path.join(dirPath, filename);
    
    if (!fs.existsSync(filePath)) {
      return null;
    }
    
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  }

  /**
   * 保存 Markdown 文件
   */
  saveMarkdown(filename, content, dir = '') {
    const dirPath = dir ? this.getDir(dir) : this.sessionDir;
    const filePath = path.join(dirPath, filename);
    fs.writeFileSync(filePath, content, 'utf8');
    return filePath;
  }

  /**
   * 读取 Markdown 文件
   */
  readMarkdown(filename, dir = '') {
    const dirPath = dir ? this.getDir(dir) : this.sessionDir;
    const filePath = path.join(dirPath, filename);
    
    if (!fs.existsSync(filePath)) {
      return null;
    }
    
    return fs.readFileSync(filePath, 'utf8');
  }

  /**
   * 保存网页内容
   */
  saveWebPage(index, source, title, content) {
    const safeTitle = title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_').slice(0, 50);
    const filename = `${String(index).padStart(3, '0')}_${source}_${safeTitle}.md`;
    const dirPath = path.join(this.sessionDir, config.directories.collected, 'web_pages');
    const filePath = path.join(dirPath, filename);
    
    const markdownContent = `---
title: "${title}"
source: "${source}"
date: "${new Date().toISOString()}"
---

${content}`;

    fs.writeFileSync(filePath, markdownContent, 'utf8');
    return filePath;
  }

  /**
   * 保存论文
   */
  savePaper(paperName, content, metadata = {}) {
    const safeName = paperName.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_');
    const dirPath = path.join(this.sessionDir, config.directories.collected, 'papers');
    
    // 保存解析结果
    const jsonPath = path.join(dirPath, `${safeName}_parsed.json`);
    fs.writeFileSync(jsonPath, JSON.stringify({ metadata, content }, null, 2), 'utf8');
    
    return jsonPath;
  }

  /**
   * 复制图片到输出目录
   */
  copyImage(sourcePath, filename) {
    const imagesDir = path.join(this.sessionDir, config.directories.images);
    const destPath = path.join(imagesDir, filename);
    fs.copyFileSync(sourcePath, destPath);
    return destPath;
  }

  /**
   * 列出目录中的文件
   */
  listFiles(dir, pattern = '') {
    const dirPath = this.getDir(dir);
    
    if (!fs.existsSync(dirPath)) {
      return [];
    }

    const files = fs.readdirSync(dirPath);
    
    if (pattern) {
      const regex = new RegExp(pattern);
      return files.filter(f => regex.test(f));
    }
    
    return files;
  }

  /**
   * 生成文件名
   */
  generateFileName(title) {
    const date = new Date();
    const dateStr = `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;
    const safeTitle = title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_').slice(0, 30);
    return `${dateStr}_${safeTitle}.md`;
  }

  /**
   * 检查文件是否存在
   */
  exists(filename, dir = '') {
    const dirPath = dir ? this.getDir(dir) : this.sessionDir;
    const filePath = path.join(dirPath, filename);
    return fs.existsSync(filePath);
  }
}

module.exports = FileUtils;
