package com.baiwang.global.document.dao;

import com.baiwang.global.document.dao.entity.Transaction;
import com.baiwang.global.document.dao.entity.TransactionExt;
import com.baiwang.global.document.dao.entity.TransactionLine;
import com.baiwang.global.document.dao.entity.TransactionLineExt;
import com.baiwang.global.document.dao.mapper.*;
import com.baiwang.global.transaction.consts.TransactionStatus;
import com.baiwang.global.transaction.consts.TransactionType;
import com.baiwang.xbridge3.common.json.JacksonObjectMapper;
import com.baiwang.xbridge3.database.core.query.EntityQueryWrapper;
import com.baiwang.xbridge3.database.extfields.model.EntityTableSchemaID;
import com.baiwang.xbridge3.database.mybatisplus.EntityObjectManager;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.fasterxml.jackson.databind.node.ObjectNode;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;
import org.springframework.util.Assert;
import org.springframework.util.CollectionUtils;

import java.time.Instant;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * 聚合 mapper 操作
 */
@Repository
@RequiredArgsConstructor
public class TransactionDAO {

  private final TransactionMapper transactionMapper;
  private final TransactionLineMapper transactionLineMapper;
  private final TransactionExtMapper transactionExtMapper;
  private final TransactionLineExtMapper transactionLineExtMapper;
  private final TransactionLineAddressMapper transactionLineAddressMapper;

  /**
   * 保存交易主记录
   */
  public Transaction createTransaction(Transaction transaction) {
    EntityTableSchemaID tableSchemaID = transaction.getTableSchemaID();
    EntityObjectManager<Transaction> transactionEntityManager = transactionMapper.getEntityObjectManager(tableSchemaID);
    EntityObjectManager<TransactionLine> transactionLineEntityManager = transactionLineMapper.getEntityObjectManager(tableSchemaID);

    // 维护交易记录版本号
    if (transaction.getOriginalTransactionId() == null) {
      transaction.setVersionNo(0);
    } else {
      if (transaction.transactionTypeEnum() == TransactionType.AdjustInvoice) {
        // 调整发票取最大的 + 1
        Integer maxVersionNo = transactionMapper.selectMaxVersionNoByOriginalTransactionId(transaction.getOriginalTransactionId());
        Assert.notNull(maxVersionNo, "Original transaction does not exists!");
        transaction.setVersionNo(maxVersionNo + 1);
      } else {
        // 其他取原发票版本 + 1
        Transaction originalTransaction = transactionMapper.selectById(transaction.getOriginalTransactionId());
        Assert.notNull(originalTransaction, "Original transaction does not exists!");
        transaction.setVersionNo(originalTransaction.getVersionNo() + 1);
      }
    }
    // 设置默认值
    transaction.setDelFlag(0); // 未删除
    transaction.setCreateDate(Instant.now());
    transaction.setUpdateDate(Instant.now());
    // 新增
    transactionEntityManager.insert(transaction);
    if (!CollectionUtils.isEmpty(transaction.getLines())) {
      transaction.getLines().forEach(item -> item.onCreateSetup(transaction));
      transactionLineEntityManager.insertMultiple(transaction.getLines());
      for (TransactionLine line : transaction.getLines()) {
        insertTransactionLineExt(line);
      }
    }
    // 扩展字段存储
    TransactionExt transactionExt = new TransactionExt();
    transactionExt.onCreateSetup(transaction);
    transactionExt.setExtData(transaction.getExtensions().toString());
    transactionExtMapper.insert(transactionExt);
    return transaction;
  }

  public boolean updateTransaction(Transaction transaction, Collection<TransactionStatus> expectedStatus) {
    EntityTableSchemaID tableSchemaID = transaction.getTableSchemaID();
    EntityObjectManager<Transaction> transactionEntityManager = transactionMapper.getEntityObjectManager(tableSchemaID);
    EntityObjectManager<TransactionLine> transactionLineEntityManager = transactionLineMapper.getEntityObjectManager(tableSchemaID);
    transaction.setUpdateDate(Instant.now());
    EntityQueryWrapper queryWrapper = EntityQueryWrapper.columnNameQuery(transactionEntityManager.getEntityTable());
    queryWrapper.eq("id", transaction.getId());
    if (!expectedStatus.isEmpty()) {
      queryWrapper.in("transaction_status", expectedStatus.stream().map(TransactionStatus::getStatus).toList());
    }
    // 更新
    int updated = transactionEntityManager.updateSelective(
        transaction, queryWrapper
    );
    if (updated <= 0) {
      return false;
    }

    TransactionExt transactionExt = new TransactionExt();
    transactionExt.setTransactionId(transaction.getId());
    transactionExt.setExtData(transaction.getExtensions().toString());
    transactionExtMapper.updateById(transactionExt);

    List<TransactionLine> existsLines = transactionLineMapper.selectList(
        Wrappers.lambdaQuery(TransactionLine.class)
            .eq(TransactionLine::getTransactionId, transaction.getId())
    );
    Map<Long, TransactionLine> toRemoveLinesMap = existsLines.stream()
        .collect(Collectors.toMap(TransactionLine::getId, Function.identity()));
    if (!CollectionUtils.isEmpty(transaction.getLines())) {
      for (TransactionLine line : transaction.getLines()) {
        TransactionLine existsLine = toRemoveLinesMap.remove(line.getId());
        if (existsLine != null) {
          line.onUpdateSetup(transaction);
          // 更新明细行
          transactionLineEntityManager.updateByIdSelective(line);
          TransactionLineExt lineExt = new TransactionLineExt();
          lineExt.setLineId(line.getId());
          lineExt.setExtData(line.getExtensions().toString());
          transactionLineExtMapper.updateById(lineExt);
        } else {
          line.onCreateSetup(transaction);
          if (line.getCreateDate() == null) {
            line.setCreateDate(Instant.now());
          }
          // 新增明细行
          transactionLineEntityManager.insertSelective(line);
          insertTransactionLineExt(line);
        }
      }
      List<Long> toRemoveLineIdList = toRemoveLinesMap.values().stream().map(TransactionLine::getId).toList();
      transactionLineMapper.deleteByIds(toRemoveLineIdList);
      transactionLineExtMapper.deleteByIds(toRemoveLineIdList);
    }
    return true;
  }

  private void insertTransactionLineExt(TransactionLine line) {
    TransactionLineExt lineExt = new TransactionLineExt();
    lineExt.onCreateSetup(line);
    ObjectNode extensions = line.getExtensions();
    if (extensions == null) {
      extensions = JacksonObjectMapper.get().createObjectNode();
    }
    lineExt.setExtData(extensions.toString());
    transactionLineExtMapper.insert(lineExt);
  }


  /**
   * 根据交易UUID查找交易记录
   */
  public Transaction findByTransactionUuid(Long tenantId, String transactionUuid) {
    return transactionMapper.selectOne(
        Wrappers.lambdaQuery(Transaction.class)
            .eq(Transaction::getTenantId, tenantId)
            .eq(Transaction::getTransactionUuid, transactionUuid)
    );
  }


  /**
   * 根据交易UUID查找交易记录
   */
  public Transaction findByTransactionId(Long transactionId) {
    return transactionMapper.selectById(transactionId);
  }
}