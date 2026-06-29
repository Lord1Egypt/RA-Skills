# 多语言术语表（Glossary）— 优化版 v2.1

> 本表为 AI 回复时的术语翻译标准。同一概念在所有对话中必须使用本表规定的译法，不可随意替换。
>
> 规则：
> - 技术标识符（字段名、域名、路径、错误码）**不翻译**，直接使用原文
> - 下表收录**业务术语**和**产品名称**的标准译法
> - 本优化版优先对齐微信支付全球平台官方英文术语，并修正多语言直译、重复与不一致问题
>
> 语言列顺序：中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية

---

## 角色与主体

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 机构 | Institution (Acquiring Institution) | 機関（アクワイアラ） | 기관 (매입 기관) | Institution acquéreuse | Institución adquirente | Instituição adquirente | Эквайринговая организация | مؤسسة (جهة قبول المدفوعات) |
| 子商户 | Sub-merchant | サブマーチャント | 하위 가맹점 | Sous-marchand | Sub-comerciante | Sub-comerciante | Субмерчант | تاجر فرعي |
| 直联商户 | Direct Merchant | 直結加盟店 | 직접 연결 가맹점 | Marchand direct | Comerciante directo | Comerciante direto | Прямой мерчант | تاجر مباشر |
| 商户平台 | Merchant Platform | マーチャントプラットフォーム | 가맹점 플랫폼 | Plateforme marchand | Plataforma de comerciante | Plataforma do comerciante | Платформа мерчанта | منصة التاجر |
| 技术支持 | Technical Support (TS) | テクニカルサポート（TS） | 기술 지원 (TS) | Support technique (TS) | Soporte técnico (TS) | Suporte técnico (TS) | Техническая поддержка (TS) | الدعم الفني (TS) |
| 商户 | Merchant | 加盟店 | 가맹점 | Marchand | Comerciante | Comerciante | Мерчант | التاجر |
| 机构号 | Institution ID | 機関ID | 기관 ID | ID d'institution | ID de institución | ID da instituição | ID организации | معرف المؤسسة |
| 子商户号 | Sub-merchant ID | サブマーチャントID | 하위 가맹점 ID | ID du sous-marchand | ID de sub-comerciante | ID do sub-comerciante | ID субмерчанта | معرف التاجر الفرعي |
| 商户号 | Merchant ID | 加盟店ID | 가맹점 ID | ID marchand | ID de comerciante | ID do comerciante | ID мерчанта | معرف التاجر |
| 机构服务商 | Institution | 機関 | 기관 | Institution | Institución | Instituição | Организация | مؤسسة |
| 收单机构 | Acquiring Institution | アクワイアリング機関 | 매입 기관 | Institution acquéreuse | Institución adquirente | Instituição adquirente | Эквайринговая организация | مؤسسة قبول المدفوعات |
| 二级商户 | Sub-merchant | サブマーチャント | 하위 가맹점 | Sous-marchand | Sub-comerciante | Sub-comerciante | Субмерчант | تاجر فرعي |
| 父子商户关系 | Parent-child Merchant Relationship | 親子加盟店関係 | 부모-자식 가맹점 관계 | Relation marchand parent-enfant | Relación comerciante padre-hijo | Relação comerciante pai-filho | Отношение родитель-дочерний мерчант | علاقة التاجر الأصلي والفرعي |
| 渠道方 | Channel | チャネル | 채널 | Canal | Canal | Canal | Канал | القناة |

---

## 支付产品

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 付款码支付 | Quick Pay | クイックペイ（決済コード決済） | 결제 코드 결제 | Paiement par code de paiement | Pago con código de pago | Pagamento com código de pagamento | Оплата по платёжному коду | الدفع برمز الدفع |
| Native 支付 | Native Payment | Native決済 | Native 결제 | Paiement Native | Pago Native | Pagamento Native | Платёж Native | دفع Native |
| JSAPI 支付 | JSAPI Payment | JSAPI決済 | JSAPI 결제 | Paiement JSAPI | Pago JSAPI | Pagamento JSAPI | Платёж JSAPI | الدفع عبر JSAPI |
| APP 支付 | In-App Payment | アプリ内決済 | 앱 내 결제 | Paiement in-app | Pago en aplicación | Pagamento in-app | Платёж в приложении | الدفع داخل التطبيق |
| 小程序支付 | Mini Program Payment | ミニプログラム決済 | 미니 프로그램 결제 | Paiement Mini Programme | Pago Mini Programa | Pagamento Mini Programa | Платёж мини-программы | الدفع عبر البرنامج المصغر |
| H5 支付 | H5 Payment | H5決済 | H5 결제 | Paiement H5 | Pago H5 | Pagamento H5 | Платёж H5 | الدفع عبر H5 |
| 委托代扣 | Auto-Debit Payment | 委託自動引落し | 위탁 자동 차감 | Paiement par prélèvement automatique autorisé | Pago con débito automático autorizado | Pagamento por débito automático autorizado | Автоматическое списание по поручению | الدفع بالخصم التلقائي المفوض |
| 扫码支付 | QR Code Pay | QRコード決済 | QR 코드 결제 | Paiement par QR code | Pago con código QR | Pagamento por QR code | Оплата QR-кодом | الدفع برمز QR |
| 刷卡支付 | Quick Pay (Barcode Payment) | バーコード決済（Quick Pay） | 바코드 결제(Quick Pay) | Paiement par code-barres (Quick Pay) | Pago con código de barras (Quick Pay) | Pagamento com código de barras (Quick Pay) | Оплата по штрих-коду (Quick Pay) | الدفع بالباركود (Quick Pay) |
| 免密支付 | Password-free Payment | パスワードレス決済 | 비밀번호 없는 결제 | Paiement sans mot de passe | Pago sin contraseña | Pagamento sem senha | Беспарольный платёж | الدفع بدون كلمة مرور |
| 先享后付 | Use First, Pay Later | 先使用後払い | 먼저 사용 후 결제 | Utiliser d'abord, payer après | Usar primero, pagar después | Usar primeiro, pagar depois | Сначала пользуйся, потом плати | استخدم أولاً وادفع لاحقاً |
| 验密支付 | Password-based Payment | パスワード確認決済 | 비밀번호 확인 결제 | Paiement avec mot de passe | Pago con contraseña | Pagamento com senha | Платёж с подтверждением пароля | الدفع بتأكيد كلمة المرور |

---

## 扩展能力

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 跨境分账 | cross-border funds-distribution | クロスボーダー資金分配 | 크로스보더 자금 분배 | Distribution transfrontalière des fonds | Distribución transfronteriza de fondos | Distribuição transfronteiriça de fundos | Трансграничное распределение средств | توزيع الأموال عبر الحدود |
| 子商户进件 | Sub-merchant Onboarding | サブマーチャント登録 | 하위 가맹점 등록 | Enregistrement sous-marchand | Incorporación de sub-comerciante | Integração de sub-comerciante | Регистрация субмерчанта | تأهيل التاجر الفرعي |
| 海关报关 | Customs Declaration | 通関申告 | 세관 신고 | Déclaration douanière | Declaración aduanera | Declaração aduaneira | Таможенная декларация | التصريح الجمركي |
| H5 支付权限申请 | H5 Payment Permission Application | H5決済権限申請 | H5 결제 권한 신청 | Demande d'autorisation H5 | Solicitud de permiso de pago H5 | Solicitação de permissão de pagamento H5 | Заявка на разрешение платежа H5 | طلب إذن الدفع H5 |
| 分账 | funds-distribution | 資金分配 | 자금 분배 | Distribution des fonds | Distribución de fondos | Distribuição de fundos | Распределение средств | توزيع الأموال |
| 分账接收方 | funds-distribution receiver | 資金分配受取人 | 자금 분배 수신자 | Bénéficiaire | Receptor | Receptor | Получатель распределения средств | مستلم توزيع الأموال |
| 分账金额 | funds-distribution amount | 分配金額 | 분배 금액 | Montant de distribution | Importe de distribución | Valor de distribuição | Сумма распределения | مبلغ التوزيع |
| 分账服务 | funds-distribution service | 資金分配サービス | 자금 분배 서비스 | Service de distribution des fonds | Servicio de distribución de fondos | Serviço de distribuição de fundos | Сервис распределения средств | خدمة توزيع الأموال |
| 境内分账 | domestic funds-distribution | 国内資金分配 | 국내 자금 분배 | Distribution domestique des fonds | Distribución doméstica de fondos | Distribuição doméstica de fundos | Внутреннее распределение средств | التوزيع المحلي للأموال |
| 子商户入驻 | Sub-merchant Onboarding | サブマーチャント登録 | 하위 가맹점 등록 | Intégration du sous-marchand | Incorporación del sub-comerciante | Integração do sub-comerciante | Регистрация субмерчанта | تأهيل التاجر الفرعي |

---

