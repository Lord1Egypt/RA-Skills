package com.baiwang.global.document.adaptor.vn;

import com.baiwang.global.transaction.adaptor.vn.VNCommonExtension;
import com.baiwang.xbridge3.database.extfields.annotation.EntityExtensionSchema;
import lombok.Data;


@EntityExtensionSchema(
    tableId = "gbw_transaction",
    extNamespace = "vn"
)
@Data
public class VNTransactionExtension extends VNCommonExtension {


}
