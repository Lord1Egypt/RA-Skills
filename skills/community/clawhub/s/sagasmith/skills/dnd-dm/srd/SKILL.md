# SRD 5.2.1 source corpus

本目录保存 D&D 5e 2024 SRD 5.2.1 的 20 个 CC-BY-4.0 Markdown 来源文件。运行时检索
使用数据库层级索引，不直接扫描文件。

初始化或增量更新：

```powershell
python -m <domain-cli> rules ingest-srd
```

该命令解析标题层级与字符位置，生成检索块，并用 `BAAI/bge-m3` 创建 1024 维归一化
Dense Vector。内容 checksum 未变化时跳过重建。

查看层级和索引状态：

```powershell
python -m <domain-cli> rules tree
python -m <domain-cli> rules status
```

来源文件映射：

- `001-018`：基础玩法、动作、探索与战斗
- `019-086`：职业、起源与专长
- `087-103`：装备、武器、护甲与工具
- `104-175`：施法规则与法术
- `176-191`：规则术语和状态
- `192-252`：玩法工具箱与魔法物品
- `253-364`：怪物与动物