## 业务概念

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 境外支付 | Cross-border Payment | クロスボーダー決済 | 국경간 결제 | Paiement transfrontalier | Pago transfronterizo | Pagamento transfronteiriço | Трансграничный платёж | الدفع عبر الحدود |
| 境内支付 | Domestic Payment | 国内決済 | 국내 결제 | Paiement domestique | Pago doméstico | Pagamento doméstico | Внутренний платёж | الدفع المحلي |
| 大陆钱包 | Mainland Wallet (CNY) | 大陸ウォレット（CNY） | 본토 지갑 (CNY) | Portefeuille continental (CNY) | Billetera continental (CNY) | Carteira continental (CNY) | Материковый кошелёк (CNY) | محفظة البر الرئيسي (CNY) |
| 香港钱包 | Hong Kong, China Wallet (HKD) | 中国香港ウォレット（HKD） | 중국 홍콩 지갑 (HKD) | Portefeuille de Hong Kong, Chine (HKD) | Billetera de Hong Kong, China (HKD) | Carteira de Hong Kong, China (HKD) | Кошелёк Гонконга, Китай (HKD) | محفظة هونغ كونغ، الصين (HKD) |
| 结算币种 | Settlement Currency | 決済通貨 | 정산 통화 | Devise de règlement | Moneda de liquidación | Moeda de liquidação | Расчётная валюта | عملة التسوية |
| 标价币种 | Transaction Currency | 表示通貨 | 표시 통화 | Devise de transaction | Moneda de transacción | Moeda de transação | Транзакционная валюта | عملة المعاملة |
| 资金池 | Fund Pool | 資金プール | 자금 풀 | Pool de fonds | Fondo común | Fundo comum | Фонд средств | مجمع الأموال |
| 换汇 | Currency Exchange | 為替 | 환전 | Change de devises | Cambio de divisas | Câmbio de moeda | Обмен валюты | تبادل العملات |
| 受理关系 | Payment Acceptance Relationship | 決済受理関係 | 결제 수락 관계 | Relation d'acceptation des paiements | Relación de aceptación de pagos | Relação de aceitação de pagamentos | Отношение приёма платежей | علاقة قبول المدفوعات |
| 融合机构 | Hybrid Institution | ハイブリッド機関 | 하이브리드 기관 | Institution hybride | Institución híbrida | Instituição híbrida | Гибридная организация | مؤسسة هجينة |
| 纯跨境机构 | Cross-border Only Institution | 純クロスボーダー機関 | 순수 크로스보더 기관 | Institution transfrontalière pure | Institución solo transfronteriza | Instituição apenas transfronteiriça | Организация исключительно для трансграничных операций | مؤسسة عابرة للحدود فقط |
| 跨境支付 | Cross-border Payment | クロスボーダー決済 | 국경간 결제 | Paiement transfrontalier | Pago transfronterizo | Pagamento transfronteiriço | Трансграничный платёж | الدفع عبر الحدود |
| 跨境电商 | Cross-border E-commerce | クロスボーダーEC | 크로스보더 전자상거래 | Commerce électronique transfrontalier | Comercio electrónico transfronterizo | Comércio eletrônico transfronteiriço | Трансграничная электронная торговля | التجارة الإلكترونية العابرة للحدود |
| 微信支付 | WeChat Pay | WeChat Pay | WeChat Pay | WeChat Pay | WeChat Pay | WeChat Pay | WeChat Pay | WeChat Pay |
| 财付通 | TenPay | 財付通 | 텐페이 | TenPay | TenPay | TenPay | TenPay | تن باي |
| 结算通道 | Settlement Channel | 決済チャネル | 정산 채널 | Canal de règlement | Canal de liquidación | Canal de liquidação | Расчётный канал | قناة التسوية |
| 汇率 | Exchange Rate | 為替レート | 환율 | Taux de change | Tasa de cambio | Taxa de câmbio | Обменный курс | سعر الصرف |
| 手续费 | Service Fee | 手数料 | 수수료 | Frais de service | Comisión de servicio | Taxa de serviço | Комиссия | رسوم الخدمة |
| 费率 | Rate | 料率 | 요율 | Taux | Tarifa | Taxa | Ставка | المعدل |
| 优惠券 | Coupon | クーポン | 쿠폰 | Coupon | Cupón | Cupom | Купон | قسيمة |
| 优惠码 | Coupon Code | クーポンコード | 쿠폰 코드 | Code promo | Código de descuento | Código de desconto | Промокод | رمز الكوبون |
| 商家汇率券 | Merchant Exchange Coupon | 加盟店為替クーポン | 가맹점 환율 쿠폰 | Coupon de taux de change marchand | Cupón de tipo de cambio del comerciante | Cupom de taxa de câmbio do comerciante | Купон обменного курса мерчанта | قسيمة سعر الصرف للتاجر |
| 专属汇率券 | Better FX Rate Coupon | 専用為替レートクーポン | 전용 환율 쿠폰 | Coupon taux FX préférentiel | Cupón de tipo de cambio preferencial | Cupom de taxa de câmbio preferencial | Купон льготного курса обмена | كوبون سعر الصرف الخاص |
| 商家券 | Merchant Offer Coupon | 加盟店クーポン | 가맹점 쿠폰 | Coupon marchand | Cupón de comerciante | Cupom do comerciante | Купон мерчанта | قسيمة التاجر |
| 微信跨境支付 | WeChat Cross-Border Pay | WeChatクロスボーダー決済 | WeChat 크로스보더 결제 | Paiement transfrontalier WeChat | Pago transfronterizo WeChat | Pagamento transfronteiriço WeChat | Трансграничный платёж WeChat | WeChat Pay عبر الحدود |
| 境外商户平台 | Overseas Merchant Platform | 海外加盟店プラットフォーム | 해외 가맹점 플랫폼 | Plateforme marchand à l'étranger | Plataforma de comerciante en el extranjero | Plataforma do comerciante no exterior | Зарубежная платформа мерчанта | منصة التاجر في الخارج |
| 资金结算出境 | Outbound Funds Settlement | 決済資金の国外送金 | 정산 자금의 해외 송금 | Règlement sortant des fonds | Liquidación de fondos hacia el exterior | Liquidação de fundos para o exterior | Вывод средств для расчётов за рубеж | تسوية الأموال إلى الخارج |
| 外汇资金结算 | Foreign exchange funds settlement | 外貨資金決済 | 외화 자금 정산 | Règlement des fonds en devises | Liquidación de fondos en divisas | Liquidação de fundos em moeda estrangeira | Расчёты средствами в иностранной валюте | تسوية أموال العملات الأجنبية |
| 收款码物料 | Collection QR Code Materials | 収金QRコード素材 | 수금 QR 코드 자료 | Supports de QR code d’encaissement | Materiales del código QR de cobro | Materiais do código QR de cobrança | Материалы с кодом для приёма платежей | مواد رمز تحصيل المدفوعات |

---

