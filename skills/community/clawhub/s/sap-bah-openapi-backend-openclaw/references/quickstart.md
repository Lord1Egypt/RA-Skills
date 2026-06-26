# Quickstart

## 1. Prepare environment

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
sudo mkdir -p /usr/download
sudo chown "$USER":staff /usr/download
export SAP_HUB_USERNAME='your_user'
export SAP_HUB_PASSWORD='your_password'
```

## 2. Download API specs with environment-variable auth

```bash
python3 Skills/sap-bah-openapi-backend-openclaw-upload-1.0.0/scripts/reliable_sap_hub_download.py \
  --api-id WAREHOUSEORDER_0001 \
  --api-id API_APAR_SEPA_MANDATE_SRV
```

## 3. Verify files in /usr/download

```bash
ls -lh /usr/download | rg 'WAREHOUSEORDER_0001|API_APAR_SEPA_MANDATE_SRV'
```

## 4. Import into APIConnectionToSAP category

```bash
python3 Skills/sap-bah-openapi-backend-openclaw-upload-1.0.0/scripts/import_sap_hub_spec.py \
  --category OSC2.0 \
  --pattern WAREHOUSEORDER_0001 \
  --mode copy
```
