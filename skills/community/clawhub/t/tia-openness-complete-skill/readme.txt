tia-openness-complete-skill/
├── __init__.py                # OpenClaw入口
├── tia_core.py                 # TIA Openness核心封装（加载程序集、连接管理）
├── hardware.py                 # 硬件配置助手（设备类型定义）
├── block_generator.py          # 程序块生成器（根据描述生成SCL）
├── actions.py                  # 操作函数（创建项目、添加设备、创建块、编译、下载）
├── utils.py                    # 辅助工具（路径处理、注册表读取）
├── templates/                  # SCL代码模板
│   ├── ob_template.scl
│   ├── fb_template.scl
│   ├── fc_template.scl
│   └── db_template.scl
├── SKILL.md                    # 技能文档（元数据、参数说明、使用示例）
└── requirements.txt            # 依赖项


注意事项
首次运行时会弹出Openness防火墙确认，请点击“是”允许连接。

下载时需要正确的PG/PC接口名称，本技能默认使用第一个可用接口，如有多个请确保配置正确。

如果项目受密码保护，请使用UMAC参数（本技能暂未集成，可扩展）。

硬件目录路径可能因TIA版本不同而略有差异，请根据实际情况调整。