## 技术概念

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 签名 | Signature | 署名 | 서명 | Signature | Firma | Assinatura | Подпись | التوقيع |
| 验签 | Signature Verification | 署名検証 | 서명 검증 | Vérification de signature | Verificación de firma | Verificação de assinatura | Проверка подписи | التحقق من التوقيع |
| 回调通知 | Callback Notification | コールバック通知 | 콜백 알림 | Notification de callback | Notificación de callback | Notificação de callback | Уведомление обратного вызова | إشعار رد الاتصال |
| 平台证书 | Platform Certificate | プラットフォーム証明書 | 플랫폼 인증서 | Certificat de plateforme | Certificado de plataforma | Certificado de plataforma | Сертификат платформы | شهادة المنصة |
| API 证书 | API Certificate | API証明書 | API 인증서 | Certificat API | Certificado API | Certificado API | Сертификат API | شهادة API |
| APIv3 密钥 | APIv3 Key | APIv3キー | APIv3 키 | Clé APIv3 | Clave APIv3 | Chave APIv3 | Ключ APIv3 | مفتاح APIv3 |
| 对账单 | Reconciliation Statement | 照合明細書 | 대사 명세서 | Relevé de rapprochement | Estado de conciliación | Extrato de reconciliação | Выписка сверки | كشف المطابقة |
| 退款 | Refund | 返金 | 환불 | Remboursement | Reembolso | Reembolso | Возврат | استرداد المبلغ |
| 撤销 | Reversal | リバーサル | 리버설 | Annulation de transaction | Reversión | Estorno | Сторнирование | عكس العملية |
| 查单 | Query Order | 注文照会 | 주문 조회 | Consultation de commande | Consulta de pedido | Consulta de pedido | Запрос заказа | استعلام الطلب |
| 关单 | Close Order | 注文クローズ | 주문 마감 | Fermeture de commande | Cierre de pedido | Fechamento de pedido | Закрытие заказа | إغلاق الطلب |
| 下单 | Create Order | 注文作成 | 주문 생성 | Création de commande | Creación de pedido | Criação de pedido | Создание заказа | إنشاء طلب |
| 调起支付 | Initiate Payment | 支払いを開始 | 결제 시작 | Lancer le paiement | Iniciar pago | Iniciar pagamento | Инициировать платёж | بدء الدفع |
| 接入质量检查 | Integration Quality Checklist | 導入品質チェック | 연동 품질 점검 | Contrôle qualité d’intégration | Lista de verificación de calidad de integración | Lista de verificação de qualidade de integração | Контрольный список качества интеграции | قائمة تدقيق جودة التكامل |
| 排障 | Troubleshooting | トラブルシューティング | 문제 해결 | Dépannage | Solución de problemas | Solução de problemas | Устранение неполадок | استكشاف الأخطاء وإصلاحها |
| 免密 | Password-free (No-password) | パスワードレス | 비밀번호 면제 | Sans mot de passe | Sin contraseña | Sem senha | Без пароля | بدون كلمة مرور |
| 验密 | Password Verification | パスワード確認 | 비밀번호 확인 | Vérification du mot de passe | Verificación de contraseña | Verificação de senha | Проверка пароля | التحقق من كلمة المرور |
| 幂等 | Idempotency / Idempotent | 冪等性 | 멱등성 | Idempotence / idempotent | Idempotencia / idempotente | Idempotência / idempotente | Идемпотентность / идемпотентный | عدم التأثر بتكرار الطلب |
| 加速点 | Acceleration Point | アクセラレーションポイント | 가속 포인트 | Point d'accélération | Punto de aceleración | Ponto de aceleração | Точка ускорения | نقطة التسريع |
| 商户证书 | Merchant Certificate | 加盟店証明書 | 가맹점 인증서 | Certificat marchand | Certificado del comerciante | Certificado do comerciante | Сертификат мерчанта | شهادة التاجر |
| 商户私钥 | Merchant Private Key | 加盟店秘密鍵 | 가맹점 개인키 | Clé privée marchand | Clave privada del comerciante | Chave privada do comerciante | Закрытый ключ мерчанта | المفتاح الخاص للتاجر |
| 商户API证书 | Merchant API Certificate | 加盟店API証明書 | 가맹점 API 인증서 | Certificat API marchand | Certificado API del comerciante | Certificado API do comerciante | Сертификат API мерчанта | شهادة API الخاصة بالتاجر |
| 商户API私钥 | Merchant API Private Key | 加盟店API秘密鍵 | 가맹점 API 개인키 | Clé privée API marchand | Clave privada API del comerciante | Chave privada API do comerciante | Закрытый ключ API мерчанта | المفتاح الخاص بـ API للتاجر |
| 平台证书序列号 | Platform Certificate Serial Number | プラットフォーム証明書シリアル番号 | 플랫폼 인증서 일련번호 | Numéro de série du certificat de plateforme | Número de serie del certificado de plataforma | Número de série do certificado de plataforma | Серийный номер сертификата платформы | الرقم التسلسلي لشهادة المنصة |
| 签名串 | Signature String | 署名文字列 | 서명 문자열 | Chaîne de signature | Cadena de firma | String de assinatura | Строка подписи | سلسلة التوقيع |
| 签名值 | Signature Value | 署名値 | 서명 값 | Valeur de signature | Valor de firma | Valor de assinatura | Значение подписи | قيمة التوقيع |
| 签名生成 | Signature Generation | 署名生成 | 서명 생성 | Génération de signature | Generación de firma | Geração de assinatura | Генерация подписи | توليد التوقيع |
| 签名验证 | Signature Verification | 署名検証 | 서명 검증 | Vérification de signature | Verificación de firma | Verificação de assinatura | Верификация подписи | التحقق من التوقيع |
| 支付签名 | paySign | 決済署名 | 결제 서명 | Signature de paiement | Firma de pago | Assinatura de pagamento | Подпись платежа | توقيع الدفع |
| 加解密 | Encryption and Decryption | 暗号化と復号 | 암호화 및 복호화 | Chiffrement et déchiffrement | Cifrado y descifrado | Criptografia e descriptografia | Шифрование и дешифрование | التشفير وفك التشفير |
| 加密算法 | Encryption Algorithm | 暗号化アルゴリズム | 암호화 알고리즘 | Algorithme de chiffrement | Algoritmo de cifrado | Algoritmo de criptografia | Алгоритм шифрования | خوارزمية التشفير |
| 敏感信息 | Sensitive Information | 機密情報 | 민감한 정보 | Informations sensibles | Información sensible | Informações sensíveis | Конфиденциальная информация | المعلومات الحساسة |
| 敏感信息加解密 | Encrypting and Decrypting Sensitive Information | 機密情報の暗号化・復号 | 민감 정보 암호화 및 복호화 | Chiffrement et déchiffrement des informations sensibles | Cifrado y descifrado de información sensible | Criptografia e descriptografia de informações sensíveis | Шифрование и дешифрование конфиденциальной информации | تشفير المعلومات الحساسة وفك تشفيرها |
| 回调报文 | Callback Message | コールバックメッセージ | 콜백 메시지 | Message de callback | Mensaje de callback | Mensagem de callback | Сообщение обратного вызова | رسالة رد الاتصال |
| 对称密钥 | Symmetric Key | 対称鍵 | 대칭 키 | Clé symétrique | Clave simétrica | Chave simétrica | Симметричный ключ | المفتاح المتماثل |
| API安全 | API Security | APIセキュリティ | API 보안 | Sécurité API | Seguridad API | Segurança API | Безопасность API | أمان API |
| 错误码 | Error Code | エラーコード | 오류 코드 | Code d'erreur | Código de error | Código de erro | Код ошибки | رمز الخطأ |
| 付款码 | Payment Code | 決済コード | 결제 코드 | Code de paiement | Código de pago | Código de pagamento | Код оплаты | رمز الدفع |
| 请求参数 | Request Parameters | リクエストパラメータ | 요청 매개변수 | Paramètres de requête | Parámetros de solicitud | Parâmetros de requisição | Параметры запроса | معاملات الطلب |
| 返回参数 | Response Parameters | レスポンスパラメータ | 응답 매개변수 | Paramètres de réponse | Parámetros de respuesta | Parâmetros de resposta | Параметры ответа | معاملات الاستجابة |
| 接口规则 | API Rules | APIルール | API 규칙 | Règles d’API | Reglas de API | Regras de API | Правила API | قواعد API |
| 数据格式 | Data Format | データ形式 | 데이터 형식 | Format de données | Formato de datos | Formato de dados | Формат данных | تنسيق البيانات |
| 枚举值 | Enumerated Value | 列挙値 | 열거 값 | Valeur énumérée | Valor enumerado | Valor enumerado | Перечисляемое значение | قيمة تعدادية |
| 域名 | Domain Name | ドメイン名 | 도메인 이름 | Nom de domaine | Nombre de dominio | Nome de domínio | Доменное имя | اسم النطاق |
| 主域名 | Main Domain Name | メインドメイン名 | 메인 도메인 이름 | Nom de domaine principal | Nombre de dominio principal | Nome de domínio principal | Основное доменное имя | اسم النطاق الرئيسي |
| 子域名 | Sub-domain Name | サブドメイン名 | 서브 도메인 이름 | Nom de sous-domaine | Nombre de subdominio | Nome de subdomínio | Поддоменное имя | اسم النطاق الفرعي |
| H5支付域名 | H5 Payment Domain Name | H5決済ドメイン名 | H5 결제 도메인 이름 | Nom de domaine de paiement H5 | Nombre de dominio de pago H5 | Nome de domínio de pagamento H5 | Доменное имя платежа H5 | اسم نطاق الدفع H5 |
| 网页授权域名 | Web Authorization Domain Name | Webアクセス権限ドメイン名 | 웹 인증 도메인 이름 | Nom de domaine d'autorisation web | Nombre de dominio de autorización web | Nome de domínio de autorização web | Доменное имя авторизации веб-страниц | اسم نطاق تفويض الويب |
| 支付目录 | Payment Directory | 決済ディレクトリ | 결제 디렉토리 | Répertoire de paiement | Directorio de pago | Diretório de pagamento | Каталог платежей | دليل الدفع |
| 商户订单号 | Merchant Order Number | 加盟店注文番号 | 가맹점 주문 번호 | Numéro de commande marchand | Número de pedido del comerciante | Número do pedido do comerciante | Номер заказа мерчанта | رقم طلب التاجر |
| 交易金额 | Transaction Amount | 取引金額 | 거래 금액 | Montant de la transaction | Monto de la transacción | Valor da transação | Сумма транзакции | مبلغ المعاملة |
| 交易类型 | Transaction Type | 取引タイプ | 거래 유형 | Type de transaction | Tipo de transacción | Tipo de transação | Тип транзакции | نوع المعاملة |
| 货币类型 | Currency Type | 通貨タイプ | 통화 유형 | Type de devise | Tipo de moneda | Tipo de moeda | Тип валюты | نوع العملة |
| 商户类别代码 | Merchant Category Code | 加盟店カテゴリーコード | 가맹점 카테고리 코드 | Code de catégorie marchand | Código de categoría de comerciante | Código de categoria do comerciante | Код категории мерчанта | رمز فئة التاجر |
| 支付权限 | Payment Authorization | 決済権限 | 결제 권한 | Autorisation de paiement | Autorización de pago | Autorização de pagamento | Разрешение на оплату | إذن الدفع |
| 开发参数配置 | Configure Development Parameters | 開発パラメータ設定 | 개발 매개변수 구성 | Configuration des paramètres de développement | Configuración de parámetros de desarrollo | Configuração de parâmetros de desenvolvimento | Настройка параметров разработки | تهيئة معاملات التطوير |
| 系统错误 | System Error | システムエラー | 시스템 오류 | Erreur système | Error del sistema | Erro do sistema | Системная ошибка | خطأ في النظام |
| 接入模式选择 | Select Integration Mode | 導入モード選択 | 연동 방식 선택 | Sélection du mode d’intégration | Selección del modo de integración | Seleção do modo de integração | Выбор режима интеграции | اختيار وضع التكامل |

---

