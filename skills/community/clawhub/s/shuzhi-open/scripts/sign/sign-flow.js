#!/usr/bin/env node
/**
 * 电子签章 - 签署流程管理
 */

const path = require('path');
const fs = require('fs');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init, getConfig, getCredentials } = require(path.join(libPath, 'client'));
const { buildHeaders } = require(path.join(libPath, 'auth'));
const { getEndpointConfig } = require(path.join(libPath, 'validate'));
const sign = require(path.join(libPath, 'modules/sign'));

const config = require(configPath);
init(config);

function parseArgs() {
  const args = process.argv.slice(2);
  const params = { action: args[0] };
  
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        params[key] = value;
        i++;
      }
    }
  }
  
  return params;
}

/**
 * 下载签署后的文件
 */
async function downloadSignedFile(flowId, outputPath) {
  // 获取签署文件列表
  const filesResult = await sign.signFlow.files(flowId);
  const files = filesResult.data || filesResult;
  
  if (!files || files.length === 0) {
    throw new Error('未找到签署文件');
  }
  
  const file = files[0];
  const fileName = file.signResultPath || file.filePath;
  
  if (!fileName) {
    throw new Error('未找到签署结果文件路径');
  }
  
  // 下载文件
  const { path: apiPath, productId } = getEndpointConfig(getConfig(), 'sign', 'fileDownload');
  const credentials = getCredentials();
  
  const url = `${getConfig().baseUrl}${apiPath}`;
  const body = { fileName };
  
  const headers = buildHeaders('POST', apiPath, body, {
    appKey: credentials.appKey,
    appSecret: credentials.appSecret,
    productId
  });
  
  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(body)
  });
  
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`下载失败: ${text}`);
  }
  
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  
  // 确定输出路径
  if (!outputPath) {
    outputPath = path.join(process.cwd(), file.signResultPath || `signed_${flowId}.pdf`);
  }
  
  // 确保目录存在
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(outputPath, buffer);
  
  return {
    fileName: file.signResultPath,
    outputPath,
    size: buffer.length
  };
}

async function main() {
  const params = parseArgs();
  const action = params.action;
  
  try {
    switch (action) {
      case 'create':
        if (params.file) {
          const filePath = path.resolve(params.file);
          const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
          const createResult = await sign.signFlow.create(data);
          console.log(JSON.stringify({ success: true, data: createResult }, null, 2));
        } else {
          console.error('用法: node sign-flow.js create --file params.json');
          process.exit(1);
        }
        break;
        
      case 'detail':
        if (!params['flow-id']) {
          console.error('用法: node sign-flow.js detail --flow-id "流程ID"');
          process.exit(1);
        }
        const detailResult = await sign.signFlow.detail(params['flow-id']);
        console.log(JSON.stringify({ success: true, data: detailResult }, null, 2));
        break;
        
      case 'preview':
        if (!params['flow-id']) {
          console.error('用法: node sign-flow.js preview --flow-id "流程ID"');
          process.exit(1);
        }
        const previewResult = await sign.signFlow.preview(params['flow-id']);
        console.log(JSON.stringify({ 
          success: true, 
          data: {
            previewUrl: previewResult.previewUrl,
            signUrl: previewResult.signUrl
          }
        }, null, 2));
        break;
        
      case 'files':
        if (!params['flow-id']) {
          console.error('用法: node sign-flow.js files --flow-id "流程ID"');
          process.exit(1);
        }
        const filesResult = await sign.signFlow.files(params['flow-id']);
        console.log(JSON.stringify({ success: true, data: filesResult }, null, 2));
        break;
        
      case 'signers':
        if (!params['flow-id']) {
          console.error('用法: node sign-flow.js signers --flow-id "流程ID"');
          process.exit(1);
        }
        const signersResult = await sign.signFlow.signers(params['flow-id']);
        console.log(JSON.stringify({ success: true, data: signersResult }, null, 2));
        break;
        
      case 'download':
        if (!params['flow-id']) {
          console.error('用法: node sign-flow.js download --flow-id "流程ID" [--output "输出路径"]');
          process.exit(1);
        }
        const downloadResult = await downloadSignedFile(params['flow-id'], params.output);
        console.log(JSON.stringify({ 
          success: true, 
          data: {
            fileName: downloadResult.fileName,
            outputPath: downloadResult.outputPath,
            sizeKB: (downloadResult.size / 1024).toFixed(2)
          }
        }, null, 2));
        break;
        
      default:
        console.error('用法:');
        console.error('  node sign-flow.js create --file params.json');
        console.error('  node sign-flow.js detail --flow-id "流程ID"');
        console.error('  node sign-flow.js preview --flow-id "流程ID"');
        console.error('  node sign-flow.js files --flow-id "流程ID"');
        console.error('  node sign-flow.js signers --flow-id "流程ID"');
        console.error('  node sign-flow.js download --flow-id "流程ID" [--output "输出路径"]');
        process.exit(1);
    }
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();