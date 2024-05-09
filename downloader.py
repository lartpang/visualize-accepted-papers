import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_papers_from_cvf(wd, save_dir):
    conf_infos = {
        "WACV2021": "https://openaccess.thecvf.com/WACV2021",
        "WACV2022": "https://openaccess.thecvf.com/WACV2022",
        "WACV2023": "https://openaccess.thecvf.com/WACV2023",
        "WACV2024": "https://openaccess.thecvf.com/WACV2024",
        #
        # "CVPR2021": "https://openaccess.thecvf.com/CVPR2021?day=all",
        # "CVPR2022": "https://openaccess.thecvf.com/CVPR2022?day=all",
        # "CVPR2023": "https://openaccess.thecvf.com/CVPR2023?day=all",
        #
        "ICCV2021": "https://openaccess.thecvf.com/ICCV2021?day=all",
        "ICCV2023": "https://openaccess.thecvf.com/ICCV2023?day=all",
    }

    for conf_name, conf_url in conf_infos.items():
        print(f"Name: {conf_name} Url: {conf_url}")

        wd.get(conf_url)
        titles = wd.find_elements(By.TAG_NAME, "dt")
        author_links = wd.find_elements(By.TAG_NAME, "dd")
        if conf_url.endswith("day=all"):
            author_links = author_links[1:-1]
        assert len(author_links) == 2 * len(titles)
        print("length of title: ", len(titles))

        paper_infos = []
        for i, title in enumerate(titles):
            authors = [e.text for e in author_links[2 * i].find_elements(By.TAG_NAME, "a")]
            links = [
                e.get_attribute("href")
                for e in author_links[2 * i + 1].find_elements(By.XPATH, './/a[not(parent::div[@class="link2"])]')
            ]
            info = (title.text, authors, links)

            print(f"[{i}/{len(titles)}] {info[0]}")
            paper_infos.append(info)
        print("The number of total accepted paper titles : ", len(paper_infos))

        with open(f"{save_dir}/{conf_name}-list.json", mode="w", encoding="utf-8") as f:
            json.dump(paper_infos, f, indent=2)


def get_papers_for_cvpr2024(wd, save_dir):
    conf_infos = {
        "CVPR2024": "https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers",
    }

    for conf_name, conf_url in conf_infos.items():
        print(f"Name: {conf_name} Url: {conf_url}")

        wd.get(conf_url)
        paper_rows = wd.find_elements(
            By.XPATH,
            "/html/body/main/div[2]/div/div/div/div/table/tbody/tr[position()>=3]/td[1]",
        )
        print("length of paper: ", len(paper_rows))

        paper_infos = []
        for i, paper_row in enumerate(paper_rows):
            title = paper_row.find_element(By.XPATH, ".//strong|.//a").text
            authors = [s.strip() for s in paper_row.find_element(By.TAG_NAME, "i").text.split("·")]
            info = (title, authors)

            print(f"[{i}/{len(paper_rows)}] {info[0]}")
            paper_infos.append(info)
        print("The number of total accepted paper titles : ", len(paper_infos))

        with open(f"{save_dir}/{conf_name}-list.json", mode="w", encoding="utf-8") as f:
            json.dump(paper_infos, f, indent=2)


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "disable-popup-blocking"])
    wd = webdriver.Chrome(options=chrome_options)

    save_dir = "./list"
    os.makedirs(save_dir, exist_ok=True)

    get_papers_from_cvf(wd, save_dir)
    get_papers_for_cvpr2024(wd, save_dir)

    wd.quit()


if __name__ == "__main__":
    main()