## 流程术语

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 上线 | Go Live / Launch | 本番リリース | 오픈 / 상용 배포 | Mise en production | Puesta en producción | Colocar em produção | Запуск в эксплуатацию | الإطلاق |
| 进件 | Onboarding (Registration) | 登録（オンボーディング） | 등록(온보딩) | Onboarding / enregistrement | Incorporación / registro | Integração / registro | Регистрация / онбординг | التأهيل / التسجيل |
| 原单重入 | Idempotent Re-submission | 冪等な再送信 | 멱등 재제출 | Re-soumission idempotente | Reenvío idempotente | Reenvio idempotente | Идемпотентная повторная отправка | إعادة تقديم الطلب الأصلي بشكل لا يتأثر بالتكرار |
| 订单闭环 | Order Lifecycle Closure | 注文ライフサイクル完結 | 주문 생명주기 마감 | Clôture du cycle de commande | Cierre del ciclo del pedido | Fechamento do ciclo do pedido | Закрытие жизненного цикла заказа | إغلاق دورة حياة الطلب |
| 轮询 | Polling | ポーリング | 폴링 | Interrogation périodique | Sondeo | Sondagem | Опрос | الاستطلاع الدوري |
| 退避重试 | Exponential Backoff Retry | 指数バックオフリトライ | 지수 백오프 재시도 | Reprise avec backoff exponentiel | Reintento con backoff exponencial | Repetição com backoff exponencial | Повторная попытка с экспоненциальной задержкой | إعادة المحاولة بتراجع أسي |
| 串单 | Cross-order Mix-up | 注文混同 | 주문 혼선 | Mélange de commandes | Mezcla de pedidos | Mistura de pedidos | Смешение заказов | اختلاط الطلبات |
| 入驻申请 | Onboarding Application | 登録申請 | 등록 신청 | Demande d’intégration | Solicitud de incorporación | Solicitação de integração | Заявка на регистрацию | طلب الانضمام |
| 子商户入驻状态 | Sub-merchant Onboarding Status | サブマーチャント登録状態 | 하위 가맹점 등록 상태 | Statut d’intégration du sous-marchand | Estado de incorporación del sub-comerciante | Status de integração do sub-comerciante | Статус регистрации субмерчанта | حالة تأهيل التاجر الفرعي |
| 审核结果 | Review Result | 審査結果 | 심사 결과 | Résultat d'examen | Resultado de revisión | Resultado de revisão | Результат проверки | نتيجة المراجعة |
| 全额退款 | Fully Refunded | 全額返金 | 전액 환불 | Remboursement intégral | Reembolso completo | Reembolso total | Полный возврат | استرداد كامل المبلغ |
| 对账 | Reconciliation | 照合 | 대사 | Réconciliation | Conciliación | Reconciliação | Сверка | المطابقة |
| 交易账单 | Transaction Statement | 取引明細書 | 거래 명세서 | Relevé de transaction | Estado de transacción | Extrato de transação | Выписка по транзакциям | كشف المعاملات |
| 退款账单 | Refund Statement | 返金明細書 | 환불 명세서 | Relevé de remboursement | Estado de reembolso | Extrato de reembolso | Выписка по возвратам | كشف الاسترداد |
| 分账账单 | funds-distribution statement | 資金分配明細書 | 자금 분배 명세서 | Relevé de distribution des fonds | Estado de distribución de fondos | Extrato de distribuição de fundos | Выписка по распределению средств | كشف توزيع الأموال |
| 查询单笔退款 | Query One Refund | 1件の返金照会 | 단건 환불 조회 | Requête d'un remboursement | Consulta de un reembolso | Consulta de um reembolso | Запрос одного возврата | استعلام استرداد واحد |
| 查询所有退款 | Query All Refunds | すべての返金照会 | 모든 환불 조회 | Requête de tous les remboursements | Consulta de todos los reembolsos | Consulta de todos os reembolsos | Запрос всех возвратов | استعلام جميع المستردات |
| 下载对账单 | Download Reconciliation Statement | 照合明細書ダウンロード | 대사 명세서 다운로드 | Télécharger le relevé de rapprochement | Descargar estado de conciliación | Baixar extrato de reconciliação | Скачать выписку сверки | تنزيل كشف المطابقة |
| 下载平台证书 | Download Platform Certificate | プラットフォーム証明書ダウンロード | 플랫폼 인증서 다운로드 | Télécharger le certificat de plateforme | Descargar certificado de plataforma | Baixar certificado de plataforma | Скачать сертификат платформы | تنزيل شهادة المنصة |
| 申请退款 | Submit Refund | 返金申請 | 환불 신청 | Demander un remboursement | Solicitar reembolso | Solicitar reembolso | Подать заявку на возврат | تقديم طلب استرداد |
| 支付结果通知 | Payment Result Notification | 決済結果通知 | 결제 결과 알림 | Notification de résultat de paiement | Notificación de resultado de pago | Notificação de resultado de pagamento | Уведомление о результате платежа | إشعار نتيجة الدفع |
| 退款通知 | Refund Notification | 返金通知 | 환불 알림 | Notification de remboursement | Notificación de reembolso | Notificação de reembolso | Уведомление о возврате | إشعار الاسترداد |
| 撤销订单 | Cancel Order | 注文取消 | 주문 취소 | Annuler la commande | Cancelar pedido | Cancelar pedido | Отменить заказ | إلغاء الطلب |
| 支付单信息 | Payment Slip Information | 決済票情報 | 결제 전표 정보 | Informations sur le bon de paiement | Información del comprobante de pago | Informações do comprovante de pagamento | Информация платёжного документа | معلومات إيصال الدفع |
| 进件成功 | Onboarding Successful | 登録成功 | 등록 성공 | Intégration réussie | Incorporación exitosa | Integração bem-sucedida | Регистрация прошла успешно | نجاح التأهيل |
| 进件失败 | Onboarding Failed | 登録失敗 | 등록 실패 | Intégration échouée | Incorporación fallida | Falha na integração | Регистрация не удалась | فشل التأهيل |
| 未完成入驻 | Incomplete Application | 未完了の登録申請 | 미완료 등록 신청 | Demande incomplète | Solicitud incompleta | Solicitação incompleta | Незавершённая заявка | طلب غير مكتمل |

---

## 报错相关

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 余额不足 | Insufficient Balance | 残高不足 | 잔액 부족 | Solde insuffisant | Saldo insuficiente | Saldo insuficiente | Недостаточный баланс | رصيد غير كافٍ |
| 受理关系不存在 | Payment Acceptance Relationship Not Found | 決済受理関係が存在しない | 결제 수락 관계가 존재하지 않음 | Relation d'acceptation des paiements introuvable | Relación de aceptación de pagos no encontrada | Relação de aceitação de pagamentos não encontrada | Отношение приёма платежей не найдено | علاقة قبول المدفوعات غير موجودة |
| 参数非法 | Invalid Parameter | パラメータ不正 | 파라미터 오류 | Paramètre invalide | Parámetro inválido | Parâmetro inválido | Недопустимый параметр | معامل غير صالح |
| 频率限制 | Rate Limited | レート制限 | 빈도 제한 | Limitation de débit | Límite de velocidad | Limitação de taxa | Ограничение частоты запросов | تحديد معدل الطلبات |
| 订单不存在 | Order Not Found | 注文が存在しない | 주문 미존재 | Commande introuvable | Pedido no encontrado | Pedido não encontrado | Заказ не найден | الطلب غير موجود |
| 权限未开通 | Permission Not Enabled | 権限が有効化されていない | 권한이 활성화되지 않음 | Permission non activée | Permiso no habilitado | Permissão não habilitada | Разрешение не включено | الإذن غير مفعّل |
| 异常返回 | Error Response | 異常返却 | 오류 응답 | Réponse d'erreur | Respuesta de error | Resposta de erro | Ответ об ошибке | استجابة الخطأ |

---

## 子商户管理

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 进件子商户 | Onboard Sub-merchant | サブマーチャント登録 | 하위 가맹점 등록 | Intégrer un sous-marchand | Incorporar sub-comerciante | Integrar sub-comerciante | Зарегистрировать субмерчанта | تأهيل تاجر فرعي |
| 修改子商户 | Modify Sub-merchant | サブマーチャント修正 | 하위 가맹점 수정 | Modifier le sous-marchand | Modificar sub-comerciante | Modificar sub-comerciante | Изменить субмерчанта | تعديل التاجر الفرعي |
| 查询子商户 | Query Sub-merchant | サブマーチャント照会 | 하위 가맹점 조회 | Interroger le sous-marchand | Consultar sub-comerciante | Consultar sub-comerciante | Запрос субмерчанта | استعلام التاجر الفرعي |
| 子商户状态 | Sub-merchant Status | サブマーチャント状態 | 하위 가맹점 상태 | Statut du sous-marchand | Estado del sub-comerciante | Status do sub-comerciante | Статус субмерчанта | حالة التاجر الفرعي |
| 申请单号 | Application ID | 申請番号 | 신청 번호 | ID de demande | ID de solicitud | ID de solicitação | ID заявки | معرف الطلب |
| 驳回原因 | Rejection Reason | 却下理由 | 거절 이유 | Motif de rejet | Motivo de rechazo | Motivo de rejeição | Причина отклонения | سبب الرفض |
| 被驳回 | Rejected | 却下された | 거절됨 | Rejeté | Rechazado | Rejeitado | Отклонено | تم الرفض |
| 申请资料 | Application Information | 申請書類 | 신청 자료 | Documents de demande | Documentos de solicitud | Documentos de solicitação | Документы заявки | وثائق الطلب |
| 超级管理员账号 | Super Administrator Account | スーパー管理者アカウント | 슈퍼 관리자 계정 | Compte super administrateur | Cuenta de super administrador | Conta de super administrador | Учётная запись суперадминистратора | حساب المشرف العام |
| 经营网址商业页面 | Website Business Page | ビジネスWebページ | 웹사이트 비즈니스 페이지 | Page commerciale du site Web | Página de negocio del sitio web | Página de negócios do site | Коммерческая страница сайта | صفحة الأعمال على الموقع |
| 经营网址首页 | Website Homepage | Webサイトホームページ | 웹사이트 홈페이지 | Page d'accueil du site | Página principal del sitio web | Página inicial do site | Главная страница сайта | الصفحة الرئيسية للموقع |
| 实体个人 | Natural Person | 自然人 | 자연인 | Personne physique | Persona física | Pessoa física | Физическое лицо | فرد طبيعي |
| 电商KYC资料 | E-commerce KYC Documents | EC向けKYC書類 | 전자상거래 KYC 서류 | Documents KYC e-commerce | Documentos KYC de e-commerce | Documentos KYC de e-commerce | Документы KYC для е-коммерции | وثائق KYC التجارة الإلكترونية |
| KYC资料 | KYC Documents | KYC書類 | KYC 서류 | Documents KYC | Documentos KYC | Documentos KYC | Документы KYC | وثائق KYC |
| 短信验证码 | SMS Verification Code | SMS認証コード | SMS 인증 코드 | Code de vérification SMS | Código de verificación SMS | Código de verificação SMS | Код подтверждения SMS | رمز التحقق عبر الرسائل القصيرة |

---

