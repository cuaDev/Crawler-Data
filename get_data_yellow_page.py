import requests
import math
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


class Crawler:
    def __init__(self, url, num_page):
        self.num_page = num_page
        self.url = url

    # Send request to website get HTML document
    def analyze_html(self):
        url_page = self.url + "?page=" + str(self.num_page)
        print(url_page)
        response = requests.get(url_page)
        html_content = response.content
        return BeautifulSoup(html_content, "lxml")


class Industry(Crawler):
    # Get a list of industries
    def get_industry_list(self):
        industry_list = []
        tags = self.analyze_html().find_all("p", {"class": "text-capitalize"})
        for tag in tags:
            get_href_industry = tag.find("a").get("href")
            get_total_company = tag.find("span").getText()[1:-1]

            industry_list.append([get_href_industry, get_total_company])
        return industry_list


class Company(Crawler):
    # Get list of industries
    def get_company_list(self):
        company_list = []
        tags = self.analyze_html().find_all("div", {"class": "yp_noidunglistings"})
        for tag in tags:
            # Get name company
            get_name_company = tag.find("h2").getText()

            # Get link to website
            a_tag = tag.find("a", {"class": "text-success"})
            if a_tag is not None:
                website_company = a_tag.get("href")
            else:
                website_company = "None"

            # Get authentication
            authen_tag = tag.find("span", {"class": "duocxacthuc"})
            if authen_tag is not None:
                get_authentication = authen_tag.getText()
            else:
                get_authentication = "Not Authentication"

            # Get contact

            get_contact = tag.find_all("div", {"class": "yp_div_logo_diachi clearfix"})
            if len(get_contact) != 0:
                p_tags = get_contact[0].find_all("p", {"class": "m-0"})

                match len(p_tags):
                    case 6:
                        logo = p_tags[0].get("src")
                        address = p_tags[1].getText()
                        phone_number = p_tags[2].getText() + p_tags[3].getText()
                        mail = p_tags[4].getText()
                        print(logo, address, phone_number, mail)

                    case 5, 4:
                        logo = p_tags[0].get("src")
                        address = p_tags[1].getText()
                        phone_number = p_tags[2].getText()
                        mail = p_tags[3].getText()
                        print(logo, address, phone_number, mail)

                    case 3:
                        logo = p_tags[0].get("src")
                        address = p_tags[1].getText()
                        phone_number = p_tags[2].getText()
                        mail = "None"
                        print(logo, address, phone_number, mail)

                # Get logo
                # get_logo = get_contact[0].find("img").get("src")

                # # Get contact
                # container_contact = get_contact[0].find(
                #     "div", {"class": "float-end yp_diachi_logo"}
                # )
                # address = container_contact

            # print(get_logo)

            # if len(get_contact) == 0:
            #     get_contact = tag.find_all("div", {"class": "h-auto clearfix mt-3"})
            #     # if len(get_contact) == 2:
            #     #     print("hi")
            #     #     address = (
            #     #         get_contact[0].getText() + get_contact[0].find("span").getText()
            #     #     )
            #     #     print(address)

            # Get address
            # address = get_contact[0].getText() + get_contact[0].find("span").getText()

            # # Get phone number
            # phone_number = contact[1].getText()

            # # Get mail
            # mail = contact[2].getText()

            # print(address)

            company_list.append(
                {
                    "Company": get_name_company,
                    "Website": website_company,
                    "Authentication": get_authentication,
                    # "Logo": get_logo
                    # "Address": address,
                }
            )
        return company_list


# Total page of yellow page

TOTAL_PAGE_NUMBER = 26

# Variable to save all company

total_company_number = []

# Export excel


def export_excel(data):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y-%H_%M_%S")
    # print(type(data))
    df = pd.DataFrame(data)
    df.to_excel("data-" + dt_string + ".xlsx")


for page_number in range(1, TOTAL_PAGE_NUMBER + 1):
    print("Pages:" + str(page_number))
    url_industry = Industry("https://yellowpages.vn/cate.asp", page_number)
    list_of_industries = url_industry.get_industry_list()
    for Industry in list_of_industries:
        # calculate page number
        total_page_industry = math.ceil(int(Industry[1]) / 45)
        for num_page_industry in range(1, total_page_industry + 1):
            company = Company(Industry[0], num_page_industry)
            total_company_number.extend(company.get_company_list())
            break
        break
    break
# export_excel(total_company_number)
