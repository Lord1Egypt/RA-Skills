#!/usr/bin/env node
/**
 * 初始化深圳20+8产业配置文件
 */

import { writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const industriesDir = join(__dirname, '..', 'references', 'industries');

// 深圳20+8产业集群配置
const industries = [
  // 数字产业（8个）
  {
    id: "01",
    name: "网络与通信",
    category: "数字产业",
    keywords: ["5G", "6G", "网络通信", "基站", "光纤通信", "物联网"],
    emoji: "📡"
  },
  {
    id: "02",
    name: "半导体与集成电路",
    category: "数字产业",
    keywords: ["半导体", "集成电路", "芯片", "光刻机", "晶圆", "国产芯片"],
    emoji: "⚡"
  },
  {
    id: "03",
    name: "超高清视频显示",
    category: "数字产业",
    keywords: ["超高清视频", "8K", "4K", "显示技术", "OLED", "Mini LED"],
    emoji: "📺"
  },
  {
    id: "04",
    name: "智能终端",
    category: "数字产业",
    keywords: ["智能终端", "智能手机", "可穿戴设备", "AR眼镜", "VR设备"],
    emoji: "📱"
  },
  {
    id: "05",
    name: "智能传感器",
    category: "数字产业",
    keywords: ["传感器", "智能传感", "MEMS", "激光雷达", "毫米波雷达"],
    emoji: "🔬"
  },
  {
    id: "06",
    name: "软件与信息服务",
    category: "数字产业",
    keywords: ["软件", "SaaS", "云计算", "企业服务", "数字化转型"],
    emoji: "💻"
  },
  {
    id: "07",
    name: "数字创意",
    category: "数字产业",
    keywords: ["数字创意", "游戏", "动漫", "数字媒体", "虚拟人", "元宇宙"],
    emoji: "🎨"
  },
  {
    id: "08",
    name: "人工智能",
    category: "数字产业",
    keywords: ["人工智能", "AI", "大模型", "GPT", "机器学习", "深度学习"],
    emoji: "🤖"
  },
  
  // 高端制造（8个）
  {
    id: "09",
    name: "智能制造",
    category: "高端制造",
    keywords: ["智能制造", "工业4.0", "工业机器人", "数字化工厂", "MES"],
    emoji: "🏭"
  },
  {
    id: "10",
    name: "高端医疗器械",
    category: "高端制造",
    keywords: ["医疗器械", "医疗设备", "影像设备", "手术机器人", "IVD"],
    emoji: "🏥"
  },
  {
    id: "11",
    name: "生物医药",
    category: "高端制造",
    keywords: ["生物医药", "新药研发", "基因治疗", "细胞治疗", "疫苗"],
    emoji: "🧬"
  },
  {
    id: "12",
    name: "大健康",
    category: "高端制造",
    keywords: ["大健康", "健康管理", "医疗健康", "康复医疗", "养老产业"],
    emoji: "💊"
  },
  {
    id: "13",
    name: "智能网联汽车",
    category: "高端制造",
    keywords: ["智能网联汽车", "自动驾驶", "车联网", "智能座舱", "L3自动驾驶"],
    emoji: "🚗"
  },
  {
    id: "14",
    name: "新能源",
    category: "高端制造",
    keywords: ["新能源", "光伏", "风电", "储能", "锂电池", "固态电池"],
    emoji: "⚡"
  },
  {
    id: "15",
    name: "安全节能环保",
    category: "高端制造",
    keywords: ["安全节能环保", "环保技术", "碳中和技术", "污染治理", "节能设备"],
    emoji: "🌱"
  },
  {
    id: "16",
    name: "智能机器人",
    category: "高端制造",
    keywords: ["智能机器人", "服务机器人", "工业机器人", "人形机器人", "协作机器人"],
    emoji: "🤖"
  },
  
  // 未来产业（8个）
  {
    id: "17",
    name: "海洋产业",
    category: "未来产业",
    keywords: ["海洋产业", "海洋工程", "深海装备", "海洋生物", "海上风电"],
    emoji: "🌊"
  },
  {
    id: "18",
    name: "先进材料",
    category: "未来产业",
    keywords: ["先进材料", "新材料", "石墨烯", "碳纤维", "纳米材料", "超导材料"],
    emoji: "🧪"
  },
  {
    id: "19",
    name: "现代时尚",
    category: "未来产业",
    keywords: ["现代时尚", "服装设计", "时尚品牌", "珠宝首饰", "潮流文化"],
    emoji: "👗"
  },
  {
    id: "20",
    name: "绿色低碳",
    category: "未来产业",
    keywords: ["绿色低碳", "碳中和", "碳交易", "清洁能源", "ESG"],
    emoji: "♻️"
  },
  {
    id: "21",
    name: "高端装备制造",
    category: "未来产业",
    keywords: ["高端装备", "数控机床", "工业母机", "精密制造", "航空装备"],
    emoji: "⚙️"
  },
  {
    id: "22",
    name: "激光与增材制造",
    category: "未来产业",
    keywords: ["激光", "增材制造", "3D打印", "激光加工", "激光雷达"],
    emoji: "💡"
  },
  {
    id: "23",
    name: "精密仪器设备",
    category: "未来产业",
    keywords: ["精密仪器", "测量设备", "检测设备", "光学仪器", "分析仪器"],
    emoji: "🔬"
  },
  {
    id: "24",
    name: "航空航天",
    category: "未来产业",
    keywords: ["航空航天", "卫星", "火箭", "无人机", "航空发动机"],
    emoji: "🚀"
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

// 生成所有配置文件
let count = 0;
for (const industry of industries) {
  const config = generateConfig(industry);
  const filename = `${industry.id}-${industry.name.replace(/[\/\s]/g, '-')}.json`;
  const filepath = join(industriesDir, filename);
  
  try {
    writeFileSync(filepath, JSON.stringify(config, null, 2), 'utf-8');
    console.log(`✅ ${industry.id}. ${industry.name}`);
    count++;
  } catch (err) {
    console.error(`❌ ${industry.id}. ${industry.name}: ${err.message}`);
  }
}

console.log(`\n🎉 成功生成 ${count} 个产业配置文件`);
console.log(`📁 位置: ${industriesDir}`);
