from common import *
from apis.config import AUTH_URL
from apis.endpoints import *
import sys
from time import sleep

def get_username():
    json_data = fetch_json(ACCOUNT_INFO, AUTH_URL)

    if json_data:
        print(f' Account Name: {json_data.get('accountInfo',{}).get('name')}')
    else:
        print('Token đã có lỗi xảy ra. Exiting...')
        sys.exit()

def claim_quests():
    print(f'{'='*50}Daily Quest{'='*50}')

    list_task_dict = fetch_json(LIST_TASKS)
    config_dict = fetch_json(CONFIG)

    # Điểm danh
    is_completed = list_task_dict.get("tasks",{})[-1].get("isCompleted")
    if is_completed:
        print(f" Điểm danh: <SKIP>")
    else:
        result_streak = send_post_request(CHECK_TASKS, {
            "taskId": "streak_days",
        })

        if result_streak:
            print(' Điểm danh: <DONE>')

    # Hamster Youtube
    hams_list = [
        task['id'] for task in list_task_dict['tasks'][:6] if not task['isCompleted'] and "hamster_youtube" in task['id']
    ]

    if hams_list:
        print(' Hamster Youtube:')
        for ham_id in hams_list:
            result_ham =send_post_request(CHECK_TASKS,{
                "taskId": f"{ham_id}",
            })
            if result_ham:
                print(f' - Checked Ham ID: {ham_id}')
    else:
        print(' Hamster Youtube: <SKIP>')

    # Secret Code
    isclaimed_cipher = config_dict.get("dailyCipher", {}).get("isClaimed")

    if isclaimed_cipher:
        print(' Cipher: <SKIP>')
    else:
        code = str(config_dict.get('dailyCipher', {}).get('cipher'))
        for index,char in reversed(list(enumerate(code))):
            if char.isdigit():
                new_code = code[:index] + code[index+1:]
                print(f" Checking: {new_code}")
                
                decode_new_code = alpha_b64(new_code)
                if decode_new_code:
                    result_secret_code = send_post_request(
                        CLAIM_DAILY_CIPHER, {
                        "cipher": f"{decode_new_code.strip().upper()}"
                        }
                    )
                    if result_secret_code:
                        print(f" Cipher Code: {code} - {decode_new_code} <DONE>")
                    break


    print('='*(50*2+len('Daily Quest')))

def tap():
    sync_dict = fetch_json(SYNC)
    
    avail_taps = sync_dict.get("clickerUser",{}).get("availableTaps",[])
    if avail_taps:
        result = send_post_request(TAP, {
            "count": avail_taps,
            "availableTaps": avail_taps,
            "timestamp": get_curr_timestamp(),
        })

        if result:
            print(f'Tapped: {avail_taps}')
    else:
        print(f'Tap đã xảy ra lỗi.')


def get_cd_boost():
    boost_dict = fetch_json(BOOST_FOR_BUY)
    return boost_dict.get("boostsForBuy", [])[-1].get("cooldownSeconds")


def wait_time(secs):
    print(f'Now: [{get_curr()}] - Next Click: [{add_secs_to_curr(secs)}]')
    sleep(secs)

def process_tap_and_boost():
    tap()

    cd_boost = get_cd_boost()
    if cd_boost == 0:
        result = send_post_request(BUY_BOOST,{
            "boostId": "BoostFullAvailableTaps",
            "timestamp": get_curr_timestamp(),
        })
        if result:
            print('Bought Boost.')
    elif cd_boost <= 3600:
        print(f'Boost đang hồi trong: {cd_boost} giây')
        wait_time(cd_boost)
    else:
        print('Boost đã sử dụng hết trong hôm nay. Hãy chờ đến ngày mai.')
        wait_time(20*60)

    print()

def run():
    

    while True:
        get_username()
        claim_quests()


        now = get_curr()
        end_time = now.replace(hour=7, minute=0, second=0, microsecond=0)
        if now > end_time:
            end_time+=timedelta(days=1)


        print(f'Thời gian restart script: {end_time}\n')

        while get_curr() < end_time:
            process_tap_and_boost()

        print("!! Restart script...")

if __name__ == "__main__":
    run()
   