## 签名与加解密

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 公钥 | Public Key | 公開鍵 | 공개키 | Clé publique | Clave pública | Chave pública | Открытый ключ | المفتاح العام |
| 私钥 | Private Key | 秘密鍵 | 개인키 | Clé privée | Clave privada | Chave privada | Закрытый ключ | المفتاح الخاص |
| RSA公钥 | RSA Public Key | RSA公開鍵 | RSA 공개키 | Clé publique RSA | Clave pública RSA | Chave pública RSA | Открытый ключ RSA | مفتاح RSA العام |
| RSA公钥加密 | RSA Public Key Encryption | RSA公開鍵暗号化 | RSA 공개키 암호화 | Chiffrement par clé publique RSA | Cifrado con clave pública RSA | Criptografia com chave pública RSA | Шифрование открытым ключом RSA | تشفير RSA بالمفتاح العام |
| 敏感信息字段 | Sensitive Information Fields | 機密情報フィールド | 민감 정보 필드 | Champs d'informations sensibles | Campos de información sensible | Campos de informações sensíveis | Поля конфиденциальной информации | حقول المعلومات الحساسة |
| 加密示例 | Encryption Example | 暗号化例 | 암호화 예시 | Exemple de chiffrement | Ejemplo de cifrado | Exemplo de criptografia | Пример шифрования | مثال التشفير |
| 认证加密算法 | Authenticated Encryption Algorithm | 認証暗号化アルゴリズム | 인증 암호화 알고리즘 | Algorithme de chiffrement authentifié | Algoritmo de cifrado autenticado | Algoritmo de criptografia autenticado | Алгоритм аутентифицированного шифрования | خوارزمية التشفير المصادق عليه |
| 加密报文 | Encrypted Message | 暗号化メッセージ | 암호화 메시지 | Message chiffré | Mensaje cifrado | Mensagem criptografada | Зашифрованное сообщение | الرسالة المشفرة |
| 加密报文格式 | Format of Encrypted Messages | 暗号化メッセージ形式 | 암호화 메시지 형식 | Format des messages chiffrés | Formato de mensajes cifrados | Formato de mensagens criptografadas | Формат зашифрованных сообщений | تنسيق الرسائل المشفرة |
| 请求签名 | Request Signature | リクエスト署名 | 요청 서명 | Signature de requête | Firma de solicitud | Assinatura de requisição | Подпись запроса | توقيع الطلب |
| 应答签名 | Response Signature | レスポンス署名 | 응답 서명 | Signature de réponse | Firma de respuesta | Assinatura de resposta | Подпись ответа | توقيع الاستجابة |
| 验签名串 | Signature Verification String | 署名検証文字列 | 서명 검증 문자열 | Chaîne de vérification de signature | Cadena de verificación de firma | String de verificação de assinatura | Строка проверки подписи | سلسلة التحقق من التوقيع |
| 获取应答签名 | Obtaining the Response Signature | 応答署名取得 | 응답 서명 획득 | Obtenir la signature de réponse | Obtener la firma de respuesta | Obter assinatura de resposta | Получение подписи ответа | الحصول على توقيع الاستجابة |
| 验证签名 | Verifying Signature | 署名検証 | 서명 검증 | Vérification de signature | Verificar firma | Verificar assinatura | Верификация подписи | التحقق من التوقيع |
| 签名信息 | Signature Information | 署名情報 | 서명 정보 | Informations de signature | Información de firma | Informações de assinatura | Информация о подписи | معلومات التوقيع |
| 认证类型 | Authentication Type | 認証タイプ | 인증 유형 | Type d'authentification | Tipo de autenticación | Tipo de autenticação | Тип аутентификации | نوع المصادقة |
| 加密方法 | Encryption Method | 暗号化方法 | 암호화 방법 | Méthode de chiffrement | Método de cifrado | Método de criptografia | Метод шифрования | طريقة التشفير |
| 通知签名 | Notification Signature | 通知署名 | 알림 서명 | Signature de notification | Firma de notificación | Assinatura de notificação | Подпись уведомления | توقيع الإشعار |
| 回调通知签名 | Callback Notification Signature | コールバック通知署名 | 콜백 알림 서명 | Signature de notification de callback | Firma de notificación de callback | Assinatura de notificação de callback | Подпись уведомления об обратном вызове | توقيع إشعار رد الاتصال |

---

## 请求与响应

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 应答 | Response | 応答 | 응답 | Réponse | Respuesta | Resposta | Ответ | الاستجابة |
| 应答主体 | Response Body | 応答本文 | 응답 본문 | Corps de réponse | Cuerpo de respuesta | Corpo de resposta | Тело ответа | نص الاستجابة |
| 应答时间戳 | Response Timestamp | 応答タイムスタンプ | 응답 타임스탬프 | Horodatage de réponse | Marca de tiempo de respuesta | Timestamp de resposta | Временная метка ответа | طابع زمن الاستجابة |
| 应答随机串 | Response Random String | 応答ランダム文字列 | 응답 랜덤 문자열 | Chaîne aléatoire de réponse | Cadena aleatoria de respuesta | String aleatório de resposta | Случайная строка ответа | السلسلة العشوائية للاستجابة |
| 应答报文主体 | Response Message Body | 応答メッセージ本文 | 응답 메시지 본문 | Corps du message de réponse | Cuerpo del mensaje de respuesta | Corpo da mensagem de resposta | Тело сообщения ответа | نص رسالة الاستجابة |
| 请求时间戳 | Request Timestamp | リクエストタイムスタンプ | 요청 타임스탬프 | Horodatage de requête | Marca de tiempo de solicitud | Timestamp de requisição | Временная метка запроса | طابع زمن الطلب |
| 请求随机串 | Request Random String | リクエストランダム文字列 | 요청 랜덤 문자열 | Chaîne aléatoire de requête | Cadena aleatoria de solicitud | String aleatório de requisição | Случайная строка запроса | السلسلة العشوائية للطلب |
| 请求报文主体 | Request Body | リクエスト本文 | 요청 본문 | Corps de la requête | Cuerpo de la solicitud | Corpo da requisição | Тело запроса | نص الطلب |
| 请求示例 | Request Example | リクエスト例 | 요청 예시 | Exemple de requête | Ejemplo de solicitud | Exemplo de requisição | Пример запроса | مثال الطلب |
| 返回示例 | Response Example | 返却例 | 응답 예시 | Exemple de réponse | Ejemplo de respuesta | Exemplo de resposta | Пример ответа | مثال الاستجابة |
| 返回状态码 | Returned Status Code | 返却ステータスコード | 반환 상태 코드 | Code de statut retourné | Código de estado devuelto | Código de status retornado | Возвращаемый код состояния | رمز الحالة المُرجَع |
| 返回信息 | Returned Message | 返却メッセージ | 반환 메시지 | Message retourné | Mensaje devuelto | Mensagem retornada | Возвращаемое сообщение | الرسالة المُرجَعة |
| 路径参数 | Path Parameter | パスパラメータ | 경로 매개변수 | Paramètre de chemin | Parámetro de ruta | Parâmetro de caminho | Параметр пути | معامل المسار |
| 附加数据 | Additional Data | 追加データ | 추가 데이터 | Données supplémentaires | Datos adicionales | Dados adicionais | Дополнительные данные | البيانات الإضافية |
| 数据密文 | Ciphertext | 暗号文 | 암호문 | Texte chiffré | Texto cifrado | Texto cifrado | Зашифрованный текст | النص المشفر |
| HTTP头 | HTTP Header | HTTPヘッダー | HTTP 헤더 | En-tête HTTP | Encabezado HTTP | Cabeçalho HTTP | HTTP-заголовок | رأس HTTP |
| HTTP Authorization头 | HTTP Authorization Header | HTTP Authorizationヘッダー | HTTP 인증 헤더 | En-tête d'autorisation HTTP | Encabezado de autorización HTTP | Cabeçalho de autorização HTTP | Заголовок авторизации HTTP | رأس تفويض HTTP |
| HTTP状态码 | HTTP Status Code | HTTPステータスコード | HTTP 상태 코드 | Code de statut HTTP | Código de estado HTTP | Código de status HTTP | HTTP-код состояния | رمز حالة HTTP |
| 时间戳 | Timestamp | タイムスタンプ | 타임스탬프 | Horodatage | Marca de tiempo | Timestamp | Временная метка | الطابع الزمني |
| 随机字符串 | Random String | ランダム文字列 | 랜덤 문자열 | Chaîne aléatoire | Cadena aleatoria | String aleatório | Случайная строка | سلسلة عشوائية |

---

## 通知与回调

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 回调 | Callback | コールバック | 콜백 | Callback | Callback | Callback | Обратный вызов | رد الاتصال |
| 回调接口 | Callback API | コールバックAPI | 콜백 API | API de callback | API de callback | API de callback | API обратного вызова | واجهة رد الاتصال |
| 回调示例 | Callback Example | コールバック例 | 콜백 예시 | Exemple de callback | Ejemplo de callback | Exemplo de callback | Пример обратного вызова | مثال رد الاتصال |
| 通知规则 | Notification Rules | 通知ルール | 알림 규칙 | Règles de notification | Reglas de notificación | Regras de notificação | Правила уведомлений | قواعد الإشعارات |
| 通知报文 | Notification Message | 通知メッセージ | 알림 메시지 | Message de notification | Mensaje de notificación | Mensagem de notificação | Сообщение уведомления | رسالة الإشعار |
| 通知应答 | Notification Response | 通知応答 | 알림 응답 | Réponse de notification | Respuesta de notificación | Resposta de notificação | Ответ на уведомление | استجابة الإشعار |
| 原始回调类型 | Original Callback Type | 元のコールバックタイプ | 원래 콜백 유형 | Type de callback original | Tipo de callback original | Tipo de callback original | Исходный тип обратного вызова | نوع رد الاتصال الأصلي |

---

