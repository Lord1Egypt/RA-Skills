#!/usr/bin/env python3
"""Simple heuristic smart wrapper for Python
"""
import sys,subprocess,os
if len(sys.argv)<2:
    print('Usage: mimo_tts_smart.py "TEXT" [OUTPUT]')
    sys.exit(2)
text=sys.argv[1]
output=sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith('--') else os.path.join(os.getcwd(),'output.mock.ogg')
style=''
if any(k in text for k in ['诗','床前','李白']): style='温柔'
elif any(k in text for k in ['笑话','哈哈','笑']): style='开心'
elif any(k in text for k in ['晚安','宝宝']): style='温柔'
elif any(k in text for k in ['唱','歌']): style='唱歌'
elif any(k in text for k in ['东北','老铁','咋']): style='东北话'

# call python base implementation
base=os.path.join(os.path.dirname(__file__),'..','base','mimo_tts.py')
cmd=['python3',base,f'<style>{style}</style>'+text,output]
res=subprocess.run(cmd)
sys.exit(res.returncode)
