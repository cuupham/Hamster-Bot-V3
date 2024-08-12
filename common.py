from datetime import datetime, timedelta
import requests
from requests.exceptions import RequestException
import base64, binascii
import re
from apis.config import BASE_URL, HEADER_GENERIC, HEADER_JSON


""" TIME """


def get_curr_timestamp():
    return round(datetime.now().timestamp())


def get_curr():
    return datetime.now()


def add_secs_to_curr(seconds: float):
    return datetime.now() + timedelta(seconds=seconds)


""" DECODE """


def alpha_b64(code: str):
    try:
        decode_str = base64.b64decode(code).decode("utf-8")

        if re.fullmatch(r"[A-Za-z]+", decode_str):
            return decode_str

    except binascii.Error as e:
        print(f"Lỗi dữ liệu base64: {e}")
    except UnicodeDecodeError as e:
        print(f"Lỗi giải mã UTF-8: {e}")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")


""" REQUEST """


def fetch_json(
    endpoint: str, url: str = BASE_URL, header: dict = HEADER_GENERIC
) -> dict:
    try:
        response = requests.post(rf"{url}/{endpoint}", headers=header)
        response.raise_for_status()
        return response.json()
    except RequestException as error:
        print(f"[fetch_json '{endpoint}' Error]: {error}\n {response.text}")


def send_post_request(
    endpoint: str, payload: dict, url: str = BASE_URL, header: dict = HEADER_JSON
):
    try:
        response = requests.post(rf"{url}/{endpoint}", headers=header, json=payload)
        response.raise_for_status()
        return response
    except RequestException as error:
        print(f"[send_post_request '{endpoint}]' Error]: {error}\n {response.text}")
