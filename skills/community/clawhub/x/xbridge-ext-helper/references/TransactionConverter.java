package com.baiwang.global.document.converter;

import com.baiwang.global.document.dao.entity.Transaction;
import com.baiwang.global.document.dao.entity.TransactionLine;
import com.baiwang.global.transaction.consts.CountryCode;
import com.baiwang.global.transaction.consts.CurrencyCode;
import com.baiwang.global.transaction.consts.TransactionStatus;
import com.baiwang.global.transaction.consts.TransactionType;
import com.baiwang.global.transaction.model.dto.TransactionDTO;
import com.baiwang.global.transaction.model.dto.TransactionLineDTO;
import com.baiwang.global.transaction.utils.DateTimeUtils;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.ObjectUtils;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

@Component
public class TransactionConverter {

  /**
   * 将TransactionDTO转换为Transaction实体
   */
  public Transaction convertToEntity(TransactionDTO source) {
    Transaction target = new Transaction();
    target.setId(source.getId());
    target.setTenantId(source.getTenantId());
    target.setCompanyId(source.getCompanyId());
    // 基础字段映射
    target.setOriginalTransactionId(source.getOriginalTransactionId());
    target.setTransactionUuid(source.getTransactionUuid());
    target.setTransactionCode(source.getTransactionCode());
    target.setTransactionType(Optional.ofNullable(source.getTransactionType()).map(TransactionType::getCode).orElse(null));
    target.setTransactionDate(DateTimeUtils.toInstant(source.getTransactionDate()));
    target.setDocSourceCode(source.getDataSourceCode());
    target.setBusinessScenario(source.getBusinessScenario());
    if (source.getCountryCode() != null) {
      target.setCountryCode(source.getCountryCode().getCode());
    }
    target.setRegionCode(source.getRegionCode());
    target.setTaxLocationCode(source.getTaxLocationCode());
    target.setSellerName(source.getSellerName());
    target.setSellerAddress(source.getSellerAddress());
    target.setSellerPhoneNumber(source.getSellerPhoneNumber());
    target.setSellerBank(source.getSellerBank());
    target.setSellerBankAccount(source.getSellerBankAccount());
    target.setBuyerId(source.getBuyerId());
    target.setBuyerType(source.getBuyerType());
    target.setBuyerAddress(source.getBuyerAddress());
    target.setBuyerPhoneNumber(source.getBuyerPhoneNumber());
    target.setBuyerBank(source.getBuyerBank());
    target.setBuyerBankAccount(source.getBuyerBankAccount());
    target.setSalesOrderNo(source.getSalesOrderNo());
    target.setSalespersonCode(source.getSalespersonCode());
    target.setPurchaseOrderNo(source.getPurchaseOrderNo());
    target.setProcessCode(source.getProcessCode());
    target.setTransactionStatus(Optional.ofNullable(source.getTransactionStatus()).map(TransactionStatus::getStatus).orElse(null));
    target.setInvoiceStatus(source.getInvoiceStatus());
    target.setIssueMethod(source.getIssueMethod());
    target.setIssueDate(DateTimeUtils.toInstant(source.getIssueDate()));
    target.setTaxDate(source.getTaxDate());
    target.setErrorCode(source.getErrorCode());
    target.setErrorMsg(source.getErrorMsg());
    target.setTotalTaxCalculated(source.getTotalTaxCalculated());
    target.setTaxOverrideType(source.getTaxOverrideType());
    target.setTaxOverrideReason(source.getTaxOverrideReason());
    target.setAdjustReason(source.getAdjustReason());
    target.setVoidReason(source.getVoidReason());
    target.setReplaceReason(source.getReplaceReason());
    target.setBatchNo(source.getBatchNo());
    target.setDelFlag(source.getDelFlag());
    target.setDocRef1(source.getDocRef1());
    target.setDocRef2(source.getDocRef2());
    target.setDocRef3(source.getDocRef3());
    target.setCreateDate(DateTimeUtils.toInstant(source.getCreateDate()));
    target.setCreateBy(source.getCreateBy());
    target.setCreateById(source.getCreateById());
    target.setUpdateDate(DateTimeUtils.toInstant(source.getUpdateDate()));
    target.setUpdateBy(source.getUpdateBy());
    target.setUpdateById(source.getUpdateById());
    if (source.getCurrencyCode() != null) {
      target.setCurrencyCode(source.getCurrencyCode().getCode());
    }
    if (source.getExchangeRateCurrencyCode() != null) {
      target.setExchangeRateCurrencyCode(source.getExchangeRateCurrencyCode().getCode());
    }
    target.setExchangeRate(source.getExchangeRate());
    target.setExchangeRateEffectiveDate(source.getExchangeRateEffectiveDate());
    target.setCompanyCode(source.getCompanyCode());
    target.setSellerTaxId(source.getSellerTaxId());
    target.setSalesPointCode(source.getSalesPointCode());
    target.setBuyerCode(source.getBuyerCode());
    target.setBuyerName(source.getBuyerName());
    target.setBuyerTaxId(source.getBuyerTaxId());
    target.setBuyerEmail(source.getBuyerEmail());
    target.setNote(source.getNote());
    target.setTaxIncluded(source.getTaxIncluded());
    target.setTotalTaxAmount(source.getTotalTaxAmount());
    target.setTotalDiscountAmount(source.getTotalDiscountAmount());
    target.setTotalTaxExclusiveAmount(source.getTotalTaxExclusiveAmount());
    target.setTotalTaxInclusiveAmount(source.getTotalTaxInclusiveAmount());
    target.setTotalTaxInclusiveAmountIc(source.getTotalTaxInclusiveAmountIc());
    target.setTotalTaxExclusiveAmountIc(source.getTotalTaxExclusiveAmountIc());
    target.setTotalTaxAmountIc(source.getTotalTaxAmountIc());
    target.setTotalTaxExclusiveDiscountAmount(source.getTotalTaxExclusiveDiscountAmount());
    target.setTotalTaxExclusiveDiscountAmountIc(source.getTotalTaxExclusiveDiscountAmountIc());
    target.setTotalTaxInclusiveDiscountAmount(source.getTotalTaxInclusiveDiscountAmount());
    target.setTotalTaxInclusiveDiscountAmountIc(source.getTotalTaxInclusiveDiscountAmountIc());
    target.setTotalTaxCalculatedIc(source.getTotalTaxCalculatedIc());
    target.setExtensions(source.getExtensions());
    if (!ObjectUtils.isEmpty(source.getOriginalIssueDate())) {
      target.setOriginalIssueDate(DateTimeUtils.toInstant(source.getOriginalIssueDate()));
    }

    List<TransactionLine> lines = convertLinesToEntities(source.getLines());
    target.setLines(lines);

    // 去除所有 BigDecimal 字段的尾随零
    stripTransactionTrailingZeros(target);

    return target;
  }

