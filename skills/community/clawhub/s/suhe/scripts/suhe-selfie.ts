#!/usr/bin/env ts-node

import axios from 'axios';
import * as fs from 'fs';

interface ImageGenerationResponse {
  output: {
    images: Array<{
      url: string;
    }>;
  };
}

interface GatewayMessage {
  target: string;
  message: {
    type: 'image_url';
    data: {
      url: string;
      caption: string;
    };
  };
}

async function generateSuheSelfie(
  apiKey: string,
  gatewayToken: string,
  inputPrompt: string,
  targetChannel: string = '#general',
  mode: 'mirror' | 'direct' = 'mirror'
): Promise<void> {
  console.log('📸 Starting Suhe Selfie Generation...');

  // Validate inputs
  if (!inputPrompt) {
    throw new Error('No prompt provided');
  }

  console.log(`🔧 Using mode: ${mode}`);
  console.log(`📥 Input prompt: ${inputPrompt}`);
  console.log(`📡 Target channel: ${targetChannel}`);

  // Generate the final prompt based on mode
  let finalPrompt: string;
  const referenceImage = 'https://pic.lilozkzy.top/reference/suhe-new.png';

  if (mode === 'mirror') {
    // Mirror selfie: best for outfits, full body shots
    finalPrompt = `make a pic of this person, but ${inputPrompt}. the person is taking a mirror selfie`;
  } else {
    // Direct selfie: best for close-ups, locations, expressions
    finalPrompt = `a close-up selfie taken by herself at ${inputPrompt}, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible`;
  }

  console.log(`🎨 Generated prompt: ${finalPrompt}`);

  try {
    // Call the Tongyi Wanxiang API
    console.log('☁️ Calling Tongyi Wanxiang API...');
    const apiResponse = await axios.post<ImageGenerationResponse>(
      'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation',
      {
        model: 'wanx-imagegen',
        input: {
          prompt: finalPrompt,
          reference_image: referenceImage,
        },
        parameters: {
          size: '1024*1024',
          n: 1,
        },
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );

    // Extract image URL from response
    const imageUrl = apiResponse.data.output.images[0]?.url;

    if (!imageUrl) {
      throw new Error('Failed to generate image: No URL returned from API');
    }

    console.log(`🖼️ Generated image: ${imageUrl}`);

    // Send image to OpenClaw gateway
    console.log('📤 Sending image to OpenClaw gateway...');
    const gatewayPayload: GatewayMessage = {
      target: targetChannel,
      message: {
        type: 'image_url',
        data: {
          url: imageUrl,
          caption: inputPrompt,
        },
      },
    };

    const gatewayResponse = await axios.post(
      'http://localhost:3000/api/v1/messages',
      gatewayPayload,
      {
        headers: {
          Authorization: `Bearer ${gatewayToken}`,
          'Content-Type': 'application/json',
        },
      }
    );

    console.log('✅ Selfie sent successfully!');
    console.log('Gateway Response:', gatewayResponse.data);
  } catch (error) {
    console.error('❌ Error during selfie generation:', error.message);
    throw error;
  }
}

// Command line argument parsing
if (require.main === module) {
  const args = process.argv.slice(2);
  
  // Check if required environment variables are set
  const apiKey = process.env.DASHSCOPE_API_KEY;
  const gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN;
  
  if (!apiKey) {
    console.error('❌ Error: DASHSCOPE_API_KEY environment variable is not set');
    console.error('💡 Solution: export DASHSCOPE_API_KEY=\'your_api_key_here\'');
    process.exit(1);
  }
  
  if (!gatewayToken) {
    console.error('❌ Error: OPENCLAW_GATEWAY_TOKEN environment variable is not set');
    console.error('💡 Solution: Run \'openclaw doctor --generate-gateway-token\' to generate one');
    process.exit(1);
  }

  // Default values
  let inputPrompt = '';
  let targetChannel = '#general';
  let mode: 'mirror' | 'direct' = 'mirror';

  // Parse arguments
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '-p':
      case '--prompt':
        inputPrompt = args[i + 1];
        i++;
        break;
      case '-c':
      case '--channel':
        targetChannel = args[i + 1];
        i++;
        break;
      case '-m':
      case '--mode':
        mode = args[i + 1] as 'mirror' | 'direct';
        i++;
        break;
      default:
        console.error(`Unknown option: ${args[i]}`);
        process.exit(1);
    }
  }

  // Validate inputs
  if (!inputPrompt) {
    console.error('❌ Error: No prompt provided');
    console.error(`Usage: ${process.argv[0]} ${process.argv[1]} -p "your prompt here" [-c target_channel] [-m mode]`);
    process.exit(1);
  }

  generateSuheSelfie(apiKey, gatewayToken, inputPrompt, targetChannel, mode).catch((error) => {
    console.error('Error:', error.message);
    process.exit(1);
  });
}

export { generateSuheSelfie };