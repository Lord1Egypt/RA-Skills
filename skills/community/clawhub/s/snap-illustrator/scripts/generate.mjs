import fs from 'fs/promises';
import path from 'path';

// Note: Using native fetch if available (Node 18+), otherwise would need node-fetch
// For maximum compatibility in scripts run by CLI
async function generateWithPollinations(prompt, outputPath) {
    const encodedPrompt = encodeURIComponent(prompt);
    // Pollinations generates a new random seed by default, we add a random seed just in case
    const seed = Math.floor(Math.random() * 1000000);
    const url = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=1280&height=720&seed=${seed}&nologo=true`;
    
    console.log(`[Method: Pollinations.ai] Requesting image for prompt: "${prompt}"...`);
    const response = await fetch(url);
    
    if (!response.ok) {
        throw new Error(`Pollinations API error: ${response.status} ${response.statusText}`);
    }
    
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    
    // Ensure directory exists
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    await fs.writeFile(outputPath, buffer);
    console.log(`Successfully saved to ${outputPath}`);
    return true;
}

async function generateWithHuggingFace(prompt, outputPath, token) {
    const url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0";
    
    console.log(`[Method: HuggingFace] Requesting image for prompt: "${prompt}"...`);
    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ inputs: prompt })
    });
    
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HF API error: ${response.status} - ${errorText}`);
    }
    
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    
    // Ensure directory exists
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    await fs.writeFile(outputPath, buffer);
    console.log(`Successfully saved to ${outputPath}`);
    return true;
}

async function main() {
    const args = process.argv.slice(2);
    let prompt = "";
    let outputPath = "";
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--prompt' && i + 1 < args.length) {
            prompt = args[i + 1];
            i++;
        } else if (args[i] === '--output' && i + 1 < args.length) {
            outputPath = args[i + 1];
            i++;
        }
    }
    
    if (!prompt || !outputPath) {
        console.error("Usage: node generate.js --prompt \"<prompt>\" --output \"<path.png>\"");
        process.exit(1);
    }

    // Determine configuration path
    const configPath = path.join(process.env.HOME || process.env.USERPROFILE, '.config', 'snap-illustrator', 'config.json');
    let config = { provider: 'pollinations', hf_token: null };
    
    try {
        const configData = await fs.readFile(configPath, 'utf-8');
        config = JSON.parse(configData);
    } catch (e) {
        // Config file doesn't exist yet, we'll use default 'pollinations'
    }
    
    // Process based on config
    try {
        if (config.provider === 'huggingface' && config.hf_token) {
            await generateWithHuggingFace(prompt, outputPath, config.hf_token);
        } else {
            try {
                // Try Pollinations first
                await generateWithPollinations(prompt, outputPath);
            } catch (pollinationsError) {
                console.error(`Pollinations failed: ${pollinationsError.message}`);
                console.error("RATE_LIMIT_OR_ERROR: Trying fallback if HuggingFace token is available in env...");
                
                // Fallback to Env HF Token if available when Pollinations fails
                const envToken = process.env.HF_TOKEN;
                if (envToken) {
                    console.log("Found HF_TOKEN in environment, attempting fallback...");
                    await generateWithHuggingFace(prompt, outputPath, envToken);
                } else {
                    console.error("No HF_TOKEN found. PLEASE_ASK_USER_FOR_TOKEN");
                    process.exit(2); // Specific exit code to indicate we need token
                }
            }
        }
    } catch (error) {
        console.error(`Generation failed: ${error.message}`);
        console.error("PLEASE_ASK_USER_FOR_TOKEN"); // Signal to the LLM agent it should ask for a token
        process.exit(2);
    }
}

main();