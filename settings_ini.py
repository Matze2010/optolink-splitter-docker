'''
   Copyright 2024 philippoo66
   
   Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.gnu.org/licenses/gpl-3.0.html

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import os
import json

# Serial Ports +++++++++++++++++++
port_optolink = os.getenv('PORT_OPTOLINK', '/dev/serial0')          # Serial port for Optolink device (mandatory, default: '/dev/ttyUSB0')
port_vitoconnect = os.getenv('PORT_VITOCONNECT', None)              # Serial port for Vitoconnect (optional, set None if no Vitoconnect) Pls check https://github.com/philippoo66/optolink-splitter/wiki/520-termios.error:-(22,-'Invalid-argument')
vs2timeout = int(os.getenv('VS2_TIMEOUT', 120))                          # Timeout (seconds) for VS2 protocol detection (default: 120)

# MQTT Connection ++++++++++++++++
mqtt = os.getenv('MQTT_HOST', "192.168.0.123:1883")     # MQTT broker address (default: "192.168.0.123:1883", set None to disable MQTT)
mqtt_user = os.getenv('MQTT_USER', None)                # MQTT user credentials: "<user>:<pwd>" (default: None for anonymous access)
mqtt_logging = bool(os.getenv('MQTT_LOGGING', False))        # dis/enables logging of paho.mqtt (default: False)

# MQTT Topics ++++++++++++++++++++
# Best practices recommendation: Always use lowercase for consistency and compatibility.
mqtt_fstr = os.getenv('MQTT_FSTR', "{dpname}")          # Format string for MQTT messages (default: "{dpname}", alternative e.g.: "{dpaddr:04X}_{dpname}")
mqtt_topic = os.getenv('MQTT_TOPIC', "Vito")            # MQTT topic for publishing data (default: "Vito")
mqtt_listen = os.getenv('MQTT_LISTEN', "Vito/cmnd")     # MQTT topic for incoming commands (default: "Vito/cmnd", set None to disable)
mqtt_respond = os.getenv('MQTT_RESPOND', "Vito/resp")   # MQTT topic for responses (default: "Vito/resp", set None to disable)
mqtt_retain = bool(os.getenv('MQTT_RETAIN', False))           # Publish retained messages. Last message per topic is stored on broker and sent to new/reconnecting subscribers. (default: False)

# TCP/IP ++++++++++++++++++++++++++
tcpip_port = 65234               # TCP/IP port for communication (default: 65234, used by Viessdata; set None to disable TCP/IP)

# Optolink Communication Timing +
fullraw_eot_time = 0.05         # Timeout (seconds) to determine end of telegram (default: 0.05)
fullraw_timeout = 2             # Overall timeout (seconds) for receiving data (default: 2)
olbreath = 0.1                  # Pause (seconds) after a request-response cycle (default: 0.1)

# Optolink Logging ++++++++++++++
log_vitoconnect = False         # Enable logging of Vitoconnect Optolink rx+tx telegram communication (default: False)
show_opto_rx = bool(os.getenv('LOG_OPTOLINK', True))             # Display received Optolink data (default: True, no output when run as service)

# Data Formatting +++++++++++++++
max_decimals = 4                # Max decimal places for float values (default: 4)
data_hex_format = '02x'         # Hexadecimal formatting (set '02X' for uppercase formatting, default: '02x')
resp_addr_format = 'x'          # Format of DP addresses in MQTT/TCPIP request responses ('d' for decimal, e.g. '04X' for 4-digit hex, default: 'x')

# Viessdata Utilities +++++++++++
write_viessdata_csv = False     # Enable writing Viessdata to CSV (default: False)
viessdata_csv_path = ""         # File path for Viessdata CSV output (default: "")
buffer_to_write = 60            # Buffer size before writing to CSV (default: 60)
dec_separator = ","             # Decimal separator for CSV output (default: ",")

# 1-Wire Sensors +++++++++++++++
# A typical sensor for temperature could be DS18B20; please mind that GPIO must be enabled for 1-Wire sensors (see Optolink-Splitter Wiki)
# Dictionary for 1-Wire sensor configuration (default: empty dictionary)
w1sensors = {                  
    # Addr: ('<w1_folder/sn>', '<slave_type>'),   # entry format
#     0xFFF4: ('28-3ce1d4438fd4', 'ds18b20'),     # Example sensor (highest known Optolink Address is 0xFF17)
#     0xFFFd: ('28-3ce1d443a4ed', 'ds18b20'),     # Another example sensor
}

# Datapoint Polling List+++++++++
poll_interval = int(os.getenv('POLL_INTERVAL', 30))              # Polling interval (seconds), 0 for continuous, -1 to disable (default: 30)
poll_items_default = [
    # (Name, DpAddr, Len, Scale/Type, Signed)

    # meine Viessdata Tabelle
    #088E;0800;0802;0804;0808;5525;5523;5527;0A82;0884;5738;088A;08A7;0A10;0C20;0A3C;0C24;555A;A38F;55D3;A152;6500;6513;6515;
    ("Anlagenzeit", 0x088E, 8, 'vdatetime'),

    ("AussenTemp", 0x0800, 2, 0.1, True),
    ("KesselTemp", 0x0802, 2, 0.1, False),
    ("WW/SpeicherTemp", 0x0804, 2, 0.1, False),
    ("AbgasTemp", 0x0808, 2, 0.1, False),

    ("AussenTemp_fltrd", 0x5525, 2, 0.1, True),
    ("AussenTemp_dmpd", 0x5523, 2, 0.1, True),
    ("AussenTemp_mixed", 0x5527, 2, 0.1, True),

    ("Eingang STB-Stoerung", 0x0A82, 1, 1, False),
    ("Brennerstoerung", 0x0884, 1, 1, False),
    ("Fehlerstatus Brennersteuergeraet", 0x5738, 1, 1, False),

    ("Brennerstarts", 0x088A, 4, 1, False),
    ("Betriebsstunden", 0x08A7, 4, 2.7777778e-4, False),  # 1/3600

    ("Stellung Umschaltventil", 0x0A10, 1, 1, False),

    ("RL/RuecklaufTemp_calcd", 0x0C20, 2, 0.01, False),
    ("Pumpenleistung", 0x0A3C, 1, 1, False),
    ("Volumenstrom", 0x0C24, 2, 0.1, False),  # eigentlich scale 1 aber für Viessdata Grafik

    ("KesselTemp_soll", 0x555A, 2, 0.1, False),
    ("BrennerLeistung", 0xA38F, 1, 0.5, False),
    ("BrennerModulation", 0x55D3, 1, 1, False),

    ("Status", 0xA152, 2, 1, False),
    ("SpeicherTemp_soll_akt", 0x6500, 2, 0.1, False),
    ("Speicherladepumpe", 0x6513, 1, 1, False),
    ("Zirkulationspumpe", 0x6515, 2, 1, False),
    # bis hierher meine Viessdata Tabelle --------

#    ("Frostgefahr, aktuelle RTS etc", 0x2500, 22, 'raw'),
    ("Frostgefahr, aktuelle RTS etc", 0x2500, 22, 'b:0:21::raw'),
    ("Frostgefahr", 0x2500, 22, 'b:16:16::raw'),
    ("RTS_akt", 0x2500, 22, 'b:12:13', 0.1, False),
]

poll_items = json.loads(os.environ.get('POLL_ITEMS')) if os.environ.get('POLL_ITEMS') else poll_items_default

