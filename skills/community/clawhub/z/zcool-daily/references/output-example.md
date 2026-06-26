# 站酷每日热门作品推荐 - 输出示例

## 完整输出示例

```
📢 2026年03月20日 站酷热门设计作品推荐：

1. ❄️ [下雪的城市](https://www.zcool.com.cn/work/ZNzMyNDgwNTY=.html) - 孙无力
   🏷️ 类型：插画 | 🌟 温馨雪景插画，氛围感拉满

2. 🎨 [原创绘本《帽子镇99号》](https://www.zcool.com.cn/work/ZNzMyODA5MjA=.html) - Simon小火
   🏷️ 类型：插画 | 🌟 充满想象力的原创绘本角色设计

3. 📛 [GOOD TIME TEA 新中式茶饮品牌](https://www.zcool.com.cn/work/ZNzI5NDc4NDA=.html) - 伊昂杨杨杨杨杨
   🏷️ 类型：品牌设计 | 🌟 新中式茶饮视觉系统，质感出众

4. 🎵 [《大唐Gang》MV](https://www.zcool.com.cn/work/ZNzMyNTEwNTI=.html) - BIG王0911
   🏷️ 类型：视频/MV | 🌟 国风说唱 MV，视觉冲击力强

5. ⚔️ [云顶之弈神拳不朽李青CG](https://www.zcool.com.cn/work/ZNzMzMjg5MDQ=.html) - 两点十分动漫
   🏷️ 类型：动画 | 🌟 东方武学风格游戏 CG，武侠氛围浓厚

6. 🛵 [小牛电动车产品渲染](https://www.zcool.com.cn/work/ZNzMzMzAyOTI=.html) - 葡萄创意
   🏷️ 类型：3D | 🌟 产品级 3D 渲染，细节精致

7. 🎮 [《剑与远征启程》九尾pv](https://www.zcool.com.cn/work/ZNzMzMzUzMjQ=.html) - 萤火MicroFire
   🏷️ 类型：动画 | 🌟 游戏角色动画 PV，特效炸裂

8. 🦌 [Illustration to 3D conversion](https://www.zcool.com.cn/work/ZNzMzMzQwNzY=.html) - 鹿言
   🏷️ 类型：3D | 🌟 2D 转 3D 风格转换，视觉效果惊艳

9. 💧 [身体与水](https://www.zcool.com.cn/work/ZNzMzMTQ0NzY=.html) - 约翰强尼
   🏷️ 类型：插画 | 🌟 充满意象的创意作品

10. 📖 [《少年》文章插画](https://www.zcool.com.cn/work/ZNzMzMzQzODQ=.html) - Danton丹彤
    🏷️ 类型：插画 | 🌟 杂志文章配图，风格清新

---

📊 今日趋势：**插画(4) | 动画(2) | 3D(2) | 品牌设计(1) | 视频(1)**
```

## 格式说明

- **标题带链接**：作品名称可点击，直接跳转站酷详情页
- **类型标签**：AI绘画、插画、3D、动画、品牌设计、视频/MV 等
- **亮点描述**：基于作品标题和关键词自动生成的特色描述
- **趋势统计**：当日热门作品类型分布

## 运行命令

```bash
python3 scripts/zcool_daily.py
```

## 输出文件

作品列表保存至：`zcool_daily/zcool_{date}.txt`