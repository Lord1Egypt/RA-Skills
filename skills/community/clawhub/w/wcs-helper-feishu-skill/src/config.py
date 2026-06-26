"""
配置项定义模块
定义所有支持的飞书插件配置选项
"""

from src.types import ConfigOption, ConfigSection


# 所有配置选项
CONFIG_OPTIONS = [
    # 流式输出
    ConfigOption(
        value='streaming_on',
        label='开启流式输出',
        command='openclaw config set channels.feishu.streaming true',
        description='AI回复时逐字显示，体验更流畅',
        requires_restart=True,
        config_key='streaming',
        enabled_value=True
    ),
    ConfigOption(
        value='streaming_off',
        label='关闭流式输出',
        command='openclaw config set channels.feishu.streaming false',
        description='一次性返回完整回复',
        requires_restart=True,
        config_key='streaming',
        enabled_value=False
    ),

    # 多任务并行
    ConfigOption(
        value='thread_on',
        label='开启多任务并行',
        command='openclaw config set channels.feishu.threadSession true',
        description='每个话题独立上下文，可同时处理多个任务',
        requires_restart=True,
        config_key='threadSession',
        enabled_value=True
    ),
    ConfigOption(
        value='thread_off',
        label='关闭多任务并行',
        command='openclaw config set channels.feishu.threadSession false',
        description='所有对话共享同一个上下文',
        requires_restart=True,
        config_key='threadSession',
        enabled_value=False
    ),

    # 群聊模式
    ConfigOption(
        value='mention_on',
        label='仅@机器人回复',
        command='openclaw config set channels.feishu.requireMention true --json',
        description='只有@机器人时才回复，适合大群',
        requires_restart=True,
        config_key='requireMention',
        enabled_value=True
    ),
    ConfigOption(
        value='mention_off',
        label='全部消息回复',
        command='openclaw config set channels.feishu.requireMention false --json',
        description='群内所有消息都回复，需要申请权限',
        requires_restart=True,
        required_permission='im:message.group_msg',
        warning='⚠️ 此模式需要先在飞书开放平台申请 im:message.group_msg 权限，\n开启后机器人在群内会回复所有消息，请注意避免刷屏。',
        config_key='requireMention',
        enabled_value=False
    ),

    # 卡片样式 - 耗时显示
    ConfigOption(
        value='footer_elapsed_on',
        label='开启耗时显示',
        command='openclaw config set channels.feishu.footer.elapsed true',
        description='在卡片底部显示处理耗时',
        requires_restart=False,
        config_key='footer.elapsed',
        enabled_value=True
    ),
    ConfigOption(
        value='footer_elapsed_off',
        label='关闭耗时显示',
        command='openclaw config set channels.feishu.footer.elapsed false',
        description='不显示处理耗时',
        requires_restart=False,
        config_key='footer.elapsed',
        enabled_value=False
    ),

    # 卡片样式 - 状态显示
    ConfigOption(
        value='footer_status_on',
        label='开启状态展示',
        command='openclaw config set channels.feishu.footer.status true',
        description='在卡片底部显示处理状态',
        requires_restart=False,
        config_key='footer.status',
        enabled_value=True
    ),
    ConfigOption(
        value='footer_status_off',
        label='关闭状态展示',
        command='openclaw config set channels.feishu.footer.status false',
        description='不显示处理状态',
        requires_restart=False,
        config_key='footer.status',
        enabled_value=False
    )
]


# 配置分组
CONFIG_SECTIONS = [
    ConfigSection(
        title='💬 回复体验',
        options=['streaming_on', 'streaming_off']
    ),
    ConfigSection(
        title='🧵 并行处理',
        options=['thread_on', 'thread_off']
    ),
    ConfigSection(
        title='👥 群聊模式',
        options=['mention_on', 'mention_off']
    ),
    ConfigSection(
        title='📊 卡片样式',
        options=['footer_elapsed_on', 'footer_elapsed_off', 'footer_status_on', 'footer_status_off']
    )
]
