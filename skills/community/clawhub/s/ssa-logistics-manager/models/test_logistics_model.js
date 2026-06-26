// logistics/models/test_logistics_model.js

const { expect } = require('chai');
const { LogisticsRecord, LogisticsStatus, TransportMode, createLogisticsRecord } = require('./logistics_model');

describe('Logistics Record Model', () => {
  let logisticsRecord;

  beforeEach(() => {
    logisticsRecord = new LogisticsRecord({
      orderId: 'ORD-001',
      customerId: 'CUST-001',
      customerInfo: {
        name: 'John Doe',
        company: 'Test Corp',
        email: 'john@testcorp.com',
        phone: '+1-234-567-8900',
        address: '123 Test St, Test City'
      },
      transportMode: '海运',
      portOfLoading: 'Shenzhen',
      portOfDischarge: 'Los Angeles',
      etd: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      eta: new Date(Date.now() + 21 * 24 * 60 * 60 * 1000).toISOString(),
      cargoInfo: {
        products: [{ name: 'HDMI Cable', quantity: 1000 }],
        totalQuantity: 1000,
        totalVolume: 5.5,
        totalWeight: 500,
        packages: 50,
        description: 'HDMI Cables'
      }
    });
  });

  describe('Initialization', () => {
    it('should create a logistics record with default values', () => {
      expect(logisticsRecord).to.be.an.instanceOf(LogisticsRecord);
      expect(logisticsRecord.logisticsId).to.match(/^LG-\d+$/);
      expect(logisticsRecord.status).to.equal('待订舱');
      expect(logisticsRecord.transportMode).to.equal('海运');
    });

    it('should initialize with provided data', () => {
      expect(logisticsRecord.orderId).to.equal('ORD-001');
      expect(logisticsRecord.customerInfo.name).to.equal('John Doe');
      expect(logisticsRecord.portOfLoading).to.equal('Shenzhen');
      expect(logisticsRecord.portOfDischarge).to.equal('Los Angeles');
    });
  });

  describe('Status Management', () => {
    it('should update status to valid value', () => {
      logisticsRecord.updateStatus('已订舱');
      expect(logisticsRecord.status).to.equal('已订舱');
    });

    it('should throw error for invalid status', () => {
      expect(() => logisticsRecord.updateStatus('invalid_status')).to.throw('无效的物流状态');
    });

    it('should update timestamp when status changes', () => {
      const oldUpdatedAt = logisticsRecord.updatedAt;
      setTimeout(() => {
        logisticsRecord.updateStatus('已订舱');
        expect(new Date(logisticsRecord.updatedAt)).to.be.greaterThan(new Date(oldUpdatedAt));
      }, 10);
    });
  });

  describe('Booking Management', () => {
    it('should update booking information', () => {
      logisticsRecord.updateBooking({
        vesselName: 'COSCO SHIPPING',
        voyageNo: 'V123',
        etd: new Date().toISOString(),
        eta: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString()
      });
      expect(logisticsRecord.vesselName).to.equal('COSCO SHIPPING');
      expect(logisticsRecord.voyageNo).to.equal('V123');
      expect(logisticsRecord.status).to.equal('已订舱');
    });

    it('should update flight info for air transport', () => {
      const airRecord = new LogisticsRecord({ transportMode: '空运' });
      airRecord.updateBooking({ flightNo: 'CA123' });
      expect(airRecord.flightNo).to.equal('CA123');
    });
  });

  describe('Shipment Status Updates', () => {
    it('should mark as loaded', () => {
      logisticsRecord.markAsLoaded(new Date().toISOString());
      expect(logisticsRecord.status).to.equal('已装船');
      expect(logisticsRecord.atd).to.not.be.null;
    });

    it('should mark as in transit', () => {
      logisticsRecord.markAsInTransit();
      expect(logisticsRecord.status).to.equal('运输中');
    });

    it('should mark as arrived', () => {
      logisticsRecord.markAsArrived(new Date().toISOString());
      expect(logisticsRecord.status).to.equal('已到港');
      expect(logisticsRecord.ata).to.not.be.null;
    });

    it('should mark as cleared', () => {
      logisticsRecord.markAsCleared({
        customsNo: 'CUSTOMS-123',
        customsDate: new Date().toISOString(),
        customsStatus: 'cleared'
      });
      expect(logisticsRecord.status).to.equal('已清关');
      expect(logisticsRecord.customsInfo.customsNo).to.equal('CUSTOMS-123');
    });

    it('should mark as delivered', () => {
      logisticsRecord.markAsDelivered();
      expect(logisticsRecord.status).to.equal('已送达');
    });
  });

  describe('Container Management', () => {
    it('should add container information', () => {
      const container = logisticsRecord.addContainer({
        containerNo: 'CONT123456',
        size: '40HQ',
        type: 'Dry',
        sealNo: 'SEAL123'
      });
      expect(container.containerNo).to.equal('CONT123456');
      expect(container.size).to.equal('40HQ');
      expect(logisticsRecord.containerInfo).to.have.lengthOf(1);
    });

    it('should add multiple containers', () => {
      logisticsRecord.addContainer({ containerNo: 'CONT001', size: '20GP' });
      logisticsRecord.addContainer({ containerNo: 'CONT002', size: '40GP' });
      expect(logisticsRecord.containerInfo).to.have.lengthOf(2);
    });
  });

  describe('Bill of Lading Management', () => {
    it('should update bill of lading information', () => {
      logisticsRecord.updateBillOfLading({
        blNo: 'BL123456',
        blType: 'Original',
        blDate: new Date().toISOString()
      });
      expect(logisticsRecord.billOfLading.blNo).to.equal('BL123456');
      expect(logisticsRecord.billOfLading.blType).to.equal('Original');
    });
  });

  describe('Notification Records', () => {
    it('should add notification record', () => {
      const record = logisticsRecord.addNotificationRecord(
        'booking',
        'email',
        '订舱确认通知',
        { email: 'customer@test.com', name: 'John Doe' }
      );
      expect(record.recordId).to.match(/^NT-\d+$/);
      expect(record.type).to.equal('booking');
      expect(record.method).to.equal('email');
      expect(logisticsRecord.notificationRecords).to.have.lengthOf(1);
    });

    it('should add multiple notification records', () => {
      logisticsRecord.addNotificationRecord('booking', 'email', '订舱通知');
      logisticsRecord.addNotificationRecord('shipment', 'email', '发货通知');
      expect(logisticsRecord.notificationRecords).to.have.lengthOf(2);
    });
  });

  describe('ETA and Overdue Detection', () => {
    it('should calculate days to ETA correctly', () => {
      const daysToETA = logisticsRecord.getDaysToETA();
      expect(daysToETA).to.be.closeTo(21, 1);
    });

    it('should detect overdue logistics', () => {
      const overdueRecord = new LogisticsRecord({
        orderId: 'ORD-001',
        eta: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        status: '运输中'
      });
      expect(overdueRecord.isOverdue()).to.be.true;
      expect(overdueRecord.getOverdueDays()).to.be.greaterThan(0);
    });

    it('should not detect overdue for delivered records', () => {
      const deliveredRecord = new LogisticsRecord({
        orderId: 'ORD-001',
        eta: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        status: '已送达'
      });
      expect(deliveredRecord.isOverdue()).to.be.false;
    });

    it('should return null for days to ETA when ETA is not set', () => {
      const record = new LogisticsRecord({ orderId: 'ORD-001' });
      expect(record.getDaysToETA()).to.be.null;
    });
  });

  describe('Overview', () => {
    it('should get logistics overview', () => {
      logisticsRecord.addContainer({ containerNo: 'CONT001', size: '40HQ' });
      logisticsRecord.updateBillOfLading({ blNo: 'BL123' });

      const overview = logisticsRecord.getOverview();
      expect(overview.logisticsId).to.equal(logisticsRecord.logisticsId);
      expect(overview.orderId).to.equal('ORD-001');
      expect(overview.customerName).to.equal('John Doe');
      expect(overview.transportMode).to.equal('海运');
      expect(overview.route).to.equal('Shenzhen → Los Angeles');
      expect(overview.status).to.equal('待订舱');
      expect(overview.containerCount).to.equal(1);
      expect(overview.blNo).to.equal('BL123');
      expect(overview.totalVolume).to.equal(5.5);
      expect(overview.totalWeight).to.equal(500);
    });
  });

  describe('Serialization', () => {
    it('should convert to plain object', () => {
      const obj = logisticsRecord.toObject();
      expect(obj).to.have.property('logisticsId');
      expect(obj).to.have.property('orderId');
      expect(obj).to.have.property('customerInfo');
      expect(obj).to.have.property('status');
      expect(obj).to.not.have.property('updateStatus'); // Should not include methods
    });

    it('should serialize and deserialize correctly', () => {
      const obj = logisticsRecord.toObject();
      const json = JSON.stringify(obj);
      const parsed = JSON.parse(json);
      const newRecord = new LogisticsRecord(parsed);

      expect(newRecord.logisticsId).to.equal(logisticsRecord.logisticsId);
      expect(newRecord.orderId).to.equal(logisticsRecord.orderId);
      expect(newRecord.status).to.equal(logisticsRecord.status);
    });
  });

  describe('Factory Function', () => {
    it('should create logistics record with factory function', () => {
      const record = createLogisticsRecord({
        orderId: 'ORD-002',
        transportMode: '空运',
        portOfLoading: 'Shenzhen',
        portOfDischarge: 'New York'
      });
      expect(record).to.be.an.instanceOf(LogisticsRecord);
      expect(record.logisticsId).to.match(/^LG-\d+$/);
    });
  });
});

describe('Logistics Status Constants', () => {
  it('should have correct status values', () => {
    expect(LogisticsStatus.PENDING_BOOKING).to.equal('待订舱');
    expect(LogisticsStatus.BOOKED).to.equal('已订舱');
    expect(LogisticsStatus.LOADED).to.equal('已装船');
    expect(LogisticsStatus.IN_TRANSIT).to.equal('运输中');
    expect(LogisticsStatus.ARRIVED).to.equal('已到港');
    expect(LogisticsStatus.CLEARED).to.equal('已清关');
    expect(LogisticsStatus.DELIVERED).to.equal('已送达');
    expect(LogisticsStatus.CANCELLED).to.equal('已取消');
  });
});

describe('Transport Mode Constants', () => {
  it('should have correct transport mode values', () => {
    expect(TransportMode.SEA).to.equal('海运');
    expect(TransportMode.AIR).to.equal('空运');
    expect(TransportMode.LAND).to.equal('陆运');
  });
});
