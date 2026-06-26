module.exports = async (ctx) => {
    const text = ctx.message.text || "";
    if (text.startsWith('生成视频：')) {
        const prompt = text.replace('生成视频：', '').trim();
        const { spawn } = require('child_process');
        const path = require('path');
        
        // 修正为指向项目根目录下的 scripts/veo_worker.py
        const scriptPath = path.join(__dirname, 'model', 'scripts', 'veo_worker.py');
        
        const child = spawn('python', [scriptPath, '--prompt', prompt, '--model', 'veo3.1', '--seconds', '8'], {
            detached: true,
            stdio: 'ignore'
        });
        child.unref();
        
        return { reply: "正在后台为您生成视频，完成后会自动在浏览器打开。" };
    }
};