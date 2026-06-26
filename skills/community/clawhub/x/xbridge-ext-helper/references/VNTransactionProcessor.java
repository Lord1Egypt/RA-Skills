package com.baiwang.global.document.adaptor.vn;

import com.alibaba.fastjson.JSON;
import com.baiwang.global.document.calculator.TransactionTaxCalculator;
import com.baiwang.global.document.calculator.TransactionTaxContext;
import com.baiwang.global.document.dao.entity.Transaction;
import com.baiwang.global.document.dao.entity.TransactionLine;
import com.baiwang.global.document.service.plugin.TransactionExtensionManager;
import com.baiwang.global.document.service.plugin.TransactionValidator;
import com.baiwang.global.document.service.plugin.model.*;
import com.baiwang.global.document.service.vn.discount.DiscountCalculationService;
import com.baiwang.global.document.service.vn.discount.DiscountDistributionContext;
import com.baiwang.global.document.service.TransactionHistoryService;
import com.baiwang.global.document.service.plugin.TransactionProcessor;
import com.baiwang.global.transaction.consts.CountryCode;
import com.baiwang.global.transaction.consts.CurrencyCode;
import com.baiwang.global.transaction.consts.TransactionType;
import com.baiwang.xbridge3.database.extfields.model.EntityTableSchemaConfig;
import com.baiwang.xbridge3.database.extfields.model.EntityTableSchemaID;
import com.baiwang.xbridge3.database.extfields.spi.EntityTableSchemaConfigItem;
import com.baiwang.xbridge3.database.extfields.spi.EntityTableSchemaConfigProvider;
import com.baiwang.xbridge3.database.extfields.support.EntitySchemaAnnotationParser;
import com.google.common.collect.Sets;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import java.util.Set;
import java.util.function.Function;

@Slf4j
@Component
@RequiredArgsConstructor
public class VNTransactionProcessor implements TransactionProcessor, EntityTableSchemaConfigProvider {

  static final Set<TransactionBusinessRoute> ROUTES = Sets.newHashSet(
      TransactionBusinessRoute.builder()
          .countryCode(CountryCode.VN)
          .transactionType(TransactionType.SalesInvoice)
          .build(),
      TransactionBusinessRoute.builder()
          .countryCode(CountryCode.VN)
          .transactionType(TransactionType.AdjustInvoice)
          .build(),
      TransactionBusinessRoute.builder()
          .countryCode(CountryCode.VN)
          .transactionType(TransactionType.ReplaceInvoice)
          .build()
  );

  private final TransactionTaxCalculator taxCalculator;
  private final TransactionHistoryService transactionHistoryService;
  private final DiscountCalculationService discountCalculationService;
  private final TransactionExtensionManager transactionExtensionManager;

  @Override
  public boolean supports(TransactionBusinessRoute route) {
    return ROUTES.contains(route);
  }

  @Override
  public EntityTableSchemaConfigItem getSchemaConfig() {
    EntityTableSchemaConfig vnTransactionSchema = EntitySchemaAnnotationParser.parseExtension(
        VNTransactionExtension.class,
        VNTransactionLineExtension.class
    );
    return EntityTableSchemaConfigItem.builder()
        .tableSchemaID(EntityTableSchemaID.parse("global.VN"))
        .tableSchemaConfig(vnTransactionSchema)
        .build();
  }

  @Override
  public void beforeCreateTransaction(TransactionCreateContext context) {
    Transaction transaction = context.getTransaction();

    // 1. 【关键步骤】保存原始单据到历史表（在折扣计算前执行）
    //saveOriginalTransactionToHistory(transaction, "CREATE");

    // 2. 处理整单折扣计算
    processCommercialDiscount(context);

    // 3. 执行金额计算和价税分离
    doCalculateAmount(transaction);
  }

  private void doCalculateAmount(Transaction transaction) {
    TransactionTaxContext taxContext = TransactionTaxContext.builder()
        .amountRounding(amountRounding(transaction))
        .invoiceAmountRounding(invoiceAmountRounding(transaction))
        .unitPriceRounding(unitPriceRounding(transaction))
        .quantityRounding(quantityRounding(transaction))
        .transaction(transaction)
        .build();
    // 金额精度预处理
    for (TransactionLine line : transaction.getLines()) {
      if (line.getQuantity() != null) {
        line.setQuantity(taxContext.getQuantityRounding().apply(line.getQuantity()));
      }
      if (line.getUnitPrice() != null) {
        line.setUnitPrice(taxContext.getUnitPriceRounding().apply(line.getUnitPrice()));
      }
      if(line.getAmount() != null){
        line.setAmount(taxContext.getAmountRounding().apply(line.getAmount()));
      }
      if (line.getDiscountAmount() != null) {
        line.setDiscountAmount(taxContext.getAmountRounding().apply(line.getDiscountAmount()));
      }
      if (line.getTaxAmount() != null) {
        line.setTaxAmount(taxContext.getAmountRounding().apply(line.getTaxAmount()));
      }
    }
    // 价税分离计算
    taxCalculator.calculateVATTax(taxContext);
  }