  /**
   * 将TransactionLineDTO列表转换为TransactionLine实体列表
   */
  public List<TransactionLine> convertLinesToEntities(List<TransactionLineDTO> lineDTOs) {
    if (lineDTOs == null || lineDTOs.isEmpty()) {
      return new ArrayList<>();
    }

    List<TransactionLine> entities = new ArrayList<>();
    for (TransactionLineDTO dto : lineDTOs) {
      TransactionLine entity = convertLineToEntity(dto);
      entities.add(entity);
    }

    return entities;
  }

  /**
   * 将单个TransactionLineDTO转换为TransactionLine实体
   */
  private TransactionLine convertLineToEntity(TransactionLineDTO source) {
    TransactionLine target = new TransactionLine();

    target.setId(source.getId());
    target.setTransactionId(source.getTransactionId());
    target.setTenantId(source.getTenantId());
    target.setTransactionDate(DateTimeUtils.toInstant(source.getTransactionDate()));
    Integer lineType = source.getLineType();
    target.setLineType(Objects.isNull(lineType) ? 0 : lineType);
    target.setLineNumber(source.getLineNumber());
    target.setTaxIncluded(source.getTaxIncluded());
    target.setItemCode(source.getItemCode());
    target.setItemName(source.getItemName());
    target.setUnit(source.getUnit());
    target.setQuantity(source.getQuantity());
    target.setUnitPrice(source.getUnitPrice());
    target.setSpecification(source.getSpecification());
    target.setAmount(source.getAmount());
    target.setDiscountAmount(source.getDiscountAmount());
    target.setTaxRate(source.getTaxRate());
    target.setTaxAmount(source.getTaxAmount());
    target.setTaxCode(source.getTaxCode());
    target.setDescription(source.getDescription());
    target.setTaxExclusiveUnitPrice(source.getTaxExclusiveUnitPrice());
    target.setTaxExclusiveAmount(source.getTaxExclusiveAmount());
    target.setTaxInclusiveUnitPrice(source.getTaxInclusiveUnitPrice());
    target.setTaxInclusiveAmount(source.getTaxInclusiveAmount());
    target.setTaxCalculated(source.getTaxCalculated());
    target.setTaxSourcing(source.getTaxSourcing());
    target.setHsCode(source.getHsCode());
    target.setLineRef1(source.getLineRef1());
    target.setLineRef2(source.getLineRef2());
    target.setLineRef3(source.getLineRef3());
    target.setCreateDate(DateTimeUtils.toInstant(source.getCreateDate()));
    target.setCreateBy(source.getCreateBy());
    target.setCreateById(source.getCreateById());
    target.setUpdateDate(DateTimeUtils.toInstant(source.getUpdateDate()));
    target.setUpdateBy(source.getUpdateBy());
    target.setUpdateById(source.getUpdateById());
    target.setTaxAmountIc(source.getTaxAmountIc());
    target.setTaxExclusiveUnitPriceIc(source.getTaxExclusiveUnitPriceIc());
    target.setTaxInclusiveUnitPriceIc(source.getTaxInclusiveUnitPriceIc());
    target.setTaxExclusiveAmountIc(source.getTaxExclusiveAmountIc());
    target.setTaxInclusiveAmountIc(source.getTaxInclusiveAmountIc());
    target.setTaxExclusiveDiscountAmountIc(source.getTaxExclusiveDiscountAmountIc());
    target.setTaxInclusiveDiscountAmountIc(source.getTaxInclusiveDiscountAmountIc());
    target.setTaxCalculatedIc(source.getTaxCalculatedIc());
    target.setDiscountTaxCalculatedIc(source.getDiscountTaxCalculatedIc());
    target.setExtensions(source.getExtensions());

    return target;
  }

