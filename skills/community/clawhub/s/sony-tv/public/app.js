const actions = {
  powerOn: '开机',
  powerOff: '关机',
  togglePower: '电源',
  up: '上',
  down: '下',
  left: '左',
  right: '右',
  confirm: '确认',
  home: '主页',
  exit: '退出',
  options: '选项',
  back: '返回',
  volumeUp: '音量 +',
  volumeDown: '音量 -',
  mute: '静音',
  channelUp: '频道 +',
  channelDown: '频道 -',
  play: '播放',
  pause: '暂停',
  stop: '停止',
  rewind: '快退',
  forward: '快进',
  hdmi1: 'HDMI 1',
  hdmi2: 'HDMI 2',
  hdmi3: 'HDMI 3',
  hdmi4: 'HDMI 4',
};

let feedbackTimeout = null;

function showFeedback(label) {
  const el = document.getElementById('feedback');
  el.textContent = label;
  el.classList.add('show');

  if (feedbackTimeout) clearTimeout(feedbackTimeout);
  feedbackTimeout = setTimeout(() => {
    el.classList.remove('show');
  }, 600);
}

async function sendAction(action) {
  try {
    const res = await fetch(`/api/${action}`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showFeedback(actions[action] || action);
    } else {
      showFeedback('发送失败');
      console.error('Action failed:', data.error);
    }
  } catch (err) {
    showFeedback('连接错误');
    console.error('Network error:', err);
  }
}

// Bind all buttons
document.querySelectorAll('[data-action]').forEach((btn) => {
  const action = btn.dataset.action;

  // Touch: fire immediately on touchstart for responsiveness
  btn.addEventListener('touchstart', (e) => {
    e.preventDefault();
    sendAction(action);
  }, { passive: false });

  // Mouse fallback
  btn.addEventListener('click', () => {
    sendAction(action);
  });

  // Long press for volume/channel repeat
  if (['volumeUp', 'volumeDown', 'channelUp', 'channelDown'].includes(action)) {
    let holdInterval = null;
    let holdTimeout = null;

    btn.addEventListener('touchstart', () => {
      holdTimeout = setTimeout(() => {
        holdInterval = setInterval(() => sendAction(action), 200);
      }, 500);
    });

    const stopHold = () => {
      if (holdTimeout) clearTimeout(holdTimeout);
      if (holdInterval) clearInterval(holdInterval);
      holdTimeout = null;
      holdInterval = null;
    };

    btn.addEventListener('touchend', stopHold);
    btn.addEventListener('touchcancel', stopHold);
  }
});

// Fetch volume on load
async function loadVolume() {
  try {
    const res = await fetch('/api/volume');
    const data = await res.json();
    if (data.success && data.result?.result?.[0]) {
      const vol = data.result.result[0][0];
      document.getElementById('volumeText').textContent = vol.volume ?? '--';
    }
  } catch {
    // Ignore volume errors on load
  }
}

// Update volume periodically
loadVolume();
setInterval(loadVolume, 10000);

// Open diagnostic page on the TV
async function openDiag() {
  const localIP = await getLocalIP();
  const diagURL = `http://${localIP}:3000/diag.html`;

  // Send to TV via appControl API
  try {
    const res = await fetch('/api/openURL', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: diagURL })
    });
    const data = await res.json();
    if (data.success) {
      showFeedback('已发送诊断页面');
    } else {
      showFeedback('发送失败: ' + (data.error || '未知'));
    }
  } catch (err) {
    showFeedback('网络错误');
  }
}

async function getLocalIP() {
  try {
    const res = await fetch('/api/localIP');
    const data = await res.json();
    return data.ip || window.location.hostname;
  } catch {
    return window.location.hostname;
  }
}
