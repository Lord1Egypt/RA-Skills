# -*- coding: utf-8 -*-
"""
读取同花顺指标说明文件
"""
import os
import glob

path = r'D:\同花顺远航版\bin\modules\document\series_pack'
files = glob.glob(os.path.join(path, '*.txt'))

print("=" * 60)
print("同花顺指标文件列表")
print("=" * 60)

for f in sorted(files):
    try:
        # 读取文件内容
        with open(f, 'rb') as file:
            data = file.read(1000)
        
        # 尝试用GBK解码文件名
        filename = os.path.basename(f)
        try:
            decoded_name = filename.encode('latin1').decode('gbk')
        except:
            decoded_name = filename
        
        # 只显示资金相关文件
        if any(keyword in decoded_name for keyword in ['资金', '主力', '吸货', '抄底', '仓位']):
            print(f"\n【{decoded_name}】")
            
            # 尝试解码内容
            try:
                content = data.decode('gbk', errors='ignore')
                print(content[:500])
            except:
                print("(内容解码失败)")
    except Exception as e:
        pass

print("\n" + "=" * 60)