  /**
   * 将Transaction实体转换为TransactionDTO
   */
  public TransactionDTO convertToDTO(Transaction source) {
    TransactionDTO target = new TransactionDTO();
    target.setId(source.getId());
    target.setTenantId(source.getTenantId());
    target.setCompanyId(source.getCompanyId());
    // 基础字段映射
    target.setTransactionUuid(source.getTransactionUuid());
    target.setTransactionCode(source.getTransactionCode());
    target.setTransactionType(Optional.ofNullable(source.getTransactionType()).map(TransactionType::fromCode).orElse(null));
    target.setInvoiceStatus(source.getInvoiceStatus());
    target.setOriginalTransactionId(source.getOriginalTransactionId());
    target.setTransactionDate(DateTimeUtils.toOffsetDateTime(source.getTransactionDate()));
    target.setDataSourceCode(source.getDocSourceCode());
    target.setBusinessScenario(source.getBusinessScenario());
    target.setCountryCode(CountryCode.fromCode(source.getCountryCode()));
    target.setRegionCode(source.getRegionCode());
    target.setTaxLocationCode(source.getTaxLocationCode());
    target.setSellerName(source.getSellerName());
    target.setSellerAddress(source.getSellerAddress());
    target.setSellerPhoneNumber(source.getSellerPhoneNumber());
    target.setSellerBank(source.getSellerBank());
    target.setSellerBankAccount(source.getSellerBankAccount());
    target.setBuyerId(source.getBuyerId());
    target.setBuyerType(source.getBuyerType());
    target.setBuyerAddress(source.getBuyerAddress());
    target.setBuyerPhoneNumber(source.getBuyerPhoneNumber());
    target.setBuyerBank(source.getBuyerBank());
    target.setBuyerBankAccount(source.getBuyerBankAccount());
    target.setSalesOrderNo(source.getSalesOrderNo());
    target.setSalespersonCode(source.getSalespersonCode());
    target.setPurchaseOrderNo(source.getPurchaseOrderNo());
    target.setProcessCode(source.getProcessCode());
    target.setTransactionStatus(source.transactionStatusEnum());
    target.setIssueMethod(source.getIssueMethod());
    target.setIssueDate(DateTimeUtils.toOffsetDateTime(source.getIssueDate()));
    target.setTaxDate(source.getTaxDate());
    target.setErrorCode(source.getErrorCode());
    target.setErrorMsg(source.getErrorMsg());
    target.setTotalTaxCalculated(source.getTotalTaxCalculated());
    target.setTaxOverrideType(source.getTaxOverrideType());
    target.setTaxOverrideReason(source.getTaxOverrideReason());
    target.setAdjustReason(source.getAdjustReason());
    target.setVoidReason(source.getVoidReason());
    target.setReplaceReason(source.getReplaceReason());
    target.setBatchNo(source.getBatchNo());
    target.setDelFlag(source.getDelFlag());
    target.setDocRef1(source.getDocRef1());
    target.setDocRef2(source.getDocRef2());
    target.setDocRef3(source.getDocRef3());
    target.setCreateDate(DateTimeUtils.toOffsetDateTime(source.getCreateDate()));
    target.setCreateBy(source.getCreateBy());
    target.setCreateById(source.getCreateById());
    target.setUpdateDate(DateTimeUtils.toOffsetDateTime(source.getUpdateDate()));
    target.setUpdateBy(source.getUpdateBy());
    target.setUpdateById(source.getUpdateById());
    target.setCurrencyCode(CurrencyCode.fromCode(source.getCurrencyCode()));
    target.setExchangeRateCurrencyCode(CurrencyCode.fromCode(source.getExchangeRateCurrencyCode()));
    target.setExchangeRate(source.getExchangeRate());
    target.setExchangeRateEffectiveDate(source.getExchangeRateEffectiveDate());
    target.setCompanyCode(source.getCompanyCode());
    target.setSellerTaxId(source.getSellerTaxId());
    target.setSalesPointCode(source.getSalesPointCode());
    target.setBuyerCode(source.getBuyerCode());
    target.setBuyerName(source.getBuyerName());
    target.setBuyerTaxId(source.getBuyerTaxId());
    target.setBuyerEmail(source.getBuyerEmail());
    target.setNote(source.getNote());
    target.setTaxIncluded(source.getTaxIncluded());
    target.setTotalTaxAmount(source.getTotalTaxAmount());
    target.setTotalDiscountAmount(source.getTotalDiscountAmount());
    target.setTotalTaxExclusiveAmount(source.getTotalTaxExclusiveAmount());
    target.setTotalTaxInclusiveAmount(source.getTotalTaxInclusiveAmount());
    target.setTotalTaxInclusiveAmountIc(source.getTotalTaxInclusiveAmountIc());
    target.setTotalTaxExclusiveAmountIc(source.getTotalTaxExclusiveAmountIc());
    target.setTotalTaxAmountIc(source.getTotalTaxAmountIc());
    target.setTotalTaxExclusiveDiscountAmount(source.getTotalTaxExclusiveDiscountAmount());
    target.setTotalTaxExclusiveDiscountAmountIc(source.getTotalTaxExclusiveDiscountAmountIc());
    target.setTotalTaxInclusiveDiscountAmount(source.getTotalTaxInclusiveDiscountAmount());
    target.setTotalTaxInclusiveDiscountAmountIc(source.getTotalTaxInclusiveDiscountAmountIc());
    target.setTotalTaxCalculatedIc(source.getTotalTaxCalculatedIc());
    target.setExtensions(source.getExtensions());

    List<TransactionLineDTO> lineDTOS = convertLinesToDTOs(source.getLines());
    target.setLines(lineDTOS);

    return target;
  }