  @Override
  public void beforeUpdateTransaction(TransactionUpdateContext context) {
    Transaction transaction = context.getTransaction();

/*    // 1. 【关键步骤】保存原始单据到历史表（在折扣计算前执行）
    String operationType = transaction.getTransactionType();
    if (TransactionType.ReplaceInvoice.getCode().equals(operationType)) {
      saveOriginalTransactionToHistory(transaction, "REPLACE");
    } else if (TransactionType.AdjustInvoice.getCode().equals(operationType)) {
      saveOriginalTransactionToHistory(transaction, "ADJUST");
    } else {
      saveOriginalTransactionToHistory(transaction, "UPDATE");
    }*/

    // 2. 处理整单折扣计算
    processCommercialDiscount(context);

    // 3. 执行金额计算和价税分离
    doCalculateAmount(transaction);
  }

  @Override
  public void beforeCommitTransaction(TransactionCommitContext context) {

  }

  /**
   * 保存原始交易数据到历史表
   * <p>
   * 在折扣计算前调用，保存原始单据数据以满足审计追踪要求。
   * </p>
   *
   * @param transaction 原始交易数据
   * @param operationType 操作类型
   */
  private void saveOriginalTransactionToHistory(Transaction transaction, String operationType) {
    try {
      transactionHistoryService.saveOriginalTransaction(transaction, operationType);
    } catch (Exception e) {
      // 历史表保存失败不应阻塞主流程，仅记录警告日志
      log.warn("保存原始交易数据到历史表失败，transactionId={}, operationType={}",
              transaction.getId(), operationType, e);
    }
  }

  /**
   * 处理整单折扣
   * <p>
   * 根据越南扩展字段中的折扣参数，计算并分摊折扣金额到明细行。
   * 支持含税/不含税折扣，以及按税率段分摊或按明细行分摊两种方式。
   * </p>
   * <p>
   * <b>注意：</b>此方法只负责折扣计算和分摊，不执行参数校验。
   * 所有参数校验已在 VNTransactionValidator.validateDiscountParameters 中完成。
   * </p>
   *
   * @param transactionValidateContext 交易校验上下文
   */
  public void processCommercialDiscount(TransactionValidateContext transactionValidateContext) {
    Transaction transaction = transactionValidateContext.getTransaction();
    // 使用折扣计算服务处理整单折扣
    DiscountDistributionContext context = discountCalculationService.calculate(transaction);

    if (context == null) {
      log.debug("交易没有折扣参数或折扣计算被跳过");
      return;
    }

    // 应用折扣分摊结果
    applyDiscountDistributionResult(transaction, context);

    log.info("整单折扣处理完成，transaction:{}", JSON.toJSONString(transaction));
    TransactionBusinessRoute businessRoute = TransactionBusinessRoute.builder()
        .transactionType(TransactionType.fromCode(transaction.getTransactionType()))
        .countryCode(CountryCode.fromCode(transaction.getCountryCode()))
        .build();
    List<TransactionValidator> validators = transactionExtensionManager.getValidatorsRegistry().getPluginsFor(businessRoute);
    for (TransactionValidator validator : validators) {
      validator.validateAccumulation(transactionValidateContext, true);
    }
  }

  /**
   * 应用折扣分摊结果到交易数据
   *
   * @param transaction 交易数据
   * @param context 折扣分摊上下文
   */
  private void applyDiscountDistributionResult(Transaction transaction, DiscountDistributionContext context) {
    // 按明细行分摊时，各行折扣金额已在分摊策略中更新
    // 如果有折扣行，添加到交易明细
    if (context.getDiscountLines() != null && !context.getDiscountLines().isEmpty()) {
      List<TransactionLine> lines = transaction.getLines();
      if (!CollectionUtils.isEmpty(lines)) {
        // 为折扣行分配行号
        int maxLineNumber = lines.stream()
                .mapToInt(line -> line.getLineNumber() == null ? 0 : line.getLineNumber())
                .max()
                .orElse(0);

        for (TransactionLine discountLine : context.getDiscountLines()) {
          discountLine.setLineNumber(++maxLineNumber);
          lines.add(discountLine);
        }
      }
    }
  }

  private Function<BigDecimal, BigDecimal> quantityRounding(Transaction transaction) {
    return raw -> raw.setScale(3, RoundingMode.HALF_UP);
  }

  private Function<BigDecimal, BigDecimal> unitPriceRounding(Transaction transaction) {
    return raw -> raw.setScale(6, RoundingMode.HALF_UP);
  }

  private Function<BigDecimal, BigDecimal> amountRounding(Transaction transaction) {
    if (CurrencyCode.VND.getCode().equals(transaction.getCurrencyCode())) {
      return raw -> raw.setScale(0, RoundingMode.HALF_UP);
    } else {
      return raw -> raw.setScale(2, RoundingMode.HALF_UP);
    }
  }

  private Function<BigDecimal, BigDecimal> invoiceAmountRounding(Transaction transaction) {
    if (CurrencyCode.VND.getCode().equals(transaction.getExchangeRateCurrencyCode())) {
      return raw -> raw.setScale(0, RoundingMode.HALF_UP);
    } else {
      return raw -> raw.setScale(2, RoundingMode.HALF_UP);
    }
  }
}
