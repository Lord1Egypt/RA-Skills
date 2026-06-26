const fs = require('fs');
let content = fs.readFileSync('produce.js', 'utf8');

// 找到函数位置
const start = content.indexOf('function generateVideoCode(scenes, audioFiles)');
const end = content.indexOf('// ========== Step 5:');

if (start === -1 || end === -1) {
  console.log('Function not found');
  process.exit(1);
}

// 完全重写函数
const newFunc = `function generateVideoCode(scenes, audioFiles) {
  log('Step 4: 生成视频代码...');
  
  let currentFrame = 0;
  const sceneFrames = [];
  
  for (const scene of scenes) {
    const audio = audioFiles.find(a => a.id === scene.id);
    const duration = audio ? audio.duration : scene.duration || 3.0;
    const frames = Math.ceil(duration * CONFIG.fps);
    sceneFrames.push({ startFrame: currentFrame, duration: frames, ...scene });
    currentFrame += frames;
  }
  
  const totalFrames = currentFrame;
  log('视频总时长: ' + (totalFrames / CONFIG.fps).toFixed(1) + '秒 (' + totalFrames + '帧)');
  
  // 收集所有导入 - 使用ASCII名称
  const imports = [];
  let imgIndex = 0;
  sceneFrames.forEach((s, si) => {
    s.visual.elements.forEach(e => {
      if ((e.type === '素材' || e.type === '背景') && e.generatedPath) {
        const importName = 'bgimg' + imgIndex;
        imports.push({ path: e.generatedPath, name: importName, sceneIndex: si });
        imgIndex++;
      }
    });
  });
  
  // 生成导入代码
  const importCode = imports.map(imp => "import " + imp.name + " from '" + imp.path.replace(/\\\\\\\\/g, '/') + "';").join('\\n');
  
  // 生成场景代码
  const sceneCodeStr = sceneFrames.map((s, si) => {
    const titleColor = s.id === 0 ? "'#FFD700'" : "'white'";
    const titleSize = s.id === 0 ? '72' : '56';
    
    const bgElement = s.visual.elements.find(e => e.type === '背景' && e.generatedPath);
    const hasBg = !!bgElement;
    
    const materialElements = s.visual.elements.filter(e => e.type === '素材' && e.generatedPath);
    const featuredMaterial = materialElements.length > 0 ? materialElements[0] : null;
    
    const emojiEl = s.visual.elements.find(e => e.type === 'emoji');
    const emojiValue = emojiEl ? emojiEl.value : '📌';
    
    const textEl = s.visual.elements.find(e => e.type === '文字');
    const textValue = textEl ? textEl.value : s.title;
    
    const descEl = s.visual.elements.find(e => e.type === '描述');
    const descValue = descEl ? descEl.value : '';
    
    // 构建JSX
    let jsx = '';
    jsx += '    <>\\n';
    
    if (hasBg) {
      const imgName = imports.find(i => i.sceneIndex === si && i.path.includes('背景'))?.name || 'bg' + si;
      jsx += '      <img src={' + imgName + '} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: 0.3 }} />\\n';
    }
    
    if (featuredMaterial) {
      const imgName = imports.find(i => i.sceneIndex === si && i.path.includes('素材'))?.name || 'mat' + si;
      jsx += '      <img src={' + imgName + '} style={{ position: "absolute", width: 120, height: 120, objectFit: "contain", opacity: 0.85, right: 30, top: 80 }} />\\n';
    }
    
    jsx += '      <AbsoluteFill style={{ width: "100%", height: "100%", backgroundColor: "#0a0a0a", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", fontFamily: "Noto Color Emoji, sans-serif" }}>\\n';
    jsx += '        <div style={{ opacity: iconAnim.opacity, transform: "scale(" + iconAnim.scale + ")", fontSize: 160, marginBottom: 40, zIndex: 1 }}>' + emojiValue + '</div>\\n';
    jsx += '        <div style={{ opacity: titleAnim.opacity, transform: "translateY(" + titleAnim.translateY + "px)", fontSize: ' + titleSize + ", color: " + titleColor + ", fontWeight: '900', textAlign: 'center', padding: '0 60px', zIndex: 1 }}>" + textValue + '</div>\\n';
    
    if (descValue) {
      jsx += "        <div style={{ opacity: descAnim.opacity, transform: 'translateY(' + descAnim.translateY + 'px)', fontSize: 36, color: '#9ca3af', marginTop: 30, textAlign: 'center', padding: '0 40px', zIndex: 1 }}>" + descValue + '</div>\\n';
    }
    
    jsx += '      </AbsoluteFill>\\n';
    jsx += '    </>\\n';
    
    return "// Scene" + s.id + "\\n" +
"const Scene" + s.id + " = () => {\\n" +
"  const frame = useCurrentFrame();\\n" +
"  const f = frame - " + s.startFrame + ";\\n" +
"  const iconAnim = popIn(f, 0);\\n" +
"  const titleAnim = fadeSlideUp(f, 25);\\n" +
"  const descAnim = fadeSlideUp(f, 50);\\n" +
"  return (\\n" + jsx + "  );\\n" +
"};\\n";
  }).join('\\n');
  
  // switch
  const switchCode = sceneFrames.map((s, i) => 
    i === 0 
      ? "if (frame < " + s.duration + ") return <Scene" + s.id + " />;"
      : "if (frame < " + (s.startFrame + s.duration) + ") return <Scene" + s.id + " />;"
  ).join('\\n  ');
  
  const code = "import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';\\n" +
"import React from 'react';\\n" +
importCode + "\\n\\n" +
"const popIn = (frame, delay) => {\\n" +
"  const progress = Math.max(0, Math.min(1, (frame - delay) / 15));\\n" +
"  const scale = 0.5 + progress * 0.5;\\n" +
"  return { scale, opacity: progress };\\n" +
"};\\n\\n" +
"const fadeSlideUp = (frame, delay, duration) => {\\n" +
"  const d = duration || 20;\\n" +
"  const progress = Math.max(0, Math.min(1, (frame - delay) / d));\\n" +
"  return { opacity: progress, translateY: interpolate(progress, [0, 1], [30, 0]) };\\n" +
"};\\n\\n" +
sceneCodeStr + "\\n\\n" +
"export const Video = () => {\\n" +
"  const frame = useCurrentFrame();\\n" +
"  " + switchCode + "\\n" +
"  return <Scene" + sceneFrames[sceneFrames.length - 1].id + " />;\\n" +
"};\\n";

  return { code, totalFrames };
}
`;

content = content.substring(0, start) + newFunc + content.substring(end);
fs.writeFileSync('produce.js', content);
console.log('Fixed!');
