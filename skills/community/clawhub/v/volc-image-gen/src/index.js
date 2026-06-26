/**
 * volc-image-gen - 火山引擎图像生成技能
 * 主入口文件 - 命令分发与参数验证
 */

const { generateImage, batchGenerate, styleMap, supportedSizes } = require('./image-gen');
const { editImage, createVariations } = require('./image-edit');

/**
 * 处理命令
 * @param {object} context - 执行上下文
 * @param {string} context.command - 命令名称
 * @param {object} context.params - 命令参数
 * @returns {Promise<object>} 执行结果
 */
async function handleCommand(context) {
  const { command, params = {} } = context;

  console.log(`\n🎨 volc-image-gen 收到命令：${command}`);
  console.log('参数:', JSON.stringify(params, null, 2));

  switch (command) {
    // ========== 文生图 ==========
    case 'generate':
    case '文生图':
    case '生成图片':
    case 'img':
    case 'image': {
      const { prompt, size, n, style, negative_prompt } = params;
      
      if (!prompt || typeof prompt !== 'string' || prompt.trim().length === 0) {
        return {
          success: false,
          error: '缺少必要参数：prompt（图片描述）',
          usage: '请提供图片描述，例如：prompt="一只可爱的猫咪"'
        };
      }

      return await generateImage({
        prompt: prompt.trim(),
        size: size || '1024x1024',
        n: n || 1,
        style: style || 'realistic',
        negative_prompt: negative_prompt || ''
      });
    }

    // ========== 图生图 ==========
    case 'edit':
    case '图生图':
    case '编辑图片':
    case 'img2img': {
      const { image, prompt, strength, size } = params;

      if (!image) {
        return {
          success: false,
          error: '缺少必要参数：image（输入图片 URL 或本地路径）'
        };
      }

      if (!prompt || typeof prompt !== 'string' || prompt.trim().length === 0) {
        return {
          success: false,
          error: '缺少必要参数：prompt（编辑描述）'
        };
      }

      return await editImage({
        image,
        prompt: prompt.trim(),
        strength: strength !== undefined ? strength : 0.7,
        size: size || '1024x1024'
      });
    }

    // ========== 批量生成 ==========
    case 'batch':
    case '批量生成':
    case 'batch_generate': {
      const { prompts, concurrent, size, style } = params;

      if (!prompts || !Array.isArray(prompts) || prompts.length === 0) {
        return {
          success: false,
          error: '缺少必要参数：prompts（提示词数组）',
          usage: '请提供提示词数组，例如：prompts=["猫咪", "狗狗", "兔子"]'
        };
      }

      return await batchGenerate(prompts, {
        concurrent: concurrent || 3,
        size: size || '1024x1024',
        style: style || 'realistic'
      });
    }

    // ========== 生成变体 ==========
    case 'variations':
    case '生成变体':
    case '变体': {
      const { image, n, strength, size } = params;

      if (!image) {
        return {
          success: false,
          error: '缺少必要参数：image（输入图片）'
        };
      }

      return await createVariations(image, {
        n: n || 3,
        strength: strength !== undefined ? strength : 0.5,
        size: size || '1024x1024'
      });
    }

    // ========== 查询帮助 ==========
    case 'help':
    case '帮助':
    case 'usage': {
      return {
        success: true,
        help: {
          name: 'volc-image-gen',
          version: '1.0.0',
          description: '火山引擎图像生成技能',
          commands: {
            '文生图': {
              command: ['generate', '文生图', '生成图片', 'img'],
              params: {
                prompt: '【必填】图片描述',
                size: '【可选】尺寸，默认 1024x1024',
                n: '【可选】生成数量，默认 1',
                style: '【可选】风格：realistic/anime/oil/watercolor/sketch/cyberpunk/fantasy',
                negative_prompt: '【可选】负面提示词'
              },
              example: '{ "command": "generate", "params": { "prompt": "一只可爱的猫咪", "style": "anime" } }'
            },
            '图生图': {
              command: ['edit', '图生图', '编辑图片', 'img2img'],
              params: {
                image: '【必填】输入图片 URL 或本地路径',
                prompt: '【必填】编辑描述',
                strength: '【可选】重绘强度 0-1，默认 0.7',
                size: '【可选】输出尺寸'
              },
              example: '{ "command": "edit", "params": { "image": "/path/to/img.png", "prompt": "换成狗狗" } }'
            },
            '批量生成': {
              command: ['batch', '批量生成'],
              params: {
                prompts: '【必填】提示词数组',
                concurrent: '【可选】并发数，默认 3',
                size: '【可选】尺寸',
                style: '【可选】风格'
              },
              example: '{ "command": "batch", "params": { "prompts": ["猫咪", "狗狗"] } }'
            },
            '生成变体': {
              command: ['variations', '生成变体', '变体'],
              params: {
                image: '【必填】输入图片',
                n: '【可选】变体数量，默认 3',
                strength: '【可选】变体强度，默认 0.5',
                size: '【可选】尺寸'
              },
              example: '{ "command": "variations", "params": { "image": "/path/to/img.png", "n": 5 } }'
            }
          },
          styles: styleMap,
          supportedSizes: supportedSizes,
          env: {
            VOLC_API_KEY: '【必填】火山引擎 API Key',
            VOLC_API_BASE: '【可选】API 基础 URL',
            VOLC_IMAGE_MODEL: '【可选】图像模型，默认 doubao-image-x'
          }
        }
      };
    }

    // ========== 未知命令 ==========
    default:
      return {
        success: false,
        error: `未知命令：${command}`,
        hint: '使用 "help" 命令查看可用命令'
      };
  }
}

// 导出所有功能
module.exports = {
  name: 'volc-image-gen',
  version: '1.0.0',
  execute: handleCommand,
  generateImage,
  editImage,
  batchGenerate,
  createVariations,
  styleMap,
  supportedSizes
};

// 如果直接运行此文件，显示帮助信息
if (require.main === module) {
  console.log('🎨 volc-image-gen v1.0.0 - 火山引擎图像生成技能');
  console.log('\n请通过 OpenClaw 调用此技能，或使用以下命令测试：');
  console.log('node src/index.js help');
}
