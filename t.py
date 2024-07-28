import requests
import schedule
import time
from datetime import datetime, timedelta

# File URL
url = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/mix"

# Telegram Bot Details
bot_token = '6589182310:AAEc8lhnfxOPU0JZEzTGMx3kCuJwTjMV5s4'
channel_username = '@internetazad66'

# Variables
config_list = []
last_download_time = None
index = 0

def download_file():
    global last_download_time
    global config_list
    
    # Download the file once a month
    if last_download_time is None or datetime.now() - last_download_time > timedelta(days=30):
        print("Downloading file...")
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            config_list = parse_configs(content)
            last_download_time = datetime.now()
            print("File downloaded and processed.")
        else:
            print("Error in downloading the file.")
    else:
        print("No need to download.")

def parse_configs(content):
    configs = []
    lines = content.split('\n')
    for line in lines:
        if any(protocol in line for protocol in ["vmess://", "vless://", "trojan://", "ss://"]):
            configs.append(line)
    return configs

def send_telegram_message(message):
    payload = {
        'UrlBox': f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_username}&text=`{message}`&parse_mode=MarkdownV2',
        'ContentTypeBox': '',
        'ContentDataBox': '',
        'HeadersBox': '',
        'RefererBox': '',
        'AgentList': 'Internet Explorer',
        'AgentBox': '',
        'VersionsList': 'HTTP/1.1',
        'MethodList': 'POST',
    }

    url = "https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx"
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")
        print(response.text)

def print_next_config():
    global config_list
    global index

    if config_list:
        if index < len(config_list):
            config = config_list[index]
            print("Config:", config)
            send_telegram_message(config)  # Send config to Telegram channel
            index += 1
        else:
            print("All configs have been printed. Starting the list from the beginning.")
            index = 0
    else:
        print("The config list is empty. Please download the file.")

# Scheduling
schedule.every(60).seconds.do(print_next_config)
schedule.every(30).days.do(download_file)

if __name__ == "__main__":
    try:
        download_file()  # First file download
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exit.")

