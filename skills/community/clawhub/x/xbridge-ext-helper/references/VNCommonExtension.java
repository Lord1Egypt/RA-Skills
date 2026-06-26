package com.baiwang.global.transaction.adaptor.vn;

import com.baiwang.xbridge3.database.core.consts.ColumnRoleType;
import com.baiwang.xbridge3.database.extfields.annotation.ColumnStandardType;
import com.baiwang.xbridge3.database.extfields.annotation.EntityColumnSchema;
import com.baiwang.xbridge3.database.extfields.model.ExtensionObjectSpec;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

/**
 * 越南交易扩展信息
 * <p>
 * 该类用于存储越南地区特有的交易相关扩展字段。
 * </p>
 *
 * @author Baiwang
 * @since 1.0
 */
@Setter
@Getter
public class VNCommonExtension {

  public static final ExtensionObjectSpec<VNCommonExtension> KEY = ExtensionObjectSpec.<VNCommonExtension>builder()
      .name("vn")
      .type(VNCommonExtension.class)
      .defaultValueSupplier(VNCommonExtension::new)
      .build();

  /**
   * 发票类型标识符，用于区分不同类型的发票
   * <p>
   * 收银机发票类型:
   * <ul>
   *   <li>{@code 01/MTT}: 收银机开具的增值税发票</li>
   *   <li>{@code 02/MTT}: 收银机开具的销售发票</li>
   * </ul>
   * <p>
   * 常规发票类型:
   * <ul>
   *   <li>{@code 01GTKT}: 常规增值税发票</li>
   *   <li>{@code 02GTTT}: 常规销售发票</li>
   * </ul>
   * </p>
   *
   * <b>约束条件:</b> 当被调整的发票为百望开具时此字段为条件必填
   *
   * @see #invoiceForm
   * @see #invoiceSeries
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Invoice Type",
      columnName = "idx_str1",
      length = 6,
      columnRole = ColumnRoleType.IndexedExtDataField,
      listShowQuery = true
  )
  private String invoiceType;

  /**
   * 发票形式编码
   * <ul>
   *   <li>{@code 1}: 增值税发票</li>
   *   <li>{@code 2}: 销售发票</li>
   * </ul>
   *
   * @see #originalInvoiceForm
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Invoice Form Type",
      columnName = "idx_str2",
      length = 1,
      columnRole = ColumnRoleType.IndexedExtDataField,
      listShowQuery = true
  )
  private String invoiceForm;

  /**
   * 发票序列号，格式如: K26MYY, C26TYY
   *
   * @see #originalInvoiceSeries
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Invoice Series",
      columnName = "idx_str3",
      length = 8,
      columnRole = ColumnRoleType.IndexedExtDataField,
      listShowQuery = true
  )
  private String invoiceSeries;

  /**
   * 发票号码
   *
   * @since 1.0
   */
  @EntityColumnSchema(
          title = "Invoice No.",
          columnName = "idx_str4",
          length = 20,
          columnRole = ColumnRoleType.IndexedExtDataField,
          listShowQuery = true
  )
  private String invoiceNo;

  /**
   * 付款方式编码
   * <ul>
   *   <li>{@code TM}: 现金</li>
   *   <li>{@code CK}: 银行转账</li>
   *   <li>{@code TM/CK}: 现金/银行转账</li>
   *   <li>{@code DTCN}: 债务抵消</li>
   *   <li>{@code KTT}: 需付款</li>
   * </ul>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Payment Method",
      columnRole = ColumnRoleType.VirtualExtDataField,
      listShowQuery = true
  )
  private String paymentMethodCode;

  /**
   * 发票类别编码
   * <ul>
   *   <li>{@code 0}: 标准发票项目</li>
   *   <li>{@code 2}: 付款/结算发票项目</li>
   * </ul>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Invoice Class",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String invoiceClass;

  /**
   * 购买方全称，若发票用于报销则需填写企业全称
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Full Buyer Name",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String fullBuyerName;

  /**
   * 预算关系代码，用于财务预算管理
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Budget Relation Id",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String budgetRelationId;

  /**
   * 购买方证件类型编码
   * <ul>
   *   <li>{@code 1}: 身份证</li>
   *   <li>{@code 2}: 护照</li>
   * </ul>
   *
   * @see #buyerIdNo
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Buyer Id Type",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String buyerIdType;

  /**
   * 购买方证件号码
   * <p>
   * 当 [buyerIdType](file:///D:\Workspace\einvoice\global-document-engine\document-engine-api\src\main\java\com\baiwang\global\transaction\adaptor\vn\VNTransactionExtension.java#L180-L180) 有值时此字段必填
   * </p>
   *
   * @see #buyerIdType
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Buyer Id No.",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String buyerIdNo;

  /**
   * 原发票形式 - 调整发票时使用
   * <p>
   * 条件必填：当被调整的发票为百望开具时
   * </p>
   *
   * @see #invoiceForm
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Original Invoice Form",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String originalInvoiceForm;

  /**
   * 原发票号码 - 调整发票时使用
   * <p>
   * 条件必填：当被调整的发票为百望开具时
   * </p>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Original Invoice No.",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String originalInvoiceNo;

  /**
   * 原发票序列号 - 调整发票时使用
   * <p>
   * 示例：K26MYY或C26TYY
   * 条件必填：当被调整的发票为百望开具时
   * </p>
   *
   * @see #invoiceSeries
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Original Invoice Series",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String originalInvoiceSeries;

  /**
   * 原发票开票日期 - 调整发票时使用
   * <p>
   * 格式：ISO 8601日期格式
   * 条件必填：当被调整的发票为百望开具时
   * </p>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Original Issue Date",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String originalIssueDate;

  /**
   * 使用交易货币开票标志
   * <ul>
   *   <li>{@code false}: 使用本币开票</li>
   *   <li>{@code true}: 使用交易货币开票</li>
   * </ul>
   * <p>
   * 默认值为false，即使用转换后的本币开票
   * </p>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Use Exchange Issue Flag",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private Boolean useExchangeIssueFlag;

  /**
   * 调整或替换原因
   * <p>
   * 记录发票调整或替换的具体原因说明
   * </p>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Adjust Reason",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String adjustReason;

  /**
   * 校验码
   * <p>
   * 对应越南 MCQT
   * </p>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
      title = "Check Code",
      columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String checkCode;


  /**
   *
   *
   * 跟 FPT 交互防重的唯一ID,  UUID
   *  transactionUuid 与 invoiceSid 一一对应
   *  交易入库时 生成 invoiceSid
   * <p>
   * 对应越南 sid
   * </p>
   *
   * @since 1.0
   */
  @EntityColumnSchema(
          title = "Invoice Sid",
          columnRole = ColumnRoleType.VirtualExtDataField
  )
  private String invoiceSid;