  /**
   * 将TransactionLine实体列表转换为TransactionLineDTO列表
   */
  public List<TransactionLineDTO> convertLinesToDTOs(List<TransactionLine> lineEntities) {
    if (lineEntities == null || lineEntities.isEmpty()) {
      return new ArrayList<>();
    }

    List<TransactionLineDTO> dtos = new ArrayList<>();
    for (TransactionLine entity : lineEntities) {
      TransactionLineDTO dto = convertLineToDTO(entity);
      dtos.add(dto);
    }

    return dtos;
  }

  /**
   * 将单个TransactionLine实体转换为TransactionLineDTO
   */
  private TransactionLineDTO convertLineToDTO(TransactionLine source) {
    TransactionLineDTO target = new TransactionLineDTO();

    target.setId(source.getId());
    target.setTransactionId(source.getTransactionId());
    target.setTenantId(source.getTenantId());
    target.setTransactionDate(DateTimeUtils.toOffsetDateTime(source.getTransactionDate()));
    target.setLineType(source.getLineType());
    target.setLineNumber(source.getLineNumber());
    target.setTaxIncluded(source.getTaxIncluded());
    target.setItemCode(source.getItemCode());
    target.setItemName(source.getItemName());
    target.setUnit(source.getUnit());
    target.setQuantity(source.getQuantity());
    target.setUnitPrice(source.getUnitPrice());
    target.setSpecification(source.getSpecification());
    target.setAmount(source.getAmount());
    target.setDiscountAmount(source.getDiscountAmount());
    target.setTaxRate(source.getTaxRate());
    target.setTaxAmount(source.getTaxAmount());
    target.setTaxCode(source.getTaxCode());
    target.setDescription(source.getDescription());
    target.setTaxExclusiveUnitPrice(source.getTaxExclusiveUnitPrice());
    target.setTaxExclusiveAmount(source.getTaxExclusiveAmount());
    target.setTaxInclusiveUnitPrice(source.getTaxInclusiveUnitPrice());
    target.setTaxInclusiveAmount(source.getTaxInclusiveAmount());
    target.setTaxCalculated(source.getTaxCalculated());
    target.setTaxSourcing(source.getTaxSourcing());
    target.setHsCode(source.getHsCode());
    target.setLineRef1(source.getLineRef1());
    target.setLineRef2(source.getLineRef2());
    target.setLineRef3(source.getLineRef3());
    target.setCreateDate(DateTimeUtils.toOffsetDateTime(source.getCreateDate()));
    target.setCreateBy(source.getCreateBy());
    target.setCreateById(source.getCreateById());
    target.setUpdateDate(DateTimeUtils.toOffsetDateTime(source.getUpdateDate()));
    target.setUpdateBy(source.getUpdateBy());
    target.setUpdateById(source.getUpdateById());
    target.setTaxAmountIc(source.getTaxAmountIc());
    target.setTaxExclusiveUnitPriceIc(source.getTaxExclusiveUnitPriceIc());
    target.setTaxInclusiveUnitPriceIc(source.getTaxInclusiveUnitPriceIc());
    target.setTaxExclusiveAmountIc(source.getTaxExclusiveAmountIc());
    target.setTaxInclusiveAmountIc(source.getTaxInclusiveAmountIc());
    target.setTaxExclusiveDiscountAmount(source.getTaxExclusiveDiscountAmount());
    target.setTaxInclusiveDiscountAmount(source.getTaxInclusiveDiscountAmount());
    target.setTaxExclusiveDiscountAmountIc(source.getTaxExclusiveDiscountAmountIc());
    target.setTaxInclusiveDiscountAmountIc(source.getTaxInclusiveDiscountAmountIc());
    target.setTaxCalculatedIc(source.getTaxCalculatedIc());
    target.setDiscountTaxCalculated(source.getDiscountTaxCalculated());
    target.setDiscountTaxCalculatedIc(source.getDiscountTaxCalculatedIc());
    target.setExtensions(source.getExtensions());

    return target;
  }

