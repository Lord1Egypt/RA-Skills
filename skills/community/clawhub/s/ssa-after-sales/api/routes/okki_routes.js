/**
 * OKKI 同步 API 路由
 * 提供投诉/返单同步到 OKKI 的 HTTP 接口
 */

const express = require('express');
const router = express.Router();
const okkiSyncController = require('../controllers/okki_sync_controller');
const { OkkiSyncLog } = require('../../models/okki_sync_log_model');

/**
 * @route POST /api/after-sales/complaint/:id/sync-okki
 * @desc 同步投诉记录到 OKKI
 * @access Public
 */
router.post('/complaint/:id/sync-okki', async (req, res) => {
  try {
    const complaintId = req.params.id;
    
    if (!complaintId) {
      return res.status(400).json({
        success: false,
        message: '投诉 ID 不能为空'
      });
    }
    
    const result = await okkiSyncController.syncComplaintToOKKI(complaintId);
    
    if (result.success) {
      res.status(200).json(result);
    } else {
      res.status(400).json(result);
    }
  } catch (error) {
    console.error('同步投诉到 OKKI 失败:', error);
    res.status(500).json({
      success: false,
      message: '服务器错误',
      error: error.message
    });
  }
});

/**
 * @route POST /api/after-sales/repeat-order/:id/sync-okki
 * @desc 同步返单报价到 OKKI
 * @access Public
 */
router.post('/repeat-order/:id/sync-okki', async (req, res) => {
  try {
    const repeatOrderId = req.params.id;
    
    if (!repeatOrderId) {
      return res.status(400).json({
        success: false,
        message: '返单 ID 不能为空'
      });
    }
    
    const result = await okkiSyncController.syncRepeatOrderToOKKI(repeatOrderId);
    
    if (result.success) {
      res.status(200).json(result);
    } else {
      res.status(400).json(result);
    }
  } catch (error) {
    console.error('同步返单到 OKKI 失败:', error);
    res.status(500).json({
      success: false,
      message: '服务器错误',
      error: error.message
    });
  }
});

/**
 * @route GET /api/after-sales/okki/:id/status
 * @desc 获取同步状态
 * @access Public
 */
router.get('/okki/:id/status', async (req, res) => {
  try {
    const id = req.params.id;
    
    if (!id) {
      return res.status(400).json({
        success: false,
        message: 'ID 不能为空'
      });
    }
    
    const log = OkkiSyncLog.getById(id);
    
    if (!log) {
      return res.status(404).json({
        success: false,
        message: '未找到同步记录',
        id
      });
    }
    
    res.status(200).json({
      success: true,
      data: log.toObject()
    });
  } catch (error) {
    console.error('获取同步状态失败:', error);
    res.status(500).json({
      success: false,
      message: '服务器错误',
      error: error.message
    });
  }
});

/**
 * @route GET /api/after-sales/okki/logs
 * @desc 获取同步日志列表
 * @access Public
 */
router.get('/okki/logs', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 20;
    const logs = OkkiSyncLog.getRecent(limit);
    
    res.status(200).json({
      success: true,
      count: logs.length,
      data: logs.map(log => log.toObject())
    });
  } catch (error) {
    console.error('获取同步日志失败:', error);
    res.status(500).json({
      success: false,
      message: '服务器错误',
      error: error.message
    });
  }
});

/**
 * @route GET /api/after-sales/okki/logs/failed
 * @desc 获取失败的同步日志
 * @access Public
 */
router.get('/okki/logs/failed', async (req, res) => {
  try {
    const logs = OkkiSyncLog.getFailed();
    
    res.status(200).json({
      success: true,
      count: logs.length,
      data: logs.map(log => log.toObject())
    });
  } catch (error) {
    console.error('获取失败日志失败:', error);
    res.status(500).json({
      success: false,
      message: '服务器错误',
      error: error.message
    });
  }
});

module.exports = router;
