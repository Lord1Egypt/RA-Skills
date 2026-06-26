#!/usr/bin/env python3
"""
企业微信消息加解密模块
=======================
基于企业微信官方 Python 加解密库实现。
参考: https://developer.work.weixin.qq.com/document/path/96211

提供三个核心功能：
  1. VerifyURL - 验证回调URL（GET请求）
  2. DecryptMsg - 解密接收到的消息（POST请求）
  3. EncryptMsg - 加密回复消息
"""

import base64
import hashlib
import hmac
import struct
import time
import socket
import xml.etree.cElementTree as ET
from Crypto.Cipher import AES


class FormatError(Exception):
    pass


class WXBizMsgCrypt:
    """企业微信消息加解密类"""

    def __init__(self, sToken, sEncodingAESKey, sCorpId):
        self.token = sToken
        self.corp_id = sCorpId
        try:
            self.aes_key = base64.b64decode(sEncodingAESKey + "=")
            assert len(self.aes_key) == 32
        except Exception:
            raise FormatError(f"EncodingAESKey 格式错误（应为43个字符）: 实际长度 {len(sEncodingAESKey)}")

    def _get_signature(self, timestamp, nonce, encrypt):
        """计算签名"""
        sort_list = sorted([self.token, timestamp, nonce, encrypt])
        sha = hashlib.sha1()
        sha.update("".join(sort_list).encode("utf-8"))
        return sha.hexdigest()

    def _encrypt(self, text):
        """AES加密"""
        text = text.encode("utf-8")
        # 16字节随机字符串
        random_str = self._get_random_str()
        # 网络字节序打包消息长度
        msg_len = struct.pack("!I", len(text))
        # 拼接
        plaintext = random_str + msg_len + text + self.corp_id.encode("utf-8")
        # PKCS#7填充
        pad_len = 32 - (len(plaintext) % 32)
        plaintext += bytes([pad_len] * pad_len)
        # AES-CBC加密
        iv = self.aes_key[:16]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(plaintext)
        return base64.b64encode(encrypted).decode("utf-8")

    def _decrypt(self, text):
        """AES解密"""
        try:
            cipher_text = base64.b64decode(text)
            iv = self.aes_key[:16]
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(cipher_text)
            # 去PKCS#7填充
            pad = decrypted[-1]
            if isinstance(pad, int):
                content = decrypted[:-pad]
            else:
                content = decrypted[:-ord(pad)]
            # 解析：16字节随机 + 4字节长度 + 消息 + CorpId
            msg_len = struct.unpack("!I", content[16:20])[0]
            msg = content[20:20 + msg_len]
            from_corp_id = content[20 + msg_len:]
            if from_corp_id.decode("utf-8") != self.corp_id:
                raise FormatError(f"CorpId不匹配: {from_corp_id.decode('utf-8')} != {self.corp_id}")
            return msg.decode("utf-8")
        except FormatError:
            raise
        except Exception as e:
            raise FormatError(f"消息解密失败: {e}")

    def _get_random_str(self):
        """生成16字节随机字符串"""
        import os
        return os.urandom(16)

    def VerifyURL(self, sMsgSignature, sTimeStamp, sNonce, sEchoStr):
        """
        验证回调URL
        企业微信在配置回调URL时会发送GET请求，需要返回解密后的echostr

        Returns:
            (0, sReplyEchoStr) 或 (errcode, None)
        """
        signature = self._get_signature(sTimeStamp, sNonce, sEchoStr)
        if signature != sMsgSignature:
            return -1, None
        try:
            reply = self._decrypt(sEchoStr)
            return 0, reply
        except Exception as e:
            return -1, str(e)

    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce):
        """
        解密接收到的消息

        Args:
            sPostData: POST请求体（XML格式）
            sMsgSignature: URL参数 msg_signature
            sTimeStamp: URL参数 timestamp
            sNonce: URL参数 nonce

        Returns:
            (0, xml_content_str) 或 (errcode, None)
        """
        try:
            tree = ET.fromstring(sPostData)
            encrypt = tree.find("Encrypt").text
        except Exception as e:
            return -1, f"XML解析失败: {e}"

        signature = self._get_signature(sTimeStamp, sNonce, encrypt)
        if signature != sMsgSignature:
            return -1, "签名验证失败"

        try:
            content = self._decrypt(encrypt)
            return 0, content
        except Exception as e:
            return -1, str(e)

    def EncryptMsg(self, sReplyMsg, sNonce, timestamp=None):
        """
        加密回复消息

        Args:
            sReplyMsg: 回复消息明文（XML格式）
            sNonce: 随机字符串
            timestamp: 时间戳

        Returns:
            (0, encrypted_xml) 或 (errcode, None)
        """
        if timestamp is None:
            timestamp = str(int(time.time()))

        try:
            encrypt = self._encrypt(sReplyMsg)
        except Exception as e:
            return -1, str(e)

        signature = self._get_signature(timestamp, sNonce, encrypt)

        resp_xml = f"""<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{sNonce}]]></Nonce>
</xml>"""
        return 0, resp_xml
