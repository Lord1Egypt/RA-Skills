"""
config.py - 过滤规则配置
定义哪些群/公众号应该被过滤掉

路径说明：
- 解密数据固定在 C:\wechat-decrypt\decrypted（wechat-decrypt 官方路径）
- 画像存储在 Skill 目录下 storage/cold/另一个我/
"""
from pathlib import Path

# 微信数据库根目录（wechat-decrypt 固定安装位置）
DECRYPTED_BASE = Path(r"C:\wechat-decrypt\decrypted")

# Skill 工作目录（自动检测当前目录）
_SKILL_ROOT = Path(__file__).parent.parent.resolve()
STORAGE_DIR = _SKILL_ROOT / "storage" / "cold" / "另一个我"

# 垃圾群/公众号关键词（包含这些的直接过滤）
JUNK_PATTERNS = [
    # 营销/福利群
    '家教', '福利', '外卖', '红包', '优惠券', '团购', '秒杀',
    '寿喜烧', '吃喝玩乐', '同城家教', '回收家教', 'Steam',
    'DD机器人', '外卖券', '霸王餐', '餐福利',
    '奶茶', '咖啡', '蛋糕', '零食', '水果', '鲜花',
    '滴滴', '打车', '出行', '出行红包',
    '邀请', '进群', '拼多多', 'PDD', '淘客',
    # 商业推送
    '论文', '辅导', '硕博', 'SCI',
    'AI', '运营', '龙虾', '课程', '知识付费',
    '美美星期四', '精准养护', '积分翻倍',
    '中小学', '安全教育', '长护服务', '定点',
    # 机器人号
    '福利君', '优惠券', '机器人',
]

# 公众号前缀（直接过滤）
PUBLIC_PREFIXES = [
    'gh_', 'brandsessionholder', 'notifymessage',
    '@placeholder', 'filehelper',
]

# 消息类型映射
MSG_TYPE_MAP = {
    1: '文本',
    3: '图片',
    34: '语音',
    43: '视频',
    47: '表情包/媒体',
    49: '链接/文件',
    10000: '系统消息',
}
