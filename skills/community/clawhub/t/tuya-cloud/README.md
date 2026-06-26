# Tuya Cloud Controller

Control and read Tuya/Smart Life devices via the Tuya Cloud OpenAPI.
The installation guide can be found here: https://medium.com/@min.shi.happy/building-a-tuya-smart-home-controller-skill-for-openclaw-beadb796c05c

---

## 1. Get your API credentials

### Step 1 — Sign in to the Tuya Developer Platform

Go to [platform.tuya.com](https://platform.tuya.com) and sign in with your Tuya account.  
In the left sidebar navigate to **Cloud → Development**.

### Step 2 — Create a cloud project

On the **My Cloud Projects** page, click **Create Cloud Project**.  
Choose the **Smart Home** project type — this is the type that links Smart Life / Tuya app devices and supports OpenAPI access.

### Step 3 — Fill in project details

Enter a project name, description, and select the **data center region** that matches your Smart Life app account:

| Region | Data center |
|---|---|
| Europe | `openapi.tuyaeu.com` |
| Americas / SEA | `openapi.tuyaus.com` |
| China | `openapi.tuyacn.com` |
| India | `openapi.tuyain.com` |

Click **Create** to proceed to the project configuration flow.

### Step 4 — Authorize API services

In the configuration wizard, authorize the cloud services the project needs.  
At minimum, subscribe to and authorize **IoT Core** and **Smart Home Device Control**.

### Step 5 — Open the project Overview

After creation, click into the project to open its **Overview** page.  
Tuya automatically generates a pair of authorization keys for every new project.

### Step 6 — Copy the authorization keys

On the Overview page, locate the **Authorization Key** section.  
Copy the two values into your `.env` file:

```bash
TUYA_ACCESS_ID=<Client ID / Access ID shown here>
TUYA_ACCESS_SECRET=<Client Secret / Access Secret shown here>
TUYA_API_ENDPOINT=https://openapi.tuyaeu.com   # match to your region
```

### Step 7 — Set device permission to Controllable

By default, devices are added with **read-only** permission.  
To be able to send commands (turn on/off, set values, etc.) you must upgrade this:

1. Inside the project, go to the **Devices** tab.
2. Find your linked devices and open the permission settings.
3. Change the permission from **Read** to **Controllable**.

Without this step, `control_device` commands will be rejected by the API.

---

## 2. Link your Smart Life devices

Inside the project, go to **Devices → Link Tuya App Account** and scan the QR code with your Smart Life app. This imports all devices from your app into the project so they are accessible via the API.

---

## 3. Install dependencies

```bash
pip install tinytuya python-dotenv
```

---

## 4. Verify the setup

```bash
python scripts/tuya_controller.py list_devices
```

You should see a list of all your linked devices with their IDs and online status.
