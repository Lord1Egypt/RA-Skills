// logistics/models/logistics_model.js
/**
 * 物流数据模型
 * 
 * 用于管理订舱、报关单据、提单追踪、客户通知
 * 设计风格参考 orders/models/order_model.js 和 production/models/production_plan_model.js
 */

/**
 * 物流状态枚举
 */
const LogisticsStatus = {
  PENDING_BOOKING: '待订舱',
  BOOKED: '已订舱',
  LOADED: '已装船',
  IN_TRANSIT: '运输中',
  ARRIVED: '已到港',
  CLEARED: '已清关',
  DELIVERED: '已送达',
  CANCELLED: '已取消'
};

/**
 * 运输方式枚举
 */
const TransportMode = {
  SEA: '海运',
  AIR: '空运',
  LAND: '陆运'
};

/**
 * 物流记录类
 */
class LogisticsRecord {
  constructor(data) {
    // 基本信息
    this.logisticsId = data.logisticsId || `LG-${Date.now()}`;
    this.orderId = data.orderId; // 关联订单 ID
    this.customerId = data.customerId;
    this.customerInfo = data.customerInfo || {
      name: '',
      company: '',
      email: '',
      phone: '',
      address: ''
    };
    
    // 货物信息
    this.cargoInfo = data.cargoInfo || {
      products: [],
      totalQuantity: 0,
      totalVolume: 0, // CBM (立方米)
      totalWeight: 0, // KG (千克)
      packages: 0, // 总件数
      description: ''
    };
    
    // 运输方式
    this.transportMode = data.transportMode || TransportMode.SEA;
    
    // 港口信息
    this.portOfLoading = data.portOfLoading || ''; // 起运港
    this.portOfDischarge = data.portOfDischarge || ''; // 目的港
    this.placeOfDelivery = data.placeOfDelivery || ''; // 交货地
    
    // 船期/航班信息
    this.vesselName = data.vesselName || ''; // 船名 (海运)
    this.voyageNo = data.voyageNo || ''; // 航次 (海运)
    this.flightNo = data.flightNo || ''; // 航班号 (空运)
    
    // 时间信息
    this.etd = data.etd || null; // 预计离港时间
    this.eta = data.eta || null; // 预计到港时间
    this.atd = data.atd || null; // 实际离港时间
    this.ata = data.ata || null; // 实际到港时间
    
    // 集装箱信息
    this.containerInfo = data.containerInfo || [];
    
    // 提单信息
    this.billOfLading = data.billOfLading || {
      blNo: '', // 提单号
      blType: '', // 提单类型 (Original/Seaway Bill)
      blDate: null, // 提单日期
      blCopy: '' // 提单副本路径
    };
    
    // 物流状态
    this.status = data.status || LogisticsStatus.PENDING_BOOKING;
    
    // 报关信息
    this.customsInfo = data.customsInfo || {
      customsNo: '', // 报关单号
      customsDate: null, // 报关日期
      customsStatus: '', // 报关状态
      documents: [] // 报关单据列表
    };
    
    // 费用信息
    this.freightInfo = data.freightInfo || {
      freightCost: 0, // 运费
      currency: 'USD',
      paymentTerms: '', // 运费支付条款
      insuranceCost: 0, // 保险费
      otherCosts: 0 // 其他费用
    };
    
    // 通知记录
    this.notificationRecords = data.notificationRecords || [];
    
    // 时间戳
    this.createdAt = data.createdAt || new Date().toISOString();
    this.updatedAt = new Date().toISOString();
    
    // 备注
    this.notes = data.notes || '';
  }

  /**
   * 更新物流状态
   * @param {string} newStatus - 新状态
   */
  updateStatus(newStatus) {
    const validStatuses = Object.values(LogisticsStatus);
    if (!validStatuses.includes(newStatus)) {
      throw new Error(`无效的物流状态：${newStatus}。有效状态：${validStatuses.join(', ')}`);
    }
    this.status = newStatus;
    this.updatedAt = new Date().toISOString();
  }

