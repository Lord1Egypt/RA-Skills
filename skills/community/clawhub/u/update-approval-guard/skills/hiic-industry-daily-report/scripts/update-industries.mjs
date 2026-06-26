#!/usr/bin/env node
/**
 * 更新深圳20+8产业配置文件
 */

import { writeFileSync, readdirSync, unlinkSync, existsSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const industriesDir = join(__dirname, '..', 'references', 'industries');

// 深圳20+8产业集群配置（正确版本）
const industries = [
  // 战略性新兴产业（8个）
  {
    id: "01",
    name: "半导体与集成电路",
    category: "战略性新兴产业",
    keywords: ["半导体", "集成电路", "芯片", "光刻机", "晶圆", "半导体设备", "国产芯片"],
    emoji: "⚡"
  },
  {
    id: "02",
    name: "人工智能",
    category: "战略性新兴产业",
    keywords: ["人工智能", "AI", "大模型", "GPT", "机器学习", "深度学习", "自然语言处理"],
    emoji: "🤖"
  },
  {
    id: "03",
    name: "网络与通信",
    category: "战略性新兴产业",
    keywords: ["5G", "6G", "网络通信", "基站", "光纤通信", "物联网", "通信技术"],
    emoji: "📡"
  },
  {
    id: "04",
    name: "超高清视频显示",
    category: "战略性新兴产业",
    keywords: ["超高清视频", "8K", "4K", "显示技术", "OLED", "Mini LED", "Micro LED"],
    emoji: "📺"
  },
  {
    id: "05",
    name: "智能终端",
    category: "战略性新兴产业",
    keywords: ["智能终端", "智能手机", "可穿戴设备", "AR眼镜", "VR设备", "智能家居"],
    emoji: "📱"
  },
  {
    id: "06",
    name: "智能传感器",
    category: "战略性新兴产业",
    keywords: ["传感器", "智能传感", "MEMS", "激光雷达", "毫米波雷达", "传感器芯片"],
    emoji: "🔬"
  },
  {
    id: "07",
    name: "软件与信息服务",
    category: "战略性新兴产业",
    keywords: ["软件", "SaaS", "云计算", "企业服务", "数字化转型", "工业软件"],
    emoji: "💻"
  },
  {
    id: "08",
    name: "数字创意",
    category: "战略性新兴产业",
    keywords: ["数字创意", "游戏", "动漫", "数字媒体", "虚拟人", "元宇宙", "数字内容"],
    emoji: "🎨"
  },
  
  // 先进制造业（8个）
  {
    id: "09",
    name: "高端装备与仪器",
    category: "先进制造业",
    keywords: ["高端装备", "数控机床", "工业母机", "精密制造", "测量仪器", "检测设备"],
    emoji: "⚙️"
  },
  {
    id: "10",
    name: "低空经济与空天",
    category: "先进制造业",
    keywords: ["低空经济", "无人机", "eVTOL", "通用航空", "卫星", "火箭", "航空航天"],
    emoji: "🚀"
  },
  {
    id: "11",
    name: "机器人",
    category: "先进制造业",
    keywords: ["机器人", "工业机器人", "服务机器人", "协作机器人", "机器人集成"],
    emoji: "🤖"
  },
  {
    id: "12",
    name: "智能机器人",
    category: "先进制造业",
    keywords: ["智能机器人", "人形机器人", "AI机器人", "智能协作机器人", "具身智能"],
    emoji: "🤖"
  },
  {
    id: "13",
    name: "现代时尚",
    category: "先进制造业",
    keywords: ["现代时尚", "服装设计", "时尚品牌", "珠宝首饰", "潮流文化", "时尚科技"],
    emoji: "👗"
  },
  {
    id: "14",
    name: "安全节能环保",
    category: "先进制造业",
    keywords: ["安全节能环保", "环保技术", "碳中和技术", "污染治理", "节能设备", "环保装备"],
    emoji: "🌱"
  },
  {
    id: "15",
    name: "新能源",
    category: "先进制造业",
    keywords: ["新能源", "光伏", "风电", "储能", "锂电池", "固态电池", "氢能"],
    emoji: "⚡"
  },
  {
    id: "16",
    name: "智能网联汽车",
    category: "先进制造业",
    keywords: ["智能网联汽车", "自动驾驶", "新能源汽车", "车联网", "智能座舱", "电动化"],
    emoji: "🚗"
  },
  
  // 未来产业（12个）
  {
    id: "17",
    name: "量子信息",
    category: "未来产业",
    keywords: ["量子信息", "量子计算", "量子通信", "量子测量", "量子芯片"],
    emoji: "🔮"
  },
  {
    id: "18",
    name: "光载信息",
    category: "未来产业",
    keywords: ["光载信息", "光通信", "光计算", "光芯片", "硅光技术"],
    emoji: "💡"
  },
  {
    id: "19",
    name: "高性能材料",
    category: "未来产业",
    keywords: ["高性能材料", "新材料", "石墨烯", "碳纤维", "复合材料", "特种材料"],
    emoji: "🧪"
  },
  {
    id: "20",
    name: "前沿新材料",
    category: "未来产业",
    keywords: ["前沿材料", "纳米材料", "超导材料", "智能材料", "仿生材料"],
    emoji: "🔬"
  },
  {
    id: "21",
    name: "海洋产业",
    category: "未来产业",
    keywords: ["海洋产业", "海洋工程", "深海装备", "海洋生物", "海上风电", "海洋资源"],
    emoji: "🌊"
  },
  {
    id: "22",
    name: "深地深海",
    category: "未来产业",
    keywords: ["深地深海", "深海探测", "深海采矿", "海底资源", "深海装备"],
    emoji: "🌊"
  },
  {
    id: "23",
    name: "生物医药",
    category: "未来产业",
    keywords: ["生物医药", "创新药", "新药研发", "基因治疗", "抗体药物", "临床试验"],
    emoji: "🧬"
  },
  {
    id: "24",
    name: "高端医疗器械",
    category: "未来产业",
    keywords: ["高端医疗器械", "医疗设备", "影像设备", "手术机器人", "IVD", "高端耗材"],
    emoji: "🏥"
  },
  {
    id: "25",
    name: "大健康",
    category: "未来产业",
    keywords: ["大健康", "健康管理", "医疗健康", "康复医疗", "养老产业", "健康科技"],
    emoji: "💊"
  },
  {
    id: "26",
    name: "生物制造",
    category: "未来产业",
    keywords: ["生物制造", "合成生物", "生物化工", "生物材料", "细胞工厂"],
    emoji: "🧫"
  },
  {
    id: "27",
    name: "脑科学与脑机工程",
    category: "未来产业",
    keywords: ["脑科学", "脑机接口", "脑机工程", "神经工程", "神经调控"],
    emoji: "🧠"
  },
  {
    id: "28",
    name: "细胞与基因",
    category: "未来产业",
    keywords: ["细胞治疗", "基因编辑", "基因治疗", "CAR-T", "干细胞", "基因测序"],
    emoji: "🧬"
  }
];

// 生成配置文件
function generateConfig(industry) {
  return {
    id: industry.id,
    name: industry.name,
    category: industry.category,
    keywords: industry.keywords,
    exclude: ["招聘", "求职", "简历", "培训课程", "出售"],
    searchSettings: {
      maxResults: 10,
      days: 1,
      language: "zh-CN"
    },
    schedule: {
      default: "daily",
      time: "09:00",
      timezone: "Asia/Shanghai"
    },
    output: {
      format: "markdown",
      emoji: industry.emoji,
      maxDescriptionLength: 200
    }
  };
}

// 创建目录
try {
  mkdirSync(industriesDir, { recursive: true });
} catch (err) {
  // 目录已存在
}

// 删除旧配置文件
if (existsSync(industriesDir)) {
  const oldFiles = readdirSync(industriesDir).filter(f => f.endsWith('.json'));
  for (const file of oldFiles) {
    try {
      unlinkSync(join(industriesDir, file));
      console.log(`🗑️  删除旧文件: ${file}`);
    } catch (err) {
      console.error(`❌ 删除失败: ${file}`);
    }
  }
}

// 生成新配置文件
let count = 0;
for (const industry of industries) {
  const config = generateConfig(industry);
  const filename = `${industry.id}-${industry.name}.json`;
  const filepath = join(industriesDir, filename);
  
  try {
    writeFileSync(filepath, JSON.stringify(config, null, 2), 'utf-8');
    console.log(`✅ ${industry.id}. ${industry.name} ${industry.emoji}`);
    count++;
  } catch (err) {
    console.error(`❌ ${industry.id}. ${industry.name}: ${err.message}`);
  }
}

console.log(`\n🎉 成功生成 ${count} 个产业配置文件`);
console.log(`📁 位置: ${industriesDir}`);
