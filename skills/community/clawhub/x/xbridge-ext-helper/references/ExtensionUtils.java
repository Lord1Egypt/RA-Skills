package com.baiwang.global.transaction.utils;

import com.baiwang.xbridge3.common.json.JacksonObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class ExtensionUtils {
    public static <T> T getExtension(String key, Class<T> type,ObjectNode extensions) {
        if (extensions == null) {
            return null;
        }
        JsonNode value = extensions.path(key);
        if (!value.isObject()) {
            return null;
        }
        return JacksonObjectMapper.get().toJavaObject(value, type);
    }

}