  /**
   * 更新订舱状态
   * @param {object} bookingInfo - 订舱信息 {vesselName, voyageNo, etd, eta}
   */
  updateBooking(bookingInfo) {
    if (bookingInfo.vesselName) this.vesselName = bookingInfo.vesselName;
    if (bookingInfo.voyageNo) this.voyageNo = bookingInfo.voyageNo;
    if (bookingInfo.flightNo) this.flightNo = bookingInfo.flightNo;
    if (bookingInfo.etd) this.etd = bookingInfo.etd;
    if (bookingInfo.eta) this.eta = bookingInfo.eta;
    this.updateStatus(LogisticsStatus.BOOKED);
  }

  /**
   * 标记为已装船
   * @param {string} atd - 实际离港时间
   */
  markAsLoaded(atd) {
    this.atd = atd || new Date().toISOString();
    this.updateStatus(LogisticsStatus.LOADED);
  }

  /**
   * 标记为运输中
   */
  markAsInTransit() {
    this.updateStatus(LogisticsStatus.IN_TRANSIT);
  }

  /**
   * 标记为已到港
   * @param {string} ata - 实际到港时间
   */
  markAsArrived(ata) {
    this.ata = ata || new Date().toISOString();
    this.updateStatus(LogisticsStatus.ARRIVED);
  }

  /**
   * 标记为已清关
   * @param {object} customsInfo - 报关信息 {customsNo, customsDate, customsStatus}
   */
  markAsCleared(customsInfo) {
    if (customsInfo) {
      this.customsInfo = { ...this.customsInfo, ...customsInfo };
    }
    this.updateStatus(LogisticsStatus.CLEARED);
  }

  /**
   * 标记为已送达
   */
  markAsDelivered() {
    this.updateStatus(LogisticsStatus.DELIVERED);
  }

  /**
   * 添加集装箱信息
   * @param {object} container - 集装箱信息 {containerNo, size, type, sealNo}
   */
  addContainer(container) {
    const containerRecord = {
      containerNo: container.containerNo || '',
      size: container.size || '20GP', // 20GP/40GP/40HQ
      type: container.type || 'Dry',
      sealNo: container.sealNo || '',
      loaded: container.loaded || false
    };
    this.containerInfo.push(containerRecord);
    this.updatedAt = new Date().toISOString();
    return containerRecord;
  }

  /**
   * 更新提单信息
   * @param {object} blInfo - 提单信息 {blNo, blType, blDate, blCopy}
   */
  updateBillOfLading(blInfo) {
    this.billOfLading = { ...this.billOfLading, ...blInfo };
    this.updatedAt = new Date().toISOString();
  }

  /**
   * 添加货物信息
   * @param {object} cargo - 货物信息 {products, totalQuantity, totalVolume, totalWeight, packages}
   */
  updateCargoInfo(cargo) {
    this.cargoInfo = { ...this.cargoInfo, ...cargo };
    this.updatedAt = new Date().toISOString();
  }

  /**
   * 更新物流追踪信息
   * @param {object} trackingData - 追踪数据 {vesselName, voyageNo, etd, eta, atd, containerInfo, billOfLading, notificationRecords}
   */
  updateTracking(trackingData) {
    if (trackingData.vesselName) this.vesselName = trackingData.vesselName;
    if (trackingData.voyageNo) this.voyageNo = trackingData.voyageNo;
    if (trackingData.flightNo) this.flightNo = trackingData.flightNo;
    if (trackingData.etd) this.etd = trackingData.etd;
    if (trackingData.eta) this.eta = trackingData.eta;
    if (trackingData.atd) this.atd = trackingData.atd;
    if (trackingData.ata) this.ata = trackingData.ata;
    if (trackingData.containerInfo && Array.isArray(trackingData.containerInfo)) {
      this.containerInfo = [...this.containerInfo, ...trackingData.containerInfo];
    }
    if (trackingData.billOfLading) {
      this.billOfLading = { ...this.billOfLading, ...trackingData.billOfLading };
    }
    if (trackingData.notificationRecords && Array.isArray(trackingData.notificationRecords)) {
      this.notificationRecords = [...this.notificationRecords, ...trackingData.notificationRecords];
    }
    this.updatedAt = new Date().toISOString();
    return this.toObject();
  }