  /**
   * 去除 Transaction 实体中所有 BigDecimal 字段的尾随零
   */
  private void stripTransactionTrailingZeros(Transaction transaction) {
    if (transaction == null) {
      return;
    }

    transaction.setTotalTaxAmount(stripDecimal(transaction.getTotalTaxAmount()));
    transaction.setTotalTaxExclusiveAmount(stripDecimal(transaction.getTotalTaxExclusiveAmount()));
    transaction.setTotalTaxInclusiveAmount(stripDecimal(transaction.getTotalTaxInclusiveAmount()));
    transaction.setTotalDiscountAmount(stripDecimal(transaction.getTotalDiscountAmount()));
    transaction.setTotalTaxCalculated(stripDecimal(transaction.getTotalTaxCalculated()));
    transaction.setTotalTaxAmountIc(stripDecimal(transaction.getTotalTaxAmountIc()));
    transaction.setTotalTaxExclusiveAmountIc(stripDecimal(transaction.getTotalTaxExclusiveAmountIc()));
    transaction.setTotalTaxInclusiveAmountIc(stripDecimal(transaction.getTotalTaxInclusiveAmountIc()));
    transaction.setTotalTaxExclusiveDiscountAmountIc(stripDecimal(transaction.getTotalTaxExclusiveDiscountAmountIc()));
    transaction.setTotalTaxInclusiveDiscountAmountIc(stripDecimal(transaction.getTotalTaxInclusiveDiscountAmountIc()));
    transaction.setTotalTaxCalculatedIc(stripDecimal(transaction.getTotalTaxCalculatedIc()));
    transaction.setTotalTaxExclusiveDiscountAmount(stripDecimal(transaction.getTotalTaxExclusiveDiscountAmount()));
    transaction.setTotalTaxInclusiveDiscountAmount(stripDecimal(transaction.getTotalTaxInclusiveDiscountAmount()));
    transaction.setExchangeRate(stripDecimal(transaction.getExchangeRate()));

    if (CollectionUtils.isNotEmpty(transaction.getLines())) {
      transaction.getLines().forEach(this::stripTransactionLineTrailingZeros);
    }
  }

