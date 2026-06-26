# Retrofit + Kotlin 代码模板参考

## 基础 Service 接口模板

```kotlin
package com.example.api

import retrofit2.http.*
import okhttp3.ResponseBody

interface ApiService {
    
    // GET 请求
    @GET("users/{id}")
    suspend fun getUserById(
        @Path("id") id: String
    ): User
    
    // 带查询参数的 GET
    @GET("users")
    suspend fun getUsers(
        @Query("page") page: Int? = null,
        @Query("size") size: Int? = null
    ): List<User>
    
    // POST 请求
    @POST("users")
    suspend fun createUser(
        @Body body: CreateUserRequest
    ): User
    
    // PUT 请求
    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") id: String,
        @Body body: UpdateUserRequest
    ): User
    
    // DELETE 请求
    @DELETE("users/{id}")
    suspend fun deleteUser(
        @Path("id") id: String
    ): ResponseBody
}
```

## 数据类模板

```kotlin
data class User(
    val id: Long,
    val username: String,
    val email: String?,
    val createdAt: String?
)

data class CreateUserRequest(
    val username: String,
    val email: String? = null,
    val password: String
)

// 泛型响应包装
data class ApiResponse<T>(
    val code: Int,
    val message: String,
    val data: T?
)
```

## Retrofit 客户端配置

```kotlin
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {
    
    private const val BASE_URL = "https://api.example.com/"
    
    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .addInterceptor { chain ->
            val request = chain.request().newBuilder()
                .addHeader("Accept", "application/json")
                .addHeader("Content-Type", "application/json")
                .build()
            chain.proceed(request)
        }
        .build()
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val apiService: ApiService = retrofit.create(ApiService::class.java)
}
```

## 认证配置

### Basic Auth

```kotlin
import okhttp3.Credentials

val client = OkHttpClient.Builder()
    .addInterceptor { chain ->
        val request = chain.request().newBuilder()
            .header("Authorization", Credentials.basic("username", "password"))
            .build()
        chain.proceed(request)
    }
    .build()
```

### Bearer Token

```kotlin
val client = OkHttpClient.Builder()
    .addInterceptor { chain ->
        val request = chain.request().newBuilder()
            .header("Authorization", "Bearer $token")
            .build()
        chain.proceed(request)
    }
    .build()
```

## 常用注解速查

| 注解 | 用途 | 示例 |
|-----|------|------|
| @GET | GET 请求 | `@GET("users")` |
| @POST | POST 请求 | `@POST("users")` |
| @PUT | PUT 请求 | `@PUT("users/{id}")` |
| @DELETE | DELETE 请求 | `@DELETE("users/{id}")` |
| @Path | URL 路径参数 | `@Path("id") id: String` |
| @Query | URL 查询参数 | `@Query("page") page: Int` |
| @QueryMap | 多个查询参数 | `@QueryMap params: Map<String, String>` |
| @Header | 请求头 | `@Header("X-Token") token: String` |
| @Headers | 固定请求头 | `@Headers("Accept: application/json")` |
| @Body | 请求体 | `@Body user: User` |
| @Field | 表单字段 | `@Field("name") name: String` |
| @FormUrlEncoded | 表单编码 | 标记方法 |
| @Multipart | 多部分上传 | 标记方法 |
| @Part | 多部分字段 | `@Part file: MultipartBody.Part` |