  /**
   * 添加通知记录
   * @param {string} type - 通知类型 (booking/shipment/arrival/delivery)
   * @param {string} method - 通知方式 (email/sms/wechat)
   * @param {string} content - 通知内容
   * @param {object} recipient - 收件人信息 {email, phone, name}
   */
  addNotificationRecord(type, method, content, recipient = {}) {
    const record = {
      recordId: `NT-${Date.now()}`,
      date: new Date().toISOString(),
      type,
      method,
      content,
      recipient: {
        email: recipient.email || '',
        phone: recipient.phone || '',
        name: recipient.name || ''
      },
      status: 'sent' // sent, failed, pending
    };
    this.notificationRecords.push(record);
    this.updatedAt = new Date().toISOString();
    return record;
  }

  /**
   * 生成报关单据
   * @param {string} docType - 单据类型 (invoice/packing_list/contract)
   * @returns {object} 单据数据
   */
  generateCustomsDoc(docType) {
    const docData = {
      logisticsId: this.logisticsId,
      orderId: this.orderId,
      docType,
      generatedAt: new Date().toISOString(),
      customer: this.customerInfo,
      cargo: this.cargoInfo,
      shipping: {
        portOfLoading: this.portOfLoading,
        portOfDischarge: this.portOfDischarge,
        vesselName: this.vesselName,
        voyageNo: this.voyageNo,
        etd: this.etd,
        eta: this.eta
      },
      billOfLading: this.billOfLading,
      containerInfo: this.containerInfo
    };
    
    // 将单据数据添加到 customsInfo.documents
    this.customsInfo.documents.push({
      docType,
      generatedAt: docData.generatedAt,
      data: docData
    });
    
    this.updatedAt = new Date().toISOString();
    return docData;
  }

  /**
   * 获取剩余天数 (到 ETA)
   * @returns {number} 剩余天数
   */
  getDaysToETA() {
    if (!this.eta) return null;
    const now = new Date();
    const eta = new Date(this.eta);
    const diffTime = eta - now;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }

  /**
   * 检查是否逾期 (超过 ETA 未送达)
   * @returns {boolean} 是否逾期
   */
  isOverdue() {
    if (!this.eta || this.status === LogisticsStatus.DELIVERED) return false;
    const now = new Date();
    const eta = new Date(this.eta);
    return now > eta;
  }

  /**
   * 获取逾期天数
   * @returns {number} 逾期天数
   */
  getOverdueDays() {
    if (!this.isOverdue()) return 0;
    const now = new Date();
    const eta = new Date(this.eta);
    const diffTime = now - eta;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }

  /**
   * 获取物流概览
   */
  getOverview() {
    return {
      logisticsId: this.logisticsId,
      orderId: this.orderId,
      customerName: this.customerInfo.name,
      transportMode: this.transportMode,
      route: `${this.portOfLoading} → ${this.portOfDischarge}`,
      status: this.status,
      vesselName: this.vesselName || this.flightNo,
      etd: this.etd,
      eta: this.eta,
      daysToETA: this.getDaysToETA(),
      isOverdue: this.isOverdue(),
      blNo: this.billOfLading.blNo,
      containerCount: this.containerInfo.length,
      totalVolume: this.cargoInfo.totalVolume,
      totalWeight: this.cargoInfo.totalWeight
    };
  }

  /**
   * 转换为纯对象 (用于 JSON 序列化)
   */
  toObject() {
    return {
      logisticsId: this.logisticsId,
      orderId: this.orderId,
      customerId: this.customerId,
      customerInfo: this.customerInfo,
      cargoInfo: this.cargoInfo,
      transportMode: this.transportMode,
      portOfLoading: this.portOfLoading,
      portOfDischarge: this.portOfDischarge,
      placeOfDelivery: this.placeOfDelivery,
      vesselName: this.vesselName,
      voyageNo: this.voyageNo,
      flightNo: this.flightNo,
      etd: this.etd,
      eta: this.eta,
      atd: this.atd,
      ata: this.ata,
      containerInfo: this.containerInfo,
      billOfLading: this.billOfLading,
      status: this.status,
      customsInfo: this.customsInfo,
      freightInfo: this.freightInfo,
      notificationRecords: this.notificationRecords,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      notes: this.notes
    };
  }
}

/**
 * 创建物流记录（工厂方法）
 * @param {object} data - 物流记录数据
 * @returns {LogisticsRecord} 物流记录实例
 */
function createLogisticsRecord(data) {
  return new LogisticsRecord(data);
}

module.exports = {
  LogisticsRecord,
  LogisticsStatus,
  TransportMode,
  createLogisticsRecord
};