  /**
   * 去除 TransactionLine 中所有 BigDecimal 字段的尾随零
   */
  private void stripTransactionLineTrailingZeros(TransactionLine line) {
    if (line == null) {
      return;
    }

    line.setQuantity(stripDecimal(line.getQuantity()));
    line.setUnitPrice(stripDecimal(line.getUnitPrice()));
    line.setAmount(stripDecimal(line.getAmount()));
    line.setDiscountAmount(stripDecimal(line.getDiscountAmount()));
    line.setTaxRate(stripDecimal(line.getTaxRate()));
    line.setTaxAmount(stripDecimal(line.getTaxAmount()));
    line.setTaxAmountIc(stripDecimal(line.getTaxAmountIc()));
    line.setTaxExclusiveUnitPrice(stripDecimal(line.getTaxExclusiveUnitPrice()));
    line.setTaxInclusiveUnitPrice(stripDecimal(line.getTaxInclusiveUnitPrice()));
    line.setTaxExclusiveUnitPriceIc(stripDecimal(line.getTaxExclusiveUnitPriceIc()));
    line.setTaxInclusiveUnitPriceIc(stripDecimal(line.getTaxInclusiveUnitPriceIc()));
    line.setTaxExclusiveAmount(stripDecimal(line.getTaxExclusiveAmount()));
    line.setTaxInclusiveAmount(stripDecimal(line.getTaxInclusiveAmount()));
    line.setTaxExclusiveAmountIc(stripDecimal(line.getTaxExclusiveAmountIc()));
    line.setTaxInclusiveAmountIc(stripDecimal(line.getTaxInclusiveAmountIc()));
    line.setTaxExclusiveDiscountAmount(stripDecimal(line.getTaxExclusiveDiscountAmount()));
    line.setTaxInclusiveDiscountAmount(stripDecimal(line.getTaxInclusiveDiscountAmount()));
    line.setTaxExclusiveDiscountAmountIc(stripDecimal(line.getTaxExclusiveDiscountAmountIc()));
    line.setTaxInclusiveDiscountAmountIc(stripDecimal(line.getTaxInclusiveDiscountAmountIc()));
    line.setTaxCalculated(stripDecimal(line.getTaxCalculated()));
    line.setDiscountTaxCalculated(stripDecimal(line.getDiscountTaxCalculated()));
    line.setTaxCalculatedIc(stripDecimal(line.getTaxCalculatedIc()));
    line.setDiscountTaxCalculatedIc(stripDecimal(line.getDiscountTaxCalculatedIc()));
  }

  /**
   * 安全地去除 BigDecimal 的尾随零
   */
  private BigDecimal stripDecimal(BigDecimal value) {
    if (value == null) {
      return null;
    }

    // 直接去除尾随零
    return value.stripTrailingZeros();
  }
}