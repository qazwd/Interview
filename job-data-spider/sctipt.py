import requests
from bs4 import BeautifulSoup
import csv

# 基础 URL
base_url = "https://pultegroup.wd1.myworkdayjobs.com/PGI"
# 请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

def get_job_listings(url):
    """
    从指定 URL 获取职位列表信息
    :param url: 职位列表页面的 URL
    :return: 职位列表信息和下一页的 URL
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = []
        # 查找所有职位信息
        jobs = soup.find_all('li', class_='css-13dcyxf')
        for job in jobs:
            title = job.find('a', class_='css-1422juy').text.strip()
            location = job.find('div', class_='css-1lh32fc').text.strip()
            job_url = base_url + job.find('a', class_='css-1422juy')['href']
            job_listings.append({
                'Title': title,
                'Location': location,
                'URL': job_url
            })
        # 查找下一页链接
        next_page = soup.find('a', {'aria-label': 'Next'})
        if next_page:
            next_page_url = base_url + next_page['href']
        else:
            next_page_url = None
        return job_listings, next_page_url
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return [], None

def save_to_csv(data, filename):
    """
    将职位数据保存到 CSV 文件
    :param data: 职位数据列表
    :param filename: 保存的 CSV 文件名
    """
    if data:
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"数据已保存到 {filename}")
    else:
        print("没有数据可保存。")

def main():
    all_jobs = []
    current_url = base_url
    while current_url:
        job_listings, next_page_url = get_job_listings(current_url)
        all_jobs.extend(job_listings)
        current_url = next_page_url
    save_to_csv(all_jobs, 'job_listings.csv')

if __name__ == "__main__":
    main()
