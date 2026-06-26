// logistics/api/routes/logistics_routes.js
/**
 * 物流 API 路由
 * 
 * 提供物流记录的 CRUD 操作和 OKKI 同步接口
 */

const express = require('express');
const router = express.Router();

const logisticsAPI = require('../logistics_api');
const okkiSyncController = require('../controllers/okki_sync_controller');
const autoNotificationService = require('../controllers/auto_notification_service');

/**
 * @route   POST /api/logistics
 * @desc    创建物流记录
 * @access  Public
 */
router.post('/', async (req, res) => {
  try {
    const recordData = req.body;
    const result = await logisticsAPI.createLogisticsRecord(recordData);
    res.status(201).json({
      success: true,
      data: result
    });
  } catch (e) {
    res.status(400).json({
      success: false,
      error: e.message
    });
  }
});

/**
 * @route   GET /api/logistics
 * @desc    查询物流记录列表
 * @access  Public
 */
router.get('/', async (req, res) => {
  try {
    const filters = req.query;
    const result = await logisticsAPI.listLogisticsRecords(filters);
    res.json({
      success: true,
      data: result
    });
  } catch (e) {
    res.status(500).json({
      success: false,
      error: e.message
    });
  }
});

/**
 * @route   GET /api/logistics/:id
 * @desc    获取物流记录详情
 * @access  Public
 */
router.get('/:id', async (req, res) => {
  try {
    const logisticsId = req.params.id;
    const result = await logisticsAPI.getLogisticsDetails(logisticsId);
    if (!result) {
      return res.status(404).json({
        success: false,
        error: '物流记录未找到'
      });
    }
    res.json({
      success: true,
      data: result
    });
  } catch (e) {
    res.status(500).json({
      success: false,
      error: e.message
    });
  }
});

/**
 * @route   PUT /api/logistics/:id/status
 * @desc    更新物流状态
 * @access  Public
 */
router.put('/:id/status', async (req, res) => {
  try {
    const logisticsId = req.params.id;
    const { newStatus, syncToOKKI } = req.body;
    
    if (!newStatus) {
      return res.status(400).json({
        success: false,
        error: '缺少 newStatus 参数'
      });
    }
    
    const result = await logisticsAPI.updateLogisticsStatus(logisticsId, newStatus);
    
    // 可选：自动触发通知和 OKKI 同步
    if (syncToOKKI) {
      try {
        await autoNotificationService.autoNotifyOnStatusChange(logisticsId, newStatus, true);
      } catch (notifyError) {
        console.warn('自动通知失败:', notifyError.message);
      }
    }
    
    res.json({
      success: true,
      data: result
    });
  } catch (e) {
    res.status(400).json({
      success: false,
      error: e.message
    });
  }
});

/**
 * @route   POST /api/logistics/:id/sync-okki
 * @desc    手动同步物流记录到 OKKI
 * @access  Public
 */
router.post('/:id/sync-okki', async (req, res) => {
  try {
    const logisticsId = req.params.id;
    const result = await okkiSyncController.syncLogisticsToOKKI(logisticsId);
    
    if (result.success) {
      res.json({
        success: true,
        data: result,
        message: '已成功同步到 OKKI'
      });
    } else {
      res.status(400).json({
        success: false,
        data: result,
        error: result.error
      });
    }
  } catch (e) {
    res.status(500).json({
      success: false,
      error: e.message
    });
  }
});

/**
 * @route   GET /api/logistics/:id/okki-status
 * @desc    获取 OKKI 同步状态
 * @access  Public
 */
router.get('/:id/okki-status', async (req, res) => {
  try {
    const logisticsId = req.params.id;
    const result = await okkiSyncController.getOKKISyncStatus(logisticsId);
    
    res.json({
      success: true,
      data: result
    });
  } catch (e) {
    res.status(500).json({
      success: false,
      error: e.message
    });
  }
});

/**
 * @route   POST /api/logistics/:id/notify
 * @desc    发送物流通知邮件
 * @access  Public
 */
router.post('/:id/notify', async (req, res) => {
  try {
    const logisticsId = req.params.id;
    const { notificationType, recipient, syncToOKKI } = req.body;
    
    if (!notificationType) {
      return res.status(400).json({
        success: false,
        error: '缺少 notificationType 参数'
      });
    }
    
    const result = await autoNotificationService.sendLogisticsNotification(
      logisticsId,
      notificationType,
      recipient || {},
      syncToOKKI || false
    );
    
    if (result.success) {
      res.json({
        success: true,
        data: result,
        message: '通知已发送'
      });
    } else {
      res.status(400).json({
        success: false,
        error: result.error
      });
    }
  } catch (e) {
    res.status(500).json({
      success: false,
      error: e.message
    });
  }
});

module.exports = router;
