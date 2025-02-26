from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import Config


def fetch_status(dr, url, username, password):
    dr.get(url)
    time.sleep(5)
    dr.find_element(By.ID, "iptUserName").send_keys(username)
    dr.find_element(By.ID, "iptPassword").send_keys(password)
    dr.find_element(By.ID, "btnLogin").click()
    time.sleep(10)
    status = dr.find_element(By.ID, "alarm").text.replace("\n", ",")
    return status


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    dr = webdriver.Chrome(options=options)
    dr.implicitly_wait(10)

    with open("output.csv", "w") as f:
        f.write("URL,Critical,Major,Minor\n")
        for url, creds in Config.IBMC_URL.items():
            try:
                status = fetch_status(dr, url, creds["username"], creds["password"])
                f.write(f"{url},{status}\n")
            except Exception as e:
                print(f"Error: {e}")
                f.write(f"{url},Error\n")
    dr.quit()
