import os


def get_token(file_path: str = "token.txt") -> str:
    """
    Đọc token từ tệp tin và trả về giá trị của nó.

    :param file_path: Đường dẫn đến tệp tin chứa token
    :return: Token nếu thành công, hoặc chuỗi rỗng nếu không có token
    :raises FileNotFoundError: Nếu tệp tin không tồn tại
    :raises IOError: Nếu không thể mở tệp tin
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Token file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            token = file.readline().strip()
            if token:
                return token
            else:
                raise ValueError(
                    "Token file is empty or does not contain a valid token"
                )
    except IOError as e:
        raise IOError(f"Error opening token file: {e}")


BASE_URL = "https://api.hamsterkombatgame.io/clicker"
AUTH_URL = "https://api.hamsterkombatgame.io/auth"
HEADER_BASE = {
    "accept-language": "en-US,en;q=0.9",
    "authorization": f"Bearer {get_token()}",
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
HEADER_GENERIC = {"accept": "*/*", **HEADER_BASE}
HEADER_JSON = {
    "accept": "application/json",
    "content-type": "application/json",
    **HEADER_BASE,
}
