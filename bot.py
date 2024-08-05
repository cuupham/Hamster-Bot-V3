import requests, sys
from datetime import datetime, timedelta
import base64, re
from time import sleep
from requests.exceptions import RequestException
import binascii

def timestamp():
    return round(datetime.now().timestamp())

def current_time():
    return datetime.now()

def add_mins_to_cur_time(mins:float):
    return datetime.now() +timedelta(minutes=mins)

def get_token(file_path="token.txt"):
    with open(file_path, "r") as file:
        return file.readline().strip()


class UrlPath:
    def __init__(self) -> None:
        self.account_info = "account-info"
        self.list_tasks = "list-tasks"
        self.check_tasks = "check-task"
        self.sync = "sync"
        self.tap = "tap"
        self.claim_daily_cipher = "claim-daily-cipher"
        self.boost_for_buy = "boosts-for-buy"
        self.buy_boost = "buy-boost"
        self.config = "config"
        self.upgrades_for_buy = "upgrades-for-buy"


class Api(UrlPath):
    URL = "https://api.hamsterkombatgame.io/clicker"

    def __init__(self, BEAR_TOKEN: str):
        super().__init__()

        self.HEADER_FIRST = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {BEAR_TOKEN}",
            "origin": "https://hamsterkombatgame.io",
            "priority": "u=1, i",
            "referer": "https://hamsterkombatgame.io/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
        self.HEADER_SECOND = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {BEAR_TOKEN}",
            "content-type": "application/json",
            "origin": "https://hamsterkombatgame.io",
            "priority": "u=1, i",
            "referer": "https://hamsterkombatgame.io/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def post_req(self, path, header, payload=None, url=URL):
        try:
            response = requests.post(rf"{url}/{path}", headers=header, json=payload)
            response.raise_for_status()  # Kiểm tra mã trạng thái HTTP
            return response
        except RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def account_info_req(self):
        return self.post_req(
            self.account_info,
            self.HEADER_FIRST,
            url="https://api.hamsterkombatgame.io/auth",
        )

    def list_tasks_req(self):
        return self.post_req(self.list_tasks, self.HEADER_FIRST)

    def streak_days(self):
        json_data = {
            "taskId": "streak_days",
        }
        return self.post_req(self.check_tasks, self.HEADER_SECOND, json_data)

    def sync_req(self):
        return self.post_req(
            self.sync,
            self.HEADER_FIRST,
        )

    def tap_req(self, tap_number: int):
        json_data = {
            "count": tap_number,
            "availableTaps": tap_number,
            "timestamp": timestamp(),
        }
        return self.post_req(self.tap, self.HEADER_SECOND, json_data)

    def claim_cipher_req(self, code: str):
        json_data = {"cipher": f"{code.strip().upper()}"}
        return self.post_req(self.claim_daily_cipher, self.HEADER_SECOND, json_data)

    def boost_for_buy_req(self):
        return self.post_req(self.boost_for_buy, self.HEADER_FIRST)

    def buy_boost_req(self):
        json_data = {
            "boostId": "BoostFullAvailableTaps",
            "timestamp": timestamp(),
        }
        return self.post_req(self.buy_boost, self.HEADER_SECOND, json_data)

    def check_task_req(self, task_id: str):
        json_data = {
            "taskId": f"{task_id}",
        }

        return self.post_req(self.check_tasks, self.HEADER_SECOND, json_data)

    def config_req(self):
        return self.post_req(self.config, self.HEADER_FIRST)

    def upgrades_for_buy_req(self):
        return self.post_req(self.upgrades_for_buy, self.HEADER_FIRST)


class Bot(Api):
    def __init__(self, BEAR_TOKEN: str):
        super().__init__(BEAR_TOKEN)
        self.check_account()
        self.claim_quests()

    def check_account(self):
        response =  self.account_info_req()
        if response:
            print(response.json().get('accountInfo',{}).get('name'))
        else:
            print('Token đã gây ra lỗi. Đang đóng chương trình...')
            sys.exit()

    def claim_quests(self):
        response = self.list_tasks_req()
        response_config = self.config_req()

        print(f'{'='*50}Daily Quest{'='*50}')
        data = response.json()

        # Điểm danh
        is_completed = data.get("tasks", {})[-1].get("isCompleted")
        if is_completed:
            print(f"Điểm danh: SKIP")
        else:
            self.streak_days()
            print("Điểm danh: DONE")

        # Hamster Youtube
        ham_list = [
            task["id"]
            for task in data["tasks"][:6]
            if not task["isCompleted"] and "hamster_youtube" in task["id"]
        ]
        if ham_list:
            for ham in ham_list:
                self.check_task_req(ham)
                print(f"Check Hams Youtube: {ham}")
        else:
            print("Check Hams Youtube: SKIP")

        # Secret Code
        
        data_config = response_config.json()
        isclaimed_cipher = data_config.get("dailyCipher", {}).get("isClaimed")

        if isclaimed_cipher:
            print("Cipher: SKIP")
        else:
            code = str(data_config.get("dailyCipher", {}).get("cipher"))

            for index, char in  reversed(list(enumerate(code))):
                if char.isdigit():
                    new_code = code[:index] + code[index + 1 :]
                    print(f"Xóa ký tự tại index {index}: {new_code}")
                    try:
                        decode_string = base64.b64decode(new_code).decode("utf-8")

                        print(f"Chuỗi Decode: {decode_string}")

                        if decode_string and bool(
                            re.fullmatch(r"[A-Za-z]+", decode_string)
                        ):
                            self.claim_cipher_req(decode_string)
                            print(f"Cipher: Code {code} - {decode_string} nhập thành công")
                            break
                    except binascii.Error as e:
                        print(f"Lỗi dữ liệu base64: {e}")
                    except UnicodeDecodeError as e:
                        print(f"Lỗi giải mã UTF-8: {e}")
                    except Exception as e:
                        print(f"Lỗi không xác định: {e}")

                    


        print('='*(50*2+len('Daily Quest')))

    def tapping(self):
        response = self.sync_req()

        data = response.json()
        available_taps = data.get("clickerUser", {}).get("availableTaps", [])

        if available_taps:
            self.tap_req(available_taps).raise_for_status()
            print(f"Tapping: {available_taps}")
        else:
            print(f'Tapping: Có lỗi xảy ra. Status code: {response.status_code}')

    def get_boost_info(self):
        response = self.boost_for_buy_req()

        data = response.json()
        cd_seconds = data.get("boostsForBuy", [])[-1].get("cooldownSeconds")
        max_taps = data.get("boostsForBuy", [])[-1].get('maxTaps')

        return cd_seconds, max_taps

