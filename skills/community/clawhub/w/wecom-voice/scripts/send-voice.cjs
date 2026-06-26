const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const USERPROFILE = process.env.USERPROFILE || process.env.HOME;
const MEDIA_DIR = path.join(USERPROFILE, '.openclaw', 'media', 'inbound');
const FFMPEG = path.join(USERPROFILE, 'AppData', 'Local', 'Microsoft', 'WinGet', 'Packages', 'Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe', 'ffmpeg-8.1-full_build', 'bin', 'ffmpeg.exe');

const text = process.argv[2] || 'hello';
const targetUser = process.argv[3] || 'FanQi';

const timestamp = Date.now();
const wavFile = path.join(MEDIA_DIR, `voice-${timestamp}.wav`);
const amrFile = path.join(MEDIA_DIR, `voice-${timestamp}.amr`);

console.log('=== WeCom Voice ===');
console.log('Text:', text);

// 1. Generate WAV using PowerShell with BOM
console.log('[1/3] TTS...');

const ps1Content = `
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.SelectVoice("Microsoft Huihui Desktop")
$synth.SetOutputToWaveFile("${wavFile.replace(/\\/g, '\\\\')}")
$synth.Speak("PLACEHOLDER")
$synth.Dispose()
`.replace('PLACEHOLDER', text);

// Write with UTF-8 BOM
const BOM = '\uFEFF';
const ps1File = path.join(MEDIA_DIR, 'temp-tts.ps1');
fs.writeFileSync(ps1File, BOM + ps1Content, 'utf8');

try {
  execSync(`powershell -ExecutionPolicy Bypass -File "${ps1File}"`, { encoding: 'utf8' });
  // Clean up
  try { fs.unlinkSync(ps1File); } catch {}
} catch (err) {
  console.error('TTS failed');
  try { fs.unlinkSync(ps1File); } catch {}
  process.exit(1);
}

if (!fs.existsSync(wavFile)) {
  console.error('WAV not created');
  process.exit(1);
}

console.log('WAV:', fs.statSync(wavFile).size, 'bytes');

// 2. Convert to AMR
console.log('[2/3] AMR...');
try {
  execSync(`"${FFMPEG}" -i "${wavFile}" -ar 8000 -ac 1 -ab 12.2k "${amrFile}" -y`, { encoding: 'utf8' });
} catch (err) {
  console.error('FFmpeg failed');
  process.exit(1);
}

console.log('AMR:', fs.statSync(amrFile).size, 'bytes');

// 3. Send
console.log('[3/3] Send...');
try {
  execSync(`openclaw message send -t "${targetUser}" --channel wecom --media "${amrFile}"`, { encoding: 'utf8' });
  console.log('Done!');
} catch (err) {
  console.error('Send failed');
  process.exit(1);
}