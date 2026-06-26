#!/usr/bin/env node
/**
 * read-file.js - 文件读取工具包装器
 * 
 * 用法：node read-file.js <文件路径>
 */

const { spawnSync } = require('child_process');
const path = require('path');

// Python 路径配置：优先使用环境变量中的 python，否则尝试常见路径
function findPython() {
    const commonPaths = [
        'python',
        'python3',
        'C:\\Users\\' + process.env.USERNAME + '\\miniconda3\\python.exe',
        'C:\\Users\\' + process.env.USERNAME + '\\Anaconda3\\python.exe',
        'D:\\miniconda3\\python.exe',
        'D:\\Anaconda3\\python.exe',
        'C:\\Program Files\\Python39\\python.exe',
        'C:\\Program Files\\Python310\\python.exe',
        'C:\\Program Files\\Python311\\python.exe'
    ];
    
    for (const pyPath of commonPaths) {
        try {
            const result = spawnSync(pyPath, ['--version'], { encoding: 'utf-8', timeout: 5000 });
            if (result.status === 0 || result.stdout || result.stderr) {
                return pyPath;
            }
        } catch (e) {
            continue;
        }
    }
    
    return null;
}

const PYTHON_PATH = findPython();
const SCRIPT_PATH = path.join(__dirname, 'read-file.py');

function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.error('用法：node read-file.js <文件路径>');
        console.error('示例：node read-file.js "D:\\文档\\笔记.txt"');
        process.exit(1);
    }
    
    // 检测 Python 是否存在
    if (!PYTHON_PATH) {
        console.error('❌ 错误：未找到 Python 环境');
        console.error('');
        console.error('请先安装 Python，推荐以下方式：');
        console.error('');
        console.error('  1. Miniconda（推荐）:');
        console.error('     https://docs.conda.io/en/latest/miniconda.html');
        console.error('');
        console.error('  2. Python 官方安装包:');
        console.error('     https://www.python.org/downloads/');
        console.error('     ⚠️ 安装时请勾选 "Add Python to PATH"');
        console.error('');
        console.error('  3. 或使用 winget 安装:');
        console.error('     winget install Python.Python.3.11');
        console.error('');
        console.error('安装完成后，重新运行此命令。');
        process.exit(1);
    }
    
    const filePath = args[0];
    
    // 使用 spawnSync 并设置环境变量强制 UTF-8
    const result = spawnSync(PYTHON_PATH, [SCRIPT_PATH, filePath], {
        encoding: 'utf-8',
        stdio: ['pipe', 'pipe', 'pipe'],
        env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8'
        },
        timeout: 60000  // 60 秒超时
    });
    
    if (result.stdout) {
        process.stdout.write(result.stdout);
    }
    
    if (result.stderr) {
        process.stderr.write(result.stderr);
    }
    
    if (result.status !== 0) {
        process.exit(result.status);
    }
}

main();
