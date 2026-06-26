// scripts/01_list_devices.js
// Lists all audio input/output devices via ffmpeg.
// Run: node scripts/01_list_devices.js
// Copy the exact VB-Cable device name into your .env as VIRTUAL_CABLE_NAME

const { execSync } = require('child_process')
const os = require('os')

function listDevices() {
  const platform = os.platform()
  let cmd

  if (platform === 'win32') {
    cmd = 'ffmpeg -list_devices true -f dshow -i dummy 2>&1'
  } else if (platform === 'darwin') {
    cmd = 'ffmpeg -f avfoundation -list_devices true -i "" 2>&1'
  } else {
    cmd = 'ffmpeg -f alsa -list_devices true -i dummy 2>&1 || pactl list sources short 2>&1'
  }

  let output
  try {
    output = execSync(cmd, { encoding: 'utf8' })
  } catch (e) {
    // ffmpeg exits non-zero when listing devices — that's expected
    output = e.stdout + e.stderr
  }

  console.log('\n=== Available Audio Devices ===\n')
  console.log(output)

  console.log('\n=== Instructions ===')
  console.log('1. Find the "CABLE Input" or "BlackHole" entry above.')
  console.log('2. Copy the exact device name string (including quotes if shown).')
  console.log('3. Add to your .env:')
  console.log('   VIRTUAL_CABLE_NAME=CABLE Input (VB-Audio Virtual Cable)')
  console.log('\nNote: Use the Output device name for Google Meet mic setting.')
  console.log('      Use the Input device name for VIRTUAL_CABLE_NAME in .env.\n')
}

listDevices()