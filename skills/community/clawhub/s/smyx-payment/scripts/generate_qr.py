#!/usr/bin/env python3
"""
生成支付宝收款码
根据订单信息生成支付宝收款二维码图片
"""

import qrcode
import sys
import os

def generate_alipay_qr(pay_url, output_path='alipay_qr.png'):
    """
    生成支付宝收款码
    
    Args:
        pay_url: 支付宝支付链接
        output_path: 输出图片路径
    """
    try:
        # 创建二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pay_url)
        qr.make(fit=True)
        
        # 生成图片
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 保存图片
        img.save(output_path)
        
        print(f"✅ 收款码已生成：{output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 生成收款码失败：{e}")
        return None


if __name__ == "__main__":
    # 测试
    if len(sys.argv) > 1:
        pay_url = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else 'alipay_qr.png'
        generate_alipay_qr(pay_url, output_path)
    else:
        # 默认测试
        test_url = "https://openapi.alipay.com/gateway.do?app_id=2021006150611467&test=1"
        generate_alipay_qr(test_url, 'test_qr.png')
