def fix_monitor_web():
    import re
    
    with open('/home/fangjinan/.openclaw/workspace/skills/video-note-maker/monitor_web.py', 'r') as f:
        content = f.read()
    
    # 修复 updateStatusElement 函数
    old_code = '''        function updateStatusElement(prefix, data) {
            const statusDot = document.getElementById(prefix + '-status .status-dot');
            const statusText = document.getElementById(prefix + '-status .status-text');
            const progressFill = document.getElementById(prefix + '-progress');
            const progressText = document.getElementById(prefix + '-text');
            
            statusDot.className = 'status-dot ' + data.status;
            statusText.textContent = data.text;
            progressFill.style.width = data.progress + '%';
            progressText.textContent = data.text;
        }'''
    
    new_code = '''        function updateStatusElement(prefix, data) {
            const statusDot = document.querySelector('#' + prefix + '-status .status-dot');
            const statusText = document.querySelector('#' + prefix + '-status .status-text');
            const progressFill = document.querySelector('#' + prefix + '-progress');
            const progressText = document.querySelector('#' + prefix + '-text');
            
            if (statusDot) statusDot.className = 'status-dot ' + data.status;
            if (statusText) statusText.textContent = data.text;
            if (progressFill) progressFill.style.width = data.progress + '%';
            if (progressText) progressText.textContent = data.text;
        }'''
    
    content = content.replace(old_code, new_code)
    
    with open('/home/fangjinan/.openclaw/workspace/skills/video-note-maker/monitor_web.py', 'w') as f:
        f.write(content)
    
    print('修改完成!')

if __name__ == '__main__':
    fix_monitor_web()