## 分账相关

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 分账产品 | funds-distribution product | 資金分配プロダクト | 자금 분배 상품 | Produit de distribution des fonds | Producto de distribución de fondos | Produto de distribuição de fundos | Продукт распределения средств | منتج توزيع الأموال |
| 分账场景 | funds-distribution scenario | 資金分配シナリオ | 자금 분배 시나리오 | Scénario de distribution des fonds | Escenario de distribución de fondos | Cenário de distribuição de fundos | Сценарий распределения средств | سيناريو توزيع الأموال |
| 分账权限 | funds-distribution permission | 資金分配権限 | 자금 분배 권한 | Autorisation de distribution des fonds | Permiso de distribución de fondos | Permissão de distribuição de fundos | Разрешение на распределение средств | إذن توزيع الأموال |
| 分账接口 | funds-distribution API | 資金分配API | 자금 분배 API | API de distribution des fonds | API de distribución de fondos | API de distribuição de fundos | API распределения средств | واجهة توزيع الأموال |
| 分账业务 | funds-distribution business | 資金分配業務 | 자금 분배 업무 | Activité de distribution des fonds | Negocio de distribución de fondos | Negócio de distribuição de fundos | Бизнес по распределению средств | أعمال توزيع الأموال |
| 分账功能 | funds-distribution function | 資金分配機能 | 자금 분배 기능 | Fonction de distribution des fonds | Función de distribución de fondos | Função de distribuição de fundos | Функция распределения средств | وظيفة توزيع الأموال |
| 分账指令 | funds-distribution command | 資金分配指示 | 자금 분배 지시 | Commande de distribution des fonds | Comando de distribución de fondos | Comando de distribuição de fundos | Команда распределения средств | أمر توزيع الأموال |
| 分账时间 | funds-distribution timing | 資金分配タイミング | 자금 분배 시점 | Moment de distribution des fonds | Tiempo de distribución de fondos | Momento de distribuição de fundos | Время распределения средств | توقيت توزيع الأموال |
| 分销方 | Distributor | 販売代理店 | 판매 대리점 | Distributeur | Distribuidor | Distribuidor | Дистрибьютор | الموزع |
| 分销佣金/抽成 | Distribution Commission | 販売手数料 | 판매 수수료 | Commission de distribution | Comisión de distribución | Comissão de distribuição | Комиссия дистрибьютора | عمولة التوزيع |
| 接入分账 | Integrate funds-distribution | 資金分配を導入 | 자금 분배 연동 | Intégrer la distribution des fonds | Integrar la distribución de fondos | Integrar a distribuição de fundos | Подключить распределение средств | دمج خدمة توزيع الأموال |
| 分账功能申请承诺函 | Commitment Letter for Funds-distribution Application | 資金分配機能申請承諾書 | 자금 분배 기능 신청 확약서 | Lettre d’engagement pour la demande de distribution des fonds | Carta de compromiso para la solicitud de distribución de fondos | Carta de compromisso para solicitação de distribuição de fundos | Письмо-обязательство для заявки на распределение средств | خطاب الالتزام بطلب وظيفة توزيع الأموال |
| 接收方类型 | Receiver Type | 受取人タイプ | 수신자 유형 | Type de bénéficiaire | Tipo de receptor | Tipo de receptor | Тип получателя | نوع المستلم |
| 接收方商户的主营业务范围 | Major Service Scope of Receiver | 受取人の主要業務範囲 | 수신자 주요 업무 범위 | Portée principale des services du bénéficiaire | Alcance principal del servicio del receptor | Escopo principal do serviço do receptor | Основная область деятельности получателя | نطاق الخدمة الرئيسي للمستلم |
| 添加接收方 | Add Receiver | 受取人追加 | 수신자 추가 | Ajouter un bénéficiaire | Añadir receptor | Adicionar receptor | Добавить получателя | إضافة مستلم |
| 商户添加分账接收方 | Merchant-added funds-distribution receivers | 加盟店による資金分配受取人追加 | 가맹점의 자금 분배 수신자 추가 | Marchands ajoutant des bénéficiaires | Comerciantes añadiendo receptores | Comerciantes adicionando receptores | Добавление мерчантами получателей распределения средств | إضافة مستلمي توزيع الأموال من قِبل التجار |
| 境内分账对象 | domestic funds-distribution receiver | 国内資金分配対象 | 국내 자금 분배 대상 | Bénéficiaire de distribution domestique des fonds | Receptor de distribución doméstica de fondos | Recebedor de distribuição doméstica de fundos | Получатель внутреннего распределения средств | مستلم التوزيع المحلي للأموال |
| 跨境收单机构服务商 | Cross-border Acquiring Service Provider | クロスボーダーアクワイアリングサービスプロバイダー | 크로스보더 매입 서비스 제공자 | Prestataire de services d’acquisition transfrontalière | Proveedor de servicios adquirentes transfronterizos | Provedor de serviços de adquirência transfronteiriça | Трансграничный поставщик эквайринговых услуг | مزود خدمة قبول المدفوعات عبر الحدود |
| 合作机构商 | Partner Institution | パートナー機関 | 파트너 기관 | Institution partenaire | Institución asociada | Instituição parceira | Партнёрская организация | المؤسسة الشريكة |
| 单笔订单 | Single Transaction | 単一取引 | 단일 거래 | Transaction unique | Transacción única | Transação única | Единичная транзакция | معاملة واحدة |
| 多次分账 | Multiple funds-distribution operations | 複数回の資金分配 | 여러 차례 자금 분배 | Distributions multiples | Distribuciones múltiples | Distribuições múltiplas | Многократное распределение | توزيعات متعددة |
| 可分账的最大比例 | Maximum Funds-distribution Proportion | 最大資金分配比率 | 최대 자금 분배 비율 | Proportion maximale de distribution | Proporción máxima de distribución | Proporção máxima de distribuição | Максимальная доля для распределения | الحد الأقصى لنسبة التوزيع |
| 资金分账服务 | funds-distribution service | 資金分配サービス | 자금 분배 서비스 | Service de distribution des fonds | Servicio de distribución de fondos | Serviço de distribuição de fundos | Сервис распределения средств | خدمة توزيع الأموال |
| 请求分账API | Funds-distribution Request API | 資金分配リクエストAPI | 자금 분배 요청 API | API de demande de distribution des fonds | API de solicitud de distribución de fondos | API de solicitação de distribuição de fundos | API запроса распределения средств | واجهة طلب توزيع الأموال |
| 查询分账接收方添加结果API | Funds-distribution Receiver Addition Result Query API | 資金分配受取人追加結果照会API | 자금 분배 수신자 추가 결과 조회 API | API de résultat d'ajout de bénéficiaire | API de resultado de adición de receptor | API de resultado de adição de receptor | API запроса результата добавления получателя распределения средств | واجهة استعلام نتيجة إضافة مستلم توزيع الأموال |

---

## 委托代扣（扩展）

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 免密代扣 | Password-free Auto-Debit | パスワードレス自動引落し | 비밀번호 없는 자동 차감 | Prélèvement automatique sans mot de passe | Débito automático sin contraseña | Débito automático sem senha | Беспарольное автоматическое списание | الخصم التلقائي بدون كلمة مرور |
| 自动扣费 | Automatic Deduction | 自動引落し | 자동 차감 | Prélèvement automatique | Deducción automática | Dedução automática | Автоматическое списание | الخصم التلقائي |
| 周期扣费 | Periodic Deduction | 定期引落し | 정기 차감 | Prélèvement périodique | Deducción periódica | Dedução periódica | Периодическое списание | الخصم الدوري |
| 免密扣款场景 | Password-free Deduction Scenario | パスワードレス引落しシナリオ | 비밀번호 없는 차감 시나리오 | Scénario de prélèvement sans mot de passe | Escenario de deducción sin contraseña | Cenário de dedução sem senha | Сценарий беспарольного списания | سيناريو الخصم بدون كلمة مرور |
| 验密扣款场景 | Password Verification Deduction Scenario | パスワード確認引落しシナリオ | 비밀번호 확인 차감 시나리오 | Scénario de prélèvement avec vérification du mot de passe | Escenario de deducción con verificación de contraseña | Cenário de dedução com verificação de senha | Сценарий списания с проверкой пароля | سيناريو الخصم بالتحقق من كلمة المرور |
| 平台服务费 | Platform Service Fee | プラットフォームサービス料 | 플랫폼 서비스 수수료 | Frais de service de plateforme | Tarifa de servicio de plataforma | Taxa de serviço da plataforma | Комиссия платформы | رسوم خدمة المنصة |
| 预签约单号 | Pre-signing Order ID | 事前契約注文番号 | 사전 계약 주문 번호 | ID de commande de pré-signature du contrat | ID de pedido de precontratación | ID do pedido de pré-contratação | ID заказа предварительного заключения договора | معرف طلب التعاقد المسبق |
| 场景特点 | Scenario Characteristics | シナリオ特徴 | 시나리오 특성 | Caractéristiques du scénario | Características del escenario | Características do cenário | Характеристики сценария | خصائص السيناريو |

---

