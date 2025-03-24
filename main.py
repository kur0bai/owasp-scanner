import argparse
import requests
import time
import threading
import sys
from colorama import Fore, Style
from bs4 import BeautifulSoup


class Spinner:
    """
    Function to show and hide spinner animation
    """

    def __init__(self, message="Loading"):
        self.spinner = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.message = message
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return  # avoid multiple threading

        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")
        sys.stdout.flush()

    def _animate(self):
        """execute spinner animation."""
        while self.running:
            for frame in self.spinner:
                if not self.running:
                    break
                sys.stdout.write(f"\r{self.message} {frame} ")
                sys.stdout.flush()
                time.sleep(0.1)  # speed


class Functions:
    def get_forms(self, url):
        """
        Easy way to get the forms from the target
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('form')

    def get_custom_payload(self):
        """
        First we try to get a custom payload provide by the user
        """
        response = input(
            Fore.CYAN + 'Do you have a custom payload? y/n: ' + Fore.WHITE)
        custom_payload = None
        if (response == 'yes' or response == 'y'):
            custom_payload = input(
                Fore.CYAN + 'Please, copy your payload here: ')
        else:
            print(Fore.YELLOW + 'Default payloads will be used for the test')
        return custom_payload

    def sqli_test(self, url):
        """
        SQL injection
        """
        custom_payload = self.get_custom_payload()
        sql_payloads = ["' OR '1'='1", "' UNION SELECT null, version() --"]
        results = []

        def send_payload(url, payload, results):
            test_url = f"{url}{'&' if '?' in url else '?'}id={payload}"

            try:
                response = requests.get(test_url)

                if "syntax error" in response.text.lower() or "mysql" in response.text.lower():
                    results.append(
                        Fore.GREEN + f'Possible SQL injection in {Fore.Red + test_url}, please check')

            except Exception as ex:
                print(Fore.Red + f'Something went wrong: {ex}')

        spinner = Spinner(Fore.CYAN + 'Starting SQL injection test')
        spinner.start()

        if custom_payload:
            send_payload(url=url, payload=custom_payload, results=results)
        else:
            for payload in sql_payloads:
                send_payload(url=url, payload=payload, results=results)

        spinner.stop()

        return results


def show_options():
    options_list = [
        '1 - SQL Injection',
        '2 - XSS Attack',
        '3 - Exit'
    ]
    print(Fore.CYAN + 'Web OWASP Scanner options:')
    for option in options_list:
        print(option)
    selected_option = int(input('Please, select and option: ' + Fore.WHITE))

    functions = Functions()

    match(selected_option):
        case 1:
            url = input(
                Fore.CYAN + 'Please, insert the target url: ' + Fore.WHITE)
            results = functions.sqli_test(url=url)
            print(Fore.GREEN + '---- SQL INJECTION RESULTS ----')
            for result in results:
                print(result)
        case 2:
            pass
        case 3:
            pass


def show_banner():
    banner = [
        Fore.GREEN + "---------------------------------------------------------------------------------------------------------------",
        Fore.GREEN + r"██████╗ ██╗    ██╗ █████╗ ███████╗██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗",
        Fore.GREEN + r"██╔═══██╗██║    ██║██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗",
        Fore.GREEN + r"██║   ██║██║ █╗ ██║███████║███████╗██████╔╝    ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝",
        Fore.CYAN + r"██║   ██║██║███╗██║██╔══██║╚════██║██╔═══╝     ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗",
        Fore.CYAN + r"╚██████╔╝╚███╔███╔╝██║  ██║███████║██║         ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║",
        Fore.CYAN + r"╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝         ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝",
        Fore.GREEN + "---------------------------------------------- + By: Kur0bai + ------------------------------------------------"
    ]

    for line in banner:
        print(line)


def main():
    parser = argparse.ArgumentParser(
        description="OWASP vulnerabilities Scanner")
    parser.add_argument('url', help="Web target URL to scan")
    args = parser.parse_args()


if __name__ == '__main__':
    show_banner()
    show_options()
    # main()
