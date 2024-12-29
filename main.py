import requests,tls_client,json,os,secrets,time,ctypes,threading,datetime,random
from colorama import Fore
from color import C
from bs4 import BeautifulSoup
from time import sleep

s = tls_client.Session(client_identifier="chrome_128", random_tls_extension_order=True)
s2 = tls_client.Session(client_identifier="chrome_128", random_tls_extension_order=True)

apikey = json.load(open("config.json"))['captcha']["apikey"]
service = json.load(open("config.json"))["captcha"]["service"]
proxy = json.load(open('config.json'))["proxy"]["ipandport"]
proxytype = json.load(open("config.json"))["proxy"]["type"]

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

class Console:
    def title():
        while True:
            payload = {
                "clientKey":apikey
            }
            proxies = {
                f"{proxytype}":f"{proxytype}{proxy}",
            }
            current_time = time.time()
            elapsed_time = current_time - Stats.start
            if elapsed_time != 0:
                try:
                    success_rate = round((Stats.created / (Stats.error + Stats.created)) * 100, 2)
                except ZeroDivisionError:
                    success_rate = 0

            elapsed_days = int(elapsed_time // 86400)
            elapsed_hours = int((elapsed_time % 86400) // 3600)
            elapsed_minutes = int((elapsed_time % 3600) // 60)
            elapsed_seconds = int(elapsed_time % 60)
            balance = requests.post('https://api.capmonster.cloud/getBalance',json=payload,proxies=proxies).json().get("balance")
            ctypes.windll.kernel32.SetConsoleTitleW(
                f'Created:{Stats.created} ~~~ Error:{Stats.error} ~~~ Solved:{Stats.solved} ~~~ Balance:{balance}$ ~~~ Success Rate:{success_rate}% ~~~ '+
                f'Elapsed:{elapsed_days}d/{elapsed_hours}h/{elapsed_minutes}m/{elapsed_seconds}s'
                )
            sleep(0.1)

class Stats:
    created = 0
    error = 0
    solved = 0
    start = time.time()
    working = True

class Solver():
    def solve(self,service):
        if service == "capmonster":
            capmonload = {
                "clientKey": f"{apikey}",
                "task": {
                    "type": "TurnstileTaskProxyless",
                    "websiteURL": "https://streamlabs.com",
                    "websiteKey": "0x4AAAAAAACELUBpqiwktdQ9"
                }
            }
            response = requests.post('https://api.capmonster.cloud/createTask', json=capmonload)
            if response.ok:
                task_id = response.json().get('taskId')
                print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET} {C["orange"]}Task Created: {task_id}{Fore.RESET}')
            else:
                print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[~] Error Task Create: {response.json()}{Fore.RESET}')
                return

            time.sleep(4.6)
            capmonload2 = {
                "clientKey": f"{apikey}",
                "taskId": task_id
            }
            captcha_response = requests.post('https://api.capmonster.cloud/getTaskResult', json=capmonload2)
            turnstiletoken = captcha_response.json().get('solution', {}).get('token')
            if not turnstiletoken:
                print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[~] Error Solving CAPTCHA: {captcha_response.json()}{Fore.RESET}')
                Stats.error += 1
                return
            print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET} {C["orange"]}Solved Captcha: {turnstiletoken[:50]}{Fore.RESET}')
            Stats.solved += 1
            return turnstiletoken
        elif service == "capsolver":
            capsolverload = {
                "clientKey": f"{apikey}",
                "task": {
                    "type": "AntiCloudflareTask",
                    "websiteURL": "https://streamlabs.com",
                    "websiteKey": "0x4AAAAAAACELUBpqiwktdQ9",
                    "proxy":f'{proxytype}{proxy}'
                }
            }
            response = requests.post('https://api.capsolver.com/createTask', json=capsolverload)
            if response.ok:
                task_id = response.json().get('taskId')
                print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET} {C["orange"]}Task Created: {task_id}{Fore.RESET}')
            else:
                print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[~] Error Task Create: {response.json()}{Fore.RESET}')
                return

            time.sleep(4.6)
            capsolverload2 = {
                "clientKey": f"{apikey}",
                "taskId": task_id
            }
            captcha_response = requests.post('https://api.capsolver.com/getTaskResult', json=capsolverload2)
            turnstiletoken = captcha_response.json().get('solution', {}).get('token')
            if not turnstiletoken:
                print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[~] Error Solving CAPTCHA: {captcha_response.json()}{Fore.RESET}')
                Stats.error += 1
                return
            print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET} {C["orange"]}Solved Captcha: {turnstiletoken[:50]}{Fore.RESET}')
            Stats.solved += 1
            return turnstiletoken


