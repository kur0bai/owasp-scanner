import argparse
import requests
from colorama import Fore, Style
from bs4 import BeautifulSoup


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
        print(Fore.CYAN + 'Do you have a custom payload? y/n ')
        response = input()
        custom_payload = None
        if (response == 'yes' or response == 'y'):
            custom_payload = input(
                Fore.CYAN + 'Please, copy your payload here: ')
        else:
            print(Fore.YELLOW + 'Default payloads will be used for the test')
        return custom_payload

    def sqli_test(self, url):
        custom_payload = self.get_custom_payload()
        sql_payloads = ["' OR '1'='1", "' UNION SELECT null, version() --"]
        results = []

        if custom_payload:
            pass

        for payload in sql_payloads:
            test_url = f"{url}{'&' if '?' in url else '?'}id={payload}"
            response = requests.get(test_url)


def show_options():
    options_list = [
        '1 - SQL Injection',
        '2 - XSS Attack',
        '3 - Exit'
    ]
    print(Fore.CYAN + 'Please, select and option to start:')
    for option in options_list:
        print(option)
    selected_option = int(input())

    functions = Functions()

    match(selected_option):
        case 1:
            url = input(Fore.CYAN + 'Please, insert the target url')
            functions.sqli_test(url=url)
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