## 支付产品（扩展）

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 小程序调起支付 | Initiate Mini Program Payment | ミニプログラム決済を開始 | 미니 프로그램 결제 시작 | Lancer le paiement Mini Programme | Iniciar pago Mini Programa | Iniciar pagamento Mini Programa | Инициировать платёж в мини-программе | بدء الدفع في البرنامج المصغر |
| APP调起支付 | Initiate APP Payment | アプリ決済を開始 | 앱 결제 시작 | Lancer le paiement APP | Iniciar pago APP | Iniciar pagamento APP | Инициировать платёж в приложении | بدء الدفع في التطبيق |
| 微信内H5调起支付 | Initiate H5 Payment in WeChat | WeChat内H5決済を開始 | WeChat 내 H5 결제 시작 | Lancer le paiement H5 dans WeChat | Iniciar pago H5 en WeChat | Iniciar pagamento H5 no WeChat | Инициировать H5-платёж внутри WeChat | بدء دفع H5 داخل WeChat |
| 微信支付收银台 | WeChat Pay Checkout | WeChat Payチェックアウト | WeChat Pay 결제창 | Checkout WeChat Pay | Checkout WeChat Pay | Checkout WeChat Pay | Страница оплаты WeChat Pay | صفحة الدفع WeChat Pay |
| paySign生成规则 | paySign Generation Rules | paySign生成ルール | paySign 생성 규칙 | Règles de génération paySign | Reglas de generación paySign | Regras de geração paySign | Правила генерации paySign | قواعد توليد paySign |
| 订单详情扩展字符串 | Extension String for Order Details | 注文詳細拡張文字列 | 주문 상세 확장 문자열 | Chaîne d'extension des détails de commande | Cadena de extensión de detalles del pedido | String de extensão de detalhes do pedido | Строка расширения деталей заказа | سلسلة توسعة تفاصيل الطلب |
| H5商城网站 | H5 Mall Website | H5ショッピングモールサイト | H5 쇼핑몰 웹사이트 | Site e-commerce H5 | Sitio de tienda en línea H5 | Site de loja online H5 | Сайт торгового центра H5 | موقع مركز التسوق H5 |
| PC网站 | PC Website | PCウェブサイト | PC 웹사이트 | Site web PC | Sitio web PC | Site web PC | Сайт для ПК | موقع الويب للحاسوب |
| 线上场景 | Online Scenario | オンラインシナリオ | 온라인 시나리오 | Scénario en ligne | Escenario en línea | Cenário online | Онлайн-сценарий | سيناريو على الإنترنت |
| 线下场景 | Offline Scenario | オフラインシナリオ | 오프라인 시나리오 | Scénario hors ligne | Escenario fuera de línea | Cenário offline | Офлайн-сценарий | سيناريو خارج الإنترنت |
| 线下商店 | Offline Store | 実店舗 | 오프라인 매장 | Magasin hors ligne | Tienda física | Loja física | Офлайн-магазин | متجر فيزيائي |
| 二维码图片 | QR Code Image | QRコード画像 | QR 코드 이미지 | Image de code QR | Imagen de código QR | Imagem de código QR | Изображение QR-кода | صورة رمز QR |
| 支付密码 | Payment Password | 決済パスワード | 결제 비밀번호 | Mot de passe de paiement | Contraseña de pago | Senha de pagamento | Платёжный пароль | كلمة مرور الدفع |
| 微信浏览器 | WeChat Browser | WeChatブラウザ | WeChat 브라우저 | Navigateur WeChat | Navegador WeChat | Navegador WeChat | Браузер WeChat | متصفح WeChat |
| 公众号 | Official Account | 公式アカウント | 공식 계정 | Compte officiel | Cuenta oficial | Conta oficial | Официальный аккаунт | الحساب الرسمي |
| 小程序 | Mini Program | ミニプログラム | 미니 프로그램 | Mini Programme | Mini Programa | Mini Programa | Мини-программа | البرنامج المصغر |
| 公众号支付 | JSAPI Payment (Official Account) | 公式アカウント決済 | 공식 계정 결제 | Paiement JSAPI via compte officiel | Pago JSAPI mediante cuenta oficial | Pagamento JSAPI via conta oficial | Платёж JSAPI через официальный аккаунт | دفع JSAPI عبر الحساب الرسمي |
| 微信开放平台 | WeChat Open Platform | WeChatオープンプラットフォーム | WeChat 오픈 플랫폼 | Plateforme ouverte WeChat | Plataforma abierta WeChat | Plataforma aberta WeChat | Открытая платформа WeChat | منصة WeChat المفتوحة |
| 应用包名 | Application Package Name | アプリパッケージ名 | 앱 패키지 이름 | Nom du package d'application | Nombre de paquete de aplicación | Nome do pacote do aplicativo | Имя пакета приложения | اسم حزمة التطبيق |
| 应用签名 | Application Signature | アプリ署名 | 앱 서명 | Signature d'application | Firma de aplicación | Assinatura do aplicativo | Подпись приложения | توقيع التطبيق |
| 开发配置 | Development Configuration | 開発設定 | 개발 설정 | Configuration de développement | Configuración de desarrollo | Configuração de desenvolvimento | Конфигурация разработки | تكوين التطوير |
| 网页应用 | Web Application | Webアプリ | 웹 앱 | Application web | Aplicación web | Aplicação web | Веб-приложение | تطبيق الويب |

---

## 报关相关

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 报关信息 | Customs Declaration Information | 通関申告情報 | 세관 신고 정보 | Informations de déclaration douanière | Información de declaración aduanera | Informações de declaração aduaneira | Информация таможенной декларации | معلومات التصريح الجمركي |
| 报关信息修改接口 | API for Modifying Customs Declaration | 通関申告情報修正API | 세관 신고 수정 API | API de modification de déclaration douanière | API de modificación de declaración aduanera | API de modificação de declaração aduaneira | API изменения таможенной декларации | واجهة تعديل التصريح الجمركي |
| 订单附加信息提交接口 | API for Additional Order Info Submission | 注文追加情報提出API | 주문 추가 정보 제출 API | API de soumission d'informations supplémentaires | API de envío de información adicional | API de envio de informações adicionais | API отправки дополнительной информации о заказе | واجهة تقديم معلومات الطلب الإضافية |
| 订单附加信息查询接口 | API for Querying Additional Order Info | 注文追加情報照会API | 주문 추가 정보 조회 API | API de requête d'informations supplémentaires | API de consulta de información adicional | API de consulta de informações adicionais | API запроса дополнительной информации о заказе | واجهة استعلام معلومات الطلب الإضافية |
| 订单附加信息重推接口 | API for Re-sending Additional Order Info | 注文追加情報再送信API | 주문 추가 정보 재전송 API | API de réenvoi d’informations supplémentaires de commande | API de reenvío de información adicional del pedido | API de reenvio de informações adicionais do pedido | API повторной отправки дополнительной информации о заказе | واجهة إعادة إرسال معلومات الطلب الإضافية |
| 自助清关 | Self-service Customs Clearance | 自助通関 | 셀프 통관 | Dédouanement en libre-service | Despacho aduanero en autoservicio | Desembaraço aduaneiro self-service | Самостоятельное таможенное оформление | التخليص الجمركي ذاتي الخدمة |
| 电子口岸 | E-port | 電子税関ポータル | 전자 세관 포털 | Portail douanier électronique | Portal aduanero electrónico | Portal aduaneiro eletrônico | Электронный таможенный портал | بوابة الجمارك الإلكترونية |
| 境内海关 | Domestic Customs | 国内税関 | 국내 세관 | Douanes domestiques | Aduana doméstica | Alfândega doméstica | Внутренняя таможня | الجمارك المحلية |
| 微信报关接口 | WeChat Customs Declaration API | WeChat通関申告API | WeChat 세관 신고 API | API de déclaration douanière WeChat | API de declaración aduanera WeChat | API de declaração aduaneira WeChat | API таможенной декларации WeChat | واجهة التصريح الجمركي WeChat |
| 身份信息校验 | User Identity Verification | 身元情報検証 | 신원 정보 검증 | Vérification d'identité utilisateur | Verificación de identidad del usuario | Verificação de identidade do usuário | Проверка личных данных пользователя | التحقق من هوية المستخدم |

---

## 商户与账户

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 收款账号 | Collection Account | 収金口座 | 수금 계좌 | Compte de collecte | Cuenta de cobro | Conta de cobrança | Счёт для получения средств | حساب التحصيل |
| 个人零钱账户 | Personal Balance Account | 個人残高口座 | 개인 잔액 계정 | Compte de solde personnel | Cuenta de saldo personal | Conta de saldo pessoal | Личный счёт с балансом | حساب الرصيد الشخصي |
| 零钱账户 | Balance Account | 残高口座 | 잔액 계정 | Compte de solde | Cuenta de saldo | Conta de saldo | Счёт с балансом | حساب الرصيد |
| 商户微信账户 | Merchant WeChat Account | 加盟店WeChatアカウント | 가맹점 WeChat 계정 | Compte WeChat marchand | Cuenta WeChat del comerciante | Conta WeChat do comerciante | Аккаунт WeChat мерчанта | حساب WeChat للتاجر |
| 商户境内微信账户 | Merchant Domestic WeChat Account | 加盟店国内WeChatアカウント | 가맹점 국내 WeChat 계정 | Compte WeChat domestique du marchand | Cuenta WeChat doméstica del comerciante | Conta WeChat doméstica do comerciante | Внутренний аккаунт WeChat мерчанта | حساب WeChat المحلي للتاجر |
| 境内微信支付商户号 | Domestic WeChat Pay Merchant ID | 国内WeChat Pay加盟店ID | 국내 WeChat Pay 가맹점 ID | ID marchand WeChat Pay domestique | ID de comerciante WeChat Pay doméstico | ID do comerciante WeChat Pay doméstico | ID внутреннего мерчанта WeChat Pay | معرف تاجر WeChat Pay المحلي |
| 微信支付商户号 | WeChat Pay Merchant ID | WeChat Pay加盟店ID | WeChat Pay 가맹점 ID | ID marchand WeChat Pay | ID de comerciante WeChat Pay | ID do comerciante WeChat Pay | ID мерчанта WeChat Pay | معرف تاجر WeChat Pay |
| 直连 | Direct Connection | 直接接続 | 직접 연결 | Connexion directe | Conexión directa | Conexão direta | Прямое подключение | الاتصال المباشر |
| 直连模式 | Direct Connection Mode | 直接接続モード | 직접 연결 모드 | Mode de connexion directe | Modo de conexión directa | Modo de conexão direta | Режим прямого подключения | وضع الاتصال المباشر |
| 直连商户 | Direct Merchant | 直接接続加盟店 | 직접 연결 가맹점 | Marchand direct | Comerciante directo | Comerciante direto | Прямой мерчант | التاجر المباشر |
| 普通服务商 | Standard Service Provider | 標準サービスプロバイダー | 표준 서비스 제공자 | Prestataire de services standard | Proveedor de servicios estándar | Provedor de serviços padrão | Стандартный поставщик услуг | مزود خدمة قياسي |
| 普通服务商模式 | Standard Service Provider Mode | 標準サービスプロバイダーモード | 표준 서비스 제공자 모드 | Mode prestataire de services standard | Modo de proveedor de servicios estándar | Modo de provedor de serviços padrão | Режим стандартного поставщика услуг | وضع مزود الخدمة القياسي |
| 企业或个人 | Enterprise or Individual | 企業または個人 | 기업 또는 개인 | Entreprise ou particulier | Empresa o particular | Empresa ou particular | Юридическое или физическое лицо | مؤسسة أو فرد |
| 境内企业主体 | Domestic Enterprise Entity | 国内企業主体 | 국내 기업 주체 | Entité d'entreprise domestique | Entidad empresarial doméstica | Entidade empresarial doméstica | Внутренний корпоративный субъект | كيان المؤسسة المحلية |
| 境内企业或个人 | Domestic Enterprise or Individual | 国内企業または個人 | 국내 기업 또는 개인 | Entreprise ou particulier domestique | Empresa o particular doméstico | Empresa ou particular doméstico | Внутреннее предприятие или физлицо | مؤسسة محلية أو فرد |
| 外部服务方 | External Service Provider | 外部サービスプロバイダー | 외부 서비스 제공자 | Prestataire externe | Proveedor externo | Provedor externo | Внешний поставщик услуг | مزود خدمة خارجي |
| 技术服务方 | Technical Service Provider | 技術サービスプロバイダー | 기술 서비스 제공자 | Prestataire de services techniques | Proveedor de servicios técnicos | Provedor de serviços técnicos | Провайдер технических услуг | مزود الخدمات التقنية |
| 技术服务 | Technical Service | 技術サービス | 기술 서비스 | Service technique | Servicio técnico | Serviço técnico | Технические услуги | الخدمة التقنية |
| 技术服务费 | Technical Service Fee | 技術サービス料 | 기술 서비스 수수료 | Frais de service technique | Tarifa de servicio técnico | Taxa de serviço técnico | Плата за технические услуги | رسوم الخدمة التقنية |
| 电商平台 | E-commerce Platform | ECプラットフォーム | 전자상거래 플랫폼 | Plateforme e-commerce | Plataforma de e-commerce | Plataforma de e-commerce | Платформа электронной торговли | منصة التجارة الإلكترونية |
| 微信跨境业务 | WeChat Cross-border Business | WeChatクロスボーダービジネス | WeChat 크로스보더 비즈니스 | Activité transfrontalière WeChat | Negocio transfronterizo WeChat | Negócio transfronteiriço WeChat | Трансграничный бизнес WeChat | أعمال WeChat عبر الحدود |
| 微信体系 | WeChat Ecosystem | WeChatエコシステム | WeChat 생태계 | Écosystème WeChat | Ecosistema WeChat | Ecossistema WeChat | Экосистема WeChat | منظومة WeChat |
| 微信商户平台 | WeChat Merchant Platform | WeChat加盟店プラットフォーム | WeChat 가맹점 플랫폼 | Plateforme marchand WeChat | Plataforma de comerciante WeChat | Plataforma do comerciante WeChat | Платформа мерчанта WeChat | منصة التاجر في WeChat |

