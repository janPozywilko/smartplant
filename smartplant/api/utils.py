from urllib import response
from paho.mqtt import publish
from influxdb_client import InfluxDBClient
import base64
import json
import requests


from smartplant.settings import INFLUX_URL, INFLUX_TOKEN, INFLUX_BUCKET, INFLUX_ORG

headers={"Authorization":"Bearer NNSXS.MUC4M7BKHJES6KLD3AMW4CNWNVP6FYT6Z2VCVRQ.LPCFTOCP7NEFLTDI42JN5PV2IVUZ5LNCHLIPFU3ZO4UFKELERJZA", "Content-Type":"application/json"}

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

query_api = client.query_api()

def encrypt64(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii') 
    
    return str(base64_message)

def downlinks(message):
    return '{"downlinks":[{"f_port":2,"frm_payload":"%s","priority": "HIGH","confirmed":true}]}'%encrypt64(message)

def get_minutes(minutes, dev_eui):
    json_response = []
    query = f'from(bucket: "testing") |> range(start: -{minutes}m) |> filter(fn: (r) => r["_measurement"] == "plantbox") |> filter(fn: (r) => r["_field"] == "ground_temperature" or r["_field"] == "humidity" or r["_field"] == "light" or r["_field"] == "moisture" or r["_field"] == "temperature") |> filter(fn: (r) => r["dev-eui"] == "{dev_eui}") |> group(columns: ["_time"])'
    tables = query_api.query(org=INFLUX_ORG, query=query)
    for table in tables:
        result = {}
        row = {}
        row['time'] = table.records[0].get_time()
        for record in table.records:
            row['time'] = record.get_time()
            result[record.get_field()] = record.get_value()
        row['data'] = result
        json_response.append(row)
    
    return json_response

def get_range(start, stop, dev_eui):
    minutes = range
    json_response = []
    query = f'from(bucket: "testing") |> range(start: {start}, stop: {stop}) |> filter(fn: (r) => r["_measurement"] == "plantbox") |> filter(fn: (r) => r["_field"] == "g" or r["_field"] == "h" or r["_field"] == "l" or r["_field"] == "m" or r["_field"] == "t") |> filter(fn: (r) => r["dev-eui"] == "{dev_eui}") |> group(columns: ["_time"])'
    tables = query_api.query(org=INFLUX_ORG, query=query)
    for table in tables:
        result = {}
        row = {}
        row['time'] = table.records[0].get_time()
        for record in table.records:
            row['time'] = record.get_time()
            result[record.get_field()] = record.get_value()
        row['data'] = result
        json_response.append(row)

    return json_response

def get_devices():
    devices = []
    response=requests.get("https://eu1.cloud.thethings.network/api/v3/applications/demo-v3-application/devices", headers={"Authorization":"Bearer NNSXS.MUC4M7BKHJES6KLD3AMW4CNWNVP6FYT6Z2VCVRQ.LPCFTOCP7NEFLTDI42JN5PV2IVUZ5LNCHLIPFU3ZO4UFKELERJZA", "Content-Type":"application/json"})
    json_response = response.json()

    for device in json_response["end_devices"]:
        device_id= device["ids"]["device_id"]
        device_eui = device["ids"]["dev_eui"]
        devices.append({"name": device_id, "device_eui": device_eui})

    return devices


def create_device_identity_server(device_id_from_request, dev_eui_from_request):
    device_id = device_id_from_request
    dev_eui = dev_eui_from_request

    data_IS = {
        "end_device": {
        "ids": {
            "device_id": device_id,
            "dev_eui": dev_eui,
            "join_eui": "1234567890123456"
        },
        "join_server_address": "eu1.cloud.thethings.network",
        "network_server_address": "eu1.cloud.thethings.network",
        "application_server_address": "eu1.cloud.thethings.network"
        }
    }
    
    url_IS = "https://eu1.cloud.thethings.network/api/v3/applications/demo-v3-application/devices"

    response_IS = requests.post(url_IS, data=json.dumps(data_IS), headers=headers)

    print(response_IS.status_code)

    return response_IS.status_code


def delete_device_identity_server(device_id):
    
    url_delete_IS = f"https://eu1.cloud.thethings.network/api/v3/applications/demo-v3-application/devices/{device_id}"

    response_delete_IS = requests.delete(url_delete_IS, headers=headers)

    return response_delete_IS.status_code


def create_device_join_server(device_id_from_request, dev_eui_from_request):
    device_id = device_id_from_request
    dev_eui = dev_eui_from_request

    data_JS = {
          "end_device": {
            "ids": {
              "device_id": device_id,
              "dev_eui": dev_eui,
              "join_eui": "1234567890123456"
            },
            "root_keys": {
              "app_key": {
                "key": "4868DC1E6296C0A329A2287BF06B5BA9"
              }
            },
            "network_server_address": "eu1.cloud.thethings.network",
            "application_server_address": "eu1.cloud.thethings.network"
          },
          "field_mask": {
            "paths": [
              "root_keys.app_key.key"
            ]
          }
        }


        

    url_JS = "https://eu1.cloud.thethings.network/api/v3/js/applications/demo-v3-application/devices"


    response_JS = requests.post(url_JS, data=json.dumps(data_JS), headers=headers)
    
    print(response_JS.status_code)

    return response_JS.status_code

def delete_device_join_server(device_id):
    
    url_delete_JS = f"https://eu1.cloud.thethings.network/api/v3/js/applications/demo-v3-application/devices/{device_id}"

    response_delete_JS = requests.delete(url_delete_JS, headers=headers)

    return response_delete_JS.status_code

def create_device_network_server(device_id_from_request, dev_eui_from_request):
    device_id = device_id_from_request
    dev_eui = dev_eui_from_request

    data_NS = {
          "end_device": {
            "ids": {
              "device_id": device_id,
              "dev_eui": dev_eui,
              "join_eui": "1234567890123456"
            },
            "frequency_plan_id": "EU_863_870_TTN",
            "lorawan_phy_version": "PHY_V1_0_3_REV_A",
            "lorawan_version": "MAC_V1_0_3",
            "supports_join": True
          },
          "field_mask": {
            "paths": [
              "frequency_plan_id",
              "lorawan_phy_version",
              "lorawan_version",
              "supports_join"
            ]
          }
        }

        

    url_NS = "https://eu1.cloud.thethings.network/api/v3/ns/applications/demo-v3-application/devices"


    response_NS = requests.post(url_NS, data=json.dumps(data_NS), headers=headers)
    
    print(response_NS.status_code)

    return response_NS.status_code

def delete_device_network_server(device_id):
    
    url_delete_NS = f"https://eu1.cloud.thethings.network/api/v3/ns/applications/demo-v3-application/devices/{device_id}"

    response_delete_NS = requests.delete(url_delete_NS, headers=headers)

    return response_delete_NS.status_code

def create_device_application_server(device_id_from_request, dev_eui_from_request):
    device_id = device_id_from_request
    dev_eui = dev_eui_from_request

    data_AS = {
          "end_device": {
            "ids": {
              "device_id": device_id,
              "dev_eui": dev_eui,
              "join_eui": "1234567890123456"
            }
          }
        }

    url_AS = "https://eu1.cloud.thethings.network/api/v3/as/applications/demo-v3-application/devices"


    response_AS = requests.post(url_AS, data=json.dumps(data_AS), headers=headers)

    print(response_AS.status_code)
    
    return response_AS.status_code

def delete_device_application_server(device_id):
    
    url_delete_AS = f"https://eu1.cloud.thethings.network/api/v3/as/applications/demo-v3-application/devices/{device_id}"

    response_delete_AS = requests.delete(url_delete_AS, headers=headers)

    return response_delete_AS.status_code