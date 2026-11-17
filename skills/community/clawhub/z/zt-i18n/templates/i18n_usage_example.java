package com.zt.example.controller;

import com.zt.digital.common.api.base.ResultVo;
import com.zt.digital.common.api.base.ResultCode;
import com.zt.digital.common.exception.BusinessException;
import com.zt.digital.common.i18n.service.MessageSourceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import java.io.Serializable;

/**
 * ZT I18n 国际化使用示例
 */
@RestController
@RequestMapping("/i18n-demo")
public class I18nDemoController {

    @Autowired
    private MessageSourceService messageSourceService;

    /**
     * 1. ResultVo 国际化
     * 返回 ResultVo 且 message 属性作为国际化 key
     */
    @GetMapping("/success")
    public ResultVo<String> testResultVoI18n() {
        // "query.result.success" 是 properties 或数据库中的 key
        return ResultVo.success("data content", "query.result.success");
    }

    /**
     * 2. 异常提示信息国际化 (带动态参数)
     * 抛出 BusinessException, message 作为国际化 key
     */
    @GetMapping("/error")
    public ResultVo testExceptionI18n() {
        // "business.error" 是 key, "Xiaomi" 和 "-20" 是填充 {0} 和 {1} 的参数
        throw new BusinessException(new ResultCode(506, "business.error", "Xiaomi", "-20"));
    }

    /**
     * 3. 手动获取国际化信息 (Service 注入)
     */
    @GetMapping("/manual")
    public ResultVo<String> testManualI18n() {
        // 获取无参数信息
        String name = messageSourceService.getMessage("name");
        
        // 获取带动态参数信息
        String ageMsg = messageSourceService.getMessage("age.range.error", 18, 60);
        
        return ResultVo.success("Name: " + name + ", AgeMsg: " + ageMsg);
    }

    /**
     * 4. 参数校验国际化
     */
    @PostMapping("/validate")
    public ResultVo testValidateI18n(@Valid @RequestBody UserReqVO user) {
        return ResultVo.success();
    }
}

/**
 * 请求入参实体, 使用校验注解配合国际化 key
 */
class UserReqVO implements Serializable {
    @NotEmpty(message = "name.not.empty")
    private String name;
    
    // getter and setter...
}