  // ==================== 整单折扣相关字段 ====================

  /**
   * 整单折扣金额（正数）
   * <p>
   * 与 {@link #commercialDiscountRate} 互斥，二者只能选其一
   * 当 discountTaxIncluded="1" 时，此金额为含税金额
   * 当 discountTaxIncluded="0" 时，此金额为不含税金额
   * </p>
   * <p>
   * <b>约束条件:</b>
   * <ul>
   *   <li>必须 ≤ 发票总金额</li>
   *   <li>精度：小数点后≤6位</li>
   *   <li>与 commercialDiscountRate 互斥</li>
   * </ul>
   * </p>
   *
   * @since 1.2
   */
  @EntityColumnSchema(
      title = "Commercial Discount Amount",
      columnName = "idx_number1",
      length = 20,
      scale = 6,
      columnRole = ColumnRoleType.IndexedExtDataField
  )
  private java.math.BigDecimal commercialDiscount;

  /**
   * 整单折扣比例 (0,1)
   * <p>
   * 与 {@link #commercialDiscount} 互斥，二者只能选其一
   * 示例: 0.10 表示10%折扣
   * </p>
   * <p>
   * <b>约束条件:</b>
   * <ul>
   *   <li>必须在 (0,1) 范围内，不包含0和1</li>
   *   <li>精度：小数点后≤4位</li>
   *   <li>与 commercialDiscount 互斥</li>
   * </ul>
   * </p>
   *
   * @since 1.2
   */
  @EntityColumnSchema(
      title = "Commercial Discount Rate",
      columnName = "idx_number2",
      length = 10,
      scale = 4,
      columnRole = ColumnRoleType.IndexedExtDataField
  )
  private java.math.BigDecimal commercialDiscountRate;

  /**
   * 折扣是否含税
   * <p>
   * "1"=含税折扣：折扣金额为含税金额，系统需进行价税分离
   * "0"=不含税折扣：折扣金额为不含税金额，系统需计算税额
   * </p>
   * <p>
   * <b>约束条件:</b> 当 commercialDiscount 或 commercialDiscountRate 有值时必填
   * </p>
   *
   * @since 1.2
   */
  @EntityColumnSchema(
      title = "Discount Tax Included",
      columnName = "idx_str5",
      length = 1,
      columnRole = ColumnRoleType.IndexedExtDataField
  )
  private String discountTaxIncluded;

  /**
   * 折扣分摊方式
   * <p>
   * 定义整单折扣如何在发票明细行之间进行分摊。
   * 用户传入数值代码指定分摊方式。
   * </p>
   * <p>
   * <b>枚举值:</b>
   * <ul>
   *   <li>{@code 0}: 按税率段汇总分摊(BY_TAX_RATE)，生成独立CK折扣行(lineType=1)</li>
   *   <li>{@code 1}: 按明细行逐行分摊(BY_LINE_ITEM)，折扣内嵌明细行</li>
   * </ul>
   * </p>
   * <p>
   * <b>约束条件:</b> 当 commercialDiscount 或 commercialDiscountRate 有值时必填
   * </p>
   *
   * @since 1.2
   */
  @EntityColumnSchema(
      title = "Commercial Discount Method",
      columnName = "idx_str6",
      length = 50,
      columnRole = ColumnRoleType.IndexedExtDataField
  )
  private String commercialDiscountMethod;

  @EntityColumnSchema(
      title = "Commercial Discount itemCodes",
      columnRole = ColumnRoleType.VirtualExtDataField,
      type = ColumnStandardType.EXT_JSON
  )
  private List<String> commercialDiscountItemCodes;
}
