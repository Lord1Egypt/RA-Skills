"""
飞书通知模块

功能：
- 格式化待审核消息
- 支持飞书推送（通过 OpenClaw 或 Webhook）

使用方法：
    from feishu_notify import FeishuNotifier
    
    notifier = FeishuNotifier(use_openclaw=True)
    notifier.send_pending_review(pending_item)
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FeishuNotifier:
    """
    飞书通知器
    
    负责格式化并推送审核消息到飞书。
    支持两种模式：
    - OpenClaw 内置推送（推荐）
    - Webhook 推送（备用）
    
    Attributes:
        use_openclaw: 是否使用 OpenClaw 内置推送
        webhook_url: Webhook URL（备用模式）
        target_user: 目标用户/群组 ID
    """
    
    def __init__(self, use_openclaw: bool = True, webhook_url: str = None, target_user: str = None):
        """
        初始化通知器
        
        Args:
            use_openclaw: 是否使用 OpenClaw 内置推送
            webhook_url: Webhook URL（备用）
            target_user: 目标用户/群组 ID
        """
        self.use_openclaw = use_openclaw
        self.webhook_url = webhook_url
        self.target_user = target_user
    
    def format_pending_message(self, pending_item: dict) -> str:
        """
        格式化待审核消息
        
        Args:
            pending_item: 待审核项字典
            
        Returns:
            格式化后的消息文本
        """
        title = pending_item['title']
        heat = pending_item.get('heat', 0)
        url = pending_item['url']
        draft = pending_item['draft']
        pending_id = pending_item['id']
        
        # 截断草稿预览（前400字）
        draft_preview = draft[:400] + "..." if len(draft) > 400 else draft
        
        return f"""📋 **知乎回答待审核**

**问题：** {title}
**热度：** {heat}万  
**链接：** {url}

---

**回答草稿（{len(draft)}字）：**
{draft_preview}

---

**待审核ID：** `{pending_id}`

💡 **操作方式：**
• 复制内容到知乎发布
• 回复 "查看 {pending_id}" 查看完整草稿
"""
    
    def format_full_draft(self, pending_item: dict) -> str:
        """
        格式化完整草稿消息
        
        Args:
            pending_item: 待审核项字典
            
        Returns:
            包含完整草稿的消息文本
        """
        draft = pending_item['draft']
        
        return f"""📄 **完整草稿**

**问题：** {pending_item['title']}
**ID：** `{pending_item['id']}`

---

{draft}

---

💡 **操作：** 复制上方内容到知乎发布
"""


# 快捷函数
def format_pending_review(pending_item: dict) -> str:
    """
    格式化待审核消息的快捷函数
    
    Args:
        pending_item: 待审核项字典
        
    Returns:
        格式化后的消息文本
    """
    notifier = FeishuNotifier()
    return notifier.format_pending_message(pending_item)


def format_full_draft(pending_item: dict) -> str:
    """
    格式化完整草稿的快捷函数
    
    Args:
        pending_item: 待审核项字典
        
    Returns:
        包含完整草稿的消息文本
    """
    notifier = FeishuNotifier()
    return notifier.format_full_draft(pending_item)
