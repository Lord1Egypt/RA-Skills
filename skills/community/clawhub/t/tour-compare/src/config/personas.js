/**
 * 人群画像配置
 * 定义不同人群的权重偏好
 */

export const personas = {
  '老人': {
    name: '老人',
    description: '注重轻松、安全、少购物',
    weights: {
      shoppingStops: -0.25,    // 购物店多扣分
      itineraryPace: 0.20,     // 行程轻松加分
      medicalAccess: 0.15,     // 医疗便利加分
      price: 0.15,
      hotel: 0.15,
      rating: 0.10,
      freeTime: 0.10
    },
    tips: [
      '选择 0 购物或极少购物的团',
      '行程节奏要慢，每天 2-3 个景点为宜',
      '避免高海拔、高强度活动',
      '选择含接送机的产品'
    ]
  },
  
  '亲子': {
    name: '亲子',
    description: '注重亲子设施、安全、趣味性',
    weights: {
      familyFacilities: 0.25,  // 亲子设施
      safety: 0.20,            // 安全性
      fun: 0.15,               // 趣味性
      price: 0.20,
      rating: 0.20,
      freeTime: 0.10
    },
    tips: [
      '选择有亲子活动/设施的酒店',
      '行程要有互动体验项目',
      '避免纯购物或纯观光的团',
      '预留自由活动时间'
    ]
  },
  
  '蜜月': {
    name: '蜜月',
    description: '注重私密性、品质、浪漫体验',
    weights: {
      privacy: 0.25,           // 私密性
      hotel: 0.25,             // 酒店品质
      romance: 0.15,           // 浪漫体验
      price: 0.15,
      rating: 0.20
    },
    tips: [
      '选择小团或独立成团',
      '升级高星酒店或特色民宿',
      '安排浪漫体验（日落、晚餐等）',
      '避免大团和购物'
    ]
  },
  
  '学生': {
    name: '学生',
    description: '注重性价比、自由度、社交',
    weights: {
      price: 0.35,             // 价格敏感
      freedom: 0.20,           // 自由度
      social: 0.15,            // 社交属性
      rating: 0.15,
      fun: 0.15
    },
    tips: [
      '选择性价比高的产品',
      '预留足够自由活动时间',
      '可选择青年旅舍或拼房',
      '关注学生优惠'
    ]
  },
  
  '朋友': {
    name: '朋友',
    description: '注重自由度、体验、拍照',
    weights: {
      freedom: 0.25,
      fun: 0.20,
      photoSpots: 0.15,
      price: 0.20,
      rating: 0.20
    },
    tips: [
      '选择半自由行产品',
      '安排网红打卡点',
      '预留拍照时间',
      '可考虑当地一日游拼团'
    ]
  },
  
  '商务': {
    name: '商务',
    description: '注重品质、效率、服务',
    weights: {
      quality: 0.30,
      efficiency: 0.25,
      service: 0.20,
      hotel: 0.15,
      price: 0.10
    },
    tips: [
      '选择高端品质团',
      '直飞航班优先',
      '选择市中心酒店',
      '关注 VIP 通道/快速入园'
    ]
  }
};

export function getPersona(group) {
  return personas[group] || personas['朋友'];
}

export function getDefaultWeights() {
  return {
    price: 0.25,
    itinerary: 0.25,
    hotel: 0.15,
    transport: 0.15,
    rating: 0.20
  };
}
