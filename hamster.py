from hams_module import (
    Bot,
    get_token,
    datetime,
    sleep,
    timedelta,
    current_time,
    add_mins_to_cur_time,
)


token = get_token()

while True:
    bot = Bot(token)
    now = datetime.now()
    end_time = now.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(
        days=1
    )

    while datetime.now() < end_time:
        bot.tapping()

        cd_boost, max_taps_boost = bot.get_boost_info()

        if max_taps_boost == 0:
            wait_mins = 30
            print(
                f"Now: {current_time()} -> Next Click: {add_mins_to_cur_time(wait_mins)}"
            )
            sleep(wait_mins * 60)

        elif 0 < max_taps_boost <= 6 and not cd_boost:
            bot.buy_boost_req()
            print("Đã buy boost THÀNH CÔNG.")
            sleep(1)
            bot.tapping()

            new_cd_boost = bot.get_boost_info()[0]
            print(
                f"Boost đang hồi phục: {new_cd_boost} giây -> Next Click: {add_mins_to_cur_time(new_cd_boost/60)}"
            )
            sleep(new_cd_boost)

        elif 0 < max_taps_boost <= 6 and cd_boost:
            print(
                f"Boost đang hồi: {cd_boost} giây -> Next Click: {add_mins_to_cur_time(cd_boost/60)}"
            )
            sleep(cd_boost)

        print()
    else:
        print(f"Restart Chương trình...")