def getVerifyCode(token):
    res2 = requests.get(f'https://api.tempmail.lol/auth/{token}')
    if res2.status_code == 200:
        messages = res2.json().get('email', [])

        for message in messages:
            html_content = message.get('html', '')
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                verification_code_div = soup.find("div", style=lambda x: x and "text-align: center" in x)
                if verification_code_div:
                    code = verification_code_div.text.strip()
                    return code
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[-] Verification code not found in messages.{Fore.RESET}')
    else:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[-] Failed to fetch messages: {res2.status_code}{Fore.RESET}')

def register():
    s.proxies = {
        f"{proxytype}":f"{proxytype}{proxy}",
    }
    res = requests.get('https://api.tempmail.lol/generate')
    if res.status_code != 200:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[~] Error Generating Temp Email{Fore.RESET}')
        return
    email = res.json().get('address')
    token = res.json().get('token')
    print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | ──────────────────────────────────────────────────────────────────────────────')
    print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET}{C["aqua"]} Got Mail:{Fore.RESET}{C["gray"]}{email}({token[:25]}.{Fore.RESET}{Fore.LIGHTCYAN_EX}**{Fore.RESET}{C["gray"]}){Fore.RESET}')
    r = s.get('https://streamlabs.com/slid/signup')
    xsrf = r.cookies.get('XSRF-TOKEN')
    print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET}{C["magenta"]} Get Xsrf:{xsrf[:40]}{Fore.RESET}')
    turnstiletoken = Solver().solve(service)
    password = ''.join([random.choice(random.choice([['a','e','f','g','h','m','n','t','y'],['A','B','E','F','G','H','J','K','L','M','N','Q','R','T','X','Y'],['2','3','4','5','6','7','8','9'],['','*','+','~','@','#','%','^','&','']])) for i in range(20)])
    payload = {
        "email": email,
        "username": "",
        "password": password,
        "agree": True,
        "agreePromotional": False,
        "dob": "",
        "captcha_token": turnstiletoken,
        "locale": "ja"
    }
    headers = {
        "Content-Type": "application/json",
        "x-xsrf-token": xsrf
    }
    r = s.post('https://api-id.streamlabs.com/v1/auth/register', headers=headers, json=payload)
    if r.status_code == 200:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET} {C["magenta"]}Account Created: {Fore.RESET}{C["gray"]}{email}:{password[:10]}.{Fore.RESET}{Fore.LIGHTCYAN_EX}**{Fore.RESET}{C["gray"]}{Fore.RESET}')
        Stats.created += 1
    else:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[~] Error Account Create: {r.json()}{Fore.RESET}')
        Stats.error += 1
        return

    time.sleep(4.7)
    code = getVerifyCode(token)
    payload2 = {
        "code": code,
        "email": email,
        "tfa_code": ""
    }
    r = s.post('https://api-id.streamlabs.com/v1/users/@me/email/verification/confirm', json=payload2)
    if r.status_code == 204:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["orange"]}[^] Email verified! - {Fore.RESET}{C["gray"]}{code}{Fore.RESET}')
    else:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[-] Error Verifying Email: {r.json()}{Fore.RESET}')
    r = s2.get('https://streamlabs.com/slid/login')
    xsrf2 = r.cookies.get('XSRF-TOKEN')
    cookies = '; '.join([f'{key}={value}' for key, value in r.cookies.items()])
    payload3 = {
        "email":email,
        "password":password
    }
    headers = {
        "cookie":cookies,
        "x-xsrf-token":xsrf2
    }
    r = s2.post('https://api-id.streamlabs.com/v1/auth/login',json=payload3,headers=headers)
    if r.status_code == 200:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["green"]}[*]{Fore.RESET} {C["aqua"]}Logged:{Fore.RESET}{C["gray"]}{r.cookies.get('access_token')[:40]}{Fore.RESET}.{Fore.LIGHTCYAN_EX}**{Fore.RESET}')
        with open("accounts.txt", "a") as f:
            f.write(f"{email}\n{password}\n{'; '.join([f'{key}={value}' for key, value in r.cookies.items()])}\n--------------------------------------\n")
    else:
        print(f'{C["gold"]}[{get_time_rn()}]{Fore.RESET} | {C["red"]}[-] Error Login:{r.json()}{Fore.RESET}')
if __name__ == "__main__":
    os.system("cls")
    threading.Thread(target=Console.title).start()
    while True:
        register()