---

## 资金与结算（扩展）

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 出境货款 | Outbound Payment for Goods | 商品代金の国外送金 | 상품대금 해외 송금 | Paiement sortant des marchandises | Pago saliente por mercancías | Pagamento de mercadorias ao exterior | Исходящий платёж за товары | مدفوعات السلع إلى الخارج |
| 出境指令 | Outbound Funds Transfer Instruction | 国外送金指示 | 해외 송금 지시 | Instruction de transfert de fonds sortant | Instrucción de transferencia de fondos al exterior | Instrução de transferência de fundos para o exterior | Поручение на перевод средств за рубеж | تعليمة تحويل الأموال إلى الخارج |
| 可分配/可退款资金 | Distributable/Refundable Funds | 分配/返金可能資金 | 분배/환불 가능 자금 | Fonds distribuables/remboursables | Fondos distribuibles/reembolsables | Fundos distribuíveis/reembolsáveis | Распределяемые/возвращаемые средства | الأموال القابلة للتوزيع/الاسترداد |
| 退货/退款 | Returns/Refunds | 返品/返金 | 반품/환불 | Retours/Remboursements | Devoluciones/Reembolsos | Devoluções/Reembolsos | Возвраты/возмещения | المرتجعات/المستردات |
| 资金境内分配 | domestic funds-distribution | 国内資金分配 | 국내 자금 분배 | Distribution domestique des fonds | Distribución doméstica de fondos | Distribuição doméstica de fundos | Внутреннее распределение средств | التوزيع المحلي للأموال |
| 截留境内 | Retained in Mainland China | 中国本土内に留保 | 중국 본토 내 유보 | Retenu en Chine continentale | Retenido en China continental | Retido na China continental | Удержание средств в материковом Китае | الاحتفاظ بالأموال داخل البر الرئيسي الصيني |
| 管理账期 | Account Period Management | 決済期間管理 | 계정 기간 관리 | Gestion de la période comptable | Gestión del período de cuenta | Gestão do período de conta | Управление расчётным периодом | إدارة فترة الحساب |
| 最大比例 | Maximum Proportion | 最大比率 | 최대 비율 | Proportion maximale | Proporción máxima | Proporção máxima | Максимальная доля | الحد الأقصى للنسبة |
| 该字段为必填项 | This Field is Required | このフィールドは必須 | 이 필드는 필수입니다 | Ce champ est obligatoire | Este campo es obligatorio | Este campo é obrigatório | Это поле обязательно для заполнения | هذا الحقل مطلوب |

---

## 产品与文档

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 产品简介 | Product Introduction | 製品概要 | 제품 소개 | Introduction du produit | Introducción del producto | Introdução do produto | Описание продукта | مقدمة المنتج |
| 应用场景 | Application Scenarios | 応用シナリオ | 적용 시나리오 | Scénarios d'application | Escenarios de aplicación | Cenários de aplicação | Сценарии применения | سيناريوهات التطبيق |
| 产品流程 | Product Process | 製品プロセス | 제품 프로세스 | Processus produit | Proceso del producto | Processo do produto | Процесс продукта | عملية المنتج |
| 产品能力 | Product Capability | 製品機能 | 제품 기능 | Capacité du produit | Capacidad del producto | Capacidade do produto | Возможности продукта | قدرة المنتج |
| 接入前准备 | Preparation Before Integration | 導入前準備 | 연동 전 준비 | Préparation avant l’intégration | Preparación antes de la integración | Preparação antes da integração | Подготовка перед интеграцией | التحضير قبل التكامل |
| 开发指引 | Development Guidelines | 開発ガイドライン | 개발 가이드라인 | Guide de développement | Guía de desarrollo | Guia de desenvolvimento | Руководство по разработке | إرشادات التطوير |
| 申请指引 | Application Guidelines | 申請ガイドライン | 신청 가이드라인 | Guide de demande | Guía de solicitud | Guia de solicitação | Руководство по заявке | إرشادات التقديم |
| API列表 | API List | APIリスト | API 목록 | Liste des API | Lista de API | Lista de API | Список API | قائمة واجهات API |
| API字典 | API Dictionary | API辞書 | API 사전 | Dictionnaire API | Diccionario API | Dicionário API | Словарь API | قاموس API |
| APIv3接口规则 | APIv3 Rules | APIv3ルール | APIv3 규칙 | Règles APIv3 | Reglas de APIv3 | Regras de APIv3 | Правила APIv3 | قواعد APIv3 |
| 开发工具 | Development Tool | 開発ツール | 개발 도구 | Outil de développement | Herramienta de desarrollo | Ferramenta de desenvolvimento | Инструмент разработки | أداة التطوير |
| 编程语言 | Programming Language | プログラミング言語 | 프로그래밍 언어 | Langage de programmation | Lenguaje de programación | Linguagem de programação | Язык программирования | لغة البرمجة |
| 前置条件 | Preconditions | 前提条件 | 사전 조건 | Prérequis | Requisitos previos | Pré-condições | Предварительные условия | الشروط المسبقة |
| 开发者 | Developer | 開発者 | 개발자 | Développeur | Desarrollador | Desenvolvedor | Разработчик | المطور |
| 跨境开发者中心 | Global Developers Center | グローバル開発者センター | 글로벌 개발자 센터 | Centre des développeurs mondiaux | Centro de desarrolladores globales | Centro de desenvolvedores globais | Глобальный центр разработчиков | مركز المطورين العالميين |
| 服务场景 | Service Scenarios | サービスシナリオ | 서비스 시나리오 | Scénarios de service | Escenarios de servicio | Cenários de serviço | Сценарии обслуживания | سيناريوهات الخدمة |
| 使用场景 | Usage Scenario | 使用シナリオ | 사용 시나리오 | Scénario d'utilisation | Escenario de uso | Cenário de uso | Сценарий использования | سيناريو الاستخدام |
| 备注 | Remarks | 備考 | 비고 | Remarques | Observaciones | Observações | Примечания | ملاحظات |

---

## 投诉与客服

| 中文 | English | 日本語 | 한국어 | Français | Español | Português | Русский | العربية |
|------|---------|--------|--------|----------|---------|-----------|---------|---------|
| 投诉单 | Dispute Form | クレームフォーム | 분쟁 양식 | Formulaire de litige | Formulario de disputa | Formulário de disputa | Форма жалобы | نموذج النزاع |
| 客诉单 | Customer Complaint Form | 顧客苦情フォーム | 고객 불만 양식 | Formulaire de réclamation client | Formulario de queja del cliente | Formulário de reclamação do cliente | Форма жалобы клиента | نموذج شكوى العميل |
| 单边交易 | Transaction Status Mismatch | 取引状態不一致 | 거래 상태 불일치 | Désaccord de statut de transaction | Discrepancia de estado de transacción | Discrepância de status de transação | Несоответствие статуса транзакции | عدم تطابق حالة المعاملة |

---

> 本文件为优化版，基于测试版 v2.0 修订，更新于 2026-06-04。
> 语言说明：中文 / English / 日本語 / 한국어 / Français / Español / Português / Русский / العربية
> 词条来源：原版 glossary.md（59条）+ Excel 境外支付 Glossary v1（新增词条）+ 名词表.xlsx（全量补充）
