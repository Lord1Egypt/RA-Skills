/**
 * 亚协知识库文件读取脚本
 * 用法: node wiki_read.js <obj_token> [输出文件]
 * 示例: node wiki_read.js W6kkbVuX6okeVfxjdGcckS88n2c
 */

const https = require('https');
const fs = require('fs');
const { exec } = require('child_process');
const path = require('path');

// 飞书应用凭证
const APP_ID = 'cli_a93b38f075b89cc4';
const APP_SECRET = 'CRSq1ZHlMM0QE488w9ph1fX0gG2eDXox';

// 获取token
function getToken() {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'open.feishu.cn', port: 443,
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {
        const resp = JSON.parse(d);
        resolve(resp.tenant_access_token);
      });
    });
    req.on('error', reject);
    req.write(JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }));
    req.end();
  });
}

// 下载文件
function downloadFile(fileToken, token, savePath) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'open.feishu.cn', port: 443,
      path: '/open-apis/drive/v1/files/' + fileToken + '/download',
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + token }
    }, res => {
      const file = fs.createWriteStream(savePath);
      res.pipe(file);
      file.on('finish', () => resolve(savePath));
    });
    req.on('error', reject);
    req.end();
  });
}

// 读取docx内容
function readDocx(filePath) {
  return new Promise((resolve, reject) => {
    // 写入临时Python脚本避免转义问题
    const pyScript = `
import zipfile
import xml.etree.ElementTree as ET
import sys

z = zipfile.ZipFile(r'${filePath.replace(/\\/g, '\\\\')}', 'r')
imgs = [n for n in z.namelist() if 'image' in n]
if len(imgs) > 0:
    print(f'WARNING: DOC_CONTAINS_IMAGES:{len(imgs)}', file=sys.stderr)
    sys.exit(0)
    
f = z.open('word/document.xml')
tree = ET.parse(f)
root = tree.getroot()
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
texts = []
for para in root.findall('.//w:p', ns):
    parts = []
    for t in para.findall('.//w:t', ns):
        if t.text:
            parts.append(t.text)
    if parts:
        texts.append(''.join(parts))
print('\\n'.join(texts))
`;
    const pyFile = path.join(__dirname, '_temp_read.py');
    fs.writeFileSync(pyFile, pyScript, 'utf8');
    
    exec('python ' + pyFile, (err, stdout, stderr) => {
      fs.unlinkSync(pyFile);
      if (err) reject(err);
      else {
        if (stderr.includes('WARNING: DOC_CONTAINS_IMAGES')) {
          resolve('[图片型文档，内容在图片中，需OCR识别]');
        } else {
          resolve(stdout);
        }
      }
    });
  });
}

// 读取pdf内容
function readPdf(filePath) {
  return new Promise((resolve, reject) => {
    const pyScript = `
import PyPDF2
reader = PyPDF2.PdfReader(r'${filePath.replace(/\\/g, '\\\\')}')
texts = []
for page in reader.pages[:10]:
    t = page.extract_text()
    if t:
        texts.append(t)
print('\\n'.join(texts))
`;
    const pyFile = path.join(__dirname, '_temp_read.py');
    fs.writeFileSync(pyFile, pyScript, 'utf8');
    
    exec('python ' + pyFile, (err, stdout, stderr) => {
      fs.unlinkSync(pyFile);
      if (err) reject(err);
      else resolve(stdout);
    });
  });
}

// 主入口
async function main() {
  const objToken = process.argv[2];
  const outputFile = process.argv[3];
  
  if (!objToken) {
    console.log('用法: node wiki_read.js <obj_token> [输出文件]');
    console.log('示例: node wiki_read.js W6kkbVuX6okeVfxjdGcckS88n2c');
    process.exit(1);
  }
  
  const token = await getToken();
  const tempPath = path.join(__dirname, '..', '..', '..', 'temp_wiki_file_' + Date.now() + '.docx');
  
  console.log('下载文件...');
  await downloadFile(objToken, token, tempPath);
  
  const stats = fs.statSync(tempPath);
  console.log('文件大小: ' + stats.size + ' bytes');
  
  const ext = tempPath.toLowerCase();
  
  try {
    let content;
    if (ext.endsWith('.docx') || ext.endsWith('.doc')) {
      content = await readDocx(tempPath);
    } else if (ext.endsWith('.pdf')) {
      content = await readPdf(tempPath);
    } else {
      console.log('不支持的文件格式');
      process.exit(1);
    }
    
    console.log('\\n=== 内容 (' + content.length + ' 字符) ===\\n');
    console.log(content);
    
    if (outputFile) {
      fs.writeFileSync(outputFile, content, 'utf8');
      console.log('\\n已保存到: ' + outputFile);
    }
  } finally {
    // 清理临时文件
    if (fs.existsSync(tempPath)) {
      fs.unlinkSync(tempPath);
    }
  }
}

main().catch(console.error);
